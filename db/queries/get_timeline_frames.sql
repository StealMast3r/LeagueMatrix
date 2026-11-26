SELECT *
FROM timeline_frames
WHERE match_id = %(match_id)s
ORDER BY frame_index;