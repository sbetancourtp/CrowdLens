from flask import Blueprint, render_template
from processing.deck_generator import generate_decks_from_entries

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():
    mock_decks = generate_decks_from_entries()

    return render_template("dashboard.html", decks=mock_decks)
