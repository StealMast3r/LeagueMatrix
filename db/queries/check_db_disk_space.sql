USE lolmatrixdb;

ANALYZE TABLE match_timelines;
ANALYZE TABLE matches;
ANALYZE TABLE participant_frames;
ANALYZE TABLE participants;
ANALYZE TABLE rank_snapshots;
ANALYZE TABLE subteams;
ANALYZE TABLE summoners;
ANALYZE TABLE teams;
ANALYZE TABLE timeline_events;
ANALYZE TABLE timeline_frames;

SELECT
    TABLE_NAME,
    TABLE_ROWS,
    data_mb,
    index_mb,
    total_mb,
    total_gb
FROM (
    SELECT
        TABLE_NAME,
        FORMAT(TABLE_ROWS, 0) AS TABLE_ROWS,
        ROUND(DATA_LENGTH / 1024 / 1024, 2) AS data_mb,
        ROUND(INDEX_LENGTH / 1024 / 1024, 2) AS index_mb,
        ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) AS total_mb,
        ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024 / 1024, 2) AS total_gb,
        0 AS sort_order
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = 'lolmatrixdb'

    UNION ALL

    SELECT
        'TOTAL',
        FORMAT(SUM(TABLE_ROWS), 0),
        ROUND(SUM(DATA_LENGTH) / 1024 / 1024, 2),
        ROUND(SUM(INDEX_LENGTH) / 1024 / 1024, 2),
        ROUND(SUM(DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2),
        ROUND(SUM(DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024 / 1024, 2),
        1
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = 'lolmatrixdb'
) AS db_stats
ORDER BY sort_order, total_mb DESC;