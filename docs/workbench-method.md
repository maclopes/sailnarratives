# How the workbench works: steps, methods and results

Version of 2026-11-14 (workbench version 26). The workbench is the tool's interface
(`workbench/intake.html`, published at https://claude.ai/artifact/28te1trNq5pVdem1xFzUD9). This
document explains what each step does, which rule or prompt it uses, how relations between
items are made, how relevance is decided, and what each step produced for the first domain
pack (traditional boats of the Tagus, the fragateiro game). The results were read from the
workbench's database on 2026-11-14.

## The method in one paragraph

Every step is either a **fixed rule** (deterministic code: counts, string matching, checks) or
a **request to Claude** with a fixed prompt that asks for JSON. Claude never decides on its own:
its answers are drafts that the author reviews, and the code checks every answer (ids must
exist, values must be from a closed list, missing answers are retried or reported). Long work
is split into small requests (pieces of text, batches of items) so that a failure loses little
and a run can resume. Facts carry the id of the passage they come from, all the way to the
lines the game shows.

## Overview

| Step (tab) | Input | Method | Output |
| --- | --- | --- | --- |
| 1 Project | the author | form | subject, audience, visit length, languages, goals, simplifications, tone |
| 2 Materials | the author, Google Drive, link check | form, Drive import, rules | a source registry with licence, reliability, read status, held-out flag |
| 3 Readiness | project and materials | rules, plus one Claude review | gaps per knowledge base, a `domain.yaml` manifest |
| 4 Concepts | source texts | Claude extracts per piece of text, Claude groups in batches, rules give statuses, Claude checks against the game, Claude summarises | a concept table with source terms, statuses and conflicts |
| 5 History | historical texts | Claude extracts practices, Claude groups, rules give statuses, Claude links to concepts | a practice table with evidence passages |
| 6 Situations | practices, concepts, game world | Claude proposes activities, Claude compares blind with the game | activity proposals, game additions, blind comparison |
| 7 Narrative | one mini-game, evidence, story bible | rules gather evidence, Claude plans, Claude writes, Claude and rules check | cast, beats and checked lines per mini-game |
| 8 Game report | all of the above, game world | Claude sorts by kind, rules match against the game, Claude compares practices with activities | an evaluation of the game with issue drafts |

All Claude requests go through the page's `sample.json(prompt, {modelTier})`: tier `default` for
reading and sorting, `complex` for planning, writing, summarising and comparing. Each request is
retried once; "not allowed", "too many requests" and "unavailable" stop the run, keeping what
was done.

---

## 1. Project

**What:** a form for the subject, audience, visit length (minutes), primary language with its
variant (for example European Portuguese), other languages, learning goals, simplifications the
simulation makes, and tone. Saved as one record (`project/main`).

**Why it matters later:** the subject, goals, visit length and audience go into every prompt;
the primary language variant decides which source terms count as the right ones (step 4) and
the glossary used in writing (step 7).

**Result:** "Boats of the Tagus", museum visitors, European Portuguese (pt-PT) first, English
second; goals: the sailing concepts the simulation shows and the working life of the river's
boats.

## 2. Materials

**What:** a registry of every source. Each has a kind (simulation, reference book, historical
account, author's document, existing activity, person who can check), title, link or file,
language, licence (open, CC0, copyright: cite and paraphrase only, permission, unknown),
reliability (A scholarly or museum, B documented local history, C uncited), read status and
notes.

**Rules:**
- *Required fields per kind* (for example a historical account needs language, licence and
  reliability); missing ones show as "incomplete".
- *Held out:* "existing activity" items, and any item marked as describing the game's existing
  activities, are kept out of every input so the blind comparison (step 6) is fair.
- *Link check:* `tagus-linkcheck` (pipeline) reports each link as works, moved, broken,
  unreachable or not checked, with an archived copy when one exists; its report can be imported.
- *Google Drive import:* walks a folder path (for example `projects/tagusnavy/historia`), lists
  the files, matches each to an existing material by title or proposes a new one, and stores the
  file's text (step 4 reads it).

**Result:** 44 materials: 36 historical accounts, 4 author's documents, 1 simulation (the
fragateiro physics), 1 reference book (Veleiro.net sailing course, pt-BR), 1 existing activity
(the game's mini-game list), 1 person (a historian). 32 read in full, 4 could not be read, 7
not read. 5 held out (the existing activities, the story bible, the method document, the
leaflet, the discussion summary). **Gaps:** no reliability grade and no licence recorded on 43
of 44 (only one is marked "cite and paraphrase"), so everything is treated as copyrighted.

## 3. Readiness

**What:** before any reading, a check of whether the materials can support each knowledge base.

**Rules** (`readiness()`), one block per base, each finding graded ok / note / gap / blocks:
- *Project:* missing subject, audience, visit length, primary language or its variant, goals.
- *Simulation:* at least one simulation item; someone who can confirm it (a developer).
- *Concepts:* reference books in each project language and variant (a pt-BR course for a pt-PT
  project gives a gap: terms differ), completeness.
- *History:* at least one account; grade A sources; ungraded, unknown licence, unread, dead
  links; half or more grade C; a historian listed.
- *Blind comparison:* something held out; author documents that may mention existing
  activities.

A base is *blocked* if any finding blocks, *usable with gaps* if any is a gap, otherwise
*ready*.

**Claude's second look** (button "Ask Claude"): the project, the materials' metadata (titles,
notes, kinds, licences, held-out flags; never the texts) and the rule findings are sent with
this instruction:

> Fixed rules have already produced the findings listed in ruleFindings. Do not repeat them.
> Suggest up to 8 further gaps, risks or contradictions that a careful researcher would notice
> from the titles, notes and metadata: missing kinds of source, imbalances, likely licence or
> reliability problems, materials that may contradict each other, questions to ask the people
> listed. … Do not invent facts about the subject.
> Return JSON only: `{"items":[{"area","severity":"blocks|gap|note","text"}]}`

**Output:** the findings, and an export of the pack manifest (`domain.yaml`).

**Result (by the rules today):** simulation ready; concepts with gaps (the only reference book
is Brazilian Portuguese, so every pt-PT term needs checking); history with gaps (no grades, no
licences, 4 unreadable); blind comparison ready (5 held out).

## 4. Concepts

Goal: the concepts a visitor can learn, each backed by sources, with its terms per language and
whether the game shows it.

### 4a. Getting the text

- **PDF:** pdf.js extracts the text layer page by page, writing a `[page N]` marker before each
  page so passages keep their location. A PDF with no text layer (a scan) is refused: paste the
  text instead.
- **Google Drive:** the text comes through the Drive connector.
- **Paste**, for anything else.

The text is stored per source (`texts/<source>`). **Result:** 21 sources with text, 895,375
characters in all (17 from Drive, 1 PDF, 1 from the game's repository, 1 author document, 1
excerpt).

### 4b. Reading: extracting candidate concepts

**Algorithm:** the text is cut into pieces of at most 6,000 characters, cutting at page,
section or file markers where possible (`chunks()`). Each piece is one request, in order; the
answers are saved after each piece, so a stopped run resumes at the next unread piece. Within a
source, candidates with the same normalised term (lower case, no accents or quotes) are merged.
Each candidate gets an id made of the source id, the text's length and a number
(`m-ref-veleiro:abc:12`); when the text changes, the ids change and the source is read again.

**Prompt** (`extractPrompt`), per piece:

> Read part i of n of one source and list the concepts a visitor could learn from it.
> - A concept is a skill, manoeuvre, force, condition or state, or a part or term needed to
>   explain one. Keep everything on the subject; the author decides scope later.
> - term: exactly as written in the source, in the source's language.
> - definition: your paraphrase in English, at most 25 words. Never copy sentences from the source.
> - location: the [page N], [section: …] or [file: …] marker the term falls under.
> - numbers: only values the source states (angles, speeds, limits), with what they measure.
> - One item per distinct term, at most 30 items. Do not add anything that is not in the text.

For the simulation's own description, the prompt adds: a concept is something the player does
or experiences that the simulation computes, detects or controls, and `measured_by` names the
signal, event or control that shows it.

Paraphrase only, with the location: this is how copyrighted sources are used (cite and
paraphrase, never quote).

**Result:** 1,334 candidate concepts from 18 sources. Largest: Pedrosa, *A Muleta e a
Tartaranha* (220), Veleiro.net course (178), Gaspar, *Os portos fluviais do Tejo* (134),
*Territórios da Lisboa Medieval* (130), "o tejo" site (124), *Portugal Marítimo* (96); the
game's physics gave 66.

### 4c. Grouping: relations between candidates

A relation here means **"these candidates name the same concept"**. It is made by meaning, not
by spelling: the same word can mean different things (Brazilian *cambar* is a tack, in the
method document a gybe).

**Algorithm:** the candidates are taken in order of source kind (simulation first, then
reference books, author documents, historical accounts), in batches of 50. Each batch is placed
into the concept table built so far (`assignPrompt`); the table is sent with each concept's id,
label and a short meaning (shortened further if the request would be too large). Candidates
Claude does not place become concepts of their own. Grouping never undoes the author's work:
existing concepts, their decisions and moves are kept, and only new candidates are placed.

**Prompt** (`assignPrompt`):

> For each candidate: if it means the same as an existing concept, give that concept's id.
> Otherwise give a short English label for a new concept; candidates in this batch that mean the
> same thing get the same new label. Group by meaning, never by spelling: the same word can mean
> different things in different sources or language variants. …
> Also report real conflicts between a candidate and the concept it joins: different numbers for
> the same quantity, or a different definition. A different language, variant or synonym … is
> not a conflict, and neither is a simulation describing how it models something, unless its
> values or behaviour contradict the source.

(An earlier version grouped all candidates in one request, `alignPrompt`; it failed on 1,500
candidates and was replaced by the batches.)

**Author review:** each concept is a card listing its source terms; the author moves a term to
another card ("Move to…"), renames, confirms ("Group is right") or drops it ("Leave out").

### 4d. Statuses: fixed rules over each group

`statuses()` gives each concept one or more statuses, from its members' sources, kinds and
languages:

| Status | Rule |
| --- | --- |
| conflicting | Claude reported a conflict for the group (number, definition, term) |
| term clash | the same normalised term, in one language, appears in two different concepts |
| variant difference | members in two variants of one language (pt-PT, pt-BR) share no term |
| missing term | no member in the primary language variant (pt-PT) |
| single source | all non-simulation members come from one source |
| not in simulation | no member from the simulation and no simulation link |
| simulation only | only the simulation names it |
| agreed | none of the above |
| out of scope | step 4e proposed it out of scope and the author has not confirmed it |

**Result:** 633 concepts from 1,069 grouped candidates (265 more were read but not yet placed:
the last grouping run stopped). 417 concepts have a single member; 121 concepts are backed by
two or more sources and 48 by three or more. Statuses: not in simulation 577, single source
477, missing term (no pt-PT word) 381, term clash 36, simulation only 35, conflicting 29 (15
number, 10 definition, 4 term), variant difference 7. 56 concepts include the simulation.

By source kind: 424 concepts come only from historical accounts, 125 only from the reference
book, 35 only from the simulation; 12 join history and the reference book, 8 the reference book
and the simulation, 4 the author, the reference book and the simulation.

Concepts with most sources: shallow draught, *arrais* (skipper), *varino*, *muleta*, lateen
sail (6 sources each); rudder, keel, river landing places (5).

Examples of conflicts: the course uses both *orça fechada* and *orça* for close-hauled; the
closest angle to the wind is 45–50° in the course against about 36° in the game; *tábua de
bolina* described as a lowered board in one source and a fixed lateral keel in another.

### 4e. Check against the game: concept to simulation

**What:** links each concept to the simulation's own concepts, flags numbers that disagree with
the game, proposes a scope, and removes conflict noise. Runs on concepts not checked yet, 30 at
a time.

**Prompt** (`linkPrompt`), with the learning goals, the visit length and the simplifications:

> For each concept below:
> - sim: ids of simulation concepts that show or measure it. Link only when the simulation
>   really lets the player see or do it …
> - numbers: if a number stated for the concept disagrees with the simulation's number for the
>   same quantity … describe it in one sentence naming both values.
> - scope: "core" if it serves the learning goals and a visitor can meet it in the game or its
>   stories; "maybe" if useful context; "out" if it does not fit a short museum visit on this
>   subject (for example modern yacht fittings, safety drills, unrelated topics).
> - keep: the indices of the listed conflicts that are real disagreements.

**Relevance** of a concept is decided here: **core** (serves a learning goal and can be met in
the game or its stories), **maybe** (context), **out** (not for a short visit). Out-of-scope
concepts leave the later steps unless the author confirms them.

**Result:** not run on the current table (0 of 633 concepts checked). Until it runs, scope is
unset, nothing is out of scope, and "not in simulation" counts only groups that contain a
simulation candidate. This is the next step to run in the Concepts tab.

### 4f. Summary of the sources

**Prompt** (`summaryPrompt`, tier complex): the table without dropped concepts, with each
member's source, term, language, meaning, numbers and statuses:

> 1. Sort the concepts into 4 to 8 types that suit this subject … Every concept goes in one type.
> 2. For each type, at most 5 points in each list: agreements …; conflicts … and one suggested
>    next step (ask a sailor, check a source, decide as a game design choice); clarifications
>    (where one source supplies what the others lack …); gaps.
> 3. An overview of 2 to 4 sentences: the main conflicts to settle first, and what is missing.
> Do not add facts that are not in the table.

**Result:** 9 types (points of sail and wind; manoeuvres and steering; sails and rig; hull and
steering gear; boat types compared with the game; places and the river compared with the game;
work, trade and rules; navigation and safety; simulation internals). Overview: settle first (1)
the sailing vocabulary (*cambar* is a tack in the Brazilian course and a gybe in the method
document; the historical sources give the European terms *virar por davante* and *virar em
roda*), (2) the closest angle to the wind (45–50° in the course, about 36° in the game), (3)
dates and figures in the history (steamboats, navigable lengths, passenger limits).

## 5. History

Goal: what people did with boats on the river, each practice backed by passages from the
sources.

### 5a. Reading: extracting practices

Same pieces of text as in 4b (historical accounts only, not held out). One request per piece.

**Prompt** (`practicePrompt`):

> List what people did with boats and the river: practices, rules and events.
> - One item per distinct practice or event: a work routine (a fishing method, a cargo run, a
>   ferry crossing, towing, building or repairing boats), a rule (a regulation, fee or licence),
>   a dated event (a ban, a survey, a new service), or a description of a boat or place without
>   action.
> - action: your English paraphrase, at most 25 words. Never copy sentences.
> - who, boat, place, period, cargo, gear, conditions: as the text states them …; "" when the
>   text does not say.
> - numbers: only values the text states …; kind: practice, rule, event or description;
>   location: the [page N] marker. At most 25 items. Do not add anything that is not in the text.

Duplicates within a source are merged on kind, boat, place and the start of the action.

**Result:** 437 passages from 10 historical sources.

### 5b. Grouping: relations between passages

A relation here means **"these passages describe the same practice or event"**. Batches of 40
are placed into the practice list built so far (`hAssignPrompt`), as in 4c:

> If it describes the same practice or event as an existing one (the same activity by the same
> kind of people or boat; places and periods may differ), give that practice's id. …
> Report real disagreements: "date" (different dates for the same event), "number" (different
> values for the same quantity; give both with their sources), "description" (accounts that
> cannot both be true). More detail, or the same practice in another period, is not a conflict.

After each batch, each practice's boats, places and periods are the union of its members'
(`mergeFields`), and its kind is the most common kind among them.

**Statuses** (`hStatuses`, rules): conflicting; single source; agreed (two or more sources, no
conflict); no boat (a practice whose sources name no boat); no place; no period; no concept
(linked, but to no concept).

**Result:** 132 practices: 38 practices, 26 events, 14 rules, 54 descriptions. 103 rest on a
single source, 29 on two or more (7 on four). 8 with conflicts (4 number, 3 description, 2
date). 45 without a period, 16 without a place, 8 practices without a boat.

Best supported: the decline of sail freight because of rail, road and bridges (6 sources);
preservation of surviving boats (5); the 1552 count of Tagus boats, boat types and terminology,
river traffic between the banks until the mid-20th century, boat building in the Tagus yards
(4 each).

Examples of conflicts: the decline of sail freight dated 1951 and 1966 against "intense
activity until the 1960s"; the 1552 count of 1,490 boats said to cover the whole Tagus in one
source and the river boats only in another.

### 5c. Practice to concept

**Prompt** (`hLinkPrompt`), 50 practices at a time, with the list of concepts not dropped:

> For each practice, give the ids of the concepts it exercises or shows (a manoeuvre, a point
> of sail, a boat part, a type of boat, a place), at most 6, and a note of at most 12 words on
> how. This is an interpretation: sources describe work, not technique, so link only what the
> practice clearly involves.

**Result:** all 132 practices linked; 82 to at least one concept (350 links), 50 to none.

**Review sheet:** for one source, a list of its passages with their practice, statuses and
conflicts, for the historian to check a single PDF.

## 6. Situations

A situation is where all three bases agree: a historical practice, the concepts it exercises,
and a simulation that can play it.

### 6a. Proposing activities

**Input:** practices of kind "practice" not dropped, 15 at a time, each with its boats, places,
periods, number of sources, up to 3 actions, conditions, cargo and linked concepts (marked
whether the game shows them); the game's boats, areas and ports; the concepts the game shows
(those with a simulation member or link). **Not** the game's existing activities (held out).

**Prompt** (`proposePrompt`), in short:

> Each activity must come from one historical practice below and let the player do a
> recognisable part of it in the game. … For each practice that can become an activity, propose
> one: title, goal, success (a rule the game can measure), boat (one of the game's boats; if the
> historical boat is not in the game, pick the closest and explain), area and route, concepts,
> minutes (1 to 6), level (1 basics, 2 manoeuvres, 3 specialised work), simplifications, needs,
> feasibility ("full", "simplified", "needs feature"), features (from a fixed list: tide and
> current, water depth and shallows, rowing and poling, towing, crew and tasks aboard, fishing
> net and catch, cargo loading and weight, steam and motor traffic, river bar and pilotage, new
> map area, new boat, rig changes, other), premise (only facts in the practice record).
> Do not skip a practice only because the game lacks something … propose the activity as it
> would be with that addition, with feasibility "needs feature" and the features named. Skip
> only practices with no boat or water activity at all … and say why.

**Rules after the answer:** ids are read from the text ("p8 Label" gives p8); a proposal naming
no known practice is dropped and counted; the boat is matched against the game's boats.
**Game additions** gathers the features across proposals, counting the activities each would
unlock (needs feature) or improve, and the sources behind them.

**Relevance:** the level orders activities (concepts drive the order); feasibility says how
much the game must change.

**Result:** 33 activities from 38 practices: 5 full, 19 simplified, 9 needing a feature; 9 at
level 1, 20 at level 2, 4 at level 3. 8 practices skipped (for example ox-cart transport to the
paper mills, petitions on the French *tartana*: no water activity). Most requested additions:
water depth and shallows (5), cargo loading and weight (4), new boat (4), fishing net and catch
(4).

### 6b. Blind comparison with the game's activities

**Prompt** (`comparePrompt`, tier complex): the game's mini-games and mission kinds (now
revealed), and the proposals:

> For each game activity of type "museum mini-game", give the closest proposal and the match:
> "same" (the same practice and essentially what the player does), "related" (the same practice
> or boat, but a different task), or "none". For each proposal, say whether the game has an
> equivalent: "same", "related" or "new".

**Result:** of the game's 9 mini-games, 2 found the same (Upwind with the Falua, Passengers
with the Catraio), 4 related (Downwind, Cargo with the Fragata, Fishing with the Muleta,
Supplies with the Canoa), 3 none (Whales, Seaweed, Free sailing: no source in the registry
describes them). Claude answered for 13 of the 33 proposals: 6 match a game activity, 6 are related, 1 is new.

