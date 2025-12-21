import torrent_notify


def test_load_notified_hashes_empty_when_missing(tmp_path, monkeypatch):
    notified_file = tmp_path / "notified.txt"
    monkeypatch.setattr(torrent_notify.config, "NOTIFIED_FILE", str(notified_file))

    hashes = torrent_notify.load_notified_hashes()

    assert hashes == set()


def test_save_and_load_notified_hashes(tmp_path, monkeypatch):
    notified_file = tmp_path / "notified.txt"
    monkeypatch.setattr(torrent_notify.config, "NOTIFIED_FILE", str(notified_file))

    torrent_notify.save_notified_hash("abc")
    torrent_notify.save_notified_hash("def")

    hashes = torrent_notify.load_notified_hashes()

    assert hashes == {"abc", "def"}
