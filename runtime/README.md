# runtime/

The narrator used by the game (TypeScript, no runtime dependencies, no LLM calls).

- `src/bank.ts`: the line bank as the game receives it (contract: the game's
  `content/narrative/README.md`).
- `src/scheduler.ts`: `Narrator`, which decides which line plays and when. Call
  `narrator.update(t, {events, difficulty})` once per frame; it returns the lines to show (and
  play). Rules: cues may play during difficulty (one every 8 s); story lines only when calm, never
  cut; reflections after a difficulty ends; a short acknowledgement when the player does what a
  cue asked (`expects`); after a random 10–20 s of calm without talk, the story continues, then
  trivia; place lines once; curiosity lines to `narrator.logbook`. Deterministic for a seed.
  Only approved lines play, unless `includeVerified` (playtest).

```bash
npm install
npm test
npm run build
```
