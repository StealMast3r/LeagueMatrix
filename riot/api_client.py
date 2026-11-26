import os
import requests
import time

_REGION_TO_PLATFORM: dict[str, str] = {
    "na1":  "https://na1.api.riotgames.com",
    "euw1": "https://euw1.api.riotgames.com",
    "eun1": "https://eun1.api.riotgames.com",
    "kr":   "https://kr.api.riotgames.com",
    "br1":  "https://br1.api.riotgames.com",
    "oc1":  "https://oc1.api.riotgames.com",
    "jp1":  "https://jp1.api.riotgames.com",
    "tr1":  "https://tr1.api.riotgames.com",
    "ru":   "https://ru.api.riotgames.com",
    "la1":  "https://la1.api.riotgames.com",
    "la2":  "https://la2.api.riotgames.com",
    "ph2":  "https://ph2.api.riotgames.com",
    "sg2":  "https://sg2.api.riotgames.com",
    "th2":  "https://th2.api.riotgames.com",
    "tw2":  "https://tw2.api.riotgames.com",
    "vn2":  "https://vn2.api.riotgames.com",
}

_REGION_TO_REGIONAL: dict[str, str] = {
    "br1":  "https://americas.api.riotgames.com",
    "eun1": "https://europe.api.riotgames.com",
    "euw1": "https://europe.api.riotgames.com",
    "jp1":  "https://asia.api.riotgames.com",
    "kr":   "https://asia.api.riotgames.com",
    "la1":  "https://americas.api.riotgames.com",
    "la2":  "https://americas.api.riotgames.com",
    "na1":  "https://americas.api.riotgames.com",
    "oc1":  "https://sea.api.riotgames.com",
    "tr1":  "https://europe.api.riotgames.com",
    "ru":   "https://europe.api.riotgames.com",
    "ph2":  "https://sea.api.riotgames.com",
    "sg2":  "https://sea.api.riotgames.com",
    "th2":  "https://sea.api.riotgames.com",
    "tw2":  "https://sea.api.riotgames.com",
    "vn2":  "https://sea.api.riotgames.com",
}

_REGION_TO_REALM: dict[str, str] = {
    "br1":  "br",
    "eun1": "eune",
    "euw1": "euw",
    "jp1":  "jp",
    "kr":   "kr",
    "la1":  "lan",
    "la2":  "las",
    "na1":  "na",
    "oc1":  "oce",
    "tr1":  "tr",
    "ru":   "ru",
    # SEA servers (Garena → Riot migration) — no dedicated realm, fall back to na
    "ph2":  "na",
    "sg2":  "na",
    "th2":  "na",
    "tw2":  "na",
    "vn2":  "na",
}

DDRAGON_URL = "https://ddragon.leagueoflegends.com"
STATIC_URL  = "https://static.developer.riotgames.com"

