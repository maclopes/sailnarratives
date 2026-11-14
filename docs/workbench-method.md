# How the workbench works: steps, methods and results

Version of 2026-11-14 (workbench version 33). The workbench is the tool's interface
(`workbench/intake.html`, published at https://claude.ai/artifact/28te1trNq5pVdem1xFzUD9). This
document explains what each step does, which rule or prompt it uses, how relations between
items are made, how relevance is decided, and what each step produced for the first domain
pack (traditional boats of the Tagus, the fragateiro game), with examples, and above all **the
problems the tool found** in the sources and the game: dates, places, boat names, methods,
terms, numbers. The results were read from the workbench's database on 14 November 2026 (the
snapshot in `data/workbench/`).

The sections follow the steps of the method. Since version 33 the workbench shows them in six
tabs: Project; Sources (sections 2 and 3); Knowledge, with the views Concepts (4), Practices (5)
and Boats and places (8); Situations (6); Narrative (7); Game report (8).

## The method in one paragraph

Every step is either a **fixed rule** (deterministic code: counts, string matching, checks) or
a **request to Claude** with a fixed prompt that asks for JSON. Claude never decides on its own:
its answers are drafts that the author reviews, and the code checks every answer (ids must
exist, values must be from a closed list, missing answers are retried or reported). Long work
is split into small requests (pieces of text, batches of items) so that a failure loses little
and a run can resume. Facts carry the id of the passage they come from, all the way to the
lines the game shows.

## Overview

| Step (tab) | Input | Method | Output | Result now |
| --- | --- | --- | --- | --- |
| 1 Project | the author | form | subject, audience, languages, goals | done |
| 2 Materials | the author, Google Drive, link check | form, Drive import, rules | source registry | 44 materials, 21 with text |
| 3 Readiness | project and materials | rules, one Claude review | gaps per base | gaps in licences and grades |
| 4 Concepts | source texts | Claude reads, Claude groups, rules give statuses, Claude checks against the game | concept table | 1,536 terms → 935 concepts |
| 5 History | historical texts | Claude reads, Claude groups, rules, Claude links to concepts | practice table | 1,258 passages → 361 practices |
| 6 Situations | practices, concepts, game world | Claude proposes, Claude compares blind | activities, additions, comparison | 78 activities; 3 of 9 mini-games found blind |
| 7 Narrative | one mini-game, evidence | rules gather evidence, Claude plans and writes, Claude and rules check | cast, beats, checked lines | 7 mini-games planned, 6 with lines (127 lines) |
| 8 Game report | all of the above, game world | rules only (since version 32) | evaluation and issue drafts | 6 of 111 boats, 37 of 178 places in the game |

All Claude requests go through the page's `sample.json(prompt, {modelTier})`: tier `default` for
reading and sorting, `complex` for planning, writing, summarising and comparing. Each request is
retried once; "not allowed", "too many requests" and "unavailable" stop the run, keeping what
was done.

## Is everything up to date? What to run

| Step | State | To do |
| --- | --- | --- |
| Knowledge, Concepts: check against the game | 891 of 935 checked; no concept has its kind yet (new in version 32) | press **Check against the game** (it now also gives each concept its kind) |
| Knowledge, Concepts: summary of the sources | written on 12 November from the old table (633 concepts) | press **Write summary** |
| Knowledge, Practices | 361 practices from 17 sources, all linked to concepts | nothing |
| Knowledge, Boats and places | new in version 31 | press **Update the list**, then merge and correct cards |
| Situations | 78 activities, compared blind | nothing |
| Narrative | Upwind (31 lines), Whales (39), Seaweed (31) written, not checked | **Check lines** on each |
| Game report | last built 10:59 on version 29 | **Build report** (no Claude requests since version 32) |
| Sources | 43 of 44 have no licence, none has a reliability grade | fill in, in Sources |

## What the tool found: problems, with examples

The tool's main use, besides drafting the narrative, is to **surface problems**: in the sources
(they disagree, or leave things out), between the sources and the game, and in its own drafts.
Every example below is from the Tagus data. Each comes with where the tool found it and what to
do next.

### Dates

