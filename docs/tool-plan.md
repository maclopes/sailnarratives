# Tool plan: Narrative Workbench

Draft 3, 2026-11-12. Generic tool with domain packs; sailing is the first pack. Illustrated version: https://claude.ai/artifact/9LLyHNJSVrcaScKBDttW9h
(private until shared). Builds on docs/system-design.md (three bases, three links, situations).

## What it is

A local web app for one person, over a folder of plain files in git. The files (YAML, JSON) are
the truth; the app is how the author reads, checks and changes them. Every action is also a
command. Each domain pack supplies an adapter to its simulation (for sailing, the game's vendored physics) so the app can run scenarios. Everything
the tool proposes is a draft until the author accepts it.

## One pattern per step

Inputs -> Proposals (with provenance: simulation, reference book, historical source,
author's document, LLM) -> Review (accept, edit, merge, split, reject with a reason, needs expert) ->
Curated output, plus Checks (warnings that never block silently).

## Screens

1. Simulation: capabilities per configuration and the simulation's limits (sailing adds a polar view);
   scenario runs on a timeline (challenge band, signal strips, events); cards for each quantity
   and event with its rule, the simulation code it reads, and a threshold slider.
2. Concepts: prerequisite graph (which sets the order); cards with PT/EN terms, evidence rules
   tied to simulation events, reference-book references, status.
3. Sources: registry (licence, reliability, read status); passages; review sheet export for a
   single source.
4. History: practice records with their evidence passages; missing fields; conflicts side by
   side.
5. Scenarios: library by origin (training book, historical practice, recorded play); run any
   scenario; expected against actual.
6. Situations: the joins of practice, concept and scenario, with simplifications; derived
   activity proposals with length, challenge profile and talk budget, ordered by concepts.
7. Questions: everything missing or contradictory, by kind, with evidence, and where it goes.
8. Lines and Playtest: the kit's line pipeline and the timing replay (later).

## Reference books

Sources of type reference (cite and paraphrase). Used for names and definitions (PT and EN), the
order of concepts, checking the simulation (simulation / books / verdict), and cue wording. When
the books describe current practice and the domain is historical, the historical sources and an
expert take precedence. Sailing example: training books describe modern boats, not lateen or gaff
working boats.

## Build order

0. Generic core: pack manifest loader, the rule engine (signals to events and difficulty), and
   generic schemas (concept, practice, scenario, situation, question). Sailing pack as the first
   user of each.
1. Simulation base: sailing adapter on the engine, reference-book scenarios, Simulation screen.
2. Concepts base: bootstrap from the simulation base and reference books, prerequisite graph, Concepts screen.
3. Sources and History: registry, practice extraction, conflicts and missing fields.
4. Links and Situations: the three link checks, situation proposals, Questions screen.
5. Blind comparison with the game's existing activities (sailing: its mini-games).
6. Lines, timing scheduler and Playtest.

## Decided

No recording of real play (scripted operator with skill levels instead). Disagreements between
history and the simulation go to the game's developers as issue drafts.

## Open

Which training books (PT and EN) for the sailing pack.
