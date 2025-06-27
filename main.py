#from messaging.telegram_client import run_bot
#from data.db.main_db import initialize_db
#from dotenv import load_dotenv
#import os

#if __name__ == "__main__":
#    load_dotenv()
#    TOKEN = os.getenv("BOT_TOKEN")
#    initialize_db()
#    run_bot(TOKEN)

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
