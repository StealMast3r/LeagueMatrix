INSERT INTO champion_mastery (
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
    next_season_milestone
)
VALUES (
    %(puuid)s,
    %(region)s,
    %(champion_id)s,
    %(champion_level)s,
    %(champion_points)s,
    %(last_play_time)s,
    %(champion_points_since_level)s,
    %(champion_points_until_level)s,
    %(mark_required)s,
    %(tokens_earned)s,
    %(champion_season_milestone)s,
    %(milestone_grades)s,
    %(next_season_milestone)s
)
ON DUPLICATE KEY UPDATE
    champion_level = VALUES(champion_level),
    champion_points = VALUES(champion_points),
    last_play_time = VALUES(last_play_time),
    champion_points_since_level = VALUES(champion_points_since_level),
    champion_points_until_level = VALUES(champion_points_until_level),
    mark_required = VALUES(mark_required),
    tokens_earned = VALUES(tokens_earned),
    champion_season_milestone = VALUES(champion_season_milestone),
    milestone_grades = VALUES(milestone_grades),
    next_season_milestone = VALUES(next_season_milestone),
    last_updated = CURRENT_TIMESTAMP;