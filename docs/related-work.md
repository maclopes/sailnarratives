# Related work and originality

Draft, 2026-11-12. A quick scan with web search, not a systematic review. Most entries were
read from abstracts and search snippets, not full papers. Before making any "first" claim
in a paper, run a structured search (ACM DL, IEEE Xplore, Scopus, arXiv, DiGRA, FDG, ICIDS,
ECGBL, Digital Heritage) and read the closest papers in full.

## 1. RAG-grounded dialogue for cultural heritage and history games

The closest family. All use retrieval to keep an LLM accurate about heritage content.

- MuseRAG++ (Scientific Reports, 2026): provenance-aware RAG for virtual-museum dialogue;
  answers traceable to museum sources. https://www.nature.com/articles/s41598-026-55700-9
- A Modular AI-Powered Framework for Semantic Retrieval and Dialogue in Serious Games for
  Cultural Heritage (Springer, 2026): multimodal RAG, Unity client, locally hosted LLM, an
  archaeological virtual museum. https://link.springer.com/chapter/10.1007/978-3-032-11381-8_24
- Humanizing Artifacts (CHI PLAY companion, 2024): artifacts narrate in first person, RAG for
  accuracy. https://dl.acm.org/doi/fullHtml/10.1145/3665463.3678792
- Playable Archives (ACM, 2026): RAG ties a Three Kingdoms card game's narrative to verified
  sources; names anachronism and hallucinated facts as the problem.
  https://doi.org/10.1145/3803784.3807556
- Evidence-grounded historical digital personae (MDPI BDCC, 2025): controlled FAQ tier plus
  open RAG with evidence-sufficiency checks. https://doi.org/10.3390/bdcc10100351
- Malinowski's Lens (2025) and Playing the Monograph (2026): RAG turns an ethnography into
  playable scenarios. https://arxiv.org/html/2511.07682v1 ,
  https://dl.acm.org/doi/10.1145/3772363.3798374
- Gamifying the Past (Advances in Archaeological Practice, 2025): embodied LLM NPCs in DIY
  archaeology games; authors say correctness cannot be guaranteed.
  https://www.cambridge.org/core/journals/advances-in-archaeological-practice/article/gamifying-the-past-embodied-llms-in-diy-archaeological-video-games/B6A3641910ADD0A3C376AB957A6CDC4C

Difference from this project: nearly all generate live, in a conversational (ask and
answer) mode, about objects or characters. Ours generates offline, ships only reviewed lines,
and speaks in response to what the player does with the boat, not to questions.

## 2. Keeping LLM narrative reliable in games

- Structured Knowledge Trees for detective games (arXiv 2609.23043): an authored JSON ground
  truth with per-fact IDs, "revealed" flags and source fields, to hold the LLM to the case and
  pace what the player learns. Very close in spirit to our fact IDs plus "heard" memory and
  callbacks. https://arxiv.org/pdf/2609.23043
- LLM-based NPCs systematic mapping study (arXiv 2611.05427): lists offline pre-generation of
  a finite set of approved variants with a deterministic runtime picker (BPST) as an existing
  architecture pattern. So "offline generate, review, select at runtime" is not new on its own.
  https://arxiv.org/html/2611.05427
- Scoping review of LLMs and games (arXiv 2403.02613): in one study only about one in five
  generated quests was judged acceptable, which supports human review.
  https://arxiv.org/pdf/2403.02613

## 3. Selecting authored lines at runtime

- Valve's dynamic dialogue (Ruskin, GDC 2012; Left 4 Dead): thousands of lines matched against
  hundreds of world facts, most specific rule wins, less specific rules as fallback. Our
  selector (prompt 07) is in this tradition.
  https://gdcvault.com/play/1015317/AI-driven-Dynamic-Dialog-through ,
  https://developer.valvesoftware.com/wiki/Response_System
- Storylets, quality-based and salience-based narrative (Short 2016; Kreminski and
  Wardrip-Fruin 2018): atomic, recombinable content chosen by state. Our beats, triggers,
  callbacks and cooldowns are a salience-based storylet system.
  https://emshort.blog/2016/04/12/beyond-branching-quality-based-and-salience-based-narrative-structures/ ,
  https://mkremins.github.io/publications/Storylets_SketchingAMap.pdf

