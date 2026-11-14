// The narrator's scheduler: decides which line to play and when. Deterministic for a given
// seed, no dependencies, no knowledge of the game's engine or user interface.
//
// Rules (docs/game-integration-plan.md):
// - a cue may play during a difficult moment, at most one every `cueGap` seconds;
// - story and place lines play only when it is calm; a line is never cut;
// - a reflection plays in the first calm moment after a difficulty, or is dropped after 20 s;
// - a cue that asks for an action (`expects`) is answered with a short acknowledgement when the
//   player does it within `within` seconds ("Isso!"); no nagging if they do not;
// - after a random 10–20 s of calm without talk, the story continues (leg and idle lines, in
//   order); when the story has nothing left, a trivia line (boats, region, fish, jobs) plays;
// - place lines play once per run; curiosity lines go to the end-of-mission logbook;
// - each beat plays one of its candidate lines once; lines that miss their window are dropped.

import type { BankLine, LineBank } from "./bank.js";

export interface NarratorOptions {
  /** seed of the random choices (idle gaps, candidate lines, trivia order) */
  seed?: number;
  /** seconds of calm without talk before the story continues: random in [min, max] */
  idleMin?: number;
  idleMax?: number;
  /** difficulty below which it counts as calm (0 to 1) */
  calmBelow?: number;
  cueGap?: number;
  reflectionWait?: number;
  /** default seconds to wait for an expected action after a cue */
  ackWindow?: number;
  /** also play lines that passed the checks but are not approved (playtest) */
  includeVerified?: boolean;
  lang?: string;
  /** the option the game drew: boat, area, places */
  context?: { boat?: string; area?: string; places?: string[] };
  /** reading speed for lines without audio */
  wordsPerSecond?: number;
}

export interface Frame {
  /** game moments that happened since the last frame (tack, sheet_in, near_place:Seixal…) */
  events?: string[];
  /** 0 calm … 1 hardest */
  difficulty: number;
}

export interface Play {
  line: BankLine;
  speaker: string;
  text: string;
  start: number;
  seconds: number;
  /** why it played: the event, "ack", "idle" or "reflection" */
  reason: string;
}

