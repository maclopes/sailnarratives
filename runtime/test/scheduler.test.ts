import { describe, expect, it } from "vitest";
import { Narrator } from "../src/scheduler.js";
import type { BankLine, LineBank } from "../src/bank.js";

const L = (id: string, trigger: string, delivery: BankLine["delivery"], pt: string, extra: Partial<BankLine> = {}): BankLine =>
  ({ id, trigger, delivery, speaker: "k1", text: { pt, en: pt }, status: "approved", ...extra });

const bank = (lines: BankLine[]): LineBank => ({ version: 1, minigame: "x", variant: "historical", languages: ["pt", "en"],
  cast: [{ id: "k1", name: { pt: "Arrais", en: "Skipper" } }], lines });

/** Run the narrator over a timeline at 10 frames per second. */
function run(n: Narrator, until: number, at: (t: number) => { events?: string[]; difficulty?: number } = () => ({})) {
  const plays = [];
  for (let i = 0; i <= until * 10; i++) {
    const t = i / 10, f = at(t);
    plays.push(...n.update(t, { events: f.events, difficulty: f.difficulty ?? 0 }));
  }
  return plays;
}

describe("Narrator", () => {
  it("acknowledges when the player does what a cue asked, and only then", () => {
    const b = bank([L("x.b1.l1", "luffing_start", "cue", "Caça a escota!", { expects: ["sheet_in", "trim_good"] }),
      L("x.ack.l1", "ack", "ack", "Isso!"), L("x.ack.l2", "ack", "ack", "Boa!")]);
    const done = run(new Narrator(b, { idleMin: 999, idleMax: 999 }), 20, (t) => ({ events: t === 2 ? ["luffing_start"] : t === 6 ? ["sheet_in"] : [] }));
    expect(done.map((p) => p.reason)).toEqual(["luffing_start", "ack"]);
    expect(done[1]!.start).toBeGreaterThanOrEqual(6);
    const notDone = run(new Narrator(b, { idleMin: 999, idleMax: 999 }), 40, (t) => ({ events: t === 2 ? ["luffing_start"] : t === 30 ? ["sheet_in"] : [] }));
    expect(notDone.map((p) => p.reason)).toEqual(["luffing_start"]); // too late: no ack, no nagging
  });

  it("acknowledges during a difficult moment, but waits for the cue to finish", () => {
    const b = bank([L("x.b1.l1", "enter_irons", "cue", "Leme a um bordo, cai!", { expects: ["out_of_irons"] }), L("x.ack.l1", "ack", "ack", "Isso!")]);
    const plays = run(new Narrator(b, { idleMin: 999, idleMax: 999 }), 10, (t) => ({ difficulty: 0.9, events: t === 1 ? ["enter_irons"] : t === 1.5 ? ["out_of_irons"] : [] }));
    expect(plays.map((p) => p.reason)).toEqual(["enter_irons", "ack"]);
    expect(plays[1]!.start).toBeGreaterThanOrEqual(plays[0]!.start + plays[0]!.seconds - 0.1);
  });

  it("continues the story after 10–20 s of calm, then tells trivia, never repeating", () => {
    const b = bank([L("x.b2.l1", "steady_leg", "leg", "Primeira parte da história."), L("x.b2.l2", "steady_leg", "leg", "Segunda parte."),
      L("x.t.l1", "idle", "trivia", "A muleta pescava de lado.", { topic: "boat" }), L("x.t.l2", "idle", "trivia", "O Seixal tinha estaleiros.", { topic: "place" })]);
    const plays = run(new Narrator(b, { seed: 7 }), 200);
    expect(plays.map((p) => p.line.id).slice(0, 2)).toEqual(["x.b2.l1", "x.b2.l2"]);
    expect(plays.slice(2).map((p) => p.line.delivery)).toEqual(["trivia", "trivia"]);
    expect(new Set(plays.map((p) => p.line.id)).size).toBe(plays.length);
    let end = 0;
    for (const p of plays) { const gap = p.start - end; expect(gap).toBeGreaterThanOrEqual(10 - 0.11); expect(gap).toBeLessThanOrEqual(20 + 0.11); end = p.start + p.seconds; }
  });

  it("never talks in quiet moments while it is hard, and resets the wait after", () => {
    const b = bank([L("x.t.l1", "idle", "trivia", "Uma curiosidade.")]);
    const plays = run(new Narrator(b, { seed: 3 }), 60, (t) => ({ difficulty: t < 40 ? 0.8 : 0 }));
    expect(plays).toHaveLength(1);
    expect(plays[0]!.start).toBeGreaterThanOrEqual(50 - 0.11);
  });

  it("drops a story line that comes during difficulty, keeps a reflection for after", () => {
    const b = bank([L("x.b1.l1", "tack", "story", "Uma história."), L("x.b2.l1", "tack", "reflection", "Bem virado.")]);
    const plays = run(new Narrator(b, { idleMin: 999, idleMax: 999 }), 30, (t) => ({ difficulty: t < 5 ? 0.9 : 0, events: t === 2 ? ["tack"] : [] }));
    expect(plays.map((p) => p.line.id)).toEqual(["x.b2.l1"]);
    expect(plays[0]!.start).toBeGreaterThanOrEqual(5);
  });

  it("plays verified lines only in playtest mode, and respects the option drawn", () => {
    const b = bank([L("x.b1.l1", "start", "story", "Verificada.", { status: "verified" }),
      L("x.b2.l1", "start", "story", "Só no catraio.", { when: { boats: ["catraio"] } })]);
    expect(run(new Narrator(b, { context: { boat: "falua" } }), 1, (t) => ({ events: t === 0 ? ["start"] : [] }))).toHaveLength(0);
    expect(run(new Narrator(b, { includeVerified: true, context: { boat: "catraio" } }), 1, (t) => ({ events: t === 0 ? ["start"] : [] }))).toHaveLength(1);
  });
});
