from collections import defaultdict, deque
from threading import Lock
from time import monotonic


_requests: dict[str, deque[float]] = defaultdict(deque)
_lock = Lock()


def allow_request(key: str, limit: int, window_seconds: int = 60) -> tuple[bool, int]:
    now = monotonic()
    with _lock:
        timestamps = _requests[key]
        while timestamps and now - timestamps[0] >= window_seconds:
            timestamps.popleft()
        if len(timestamps) >= limit:
            retry_after = max(1, int(window_seconds - (now - timestamps[0])))
            return False, retry_after
        timestamps.append(now)
        return True, 0