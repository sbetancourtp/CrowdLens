# main.py

from messaging.telegram_client import run_bot
from data.db.main_db import initialize_db
from dotenv import load_dotenv
import os
import threading
import time
from app import app
from processing.deck_generator import generate_decks_from_entries
from semantic_processing.semantic_deck_generator import generate_semantic_decks


if __name__ == "__main__":
    # Load env variables
    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")

    initialize_db()

    bot_thread = threading.Thread(target=run_bot, args=(TOKEN,), daemon=True)
    bot_thread.start()

    time.sleep(3)

    # generate_decks_from_entries - generate_semantic_decks
    deck_thread = threading.Thread(target=generate_semantic_decks, daemon=True)
    deck_thread.start()

    # Execute Flask app on main thread
    app.run(debug=True, use_reloader=False)
