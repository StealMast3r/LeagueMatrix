SELECT puuid, summoner_name, tag_line, region, profile_icon_id, summoner_level, revision_date, last_updated
FROM summoners
WHERE summoner_name = %(summoner_name)s AND tag_line = %(tag_line)s AND region = %(region)s