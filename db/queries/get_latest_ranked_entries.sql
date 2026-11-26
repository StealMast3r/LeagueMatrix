SELECT *
FROM rank_snapshots
WHERE puuid = %(puuid)s
AND region = %(region)s
AND captured_at = (
    SELECT MAX(captured_at)
    FROM rank_snapshots
    WHERE puuid = %(puuid)s
    AND region = %(region)s
);