## 7. Narrative

For one of the game's mini-games, and optionally one of its options (boat × place).

### 7a. Gathering evidence (rules)

`evidenceFor()` selects, without Claude:
1. the practice of the proposal the blind comparison matched to this mini-game, if any;
2. then up to 5 practices whose boats include the mini-game's boat, **most sources first**;
3. up to 6 passages of each, as evidence records (`e1`, `e2`…: source, location, paraphrase,
   numbers);
4. up to 10 concepts linked to the proposal or those practices, with 2 source terms each.

At most 45 records. **Relevance for the narrative is therefore:** matched by the blind
comparison, then same boat, then number of sources.

Also gathered: the places the boat may pass (the area's ports and landmarks, minus landmarks
built after the chosen period, plus places named in the evidence), the game moments that can
trigger a line (33), the author's story bible if it mentions the boat, and a glossary of
pt-PT terms to use and other variants to avoid (from the concept table).

### 7b. Planning cast and beats

**Prompt** (`planPrompt`, tier complex), with the evidence, the bible (marked "proposals, not
evidence"), the game moments, the deliveries, the narrator (in character in a period, or a
present-day guide) and the talk setting (quiet, normal, chatty):

> - 1 to 3 characters, invented and labelled fictional, whose trade and world come from the
>   evidence (cite evidence ids for their role).
> - 4 to 6 story beats in the order setup, complication, turn, close, plus at most one curiosity
>   card. The sailing difficulty is the complication.
> - Leg beats (trigger "steady_leg"): talk for the long calm stretches … Place beats (trigger
>   "near_place:<name>"): only from evidence that mentions it.
> - Never put a story line on a difficult moment: a difficult moment gets at most a cue, and the
>   story continues as a reflection after it is solved.
> - Each beat: trigger, delivery, character, gist, concept, evidence ids.

