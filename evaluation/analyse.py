"""Compare the experts' answers with the tool.

    python evaluation/analyse.py evaluation/respostas/

The folder holds, per participant, a copy of materiais/registo.csv filled in (any file name
ending in -registo.csv) and the step-1 answers (files ending in -recordacao.csv, same columns as
materiais/recordacao-livre.csv). Prints, as Markdown tables for the paper:

- precision: how many of the tool's statements the experts judged correct, per section;
- novelty: correct statements the experts did not already know;
- relevance: Spearman correlation between the tool's number of sources and the experts'
  importance (sections A to C);
- conflicts: which version the experts chose; terms: which words they chose; lines;
- activities (Folha 2B, blind): the game's mini-games against the tool's proposals: did the boats
  do this, is the boat right, and how important is it to show;
- coverage: of the boats and places the experts named unprompted (step 1), how many the tool's
  knowledge base has, and how many the game has.
"""

from __future__ import annotations

import csv
import glob
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECTIONS = {"G": "Activities (blind)", "A": "Boats missing from the game", "B": "Places missing from the game", "C": "Practices", "D": "Conflicts", "E": "Terms", "F": "Lines"}


def norm(t: str) -> str:
    t = unicodedata.normalize("NFD", str(t or "").lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"\bd['’]\s?", "de ", t)
    t = re.sub(r"[-‐–'\"“”‘’]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"^(barcos?|boats?) (?!de |do |da |a )", "", t)
    t = re.sub(r" (do|de|of the) (tejo|tagus)$", "", t)
    return t.rstrip("s")


def rank(xs: list[float]) -> list[float]:
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(x: list[float], y: list[float]) -> float | None:
    if len(x) < 3:
        return None
    rx, ry = rank(x), rank(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else None


def main(folder: Path) -> None:
    rows = [r for f in glob.glob(str(folder / "*-registo.csv")) for r in csv.DictReader(open(f, encoding="utf-8"))]
    recall = [r for f in glob.glob(str(folder / "*-recordacao.csv")) for r in csv.DictReader(open(f, encoding="utf-8"))]
    people = sorted({r["participante"] for r in rows})
    print(f"Participants: {len(people)} ({', '.join(people)})\n")
    col = lambda r, k: next((v for kk, v in r.items() if kk.startswith(k)), "").strip().lower().replace("ã", "a")

    print("| Section | Judged | Correct | Not correct | Don't know | Correct and new to the expert |\n|---|---|---|---|---|---|")
    for s in "ABCF":
        rs = [r for r in rows if r["seccao"] == s and col(r, "certo")]
        c = Counter(col(r, "certo") for r in rs)
        new = sum(1 for r in rs if col(r, "certo") == "sim" and col(r, "ja_sabia") == "nao")
        judged = c["sim"] + c["nao"]
        pct = f"{100 * c['sim'] / judged:.0f}%" if judged else "-"
        print(f"| {SECTIONS[s]} | {len(rs)} | {c['sim']} ({pct}) | {c['nao']} | {c.get('nao_sei', 0)} | {new} |")

    imp = defaultdict(list)
    src = {}
    for r in rows:
        if r["seccao"] in "ABC" and col(r, "importante") in ("1", "2", "3") and r["fontes_ferramenta"]:
            imp[r["item"]].append(int(col(r, "importante")))
            src[r["item"]] = float(r["fontes_ferramenta"])
    ids = sorted(imp)
    rho = spearman([src[i] for i in ids], [sum(imp[i]) / len(imp[i]) for i in ids])
    print(f"\nRelevance: Spearman rho between the tool's sources and the experts' mean importance, {len(ids)} items: "
          + (f"{rho:.2f}" if rho is not None else "not enough data"))

    print("\n| Conflict | Versions chosen |\n|---|---|")
    for item in sorted({r["item"] for r in rows if r["seccao"] == "D"}, key=lambda x: int(x[1:])):
        c = Counter(r["versao_escolhida"].strip() or "-" for r in rows if r["item"] == item)
        print(f"| {item} | {'; '.join(f'{k}: {v}' for k, v in c.most_common())} |")
    print("\n| Term | Words chosen |\n|---|---|")
    for item in sorted({r["item"] for r in rows if r["seccao"] == "E"}, key=lambda x: int(x[1:])):
        c = Counter(w.strip() for r in rows if r["item"] == item for w in r["termo_escolhido"].split(";") if w.strip())
        print(f"| {item} | {'; '.join(f'{k}: {v}' for k, v in c.most_common()) or '-'} |")

    act = [r for r in rows if r["seccao"] == "G"]
    if act:
        print("\n| Activities (blind) | Items | Did this (yes of judged) | Right boat (yes of judged) | Mean importance |\n|---|---|---|---|---|")
        def share(rs: list, k: str) -> str:
            c = Counter(col(r, k) for r in rs)
            j = c["sim"] + c["nao"]
            return f"{c['sim']}/{j} ({100 * c['sim'] / j:.0f}%)" if j else "-"
        def mean_imp(rs: list) -> str:
            v = [int(col(r, "importante")) for r in rs if col(r, "importante") in ("1", "2", "3")]
            return f"{sum(v) / len(v):.2f}" if v else "-"
        groups = [("The game's mini-games", [r for r in act if r["origem"] == "jogo"]),
                  ("The tool's proposals", [r for r in act if r["origem"] == "ferramenta"]),
                  ("  related to a mini-game", [r for r in act if r["origem"] == "ferramenta" and r["estado_ferramenta"] == "related"]),
                  ("  new to the game", [r for r in act if r["origem"] == "ferramenta" and r["estado_ferramenta"] == "new"])]
        for name, rs in groups:
            print(f"| {name} | {len({r['item'] for r in rs})} | {share(rs, 'certo')} | {share(rs, 'barco_certo')} | {mean_imp(rs)} |")
        # per participant: is the mean importance of the tool's proposals at least that of the game's?
        ge = 0
        for pp in people:
            g, t2 = mean_imp([r for r in act if r["participante"] == pp and r["origem"] == "jogo"]), mean_imp([r for r in act if r["participante"] == pp and r["origem"] == "ferramenta"])
            ge += g != "-" and t2 != "-" and float(t2) >= float(g)
        print(f"\nParticipants rating the tool's proposals at least as important as the game's, on average: {ge} of {len(people)}")
        print("\n| Item | Origin | Did this | Right boat | Importance |\n|---|---|---|---|---|")
        for item in sorted({r["item"] for r in act}, key=lambda x: int(x[1:])):
            rs = [r for r in act if r["item"] == item]
            print(f"| {item} {rs[0]['texto'][:60]} | {rs[0]['origem']} {rs[0]['estado_ferramenta']} | {share(rs, 'certo')} | {share(rs, 'barco_certo')} | {mean_imp(rs)} |")

    rep = max((json.load(open(f, encoding="utf-8")) for f in glob.glob(str(ROOT / "data/workbench/reports/*.json"))), key=lambda r: r["createdAt"])
    tool = {k: {norm(n) for e in rep[k] for n in [e["name"], *e.get("also", [])]} for k in ("boats", "places")}
    import yaml
    al = yaml.safe_load(open(ROOT / "domains/sailing/aliases.yaml", encoding="utf-8")) or {}
    other = {norm(o): norm(own) for own, os in (al.get("places") or {}).items() for o in os}
    other.update({norm(o): norm(own) for own, os in (al.get("boats") or {}).items() for o in os})
    world = json.load(open(ROOT / "domains/sailing/game-world.json", encoding="utf-8"))
    game = {"boats": {norm(b["name"]) for b in world["boats"]},
            "places": {norm(p) for ps in world["ports"].values() for p in ps} | {norm(p) for p in world.get("landmarks", [])}}
    print("\n| Named unprompted (step 1) | Distinct names | In the tool's knowledge base | In the game |\n|---|---|---|---|")
    for kind, key in (("barco", "boats"), ("lugar", "places")):
        names = {other.get(norm(r["nome_como_dito"]), norm(r["nome_como_dito"])) for r in recall if r.get("tipo (barco/lugar/trabalho/epoca/palavra/erro)", "").strip().lower() == kind and r["nome_como_dito"].strip()}
        in_tool = {n for n in names if n in tool[key]}
        in_game = {n for n in names if n in game[key]}
        print(f"| {key} | {len(names)} | {len(in_tool)} | {len(in_game)} |")
        if names - tool[key]:
            print(f"|  | not in the tool: {', '.join(sorted(names - tool[key]))} | | |")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "evaluation" / "respostas"))
