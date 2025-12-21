import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if "config" not in sys.modules:
    config = ModuleType("config")
    config.TELEGRAM_TOKEN = "test-token"
    config.QBITTORRENT_URL = "http://localhost:8080"
    config.QBITTORRENT_USERNAME = "user"
    config.QBITTORRENT_PASSWORD = "pass"
    config.NOTIFY_CHAT_ID = 1
    config.CHECK_COMPLETED_INTERVAL = 60
    config.NOTIFIED_FILE = "notified.txt"
    config.SANITIZE_FILE = "sanitize_rules.txt"
    sys.modules["config"] = config
