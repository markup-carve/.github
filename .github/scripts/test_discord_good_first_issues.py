import importlib.util
import json
from pathlib import Path

SCRIPT = Path(__file__).with_name("discord_good_first_issues.py")
SPEC = importlib.util.spec_from_file_location("discord_good_first_issues", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_discord_payload_is_bounded_and_disables_mentions() -> None:
    payload = MODULE.discord_payload(
        {
            "number": 7,
            "title": "Friendly starter " * 30,
            "html_url": "https://github.com/markup-carve/carve/issues/7",
            "repository_url": "https://api.github.com/repos/markup-carve/carve",
            "body": "@everyone " + "x" * 1200,
            "labels": [{"name": "good first issue"}],
            "user": {"login": "contributor"},
        }
    )
    assert payload["allowed_mentions"] == {"parse": []}
    assert payload["content"].endswith("markup-carve/carve**")
    assert len(payload["embeds"][0]["title"]) == 256
    assert len(payload["embeds"][0]["description"]) == 1000


def test_seen_state_round_trip(tmp_path: Path) -> None:
    MODULE.STATE_PATH = tmp_path / "state.json"
    assert MODULE.load_seen() == set()
    MODULE.save_seen({9, 2})
    assert json.loads(MODULE.STATE_PATH.read_text()) == {"seen": [2, 9]}
    assert MODULE.load_seen() == {2, 9}
