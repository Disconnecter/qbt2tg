from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

def get_main_reply_keyboard():
    keyboard = [
        [KeyboardButton("Torrent List")],
        [KeyboardButton("Active Downloads")],
        [KeyboardButton("Help")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Select an action:",
        reply_markup=get_main_reply_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Use the buttons below or send a .torrent file to add a new torrent.\n"
        "To delete a torrent, use the 🗑 button in the torrent list.",
        reply_markup=get_main_reply_keyboard()
    )

async def handle_main_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    if text == "torrent list":
        from .torrent_ops import list_torrents
        await list_torrents(update, context)
    elif text == "active downloads":
        from .torrent_ops import status_torrents
        await status_torrents(update, context)
    elif text == "help":
        await help_command(update, context)
    else:
        await update.message.reply_text("Unknown command. Use the buttons or send a .torrent file.")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith('del_'):
        from .torrent_ops import del_torrent
        hash_ = data[4:]
        await del_torrent(update, context, hash_)
    elif data.startswith('cat_'):
        from .file_upload import handle_category_choice
        category = data[4:]
        await handle_category_choice(update, context, category)
    else:
        await query.answer()