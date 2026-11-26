# python -m tests.test_year_in_lol
import time
from datetime import datetime, timedelta
from services import league_services

def create_date_range() -> list:

    # 2026 Season Start: January 8, 2026 (Patch 26.1)
    start = datetime(2026, 1, 7, 1, 0, 0)
    start_s = int(start.timestamp())
    # 2026 Season End:   November 25rd, 2026 (Patch 26.23)  
    end = datetime(2026, 11, 25, 9, 0, 0)
    end_s = int(end.timestamp())

    days = []
    current_end = end

    while current_end > start:
        current_start = max(current_end - timedelta(days=2), start)
        days.append((
            int(current_start.timestamp()),
            int(current_end.timestamp())
        ))
        current_end = current_start

    # days.reverse() chronological order if needed
    return days

def ingest_missing_matches(calendar: list, server: str, summoner_name: str):

    summoner = league_services.register_summoner(server, summoner_name=summoner_name)
    summoner_db = league_services.get_stored_summoner(server, summoner_name)

    i = 0
    for day in calendar:

        start_time = day[0]
        start_date = datetime.fromtimestamp(start_time).strftime("%Y-%m-%d")
        end_time = day[1]
        end_date = datetime.fromtimestamp(end_time).strftime("%Y-%m-%d")

        matchlist = league_services.fetch_recent_match_ids(
            server=server,

            puuid=summoner_db["puuid"],
            count=100,
            start_time=start_time,
            end_time=end_time
        )

        for match_id in matchlist:
            try:
                match_status = league_services.store_match(match_id)
                timeline_status = league_services.store_timeline(match_id)
                print(match_status, timeline_status)
            except:
                print(f"Failed to store {match_id}")

        i = i + 1
        print(summoner_name, i, start_date, end_date, len(matchlist))

def request_yearly_summary():
    pass

def main(server: str, summoner_name: str):
    calendar = create_date_range()
    ingest_missing_matches(calendar, server, summoner_name)
    #data = request_yearly_summary()

if __name__ == "__main__":
    server = "na1"
    summoner_name = "Steal#3V3"
    main(server, summoner_name)

    server = "na1"
    summoner_name = "Firestorm#na2"
    main(server, summoner_name)

    server = "euw1"
    summoner_name = "Lost Kitten#Hiss"
    main(server, summoner_name)