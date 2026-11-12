# System design

Draft 2, 2026-11-12. Replaces draft 1 (five components). Scope: this repository builds a tool
for one author. The tool proposes drafts; the author curates them. It writes no story of its own.

## The idea in one paragraph

Three knowledge bases, each built from its own evidence: what the game's **physics** can
simulate, what **concepts** a visitor should learn, and what **history** says people did. The
tool links them, and where all three links hold it proposes a **situation**: a historical
practice that exercises a concept and that the game can reproduce. Activities (mini-game
proposals), story beats and lines are derived from situations. Along the way the tool reports
what is missing and what contradicts, as research questions.

```
  Physics (game code)      Concepts (training books + physics)      History (accounts)
        │                          │                                      │
        └── can show/measure? ─────┤                                      │
                                   ├── which concept does it exercise? ───┤
        └──────────────── can the game reproduce it? ─────────────────────┘
                                   ▼
                              Situations  ──►  activities, story beats, lines
                                   │
                                   └──►  missing and contradictory information
```

## Context: museums

Visits are short, so activities last a few minutes and lines are short. Situations may simplify
history (no tide, no crew, one boat). Each simplification is recorded, and a line may
acknowledge it ("on the real river the tide decided when you left"), so a simplified game stays
honest.

## 1. The three knowledge bases

| Base | Items | Built from | Bootstrap |
| --- | --- | --- | --- |
| Physics | Capabilities: for each boat and wind, the states and manoeuvres the game produces (points of sail, tack, gybe, stall, heel, drift athwart in the muleta's fishing mode) and its limits (no current, no tide, no rowing) | The vendored game physics, exercised by scripted scenarios | Automatic |
| Concepts | Sailing concepts and general concepts, with PT/EN terms, prerequisites, and evidence rules tied to physics events | Training books (PT, EN), the physics model, the author's documents | Proposed, then curated |
| History | Practices: who, boat, place, period, conditions, sequence of actions, numbers. Each practice is supported by evidence passages from sources | Historical accounts in the source registry | Extracted as drafts, then curated |

A practice is the unit of history, and passages are its evidence. Several passages can support
the same practice, or contradict each other about it.

## 2. The three links

| Link | Question | Result |
| --- | --- | --- |
| Concept to physics | Can the game show this concept and measure it? | An evidence rule, or a game gap (for example tide) |
| Practice to concept | Which concept does this action exercise? | A mapping, marked as interpretation (the sources describe work, not technique) |
| Practice to physics | Can the game reproduce what the source describes? | A scenario run with expected ranges, and a verdict: reproduces, partly, cannot (with the simplification) |

## 3. Scenarios

A scenario is the runnable form of a manoeuvre or a practice: a sequence of goals (hold a
point of sail, tack, stop alongside, drift athwart) with a boat, a wind and expected outcomes.
It records its origin:

- training-book manoeuvres: the catalogue used to test the physics observer and the concepts'
  evidence rules;
- historical practices: to check the game against history;
- recorded play (later): to calibrate thresholds and timing against real visitors.

## 4. Situations and what is derived from them

A situation joins one practice, one or more concepts, and a feasible scenario, plus the list of
simplifications. From it the tool proposes:

- an **activity** (a mini-game proposal): goal, success rule, length within the museum budget,
  the challenge profile and the calm windows (talk budget);
- **story beats** from the practice: people, purpose, place, period, true details;
- **lines**, through the kit's pipeline (retrieve, generate, verify, review).

Order: concepts drive it. The prerequisite graph gives the progression, and activities are
placed along it.

## 5. Missing and contradictory information

A first-class output, because filling it is most of the research work.

| Kind | Example | Goes to |
| --- | --- | --- |
| Missing field in a practice | The catraio's rig and size are unsourced | A source search, or the historian |
| Conflict between passages | Crew of three in one source, three to five in another; 1785 against 1875 | The historian, with both passages side by side |
| History against physics | A practice the game boat cannot reproduce, or reproduces at implausible speed | The author: a game gap, a tuning issue or a doubtful source |
| Concept without evidence | A concept the game cannot show or measure | A game gap, or the concept leaves scope |
| Concept against history | Modern technique or terms applied to a historical boat | The author or a sailor |

Each item becomes a research question with its evidence attached. Since one historian will
check a particular PDF, the tool can export the questions and claims tied to that one source as
a short review sheet.

## 6. Does the tool rediscover the game's mini-games?

The game already has mini-games. We ignore them while designing, and use them later as a test:
derive activities blind, then compare.

- Held out from the inputs: the game's mini-game definitions, and every document that describes
  them (the leaflet, the mini-game parts of the method doc and of the discussion summary, the
  story bible).
- Inputs allowed: the physics, the training books, and the historical sources.
- Comparison: for each existing mini-game, did the tool propose a similar activity (same
  practice and concept), a different one for the same practice, or nothing? And what did the
  tool propose that the game lacks?

This tests whether the method is systematic, rather than tuned to what already exists.

## 7. At runtime: challenge-aware timing

Unchanged from draft 1. The game feeds the observer each physics step; it computes events and a
challenge level (0 to 1); lines play only in calm windows; cues may play during difficulty;
reflections play right after it. Delivery is mostly text, with voice as an option (voice length
replaces reading time). Thresholds live in `runtime/src/observer/config.ts` and are documented in
`knowledge/game-physics.yaml`.

## Decisions so far

- Target game: the web version (fragateiro) only.
- Delivery: mostly text; voice later.
- Languages: Portuguese and English first; French later.
- One person operates the tool; a historian may check one specific PDF.
- Concepts drive the order.
- Situations may simplify; simplifications are recorded and may be named in dialogue.
- Mini-games are ignored for now and used later as a blind comparison.

## Open questions

- Recording real play in the museum (consent notice, anonymous logs).
- When history and physics disagree, report to the fragateiro developers or only record it?
- Which training books: titles and editions in PT and EN.
