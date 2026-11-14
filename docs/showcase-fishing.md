# Showcase: from a page in a book to a line in the game

One example followed through every step of the authoring tool: how one paragraph of a history
of the *muleta* becomes the first thing the skipper says in the game's mini-game *Fishing with
the Muleta*. Everything below is real data from the workbench (snapshot of 14 November 2026,
`data/workbench/`), not an illustration.

```
Source ─► passage ─► practice ─┬─► concepts ─► situation ─► narrative ─► checked line ─► game
                               └─► boats and places ──────────────────────────────┐
                                                                 game report ◄────┘
```

| Step | Tool tab | Who does what | What it produced for this example |
| --- | --- | --- | --- |
| 1 | Project | the author fills a form | subject, audience, pt-PT first |
| 2 | Sources | the author registers the source; rules check readiness | Pedrosa, *A Muleta e a Tartaranha*: historical, pt-PT, licence unknown |
| 3a | Knowledge: reading | Claude paraphrases each piece of text | a passage from page "1. Introdução" |
| 3b | Knowledge: Practices | Claude groups passages; rules give statuses | the practice "Muleta sideways trawling" |
| 3c | Knowledge: Concepts | Claude groups terms and links them to the game | "Trawling broadside", core, shown by the game |
| 3d | Knowledge: Boats and places | rules merge names | "Muleta": 8 sources, in the game |
| 4 | Situations | Claude proposes activities, without seeing the game's | "Haul the Net Broadside", the same as the game's Fishing mini-game |
| 5 | Narrative | rules gather evidence; Claude plans, writes and checks; the author approves | a skipper, a beat, a verified line in PT and EN |
| 6 | Export | a script writes the game's line bank | `fishing.b1.l1` in `content/narrative/from-tool/lines/fishing.json` |
| 7 | The game | the game's narrator plays it | a caption when the mission starts |
| 8 | Game report | rules assemble the findings | the Muleta's fishing is covered; hauling the net is not |

---

## 1. Project

The author describes the work once: *Boats of the Tagus*, for museum visitors, European
Portuguese first and English second. Learning goals: the sailing concepts the simulation
shows, and the working life of the river's boats. Every later prompt receives this.

## 2. Sources

The author registers the source:

> **Pedrosa, *A Muleta e a Tartaranha (sec. XV–XX)*** · historical account · Portuguese
> (Portugal) · read in full · licence not known · notes: "Muleta history, regulation, fishing
> method."

The readiness checks flag what is missing: no licence and no reliability grade. Because the
licence is unknown, the tool treats the book as copyrighted: it will only ever **paraphrase and
cite** it, never quote it.

## 3. Knowledge

### 3a. Reading

The text is cut into 15 pieces (at page markers) and Claude reads each one, listing what people
did with boats, in its own words and with the page. From Pedrosa it took 196 passages. One of
them:

> **Passage** `m-hist-pedrosa:…:p1` · page "1. Introdução" · kind: description
> *action:* "The muleta, emblem of Seixal and Barreiro, trawled sideways: the net (tartaranha)
> was cast windward and the boat drifted across wind and current."
> *boat:* muleta · *place:* Seixal; Barreiro · *gear:* tartaranha net · *conditions:* drifting
> broadside to wind and current

Rule applied: paraphrase only, at most 25 words, every field "as the text states it", nothing
added.

### 3b. Practices: grouping across sources

Claude places each passage in the practice table. This one joined three others:

> **Practice p41, "Muleta sideways trawling"** · 4 passages from 2 sources (Pedrosa,
> *Embarcações do Rio Tejo*) · boats: muleta, batel · places: Seixal and Barreiro, between
> Peniche and Setúbal, the Tagus estuary · periods: 1772, 1891
> **Conflict found:** Duhamel du Monceau (quoted by Pedrosa) says muletas trawled sideways for
> sardines between Peniche and Setúbal; Pedrosa says that is wrong. Both stay, side by side, for
> the historian.

The practice is then linked to the concepts it exercises (an interpretation, marked as such):
the muleta, the *tartaranha* net, trawling broadside, windward, drifting with wind and current,
lying athwart wind and current. Link note: "Net cast windward while boat drifts sideways."

### 3c. Concepts: what a visitor can learn

From all the sources, terms that mean the same thing are grouped into concepts:

> **Concept c803, "Trawling broadside (arrasto)"** · from *Portugal Marítimo*: *arrasto*,
> *arrasto pelo través* ("trawling with the boat broadside to its direction of drag") · linked to
> two of the simulation's own concepts (the game's fishing mode) · scope **core**: "Fishing
> drift and net drag are simulated; oars are not."

The relation to the game is made here (Check against the game): the concept is something the
player can actually do in the simulation.

### 3d. Boats and places

Rules merge every way the sources write a boat's name:

> **Muleta** · 8 sources · **in the game**

