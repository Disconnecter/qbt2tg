import qbittorrent_api


class DummyResponse:
    ok = True


def test_pause_and_resume_use_expected_payload(monkeypatch):
    calls = []

    def fake_qb_api(path, method="get", data=None, files=None):
        calls.append((path, method, data, files))
        return DummyResponse()

    monkeypatch.setattr(qbittorrent_api, "qb_api", fake_qb_api)

    assert qbittorrent_api.pause_torrent("hash1") is True
    assert qbittorrent_api.resume_torrent("hash2") is True

    assert calls == [
        ("torrents/pause", "post", {"hashes": "hash1"}, None),
        ("torrents/resume", "post", {"hashes": "hash2"}, None),
    ]


def test_delete_torrent_formats_delete_files_flag(monkeypatch):
    calls = []

    def fake_qb_api(path, method="get", data=None, files=None):
        calls.append((path, method, data, files))
        return DummyResponse()

    monkeypatch.setattr(qbittorrent_api, "qb_api", fake_qb_api)

    assert qbittorrent_api.delete_torrent("hash3", delete_files=True) is True

    assert calls == [
        ("torrents/delete", "post", {"hashes": "hash3", "deleteFiles": "true"}, None),
    ]
