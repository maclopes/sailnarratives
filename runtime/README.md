# runtime/

Deterministic line selector used by the game (TypeScript, no runtime dependencies).
It reads an exported mission file and picks which reviewed line to play for a game trigger.
No LLM calls happen here.

Status: scaffold only. The selector is implemented in `prompts/07-runtime-selector.md`,
which also adds a C#-friendly description of the algorithm to this README.

```bash
npm install
npm test
npm run build
```
