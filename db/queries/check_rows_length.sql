USE lolmatrixdb;

SELECT 'match_timelines' AS table_name, COUNT(*) AS total_rows
FROM match_timelines

UNION ALL

SELECT 'matches', COUNT(*) FROM matches

UNION ALL

SELECT 'participant_frames', COUNT(*) FROM participant_frames

UNION ALL

SELECT 'participants', COUNT(*) FROM participants

UNION ALL

SELECT 'rank_snapshots', COUNT(*) FROM rank_snapshots

UNION ALL

SELECT 'subteams', COUNT(*) FROM subteams

UNION ALL

SELECT 'summoners', COUNT(*) FROM summoners

UNION ALL

SELECT 'teams', COUNT(*) FROM teams

UNION ALL

SELECT 'timeline_events', COUNT(*) FROM timeline_events

UNION ALL

SELECT 'timeline_frames', COUNT(*) FROM timeline_frames;