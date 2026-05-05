from flask import Flask

app = Flask(__name__)

from app.routes.dashboard_routes import dashboard
