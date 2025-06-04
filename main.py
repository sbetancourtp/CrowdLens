from messaging.telegram_client import run_bot
from data.db.main_db import initialize_db

if __name__ == "__main__":
    TOKEN = "7781537287:AAHTwrmZEjeY4QU_SlcvDUAc1F72Eqgc5EQ"
    initialize_db()
    run_bot(TOKEN)
