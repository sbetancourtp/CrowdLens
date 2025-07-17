from flask import Flask
from app.routes.dashboard_routes import dashboard_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(dashboard_bp)
    return app
