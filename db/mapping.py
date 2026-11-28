import json

ARENA_QUEUE_IDS = {1700, 1710, 1740, 1750}

def is_arena_match(queue_id: int) -> bool:
    return queue_id in ARENA_QUEUE_IDS

def build_match_row(match_data) -> dict:
    info = match_data["info"]
    metadata = match_data["metadata"]

    row = {
        "match_id": metadata.get("matchId", "N/A"),
        "platform_id": info.get("platformId", "N/A"),
        "game_id": info.get("gameId", 0),
        "end_of_game_result": info.get("endOfGameResult", "N/A"),
        "data_version": metadata.get("dataVersion", "N/A"),
        "game_creation": info.get("gameCreation", 0),
        "game_duration": info.get("gameDuration", 0),
        "game_end_timestamp": info.get("gameEndTimestamp", 0),
        "game_start_timestamp": info.get("gameStartTimestamp", 0),
        "map_id": info.get("mapId", 0),
        "queue_id": info.get("queueId", 0),
        "game_mode": info.get("gameMode", "N/A"),
        "game_type": info.get("gameType", "N/A"),
        "game_version": info.get("gameVersion", "N/A"),
        "patch": ".".join(info["gameVersion"].split(".")[:2]),
    }
    return row

def build_team_rows(match_data) -> list:
    info = match_data["info"]
    metadata = match_data["metadata"]
    rows = []

    for team in info["teams"]:
        objectives = team["objectives"]
        champions = objectives.get("champion", {})
        baron = objectives.get("baron", {})
        dragon = objectives.get("dragon", {})
        inhibitor = objectives.get("inhibitor", {})
        rift_herald = objectives.get("riftHerald", {})
        tower = objectives.get("tower", {})
        row = {
            "match_id": metadata.get("matchId", "N/A"),
            "team_id": team.get("teamId", 0),
            "win": team.get("win", False),
            "bans": json.dumps(team["bans"]),

            "champion_kills": champions.get("kills", 0),
            "first_blood": champions.get("first", False),
            "baron_kills": baron.get("kills", 0),
            "baron_first": baron.get("first", 0),
            "dragon_kills": dragon.get("kills", 0),
            "dragon_first": dragon.get("first", 0),
            "inhibitor_kills": inhibitor.get("kills", 0),
            "inhibitor_first": inhibitor.get("first", 0),
            "rift_herald_kills": rift_herald.get("kills", 0),
            "rift_herald_first": rift_herald.get("first", 0),
            "tower_kills": tower.get("kills", 0),
            "tower_first": tower.get("first", 0),
        }
        rows.append(row)
    return rows

def build_subteam_rows(match_data):

    rows = []
    subteam_ids = set()
    match_id = match_data["metadata"]["matchId"]

    for participant in match_data["info"]["participants"]:
        subteam_id = participant.get("playerSubteamId", None)

        if subteam_id is None:
            continue

        if subteam_id in subteam_ids:
            continue

        rows.append({
            "match_id": match_id,
            "subteam_id": subteam_id,
            "placement": participant["subteamPlacement"]
        })

        subteam_ids.add(subteam_id)

    return rows

def build_runes_columns(perks):
    stat_perks = perks.get("statPerks", {})

    styles = {}
    for style in perks.get("styles", []):
        styles[style["description"]] = style

    primary = styles.get("primaryStyle", {})
    sub = styles.get("subStyle", {})

    row = {
        "primary_style_id": primary.get("style", 0),
        "sub_style_id": sub.get("style", 0),
        "stat_defense": stat_perks.get("defense", 0),
        "stat_flex": stat_perks.get("flex", 0),
        "stat_offense": stat_perks.get("offense", 0),
    }

    for i, selection in enumerate(primary.get("selections", [])):
        row[f"primary_perk_{i}"] = selection.get("perk", 0)

    for i, selection in enumerate(sub.get("selections", [])):
        row[f"sub_perk_{i}"] = selection.get("perk", 0)

    return row

