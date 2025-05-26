from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import os
from qbittorrent_api import (
    get_all_torrents, get_torrent_by_hash, delete_torrent
)
from utils import (
    clean_nfo_and_delete_folder,
    sanitize_torrent_name
)

async def list_torrents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    torrents = get_all_torrents()
    if not torrents:
        from .main_menu import get_main_reply_keyboard
        await update.message.reply_text("No torrents.", reply_markup=get_main_reply_keyboard())
        return
    keyboard = []
    for idx, t in enumerate(torrents, 1):
        short = sanitize_torrent_name(t['name'])
        if len(short) > 60:
            short = short[:57] + "..."
        text = f"{idx}. {short}🗑"
        keyboard.append([InlineKeyboardButton(text, callback_data=f"del_{t['hash']}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Click on a row to delete a torrent:", reply_markup=reply_markup)

async def status_torrents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    torrents = get_all_torrents()
    loading = [t for t in torrents if t['progress'] < 1.0 and t['state'] not in ('pausedUP', 'pausedDL')]
    from .main_menu import get_main_reply_keyboard
    if not loading:
        await update.message.reply_text("No active downloads.", reply_markup=get_main_reply_keyboard())
        return

    name = sanitize_torrent_name(t['name'])
    msg_lines = [f"{name} ({t['progress']*100:.1f}% | {t['state']})" for t in loading]
    await update.message.reply_text('\n'.join(msg_lines), reply_markup=get_main_reply_keyboard())

async def del_torrent(update: Update, context: ContextTypes.DEFAULT_TYPE, hash_):
    t = get_torrent_by_hash(hash_)
    torrent_path = None
    if t:
        save_path = t.get('save_path', '')
        name = t.get('name', '')
        torrent_path = os.path.join(save_path, name)
    if delete_torrent(hash_, True):
        clean_nfo_and_delete_folder(torrent_path)
        await update.callback_query.edit_message_text("Torrent and folder deleted (nfo files too).")
    else:
        await update.callback_query.edit_message_text("Failed to delete torrent.")
