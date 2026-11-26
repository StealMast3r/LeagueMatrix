INSERT INTO summoners (
    puuid,
    summoner_name,
    tag_line,
    region,
    profile_icon_id,
    summoner_level,
    revision_date
)
VALUES (
    %(puuid)s,
    %(summoner_name)s,
    %(tag_line)s,
    %(region)s,
    %(profile_icon_id)s,
    %(summoner_level)s,
    %(revision_date)s
)
ON DUPLICATE KEY UPDATE
    summoner_name   = VALUES(summoner_name),
    tag_line        = VALUES(tag_line),
    profile_icon_id = VALUES(profile_icon_id),
    summoner_level  = VALUES(summoner_level),
    revision_date   = VALUES(revision_date),
    last_updated    = CURRENT_TIMESTAMP;