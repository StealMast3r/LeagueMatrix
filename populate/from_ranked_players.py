# python -m populate.from_ranked_players
import random

from datetime import datetime

from services import league_services

_QUEUES_WEIGHTED   = {"RANKED_SOLO_5x5": 90, "RANKED_FLEX_SR": 10}

_APEX_LEAGUES      = frozenset({"challengerleagues", "grandmasterleagues", "masterleagues"})
_RANKED_LEAGUES    = frozenset({"IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "EMERALD", "DIAMOND"})
_ALL_LEAGUES       = _APEX_LEAGUES | _RANKED_LEAGUES

_DIVISIONS         = frozenset({"I", "II", "III", "IV"})
_SERVERS           = frozenset({"kr", "na1", "euw1", "br1", "eun1"})

_PLAYERS_PER_DISCOVERY = 2
_MATCHES_PER_PLAYER = 2

class RankedLadderPopulator:

    def __init__(self, discoveries: int):
        self.discoveries = discoveries
        attempt = 0
        players_discovered = []

        while attempt < discoveries:

            random_server = random.choice(tuple(_SERVERS))
            random_queue = random.choices(population=list(_QUEUES_WEIGHTED.keys()), weights=list(_QUEUES_WEIGHTED.values()), k=1)[0]
            random_league = random.choice(list(_ALL_LEAGUES))

            print(
                f"[{attempt + 1}/{discoveries}]",
                datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                random_server,
                random_queue,
                random_league
            )

            try:

                if random_league in _APEX_LEAGUES:
                    players_discovered = self.apex_populator(random_server, random_queue, random_league)
                else:
                    random_division = random.choice(list(_DIVISIONS))
                    random_page = random.randint(1, 15)
                    print(
                        f"[{attempt + 1}/{discoveries}]",
                        datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                        random_league, 
                        random_division, 
                        f"p.{random_page}")
                    players_discovered = self.normal_populator(random_server, random_queue, random_division, random_league, random_page)

                players_discovered = players_discovered or []
                if not players_discovered:
                    print("No players found")
                    attempt += 1
                    continue

                random_players = random.sample(
                    players_discovered,
                    k=min(_PLAYERS_PER_DISCOVERY, len(players_discovered))
                )

                self.dump_random_matches(random_server, random_players, _MATCHES_PER_PLAYER)
            
            except Exception as e:
                print("Discovery Failed: ", e)

            attempt += 1

    def apex_populator(self, random_server, random_queue, random_league) -> list:
        return league_services.fetch_ranked_apex_entries(random_server, random_queue, random_league)

    def normal_populator(self, random_server, random_queue, random_division, random_league, random_page) -> list:
        return league_services.fetch_ranked_league_entries(random_server, random_queue, random_division, random_league, random_page)

    def dump_random_matches(self, random_server, random_players: list, count: int):
        for player in random_players:
            try:
                puuid = player["puuid"]
                summoner_data = league_services.register_summoner(random_server, puuid=puuid)
                league_services.capture_summoner_ranks(f"{summoner_data["summoner_name"]}#{summoner_data["tag_line"]}", random_server)
                matchlist = league_services.fetch_recent_match_ids(random_server, puuid, count=count) or []
            except Exception as e:
                print("Player Failed: ", e)
                continue

            for match_id in matchlist:
                try:
                    league_services.store_match(match_id)
                except Exception as e:
                    print(f"Match {match_id} failed:", e)

RankedLadderPopulator(3000)