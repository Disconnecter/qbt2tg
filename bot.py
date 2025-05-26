from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
)
import config
from handlers import (
    send_main_menu, help_command, handle_main_reply,
    handle_buttons, handle_torrent_file, notify_finished
)
from qbittorrent_api import qb_login

def main():
    qb_login()
    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", send_main_menu))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(handle_buttons))
    application.add_handler(MessageHandler(filters.Document.MimeType("application/x-bittorrent"), handle_torrent_file))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_main_reply))
    application.job_queue.run_repeating(
        notify_finished,
        interval=config.CHECK_COMPLETED_INTERVAL,
        first=5
    )
    application.run_polling()

if __name__ == "__main__":
    main()
