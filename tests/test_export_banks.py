import json
from pathlib import Path

from tagus_narrative.export_banks import export


def write(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")


def test_exports_checked_lines_and_maps_place_names(tmp_path: Path) -> None:
    game = tmp_path / "game"
    write(game / "from-game/world.json", {"ports": {"tejo": ["Lisboa"]}, "aliases": {"places": {"Lisboa": ["Lisbon"]}}})
    write(game / "from-game/moments.json", {"version": 1, "moments": [{"id": "start", "when": ""}]})
    dump = tmp_path / "dump"
    ev = [{"id": "e1", "origin": "src:1:p1", "source": "Src", "sourceId": "src", "location": "p. 1", "text": "a fact"}]
    write(dump / "narrative/mini-x.json", {"game": "mini.x", "title": "X", "cast": [{"id": "k1", "name": "Zé (fictional)"}],
          "beats": [{"id": "b1", "part": "setup", "trigger": "start", "delivery": "story", "character": "k1", "evidence": ["e1"]},
                    {"id": "b2", "part": "place", "trigger": "near_place:Lisbon", "delivery": "story", "character": "k1", "evidence": []},
                    {"id": "b3", "part": "close", "trigger": "unknown_moment", "delivery": "story", "character": "k1", "evidence": []}],
          "evidence": ev})
    write(dump / "narrativeLines/mini-x.json", {"lines": [
        {"id": "l1", "beat": "b1", "pt": "p", "en": "e", "claims": [{"evidence": ["e1"]}], "status": "verified"},
        {"id": "l2", "beat": "b2", "pt": "p", "en": "e", "status": "approved"},
        {"id": "l3", "beat": "b1", "pt": "p", "en": "e", "status": "needs work"},
        {"id": "l4", "beat": "b3", "pt": "p", "en": "e", "status": "approved"}]})
    problems = export(dump, game, {"approved", "verified"})
    bank = json.loads((game / "from-tool/lines/x.json").read_text(encoding="utf-8"))
    assert [l["id"] for l in bank["lines"]] == ["x.b1.l1", "x.b2.l2"]
    assert bank["lines"][1]["trigger"] == "near_place:Lisboa"
    assert bank["lines"][0]["sources"] == ["src:1:p1"] and bank["evidence"][0]["id"] == "src:1:p1"
    assert bank["cast"][0]["name"]["pt"] == "Zé"
    assert bank["missing"] == ["close"]
    assert any("unknown_moment" in p for p in problems)
    index = json.loads((game / "from-tool/index.json").read_text(encoding="utf-8"))
    assert index["banks"][0]["approved"] == 1
