"""Validate narrative line records against schema/line-record.schema.json.

Accepted inputs, per file:
- ``.json`` holding one line record (an object) or a list of records
- ``.jsonl`` holding one record per line

Errors are reported by line ``id``. A record without a usable id is reported
as ``<file>#<index>``. Duplicate ids across all checked files are errors too.

Usage::

    python -m tagus_narrative.validate examples/*.json lines/draft/*.json
    tagus-validate --schema schema/line-record.schema.json lines/draft/mission-03.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

SCHEMA_RELPATH = Path("schema") / "line-record.schema.json"
SCHEMA_ENV = "TAGUS_LINE_SCHEMA"


@dataclass(frozen=True)
class LoadedRecord:
    """One record read from a file, with where it came from."""

    source: Path
    index: int
    data: Any

    @property
    def label(self) -> str:
        """The line id, or ``file#index`` when the record has no string id."""
        if isinstance(self.data, dict) and isinstance(self.data.get("id"), str):
            return str(self.data["id"])
        return f"{self.source}#{self.index}"


@dataclass
class Report:
    """Validation outcome: errors grouped by line label, plus file-level errors."""

    checked: int = 0
    errors: dict[str, list[str]] = field(default_factory=dict)
    file_errors: dict[str, list[str]] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors and not self.file_errors

    def add(self, label: str, message: str) -> None:
        self.errors.setdefault(label, []).append(message)

    def add_file_error(self, path: Path, message: str) -> None:
        self.file_errors.setdefault(str(path), []).append(message)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "checked": self.checked,
            "errors": self.errors,
            "file_errors": self.file_errors,
        }


def find_schema(start: Path | None = None) -> Path:
    """Locate the line-record schema.

    Order: ``$TAGUS_LINE_SCHEMA``, then ``schema/line-record.schema.json`` in
    ``start`` (default: cwd) or any parent, then relative to this package.
    """
    env = os.environ.get(SCHEMA_ENV)
    if env:
        return Path(env)
    here = (start or Path.cwd()).resolve()
    for directory in (here, *here.parents):
        candidate = directory / SCHEMA_RELPATH
        if candidate.is_file():
            return candidate
    for directory in Path(__file__).resolve().parents:
        candidate = directory / SCHEMA_RELPATH
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"cannot find {SCHEMA_RELPATH}; pass --schema or set ${SCHEMA_ENV}")


def load_validator(schema_path: Path) -> Draft202012Validator:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def iter_records(path: Path) -> Iterator[LoadedRecord]:
    """Yield records from a .json or .jsonl file. Raises ValueError on bad JSON."""
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".jsonl":
        for lineno, raw in enumerate(text.splitlines(), start=1):
            if not raw.strip():
                continue
            try:
                yield LoadedRecord(path, lineno, json.loads(raw))
            except json.JSONDecodeError as exc:
                raise ValueError(f"line {lineno}: invalid JSON: {exc.msg}") from exc
        return
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON at line {exc.lineno}: {exc.msg}") from exc
    items = data if isinstance(data, list) else [data]
    for index, item in enumerate(items):
        yield LoadedRecord(path, index, item)


def _format_error(error: Any) -> str:
    location = "/".join(str(part) for part in error.absolute_path) or "(record)"
    return f"{location}: {error.message}"


def record_errors(record: Any, validator: Draft202012Validator) -> list[str]:
    """Schema errors for one record, sorted by location for stable output."""
    errors = sorted(validator.iter_errors(record), key=lambda e: list(map(str, e.absolute_path)))
    return [_format_error(e) for e in errors]


def validate_records(
    records: Iterable[LoadedRecord], validator: Draft202012Validator, report: Report
) -> None:
    first_seen: dict[str, LoadedRecord] = {}
    for record in records:
        report.checked += 1
        for message in record_errors(record.data, validator):
            report.add(record.label, message)
        if isinstance(record.data, dict) and isinstance(record.data.get("id"), str):
            line_id = record.data["id"]
            if line_id in first_seen:
                prev = first_seen[line_id]
                report.add(line_id, f"id: duplicate id, first seen in {prev.source}#{prev.index}")
            else:
                first_seen[line_id] = record


def validate_files(paths: Sequence[Path], schema_path: Path | None = None) -> Report:
    """Validate every record in ``paths`` against the line-record schema."""
    validator = load_validator(schema_path or find_schema())
    report = Report()
    loaded: list[LoadedRecord] = []
    for path in paths:
        try:
            loaded.extend(iter_records(path))
        except (OSError, ValueError) as exc:
            report.add_file_error(path, str(exc))
    validate_records(loaded, validator, report)
    return report


def format_report(report: Report) -> str:
    lines: list[str] = []
    for path, messages in report.file_errors.items():
        lines.extend(f"FILE {path}: {m}" for m in messages)
    for label in sorted(report.errors):
        lines.append(f"{label}:")
        lines.extend(f"  - {m}" for m in report.errors[label])
    bad = len(report.errors)
    lines.append(
        f"{report.checked} record(s) checked, {bad} with errors, "
        f"{len(report.file_errors)} unreadable file(s)"
    )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="tagus-validate",
        description="Validate narrative line records (.json or .jsonl) against the schema.",
    )
    parser.add_argument("files", nargs="+", type=Path, help="line files to check")
    parser.add_argument("--schema", type=Path, help="schema path (default: auto-detect)")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    args = parser.parse_args(argv)

    try:
        report = validate_files(args.files, args.schema)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report.to_dict(), indent=2) if args.json else format_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