## 4. Claim-level verification

- FActScore (atomic claims checked against retrieved evidence), RARR (whole-text attribution
  and revision), and later work on decomposition errors (DnDScore, arXiv 2412.13175),
  single-pass checking (VeriFastScore, arXiv 2505.16973) and benchmarks where the best checkers
  reach F1 of about 0.63 (arXiv 2311.09000). Our verifier (prompt 05) applies this to very short
  lines with a closed evidence set, which is an easier and more reliable setting, but the
  decomposition and verifier-error issues still apply, so human review stays in the loop.
  https://export.arxiv.org/pdf/2412.13175 , https://arxiv.org/pdf/2505.16973v2 ,
  https://arxiv.org/pdf/2311.09000v1

## 5. Learning: narrative, integration, curiosity

- Intrinsic integration (Habgood and Ainsworth, 2011): learning content should live in the
  core mechanic. Recent LLM examples: Wonder Town (physics, 2026).
  https://strathprints.strath.ac.uk/97716/
- Narrative versus exposition and seductive details: interesting but irrelevant detail can
  hurt recall (Harp and Mayer), though recent studies are mixed; narrative helps low prior
  knowledge learners most. This cuts both ways for us: the story may help recall or distract
  from the facts. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10176302/ ,
  https://en.wikipedia.org/wiki/Seductive_details
- Curiosity and information gap (Loewenstein 1994); Pique sequences material by novelty and
  information gap; active player modelling (arXiv 1312.2936); the "noisy TV" risk of
  novelty-seeking. Relevant to the optional condition C.
  https://arxiv.org/pdf/1312.2936 , https://pmc.ncbi.nlm.nih.gov/articles/PMC9194910
- Sailing games (ASA Sailing Challenge, eSail, MarineVerse, NauticEd VR) teach points of sail
  and tacking, but I found no controlled study of learning outcomes.
  https://americansailing.com/sailing-challenge-app/ ,
  https://new.marineverse.com/learn-how-to-sail

## What is original here

Not original on its own: RAG grounding for heritage, offline generation with human review,
rule or salience-based line selection, claim-level verification. Each has clear precedent
above, and a paper should cite it rather than claim it.

Plausibly original, mainly as a combination and in the evaluation:

1. Narration driven by physical sailing events, not by questions. Lines fire on simulation
   events (tack, in irons, wind shift, steamer wake) and sailing instruction is a character's
   reaction to what the player just did. Heritage RAG systems are conversational; storylet
   systems are not grounded in sources. Joining the two in a physics simulation, where the
   sailing is the plot, is the core idea.
2. Provenance that ships with the game. Every line carries chunk IDs, licence, a fictional
   flag and conflict flags through to the exported bank and credits. Fact and fiction are
   labelled per line, and source conflicts stay visible instead of being resolved by the
   model. Most systems keep provenance at answer time only.
3. Story first, retrieval second, as a fix for "trivia streams". The beat (setup,
   complication, turn, close), the character's want and callbacks constrain what is
   retrieved, rather than (boat x place x trigger) driving fact cards.
4. A controlled study the pipeline makes possible: the same verified facts, at the same
   triggers, as story arcs with callbacks (A) or as plain fact cards (B), measuring recall,
   interruption, enjoyment and sailing performance; optional curiosity-selected versus random
   lines (C). Holding facts constant isolates the effect of narrative framing. Given the mixed
   seductive-details literature, either result is publishable.
5. Domain and data: a source-graded, licence-aware PT/EN/FR corpus on Tagus and Azores
   heritage boats with a museum partner, and, as far as this scan shows, the first learning
   evaluation of a sailing game.

Suggested framing: "grounded, salience-based narration for learning in a physics
simulation", with the A/B (and C) study as the main evidence. Add prior knowledge as a
covariate, since narrative effects depend on it.

## To do

- [ ] Read in full: MuseRAG++, Playable Archives, Structured Knowledge Trees, the LLM-NPC
      mapping study (BPST), Humanizing Artifacts
- [ ] Systematic search for sailing or maritime heritage serious games with evaluations
- [ ] Search for studies of event-triggered (not conversational) educational narration
- [ ] Check the curiosity-driven content selection literature in games beyond Pique
