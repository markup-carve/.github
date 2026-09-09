import importlib.util
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "discord_community_prs", SCRIPTS / "discord_community_prs.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def item(
    *, association: str = "NONE", user_type: str = "User", login: str = "outside"
) -> dict:
    return {
        "id": 42,
        "number": 3,
        "title": "Improve parser behavior",
        "html_url": "https://github.com/markup-carve/carve/pull/3",
        "repository_url": "https://api.github.com/repos/markup-carve/carve",
        "body": "A focused contribution.",
        "author_association": association,
        "user": {"login": login, "type": user_type},
    }


def test_filter_keeps_community_and_excludes_internal_and_bots() -> None:
    assert MODULE.is_community_pr(item())
    assert not MODULE.is_community_pr(item(association="MEMBER"))
    assert not MODULE.is_community_pr(item(association="OWNER"))
    assert not MODULE.is_community_pr(item(user_type="Bot"))
    assert not MODULE.is_community_pr(item(login="dependabot[bot]"))


def test_payload_announces_only_open_pr_context_without_mentions() -> None:
    payload = MODULE.discord_payload(item())
    assert payload["allowed_mentions"] == {"parse": []}
    assert "New community contribution" in payload["content"]
    assert "Open pull request" in payload["embeds"][0]["footer"]["text"]
    assert "closed" not in str(payload).lower()
    assert "merged" not in str(payload).lower()
