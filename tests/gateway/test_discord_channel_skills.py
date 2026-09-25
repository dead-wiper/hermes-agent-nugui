"""Tests for Discord channel_skill_bindings auto-skill resolution."""
from types import SimpleNamespace
from unittest.mock import MagicMock


def _make_adapter():
    """Create a minimal DiscordAdapter with mocked config."""
    from plugins.platforms.discord.adapter import DiscordAdapter
    adapter = object.__new__(DiscordAdapter)
    adapter.config = MagicMock()
    adapter.config.extra = {}
    return adapter


class TestResolveChannelSkills:


    def test_match_by_parent_id(self):
        adapter = _make_adapter()
        adapter.config.extra = {
            "channel_skill_bindings": [
                {"id": "200", "skills": ["forum-skill"]},
            ]
        }
        # channel_id doesn't match, but parent_id does (forum thread)
        assert adapter._resolve_channel_skills("999", parent_id="200") == ["forum-skill"]

    def test_no_match_returns_none(self):
        adapter = _make_adapter()
        adapter.config.extra = {
            "channel_skill_bindings": [
                {"id": "100", "skills": ["skill-a"]},
            ]
        }
        assert adapter._resolve_channel_skills("999") is None

    def test_explicit_thread_request_preserves_original_title(self):
        adapter = _make_adapter()
        source = SimpleNamespace(
            chat_id="thread-1",
            parent_chat_id="channel-1",
            auto_thread_initial_name="元投稿の文言 スレ",
        )

        assert adapter.should_semantic_rename_discord_thread(source) is False

    def test_ordinary_auto_thread_remains_semantically_renamable(self):
        adapter = _make_adapter()
        source = SimpleNamespace(
            chat_id="thread-1",
            parent_chat_id="channel-1",
            auto_thread_initial_name="通常の自動スレッド",
        )

        assert adapter.should_semantic_rename_discord_thread(source) is True


