from flask import Blueprint, render_template
from website.services.dashboard_services import get_dashboard_stats

pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/")
def index():
    return render_template("index.html")

@pages_bp.route("/dashboard")
def dashboard():
    stats = get_dashboard_stats()
    return render_template("dashboard.html", db_usage=stats["db_usage"], rows_length=stats["rows_length"])

@pages_bp.route("/matches")
def matches():
    return render_template("matches.html")

@pages_bp.route("/analytics")
def analytics():
    return render_template("analytics.html")