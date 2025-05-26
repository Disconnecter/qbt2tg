import config
from qbittorrent_api import get_all_torrents
from torrent_notify import load_notified_hashes, save_notified_hash
from telegram.constants import ParseMode

notified_torrents = load_notified_hashes()

async def notify_finished(context):
    global notified_torrents
    torrents = get_all_torrents()
    chat_id = config.NOTIFY_CHAT_ID
    for t in torrents:
        hash_ = t['hash']
        if t['progress'] == 1.0 and hash_ not in notified_torrents:
            notified_torrents.add(hash_)
            save_notified_hash(hash_)
            msg = f"✅: <b>{t['name']}</b>"
            try:
                await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode=ParseMode.HTML)
            except Exception:
                pass
