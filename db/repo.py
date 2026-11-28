from pathlib import Path

QUERIES_DIR = Path(__file__).parent / "queries"

def load_query(name):
    return (QUERIES_DIR / f"{name}.sql").read_text()

class SummonerRepo:

    def __init__(self, conn):
        self.conn = conn

    def upsert(self, row):
        with self.conn.cursor() as cur:
            cur.execute(load_query("upsert_summoner"), row)
        self.conn.commit()

    def get_by_name(self, player_name, tag_line, server):
        player_dict = {
            "summoner_name": player_name,
            "tag_line": tag_line,
            "region": server,
        }
        with self.conn.cursor() as cur:
            cur.execute(load_query("get_summoner"), player_dict)
            return cur.fetchone()

    def get_by_puuid(self, server, puuid):
        player_dict = {
            "puuid": puuid,
            "region": server
        }
        with self.conn.cursor() as cur:
            cur.execute(load_query("get_summoner_by_puuid"), player_dict)
            return cur.fetchone()

class MatchRepo:

    def __init__(self, conn):
            self.conn = conn

    def match_exists(self, match_id):
        match_dict = {"match_id": match_id}
        with self.conn.cursor() as cur:
            cur.execute(load_query("exists_match"), match_dict)
            return cur.fetchone() is not None

    def insert(self, match, teams, participants, subteams):
        try:
            with self.conn.cursor() as cur:
                cur.execute(load_query("insert_match"), match)
                cur.executemany(load_query("insert_team"), teams)
                if subteams:
                    cur.executemany(load_query("insert_subteam"), subteams)
                cur.executemany(load_query("insert_participant"), participants)
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def get_match_by_id(self, match_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute(load_query("get_match_by_id"), {"match_id": match_id})
                return cur.fetchone()
        except Exception:
            raise

    def get_participants_by_match_id(self, match_id):
        try:
            with self.conn.cursor() as cur:
                cur.execute(load_query("get_participants_by_match_id"), {"match_id": match_id})
                return cur.fetchall()
        except Exception:
            raise ValueError

    def get_participants_by_puuid(self, puuid):
        try:
            with self.conn.cursor() as cur:
                cur.execute(load_query("get_participants_by_puuid"), {"puuid": puuid})
                return cur.fetchall()
        except Exception:
            raise ValueError

    def get_matches(self, match_ids: list) -> list:
        if not match_ids:
            return []

        try:
            placeholders = ", ".join(["%s"] * len(match_ids))
            query = load_query("get_matches").format(placeholders=placeholders)
            with self.conn.cursor() as cur:
                cur.execute(query, tuple(match_ids))
                return cur.fetchall()
        except Exception as e:
            raise ValueError(f"Failed to retrieve matches: {e}") from e

    def get_teams(self, match_ids: list) -> list:
        if not match_ids:
            return []

        try:
            placeholders = ", ".join(["%s"] * len(match_ids))
            query = load_query("get_teams").format(placeholders=placeholders)
            with self.conn.cursor() as cur:
                cur.execute(query, tuple(match_ids))
                return cur.fetchall()
        except Exception as e:
            raise ValueError(f"Failed to retrieve matches: {e}") from e

    def get_subteams(self, match_ids: list) -> list:
        if not match_ids:
            return []

        try:
            placeholders = ", ".join(["%s"] * len(match_ids))
            query = load_query("get_subteams").format(placeholders=placeholders)
            with self.conn.cursor() as cur:
                cur.execute(query, tuple(match_ids))
                return cur.fetchall()
        except Exception as e:
            raise ValueError(f"Failed to retrieve matches: {e}") from e

    def get_all_participants(self, match_ids: list) -> list:
        if not match_ids:
            return []

        try:
            placeholders = ", ".join(["%s"] * len(match_ids))
            query = load_query("get_all_participants").format(placeholders=placeholders)
            with self.conn.cursor() as cur:
                cur.execute(query, tuple(match_ids))
                return cur.fetchall()
        except Exception as e:
            raise ValueError(f"Failed to retrieve matches: {e}") from e

class TimelineRepo:

    def __init__(self, conn):
        self.conn = conn

    def timeline_exists(self, match_id: str):
        match_dict = {"match_id": match_id}
        with self.conn.cursor() as cur:
            cur.execute(load_query("exists_timeline"), match_dict)
            return cur.fetchone() is not None

    def insert(self, match_timeline, timeline_frames, timeline_events, participant_frames):
        try:
            with self.conn.cursor() as cur:
                cur.execute(load_query("insert_match_timeline"), match_timeline)
                cur.executemany(load_query("insert_timeline_frame"), timeline_frames)
                cur.executemany(load_query("insert_timeline_event"), timeline_events)
                cur.executemany(load_query("insert_participant_frame"), participant_frames)
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def get_timeline(self, match_id: str) -> dict | None:
        search_dict = {"match_id": match_id}
        with self.conn.cursor() as cur:

            cur.execute(load_query("get_match_timeline"), search_dict)
            timeline = cur.fetchone()
            if timeline is None:
                return None

            cur.execute(load_query("get_timeline_frames"), search_dict)
            frames = cur.fetchall()

            cur.execute(load_query("get_timeline_events"), search_dict)
            events = cur.fetchall()

            cur.execute(load_query("get_participant_frames"), search_dict)
            participant_frames = cur.fetchall()
        
        return {
            "timeline": timeline,
            "frames": frames,
            "events": events,
            "participant_frames": participant_frames,
            "match_id": match_id
        }

    def get_all_timelines(self, match_ids: list) -> list:
        if not match_ids:
            return []

        try:
            placeholders = ", ".join(["%s"] * len(match_ids))
            query = load_query("get_all_timelines").format(placeholders=placeholders)#!
            with self.conn.cursor() as cur:
                cur.execute(query, tuple(match_ids))
                return cur.fetchall()
        except Exception as e:
            raise ValueError(f"Failed to retrieve matches: {e}") from e

    def get_all_timeline_frames(self, match_ids: list) -> list:
            if not match_ids:
                return []
    
            try:
                placeholders = ", ".join(["%s"] * len(match_ids))
                query = load_query("get_all_timeline_frames").format(placeholders=placeholders)
                with self.conn.cursor() as cur:
                    cur.execute(query, tuple(match_ids))
                    return cur.fetchall()
            except Exception as e:
                raise ValueError(f"Failed to retrieve matches: {e}") from e

    def get_all_participant_frames(self, match_ids: list) -> list:
            if not match_ids:
                return []
    
            try:
                placeholders = ", ".join(["%s"] * len(match_ids))
                query = load_query("get_all_participant_frames").format(placeholders=placeholders)
                with self.conn.cursor() as cur:
                    cur.execute(query, tuple(match_ids))
                    return cur.fetchall()
            except Exception as e:
                raise ValueError(f"Failed to retrieve matches: {e}") from e

    def get_all_timeline_events(self, match_ids: list) -> list:
            if not match_ids:
                return []
    
            try:
                placeholders = ", ".join(["%s"] * len(match_ids))
                query = load_query("get_all_timeline_events").format(placeholders=placeholders)
                with self.conn.cursor() as cur:
                    cur.execute(query, tuple(match_ids))
                    return cur.fetchall()
            except Exception as e:
                raise ValueError(f"Failed to retrieve matches: {e}") from e

class RankedRepo:

    def __init__(self, conn):
        self.conn = conn

    def insert_entry(self, entry):
        try:
            with self.conn.cursor() as cur:
                cur.execute(load_query("insert_ranked_entry"), entry)
            self.conn.commit()
        except:
            self.conn.rollback()
            raise ValueError

    def get_all_latest_entries(self, puuid: str, server: str):
        search_dict = {
            "puuid": puuid,
            "region": server
        }
        with self.conn.cursor() as cur:
            cur.execute(load_query("get_latest_ranked_entries"), search_dict)
            return cur.fetchall()

    def get_latest_entry(self, puuid, region, queue_type):
        search_dict = {
            "puuid": puuid,
            "region": region,
            "queue_type": queue_type
        }
        try:
            with self.conn.cursor() as cur:
                cur.execute(load_query("get_latest_rank_by_queue"), search_dict)
                return cur.fetchone()
        except:
            raise ValueError

class MasteryRepo:

    def __init__(self, conn):
        self.conn = conn

    def insert_entry(self, entry):
        try:
            with self.conn.cursor() as cur:
                cur.execute(load_query("upsert_mastery_entry"), entry)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise ValueError(e)

    def get_mastery_entries(self, server, puuid):
        try:
            with self.conn.cursor() as cur:
                cur.execute(load_query("get_mastery_entries"), {"puuid": puuid, "region": server})
                return cur.fetchall()
        except Exception as e:
            raise ValueError(e)