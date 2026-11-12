# System design

Draft 3, 2026-11-12. A generic tool with domain packs; sailing on the Tagus is the first pack.
The tool proposes drafts and one author curates them. It writes no story of its own.

## What the tool does

It helps an author build short, grounded narrative for a simulation-based learning game, for
museums. It starts from three kinds of evidence, links them, proposes situations where all three
agree, and reports what is missing or contradictory. From situations it derives activity
proposals, story beats and lines, and at runtime it times lines by how hard the moment is.

Nothing in the tool is specific to one subject. Everything specific lives in a domain pack.

## Generic tool and domain pack

| Part | Generic tool | Supplied by the domain pack |
| --- | --- | --- |
| Simulation base | Adapter interface; a rule engine that turns named signals into derived quantities, events and a difficulty level; a scenario runner | The adapter for its simulation, the vocabulary (signals, quantities, events, difficulty factors) and thresholds, the simulation's known limits |
| Concepts base | Concept schema (terms per language, kind, prerequisites, evidence rules over events), proposal and curation | Reference books, the concept kinds it uses |
| History base | Practice schema (actor, object, place, period, conditions, actions, quantities) with evidence passages; extraction and curation | The sources |
| Links, situations, questions | All generic | Nothing |
| Runtime | A scheduler that plays lines by difficulty and calm windows | Thresholds tuned for the domain |
| Interface | Generic screens | Optional views (for sailing: polar diagram, boat track) |
| Author documents | Read as inputs or held out | The documents themselves |

A pack is a folder under `domains/` with a manifest, `domain.yaml`. Test of generality: a second
domain (for example a historical mill or a steam engine simulation) should need only a new pack,
with no change to the tool. We will not build it now, but each design choice should pass that
thought experiment.

## 1. Three knowledge bases

| Base | Items | Built from | Bootstrap |
| --- | --- | --- | --- |
| Simulation | Capabilities: what the simulation produces for each configuration, and its limits | The simulation code, exercised by scenarios | Automatic, through the adapter |
| Concepts | What to learn: terms, prerequisites (which set the order), evidence rules | Reference books, the simulation base, author documents | Proposed, then curated |
| History | Practices, each backed by evidence passages | Historical accounts in the source registry | Extracted as drafts, then curated |

A practice is the unit of history and passages are its evidence; several passages can support or
contradict the same practice.

## 2. Three links

| Link | Question | Result |
| --- | --- | --- |
| Concept to simulation | Can the simulation show this concept and measure it? | An evidence rule, or a simulation gap |
| Practice to concept | Which concept does this action exercise? | A mapping, marked as interpretation |
| Practice to simulation | Can the simulation reproduce what the source describes? | A scenario run and a verdict: reproduces, partly, cannot (with the simplification) |

## 3. Scenarios

The runnable form of a manoeuvre or a practice: a sequence of goals with a configuration and
expected outcomes. Origins: reference-book exercises (to test the adapter and the evidence
rules) and historical practices (to check the simulation against history). Real play will not be
recorded, so timing is calibrated on scenarios run by a scripted operator with skill levels and
noise, plus the author's judgement.

## 4. Situations and what is derived

A situation joins a practice, its concepts and a feasible scenario, with its simplifications.
Short museum visits allow simplified perspectives; each simplification is recorded and a line
may name it. From a situation the tool proposes an activity (goal, success rule, length within
the visit budget, difficulty profile, talk budget), story beats from the practice, and lines
through the line pipeline (retrieve, generate, verify, review). Concepts drive the order.

## 5. Missing and contradictory information

| Kind | Goes to |
| --- | --- |
| Missing field in a practice | A source search, or the historian |
| Conflict between passages | The historian, both passages side by side |
| History against simulation | The game's developers, as an issue draft |
| Concept without evidence in the simulation | The game's developers, or the concept leaves scope |
| Concept against history (modern terms on old practice) | The author |

The tool exports a review sheet for one source (the historian will check a single PDF), and
issue drafts for the game's developers.

## 6. Blind test against the game's existing activities

The pack lists what describes the game's existing mini-games, and those inputs are held out.
The tool derives activities blind; then we compare: same practice and concept, different
activity for the same practice, missed, or new.

## 7. Runtime

The game feeds the pack's adapter each step; the adapter's rules give events and a difficulty
level; the generic scheduler plays cues during difficulty, story lines in calm windows, and
reflections right after a difficulty ends. Delivery is mostly text, voice optional.

## Decisions

- Generic tool, domain packs; sailing (fragateiro, web) is the first pack.
- Mostly text, voice later. Portuguese and English first.
- One operator; a historian may check one PDF.
- Concepts drive the order. Simplifications allowed, recorded, nameable in dialogue.
- No recording of real play.
- Disagreements between history and the simulation are reported to the game's developers.
- Existing mini-games held out, used for a blind comparison.

## Still to generalise

- The line-record schema has sailing fields (`boat`, `zone`, `mission`); they become generic
  (`entity`, `place`, `activity`) with the pack naming them.
- The sailing adapter (`domains/sailing/adapter/observer`) mixes the generic rule engine with
  sailing rules; it will be split into the generic engine in `runtime/` and the sailing rules in
  the pack.
