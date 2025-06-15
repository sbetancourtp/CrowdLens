from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters, ConversationHandler
)
from uuid import uuid4
from models.entry_models import EntryRepo
from data.db.main_db import write_entry_to_db

SEND_ENTRY_WAITING_MESSAGE = 1


async def send_entry_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please send the me ssage now. Ensure that the text is well-written"
        " and free of any inappropriate or offensive language, as such content will be excluded."
    )
    return SEND_ENTRY_WAITING_MESSAGE


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Aquí están los comandos disponibles:\n/start - Inicia el bot\n/help - Muestra esta ayuda")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operación cancelada.")
    return ConversationHandler.END


async def capture_entry_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if message.text:
        media_type = "text"
    elif message.photo:
        media_type = "photo"
    elif message.voice:
        media_type = "voice"
    else:
        media_type = "unknown"

    entry = EntryRepo(
        entry_id=str(uuid4()),
        message_id=message.message_id,
        user_id=message.from_user.id,
        username=message.from_user.username,
        timestamp=message.date,
        text=message.text,
        raw_message=message.to_dict(),
        media_type=media_type,
        save_flag=False
    )

    # this func shows in telegram chat what was saved in the DB, debug purposes
    # await message.reply_text(f"Entry received:\n{entry}")

    write_entry_to_db(entry)

    print('Entry successfully written to DB ✅')

    return ConversationHandler.END


def run_bot(token: str):
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    send_entry_conv = ConversationHandler(
        entry_points=[CommandHandler("send_entry", send_entry_command)],
        states={
            SEND_ENTRY_WAITING_MESSAGE: [
                MessageHandler(filters.ALL, capture_entry_message)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(send_entry_conv)

    app.run_polling()