def build_participant_rows(match_data) -> list:
    info = match_data["info"]
    metadata = match_data["metadata"]
    rows = []
    for participant in info["participants"]:
        row = {
            "match_id": metadata.get("matchId", "N/A"),
            "participant_id": participant.get("participantId", 0),
            "team_id": participant.get("teamId", 0),
            "puuid": participant.get("puuid", "N/A"),
            "riot_id_game_name": participant.get("riotIdGameName", 0),
            "riot_id_tagline": participant.get("riotIdTagline", 0),
            "summoner_level": participant.get("summonerLevel", 0),
            "win": participant.get("win", False),
            "champion_id": participant.get("championId", 0),
            "champion_name": participant.get("championName", "N/A"),
            "champion_level": participant.get("champLevel", 0),
            "champion_experience": participant.get("champExperience", 0),
            "team_position": participant.get("teamPosition", "N/A"),
            "individual_position": participant.get("individualPosition", "N/A"),
            "lane": participant.get("lane", "N/A"),
            "player_role": participant.get("role", "N/A"),
            "kills": participant.get("kills", 0),
            "deaths": participant.get("deaths", 0),
            "assists": participant.get("assists", 0),
            "total_minions_killed": participant.get("totalMinionsKilled", 0),
            "neutral_minions_killed": participant.get("neutralMinionsKilled", 0),
            "total_ally_jungle_minions_killed": participant.get("totalAllyJungleMinionsKilled", 0),
            "total_enemy_jungle_minions_killed": participant.get("totalEnemyJungleMinionsKilled", 0),
            "killing_sprees": participant.get("killingSprees", 0),
            "largest_killing_spree": participant.get("largestKillingSpree", 0),
            "largest_multi_kill": participant.get("largestMultiKill", 0),
            "largest_crit_strike": participant.get("largestCriticalStrike", 0),
            "double_kills": participant.get("doubleKills", 0),
            "triple_kills": participant.get("tripleKills", 0),
            "quadra_kills": participant.get("quadraKills", 0),
            "penta_kills": participant.get("pentaKills", 0),
            "unreal_kills": participant.get("unrealKills", 0),
            "longest_time_spent_living": participant.get("longestTimeSpentLiving", 0),
            "total_time_spent_dead": participant.get("totalTimeSpentDead", 0),
            "time_played": participant.get("timePlayed", 0),
            "gold_earned": participant.get("goldEarned", 0),
            "gold_spent": participant.get("goldSpent", 0),
            "item0": participant.get("item0", 0),
            "item1": participant.get("item1", 0),
            "item2": participant.get("item2", 0),
            "item3": participant.get("item3", 0),
            "item4": participant.get("item4", 0),
            "item5": participant.get("item5", 0),
            "item6": participant.get("item6", 0),
            "items_purchased": participant.get("itemsPurchased", 0),
            "total_dmg_dealt": participant.get("totalDamageDealt", 0),
            "magic_dmg_dealt": participant.get("magicDamageDealt", 0),
            "phy_dmg_dealt": participant.get("physicalDamageDealt", 0),
            "true_dmg_dealt": participant.get("trueDamageDealt", 0),
            "total_dmg_dealt_champions": participant.get("totalDamageDealtToChampions", 0),
            "magic_dmg_dealt_champions": participant.get("magicDamageDealtToChampions", 0),
            "phy_dmg_dealt_champions": participant.get("physicalDamageDealtToChampions", 0),
            "true_dmg_dealt_champions": participant.get("trueDamageDealtToChampions", 0),
            "total_dmg_taken": participant.get("totalDamageTaken", 0),
            "magic_dmg_taken": participant.get("magicDamageTaken", 0),
            "phy_dmg_taken": participant.get("physicalDamageTaken", 0),
            "true_dmg_taken": participant.get("trueDamageTaken", 0),
            "self_mitigated_dmg": participant.get("damageSelfMitigated", 0),
            "total_heal": participant.get("totalHeal", 0),
            "total_heals_on_teammates": participant.get("totalHealsOnTeammates", 0),
            "total_dmg_shielded_on_teammates": participant.get("totalDamageShieldedOnTeammates", 0),
            "time_cc_others": participant.get("timeCCingOthers", 0),
            "total_time_cc_dealt": participant.get("totalTimeCCDealt", 0),
            "dmg_dealt_to_buildings": participant.get("damageDealtToBuildings", 0),
            "dmg_dealt_to_epic_monsters": participant.get("damageDealtToEpicMonsters", 0),
            "dmg_dealt_to_objectives": participant.get("damageDealtToObjectives", 0),
            "dmg_dealt_to_turrets": participant.get("damageDealtToTurrets", 0),
            "baron_kills": participant.get("baronKills", 0),
            "dragon_kills": participant.get("dragonKills", 0),
            "turret_kills": participant.get("turretKills", 0),
            "turret_takedowns": participant.get("turretTakedowns", 0),
            "turrets_lost": participant.get("turretsLost", 0),
            "inhibitor_kills": participant.get("inhibitorKills", 0),
            "inhibitor_takedowns": participant.get("inhibitorTakedowns", 0),
            "inhibitors_lost": participant.get("inhibitorsLost", 0),
            "nexus_kills": participant.get("nexusKills", 0),
            "nexus_lost": participant.get("nexusLost", 0),
            "nexus_takedowns": participant.get("nexusTakedowns", 0),
            "objectives_stolen": participant.get("objectivesStolen", 0),
            "objectives_stolen_assists": participant.get("objectivesStolenAssists", 0),
            "first_blood_kill": participant.get("firstBloodKill", False),
            "first_blood_assist": participant.get("firstBloodAssist", False),
            "first_tower_kill": participant.get("firstTowerKill", False),
            "first_tower_assist": participant.get("firstTowerAssist", False),
            "vision_score": participant.get("visionScore", 0),
            "wards_placed": participant.get("wardsPlaced", 0),
            "wards_killed": participant.get("wardsKilled", 0),
            "detector_wards_placed": participant.get("detectorWardsPlaced", 0),
            "sight_wards_bought": participant.get("sightWardsBoughtInGame", 0),
            "vision_wards_bought": participant.get("visionWardsBoughtInGame", 0),
            "spell1_casts": participant.get("spell1Casts", 0),
            "spell2_casts": participant.get("spell2Casts", 0),
            "spell3_casts": participant.get("spell3Casts", 0),
            "spell4_casts": participant.get("spell4Casts", 0),
            "summoner1_id": participant.get("summoner1Id", 0),
            "summoner2_id": participant.get("summoner2Id", 0),
            "summoner1_casts": participant.get("summoner1Casts", 0),
            "summoner2_casts": participant.get("summoner2Casts", 0),
            "all_in_pings": participant.get("allInPings", 0),
            "assist_me_pings": participant.get("assistMePings", 0),
            "basic_pings": participant.get("basicPings", 0),
            "command_pings": participant.get("commandPings", 0),
            "danger_pings": participant.get("dangerPings", 0),
            "enemy_missing_pings": participant.get("enemyMissingPings", 0),
            "enemy_vision_pings": participant.get("enemyVisionPings", 0),
            "get_back_pings": participant.get("getBackPings", 0),
            "hold_pings": participant.get("holdPings", 0),
            "need_vision_pings": participant.get("needVisionPings", 0),
            "omw_pings": participant.get("onMyWayPings", 0),
            "push_pings": participant.get("pushPings", 0),
            "retreat_pings": participant.get("retreatPings", 0),
            "vision_cleared_pings": participant.get("visionClearedPings", 0),
            "game_ended_in_surrender": participant.get("gameEndedInSurrender", False),
            "game_ended_in_early_surrender": participant.get("gameEndedInEarlySurrender", False),
            "was_afk": participant.get("wasAfk", False),

            "player_augment_1": participant.get("playerAugment1", None),
            "player_augment_2": participant.get("playerAugment2", None),
            "player_augment_3": participant.get("playerAugment3", None),
            "player_augment_4": participant.get("playerAugment4", None),
            "player_augment_5": participant.get("playerAugment5", None),
            "player_augment_6": participant.get("playerAugment6", None),

            "challenges": json.dumps(participant.get("challenges", {})),
            "missions": json.dumps(participant.get("missions", {})),

        }
        
        if is_arena_match(match_data["info"]["queueId"]):
            row["subteam_id"] = participant.get("playerSubteamId")
        else:
            row["subteam_id"] = None

        row.update(build_runes_columns(participant["perks"]))
        rows.append(row)
    return rows

