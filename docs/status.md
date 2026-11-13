# Status and next steps

Updated 2026-11-14. Read this first when starting a new session.

## Where things are

- Workbench (the tool's interface): https://claude.ai/artifact/28te1trNq5pVdem1xFzUD9, source
  `workbench/intake.html` (version label at the top of the page; see `workbench/README.md`).
  Its data (materials, texts, concepts, practices, situations, narrative lines, game reports)
  lives in the artifact's database, not in this repository.
- Design: `docs/system-design.md`; plan: `docs/tool-plan.md`; game integration and speech:
  `docs/game-integration-plan.md`; related work: `docs/related-work.md`; figures: `docs/figures/`.
- Sailing pack: `domains/sailing/` (world list `game-world.json`, built by
  `scripts/build_game_world.py` from a fragateiro checkout; landmarks `landmarks.yaml`).
- The game (TagusNavyVirtualMuseum/fragateiro), branch `claude/kind-ptolemy-rribn8`:
  `content/narrative/` is the shared folder with this tool (contract in its README, schemas,
  `from-game/world.json` and `moments.json`, `from-tool/index.json`), checked by
  `tests/narrative.test.ts`. No pull request yet.

## Decisions to keep

- The tool proposes, the author curates; the tool writes no story of its own.
- No further reading or uploading of copyrighted sources for now; redo concept extraction later
  on a better computer, possibly with a local model.
- No pull requests unless asked.

## Next steps

1. Workbench export writes `from-tool/lines/<mini-game>.json` in the contract format, with the
   same checks as the game's test; first bank: Passengers.
2. Runtime in `runtime/`: observer split (generic engine + sailing rules) and scheduler, with
   scripted-sail tests; Playtest view in the workbench.
3. Game integration behind `?narrative=on` (captions, hooks, place watcher), then speech
   (offline text to speech).
4. The game should generate `from-game/world.json` itself at each release.

## Open questions

Who changes fragateiro (its developers or a pull request); museum hardware (speakers,
headphones); French now or later; narrator per edition (historical or present-day guide).
