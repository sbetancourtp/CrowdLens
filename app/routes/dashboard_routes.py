from flask import Blueprint, render_template, jsonify

from data import shared_state

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():
    with shared_state.decks_lock:
        decks = shared_state.shared_decks

    return render_template("dashboard.html", decks=decks)


@dashboard_bp.route("/api/decks")
def api_decks():
    with shared_state.decks_lock:
        decks = shared_state.shared_decks.copy()
    return jsonify([deck.model_dump() for deck in decks])
