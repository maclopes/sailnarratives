# Plan: playing the narrative in the game, with optional speech

Draft, 2026-11-13. Target: the fragateiro web game (TypeScript, Babylon.js). No change to the game
is made until this plan is agreed.

## Principles

- The game never calls an LLM. It reads a reviewed line bank (files) and a small runtime
  decides what to say and when.
- The game keeps its physics and mission code. Narration is a separate module with a few
  hooks, behind a setting, so it can be switched off.
- Text is always shown (museums are noisy); speech is optional and pre-generated.
- Content stays editable without code, like the game's `content/texts` and
  `content/minigames.json`.

## The pieces

```
sailnarratives (the tool)                     fragateiro (the game)
  Narrative tab ── export ──► line bank files ──► content/narrative/<mini-game>.json
  voice step (later) ──────► audio files ─────► content/narrative/audio/<lang>/<line>.ogg
  runtime/ (TypeScript, no dependencies) ──────► imported by games/sailing/main.ts
      observer: physics → game moments + difficulty
      scheduler: which line, when, by whom
```

### 1. Line bank files (content)

One JSON file per mini-game and narrator variant, written by the tool's export:
`content/narrative/<mini-game>.<variant>.json` (variant: `historical-1925`, `guide`), plus
`content/narrative/index.json` listing them. Each line: id, beat part, trigger (a game moment,
or `near_place:<name>`), delivery (cue, story, reflection, curiosity, leg pool), character,
text per language (pt, en; fr later), optional audio per language with its duration, fictional
flag, evidence ids, and a credits list of sources. The game's tests check that every trigger is
a known game moment, every place exists on the map, and every language has the same keys, as
they already do for texts and mini-games.

### Mini-games with options (several boats or places)

The game's `content/minigames.json` can list several boats and places for one mini-game and draws
one each time. Lines therefore carry optional conditions, and come in three layers:

- **General lines:** the task and the sailing; no conditions; valid in every option.
- **Option lines:** `when: {boats: [...], areas: [...], places: [...]}`; the cast and the story
  of one boat or area (a Tagus catraeiro is not a middle-Tagus barqueiro).
- **Place lines:** triggered by `near_place:<name>`, so they play only where the boat really is.

At mission start the game passes the drawn boat and place to the narrator, which keeps the
general lines and those whose conditions match. In the tool, each mini-game's options (boat ×
place) can be planned separately or share one cast; the export merges them into one file and runs
a coverage check (each option needs at least a setup and a close line). An option without lines
(for example a place added to the game later) falls back to the general lines, never to lines
written for another boat or place.

### 2. Runtime (built in this repository, imported by the game)

- **Observer:** the parked draft (`domains/sailing/adapter/observer`), split into a generic
  engine in `runtime/` and the sailing rules in the pack. Fed once per frame with the boat
  state and the mission context; emits game moments (tack, gybe, in irons, steady leg, gust,
  near vessel, arrival…) and a difficulty level 0 to 1 with calm windows.
- **Scheduler:** applies the delivery rules from the design:
  - a cue may play during difficulty, at most one every 8 s;
  - story lines play only in calm windows, and a line is never cut;
  - a reflection plays in the first calm window after a difficulty, or expires after 20 s;
  - leg pools play in turn on steady legs, without repeats;
  - place lines play once per run;
  - curiosity cards go to an end-of-mission logbook;
  - lines that miss their window are dropped, not queued.

  It is deterministic for a given seed, and has no dependencies.
- **Speaker interface:** `show(line, lang)` for captions and `play(audio)` for speech, so the
  game provides the user interface and the runtime stays independent of Babylon.js and the DOM.

### 3. Hooks in the game (small, in `games/sailing/main.ts`)

| Where | What |
| --- | --- |
| `startMission` / `finishMission` | `narrator.start(miniGame, variant, getLang())` / `narrator.end()` (shows the logbook) |
| render loop, after `stepWithLand` | `narrator.update(fromSim(sim, context))`, with the context: aground, collision, distance to the target, time left, arrival |
| existing mission events (whale fright and close, catch, supply loaded, drill tack and gybe, collision) | pass them as `context.events`, next to the existing toasts |
| a place watcher (new, small) | emits `near_place:<name>` once per pass, from the map's named places and landmarks within a few hundred metres |
| settings panel | narration on or off, narrator (historical or guide), talk (quiet, normal, chatty), voice on or off, captions size |

### 4. On screen

A caption area separate from the toasts: the speaker's name and the line, placed so it never
covers the instruments, shown for the reading time (or the audio length). Cues get a short,
plain style; story lines a speech-bubble style. Curiosity cards appear in the end-of-mission
screen as a logbook, with the sources named.

## Speech

| Option | For | Against |
| --- | --- | --- |
| A. Recorded voices (actors) | Best quality, real Lisbon and Tagus accents | Cost; re-recording after every edit |
| B. Text to speech generated offline by the tool, shipped as audio files | Works offline in the museum; one voice per character; the exact length is known for timing; regenerated in minutes after edits | Synthetic voice; needs a good European Portuguese voice |
| C. The browser's own speech synthesis at runtime | No files, no cost | European Portuguese voices often missing (Brazilian instead), varies per device, no control per character |

Recommendation: B for the line bank, with A for a few key lines if the museum wants it, and C
only as a fallback for the home edition when audio files are missing.

- **In the tool:** a Voice step assigns a voice to each character and generates one file per
  line and language (small compressed files, tens of kilobytes each). The line bank stores each
  file's path and duration, and the scheduler uses that duration instead of reading time. The
  generation runs on the better computer, with a local text-to-speech engine that has a
  European Portuguese voice (to be chosen and listened to), so no text leaves the machine. In
  the workbench, a Listen button can preview lines with Claude's voices before files exist.
- **In the game:** an audio player beside the existing synthesised sound. It lowers wind and
  water while a line plays, keeps one voice at a time, has a voice on/off switch, and always
  keeps captions on. In the museum, voice suits headphones or a handset; with open speakers,
  text only.

## Testing

- Runtime: unit tests (vitest) and scripted sails run on the game's own physics (vendored),
  checking that the scheduler never talks during a manoeuvre, never repeats, and respects
  cooldowns.
- Tool: a Playtest view replays a scripted sail with a mini-game's lines and shows what played
  when, what waited and what was dropped.
- Game: content tests for the line bank files; a hidden debug view of the narrator's queue.
- Museum: a pilot with visitors, then the study conditions (story arcs against fact cards; talk
  anytime against challenge-aware timing).

## Phases

1. **Runtime:** the observer split into engine and sailing rules, the scheduler, and tests with
   scripted sails. In this repository.
2. **Export v1 and Playtest:** a stable line bank format, a validator, and the Playtest view in
   the workbench, with a Listen preview.
3. **Game integration behind a setting** (`?narrative=on`), for one mini-game first (Passengers
   with the Catraio): captions, hooks, place watcher, logbook. This is a change to fragateiro,
   made only when you decide, either by its developers or as a pull request for their review.
4. **Speech:** voice assignment and offline audio generation in the tool, and the game's audio
   player with ducking.
5. **All Tagus mini-games, museum pilot, study.**

## Open questions

- Who changes fragateiro: its developers following this plan, or a pull request from this
  project for them to review?
- Museum hardware: open speakers, headphones or handsets? This decides whether voice is on by
  default.
- French: translate the line bank now or later?
- Narrator per edition: historical in the museum, present-day guide at home, or a choice?
- The game has new areas and lighthouses since the tool's world list was built; rebuild it
  before the next game report.
