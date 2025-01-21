from time import time

times = {}

def antispam(user: int, limit: int) -> bool | int:
    assert isinstance(user, int) and isinstance(
        limit, int
    ), "Both arguments must be integers"

    now, last = time(), times.get(user, 0)
    diff = now - last

    if diff < limit:
        return int(limit - diff)

    times[user] = now
    return False
