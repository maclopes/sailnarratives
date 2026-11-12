"""Check the links in a domain pack manifest and write a report the intake page can import.

Run it where there is internet access (normally your own computer):

    tagus-linkcheck domain.yaml -o link-report.json

Then paste link-report.json into the intake page (Materials, "Link check results").

Statuses: ok, redirected (works, at another address), broken (the site answers with an
error), unreachable (no answer: the name does not resolve, or the connection fails), and
blocked_here (a proxy on this machine refused the request, so the link was not really
checked). For links that are not ok, the Internet Archive is asked for an archived copy.
"""

from __future__ import annotations

import argparse
import json
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Iterable, Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

USER_AGENT = "tagus-narrative-linkcheck/0.1 (heritage research tool)"
TIMEOUT = 15
PAUSE_SAME_HOST = 1.0
ARCHIVE_API = "https://archive.org/wayback/available?url="


@dataclass
class LinkResult:
    url: str
    status: str
    httpStatus: int | None = None  # noqa: N815 (field name shared with the page)
    finalUrl: str | None = None  # noqa: N815
    archiveUrl: str | None = None  # noqa: N815
    detail: str | None = None


Opener = Callable[[urllib.request.Request], Any]


def extract_urls(manifest: Any) -> list[str]:
    """Every distinct http(s) value of a ``url`` key, in order of appearance."""
    found: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if (
                    key == "url"
                    and isinstance(value, str)
                    and value.startswith(("http://", "https://"))
                ):
                    if value not in found:
                        found.append(value)
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(manifest)
    return found


def classify_error(exc: BaseException) -> tuple[str, int | None, str]:
    """Map a urllib exception to (status, http status, detail)."""
    if isinstance(exc, urllib.error.HTTPError):
        return "broken", exc.code, f"HTTP {exc.code}"
    reason: Any = getattr(exc, "reason", exc)
    text = str(reason)
    if "Tunnel connection failed" in text or "ProxyError" in type(reason).__name__:
        return "blocked_here", None, text
    if (
        isinstance(reason, socket.gaierror)
        or "Name or service not known" in text
        or "nodename nor servname" in text
    ):
        return "unreachable", None, "the address does not resolve"
    if isinstance(reason, (TimeoutError, socket.timeout)):
        return "unreachable", None, "timed out"
    return "unreachable", None, text


def _request(url: str, method: str) -> urllib.request.Request:
    headers = {"User-Agent": USER_AGENT}
    if method == "GET":
        headers["Range"] = "bytes=0-0"
    return urllib.request.Request(url, method=method, headers=headers)


def _default_opener(req: urllib.request.Request) -> Any:
    return urllib.request.urlopen(req, timeout=TIMEOUT)  # noqa: S310 (http(s) only, checked above)


def check_url(url: str, opener: Opener = _default_opener) -> LinkResult:
    """HEAD first; some servers refuse HEAD, so fall back to a one-byte GET."""
    last: tuple[str, int | None, str] | None = None
    for method in ("HEAD", "GET"):
        try:
            with opener(_request(url, method)) as resp:
                final = resp.geturl()
                code = getattr(resp, "status", None)
                status = "redirected" if final and final.rstrip("/") != url.rstrip("/") else "ok"
                return LinkResult(url, status, code, final if status == "redirected" else None)
        except (urllib.error.URLError, OSError) as exc:
            last = classify_error(exc)
            if last[0] == "broken" and last[1] in (403, 405, 501) and method == "HEAD":
                continue
            break
    assert last is not None
    return LinkResult(url, last[0], last[1], None, None, last[2])


def find_archive(url: str, opener: Opener = _default_opener) -> str | None:
    """Closest Internet Archive snapshot, or None (also when the archive is unreachable)."""
    try:
        req = urllib.request.Request(
            ARCHIVE_API + urllib.parse.quote(url, safe=""), headers={"User-Agent": USER_AGENT}
        )
        with opener(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, ValueError):
        return None
    snap = data.get("archived_snapshots", {}).get("closest", {})
    return snap.get("url") if snap.get("available") else None


def check_all(
    urls: Iterable[str], opener: Opener = _default_opener, pause: float = PAUSE_SAME_HOST
) -> list[LinkResult]:
    results: list[LinkResult] = []
    last_hit: dict[str, float] = {}
    for url in urls:
        host = urllib.parse.urlsplit(url).netloc
        wait = last_hit.get(host, -1e9) + pause - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        result = check_url(url, opener)
        last_hit[host] = time.monotonic()
        if result.status in ("broken", "unreachable"):
            result.archiveUrl = find_archive(url, opener)
        results.append(result)
    return results


def build_report(results: Sequence[LinkResult]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for r in results:
        counts[r.status] = counts.get(r.status, 0) + 1
    return {
        "checkedAt": datetime.now(UTC).isoformat(timespec="seconds"),
        "counts": counts,
        "results": [{k: v for k, v in asdict(r).items() if v is not None} for r in results],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="tagus-linkcheck", description=__doc__.split("\n\n")[0])
    parser.add_argument("manifest", type=Path, help="domain.yaml exported by the intake page")
    parser.add_argument(
        "-o", "--output", type=Path, help="write the JSON report here (default: print it)"
    )
    args = parser.parse_args(argv)

    manifest = yaml.safe_load(args.manifest.read_text(encoding="utf-8"))
    urls = extract_urls(manifest)
    print(f"Checking {len(urls)} links…", file=sys.stderr)
    report = build_report(check_all(urls))
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
        print(f"Wrote {args.output}: {report['counts']}", file=sys.stderr)
    else:
        print(text)
    if report["counts"].get("blocked_here"):
        print(
            "Some links were refused by a proxy on this machine;"
            " run the check somewhere with open internet.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
