# Project: a tool for grounded narrative in simulation-based learning games

Goal: a generic tool that helps one author create, ground, verify and time short narrative lines
for a simulation-based learning game in a museum. Output is a reviewed line bank (PT/EN first)
that the game selects from at runtime. No live LLM calls in the game.

Scope: build the tool, not the narrative, and keep the tool generic. Everything specific to one
subject lives in a domain pack under domains/ (manifest: domain.yaml). The first pack is
domains/sailing (traditional Tagus boats, the fragateiro web game, read-only). The tool proposes
drafts; the author curates them. Do not author story content.

Design (docs/system-design.md): three knowledge bases (simulation, concepts, history), three
links between them, situations where all three agree, and a report of missing and contradictory
information. Runtime: lines timed by difficulty (never talk during a hard moment).

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
- runtime/       generic runtime library used by the game (TypeScript, no dependencies)
- tests/         unit tests and golden examples
- docs/          generic design, plan, related work
- domains/       domain packs (sailing first): adapter, vocabulary, vendored simulation, author documents

Conventions: Python 3.11+ for the pipeline, TypeScript for runtime, pytest and vitest, type hints, small functions, README per folder. Keep the LLM and embedding providers behind interfaces so they can be swapped. Never commit API keys.
