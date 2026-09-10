from threading import Lock


class Metrics:
    def __init__(self):
        self._lock = Lock()
        self._values: dict[str, float] = {}

    def increment(self, name: str, amount: float = 1) -> None:
        with self._lock:
            self._values[name] = self._values.get(name, 0) + amount

    def observe(self, name: str, value: float) -> None:
        with self._lock:
            self._values[name] = self._values.get(name, 0) + value

    def snapshot(self) -> dict[str, float]:
        with self._lock:
            return dict(self._values)


metrics = Metrics()