from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import os
from qbittorrent_api import (
    get_all_torrents, get_torrent_by_hash, delete_torrent,
    pause_torrent, resume_torrent
)
from utils import (
    clean_nfo_and_delete_folder,
    sanitize_torrent_name
)

STATE_LABELS = {
    'pauseddl': 'Paused',
    'pausedup': 'Paused',
    'queueddl': 'Queued',
    'queuedup': 'Queued',
    'stalleddl': 'Stalled',
    'stalledup': 'Stalled',
    'downloading': 'Downloading',
    'uploading': 'Seeding',
    'checkingdl': 'Checking',
    'checkingup': 'Checking',
    'checkingresumedata': 'Checking',
    'metadl': 'Fetching metadata',
    'forceddl': 'Forced',
    'forcedup': 'Forced',
    'moving': 'Moving',
    'error': 'Error',
    'missingfiles': 'Missing files',
    'unknown': 'Unknown'
}


def format_state_label(state):
    if not state:
        return STATE_LABELS['unknown']
    return STATE_LABELS.get(state.lower(), state)

async def list_torrents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    torrents = get_all_torrents()
    if not torrents:
        from .main_menu import get_main_reply_keyboard
        await update.message.reply_text("No torrents.", reply_markup=get_main_reply_keyboard())
        return
    for idx, t in enumerate(torrents, 1):
        short = sanitize_torrent_name(t['name'])
        if len(short) > 60:
            short = short[:57] + "..."
        state = t.get('state', 'unknown')
        state_label = format_state_label(state)
        progress = t.get('progress', 0) * 100
        text = f"{idx}. {short}\n{progress:.1f}% | {state_label}"
        is_paused = state.lower().startswith('paused')
        control_label = "Start" if is_paused else "Stop"
        control_action = "resume" if is_paused else "pause"
        keyboard = [[
            InlineKeyboardButton(control_label, callback_data=f"{control_action}_{t['hash']}"),
            InlineKeyboardButton("Delete", callback_data=f"del_{t['hash']}")
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text, reply_markup=reply_markup)

async def status_torrents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    torrents = get_all_torrents()
    loading = [t for t in torrents if t['progress'] < 1.0 and t['state'] not in ('pausedUP', 'pausedDL')]
    from .main_menu import get_main_reply_keyboard
    if not loading:
        await update.message.reply_text("No active downloads.", reply_markup=get_main_reply_keyboard())
        return
    msg_lines = []
    for t in loading:
        name = sanitize_torrent_name(t['name'])
        state_label = format_state_label(t.get('state', 'unknown'))
        msg_lines.append(f"{name} ({t['progress']*100:.1f}% | {state_label})")
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

async def pause_torrent_action(update: Update, context: ContextTypes.DEFAULT_TYPE, hash_):
    query = update.callback_query
    if pause_torrent(hash_):
        await query.answer("Torrent paused.")
    else:
        await query.answer("Failed to pause torrent.", show_alert=True)

async def resume_torrent_action(update: Update, context: ContextTypes.DEFAULT_TYPE, hash_):
    query = update.callback_query
    if resume_torrent(hash_):
        await query.answer("Torrent started.")
    else:
        await query.answer("Failed to start torrent.", show_alert=True)
