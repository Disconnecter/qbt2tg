import os

import utils


def test_load_sanitize_rules_ignores_comments_and_blanks(tmp_path):
    rules_file = tmp_path / "rules.txt"
    rules_file.write_text("# comment\n\n  \nfoo\nbar\n", encoding="utf-8")

    rules = utils.load_sanitize_rules(str(rules_file))

    assert rules == ["foo", "bar"]


def test_sanitize_torrent_name_applies_rules(monkeypatch):
    monkeypatch.setattr(utils, "load_sanitize_rules", lambda: [r"\b1080p\b", r"\bBluRay\b"])

    cleaned = utils.sanitize_torrent_name("My.Show.S01E01.1080p.BluRay")

    assert cleaned == "My Show S01E01"


def test_sanitize_torrent_name_skips_invalid_regex(monkeypatch):
    monkeypatch.setattr(utils, "load_sanitize_rules", lambda: ["["])

    cleaned = utils.sanitize_torrent_name("A.B")

    assert cleaned == "A B"


def test_clean_nfo_and_delete_folder_removes_tree(tmp_path):
    root = tmp_path / "downloads"
    nested = root / "season1"
    nested.mkdir(parents=True)
    (nested / "info.nfo").write_text("nfo", encoding="utf-8")
    (nested / "keep.txt").write_text("keep", encoding="utf-8")

    utils.clean_nfo_and_delete_folder(str(root))

    assert not os.path.exists(root)
