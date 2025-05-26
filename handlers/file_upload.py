import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from qbittorrent_api import get_categories, add_torrent

user_file_cache = {}

async def handle_torrent_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if not doc.file_name.endswith('.torrent'):
        from .main_menu import get_main_reply_keyboard
        await update.message.reply_text("Please send a .torrent file.", reply_markup=get_main_reply_keyboard())
        return
    file_path = f"/tmp/{update.effective_user.id}_{doc.file_name}"
    file = await doc.get_file()
    await file.download_to_drive(file_path)
    user_file_cache[update.effective_user.id] = file_path
    categories = get_categories()
    keyboard = []
    if categories:
        for cat in categories.keys():
            keyboard.append([InlineKeyboardButton(cat, callback_data=f"cat_{cat}")])
    keyboard.append([InlineKeyboardButton("No category", callback_data="cat_")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Choose a category for the new torrent:",
        reply_markup=reply_markup
    )

async def handle_category_choice(update: Update, context: ContextTypes.DEFAULT_TYPE, category):
    query = update.callback_query
    await query.answer()
    chat_id = query.from_user.id
    file_path = user_file_cache.get(chat_id)
    if not file_path or not os.path.exists(file_path):
        await query.edit_message_text("File not found. Start again.")
        return
    if add_torrent(file_path, category):
        await query.edit_message_text("Torrent added.")
    else:
        await query.edit_message_text("Failed to add torrent.")
    os.remove(file_path)
    user_file_cache.pop(chat_id, None)