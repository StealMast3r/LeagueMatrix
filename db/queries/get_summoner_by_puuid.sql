SELECT puuid, summoner_name, tag_line, region, profile_icon_id, summoner_level, revision_date, last_updated
FROM summoners
WHERE puuid = %(puuid)s AND region = %(region)s