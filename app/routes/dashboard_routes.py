from flask import Blueprint, render_template
from models.deck_models import DeckRepo
from uuid import uuid4
from datetime import datetime

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def dashboard():
    # Simulamos algunos decks de prueba
    mock_decks = [
        DeckRepo(
            deck_id=uuid4(),
            deck_title=f"Deck {i+1}",
            first_entry_date=datetime(2024, 1, 1),
            last_entry_date=datetime(2024, 6, 1),
            provided_keywords=["demo", "flask"],
            generated_keywords=["example", "keywords"],
            all_entries_summary_sentence="Resumen simulado.",
            save_flag=False,
            priority=i + 1
        )
        for i in range(11)
    ]
    mock_decks = sorted(mock_decks, key=lambda d: d.priority)

    return render_template("dashboard.html", decks=mock_decks)
