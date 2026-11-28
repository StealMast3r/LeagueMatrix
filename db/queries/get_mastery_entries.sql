
SELECT
    puuid,
    region,
    champion_id,
    champion_level,
    champion_points,
    last_play_time,
    champion_points_since_level,
    champion_points_until_level,
    mark_required,
    tokens_earned,
    champion_season_milestone,
    milestone_grades,
    next_season_milestone,
    last_updated
FROM champion_mastery
WHERE puuid = %(puuid)s AND region = %(region)s
ORDER BY champion_points DESC;