### 7c. Writing lines

**Prompt** (`linesPrompt`, tier complex): two candidates per beat (a pool of 2, 3 or 5 for leg
beats), in European Portuguese and English, with word limits (cue 6, reflection 25, story 35,
curiosity 60), the glossary, and:

> Use only facts in that beat's evidence. Names of characters, feelings and small actions are
> colour: they must not state checkable facts. … claims: every factual statement in the line,
> each with the evidence ids that support it. fictional: true when the line states no fact from
> the evidence.

### 7d. Checking lines (Claude and rules)

- **Claude, independently** (`checkPrompt`): for each factual statement, "supported",
  "unsupported" or "contradicted" by the listed evidence.
- **Rules** (`mechChecks`, `glossaryWarnings`): word limits; every number in the line must be in
  the evidence (thousands separators ignored); the same numbers in PT and EN; no landmark built
  after the period; no avoided variant term.
- A line becomes **verified** when all claims are supported and no rule fails, otherwise **needs
  work**; the author approves. Only verified and approved lines are exported, each with its
  trigger, delivery, conditions (`when`: boats, areas, places) and evidence ids; the export
  reports, per option, whether a setup and a close line exist.

**Result:**

| Mini-game | Evidence | Cast | Beats | Lines | Verified | Needs work |
| --- | --- | --- | --- | --- | --- | --- |
| Passengers with the Catraio (with story bible) | 35 | 2 | 7 | 14 | 3 | 11 |
| Supplies with the Canoa | 42 | 2 | 6 (with a leg and a place beat) | 13 | 9 | 4 |
| Fishing with the Muleta | 42 | 2 | 7 (with a leg, a place and a curiosity) | 15 | 12 | 3 |
| Cargo with the Fragata | 44 | 2 | 6 | not written yet | | |