/** Small seeded generator (mulberry32). */
function rng(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const beatOf = (l: BankLine) => l.id.split(".").slice(0, -1).join(".") || l.id;

export class Narrator {
  readonly logbook: BankLine[] = [];
  readonly played: Play[] = [];
  private readonly o: Required<Omit<NarratorOptions, "context">> & { context: NarratorOptions["context"] };
  private readonly rand: () => number;
  private readonly lines: BankLine[];
  private readonly doneBeats = new Set<string>();
  private readonly usedIds = new Set<string>();
  private readonly names: Record<string, string>;
  private speakingUntil = -Infinity;
  private lastCue = -Infinity;
  private calmSince = 0;
  private idleNeed: number;
  private pendingReflection: { lines: BankLine[]; until: number; reason: string } | null = null;
  private expecting: { events: Set<string>; until: number; speaker: string } | null = null;
  private pendingAck: { speaker: string; until: number } | null = null;
  private trivia: BankLine[];
  private lastAck = "";

  constructor(bank: LineBank, options: NarratorOptions = {}) {
    this.o = {
      seed: 1, idleMin: 10, idleMax: 20, calmBelow: 0.4, cueGap: 8, reflectionWait: 20, ackWindow: 15,
      includeVerified: false, lang: "pt", wordsPerSecond: 2.5, ...options, context: options.context,
    };
    this.rand = rng(this.o.seed);
    const ok = (l: BankLine) => l.status === "approved" || (this.o.includeVerified && l.status === "verified");
    this.lines = bank.lines.filter((l) => ok(l) && this.fits(l));
    this.names = Object.fromEntries(bank.cast.map((c) => [c.id, c.name[this.o.lang] ?? Object.values(c.name)[0] ?? c.id]));
    this.trivia = this.shuffle(this.lines.filter((l) => l.delivery === "trivia"));
    this.idleNeed = this.drawIdle();
  }

  /** Call once per frame with the time in seconds since the mission started. */
  update(t: number, frame: Frame): Play[] {
    const out: Play[] = [];
    const calm = frame.difficulty < this.o.calmBelow;
    const events = frame.events ?? [];

    // 1. the player did what a cue asked: acknowledge (short, allowed during difficulty)
    if (this.expecting && t > this.expecting.until) this.expecting = null;
    if (this.expecting && events.some((e) => this.expecting!.events.has(e))) {
      this.pendingAck = { speaker: this.expecting.speaker, until: t + 3 };
      this.expecting = null;
    }
    if (this.pendingAck && t > this.pendingAck.until) this.pendingAck = null;
    if (this.pendingAck && t >= this.speakingUntil) {
      const ack = this.pickAck(this.pendingAck.speaker);
      this.pendingAck = null;
      if (ack) out.push(this.say(ack, t, "ack", false));
    }

    // 2. lines triggered by this frame's events
    for (const e of events) {
      const cands = this.lines.filter((l) => l.trigger === e && l.delivery !== "ack" && !this.doneBeats.has(beatOf(l)));
      for (const beat of [...new Set(cands.map(beatOf))]) {
        const group = cands.filter((l) => beatOf(l) === beat);
        const first = group[0]!;
        if (first.delivery === "curiosity") { this.logbook.push(this.choose(group)); this.doneBeats.add(beat); continue; }
        if (first.delivery === "reflection") { this.pendingReflection = { lines: group, until: t + this.o.reflectionWait, reason: e }; continue; }
        if (first.delivery === "leg" || first.delivery === "trivia") continue; // played in quiet moments
        if (t < this.speakingUntil) continue; // never cut a line; a missed window is dropped
        if (first.delivery === "cue") {
          if (t - this.lastCue < this.o.cueGap) continue;
          const line = this.choose(group);
          out.push(this.say(line, t, e, true));
          this.lastCue = t;
          if (line.expects?.length) this.expecting = { events: new Set(line.expects), until: t + (line.within ?? this.o.ackWindow), speaker: line.speaker };
          continue;
        }
        if (!calm) continue; // story and place lines need calm
        out.push(this.say(this.choose(group), t, e, true));
      }
    }

    // 3. a reflection right after the difficulty ends
    if (this.pendingReflection) {
      if (t > this.pendingReflection.until) this.pendingReflection = null;
      else if (calm && t >= this.speakingUntil) {
        const r = this.pendingReflection; this.pendingReflection = null;
        out.push(this.say(this.choose(r.lines), t, "reflection", true));
      }
    }

    // 4. quiet moments: after a random 10–20 s of calm without talk, continue the story or tell trivia
    if (!calm || t < this.speakingUntil) this.calmSince = Math.max(t, this.speakingUntil);
    if (calm && t >= this.speakingUntil && t - this.calmSince >= this.idleNeed && !out.length) {
      const story = this.lines.filter((l) => (l.delivery === "leg" || l.trigger === "idle") && l.delivery !== "trivia" && !this.usedIds.has(l.id));
      const next = story[0] ?? this.trivia.find((l) => !this.usedIds.has(l.id));
      if (next) out.push(this.say(next, t, "idle", false));
      else this.calmSince = t; // nothing left to say: stay quiet
    }
    return out;
  }

  private say(line: BankLine, t: number, reason: string, wholeBeat: boolean): Play {
    if (wholeBeat) this.doneBeats.add(beatOf(line));
    this.usedIds.add(line.id);
    const text = line.text[this.o.lang] ?? line.text.pt ?? Object.values(line.text)[0] ?? "";
    const audio = line.audio?.[this.o.lang]?.seconds;
    const seconds = audio ?? text.split(/\s+/).filter(Boolean).length / this.o.wordsPerSecond + 1.5;
    this.speakingUntil = t + seconds;
    this.calmSince = this.speakingUntil;
    this.idleNeed = this.drawIdle();
    const play = { line, speaker: this.names[line.speaker] ?? line.speaker, text, start: t, seconds, reason };
    this.played.push(play);
    return play;
  }

  private pickAck(speaker: string): BankLine | undefined {
    const acks = this.lines.filter((l) => l.delivery === "ack");
    const own = acks.filter((l) => l.speaker === speaker);
    const pool = (own.length ? own : acks).filter((l) => l.id !== this.lastAck);
    const ack = pool.length ? pool[Math.floor(this.rand() * pool.length)] : acks[0];
    if (ack) this.lastAck = ack.id;
    return ack;
  }

  private choose(group: BankLine[]): BankLine {
    return group[Math.floor(this.rand() * group.length)] ?? group[0]!;
  }

  private shuffle<T>(xs: T[]): T[] {
    const a = xs.slice();
    for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(this.rand() * (i + 1)); [a[i], a[j]] = [a[j]!, a[i]!]; }
    return a;
  }

  private drawIdle(): number {
    return this.o.idleMin + this.rand() * (this.o.idleMax - this.o.idleMin);
  }

  private fits(l: BankLine): boolean {
    const w = l.when, c = this.o.context;
    if (!w || !c) return true;
    if (w.boats?.length && c.boat && !w.boats.includes(c.boat)) return false;
    if (w.areas?.length && c.area && !w.areas.includes(c.area)) return false;
    if (w.places?.length && c.places?.length && !w.places.some((p) => c.places!.includes(p))) return false;
    return true;
  }
}
