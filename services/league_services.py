import os
from datetime import datetime, timedelta

from riot.api_client import RiotApiClient, split_riot_id

from db.conn import get_connection
from db.mapping import (
    build_match_row, 
    build_participant_rows, 
    build_team_rows, 
    build_match_timeline, 
    build_timeline_frames_events_participants, 
    build_subteam_rows, 
    build_ranked_entries,
    build_champion_mastery_entries
)
from db.repo import (
    SummonerRepo, 
    MatchRepo, 
    TimelineRepo, 
    RankedRepo,
    MasteryRepo
)

# ============================================================
# CONSTANTS & HELPERS
# ============================================================

ARENA_QUEUE_IDS = frozenset({1700, 1710, 1740, 1750})

def is_arena_queue(queue_id: int) -> bool:
    return queue_id in ARENA_QUEUE_IDS

# ============================================================
# SUMMONER SERVICES
# ============================================================

def register_summoner(server: str, summoner_name: str | None = None, puuid: str | None = None) -> dict:

    riot_client = RiotApiClient(os.environ.get("RIOT_API_KEY"), server)

    if puuid:
        account = riot_client.get_account(puuid=puuid)
    elif summoner_name:
        game_name, tag_line = split_riot_id(summoner_name)
        account = riot_client.get_account(summoner_name=game_name, tag=tag_line)
    else:
        raise ValueError("Either puuid or summoner_name must be provided.")
    
    summoner = riot_client.get_summoner(account["puuid"])

    row = {
        "puuid": account["puuid"],
        "summoner_name": account["gameName"],
        "tag_line": account["tagLine"],
        "region": riot_client.region,
        "profile_icon_id": summoner["profileIconId"],
        "summoner_level": summoner["summonerLevel"],
        "revision_date": summoner["revisionDate"],
    }

    with get_connection() as conn:
        SummonerRepo(conn).upsert(row)

    return row

def get_stored_summoner(server: str, summoner_name: str) -> dict | None:

    try:
        game_name, tag_line = split_riot_id(summoner_name)
    except ValueError:
        return None

    with get_connection() as conn:
        row = SummonerRepo(conn).get_by_name(game_name, tag_line, server)

    return row

# ============================================================
# MATCH SERVICES
# ============================================================

def store_match(match_id: str) -> bool:

    with get_connection() as conn:
        if MatchRepo(conn).match_exists(match_id):
            return False

    server = match_id.partition("_")[0]
    client = RiotApiClient(os.environ.get("RIOT_API_KEY"), server)

    match_data = client.get_match(match_id)

    match = build_match_row(match_data)
    teams = build_team_rows(match_data)
    participants = build_participant_rows(match_data)

    if is_arena_queue(match_data["info"]["queueId"]):
        subteams = build_subteam_rows(match_data)
    else:
        subteams = []

    with get_connection() as conn:
        MatchRepo(conn).insert(match, teams, participants, subteams)

    return True

def get_stored_match(match_id: str) -> dict | None:

    with get_connection() as conn:
        if not MatchRepo(conn).match_exists(match_id):
            return None
        return MatchRepo(conn).get_match_by_id(match_id)

def get_match_participants(match_id: str) -> list[dict]:
    with get_connection() as conn:
        return MatchRepo(conn).get_participants_by_match_id(match_id)

# ============================================================
# TIMELINE SERVICES
# ============================================================

def store_timeline(match_id: str) -> bool:
    
    with get_connection() as conn:
        if TimelineRepo(conn).timeline_exists(match_id):
            return False
    
    server = match_id.partition("_")[0]
    client = RiotApiClient(os.environ.get("RIOT_API_KEY"), server)

    timeline_data = client.get_match_timeline(match_id)

    match_timeline = build_match_timeline(timeline_data)
    timeline_frames, timeline_events, participant_frames = build_timeline_frames_events_participants(timeline_data)

    with get_connection() as conn:
        TimelineRepo(conn).insert(match_timeline, timeline_frames, timeline_events, participant_frames)

    return True

def get_stored_timeline(match_id: str) -> dict | None:

    with get_connection() as conn:
        if not TimelineRepo(conn).timeline_exists(match_id):
            return None
        return TimelineRepo(conn).get_timeline(match_id)

# ============================================================
# RANKED SERVICES
# ============================================================

def capture_summoner_ranks(summoner_name: str, server: str) -> list[dict]:

    client = RiotApiClient(os.environ.get("RIOT_API_KEY"), server)

    summoner = get_stored_summoner(server, summoner_name)
    if summoner is None:
        summoner = register_summoner(server, summoner_name=summoner_name)

    ranked_entries = client.get_league_entries_by_puuid(summoner["puuid"])
    entries = build_ranked_entries(summoner["puuid"], server, ranked_entries)

    for entry in entries:

        with get_connection() as conn:

            latest = RankedRepo(conn).get_latest_entry(summoner["puuid"], server, entry["queue_type"])

            if latest is not None:
                last_captured = latest["captured_at"]

                if datetime.now() - last_captured < timedelta(minutes=30):
                    continue

            RankedRepo(conn).insert_entry(entry)

    return ranked_entries

def get_latest_rank_snapshots(server: str, puuid: str) -> dict:

    with get_connection() as conn:
        return RankedRepo(conn).get_all_latest_entries(puuid, server)

# ============================================================
# CHAMPION MASTERY SERVICES
# ============================================================

def upsert_champion_mastery(server: str, puuid: str) -> list[dict]:
    client = RiotApiClient(os.environ.get("RIOT_API_KEY"), server)
    
    mastery_data = client.get_champion_mastery(puuid)
    mastery_entries = build_champion_mastery_entries(server, puuid, mastery_data)
    with get_connection() as conn:
        for entry in mastery_entries:
            MasteryRepo(conn).insert_entry(entry)

    return mastery_data

def get_mastery_entries(server: str, puuid: str) -> list[dict]:
    with get_connection() as conn:
        return MasteryRepo(conn).get_mastery_entries(server, puuid)

# ============================================================
# RIOT API SERVICES
# ============================================================

def fetch_recent_match_ids(
    server: str,
    puuid: str,
    queue: int | None = None,
    game_type: str | None = None,
    start: int = 0,
    count: int = 20,
    start_time: int | None = None,
    end_time: int | None = None,
) -> list[dict]:
    client = RiotApiClient(os.environ.get("RIOT_API_KEY"), server)
    
    return client.get_matches_by_puuid(
        puuid=puuid,
        queue=queue,
        type=game_type,
        start=start,
        count=count,
        start_time=start_time,
        end_time=end_time
    )

def fetch_ranked_league_entries(server: str, queue: str, division, tier, page) -> list[dict]:
    client = RiotApiClient(os.environ.get("RIOT_API_KEY"), server)
    return client.get_ranked_league_entries(tier, division, queue, page)

def fetch_ranked_apex_entries(server, queue, tier) -> list:
    client = RiotApiClient(os.environ.get("RIOT_API_KEY"), server)
    return client.get_high_tier_league_entries(queue, tier)["entries"]

# ============================================================
# RIOT STATIC API SERVICES
# ============================================================

def fetch_current_patch(server):
    client = RiotApiClient(os.environ.get("RIOT_API_KEY"), server)
    return client.get_current_server_versions()

def fetch_current_champions(server):
    client = RiotApiClient(os.environ.get("RIOT_API_KEY"), server)
    return client.get_current_champions_json()

def fetch_current_champion_information(server, champion_name):
    client = RiotApiClient(os.environ.get("RIOT_API_KEY"), server)
    return client.get_champion_information(champion_name)

def fetch_current_champion_information_by_int(server, champion_int):
    pass