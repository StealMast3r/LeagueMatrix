SELECT
    m.total_matches,
    s.total_summoners,
    p.total_participant_rows,
    p.unique_players_in_matches,
    p.unique_champions_played,
    m.patches_recorded,
    m.avg_game_duration_seconds,
    p.avg_kills,
    p.avg_deaths,
    p.avg_assists,
    p.avg_kda,
    p.avg_gold_earned,
    p.avg_champion_damage,
    p.avg_vision_score,
    p.participant_win_rate_percent,
    p.total_penta_kills,
    t.total_team_rows,
    t.total_barons_killed,
    t.total_dragons_killed,
    t.total_towers_killed,
    st.total_arena_subteams,
    mt.matches_with_timeline,
    ROUND(mt.matches_with_timeline * 100.0 / NULLIF(m.total_matches, 0), 1)
        AS timeline_coverage_percent,
    tf.total_timeline_frames,
    te.total_timeline_events,
    pf.total_participant_frames,
    rs.total_rank_snapshots,
    rs.latest_rank_snapshot_at,
    s.latest_summoner_update_at
FROM (
    SELECT
        COUNT(*) AS total_matches,
        COUNT(DISTINCT patch) AS patches_recorded,
        ROUND(AVG(game_duration)) AS avg_game_duration_seconds
    FROM matches
) AS m
CROSS JOIN (
    SELECT
        COUNT(*) AS total_participant_rows,
        COUNT(DISTINCT puuid) AS unique_players_in_matches,
        COUNT(DISTINCT champion_name) AS unique_champions_played,
        ROUND(AVG(kills), 2) AS avg_kills,
        ROUND(AVG(deaths), 2) AS avg_deaths,
        ROUND(AVG(assists), 2) AS avg_assists,
        ROUND(AVG((kills + assists) / GREATEST(deaths, 1)), 2) AS avg_kda,
        ROUND(AVG(gold_earned)) AS avg_gold_earned,
        ROUND(AVG(total_dmg_dealt_champions)) AS avg_champion_damage,
        ROUND(AVG(vision_score), 2) AS avg_vision_score,
        ROUND(AVG(win) * 100, 1) AS participant_win_rate_percent,
        COALESCE(SUM(penta_kills), 0) AS total_penta_kills
    FROM participants
) AS p
CROSS JOIN (
    SELECT
        COUNT(*) AS total_summoners,
        MAX(last_updated) AS latest_summoner_update_at
    FROM summoners
) AS s
CROSS JOIN (
    SELECT
        COUNT(*) AS total_team_rows,
        COALESCE(SUM(baron_kills), 0) AS total_barons_killed,
        COALESCE(SUM(dragon_kills), 0) AS total_dragons_killed,
        COALESCE(SUM(tower_kills), 0) AS total_towers_killed
    FROM teams
) AS t
CROSS JOIN (
    SELECT COUNT(*) AS total_arena_subteams
    FROM subteams
) AS st
CROSS JOIN (
    SELECT COUNT(*) AS matches_with_timeline
    FROM match_timelines
) AS mt
CROSS JOIN (
    SELECT COUNT(*) AS total_timeline_frames
    FROM timeline_frames
) AS tf
CROSS JOIN (
    SELECT COUNT(*) AS total_timeline_events
    FROM timeline_events
) AS te
CROSS JOIN (
    SELECT COUNT(*) AS total_participant_frames
    FROM participant_frames
) AS pf
CROSS JOIN (
    SELECT
        COUNT(*) AS total_rank_snapshots,
        MAX(captured_at) AS latest_rank_snapshot_at
    FROM rank_snapshots
) AS rs;