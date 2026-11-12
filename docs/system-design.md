# System design: five components

Draft, 2026-11-12. Revises the kit (CLAUDE.md and prompts 01 to 08) around five components.

Scope: this repository builds a **tool** for authors. The tool bootstraps drafts (concepts,
sources, missions) from the game and the documents, the author curates them, and the tool then
helps write, ground, verify, review and export lines, and schedules them at runtime. The tool
does not ship narrative of its own: every list and line it proposes is a draft until a person
accepts it.

```
 (1) Game physics model ──► (2) Concepts ◄── curated by a sailor / Museu de Marinha
        │  signals, events,        │
        │  challenge               │                (3) Sources (database)
        ▼                          ▼                         │
 (5) Runtime: observe ──► challenge-aware ◄── line bank ◄── generate + verify + review
     each physics step     scheduler                 ▲
                                                     │
                               (4) Missions and general concepts (bootstrap)
```

## Which game

The physics reference is the web game `TagusNavyVirtualMuseum/fragateiro` (TypeScript, Babylon.js),
the successor to the Unity simulator (Fazenda et al., 2025) embedded on the
TagusNavyVirtualMuseum site. Its physics (`src/physics/`) is plain TypeScript with no 3D or
browser code, so our runtime can read the same state the game computes. We do not modify the
game; integration later is one call per physics step (see component 5). A C# description of
the runtime stays in scope for the Unity build.

## 1. Understanding the game physics

File: `knowledge/game-physics.yaml`.

What the simulator exposes each step (from `src/physics/types.ts` and `simulator.ts`):
boat state (position, heading, surge u, sway v, yaw rate, heel), controls (rudder, sheets per
sail group, mode), and a force report (true and apparent wind angle and speed, per-sail angle
of attack and luffing, heel moment). The mission layer adds aground, collisions, distances to
targets, other boats, whale state, timers. `SailboatSim.bestSheets()` gives the ideal trim, so
trim error is measurable.

From these we derive:

- quantities: point of sail, tack side, luffing fraction, trim error, heel ratio (to the 30°
  capsize), leeway angle, velocity made good, steerage way;
- events (the trigger vocabulary): tack, gybe, controlled or uncontrolled gybe, enter and leave
  irons, luffing starts and stops, heel warning, gust, wind shift, aground, collision, near
  vessel, approach target, arrive;
- a challenge level in [0, 1] (component 5).

The game models wind only (steady or gusty with shifts). It has no current or tide, so tide and
current are general (heritage) concepts here, not physics concepts, until the game adds them.

## 2. Concepts to learn, bootstrapped from the physics and curated

File: `knowledge/concepts.yaml`.

Each sailing concept is tied to the physics: which signals show it, how the game can tell
mastery from struggle (evidence), prerequisites, boats where it matters, and PT/EN/FR terms.
Example: *caçar / folgar* is evidenced by trim error and luffing fraction; struggle is luffing
above 50 % for 5 s while the heading is steady.

Tool step `bootstrap concepts` proposes the list from three inputs: the physics model
(component 1: each derived quantity and event suggests a concept and its evidence), the
author's documents (for example the method doc's concept table), and the game's drills. Each
proposal says which input it came from. Every entry starts as `status: draft`; the author
accepts, edits, merges or rejects it in the review tool, and it becomes `curated`. Terms the
inputs mark [to confirm] stay flagged.

General (heritage) concepts live in the same file under `kind: heritage`, with no physics
signals; the tool proposes them from the source registry (component 3) by theme, and the author
curates them. They are what the story lines carry; the sailing concepts are what the player
does.

## 3. Sources as the database

File: `knowledge/sources.yaml` (registry), then `corpus/chunks.jsonl` (prompt 02).

One entry per source: type, URL, licence, reliability A/B/C, what to use it for, cautions, and
whether it has been read, partly read, or could not be fetched. The tool can seed the registry
by parsing a source table in the author's documents (the method doc has one); the author sets
reliability and licence. The game's physics documentation is a source for the sailing
concepts. Retrieval and verification only ever cite chunks from registered sources.

