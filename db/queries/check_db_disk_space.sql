SELECT
    table_name,
    table_rows,
    data_mb,
    index_mb,
    total_mb,
    total_gb
FROM (
    SELECT
        TABLE_NAME AS table_name,
        TABLE_ROWS AS table_rows,
        ROUND(DATA_LENGTH / 1024 / 1024, 2) AS data_mb,
        ROUND(INDEX_LENGTH / 1024 / 1024, 2) AS index_mb,
        ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) AS total_mb,
        ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024 / 1024, 2) AS total_gb,
        0 AS sort_order
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_TYPE = 'BASE TABLE'

    UNION ALL

    SELECT
        'TOTAL' AS table_name,
        COALESCE(SUM(TABLE_ROWS), 0) AS table_rows,
        ROUND(COALESCE(SUM(DATA_LENGTH), 0) / 1024 / 1024, 2) AS data_mb,
        ROUND(COALESCE(SUM(INDEX_LENGTH), 0) / 1024 / 1024, 2) AS index_mb,
        ROUND(COALESCE(SUM(DATA_LENGTH + INDEX_LENGTH), 0) / 1024 / 1024, 2) AS total_mb,
        ROUND(COALESCE(SUM(DATA_LENGTH + INDEX_LENGTH), 0) / 1024 / 1024 / 1024, 2) AS total_gb,
        1 AS sort_order
    FROM information_schema.TABLES
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_TYPE = 'BASE TABLE'
) AS db_stats
ORDER BY sort_order, total_mb DESC;
