# Project: narrative engine for the Tagus sailing game

Goal: a toolchain that helps a researcher create, ground, verify and ship short narrative lines for a sailing game about the heritage boats of the Tagus (and the Azores whaling boat). Output is a reviewed JSON line bank (PT/EN/FR) that the game (Unity now, web later) selects from at runtime. No live LLM calls in the game.

Principles
- Story first, retrieval second: characters, arcs and beats are authored in YAML; retrieval supplies true detail for each beat.
- Every factual claim in a line must be supported by retrieved chunks and carry their IDs. Invented characters and colour are marked fictional.
- Offline generation, human review, deterministic runtime selection.
- Facts with conflicting sources stay flagged, never silently resolved.
- Respect licences: record licence per chunk; paraphrase and cite copyrighted sources, do not quote them.
- Portuguese is the primary language; English and French are translations that need native review.

Layout (create as needed)
- corpus/        raw sources and chunk store with metadata
- story/         story bibles, cast and arcs (YAML), one file per mission
- schema/        JSON schemas (line-record.schema.json is the contract)
- pipeline/      ingest, index, retrieve, generate, verify
- review/        review tool and exports
- runtime/       selector library used by the game (TypeScript, no dependencies)
- tests/         unit tests and golden examples
- docs/          method doc, story bible, discussion summary

Conventions: Python 3.11+ for the pipeline, TypeScript for runtime, pytest and vitest, type hints, small functions, README per folder. Keep the LLM and embedding providers behind interfaces so they can be swapped. Never commit API keys.
