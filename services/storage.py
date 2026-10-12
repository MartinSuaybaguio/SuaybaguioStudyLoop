import json
import threading
from pathlib import Path


class Storage:
    def __init__(self, path=None):
        self.path = Path(path or Path(__file__).resolve().parent.parent / "data" / "studyloop.json")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _read(self) -> dict:
        if not self.path.exists():
            return {}
        try:
            return json.loads(self.path.read_text("utf-8"))
        except json.JSONDecodeError:
            return {}

    def exists(self, name: str) -> bool:
        return name.strip().lower() in self._read()

    def load(self, name: str):
        return self._read().get(name.strip().lower())

    def save(self, name: str, record: dict) -> None:
        with self._lock:
            data = self._read()
            data[name.strip().lower()] = record
            self.path.write_text(json.dumps(data, indent=2), "utf-8")
