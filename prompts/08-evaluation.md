Design and implement an evaluation harness under tests/eval and a short protocol document in docs/evaluation.md.

Automatic metrics on a line bank: faithfulness (share of claims supported by cited chunks, from the verifier), citation coverage, redundancy between lines, concept coverage per mission, language parity (every PT line has EN and FR with identical numbers and names), and a "trivia score" that flags lines whose structure is a bare fact with no character, want or reaction (use an LLM judge with a rubric and report agreement with 20 manually labelled examples that I will provide in tests/eval/labels.yaml).

Player study protocol (documented, not implemented): two conditions with the same facts, A = story arcs with callbacks, B = plain fact cards at the same triggers; measures = recall of facts after the session, perceived interruption, enjoyment, and sailing performance change; include a short questionnaire in PT/EN/FR, sample-size reasoning, and a note on ethics and consent. Optional condition C = curiosity-selected lines (selected by novelty or information gap) versus random selection, with the analysis plan.

Produce a one-page results template. Keep every threshold configurable and explain the defaults.
