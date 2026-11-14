"""Save a snapshot of the workbench's database in the repository (data/workbench/).

    python workbench/snapshot.py DUMP_DIR [--out data/workbench]

DUMP_DIR holds the database records as JSON files, one folder per collection, as saved by an
artifact data listing. The snapshot keeps what is safe to publish: the author's decisions and
the tool's results (paraphrases, never quotations). It leaves out the full texts of the sources
(`texts`, mostly copyrighted), links to the author's private Google Drive and uploaded files, and
the raw duplicates of each reading. The snapshot can be loaded back into the workbench.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any

SKIP_COLLECTIONS = {"texts"}
DROP_KEYS = {"driveId", "driveUrl", "assetId", "raw"}
PRIVATE = re.compile(r"https?://(drive|docs)\.google\.com/\S*")


def clean(v: Any) -> Any:
    if isinstance(v, dict):
        return {k: clean(x) for k, x in v.items() if k not in DROP_KEYS}
    if isinstance(v, list):
        return [clean(x) for x in v]
    if isinstance(v, str):
        return PRIVATE.sub("[private link removed]", v)
    return v


def snapshot(dump: Path, out: Path) -> dict[str, int]:
    if out.exists():
        shutil.rmtree(out)
    counts: dict[str, int] = {}
    for coll in sorted(p for p in dump.iterdir() if p.is_dir()):
        if coll.name in SKIP_COLLECTIONS:
            continue
        for f in sorted(coll.glob("*.json")):
            target = out / coll.name / f.name
            target.parent.mkdir(parents=True, exist_ok=True)
            data = clean(json.loads(f.read_text(encoding="utf-8")))
            target.write_text(json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
            counts[coll.name] = counts.get(coll.name, 0) + 1
    return counts


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("dump", type=Path)
    ap.add_argument("--out", type=Path, default=Path("data/workbench"))
    a = ap.parse_args()
    for k, n in snapshot(a.dump, a.out).items():
        print(f"{k}: {n}")


if __name__ == "__main__":
    main()
