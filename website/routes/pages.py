from flask import Blueprint, render_template
from website.services.dashboard_services import get_dashboard_stats

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def dashboard():
    return render_template("dashboard.html", stats=get_dashboard_stats())


@pages_bp.route("/summoners")
def summoners():
    return render_template("summoners.html")


@pages_bp.route("/matches")
def matches():
    return render_template("matches.html")


@pages_bp.route("/analytics")
def analytics():
    return render_template("analytics.html")