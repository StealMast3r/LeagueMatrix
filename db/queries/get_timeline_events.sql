SELECT *
FROM timeline_events
WHERE match_id = %(match_id)s
ORDER BY timestamp_ms;