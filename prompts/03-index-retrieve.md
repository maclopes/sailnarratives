Implement indexing and retrieval under pipeline/retrieve.

Embed chunks from corpus/chunks.jsonl with a multilingual embedding model behind an interface (default: a local sentence-transformers multilingual model; allow an API provider via config). Store vectors in a local file-based store (sqlite with a vector extension, or FAISS) so it runs without a server.

Expose retrieve(query, boat=None, zone=None, period=None, themes=None, language_pref="pt", k=8) that first filters by metadata, then ranks by semantic similarity, with a small bonus for reliability A and for chunks tagged to the exact boat and zone. Return chunks with scores and their claims. Add a CLI: `retrieve "why zigzag against the wind" --boat catraio --zone tagus-lisbon-almada`.

Add an evaluation file tests/retrieval_goldens.yaml with 15 beat queries drawn from docs/story-bible-catraio-baleeiro.md (the "Fact retrieval must supply" column) and the chunk IDs that should appear in the top 5; implement a recall@5 report. Do not tune on the goldens only; explain any change you make to scoring.
