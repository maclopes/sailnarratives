# data/

## workbench/

A snapshot of the workbench's database (the artifact's own storage on claude.ai), so the author's
decisions and the tool's results are not kept in one place only. One folder per collection, one
JSON file per record:

| Folder | Holds |
| --- | --- |
| `project/` | the project form |
| `materials/` | the source registry (links to private Google Drive files removed) |
| `candidates/` | the concepts read from each source (paraphrased) |
| `concepts/current.json` | the concept table, with the author's groups and decisions |
| `summaries/` | the summary of the sources |
| `practiceCands/` | the passages read from each historical source (paraphrased) |
| `practices/current.json` | the practice table, with the author's groups and decisions |
| `entities/` | boats and places (from workbench version 31) |
| `situations/` | activity proposals and the blind comparison |
| `world/` | the game's world list and moments as loaded in the workbench |
| `narrative/`, `narrativeLines/`, `narrativeSettings/` | cast, beats and lines per mini-game |
| `report/`, `reports/` | the game report's working data and the reports built |

**Not included:** the full texts of the sources (`texts`, mostly under copyright) and uploaded
files. They stay in the workbench (and later on the author's computer, for a local model).

Made with `python workbench/snapshot.py DUMP_DIR`, from a listing of every collection saved as
JSON files. Snapshot of 14 November 2026, workbench version 30. The records can be written back
to the workbench's database if it is ever lost.
