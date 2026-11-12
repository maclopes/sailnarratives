"""Tests for the line-record validator (prompt 01)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tagus_narrative.validate import find_schema, main, validate_files

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schema" / "line-record.schema.json"
EXAMPLE = ROOT / "examples" / "cat-03-turn-02.json"


def test_example_record_is_valid() -> None:
    report = validate_files([EXAMPLE], SCHEMA)
    assert report.checked == 1
    assert report.ok, report.errors


def test_schema_is_found_from_repo_root(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TAGUS_LINE_SCHEMA", raising=False)
    assert find_schema(ROOT) == SCHEMA


def test_errors_are_reported_by_line_id(tmp_path: Path) -> None:
    record = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    bad = dict(record, id="cat-03-bad", beat="middle", depth=3)
    del bad["text"]
    path = tmp_path / "bad.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in (record, bad)), encoding="utf-8")

    report = validate_files([path], SCHEMA)

    assert report.checked == 2
    assert set(report.errors) == {"cat-03-bad"}
    messages = " ".join(report.errors["cat-03-bad"])
    assert (
        "beat" in messages and "depth" in messages and "'text' is a required property" in messages
    )


def test_duplicate_ids_across_files(tmp_path: Path) -> None:
    copy = tmp_path / "copy.json"
    copy.write_text(EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")
    report = validate_files([EXAMPLE, copy], SCHEMA)
    assert any("duplicate id" in m for m in report.errors["cat-03-turn-02"])


def test_cli_exit_codes(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--schema", str(SCHEMA), str(EXAMPLE)]) == 0
    broken = tmp_path / "broken.json"
    broken.write_text("{not json", encoding="utf-8")
    assert main(["--schema", str(SCHEMA), str(broken)]) == 1
    assert "invalid JSON" in capsys.readouterr().out
