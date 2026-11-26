INSERT INTO match_timelines (
    match_id,
    frame_interval,
    end_of_game_result
)
VALUES (
    %(match_id)s,
    %(frame_interval)s,
    %(end_of_game_result)s
);