def build_match_timeline(timeline_data):
    info = timeline_data["info"]
    metadata = timeline_data["metadata"]

    row = {
        "match_id": metadata.get("matchId", "N/A"),
        "frame_interval": info.get("frameInterval", 0),
        "end_of_game_result": info.get("endOfGameResult", "N/A")
    }
    return row

def build_timeline_frames_events_participants(timeline_data):
    metadata = timeline_data["metadata"]
    frames = timeline_data["info"]["frames"]
    participants = timeline_data["info"]["participants"]

    frame_index = 0
    rows = []
    event_rows = []
    participant_rows = []

    participant_puuids = {}
    for participant in participants:
        participant_id = participant["participantId"]
        puuid = participant["puuid"]
        participant_puuids[participant_id] = puuid

    for frame in frames:

        row = {
            "match_id": metadata.get("matchId", "N/A"),
            "frame_index": frame_index,
            "timestamp_ms": frame.get("timestamp", 0)
        }
        rows.append(row)

        participant_frames = frame["participantFrames"]
        for participant_id, participant in participant_frames.items():

            participant_id = int(participant_id)
            puuid = participant_puuids[participant_id]
            position = participant.get("position", {})

            participant_row = {
                "match_id": metadata.get("matchId", "N/A"),
                "frame_index": frame_index,
                "participant_id": int(participant_id),
                "puuid": puuid,

                "level": participant.get("level"),
                "current_gold": participant.get("currentGold"),
                "total_gold": participant.get("totalGold"),
                "xp": participant.get("xp"),
                "minions_killed": participant.get("minionsKilled"),
                "jungle_minions_killed": participant.get("jungleMinionsKilled"),
                "gold_per_second": participant.get("goldPerSecond"),
                "time_enemy_spent_controlled": participant.get("timeEnemySpentControlled"),

                "position_x": position.get("x"),
                "position_y": position.get("y"),

                "champion_stats": json.dumps(participant.get("championStats", {})),
                "damage_stats": json.dumps(participant.get("damageStats", {}))
            }
        participant_rows.append(participant_row)

        for event in frame["events"]:

            event_data = {}

            for key, value in event.items():
                if key == "type" or key == "timestamp":
                    continue
                event_data[key] = value

            event_row = {
                "match_id": metadata.get("matchId", "N/A"),
                "frame_index": frame_index,
                "timestamp_ms": event["timestamp"],
                "event_type": event["type"],
                "event_data": json.dumps(event_data)
            }   
            event_rows.append(event_row)

        frame_index = frame_index + 1
    return rows, event_rows, participant_rows

