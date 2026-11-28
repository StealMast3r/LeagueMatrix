# from riot.constants import is_arena_queue

ARENA_QUEUE_IDS = frozenset({1700, 1710, 1740, 1750})

def is_arena_queue(queue_id: int) -> bool:
    return queue_id in ARENA_QUEUE_IDS