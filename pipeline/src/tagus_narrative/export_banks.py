"""Write the workbench's narratives as line banks for a game's shared narrative folder.

    tagus-export-banks DUMP_DIR GAME_NARRATIVE_DIR [--include verified]

DUMP_DIR holds the workbench's database records as JSON files (narrative/, narrativeLines/,
materials/), as saved by an artifact data listing. GAME_NARRATIVE_DIR is the game's shared
folder (for fragateiro: content/narrative), whose README is the contract: the game's world list
and moments are read from from-game/, and one bank per mini-game is written to
from-tool/lines/<mini-game>.json, with from-tool/index.json listing them.

Only checked lines are exported: "approved" by the author, and, with --include verified, lines
whose claims all passed the checks but are not approved yet. Every line keeps its evidence ids;
the bank lists the evidence (paraphrases, never quotations) and credits its sources.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

CONTRACT_VERSION = 1
LICENCES = {"": "copyright, unknown licence: cited and paraphrased", "cite": "copyright: cited and paraphrased",
            "open": "open licence", "cc0": "CC0 or public domain", "permission": "used with permission"}


def norm(text: str) -> str:
    t = unicodedata.normalize("NFD", str(text or "").lower())
    return re.sub(r"\s+", " ", "".join(c for c in t if not unicodedata.combining(c))).strip()


def game_places(world: dict[str, Any]) -> dict[str, str]:
    """Normalised name (including other names from the pack's aliases) -> the game's own name."""
    def names(v: Any) -> list[str]:
        if isinstance(v, str):
            return [v]
        if isinstance(v, dict):
            return [n for x in v.values() for n in names(x)]
        if isinstance(v, list):
            return [n for x in v for n in names(x)]
        return []
    out = {norm(n): n for key in ("ports", "extra_places", "map_places", "landmarks") for n in names(world.get(key))}
    for own, others in (world.get("aliases", {}).get("places") or {}).items():
        for o in others:
            out.setdefault(norm(o), own)
    return out


def read_dir(path: Path) -> dict[str, Any]:
    return {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in sorted(path.glob("*.json"))} if path.is_dir() else {}


def bank_for(plan: dict[str, Any], lines: list[dict[str, Any]], materials: dict[str, Any], places: dict[str, str],
             moments: set[str], include: set[str]) -> tuple[dict[str, Any], list[str]]:
    minigame = str(plan["game"]).removeprefix("mini.")
    problems: list[str] = []
    beats = {b["id"]: b for b in plan["beats"]}
    evidence = {e["id"]: e for e in plan["evidence"]}
    cast = [{"id": k["id"], "name": {"pt": re.sub(r"\s*\(fictional\)$", "", k["name"]), "en": re.sub(r"\s*\(fictional\)$", "", k["name"])},
             "role": k.get("role", ""), "fictional": True} for k in plan["cast"]]
    out_lines, used = [], {}
    for line in lines:
        if line.get("status") not in include:
            continue
        beat = beats.get(line["beat"])
        if not beat:
            continue
        trigger = beat["trigger"]
        if trigger.startswith("near_place:"):
            name = places.get(norm(trigger.split(":", 1)[1]))
            if not name:
                problems.append(f"{minigame} {line['id']}: place {trigger} is not in the game; line left out")
                continue
            trigger = "near_place:" + name
        elif trigger not in moments:
            problems.append(f"{minigame} {line['id']}: moment {trigger} is not in the game; line left out")
            continue
        ev_ids = list(dict.fromkeys([i for c in line.get("claims", []) for i in c.get("evidence", [])] + beat.get("evidence", [])))
        recs = [evidence[i] for i in ev_ids if i in evidence]
        for r in recs:
            used[r["origin"]] = r
        out = {"id": f"{minigame}.{beat['id']}.{line['id']}", "beat": beat["part"], "trigger": trigger,
               "delivery": "leg" if beat["part"] == "leg" else beat["delivery"], "speaker": beat["character"],
               "text": {"pt": line["pt"], "en": line["en"]}, "fictional": bool(line.get("fictional")),
               "sources": [r["origin"] for r in recs], "status": "approved" if line["status"] == "approved" else "verified"}
        if beat.get("concept"):
            out["concept"] = beat["concept"]
        option = plan.get("option")
        if option:
            pl = option.get("place") or {}
            out["when"] = {"boats": [option["boat"]], "areas": [pl["area"]] if pl.get("area") else [],
                           "places": [p for p in (pl.get("from") or pl.get("at"), pl.get("to")) if p]}
        out_lines.append(out)
    have = {l["beat"] for l in out_lines}
    coverage = [p for p in ("setup", "close") if p not in have]
    credits: dict[str, dict[str, str]] = {}
    for r in used.values():
        m = materials.get(r.get("sourceId", ""), {})
        credits.setdefault(r["source"], {"id": r.get("sourceId", ""), "title": m.get("title", r["source"]),
                                          "licence": LICENCES.get(m.get("licence", ""), m.get("licence", ""))})
    bank = {"version": CONTRACT_VERSION, "minigame": minigame, "title": plan.get("title", ""),
            "variant": (plan.get("settings") or {}).get("mode", "historical"), "languages": ["pt", "en"],
            "cast": cast, "lines": out_lines, "missing": coverage,
            "evidence": [{"id": r["origin"], "source": r["source"], "location": r.get("location", ""), "paraphrase": r["text"]} for r in used.values()],
            "credits": list(credits.values()), "exportedAt": plan.get("updatedAt", "")}
    return bank, problems


def export(dump: Path, game_dir: Path, include: set[str]) -> list[str]:
    world = json.loads((game_dir / "from-game/world.json").read_text(encoding="utf-8"))
    moments = {m["id"] for m in json.loads((game_dir / "from-game/moments.json").read_text(encoding="utf-8"))["moments"]}
    pack_aliases = Path(__file__).resolve().parents[3] / "domains/sailing/aliases.yaml"
    if "aliases" not in world and pack_aliases.exists():
        import yaml
        world["aliases"] = yaml.safe_load(pack_aliases.read_text(encoding="utf-8")) or {}
    places = game_places(world)
    plans, lines, materials = read_dir(dump / "narrative"), read_dir(dump / "narrativeLines"), read_dir(dump / "materials")
    out_dir = game_dir / "from-tool/lines"
    out_dir.mkdir(parents=True, exist_ok=True)
    index, problems = [], []
    for key, plan in plans.items():
        if "~" in key:
            continue  # per-option plans are merged by the workbench export; not used yet
        bank, probs = bank_for(plan, (lines.get(key) or {}).get("lines", []), materials, places, moments, include)
        problems += probs
        if not bank["lines"]:
            problems.append(f"{bank['minigame']}: no line passed the checks; no bank written")
            continue
        name = f"{bank['minigame']}.json"
        (out_dir / name).write_text(json.dumps(bank, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        index.append({"minigame": bank["minigame"], "variant": bank["variant"], "file": "lines/" + name,
                      "lines": len(bank["lines"]), "approved": sum(1 for l in bank["lines"] if l["status"] == "approved")})
    (game_dir / "from-tool/index.json").write_text(json.dumps({"version": CONTRACT_VERSION, "banks": index}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("dump", type=Path)
    ap.add_argument("game_dir", type=Path)
    ap.add_argument("--include", choices=["approved", "verified"], default="approved",
                    help="approved: only lines the author approved; verified: also lines that passed every check")
    a = ap.parse_args(argv)
    include = {"approved"} | ({"verified"} if a.include == "verified" else set())
    for p in export(a.dump, a.game_dir, include):
        print(p, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
