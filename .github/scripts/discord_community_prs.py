"""Post newly discovered open community pull requests to Discord once."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from discord_good_first_issues import request_json

GITHUB_API = "https://api.github.com"
QUERY = "org:markup-carve is:pr is:open"
STATE_PATH = Path(".bridge-state/community-prs.json")
INTERNAL_ASSOCIATIONS = {"OWNER", "MEMBER", "COLLABORATOR"}


def is_community_pr(item: dict[str, Any]) -> bool:
    user = item.get("user", {})
    login = user.get("login", "")
    return (
        item.get("author_association") not in INTERNAL_ASSOCIATIONS
        and user.get("type") != "Bot"
        and not login.endswith("[bot]")
    )


def current_community_prs(github_token: str) -> list[dict[str, Any]]:
    from urllib.parse import quote_plus

    result: list[dict[str, Any]] = []
    page = 1
    while True:
        url = f"{GITHUB_API}/search/issues?q={quote_plus(QUERY)}&sort=created&order=asc&per_page=100&page={page}"
        response = request_json("GET", url, token=github_token)
        items = response.get("items", [])
        result.extend(item for item in items if is_community_pr(item))
        if len(items) < 100:
            return result
        page += 1


def discord_payload(item: dict[str, Any]) -> dict[str, Any]:
    repository = item["repository_url"].rsplit("/", 1)[-1]
    title = f"Community PR · {repository}#{item['number']}: {item['title']}"[:256]
    description = (item.get("body") or "No description provided.")[:1000]
    return {
        "username": "Carve GitHub",
        "content": f"New community contribution from **@{item['user']['login']}**",
        "embeds": [
            {
                "title": title,
                "url": item["html_url"],
                "description": description,
                "color": 0x3498DB,
                "footer": {"text": "Open pull request · discussion and review welcome"},
            }
        ],
        "allowed_mentions": {"parse": []},
    }


def load_seen() -> set[int]:
    try:
        value = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        return {int(item_id) for item_id in value.get("seen", [])}
    except (FileNotFoundError, json.JSONDecodeError, TypeError, ValueError):
        return set()


def save_seen(seen: set[int]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps({"seen": sorted(seen)}) + "\n", encoding="utf-8")


def main() -> None:
    github_token = os.environ["GH_TOKEN"]
    discord_webhook = os.environ["DISCORD_WEBHOOK"]
    seen = load_seen()
    pull_requests = current_community_prs(github_token)
    new_items = [item for item in pull_requests if int(item["id"]) not in seen]
    for item in new_items:
        request_json("POST", discord_webhook, payload=discord_payload(item))
        seen.add(int(item["id"]))
        save_seen(seen)
    save_seen(seen)
    print(
        f"Found {len(pull_requests)} open community PRs; posted {len(new_items)} new item(s)."
    )


if __name__ == "__main__":
    main()
