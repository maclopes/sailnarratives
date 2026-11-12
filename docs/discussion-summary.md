# Discussion summary: grounded narrative for the Tagus sailing game

## Context
A sailing game on the heritage boats of the Tagus (Unity today; a web version planned) with a museum perspective. A leaflet and a method doc already exist (see method-tagus-boats-game.md and the leaflet PDFs). Eight minigames: Downwind and Upwind with the Falua; Passengers with the Catraio; Whale watching with the Baleeiro; Seaweed with the Moliceiro; Cargo with the Fragata; Fishing with the Muleta; Supplies with the Canoa.

## The idea
Use a retrieval-grounded system so that during each sail the game can tell short, historically grounded things. The same mission should have different dialogue depending on the boat and the location. Sources: the existing source library, Wikipedia and Wikidata, museum and archive material.

## Decisions
1. Run retrieval and generation offline, not live in the game. Live calls add latency, cost and hallucination risk, and make PT/EN/FR consistency hard. The game selects from a reviewed line bank using triggers (a tack, a jibe, a wind shift, passing a landmark, being in irons).
2. Pipeline: tagged corpus (boat, place, period, theme, language, licence, reliability) -> multilingual embeddings with metadata filters -> LLM writes short lines with source IDs -> a verifier checks every claim against the retrieved chunks -> human review -> runtime selection.
3. Optional runtime retrieval only for depth-2 curiosity cards, with a small in-browser embedding model and no live generation. A free-form "ask the boatman" mode, if ever added, is separate, labelled, and answers only from retrieved passages with citations.
4. Risk of trivia: lines chosen by (boat x place x trigger) alone give a stream of "did you know" cards. Fix: write the story first, then retrieve.
   - A small story bible: recurring characters with a stake, one short arc per mission (setup, complication, turn, close).
   - Sailing is the plot: headwind, irons, traffic are the complications; sailing instruction is the character's reaction to what the player does.
   - A thread across missions: time (each boat is an era) chosen; place thread kept as an option for Tagus-only missions.
   - Fiction and fact are labelled; characters are invented, context is documented; every factual line cites sources.
   - Continuity at runtime: a small memory of lines heard, with callbacks between lines.
5. Line record fields that make it narrative: beat, character, thread, concept, callbacks, depth, fictional flag, sources.
6. Possible research angle: select curiosities by player state (novelty, information gap) instead of at random, and compare with random facts and with plain cards.

## Risks
- Copyright: Wikipedia is CC BY-SA (attribution and share-alike); news articles and the book Historias do Tejo should be paraphrased and cited, not quoted, unless permission is obtained.
- Whaling tone: the Baleeiro mission must match the ending "you watched it, not harpooned it", and avoid romanticising the hunt.
- Translation: PT/FR lines need native review.
- Source conflicts (for example 1785 vs 1875 for João de Souza's album) stay flagged in the data.
- Rules, times and scores in the leaflet are proposals; PT/FR terms for some points of sail and the catita are unconfirmed.

## Worked examples (proposals)
- Catraio: set in the mid-1920s, Tio Joaquim crossing Lisbon to Almada with a passenger whose reason is revealed during the crossing.
- Baleeiro: set today, Mestre Manuel, a former whaler, taking a young crew out to watch; the old launch rocket now means "go and look".
See story-bible-catraio-baleeiro.md.

## Next steps
Verify the facts listed in the story bible; write the line bank for two missions in Portuguese first; build the pipeline in the prompts folder; test story arcs against plain fact cards with players.