def build_ranked_entries(puuid, region, ranked_entries):

    ranked_rows = []
    for entry in ranked_entries:
        row = {
            "puuid": puuid,
            "region": region,
            "queue_type": entry.get("queueType", "N/A"),
            "tier": entry.get("tier", "N/A"),
            "division": entry.get("rank", "N/A"),
            "league_points": entry.get("leaguePoints", 0),
            "wins": entry.get("wins", 0),
            "losses": entry.get("losses", 0),
            "veteran": entry.get("veteran", False),
            "inactive": entry.get("inactive", False),
            "fresh_blood": entry.get("freshBlood", False),
            "hot_streak": entry.get("hotStreak", False),
        }
        ranked_rows.append(row)

    return ranked_rows

def build_champion_mastery_entries(server, puuid, mastery_data):
    mastery_rows = []
    for entry in mastery_data:
        row = {
            "puuid": puuid,
            "region": server,
            "champion_id": entry.get("championId", 0),
            "champion_level": entry.get("championLevel", 0),
            "champion_points": entry.get("championPoints", 0),
            "last_play_time": entry.get("lastPlayTime", 0),
            "champion_points_since_level": entry.get("championPointsSinceLastLevel", 0),
            "champion_points_until_level": entry.get("championPointsUntilNextLevel", 0),
            "mark_required": entry.get("markRequiredForNextLevel", 0),
            "tokens_earned": entry.get("tokensEarned", 0),
            "champion_season_milestone": entry.get("championSeasonMilestone", 0),
            "milestone_grades": json.dumps(entry.get("milestoneGrades", [])),
            "next_season_milestone": json.dumps(entry.get("nextSeasonMilestone", {}))
        }
        mastery_rows.append(row)

    return mastery_rows