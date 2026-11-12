# sailnarratives: narrative engine for the Tagus sailing game

An offline toolchain that helps a researcher create, ground, verify and ship short
narrative lines for a sailing game about the heritage boats of the Tagus (and the Azores
whaling boat). The output is a reviewed JSON line bank (PT/EN/FR). The game (Unity now,
web later; see the TagusNavyVirtualMuseum repository) selects lines from it at runtime by
sailing triggers such as a tack, being in irons or reaching the dock. The game makes no
live LLM calls.

Story first, retrieval second: characters and arcs are written by hand
(`docs/story-bible-catraio-baleeiro.md`); retrieval supplies the true detail for each beat;
every factual claim carries source IDs; invented colour is marked fictional.

## Pipeline stages

| Stage | Folder | What it does | Status |
| --- | --- | --- | --- |
| Ingest | `pipeline/` (ingest), `corpus/` | Collect sources, chunk them, tag boat/place/period/theme/licence/reliability, extract atomic claims, flag conflicts | prompt 02 |
| Index | `pipeline/` (retrieve) | Multilingual embeddings in a local file-based store | prompt 03 |
| Retrieve | `pipeline/` (retrieve) | Metadata filter, then semantic ranking with reliability and boat/zone bonuses | prompt 03 |
| Story | `story/` | Missions, cast, beats and the trigger vocabulary in YAML, with a validator | prompt 04 |
| Generate | `pipeline/` (generate) | Lines in the character's voice from the beat and retrieved chunks, PT first, then EN/FR | prompt 05 |
| Verify | `pipeline/` (verify) | Independent claim-by-claim check against cited chunks, plus deterministic checks | prompt 05 |
| Review | `review/` | Local web app: approve, edit, reject; audit trail; trigger coverage | prompt 06 |
| Export | `review/` | Approved lines, triggers and credits as JSON for Unity and the web runtime | prompt 06 |
| Runtime | `runtime/` | Deterministic TypeScript selector (and a C# description) | prompt 07 |
| Evaluation | `tests/eval`, `docs/evaluation.md` | Faithfulness, coverage, parity, trivia score; player study protocol | prompt 08 |

Implemented so far: the scaffold and the line-record validator (prompt 01).

## Layout

```
CLAUDE.md        project rules for Claude Code
docs/            method doc, story bible, discussion summary, related work, leaflets
schema/          JSON schemas; line-record.schema.json is the contract
examples/        example line records
prompts/         the staged build prompts 00 to 08
corpus/          raw sources (corpus/raw/) and the chunk store
story/           mission, cast and trigger YAML
pipeline/src/    Python package tagus_narrative
review/          review tool and exporters
lines/           draft/ and approved/ line banks
runtime/         TypeScript selector library
tests/           pytest tests and golden examples
```

## Setup and tests

Needs Python 3.11+ and Node 18+.

```bash
make setup
```

```bash
make test
```

```bash
make lint
```

## Validate line files

Checks `.json` (one record or a list) and `.jsonl` files against
`schema/line-record.schema.json` and reports errors by line id, including duplicate ids.

```bash
make validate FILES="examples/*.json lines/draft/*.json"
```

```bash
.venv/bin/tagus-validate --json lines/draft/mission-03.jsonl
```

Exit code 0 when everything is valid, 1 when any record or file has errors, 2 when the
schema cannot be found.
