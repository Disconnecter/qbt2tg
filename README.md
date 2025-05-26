# qbt2tg — Telegram Bot for qBittorrent

**qbt2tg** is a modular Telegram bot that lets you manage your qBittorrent downloads directly from Telegram.
Upload `.torrent` files, choose categories, list and delete torrents, get notifications on completion, and enjoy smart torrent name sanitizing—all from chat!

---

## Features

- **Add torrents:** Upload `.torrent` files from Telegram, select a qBittorrent category.
- **Sanitized names:** Human-readable torrent names, free of technical junk (configurable via `sanitize_rules.txt`).
- **List torrents:** Numbered, clean list for quick management.
- **Remove torrents:** Delete torrents and downloaded files by number (with folder cleanup).
- **Status checks:** See all active downloads at any time.
- **Completion notifications:** Get a Telegram message as soon as a download finishes.
- **All commands available as chat buttons.**
- **Easy to extend:** Modular codebase, clean Python, all logic separated by role.
- **All sanitizer rules editable in one file.**

---

## Requirements

- **Python 3.8+**
- **qBittorrent** v4.1+ with enabled Web UI (set up in the qBittorrent app)
- Telegram bot token (get from [@BotFather](https://t.me/BotFather))

### Python dependencies:

```sh
pip install python-telegram-bot requests apscheduler
```

---

### Setup:

1. Clone this repo and enter the folder.
2. Rename `config_sample.py.` to `config.py`.
3. Edit config.py with your tokens, qBittorrent host, user, and password.

```sh
# config.py
TELEGRAM_TOKEN = 'token'
QBITTORRENT_URL = 'http://localhost:8080'
QBITTORRENT_USERNAME = 'user'
QBITTORRENT_PASSWORD = 'pass'
NOTIFY_CHAT_ID = 1
CHECK_COMPLETED_INTERVAL = 60
NOTIFIED_FILE = "notified.txt"
```

4. Edit sanitize_rules.txt if you want to adjust how names are cleaned up (see next section).
5. Start the bot:
```sh
python3 bot.py
```
