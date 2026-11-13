"""Build the sailing pack's game world list from a fragateiro checkout (read-only).

The tool compares the places and boats named in the sources with this list, to report what
the game is missing. Run: python3 build_game_world.py /path/to/fragateiro > ../game-world.json
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


def strings(block: str) -> list[str]:
    return [m.group(2) for m in re.finditer(r"(['\"])((?:(?!\1).)+)\1", block)]


def main(root: Path) -> dict:
    area_ts = (root / "src/world/area.ts").read_text(encoding="utf-8")
    dest_ts = (root / "src/world/destinations.ts").read_text(encoding="utf-8")
    tejo_ports = strings(re.search(r"DESTINATION_NAMES = \[(.*?)\];", dest_ts, re.S).group(1))
    areas: dict[str, list[str]] = {"tejo": tejo_ports}
    for m in re.finditer(r"^  (\w+): \{\s*\n\s*id: '(\w+)'(.*?)\n  \},?$", area_ts, re.S | re.M):
        ports = re.search(r"ports: \[(.*?)\]", m.group(3), re.S)
        if ports:
            areas[m.group(2)] = strings(ports.group(1))
    extra = [m.group(1) for m in re.finditer(r"name: '([^']+)', kind: '(?:mark|village|hamlet)'", dest_ts + area_ts)]
    landmarks = sorted({m.group(1) for f in (root / "src/engine").glob("*.ts")
                        for m in re.finditer(r"labels\.push\(\{ name: '([^']+)'", f.read_text(encoding="utf-8"))})
    map_places: dict[str, list[str]] = {}
    seamarks: dict[str, list[str]] = {}
    for f in sorted((root / "src/assets/map").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        map_places[f.stem] = sorted({p["name"] for p in d.get("places", []) if p.get("name")})
        seamarks[f.stem] = sorted({s["name"] for s in d.get("seamarks", []) if s.get("name")})
    boats = []
    index_ts = (root / "src/physics/index.ts").read_text(encoding="utf-8")
    dev = set(re.findall(r"BOATS_IN_DEVELOPMENT[^=]*= \[(.*?)\]", index_ts)[0].replace(" ", "").split(","))
    for f in sorted((root / "src/physics/boats").glob("*.ts")):
        t = f.read_text(encoding="utf-8")
        name = re.search(r"name: '([^']+)'", t).group(1)
        desc = re.search(r"description:\s*(['\"])(.*?)\1", t, re.S)
        home = re.search(r"home: '([^']+)'", t)
        const = re.search(r"export const (\w+)", t).group(1)
        boats.append({"name": name, "description": desc.group(2) if desc else "",
                      "home": home.group(1) if home else "tejo", "in_development": const in dev})
    texts = {}
    for line in (root / "content/texts/en.txt").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            texts[k.strip()] = v.strip()
    area_names = {k.split(".", 1)[1]: v for k, v in texts.items() if re.fullmatch(r"area\.[a-z]+", k)}
    activities = []
    for k, v in texts.items():
        kind = k.split(".")[0]
        if kind in ("kind", "mini", "drill") and k.count(".") == 1 and k != "drill.n":
            activities.append({"id": k, "type": {"kind": "mission kind", "mini": "museum mini-game", "drill": "drill"}[kind],
                               "title": v, "description": texts.get(k + ".desc", "")})
        elif kind in ("route", "ground") and k.count(".") == 1 and k != "route.traditionally":
            activities.append({"id": k, "type": "transport route" if kind == "route" else "fishing ground",
                               "title": k.split(".", 1)[1], "description": v})
    mg = json.loads((root / "content/minigames.json").read_text(encoding="utf-8"))
    for g in mg.get("minigames", []):
        for a in activities:
            if a["id"] == "mini." + g["id"]:
                a["boats"] = g.get("boats", [])
                a["places"] = [{k: v for k, v in pl.items() if k in ("area", "from", "to", "at")} for pl in g.get("places", [])]
                a["kind"] = g.get("type", "")
    commit = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    return {"game": "fragateiro", "commit": commit, "area_names": area_names, "map_files": {"tejo": "tagus"},
            "activities": activities, "ports": areas, "extra_places": extra,
            "landmarks": landmarks, "boats": boats, "map_places": map_places, "seamarks": seamarks}


if __name__ == "__main__":
    print(json.dumps(main(Path(sys.argv[1])), ensure_ascii=False, indent=1))