Why lines needed work: 15 claims unsupported by their evidence (none contradicted), 3 lines
with different numbers in PT and EN, 1 over the word limit. 9 lines are fictional colour.

## 8. Game report

An evaluation of the game against the sources (a main goal of the tool).

**1. Sorting by kind** (`classifyPrompt`), 40 items at a time, retried in 15s for any missing:
concepts not dropped, plus the boats and places named in the practices. Categories: boat,
place, sailing, hull, practice, role, cargo, event, regulation, internal, other. For boats and
places, the usual modern name; for places, the game area it lies in (or outside); for sailing,
hull and practice items the game does not show, what the simulation would need.

**2. Matching against the game (rules):** a boat is *in game*, *in development* or *missing*
(name compared after normalising, singular); a place is a *port*, *landmark*, *on map* (a named
place on the area's map), *sea mark only*, *outside the game's areas*, *area unknown* or
*missing*. Boats and places from concepts and from practices are merged by name and area; each
keeps the set of sources that name it.

**3. Physics:** sailing and hull concepts are *shown* (a simulation member or link), *not shown*
(with what is needed) or *out of scope*.

**4. Practices against activities** (`activityPrompt`), 30 at a time: *covered* (a game activity
lets the player do essentially this, with a fitting boat and place), *partly*, *missing*, with
the closest activity.

**5. Conflicts** on boats, places, sailing, hull, practices and events; **anachronisms**
(landmarks newer than the narrative's period); **game additions** from step 6.

**Relevance:** every finding counts the **independent sources** behind it; issue drafts are
written only for findings with at least the chosen number of sources (1, 2 or 3; default 2),
most sources first. Each draft carries its paraphrased evidence and the sources' names.

**Result:** the two reports stored date from 13 November, before the fixes to sorting (batches
of 40, coverage check, boats and places from the practices) and before the rebuilt world list
(Oeste area, lighthouses). They show the sailing side only: 21 sailing and hull concepts shown,
89 not shown (most often needing navigation marks in channels, reefing control, halyard tension,
a person-overboard event) and 35 out of scope; of 38 practices compared, none covered by the
game's activities. **Boats and places: 0, because of the bug since fixed. Build the report
again** to get the boats, places, additions and anachronisms, and to compare against the
current game.

---

## How relations are made, in summary

| Relation | Made by | Kept as |
| --- | --- | --- |
| candidate ↔ candidate (same concept) | Claude, by meaning, in batches; author moves | concept members |
| passage ↔ passage (same practice) | Claude, by activity and kind of people or boat, in batches; author moves | practice members |
| concept → simulation | the simulation's own candidates in the same group, or Claude's link check | `simLinks` |
| practice → concept | Claude, marked as interpretation | `concepts` and a note |
| practice → activity proposal | one proposal per practice, by Claude | `practice` on each proposal |
| proposal ↔ game activity | Claude, blind | the blind comparison |
| boat, place → the game | rules: normalised name, area | statuses in the report |
| line → evidence → source passage | Claude names evidence ids per claim; Claude checks; rules check numbers | `claims`, `sources` |

## How relevance is decided, in summary

- **Number of independent sources** behind a concept, practice, boat or place: the main measure.
  It orders the narrative's evidence and the report's findings, and sets the threshold for
  issue drafts.
- **Scope** of a concept (core, maybe, out), proposed by Claude from the learning goals and the
  visit length, confirmed by the author.
- **Presence in the game:** whether the simulation shows a concept, and whether the game has a
  boat, place or activity.
- **Level** of an activity (1 to 3): the order for the learner.
- **The author's decisions:** left-out items leave every later step; undecided items are used.

## Known limits

- Claude's extraction and grouping are drafts; a different run can group differently. The author's
  moves and decisions are the reference.
- Reading is slow (about 150 requests, one at a time) and sends copyrighted text to Claude; the
  plan is to re-read on a local model.
- Some steps are incomplete or out of date: the game check (4e) has not run on the current
  concept table, 265 candidates are not yet grouped, and the game report (8) predates later fixes.