(Elsewhere the same rules merge "Barco Moliceiro" into Moliceiro and the four spellings of the
*barco d'água acima* into one card.)

## 4. Situations: an activity, proposed blind

From practices and concepts, and without seeing the game's own mini-games, Claude proposes
activities the game could offer:

> **"Haul the Net Broadside"** · Muleta · Tagus area, Cabo Espichel to Sesimbra · level 3 ·
> 4 minutes · goal: "Sail slowly and steadily across the wind as a muleta did when trawling with
> the tartaranha net." · success: "Hold a beam reach at 1 to 2 knots for 90 seconds with the
> sails balanced." · leaves out: the net, the cable, the windlass · needs: a net and catch, crew
> tasks.

**Blind comparison:** only now are the game's mini-games shown. Claude finds this proposal **the
same** as the game's *Fishing with the Muleta*: "the Muleta sailing slowly across the wind
trawling its net." The method, starting from history, arrived at an activity the developers had
already made.

## 5. Narrative

**Evidence (rules, no Claude).** For the Fishing mini-game the tool gathers the practices with
the same boat, most sources first, and their passages: 42 evidence records, each with its source
and page.

**Plan (Claude, then the author).** Two invented characters, labelled fictional, whose trade
comes from the evidence: *Arrais Joaquim*, skipper of a Seixal muleta in the 1880s ("dry,
practical, few words"), and *Manel*, the youngest of the crew, who "asks the questions a visitor
would ask". Seven beats; the first:

> **Beat b1** · setup · trigger: `start` (the mission begins) · delivery: story (only when sailing
> is calm) · gist: "Leaving Seixal, Joaquim says the muleta does not chase fish bow-first. She
> will lie across wind and current and drag the tartaranha from her side." · evidence: three
> passages.

**Write (Claude).** Two candidate lines per beat, in Portuguese and English, each listing the
claims it makes and the evidence behind each claim:

> **PT:** "Largamos do Seixal. A muleta não corre atrás do peixe de proa. Vai atravessada ao
> vento e à corrente, a arrastar a tartaranha pelo costado."
> **EN:** "We leave Seixal. The muleta doesn't chase fish bow-first. She lies across wind and
> current, dragging the tartaranha from her side."

**Check (Claude, independently, and rules).** Each claim against its evidence:

| Claim | Evidence | Verdict |
| --- | --- | --- |
| The muleta does not chase fish bow-first; she lies across wind and current | Pedrosa, 1. Introdução | supported |
| The muleta drags the tartaranha net from her side | *Embarcações do Rio Tejo*, Mar da Palha; Pedrosa | supported |

Rules: within 35 words, no number missing from the evidence, the same numbers in both
languages, no Brazilian term where a European one exists, nothing built after the period. All
pass, so the line is **verified**; the author approves it.

For contrast, a line from the same plan that **failed**: "… Nas águas do Entre-Cabos." The name
*Entre-Cabos* is in the sources, but not in that beat's evidence, so the check marks it
unsupported and the line is not exported.

## 6. Export

`tagus-export-banks` writes the game's line bank, in the format agreed in the game's
`content/narrative/README.md`:

```json
{ "id": "fishing.b1.l1", "beat": "setup", "trigger": "start", "delivery": "story",
  "speaker": "k1",
  "text": { "pt": "Largamos do Seixal. …", "en": "We leave Seixal. …" },
  "fictional": false,
  "sources": ["mmwdz12sr2kq0:t59:p46", "m-hist-pedrosa:1tsz:p1", "mmwdz12sr2kq0:t59:p31"],
  "status": "verified" }
```

The bank also carries the paraphrased evidence and credits the two sources by name. The game's
tests check that every trigger is a moment the game knows and every line has both languages.

## 7. In the game

When the visitor starts *Fishing with the Muleta* (Narration in test mode until the line is
approved), the narrator shows the caption **Arrais Joaquim: "Largamos do Seixal…"**. It never
talks while sailing is hard: when the sail starts to luff, a short cue may play; the story waits
for a calm stretch. Once the replies and trivia are written for this mini-game (workbench,
Narrative, "Replies and trivia"), Joaquim also answers "Isso!" when the visitor does what a cue
asked, and after 10–20 quiet seconds the story continues, then a piece of trivia from the same
evidence.

## 8. Game report

The same records evaluate the game, with no further reading:

- **Muleta:** named by 8 sources, in the game.
- **Practice "Muleta fishing grounds with the tartaranha net"** (3 sources): **covered** by the
  Fishing mini-game.
- **Practice "Hauling the tartaranha net"** (Pedrosa, p. 32): **partly** covered: the game drags
  the net, but has no cable paid out or hours-long hauling by hand.
- **Practice "Tartaranha fishermen as bar pilots"** (Pedrosa, pp. 14, 36, 37): **no activity**.
- **Game addition** suggested by these activities: *fishing net and catch* (unlocks 7 proposed
  activities, improves 4).

## What this example shows about the method

- **Every fact has an address:** the caption points to passages, the passages to pages of named
  sources. A historian can check the line without reading the whole book.
- **Fiction is labelled:** Joaquim and Manel are invented; what they say about the muleta is not.
- **Claude drafts, the author decides,** and the checks are independent of the writer.
- **The same knowledge serves two purposes:** the narrative, and a report on what the game
  shows and lacks.
- **Copyright:** the source is only paraphrased and cited; its text never reaches the game or
  this repository.