| Problem | Sources | Found by | Next step |
| --- | --- | --- | --- |
| The end of sail freight on the Tagus is dated **1951 and 1966** in one account, **"until the 1970s, ending with the Ponte 25 de Abril"** in another, and blamed on **road transport in the first quarter of the 20th century** in a third | getLISBON, Museu da Paisagem, Freire | grouping of practices (date) | the historian: probably different trades (cargo, ferries) ending at different times |
| The Lisbon–Azambuja **steamers stopped on 30 July 1857** when the railway opened, and stopped calling at Barquinha after **1862**: the same practice card also says sail freight declined in the 1950s–60s | Freire | grouping (date) | split the card: steam passenger service and sail freight are different practices |
| Master Reguinga's shipwreck and the festival it began are dated **1863** in one account and **1 July 1824** in another | *Mar da Costa* | grouping (date) | check the parish or newspaper record |
| The Rossio de Abrantes: boats **over 20 t until the early 1950s**, or **up to 30 t until the late 1950s** | Gaspar, another account | grouping (number and date) | the historian |
| 130 of 361 practices have **no date or period** at all, including well-attested ones (fragata crews and rowing, the muleta's fishing grounds, the xávega at Costa da Caparica) | all | rule: "no period" | look for dates in the sources, or accept "undated" |
| A single card spans **six periods**: 1857, 1950s, 1951, 1966, "the 1970s", "the first quarter of the 20th century" | — | the card's periods | a sign the card mixes several events |

### Places

| Problem | Example | Found by | Next step |
| --- | --- | --- | --- |
| **Old names** of places | *Punhete* (47 mentions) is today's Constância; *Aldeia Galega* or *Aldeagalega* is Montijo; "porto da Barquinha" is Vila Nova da Barquinha | sorting by kind gives the modern official name; the pack's `aliases.yaml` adds others | keep the old name for lines set in the past (the narrator can say *Punhete*), the modern one for the map |
| One place in **two areas** | the Mouchões, under the Tagus map and the Middle Tagus map | Boats and places | fixed by rule in version 31 (one card, the area most sources give) |
| Places **between the game's maps** | Santarém (6 sources), Chamusca, Azambuja, Valada, Muge, Porto do Sabugueiro | game report: "outside the game's areas" | an issue for the game's developers: a map area between Vila Franca and Constância |
| Well-attested places **missing on a map** | Mar da Palha, the bar (*Barra do Tejo*), Cais das Colunas, the Mouchões | game report: "missing" | an issue: name them on the Tagus map |
| A main landing that is **only a sea mark** in the game | Cacilhas | game report | an issue: make it a named place |
| Places Claude **could not place** | Porto de Arraiolos, Portos dos Frades, Porto da Cortiça (medieval river ports, 3 sources each) | "area unknown" | the historian, or a gazetteer |
| **Lists and routes** read as one place | "Peniche; Setúbal", "Lisbon to Santarém", "Tejo between Santarém and Cascais" | rules (version 27) | split or treated as the river itself |
| The **river itself** counted as a place | "Tejo", "Estuário do Tejo", "Margem Direita do Tejo", "Rio de Lisboa" | rules and the pack's aliases | counted as the area, not as a missing place |
| A place Claude wrote in a **line** but the game knows by another name | a line triggered at "Lisbon"; the game's port is "Lisboa" | export | mapped by the pack's aliases |

### Boat names

| Problem | Example | Found by | Next step |
| --- | --- | --- | --- |
| **Spellings** of one type | *barco d'água acima*, *barco de água acima*, *barcos d'água acima* | rules (merging "d'" and "de", plurals) | merged automatically |
| A **generic word** in front | "Barco Moliceiro" and "Moliceiro"; "barco catraio" and "Catraio"; "Barco Rabelo" and "Rabelo" | rules (the pack's `boat_words`) | merged automatically (version 29) |
| A place **after** the name | "Fragata do Tejo", "Batel do Tejo" | rules | merged |
| **Regional names** that may be one type | *barco d'água acima* and *barco de Riba-Tejo* (also written "Riba Tejo") | Boats and places | merge them with Move to… if a historian confirms (10 sources become 12) |
| **One word, several boats** | *bateira*: a cargo boat (one source), the Avieiro fishermen's boat they also lived on (another), a small boat on the Lisbon run (a third) | grouping (definition) | split into separate concepts: different *bateiras* |
| **A type and a family** | *barca* as one boat type, and as the general word for river boats; *bote* as a type, and in *bote de fragata*, *bote cacilheiro*, *bote de tartaranha* | term clash | decide which sources mean a type |
| **Synonyms across languages** | *vapor*, *barco a vapor*, "steamboat", "steamer", "steam passenger boat" | the pack's aliases | merged |
| A name **joining two boats** | "Muleta / Barino", "Canoa and Catraio" | rules (lists) | split |
| Boats **the sources name most that the game lacks** | barco d'água acima (10 sources), varino (9), barca (8), bote (7), batel (6), bateira (6) | game report | issues for the developers |
| The game's boats **no source names** | the Baleeiro, the Bac, the Pinasse | game report | look for Azorean, Arcachon and Aveiro-coast sources |

### Methods and practices

| Problem | Example | Found by | Next step |
| --- | --- | --- | --- |
| A source **disputes a source it quotes** | Duhamel du Monceau says muletas trawled sideways for sardines between Peniche and Setúbal; Pedrosa says that is wrong | grouping (description) | keep both; the narrative should not state either as fact |
| A source **contradicts its own documents** | Pedrosa says all muletas were cargo boats and none fished, but cites documents of 1620, 1633 and 1634–1645 showing muletas fishing | grouping (description) | the historian |
| A method **the source doubts** | Rebelo says the muleta paid out cable and hauled the net by hand for hours; Pedrosa doubts it | reading (kept as "the source doubts") | an activity may leave it out; a line may say "it is said" |
| **How the leeboard worked** | the *tábua de bolina* as a board lowered in shallow water, or as a fixed side keel, one each side on the muleta | grouping (definition) | ask a sailor; the game's muleta has one |
| **Dwellings** described differently | Costa da Caparica: only straw huts in 18th- and 19th-century accounts, but plank *palheiros* in the Ílhavo settlers' tradition; the only stone-and-wood house around 1900 a tavern, disputed by the editor (masonry by 1859) | grouping (description) | the historian |
| **The same figure, different scope** | 1,490 boats in 1552: on the whole Tagus with the estuary (mediotejo), or the river boats serving Lisbon (getLISBON) | grouping (description) | read the 1552 source |
| Practices with **no boat** | the xávega beach net, towing boats from the bank at Cachão do Cabril, lime shipments to Lisbon | rule: "no boat" (37 practices) | the activity step skips or asks for a boat |
| Practices **far from the game** | Nile irrigation, the Almourol dam project, curative springs, brandy distilling to save freight | situations skip them with a reason; the report lists them | leave them out in Knowledge |

### Numbers

| Problem | Example | Found by |
| --- | --- | --- |
| A **regulation** that contradicts itself | the 1572 *Regimento dos Barqueiros*: the batel from Lisbon to Almada carries at most 8 people (paragraph 19) or 12 (paragraph 61) | grouping (number) |
| A **rig** counted differently | a muleta's sails: 9 or 10 (Baldaque da Silva), up to 20 (Smyth, 1867), at least 20 (Folin, 1892) | grouping (number) |
| An **event** counted differently | boats seized by the English at the bar in 1650: 16 (English source), 14 (the king's letter) | grouping (number) |
| **Distances** | the Tagus permanently navigable for 85 km, or 65 km; traffic up to 20–30 km above Lisbon, or as far as the tide (Sabugueiro) | grouping (number) |
| **Sailing** against the game | the closest angle to the wind: 45–50° in the sailing course, about 36° for the game's Falua, 50° for the Rabelo; a square sail no closer than 50°, or braced to 35° | check against the game (number) |

### Terms and languages

| Problem | Example | Found by |
| --- | --- | --- |
| **Portuguese variants** | tack: *cambar* (Brazil) / *virar de bordo*, *dar por davante* (Portugal); gybe: *jaibe* / *virar em roda*; starboard: *boreste* / *estibordo*; shrouds: *brandais* / *ovéns*; leeway: *deriva* / *abatimento* | rule: variant difference (7 concepts) |
| **One word, two meanings** | *cambar*: a tack in the Brazilian course, a gybe in the method document; *mestre*: the master of a fishing crew, or a master boatbuilder; *painel*: an open stern panel, or the moliceiro's painted panels; *barra*: high-sea fishing beyond the bar, or the river-mouth limit | rule: term clash (38 words) |
| **No European Portuguese word** | 674 concepts, mostly from the Brazilian course and English sources | rule: missing term |

### The narrative's own drafts

| Problem | Example (line, then what the check said) | Found by |
| --- | --- | --- |
| An **invented detail** | Passengers: "… Obrigado pela moeda, menina." ("Thanks for the coin, miss.") → *the passenger paid with a coin*: unsupported | the independent claim check |
| An invented **exchange** | Supplies: "Passa cá o pão e leva o peixe da muleta pela água, fresco, que não espera." → *bread is handed over*, *the fish must arrive fresh*: unsupported | claim check |
| A **true name, wrong evidence** | Fishing: "Nas águas do Entre-Cabos" → the name is in the sources but not in that beat's evidence: unsupported | claim check |
| An added **cause** | Fishing: "Sem esse equilíbrio, não há abatimento de lado" → unsupported | claim check |
| **Sailing commands** with no source | Passengers: "Arriba! Folga, deixa encher!" → unsupported: the historical evidence describes work, not commands; such cues need the simulation's or the sailing course's evidence | claim check |
| **Numbers** that differ between PT and EN | 3 lines | rules |
| **Too long** | a story line of 26 words (limit 25 for that delivery) | rules |

### Readiness of the sources

| Problem | Example | Found by |
| --- | --- | --- |
| The only reference book is in **another variant** | Veleiro.net is Brazilian Portuguese; the project is European Portuguese | readiness rule; it predicted the variant problems above |
| **No licence, no grade** | 43 of 44 sources have no licence, none has a reliability grade | readiness rules |
| **Unreadable** sources | 4 could not be read | readiness rules |
| Author documents that **describe the game** | the story bible, the method document, the leaflet, the discussion summary: held out so the blind comparison is fair | readiness (blind comparison) |

### Mistakes of the tool itself (and their fixes)

| Problem | Example | Fixed |
| --- | --- | --- |
| A conflict that is not one | "Leeward: No conflict." recorded as a conflict; supply limits of 7, 10 and 20 *léguas* that are different rules | to remove by hand; the prompt asks to drop such cases |
| A concept reported **not shown** that the game has | the lateen sail (7 sources): the game's Muleta carries lateen-like sails, but the concept has no link to the simulation | to link by hand |
| Boats and places **counted several times** | "barco catraio" and "Catraio"; Lisboa and "Porto de Lisboa"; the Mouchões in two areas | versions 27–31 |
| Countries and seas counted as **places outside the maps** | Spain, the Indian Ocean, the Nile | version 27 (regions) |

---

## 1. Project

**What:** a form for the subject, audience, visit length, primary language with its variant,
other languages, learning goals, the simulation's simplifications, and tone. Saved as one
record (`project/main`).

**Why it matters later:** the subject, goals, visit length and audience go into every prompt;
the primary language variant decides which source terms count as the right ones (step 4) and
the glossary used in writing (step 7).

**Result:** "Boats of the Tagus", museum visitors, European Portuguese (pt-PT) first, English
second. Goals: the sailing concepts the simulation shows (points of sail, trim, tacking,
gybing) and the working life of the river's boats.

## 2. Materials

**What:** a registry of every source: kind (simulation, reference book, historical account,
author's document, existing activity, person who can check), title, link or file, language,
licence (open, CC0, copyright: cite and paraphrase only, permission, unknown), reliability (A
scholarly or museum, B documented local history, C uncited), read status and notes.

**Rules:**
- *Required fields per kind* (a historical account needs language, licence and reliability);
  missing ones show as "incomplete".
- *Held out:* "existing activity" items, and any item marked as describing the game's existing
  activities, are kept out of every input so the blind comparison (step 6) is fair.
- *Link check:* `tagus-linkcheck` (pipeline) reports each link as works, moved, broken,
  unreachable or not checked, with an archived copy when one exists.
- *Google Drive import:* walks a folder path (`projects/tagusnavy/historia`), lists the files,
  matches each to a material by title or proposes a new one, and stores the file's text.

**Result:** 44 materials: 36 historical accounts, 4 author's documents, 1 simulation (the
fragateiro physics), 1 reference book (Veleiro.net sailing course, Brazilian Portuguese), 1
existing activity (the game's mini-game list), 1 person (a historian). 5 held out (the
existing activities, the story bible, the method document, the leaflet, the discussion summary).

**Example of relevant information:** the registry is where copyright is decided. Only one source
is marked "cite and paraphrase"; the other 43 have no licence, so the tool treats all of them as
copyrighted (paraphrase, never quote) and warns before sending their text to Claude.

**Problems found at this step (examples):**
- *Licences and grades:* 43 of 44 sources have no licence, none a reliability grade.
- *Titles from file names:* "BOOK Territorios da Lisboa Medieval 3 22", "jorgeGasparOsportosfluviaisdoTejo",
  "(9) Facebook": the Drive import keeps file names, which then appear in credits and reports
  until the author corrects them.
- *Unreadable sources:* 4 web pages could not be read (blocked or gone); the link check offers
  archived copies.
- *Sources about one area only:* nothing on the Azores, Arcachon or the Aveiro coast, although
  the game has boats there.

## 3. Readiness

**What:** before any reading, a check of whether the materials can support each knowledge base.

**Rules** (`readiness()`), one block per base, each finding graded ok, note, gap or blocks:
- *Project:* missing subject, audience, visit length, primary language or its variant, goals.
- *Simulation:* at least one simulation item; someone who can confirm it (a developer).
- *Concepts:* reference books in each project language and variant, completeness.
- *History:* at least one account; grade A sources; ungraded, unknown licence, unread, dead
  links; half or more grade C; a historian listed.
- *Blind comparison:* something held out; author documents that may mention existing activities.

A base is *blocked* if any finding blocks, *usable with gaps* if any is a gap, otherwise *ready*.

**Claude's second look** sends the metadata (never the texts) and the rule findings:

> Fixed rules have already produced the findings listed in ruleFindings. Do not repeat them.
> Suggest up to 8 further gaps, risks or contradictions that a careful researcher would notice
> from the titles, notes and metadata … Do not invent facts about the subject.

**Result:** simulation ready; concepts usable with gaps; history usable with gaps; blind
comparison ready.

**Example of relevant information:** "The Portuguese reference books are Portuguese (Brazil),
not Portuguese (Portugal): terms may differ, so each term needs checking." This warning came true
in step 4: the course says *cambar* and *jaibe*, the Tagus sources *virar por davante* and
*virar em roda*.

**Problems found at this step (examples):** the only reference book in the wrong variant of
Portuguese (above); 5 author documents that describe the game's existing activities, held out
so the blind comparison stays fair; nobody listed to check the concepts (an instructor); and a
historian listed but not yet named.

## 4. Concepts

Goal: the concepts a visitor can learn, each backed by sources, with its terms per language and
whether the game shows it.

### 4a. Getting the text

pdf.js extracts a PDF's text layer page by page with a `[page N]` marker before each page (a
scan with no text layer is refused); Google Drive files come through the Drive connector;
anything else is pasted. **Result:** 21 sources with text, about 0.9 million characters.

### 4b. Reading: extracting candidate concepts

**Algorithm:** the text is cut into pieces of at most 6,000 characters at page, section or file
markers (`chunks()`), one request per piece, in order, saved after each piece (a stopped run
resumes). Within a source, candidates with the same normalised term are merged. Each gets an id
(source, text length, number); a changed text is read again.

**Prompt** (`extractPrompt`), per piece:

> Read part i of n of one source and list the concepts a visitor could learn from it.
> - A concept is a skill, manoeuvre, force, condition or state, or a part or term needed to
>   explain one. Keep everything on the subject; the author decides scope later.
> - term: exactly as written in the source, in the source's language.
> - definition: your paraphrase in English, at most 25 words. Never copy sentences from the source.
> - location: the [page N], [section: …] or [file: …] marker the term falls under.
> - numbers: only values the source states (angles, speeds, limits), with what they measure.
> - One item per distinct term, at most 30 items. Do not add anything that is not in the text.

For the simulation's own description, a concept is something the player does or experiences
that the simulation computes, detects or controls, and `measured_by` names the signal, event or
control.

**Result:** 1,536 candidates from 19 sources. Most: Pedrosa, *A Muleta e a Tartaranha* (220),
Veleiro.net (178), the moliceiro heritage file (175), Gaspar, *Os portos fluviais do Tejo* (134),
*Territórios da Lisboa Medieval* (130).

**Example (one candidate):** Veleiro.net, page 7, term *Orça Fechada* (pt-BR): "Close-hauled:
sailing as close to the wind line as possible, heading against it."

### 4c. Grouping: relations between candidates

A relation here means **"these candidates name the same concept"**, decided by meaning, not
spelling.

**Algorithm:** candidates in order of source kind (simulation, reference books, author documents,
historical accounts), in batches of 50, are placed into the table built so far
(`assignPrompt`), which is sent with each concept's id, label and a short meaning. Candidates
not placed become concepts of their own. Existing concepts, decisions and moves are kept.

**Prompt** (`assignPrompt`):

> For each candidate: if it means the same as an existing concept, give that concept's id.
> Otherwise give a short English label for a new concept … Group by meaning, never by spelling:
> the same word can mean different things in different sources or language variants. …
> Also report real conflicts between a candidate and the concept it joins: different numbers for
> the same quantity, or a different definition. A different language, variant or synonym … is
> not a conflict, and neither is a simulation describing how it models something, unless its
> values or behaviour contradict the source.

**Author review:** each concept is a card; the author moves a term ("Move to…"), renames,
confirms ("Group is right") or drops it ("Leave out").

**Result:** 935 concepts. 771 rest on one source, 93 on two, 36 on three, 35 on four or more.
By kind of source: 718 only from historical accounts, 129 only from the reference book, 44 only
from the simulation; 11 join history and the reference book, 4 history, the reference book and
the simulation.

**Example (one concept card, "Close-hauled"):**

| Source | Term | Meaning (paraphrase) | Where |
| --- | --- | --- | --- |
| fragateiro (simulation) | close-hauled | as close to the wind as possible, sails hauled in | PHYSICS.md, Sails and sheets |
| Veleiro.net (pt-BR) | Orça Fechada, orça | as close to the wind line as possible | pages 7, 22 |
| Method document | bolina | as close to the wind as the rig permits; the only way to gain ground upwind | Foundations |
| Moliceiro heritage file | bolinar | sailing close to the wind to gain windward distance | — |

Linked to the simulation's *no-go zone* and *polar*; scope core; one conflict (below).

**Example of a grouping error to fix by hand:** the card "Sheet" holds the pt-PT verb *caçar*
(to sheet in), which belongs in "Sheeting in": the same word sits in two cards (a *term clash*,
see 4d).

### 4d. Statuses: fixed rules over each group

| Status | Rule | Count |
| --- | --- | --- |
| single source | all non-simulation members come from one source | 727 |
| not in simulation | no simulation member and no simulation link | 698 |
| missing term | no member in pt-PT | 674 |
| out of scope | step 4e proposed "out" | 430 |
| term clash | the same word, in one language, in two concepts | 74 |
| simulation only | only the simulation names it | 44 |
| agreed | none of the others | 23 |
| conflicting | a reported conflict | 12 |
| variant difference | pt-PT and pt-BR members share no term | 7 |

**Examples:**
- *Agreed* (several sources, no problem, and the game shows it): shallow draught (8 sources),
  rudder (7), *arrais* (skipper, 7), flat-bottomed hull (7), keel (6), *muleta* (6), *falua* (6).
- *Variant difference*, the most useful finding for writing lines: tacking (pt-BR *cambar*,
  *cambada*; pt-PT *virar de bordo*, *dar por davante*), gybing (*jaibe*; *virar em roda*),
  starboard (*boreste*; *estibordo*), shrouds (*brandais*; *ovéns*), leeway (*deriva*;
  *abatimento*).
- *Term clash* (38 words in two or more cards). Duplicates to merge: *boca* (beam) twice,
  *vela grande* in "Mainsail" and "Muleta main sail", *fragatas* in "Fragata" and "Fragatas of Vila
  Nova da Barquinha", *cais* in "Quay" and "River landing places". Real double meanings, to keep
  apart: *barca* (a boat type, and the ferry barca at Porto do Tejo), *mestre* (the master of a
  fishing crew, and a master boatbuilder), *painel* (a stern panel, and the moliceiro's painted
  panels), *barra* (fishing beyond the bar, and the river-mouth limit), *cheias* (floods, and the
  silt they leave, *nateiros*).
- *Conflicting* beyond sailing: *bateira* described as a cargo boat, as the Avieiros' fishing
  boat and home, and as a small boat on the Lisbon run; the batel's passenger limit (8 or 12); the
  barco da carreira (one boat a week, 2–4 per route, 100 from Abrantes in 1552).
- *Single source* (727 concepts): for example most of the moliceiro's terms (only the moliceiro
  heritage file), and most medieval terms (only *Territórios da Lisboa Medieval*).

### 4e. Check against the game: concept to simulation, and relevance

**Prompt** (`linkPrompt`), 30 concepts at a time, with the learning goals, visit length and
simplifications:

> - sim: ids of simulation concepts that show or measure it. Link only when the simulation
>   really lets the player see or do it …
> - numbers: if a number stated for the concept disagrees with the simulation's number for the
>   same quantity … describe it in one sentence naming both values.
> - scope: "core" if it serves the learning goals and a visitor can meet it in the game or its
>   stories; "maybe" if useful context; "out" if it does not fit a short museum visit on this
>   subject (for example modern yacht fittings, safety drills, unrelated topics).
> - keep: the indices of the listed conflicts that are real disagreements.

**Relevance of a concept is decided here:** core, maybe or out. Out-of-scope concepts leave the
later steps unless the author confirms them.

**Result:** 891 of 935 checked: 131 core, 330 maybe, 430 out; 187 linked to the simulation; 5
number conflicts found by this check.

**Examples with Claude's reason:**
- core: close-hauled ("central point of sail; shown in polar and no-go zone"), in irons ("sails
  flap, speed near zero"), sheeting in ("sheet control directly lets player trim in");
- maybe: reefing ("sail reduction context; not a simulated control"), gaff rig ("Fragata rig;
  useful boat context"), lying athwart wind and current ("working life; sim has no current");
- out: storm sail ("modern storm jib detail"), boom vang ("modern yacht fitting, not modelled"),
  topping lift, halyard, shrouds ("rigging detail, not simulated").
- Beyond sailing: *core*: the *barcos d'água acima* ("working life of the river's cargo boats"),
  the *arrais* ("skipper at the helm; the player steers"), the *camaradas* ("working life of
  crew; the simulation omits crew"), the river landing places ("ports where cargo was loaded;
  game ports"); *maybe*: towing from the bank ("not simulated"), the helmsman ("crew not
  simulated").

**A problem this step revealed:** the only sailing course is about **modern yachts**, so many of
its terms are out of scope for traditional river boats: winch, cockpit, genoa, spreader, cleat,
turnbuckle, lifeline ("yacht term, not for traditional river boats"). The concepts the game
needs (the lateen rig, the leeboard, poling, towing) come from the historical sources instead.
Scope now: 131 core, 330 maybe, 430 out.

### 4f. Summary of the sources

**Prompt** (`summaryPrompt`): sort the concepts into 4 to 8 types; per type, agreements,
conflicts with a next step, clarifications and gaps; an overview of the conflicts to settle
first. "Do not add facts that are not in the table."

**Result (from the old table, to rewrite):** "Settle first (1) the sailing vocabulary, where
*cambar* means tack in the Brazilian course and gybe in the method document, while the
historical sources give the European terms (*virar por davante*, *virar em roda*); (2) the
closest angle to the wind, 45–50° in the course against about 36° in the game; (3) dates and
figures in the history."

## 5. History

Goal: what people did with boats on the river, each practice backed by passages.

### 5a. Reading: extracting practices

The same pieces of text (historical accounts only). **Prompt** (`practicePrompt`):

> List what people did with boats and the river: practices, rules and events.
> - One item per distinct practice or event: a work routine (a fishing method, a cargo run, a
>   ferry crossing, towing, building or repairing boats), a rule (a regulation, fee or licence),
>   a dated event (a ban, a survey, a new service), or a description of a boat or place without
>   action.
> - action: your English paraphrase, at most 25 words. Never copy sentences.
> - who, boat, place, period, cargo, gear, conditions: as the text states them … "" when the
>   text does not say. numbers: only values the text states. Do not add anything that is not in
>   the text.

**Result:** 1,258 passages from 17 sources; most from Gaspar (252), Pedrosa (196), the moliceiro
file (172), *Territórios da Lisboa Medieval* (122).

**Example (one passage):** Pedrosa, page 23: "Duhamel Du Monceau says muletas trawled sideways
like Mediterranean tartanas, fishing sardines at night between Peniche and Setúbal"; gear: nets,
fire for night fishing (*candeio*); crew 5–6 men.

### 5b. Grouping: relations between passages

A relation means **"these passages describe the same practice or event"**. Batches of 40
(`hAssignPrompt`):

> If it describes the same practice or event as an existing one (the same activity by the same
> kind of people or boat; places and periods may differ), give that practice's id. …
> Report real disagreements: "date" …, "number" …, "description" (accounts that cannot both be
> true). More detail, or the same practice in another period, is not a conflict.

Each practice's boats, places and periods are the union of its members'.

**Statuses** (rules): conflicting; single source; agreed (two or more sources, no conflict); no
boat; no place; no period; no concept.

**Result:** 361 practices: 111 practices, 69 events, 26 rules, 155 descriptions. 309 on one
source, 35 on two, 17 on three or more. 12 with conflicts (6 number, 5 description, 3 date). 130
without a period, 24 without a place, 37 practices without a boat.

**Problems found at this step (examples):**
- *Dates:* Master Reguinga's shipwreck and festival, 1863 or 1 July 1824 (*Mar da Costa*); the end
  of sail freight, 1951/1966, the 1970s, or the early 20th century.
- *Methods:* Duhamel du Monceau's sardine trawling disputed by Pedrosa; Pedrosa saying no muleta
  fished while citing documents of muletas fishing; the Costa da Caparica huts, straw or plank.
- *Numbers:* the batel's 8 or 12 passengers in one regulation; 16 or 14 boats seized in 1650.
- *Scope:* 1,490 boats in 1552, on the whole Tagus or only serving Lisbon.
- *Old place names* kept as written: *Punhete* (Constância), *Aldeia Galega* (Montijo).
- *Missing information:* no period for well-attested practices (fragata crews, the muleta's
  fishing grounds); no boat for the xávega beach net.

**Example (one practice card, "Muleta sideways trawling"):** boats *muleta*, *batel*; places
Seixal and Barreiro, between Peniche and Setúbal, the Tagus estuary; periods 1772, 1891. Passages:
Pedrosa (introduction: the net cast to windward, the boat drifting across the wind), Pedrosa
(Baldaque da Silva on balancing the sails against wind and current, with the long poles,
*botalós*), Pedrosa page 23 (Duhamel Du Monceau), *Embarcações do Rio Tejo* (muleta and batel
trawling from the side with the *tartaranha*). Linked concepts: trawling broadside, windward,
drifting with current and wind, the *tartaranha* net, lying athwart wind and current.

**Best supported practices:** freight of the *barcos d'água acima* between the Ribatejo and
Lisbon (4 sources), river traffic linking the banks until the mid-20th century (4), supplying
ships at anchor in Lisbon (3).

### 5c. Practice to concept

**Prompt** (`hLinkPrompt`): "give the ids of the concepts it exercises or shows … at most 6, and
a note of at most 12 words on how. This is an interpretation: sources describe work, not
technique, so link only what the practice clearly involves." **Result:** 351 of 361 practices
linked to at least one concept.

## 6. Situations

A situation is where all three bases agree: a practice, its concepts, a simulation that can play it.

### 6a. Proposing activities

**Input:** practices (not dropped), 15 at a time, each with boats, places, periods, number of
sources, actions, conditions, cargo and linked concepts; the game's boats, areas and ports; the
concepts the game shows. **Not** the game's existing activities.

**Prompt** (`proposePrompt`), in short:

> Each activity must come from one historical practice below and let the player do a
> recognisable part of it in the game. … title, goal, success (a rule the game can measure),
> boat (one of the game's boats …), area and route, concepts, minutes (1 to 6), level (1 basics,
> 2 manoeuvres, 3 specialised work), simplifications, needs, feasibility ("full", "simplified",
> "needs feature"), features (from a fixed list), premise (only facts in the practice record).
> Do not skip a practice only because the game lacks something … Skip only practices with no
> boat or water activity at all … and say why.

**Result:** 72 activities: 3 full, 37 simplified, 32 needing a game feature; 28 at level 1, 35 at
level 2, 9 at level 3. 16 practices skipped (ox-cart transport to the river ports, petitions on
the French *tartana*, early illustrations: no water activity).

**Examples:**
- *Full:* "Crossing between the banks" (level 2, 4 min, Falua, Lisboa–Almada–Seixal): "cross from
  Lisboa to Almada and back within 5 minutes, with at least one tack or gybe". From the practice
  "river traffic linking the Tagus banks until the mid-20th century". Leaves out: no current, no
  passengers or goods shown.
- *Full:* "Leeboard down" (level 1, Muleta): sail close-hauled and keep leeway below a set angle
  for 60 seconds.
- *Simplified:* "Back upriver with the wind" (Fragata, Lisboa to Vila Franca de Xira): reach the
  quay in 6 minutes with at least 2 tacks. Needs current to make upriver sailing truly harder.
- *Needs feature:* "Becalmed fragata": make progress in a weak wind and see why a fragata needed
  a rowed tow; needs rowing, towing and crew.

**Game additions** (counted over all proposals): cargo loading and weight (25 activities), a new
map area (18), a new boat (16), crew and tasks aboard (11), fishing net and catch (9), tide and
current (8), water depth and shallows (7).

**Problems found at this step (examples):**
- *Boats the game lacks, replaced:* the *barcos d'água acima* by the Fragata ("the closest game
  boat"), the steam cargo boats by the Fragata, the tartana by the Muleta, the rasca by the
  Muleta ("both ventured beyond the bar"). Each substitution is written down and is a finding for
  the developers.
- *Places the game lacks:* "Fair wind to Lisbon" needs "a continuous map from the Ribatejo to
  Lisboa"; "Coastal trade leg" needs the Algarve and Morocco.
- *Mechanics the game lacks:* a net and its hauling ("Haul the net broadside"), a towed rowing
  boat ("Becalmed fragata"), shallows and a ship to follow ("Pilot across the bar"), switchable
  rigs ("Change the rig").
- *Practices that are not activities,* skipped with a reason: boatmen leaving for the railway or
  lorry driving; brandy distilling to save freight; flood dikes; riverbank angling ("done from
  the shore, with no boat"); the xávega ("names no boat or sailing").

### 6b. Blind comparison with the game's activities

**Prompt** (`comparePrompt`): for each game mini-game, the closest proposal and the match
("same", "related", "none"); for each proposal, whether the game has it ("same", "related",
"new").

**Result:** of the game's 9 mini-games, **3 found the same** without seeing them, 5 related, 1 not:

| Game mini-game | Match | Closest proposal | Why |
| --- | --- | --- | --- |
| Passengers (Catraio) | same | Small catraio crossing | both cross between Lisbon and Almada by catraio |
| Seaweed (Moliceiro) | same | Moliço run | both sail a moliceiro to the *moliço* grounds in the Ria de Aveiro |
| Fishing (Muleta) | same | Haul the net broadside | both sail a muleta broadside to drag the trawl |
| Upwind | related | Back upriver with the wind | same practice (tacking), Fragata going upriver, not a Falua to a mark |
| Downwind | related | Festival day regatta run | running with sails out, but a Moliceiro |
| Cargo (Fragata) | related | Timber to the Tercenas | Fragata cargo in busy traffic, but downriver delivery |
| Supplies (Canoa) | related | Supply run to the anchored ship | out to a vessel and back, by Catraio |
| Whales (Baleeiro) | related | Sail to the distant fishing banks | same boat, but a long voyage |
| Free sailing | none | — | no proposal is free sailing |

Of the 72 proposals, 7 match a game activity, 54 are related and 11 are new. **Examples of new
activities the game lacks:** docking at the Cais das Colunas, the becalmed fragata, the quay of
the steam cargo boats, piloting across the bar, changing the rig, shortening sail.

## 7. Narrative

### 7a. Gathering evidence (rules, no Claude)

`evidenceFor()` takes, in order: the practice of the proposal the blind comparison matched to
the mini-game; up to 5 more practices with the same boat, **most sources first**; up to 6
passages of each; up to 10 linked concepts with 2 source terms each. At most 45 evidence records
(`e1`…). **Relevance for the narrative:** matched blind, then same boat, then number of sources.

Also: the places the boat may pass (ports and landmarks of the area, minus landmarks built after
the chosen period, plus places in the evidence), the 33 game moments, the author's story bible
if it mentions the boat, and a glossary of pt-PT terms to use and variants to avoid.

### 7b. Planning cast and beats

**Prompt** (`planPrompt`): 1 to 3 invented characters labelled fictional, whose trade comes from
the evidence; 4 to 6 beats (setup, complication, turn, close) plus leg beats (`steady_leg`) and
place beats (`near_place:<name>`); "never put a story line on a difficult moment: a difficult
moment gets at most a cue, and the story continues as a reflection after it is solved"; each beat
with a trigger, delivery, character, gist, concept and evidence ids.

**Example ("Fishing with the Muleta"):** cast: Arrais Joaquim (fictional skipper of a Seixal
muleta in the 1880s) and Manel (the youngest of the 5 or 6 crew). Beats: setup at `start`; a leg
pool at `steady_leg`; a place beat at `near_place:Seixal`; a cue when the sail starts luffing; a
reflection when it stops; a close at `catch`; a curiosity card at `net_out`. Evidence came from
6 practices (sideways trawling, the fishing grounds, the origins of the muleta…).

### 7c. Writing lines

**Prompt** (`linesPrompt`): two candidates per beat (a pool for leg beats), pt-PT and English,
word limits (cue 6, reflection 25, story 35, curiosity 60), the glossary, and: "Use only facts in
that beat's evidence. Names of characters, feelings and small actions are colour: they must not
state checkable facts … claims: every factual statement in the line, each with the evidence ids
that support it."

### 7d. Checking lines

Claude checks each claim independently ("supported", "unsupported", "contradicted"); rules check
word limits, that every number is in the evidence, the same numbers in PT and EN, no landmark
newer than the period, no avoided variant term. A line is **verified** when everything passes,
otherwise **needs work**; the author approves.

**Result:**

| Mini-game | Evidence | Beats | Lines | Verified | Needs work | Not checked |
| --- | --- | --- | --- | --- | --- | --- |
| Passengers (Catraio), with story bible | 35 | 7 | 14 | 3 | 11 | |
| Supplies (Canoa) | 42 | 6 | 13 | 9 | 4 | |
| Fishing (Muleta) | 42 | 7 | 15 | 12 | 3 | |
| Seaweed (Moliceiro) | | 7 | 15 | | | 15 |
| Cargo (Fragata) | 44 | 6 | 0 | | | |

Of 94 checked claims, 79 were supported and 15 unsupported (none contradicted); 3 lines had
different numbers in PT and EN, 1 was too long.

**Examples:**
- *Verified* (Fishing, setup): "Largamos do Seixal. A muleta não corre atrás do peixe de proa.
  Vai atravessada ao vento e à corrente, a arrastar a tartaranha pelo costado." / "We leave
  Seixal. The muleta doesn't chase fish bow-first. She lies across wind and current, dragging the
  tartaranha from her side." Both claims supported by Pedrosa and *Embarcações do Rio Tejo*.
- *Verified* (Fishing, leg pool): "E estes paus compridos, à proa e à popa? São os botalós, Manel.
  Neles se armam as velas e se amarram as asas da rede."
- *Needs work* (Fishing, leg pool): "… entre o Cabo da Roca e Setúbal. Nas águas do Entre-Cabos."
  The fishing grounds are supported; the name "Entre-Cabos" for them is not in that beat's
  evidence (it is in another record), so the check flags it.
- *Needs work* (Fishing, reflection): "Sem esse equilíbrio, não há abatimento de lado." Claude
  added a cause the evidence does not state.

**To fix:** the Seaweed plan has a place beat at `near_place:Ria de Aveiro`, which is an area,
not a place; the game's check would reject it.

**Problems found at this step (examples, more in "What the tool found"):** invented details
("Obrigado pela moeda, menina": nothing says passengers paid with a coin), an invented exchange
of bread for fish, a true name used without its evidence (*Entre-Cabos*), an added cause ("without
that balance there is no sideways drift"), sailing commands with no source behind them ("Arriba!
Folga, deixa encher!"), numbers that differ between Portuguese and English, a line one word too
long. 15 of 94 checked claims were unsupported; none contradicted the evidence.

## 8. Game report

The full report of 14 November, with every boat, place, concept and practice, is in
[`docs/game-report-2026-11-14.md`](game-report-2026-11-14.md). Problems it found, in short:
boats the sources name most that the game lacks (the *barco d'água acima*, the varino, the
barca, the bote, the batel, the bateira); places between the game's two Tagus maps (Santarém,
Chamusca, Azambuja, Valada, Muge); well-attested places with no name on the map (Mar da Palha,
the bar, Cais das Colunas, the Mouchões) or only a sea mark (Cacilhas); 13 concepts that need
tide or current and 11 that need water depth; 60 practices with no activity (the crew of a
barco d'água acima, the fragata's rowed tow, *xávega* beach nets, the royal journeys
Almeirim–Lisbon).

**1. Sorting by kind** (`classifyPrompt`), 40 at a time, retried in 15s: boat, place, sailing,
hull, practice, role, cargo, event, regulation, internal, other; the modern name for boats and
places, the game area of a place, and what the simulation would need for what it does not show.
**Result:** 1,346 items sorted: 403 places, 276 boats, 179 hull, 117 sailing, 73 practices.

**2. Matching against the game (rules):** a boat is *in game*, *in development* or *missing*; a
place is a *port*, *landmark*, *on map*, *sea mark only*, *outside the game's areas*, *area
unknown* or *missing*. Boats and places from concepts and from practices are merged by name and
area, each keeping the sources that name it.

**3. Physics:** sailing and hull concepts *shown*, *not shown* (with what is needed) or *out of
scope*. **4. Practices against activities** (`activityPrompt`): *covered*, *partly*, *missing*.
**5. Conflicts, anachronisms, game additions.**

**Relevance:** every finding counts its **independent sources**; issue drafts are written only for
findings with at least the chosen number of sources (default 2), most sources first.

**Detailed report:** the report of 14 November, 10:59 (workbench version 29, game `1d66225`)
is written up in full in [`docs/game-report-2026-11-14.md`](game-report-2026-11-14.md): 6 of 111
boats and 37 of 178 places in the game, 133 of 190 sailing and boat concepts shown, 10 of 111
practices covered and 41 partly, 11 conflicts, the game additions, recommendations for the
game's developers, and every list in the appendices.

The earlier figures below are from the report of 07:11, kept to show how the fixes changed it.

**Result (report of 14 November, 07:11, on the old world list):**

| | In the game | Not in the game |
| --- | --- | --- |
| Boats (129) | 6: Fragata (11 sources), Falua (7), Muleta (7), Canoa (5), Catraio (3), Moliceiro (2) | 123 |
| Places (202) | 38: Lisboa (12), Vila Nova da Barquinha (8), Vila Franca de Xira (8), Abrantes (7), Montijo (7)… | 121 missing or outside, 43 area unknown |
| Sailing and hull (219) | 132 shown | 50 not shown, 37 out of scope |
| Practices (85) | 7 covered, 26 partly | 52 missing |

**Examples of relevant findings:**
- *Boats the sources name most that the game lacks:* Varino (10 sources), *barco d'água acima*
  (10), Barca (9), Bote and Bote cacilheiro (7 each), the steamboat (7), Batel (6), Bateira (6).
- *Places:* Mar da Palha (6), the Esteiros (6), Mouchões (5), Cais das Colunas (3) are missing
  on the Tagus map; Santarém, Chamusca and Azambuja lie outside the game's maps (upriver).
- *Not shown by the simulation:* lateen sail (7 sources; to check: the game's Muleta has
  lateen-like sails, so this may be a classification error), silting of the riverbed (6, needs
  water depth), floods (3), sailing upstream (3, needs current), towpaths (3, needs towing from
  the bank). Most requested: tide and current, water depth.
- *Practices covered:* the Ribatejo–Lisbon freight run (the route Vila Franca–Lisboa), river
  traffic between the banks (transport missions), the muleta's fishing grounds (fishing).
  *Partly:* fragatas handling cargo in Lisbon harbour (Cargo mini-game, but no loading).
  *Missing:* crew roles aboard the *barco d'água acima*, the fragata's rowed tow, the royal
  boat journeys Almeirim–Lisbon.
- *Game additions (activities unlocked / improved, sources):* new map area 15 / 4 (8 sources),
  new boat 14 / 2 (9), cargo loading and weight 12 / 18 (12), crew and tasks 8 / 5 (11).

**Noise in this report, fixed in workbench version 27:** the river itself ("Tejo", "Tagus",
"Estuário do Tejo", "Tagus between Abrantes and Azambuja") was counted as a missing place; the
same boat appeared under several names (*barco a vapor*, *vapor*, steam passenger boat;
*barco d'água acima* twice); fields listing several places ("Peniche; Setúbal") and routes
("Lisbon to Santarém") were counted as places; countries and seas (Spain, the Indian Ocean)
were counted as places outside the maps. Version 27 counts the river and its stretches as the
area itself (names from the pack's `aliases.yaml`), sorts countries, seas and regions apart,
merges spellings and translations into one name, splits lists and leaves routes out. Tried on
today's data, places missing or outside the maps fall from 121 to about 77 and boats missing
from 123 to about 108, before Claude's new sorting merges the remaining spellings. Anachronisms:
none, because no narrative has a period set yet.

---

## Statistics of conflicts

Conflicts are found at three levels: between sources (Claude, while grouping), between sources
and the game (Claude, in the check against the game), and between word forms (rules). Counted on
today's data, and sorted by what they are about:

| Kind | Count | Found by | Examples |
| --- | --- | --- | --- |
| **Terminology: Portuguese variants** (pt-PT against pt-BR) | 7 concepts | rule (variant difference) | *virar de bordo / cambar* (tack); *virar em roda / jaibe* (gybe); *estibordo / boreste*; *ovéns / brandais*; *abatimento / deriva* |
| **Terminology: one word, two concepts** | 38 words (74 concepts) | rule (term clash) | *caçar* in "Sheet" and "Sheeting in"; *boca*; *vela grande*; *barca*; *mestre*; *painel*. Mostly duplicates to merge, some real double meanings |
| **Terminology: no pt-PT word** | 674 concepts | rule (missing term) | most concepts from the Brazilian course or English sources |
| **Sailing numbers** (angles, sail settings) | 4 | Claude, grouping and check against the game | closest angle to the wind 45–50° in the course against about 36° in the game (Rabelo 50°); downwind sail at 90° against no matching angle in the game; square sail no closer than 50° against "braced to 35°" |
| **Definitions that differ** | 3 | Claude, grouping | *tábua de bolina*: a lowered board (one source) or a fixed side keel (another); a gust: a stronger wind, or also a change of direction (the game); *bateira*: a cargo boat, or the boat the Avieiro fishermen lived on |
| **Historical quantities** | 5 | Claude, grouping | the batel's passenger limit, 8 or 12 (two paragraphs of the 1572 *Regimento dos Barqueiros*, found twice); a muleta's sails, 9–10 (Baldaque da Silva) or up to 20 (Smyth 1867, Folin 1892); boats seized at the bar in 1650, 16 or 14; boats per route on the scheduled service |
| **Geography** | 3 | Claude, grouping | the Tagus permanently navigable for 85 km or 65 km (found twice); traffic up to 20–30 km above Lisbon, or as far as the tide (Sabugueiro) |
| **Dates** | 4 | Claude, grouping | decline of sail freight dated 1951 and 1966, against "until the 1970s" (Museu da Paisagem) and the end of the Lisbon–Azambuja steamers in 1857 after the railway (Freire); Rossio de Abrantes: boats over 20 t until the early 1950s, or up to 30 t until the late 1950s; Master Reguinga's shipwreck and festival, 1863 or 1 July 1824 (*Mar da Costa*) |
| **Accounts that cannot both be true** | 2 | Claude, grouping | Costa da Caparica: straw huts in 18th–19th-century accounts, plank *palheiros* in the Ílhavo tradition; the only stone-and-wood house around 1900 a tavern, disputed by the editor (masonry by 1859) |
| **Same figure, different scope** | 1 | Claude, grouping | the 1552 count of 1,490 boats: the whole Tagus (mediotejo) or the river boats serving Lisbon (getLISBON) |
| **A source against what it quotes** | 2 | Claude, grouping | Pedrosa says Duhamel Du Monceau was wrong about muletas fishing at sea; Pedrosa says no muleta fished, while documents he cites (1620, 1633, 1634) show them fishing |
| **Not real conflicts (noise)** | 3 | Claude | "No conflict" written as a conflict; supply limits of 7, 10 and 20 *léguas* that are different rules; a muleta crew size "that may differ" without a second figure |

In short: Claude reported 27 conflicts (13 between concepts, 14 between practices); 24 are real
and 3 are noise. Numbers are the most common (12: sailing angles, historical quantities,
distances), then dates (4), definitions (3) and differing accounts (2). Terminology is by far the largest problem
overall, but it is found by the rules, not by Claude: 7 concepts where the Portuguese variants
disagree, 74 words used in two concepts, and 674 concepts with no European Portuguese word yet.

---

## How relations are made, in summary

| Relation | Made by | Kept as |
| --- | --- | --- |
| candidate ↔ candidate (same concept) | Claude, by meaning, in batches; author moves | concept members |
| passage ↔ passage (same practice) | Claude, by activity and kind of people or boat; author moves | practice members |
| concept → simulation | a simulation candidate in the group, or Claude's check against the game | `simLinks` |
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

- Claude's extraction and grouping are drafts; a different run can group differently. The
  author's moves and decisions are the reference.
- Reading is slow (one request per piece of text, one at a time) and sends copyrighted text to
  Claude; the plan is to re-read on a local model.
- The report's merging of names depends on Claude giving one name per boat or place, and on the
  pack's list of other names for each area (`domains/sailing/aliases.yaml`).
