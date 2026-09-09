"""Post newly discovered `good first issue` items to Discord."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

GITHUB_API = "https://api.github.com"
QUERY = 'org:markup-carve is:issue is:open label:"good first issue"'
STATE_PATH = Path(".bridge-state/good-first-issues.json")


def request_json(
    method: str,
    url: str,
    *,
    token: str | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "markup-carve-discord",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
        headers["X-GitHub-Api-Version"] = "2022-11-28"
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode()
    for attempt in range(3):
        try:
            with urlopen(
                Request(url, data=data, headers=headers, method=method)
            ) as response:
                raw = response.read()
                return json.loads(raw) if raw else {}
        except HTTPError as error:
            if error.code == 429 and attempt < 2:
                time.sleep(float(error.headers.get("Retry-After", "1")))
                continue
            detail = error.read().decode(errors="replace")
            raise RuntimeError(
                f"{method} request failed with HTTP {error.code}: {detail}"
            ) from error
    raise RuntimeError("request retry limit reached")


def current_issues(github_token: str) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    page = 1
    while True:
        url = f"{GITHUB_API}/search/issues?q={quote_plus(QUERY)}&sort=created&order=asc&per_page=100&page={page}"
        response = request_json("GET", url, token=github_token)
        items = response.get("items", [])
        result.extend(items)
        if len(items) < 100:
            return result
        page += 1


def discord_payload(issue: dict[str, Any]) -> dict[str, Any]:
    repository = issue["repository_url"].rsplit("/", 1)[-1]
    labels = ", ".join(label["name"] for label in issue.get("labels", []))[:1024]
    title = f"#{issue['number']}: {issue['title']}"[:256]
    return {
        "username": "Carve GitHub",
        "content": f"New good first issue in **markup-carve/{repository}**",
        "embeds": [
            {
                "title": title,
                "url": issue["html_url"],
                "description": (issue.get("body") or "No description provided.")[:1000],
                "color": 0x57F287,
                "fields": [{"name": "Labels", "value": labels or "good first issue"}],
                "footer": {"text": f"Opened by {issue['user']['login']}"},
            }
        ],
        "allowed_mentions": {"parse": []},
    }


def load_seen() -> set[int]:
    try:
        value = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        return {int(issue_id) for issue_id in value.get("seen", [])}
    except (FileNotFoundError, json.JSONDecodeError, TypeError, ValueError):
        return set()


def save_seen(seen: set[int]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps({"seen": sorted(seen)}) + "\n", encoding="utf-8")


def main() -> None:
    github_token = os.environ["GH_TOKEN"]
    discord_webhook = os.environ["DISCORD_WEBHOOK"]
    seen = load_seen()
    issues = current_issues(github_token)
    new_issues = [issue for issue in issues if int(issue["id"]) not in seen]
    for issue in new_issues:
        request_json("POST", discord_webhook, payload=discord_payload(issue))
        seen.add(int(issue["id"]))
        # Preserve every successful delivery if a later webhook call fails.
        save_seen(seen)
    save_seen(seen)
    print(
        f"Found {len(issues)} open good-first issues; posted {len(new_issues)} new item(s)."
    )


if __name__ == "__main__":
    main()
