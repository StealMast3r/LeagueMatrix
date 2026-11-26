INSERT INTO timeline_frames (
    match_id,
    frame_index,
    timestamp_ms
)
VALUES (
    %(match_id)s,
    %(frame_index)s,
    %(timestamp_ms)s
);