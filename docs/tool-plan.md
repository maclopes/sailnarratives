# Tool plan: Narrative Workbench

Draft, 2026-11-12. Illustrated version with screen sketches: https://claude.ai/artifact/9LLyHNJSVrcaScKBDttW9h
(private until shared). Builds on docs/system-design.md.

## What it is

A local web app over a folder of plain files in git. The files (YAML, JSON) are the truth;
the app is how people read, check and change them. Every app action is also a command. The app
runs fragateiro's own physics code to replay and record sails. Everything the tool proposes is
a draft until a person accepts it.

Roles: researcher (runs steps, tunes, exports), sailor or instructor (physics and concepts,
PT terms), historian or curator (sources, facts, conflicts), writer (cast, arcs, beats,
choosing lines), translator (EN and FR).

## One pattern per step

Inputs -> Proposals (with provenance: physics, document, training book, game code, LLM) ->
Review (accept, edit, merge, split, reject with reason, needs expert) -> Curated output, plus
Checks (warnings that never block silently).

## Screens

1. Physics: timeline of a recorded sail (challenge band with calm windows, signal strips,
   events as marks); quantity and event cards (rule, formula, game file, firing count,
   threshold slider that re-runs all recordings); polar view per boat; cross-reference rows.
   Recordings come from play or from scripted headless scenarios, which double as tests.
2. Concepts: prerequisite map; cards with PT/EN/FR terms, evidence and struggle rules linked to
   physics events, missions that exercise them (measured), references, status.
3. Sources: registry table (type, licence, reliability, read status, counts); chunks with
   claims; conflicts view; add by URL, PDF or interview note.
4. Missions: skeletons from the game's mission definitions; phases and talk budget (calm
   windows) measured from recorded runs; empty story slots for the writer.
5. Lines: board per mission and beat; PT/EN/FR side by side; delivery class and length against
   its window; claims with verdicts and chunks; approve, edit (re-verified), reject, needs source.
6. Playtest: replay a recording with the approved lines and the scheduler; what played, waited
   or dropped and why; compare talk-anytime with challenge-aware timing.

## Training books

Registered as sources (cite and paraphrase; copyrighted). Used for (1) names, definitions and
teaching order, (2) checking the physics: each quantity gets game / books / verdict (agrees,
differs, needs expert), (3) standard wording for cues. Limit: books describe modern boats, so
each check has a third column for traditional-boat sources and the sailor or museum, which wins
for anything about a specific boat. Candidates to confirm: RYA dinghy handbooks, US Sailing
beginner book, Le Cours des Glénans (FR), Federação Portuguesa de Vela material (PT), the
fragateiro physics notes and the Unity simulator paper.

## Interaction

Click-through provenance on everything; run-step buttons (LLM steps show cost first; results
are drafts); review queue per role with keyboard shortcuts; an in-context "ask" panel whose
answers arrive as drafts; threshold sliders with preview; comments and an audit log stored with
the files; export for the web game and Unity.

## Build order

1. Physics observer, scenarios, recordings, Physics screen.
2. Challenge-aware scheduler, Playtest screen.
3. Concept bootstrap, Concepts screen, review queue.
4. Mission bootstrap with phases and talk budget, Missions screen.
5. Source registry, ingest, retrieval, Sources screen (kit prompts 02, 03).
6. Generation, verification, review, export (kit 05, 06), evaluation (08).

## Decisions needed

Web first or Unity first; text or voice; which training books are available; who fills each
role and whether they share a machine; front-end stack.
