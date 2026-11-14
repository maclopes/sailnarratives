# Evaluation: historical accuracy, with expert interviews

The question is **historical accuracy**, not how well people sail or learn: do the tool's
knowledge base and findings agree with people who know the traditional boats of the Tagus, and
does the tool find things they would not? Experts do not play the game; they are interviewed.

## Who

4 to 8 people, one at a time, ideally of different kinds: sailors of the remaining traditional
boats (the associations and municipalities of Seixal, Moita, Sarilhos Pequenos keep some
sailing), a river historian, someone from the Museu de Marinha, a boatbuilder. If two are known to
disagree, include both: their disagreements are a result too.

## The interview (45 to 60 minutes), in this order

The order matters: what the expert says before seeing anything is not influenced by the game or
the tool.

| Step | What | Material | Gives |
| --- | --- | --- | --- |
| 0 | Consent, recording, profile | `guiao-entrevista.md`, Folha 1 | who the expert is |
| 1 | **Free recall**, nothing shown: boats, places, work, periods, words, common mistakes | Folha 1 (the interviewer writes) | an independent list to compare with the tool (coverage) |
| 2 | **The game's content**, shown on paper, not played: boats, areas, places, activities. Right, wrong, missing? | Folha 2 | the expert's evaluation of the game |
| 3 | **The tool's findings**: missing boats and places, practices, conflicts (which version is right), terms, lines. Correct? Important? Already known? | Folha 3 | precision, relevance, novelty; the conflicts settled |
| 4 | Anything else; other people to hear | Folha 1 | |

## Files

| File | For |
| --- | --- |
| `guiao-entrevista.md` | the interviewer's guide, in Portuguese, with the neutral opening to read aloud |
| `items.yaml` | the items of Folha 3, in Portuguese, each pointing to the tool's data (`ref`) |
| `build_materials.py` | builds the sheets and templates: `python evaluation/build_materials.py --pdf` (needs a checkout of the game next to this repository for its Portuguese texts and boat pictures) |
| `materiais/folha-1-registo.pdf` | the interviewer's record sheet (profile, step 1, step 2 notes) |
| `materiais/folha-2-o-jogo.pdf` | what the game has today (with the boats' pictures), large print, boxes to tick |
| `materiais/folha-3-achados.pdf` | the tool's findings to judge, large print, boxes to tick |
| `materiais/registo.csv` | one row per Folha 3 item, with the tool's number of sources; copy per participant and fill in |
| `materiais/recordacao-livre.csv` | the step-1 answers, one row per name said |
| `analyse.py` | the comparison: `python evaluation/analyse.py evaluation/respostas/` |

After each interview, save `respostas/P1-registo.csv` and `respostas/P1-recordacao.csv` (P2,
P3… for the others). Answers stay anonymous: participants are coded P1, P2…; recordings are
deleted once transcribed and never committed.

## What the analysis gives (tables for the paper)

- **Precision:** the share of the tool's statements (sections A, B, C, F) the experts judged
  correct.
- **Novelty:** correct statements the expert did not already know: the clearest sign of
  usefulness.
- **Relevance:** the Spearman correlation between the number of sources behind an item (the
  tool's measure of importance) and the experts' importance.
- **Conflicts:** which version the experts chose for each contradiction between sources (and how
  they know); this also corrects the knowledge base.
- **Terms:** the words the experts use, against the tool's European Portuguese glossary.
- **Coverage:** of the boats and places the experts named unprompted (step 1), how many the
  tool's knowledge base has, and how many the game has; the names the tool lacks show the gaps in
  its sources. Names are matched after removing accents, plurals, a generic "barco" in front and
  "do Tejo" after, and through the old names in `domains/sailing/aliases.yaml` (Aldeia Galega for
  Montijo, Punhete for Constância). Work, periods and words from step 1 are compared by hand.

## Notes

- Sheets show the tool's findings of 14 November 2026 (report `r20261114105910`, game commit
  `1d66225`). If the knowledge base changes, rebuild the sheets before the interviews.
- Ethics: the study asks adults about their knowledge, anonymously, with consent; check whether
  your institution needs an ethics committee's approval.
