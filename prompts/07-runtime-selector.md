Implement the runtime selector library under runtime/ in TypeScript with no dependencies, plus a C#-friendly description of the same algorithm in runtime/README.md.

API: createNarrator(missionData, options) returns an object with onTrigger(triggerKey, gameState) -> Line | null, heard() -> string[], and reset(). gameState has boat, zone, concept hints (for example the player just tacked), and a random seed.

Selection rules: filter by trigger and boat and zone; prefer beats in story order (setup, complication, turn, close) and never repeat a heard line; prefer lines whose callbacks have been heard; prefer lines teaching a concept the player is currently struggling with (hint from gameState); respect cooldowns so two lines do not play within N seconds; if nothing sourced matches, return a generic fact-free line for that character and trigger. Depth-2 cards are returned only through a separate requestCuriosity(gameState) call.

Add vitest tests that simulate the Catraio mission with a scripted sequence of triggers and check: story order is respected, no repeats, callbacks are used when satisfied, the generic fallback appears only when needed, and the output is deterministic for a given seed. Provide a small CLI that replays a mission from a JSON event list so I can try it without the game.
