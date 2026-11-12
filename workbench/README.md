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

## Checking links

The page cannot open other websites, so links are checked by a command run where there is
internet (normally your own computer):

1. In the intake, Readiness tab: Download (or Copy) `domain.yaml`.
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
