# workbench/

The tool's screens. Each is a single HTML page with no build step.

- `intake.html`: step 0, materials intake. Records the project (audience, visit length,
  languages, goals, tone, simplifications) and its materials by kind (simulation, reference
  books, historical accounts, author documents, existing activities, people who can check).
  Tabs (from version 31): 1 Project, 2 Sources, 3 Concepts, 4 History, boats and places,
  5 Situations, 6 Narrative, 7 Game report.

  Tab 2, Sources (was Materials and Readiness): the source registry and, on the same tab, the
  readiness report per knowledge base from fixed, generic rules, an optional second look by
  Claude (drafts), and the domain pack manifest (`domain.yaml`).

  Tab 3, Concepts: the concepts base. For each chosen source with text (extracted from an
  attached PDF in the page, or pasted), Claude lists candidate concepts in the source's own
  words; a second request groups them across sources and languages. The tool then gives each
  concept statuses with fixed rules: agreed, conflicting, term clash, variant difference,
  missing term, single source, not in simulation, simulation only. Each card groups terms
  that the tool thinks mean the same thing. The author moves terms between cards ("Move to…"),
  renames, and marks a card "Group is right" or "Leave out" (dropped from later steps);
  undecided cards are still used, and changing a card's terms makes it undecided again. The
  History cards work the same way for passages describing one practice. "Write summary" asks Claude for a
  short reading of the table by type of concept (agreements, conflicts with a suggested next
  step, clarifications, gaps), which can be copied or downloaded as Markdown. Data: texts/,
  candidates/, concepts/current, summaries/concepts in the artifact database.

  Tab 4, History, boats and places: the history base. Claude reads each chosen historical source (licence shown;
  copyrighted or unknown-licence sources are flagged before sending) for practices, rules and
  events: who, boat, place, period, cargo, gear, conditions, numbers, location, as English
  paraphrase. They are grouped across sources in batches (decisions kept, resumable), with
  statuses: agreed, conflicting (date, number, account), single source, no boat, no place, no
  period, no concept. Each practice is linked to the concepts it exercises (an interpretation).
  A review sheet for one source lists every claim taken from it with its location and the
  questions raised, for a historian to mark. Data: practiceCands/, practices/current.
  Boats and places (same tab): one card per boat type or place named in the practices or the
  concept table, built by fixed rules with no Claude request (spellings, a generic "barco" in
  front, "do Tejo" after, and the pack's other names in `aliases.yaml` are merged). The author
  moves names between cards, sets the kind (boat, place, region) and a place's map area, renames,
  or leaves a card out; rebuilding keeps those changes. Data: entities/current.

  Tab 5, Situations: for each historical practice, proposes an activity from what the game can
  simulate (its boats, areas and ports, and the concepts it shows): goal, measurable success
  rule, boat (with a substitution note when the historical boat is missing), area and route,
  concepts, level 1-3, minutes, simplifications, what the game would still need, feasibility
  (full, simplified, needs feature) and a premise drawn only from the practice record. The
  proposals never see the game's activity list. "Compare with the game's mini-games" then runs
  the blind comparison: for each museum mini-game, same, related or none; for each proposal,
  same, related or new. Practices blocked only by something the game lacks are proposed
  anyway as "needs feature", naming the addition (tide and current, water depth, rowing,
  towing, crew, nets, cargo, steam traffic, river bar, new map area, new boat, rig changes);
  "Reconsider skipped" reruns just the skipped ones. A table groups the additions by how many
  activities each would unlock or improve and how many sources back them; the game report turns
  them into issue drafts. Uses processed records only; no source is read again.
  Data: situations/current, situations/blind.

  Tab 6, Narrative: for each of the game's mini-games, gathers the evidence behind it (the
  practice its blind-comparison match came from, other practices with its boat, and their
  concepts, each with source and location), proposes a cast (fictional, per activity) and 4-6
  beats (trigger = a game moment, delivery = cue, story, reflection or curiosity), starting from
  the author's story bible where it covers the mini-game. Writes two candidate lines per beat in
  European Portuguese and English using only the beat's evidence, with a glossary that prefers
  European terms; checks every claim in a separate request, plus word limits, numbers found in
  the evidence and PT/EN number parity (term warnings are separate). The author edits (re-check),
  approves or rejects; Export line bank writes verified and approved lines in the kit's
  line-record shape with delivery, sources and credits. Data: narrative/<mini-game>,
  world/events (the pack's game moments), texts/m-auth-bible.

  Narrative settings per mini-game: narrator (in character in a historical period, or a
  present-day guide), period, and talk (quiet, normal, chatty). Chatty adds leg beats (a pool
  of lines for the long calm stretches, played in turn on steady_leg) and place beats
  (near_place:<name>, only for places the evidence mentions). In a historical setting, the
  landmarks the game shows that were built after the period are listed (author data in
  domains/sailing/landmarks.yaml, marked "to verify"), lines that mention them fail the check,
  and the game report drafts an issue to hide them in a historical edition.

  Mini-games with several boats or places: a second list chooses "All options (shared
  lines)" or one option (boat × place). Shared plans must fit every option (no place beats);
  option plans are stored separately (narrative/<mini-game>~<option>). Export merges them into
  one line bank: shared lines have no conditions, option lines carry `when: {boats, areas,
  places}`, and a coverage check lists options without a verified or approved setup or close
  line (the game would fall back to the shared lines there).

  Tab 7, Game report: evaluates the game against the sources. Concepts are sorted by kind
  (sailing, boat part, practice, role, cargo, event, regulation, internal; only concepts not
  sorted before), boats and places come from the Boats and places list (tab 4) and are checked
  against the pack's game world list (area by area), sailing
  concepts against the simulation, and historical practices (from the History tab when it has run) against the game's activities.
  Every finding counts its sources; a threshold hides weak ones. It drafts one issue per
  finding for the game's developers (copy or download as Markdown) and keeps earlier reports,
  so a new game release shows what changed. The world list comes from
  `domains/sailing/scripts/build_game_world.py` and is stored as world/game. Countries, seas and
  regions are sorted apart; the area's own names (the river and its stretches, from the pack's
  `aliases.yaml`) count as the area itself, not as missing places; spellings and translations of
  one boat or place are merged; lists and routes are not counted as places.

  Published as a claude.ai artifact (private; it keeps its data in the artifact's database):
  https://claude.ai/artifact/28te1trNq5pVdem1xFzUD9
  Opened as a local file it still works, but nothing is saved.

## Importing from Google Drive

Materials tab, "Import from Google Drive": give a folder link or name, list its files, check
the kind and the "Add as" column (matches to existing materials are guesses), and import. The
page reads each file's text with your Google Drive connector (read-only: it may only search
and read) and stores the text for the concepts and history steps. Files stay in Drive.

## Checking links

The page cannot open other websites, so links are checked by a command run where there is
internet (normally your own computer):

1. In the intake, Sources tab (Readiness, Domain pack manifest): Download (or Copy) `domain.yaml`.
2. Run the check:

   ```bash
   make setup-py
   .venv/bin/tagus-linkcheck domain.yaml -o link-report.json
   ```

3. In the intake, Materials tab, open "Link check results", paste the contents of
   `link-report.json`, and press Apply results.

Statuses: link works, link moved, link broken (the site answers with an error), link
unreachable (no answer), and link not checked (a proxy on that machine refused the request; run
it elsewhere). For dead links the report includes an Internet Archive copy when one exists.

On a phone, the Claude app cannot open files for upload: save the entry, then send the file in
the chat and say which entry it belongs to.
