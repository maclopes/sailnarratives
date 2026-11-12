# sailnarratives: a tool for grounded narrative in learning games

A generic tool that helps one author build short, grounded and well-timed narrative for a
simulation-based learning game in a museum. It links three kinds of evidence (what the
simulation can do, what is to be learned, what history records), proposes situations where they
agree, reports missing and contradictory information, and derives activities, story beats and
lines for the author to curate. At runtime, lines are timed by difficulty.

Everything specific to a subject lives in a domain pack under `domains/`. The first pack is
`domains/sailing`: traditional boats of the Tagus and the fragateiro web game.

Design: `docs/system-design.md`. Plan: `docs/tool-plan.md`. Related work: `docs/related-work.md`.

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

Implemented so far: the scaffold and the line-record validator (prompt 01). The stages below come from the original kit and will be regrouped around the design's three bases.

## Layout

```
CLAUDE.md        project rules for Claude Code
docs/            generic design, plan and related work
domains/         domain packs; sailing/ holds the adapter, vendored game physics and author documents
schema/          JSON schemas; line-record.schema.json is the contract
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
make validate FILES="domains/*/examples/*.json lines/draft/*.json"
```

```bash
.venv/bin/tagus-validate --json lines/draft/mission-03.jsonl
```

Exit code 0 when everything is valid, 1 when any record or file has errors, 2 when the
schema cannot be found.
