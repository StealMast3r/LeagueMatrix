INSERT INTO timeline_events (
    match_id,
    frame_index,
    timestamp_ms,
    event_type,
    event_data
)
VALUES (
    %(match_id)s,
    %(frame_index)s,
    %(timestamp_ms)s,
    %(event_type)s,
    %(event_data)s
);