# workbench/

The tool's screens. Each is a single HTML page with no build step.

- `intake.html`: step 0, materials intake. Records the project (audience, visit length,
  languages, goals, tone, simplifications) and its materials by kind (simulation, reference
  books, historical accounts, author documents, existing activities, people who can check).
  Gives a readiness report per knowledge base from fixed, generic rules, an optional second look
  by Claude (drafts), and exports the domain pack manifest (`domain.yaml`).

  Published as a claude.ai artifact (private; it keeps its data in the artifact's database):
  https://claude.ai/artifact/28te1trNq5pVdem1xFzUD9
  Opened as a local file it still works, but nothing is saved.