_DDRAGON_VERSION_TTL_SECONDS = 21600
_HIGH_TIER_LEAGUES = frozenset({"challengerleagues", "grandmasterleagues", "masterleagues"})
_RANKED_LEAGUES    = frozenset({"IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "EMERALD", "DIAMOND"})
_DIVISIONS         = frozenset({"I", "II", "III", "IV"})
_QUEUES            = frozenset({"RANKED_SOLO_5x5", "RANKED_FLEX_SR"})

def split_riot_id(riot_id: str):
    game_name, separator, tag_line = riot_id.strip().rpartition("#")
    if not separator or not game_name or not tag_line:
        raise ValueError(f"Expected Name#Tag, got {riot_id!r}")
    return game_name, tag_line

class RiotApiClient:

    def __init__(self, api_key: str | None = None, region: str = "na1") -> None:
        resolved_api_key = api_key or os.environ.get("RIOT_API_KEY")
        if not resolved_api_key:
            raise ValueError("No Riot API key found. Set the RIOT_API_KEY environment variable or pass api_key= explicitly.")
        
        region = region.lower()

        platform_url = _REGION_TO_PLATFORM.get(region)
        regional_url = _REGION_TO_REGIONAL.get(region)
        realm        = _REGION_TO_REALM.get(region)

        if not platform_url or not regional_url:
            raise ValueError(f"Invalid region '{region}'. Valid regions: {sorted(_REGION_TO_PLATFORM)}")
        
        self.api_key      = resolved_api_key
        self.region       = region
        self.platform_url = platform_url
        self.regional_url = regional_url
        self.realm        = realm

        self._ddragon_version: str | None = None
        self._ddragon_version_fetched_at: float = 0.0

    def _is_static_url(self, url: str) -> bool:
        return url.startswith((DDRAGON_URL, STATIC_URL))

    def _make_request(self, url: str, retries: int = 3):
        if not url:
            raise ValueError("Invalid URL provided.")
        if retries < 1:
            raise ValueError("retries must be >= 1.")

        is_static = self._is_static_url(url)
        if is_static:
            headers = {}
        else:
            headers = {"X-Riot-Token": self.api_key}

        for attempt in range(1, retries + 1):
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if not is_static:
                    time.sleep(1.2)
            except requests.RequestException as exc:
                if attempt == retries:
                    raise Exception(f"Requests error. Reach retries limit ({retries})")
                time.sleep(1.5 * attempt)
                continue

            status = response.status_code

            if status == 200:
                return response.json()

            if status == 404:
                raise Exception("Ressource not found.")

            if status in (401, 403):
                raise Exception("Check API key.")

            if status == 429:
                retry_after = float(response.headers.get("Retry-After", 2))
                if attempt == retries:
                    raise Exception("Rate limit exhausted after all retries.")
                time.sleep(retry_after + 0.1)
                continue

            if status >= 500:
                backoff = 1.5 * (2 ** (attempt - 1))
                if attempt == retries:
                    raise Exception("Server error.")
                time.sleep(backoff)
                continue

            raise Exception("No Response")

        raise Exception("Exhausted retries")

    # -------------------------------
    # Internal: DDragon version cache
    # -------------------------------

    def _get_ddragon_version(self) -> str:
        """Return cached DDragon patch version, refreshing at most every 6 hour."""
        now = time.monotonic()
        if (
            not self._ddragon_version
            or (now - self._ddragon_version_fetched_at) > _DDRAGON_VERSION_TTL_SECONDS
        ):
            data = self.get_current_server_versions()
            self._ddragon_version = data["dd"]
            self._ddragon_version_fetched_at = now
        return self._ddragon_version

    # ---------------------------
    # DDragon / static endpoints
    # --------------------------

    def get_current_server_versions(self) -> dict:
        """Returns realm version metadata (dd, l, n, profileiconmax, ...)."""
        url = f"{DDRAGON_URL}/realms/{self.realm}.json"
        return self._make_request(url)

    def get_version_history(self) -> list:
        """Returns the full list of published patch versions."""
        url = f"{DDRAGON_URL}/api/versions.json"
        return self._make_request(url)

    def get_current_champions_json(self) -> dict:
        """Returns the full champion roster data for the current patch."""
        v = self._get_ddragon_version()
        url = f"{DDRAGON_URL}/cdn/{v}/data/en_US/champion.json"
        return self._make_request(url) 

    def get_champion_information(self, champion_name: str) -> dict:
        """
        Returns detailed data for a single champion.
        Note: champion_name is case-sensitive and must match DDragon's key
        (e.g. 'AurelionSol', 'MonkeyKing' for Wukong).
        """
        v = self._get_ddragon_version()
        url = f"{DDRAGON_URL}/cdn/{v}/data/en_US/champion/{champion_name}.json"
        return self._make_request(url)

    def get_profile_icon_url(self, icon_id: int) -> str:
        """Returns the CDN URL for a profile icon image (no HTTP request made)."""
        v = self._get_ddragon_version()
        return f"{DDRAGON_URL}/cdn/{v}/img/profileicon/{icon_id}.png"

    def get_summoner_spells(self) -> dict:
        """Returns summoner spell data for the current patch."""
        v = self._get_ddragon_version()
        url = f"{DDRAGON_URL}/cdn/{v}/data/en_US/summoner.json"
        return self._make_request(url)

    def get_queues(self) -> list:
        """Returns the full list of queue type definitions."""
        url = f"{STATIC_URL}/docs/lol/queues.json"
        return self._make_request(url)

    # -----------------------------------------------------------------------
    # Account-V1
    # -----------------------------------------------------------------------

    def get_account(
        self,
        summoner_name: str | None = None,
        tag: str | None = None,
        puuid: str | None = None,
    ) -> dict:
        """
        Returns: puuid, gameName, tagLine.
        Call with either puuid=... or (summoner_name=..., tag=...).
        """
        if puuid:
            url = f"{self.regional_url}/riot/account/v1/accounts/by-puuid/{puuid}"
        elif summoner_name and tag:
            url = f"{self.regional_url}/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag}"
        else:
            raise ValueError("Provide either 'puuid' or both 'summoner_name' and 'tag'.")
        return self._make_request(url)

    # -----------------------------------------------------------------------
    # Summoner-V4
    # -----------------------------------------------------------------------

    def get_summoner(
        self,
        puuid:       str | None = None,
        summoner_id: str | None = None,
        account_id:  str | None = None,
    ) -> dict:
        """
        Returns: id, accountId, puuid, profileIconId, revisionDate, summonerLevel.
        Call with exactly one of the three identifiers.
        """
        if puuid:
            url = f"{self.platform_url}/lol/summoner/v4/summoners/by-puuid/{puuid}"
        elif summoner_id:
            url = f"{self.platform_url}/lol/summoner/v4/summoners/{summoner_id}"
        elif account_id:
            url = f"{self.platform_url}/lol/summoner/v4/summoners/by-account/{account_id}"
        else:
            raise ValueError("Provide one of 'puuid', 'summoner_id', or 'account_id'.")
        return self._make_request(url)

    # -----------------------------------------------------------------------
    # Champion-Mastery-V4
    # -----------------------------------------------------------------------

    def get_champion_mastery(self, puuid: str) -> list:
        """Returns all champion mastery entries for a summoner."""
        url = f"{self.platform_url}/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}"
        return self._make_request(url)

    def get_champion_mastery_score(self, puuid: str) -> int:
        """Returns the total mastery score (sum of all champion mastery levels)."""
        url = f"{self.platform_url}/lol/champion-mastery/v4/scores/by-puuid/{puuid}"
        return self._make_request(url)

    def get_top_champion_masteries(self, puuid: str, amount: int = 3) -> list:
        """Returns the top N champion masteries for a summoner."""
        if amount < 1 or amount > 100:
            raise ValueError("amount must be between 1 and 100.")
        url = f"{self.platform_url}/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top?count={amount}"
        return self._make_request(url)

    # -----------------------------------------------------------------------
    # League-V4
    # -----------------------------------------------------------------------

    def get_league_entries_by_puuid(self, puuid: str) -> list:
        """Returns all ranked queue entries for a summoner (SoloQ, Flex, etc.)."""
        url = f"{self.platform_url}/lol/league/v4/entries/by-puuid/{puuid}"
        return self._make_request(url)

    def get_high_tier_league_entries(self, queue: str, league: str) -> list:
        """
    Returns the full player list for Challenger / Grandmaster / Master in Queue.
        league must be one of: 'challengerleagues', 'grandmasterleagues', 'masterleagues'
        """
        league = league.lower()
        if league not in _HIGH_TIER_LEAGUES:
            raise ValueError(f"league must be one of {sorted(_HIGH_TIER_LEAGUES)}")
        if queue not in _QUEUES:
            raise ValueError(f"queue must be one of {sorted(_QUEUES)}")
        url = f"{self.platform_url}/lol/league/v4/{league}/by-queue/{queue}"
        return self._make_request(url)

    def get_ranked_league_entries(self, league: str, division: str, queue: str, page: int = 1) -> list:
        """
        Returns a paginated list of summoners at a given tier/division in Queue.
        league:   IRON / BRONZE / SILVER / GOLD / PLATINUM / EMERALD / DIAMOND
        division: I / II / III / IV
        page:     1-based page number
        queue:    RANKED_SOLO_5V5 / RANKED_FLEX_SR
        """
        league   = league.upper()
        division = division.upper()
        if league not in _RANKED_LEAGUES:
            raise ValueError(f"league must be one of {sorted(_RANKED_LEAGUES)}")
        if division not in _DIVISIONS:
            raise ValueError(f"division must be one of {sorted(_DIVISIONS)}")
        if queue not in _QUEUES:
            raise ValueError(f"queue must be one of {sorted(_QUEUES)}")
        if not isinstance(page, int) or page < 1:
            raise ValueError("page must be a positive integer.")
        url = (
            f"{self.platform_url}/lol/league/v4/entries"
            f"/{queue}/{league}/{division}?page={page}"
        )
        return self._make_request(url)

    # -----------------------------------------------------------------------
    # Match-V5
    # -----------------------------------------------------------------------

    def get_matches_by_puuid(
        self,
        puuid:      str,
        queue:      int | None = None,
        type:       str | None = None,
        start:      int = 0,
        count:      int = 20,
        start_time: int | None = None,
        end_time:   int | None = None,
    ) -> list:
        """
        Returns a list of match IDs for a summoner.

        queue:      queueId integer (see get_queues())
        type:       'ranked', 'normal', 'tourney', 'tutorial'
        start:      offset into match history (default 0)
        count:      number of matches to return (max 100)
        start_time: epoch timestamp in seconds (matches from June 16 2021 onwards)
        end_time:   epoch timestamp in seconds
        """
        count = min(max(count, 1), 100)
        params: dict[str, int | str] = {"start": start, "count": count}
        if queue      is not None: params["queue"]     = queue
        if type       is not None: params["type"]      = type
        if start_time is not None: params["startTime"] = start_time
        if end_time   is not None: params["endTime"]   = end_time

        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{self.regional_url}/lol/match/v5/matches/by-puuid/{puuid}/ids?{query_string}"
        return self._make_request(url)

    def get_match(self, match_id: str) -> dict:
        """Returns full match data for a given match ID."""
        url = f"{self.regional_url}/lol/match/v5/matches/{match_id}"
        return self._make_request(url)

    def get_match_timeline(self, match_id: str) -> dict:
        """Returns frame-by-frame timeline data for a match."""
        url = f"{self.regional_url}/lol/match/v5/matches/{match_id}/timeline"
        return self._make_request(url)

    # -----------------------------------------------------------------------
    # Spectator-V5
    # -----------------------------------------------------------------------

    def get_current_match_by_puuid(self, puuid: str) -> dict:
        """
        Returns live game data for a summoner currently in-game.
        Note: Arena (2v2v2v2) matches are not exposed by this endpoint.
        """
        url = f"{self.platform_url}/lol/spectator/v5/active-games/by-summoner/{puuid}"
        return self._make_request(url)

    # -----------------------------------------------------------------------
    # Challenges-V1
    # -----------------------------------------------------------------------

    def get_challenges(self, puuid: str) -> dict:
        """Returns challenge progression data for a summoner."""
        url = f"{self.platform_url}/lol/challenges/v1/player-data/{puuid}"
        return self._make_request(url)

    def get_challenges_config(self) -> list:
        """Returns the configuration and metadata for all challenges."""
        url = f"{self.platform_url}/lol/challenges/v1/challenges/config"
        return self._make_request(url)