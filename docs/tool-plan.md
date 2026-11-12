# Tool plan: Narrative Workbench

Draft 2, 2026-11-12. Illustrated version: https://claude.ai/artifact/9LLyHNJSVrcaScKBDttW9h
(private until shared). Builds on docs/system-design.md (three bases, three links, situations).

## What it is

A local web app for one person, over a folder of plain files in git. The files (YAML, JSON) are
the truth; the app is how the author reads, checks and changes them. Every action is also a
command. The app runs the game's own physics (vendored, read-only) to run scenarios. Everything
the tool proposes is a draft until the author accepts it.

## One pattern per step

Inputs -> Proposals (with provenance: physics, training book, historical source, author's
document, LLM) -> Review (accept, edit, merge, split, reject with a reason, needs expert) ->
Curated output, plus Checks (warnings that never block silently).

## Screens

1. Physics: capabilities per boat and wind (polar, manoeuvres the game produces, limits);
   scenario runs on a timeline (challenge band, signal strips, events); cards for each quantity
   and event with its rule, game file and a threshold slider.
2. Concepts: prerequisite graph (which sets the order); cards with PT/EN terms, evidence rules
   tied to physics events, training-book references, status.
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

## Training books

Sources of type training (cite and paraphrase). Used for names and definitions (PT and EN), the
order of concepts, checking the physics (game / books / verdict), and cue wording. Books describe
modern boats; for a specific traditional boat the historical sources and a sailor take
precedence.

## Build order

1. Physics base: observer, training-book manoeuvre scenarios, Physics screen.
2. Concepts base: bootstrap from physics and books, prerequisite graph, Concepts screen.
3. Sources and History: registry, practice extraction, conflicts and missing fields.
4. Links and Situations: the three link checks, situation proposals, Questions screen.
5. Blind comparison with the game's mini-games.
6. Lines, timing scheduler and Playtest.

## Open

Recording real play; reporting disagreements to the game developers; which training books.