## 4. Bootstrap of missions and general concepts

File: `story/missions-bootstrap.yaml`.

Tool step `bootstrap missions` reads the game's mission definitions (in fragateiro:
`content/minigames.json` and `src/world/missions.ts`, five drills and eight mini-games) and
writes one skeleton per mission: boat, place, goal, phases (start, legs, manoeuvres, approach,
finish) with the challenge expected in each, the sailing concepts the mission exercises
(matched from component 2), and empty slots for the author's cast, arc and beats. It writes no
story text. Missions that already have an authored arc (the story bible's Catraio and
Baleeiro) are merged in, not overwritten.

## 5. Mixing narrative into play, by challenge

Rule: do not talk while the player is in a difficult moment. Speak in the calm stretches, and
talk about a difficulty after it is over.

The runtime observes every physics step and keeps a challenge level from these factors, taking
the largest (one hard thing is enough to make a moment hard):

| Factor | Signal | Load |
| --- | --- | --- |
| Manoeuvre in progress | wind within 20° of the bow or stern while turning (tack, gybe) | 0.9 |
| In irons | sails luffing, under 0.5 m/s, wind inside the no-go zone | 0.8 |
| Heel | heel / capsize angle above 0.6 | 0.6 to 1.0 |
| Close quarters | land, another boat or a target (dock, buoy, whale, boat alongside) within a few boat lengths, or time to contact under 15 s | 0.7 to 0.9 |
| Gust or shift | wind speed up 30 % or direction moved 10° in the last 5 s | 0.5 |
| Busy hands | rudder and sheet changes per second above a threshold | 0.5 |
| Time pressure | last 15 s of a timed task | 0.6 |

The level rises at once and falls slowly (about 3 s), so a line never starts in the second
after a manoeuvre. A calm window is load under 0.3 for 2 s, on a steady heading, with no target
closer than the time the line takes to read.

Lines get a delivery class (new optional fields in the line schema):

| Delivery | What | When it may play | Limits |
| --- | --- | --- | --- |
| `cue` | instruction, at most 6 words ("Folga a escota!") | up to load 0.8, only for the concept the player is failing at that moment | one per 8 s; never history |
| `story` | the character's line for a beat (depth 1) | calm window only | must fit the window; drops after `ttl_s` |
| `reflection` | about what just happened ("That's how you get out of irons") | first calm window after the difficulty ends | high priority, short ttl (about 20 s) |
| `curiosity` | depth-2 card | paused, mission end, or a long calm leg, on request | never interrupts |

A line already showing is never cut. Lines that miss their window are dropped, not queued
forever, so the story does not lag behind the sailing.

For authors this means a beat is tied to the moment after a difficulty, not during it: the
story validator warns when a `story` line is triggered by an event that is itself high-load
(for example `enter_irons`) and suggests the matching resolution event (`out_of_irons`). The
story bible's Catraio turn beat is such a case. Talking right after the player solves a problem
is also a good moment for learning, and the study can test it (talk-anytime versus
challenge-aware timing).

## What changes in the kit

- CLAUDE.md: the five components and the game reference.
- Line schema: optional `delivery`, `max_load`, `ttl_s` (backward compatible).
- New tool steps: `bootstrap concepts`, `bootstrap sources`, `bootstrap missions`, each writing
  drafts for the author to curate, plus the physics observer.
- Prompt 04: missions start from `story/missions-bootstrap.yaml`; beats name the phase and use
  the event vocabulary in `knowledge/game-physics.yaml`.
- Prompt 07: the selector becomes a challenge-aware scheduler on top of the observer.
- Prompt 08: add a timing condition to the study (anytime versus challenge-aware).

## Open questions

- Is fragateiro (web) the target for the first study, with Unity later, or the reverse?
- Thresholds (36° no-go, 0.3 calm, 3 s decay) are first guesses from the physics; tune them with
  recorded play sessions.
- Text only (toasts) or voice? Voice changes how long a line occupies the window.
- Who curates the concepts and PT terms (a sailor, the Museu de Marinha)?
