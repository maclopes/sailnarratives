"""Tests for the link checker, with a fake network."""

from __future__ import annotations

import io
import json
import socket
import urllib.error
from typing import Any

from tagus_narrative.linkcheck import (
    build_report,
    check_all,
    check_url,
    classify_error,
    extract_urls,
)


class FakeResponse(io.BytesIO):
    def __init__(self, url: str, status: int = 200, body: bytes = b"") -> None:
        super().__init__(body)
        self._url, self.status = url, status

    def geturl(self) -> str:
        return self._url


def make_opener(table: dict[str, Any]):
    calls: list[tuple[str, str]] = []

    def opener(req: Any) -> Any:
        calls.append((req.get_method(), req.full_url))
        outcome = table.get(req.full_url)
        if outcome is None and req.full_url.startswith("https://archive.org/"):
            outcome = table.get("archive")
        if isinstance(outcome, BaseException):
            raise outcome
        if callable(outcome):
            return outcome(req)
        return outcome

    opener.calls = calls  # type: ignore[attr-defined]
    return opener


def test_extract_urls_from_manifest() -> None:
    manifest = {
        "materials": {
            "historical": [{"title": "A", "url": "https://a.example/x"}, {"title": "B"}],
            "reference": [
                {"title": "C", "url": "http://c.example/"},
                {"title": "dup", "url": "https://a.example/x"},
            ],
        },
        "people": [{"title": "D", "url": "mailto:someone"}],
    }
    assert extract_urls(manifest) == ["https://a.example/x", "http://c.example/"]


def test_classify_errors() -> None:
    assert classify_error(urllib.error.HTTPError("u", 404, "nf", {}, None))[:2] == ("broken", 404)  # type: ignore[arg-type]
    assert (
        classify_error(urllib.error.URLError(socket.gaierror(-2, "Name or service not known")))[0]
        == "unreachable"
    )
    assert (
        classify_error(urllib.error.URLError(OSError("Tunnel connection failed: 403 Forbidden")))[0]
        == "blocked_here"
    )
    assert classify_error(urllib.error.URLError(TimeoutError()))[0] == "unreachable"


def test_ok_redirect_and_head_fallback() -> None:
    opener = make_opener(
        {
            "https://ok.example/": FakeResponse("https://ok.example/"),
            "https://moved.example/": FakeResponse("https://new.example/page"),
        }
    )
    assert check_url("https://ok.example/", opener).status == "ok"
    moved = check_url("https://moved.example/", opener)
    assert moved.status == "redirected" and moved.finalUrl == "https://new.example/page"

    seq = iter(
        [
            urllib.error.HTTPError("u", 405, "no HEAD", {}, None),
            FakeResponse("https://nohead.example/"),
        ]
    )  # type: ignore[arg-type]

    def flaky(req: Any) -> Any:
        item = next(seq)
        if isinstance(item, BaseException):
            raise item
        return item

    result = check_url("https://nohead.example/", make_opener({"https://nohead.example/": flaky}))
    assert result.status == "ok"


def test_dead_link_gets_archive_copy_and_report_counts() -> None:
    archive = FakeResponse(
        "x",
        body=json.dumps(
            {
                "archived_snapshots": {
                    "closest": {
                        "available": True,
                        "url": "https://web.archive.org/web/2010/http://dead.example/",
                    }
                }
            }
        ).encode(),
    )
    opener = make_opener(
        {
            "http://dead.example/": urllib.error.URLError(
                socket.gaierror(-2, "Name or service not known")
            ),
            "https://ok.example/": FakeResponse("https://ok.example/"),
            "archive": archive,
        }
    )
    results = check_all(["http://dead.example/", "https://ok.example/"], opener, pause=0)
    assert results[0].status == "unreachable"
    assert results[0].archiveUrl == "https://web.archive.org/web/2010/http://dead.example/"
    report = build_report(results)
    assert report["counts"] == {"unreachable": 1, "ok": 1}
    assert "archiveUrl" not in report["results"][1]
