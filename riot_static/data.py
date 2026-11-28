# python -m riot_static.data
import os
from pathlib import Path

from services import league_services

from riot.api_client import RiotApiClient

BASE_URL = "https://ddragon.leagueoflegends.com"
REALM_URL = f"{BASE_URL}/realms/na.json"

CACHE_DIR = Path(__file__).parent / "cache"

_SERVER = "na1"
DEFAULT_LOCALE = "en_US"

def get_current_patch():
    client = RiotApiClient(os.environ.get("RIOT_API_KEY"), _SERVER)
    return client.get_current_server_versions()["v"]

def get_current_champions():
    client = RiotApiClient(os.environ.get("RIOT_API_KEY"), _SERVER)
    return client.get_current_champions_json()

def get_current_champion_information(champion_name):
    client = RiotApiClient(os.environ.get("RIOT_API_KEY"), _SERVER)
    return client.get_champion_information(champion_name)