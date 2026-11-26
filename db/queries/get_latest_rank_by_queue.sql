SELECT *
FROM rank_snapshots
WHERE puuid = %(puuid)s
AND region = %(region)s
AND queue_type = %(queue_type)s
ORDER BY captured_at DESC
LIMIT 1;