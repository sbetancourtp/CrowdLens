from flask import Blueprint, render_template

from data import shared_state

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def dashboard():
    with shared_state.decks_lock:
        decks = shared_state.shared_decks

    return render_template("dashboard.html", decks=decks)
