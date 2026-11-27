# python -m riot_static.data
from pathlib import Path

from services import league_services

BASE_URL = "https://ddragon.leagueoflegends.com"
REALM_URL = f"{BASE_URL}/realms/na.json"

CACHE_DIR = Path(__file__).parent / "cache"

_SERVER = "na1"
DEFAULT_LOCALE = "en_US"

def get_current_patch():
    return league_services.fetch_current_patch(_SERVER)["v"]

def get_current_champions():
    return league_services.fetch_current_champions(_SERVER)

def get_current_champion_information(champion_name):
    return league_services.fetch_current_champion_information(_SERVER, champion_name)