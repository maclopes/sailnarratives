# Sailing pack: traditional boats of the Tagus

First domain pack for the tool. Manifest: `domain.yaml`.

- `adapter/observer/`: turns the game's physics state into frames, events and a difficulty level
  (parked draft, untested).
- `signals-events.yaml`: the vocabulary of signals, derived quantities, events and difficulty
  factors.
- `vendor/fragateiro-physics/`: unmodified CC0 copy of the game's physics.
- `docs/`: the author's documents (method doc, story bible, discussion summary, leaflet).
- `examples/`: example line records.
- `game-world.json`: the game's ports by area, landmarks, named map places, seamarks and boats,
  built from the fragateiro code by `scripts/build_game_world.py`. The tool compares places and
  boats named in the sources with it, to report what the game is missing.
- `landmarks.yaml`: the game's landmarks with the year they were completed (author data, "to
  verify"), merged into `game-world.json`, for checking a historical setting against the scenery.
