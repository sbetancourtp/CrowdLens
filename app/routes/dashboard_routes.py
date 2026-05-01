from flask import Blueprint, render_template, jsonify, abort, url_for

from data import shared_state
from models.deck_models import DeckRepo
from typing import List

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():
    with shared_state.decks_lock:
        decks: List[DeckRepo] = shared_state.shared_decks
    sorted_decks = sorted(decks, key=lambda d: (-len(d.entries_list)))
    #prior_decks = [deck.priority + num for deck, num in enumerate(sorted_decks)]

    return render_template("dashboard.html", decks=sorted_decks)


@dashboard_bp.route("/api/decks")
def api_decks():
    with shared_state.decks_lock:
        decks = shared_state.shared_decks.copy()
    return jsonify([deck.model_dump() for deck in decks])


@dashboard_bp.route("/deck/<deck_id>")
def deck_details(deck_id: str):
    with shared_state.decks_lock:
        matching_deck = next((deck for deck in shared_state.shared_decks if str(deck.deck_id) == deck_id), None)

    if not matching_deck:
        abort(404)

    # Sort entries from most recent to oldest
    sorted_entries = sorted(matching_deck.entries_list, key=lambda e: e.timestamp, reverse=True)

    return render_template(
        "deck_details.html",
        deck=matching_deck,
        entries=sorted_entries
    )
