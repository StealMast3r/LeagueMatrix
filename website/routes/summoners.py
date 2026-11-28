from flask import Blueprint, render_template, request

from services.league_services import get_stored_summoner

summoners_bp = Blueprint("summoners", __name__)

@summoners_bp.route("/")
def index():
    return render_template("summoners.html")

@summoners_bp.route("/search", methods=["POST"])
def search():

    riot_id = request.form.get("riot_id", "").strip()
    region = request.form.get("region", "").strip()

    if not riot_id or not region:
        return render_template(
            "summoners.html",
            error="Please provide a Riot ID and region."
        )

    summoner = get_stored_summoner(
        server=region,
        summoner_name=riot_id
    )

    if summoner is None:
        return render_template(
            "summoners.html",
            not_found=True,
            riot_id=riot_id,
            region=region
        )

    return render_template(
        "summoners.html",
        summoner=summoner
    )