import json
import threading
from datetime import datetime, timezone
from pathlib import Path

_lock = threading.Lock()
_BASE = Path(__file__).resolve().parents[2] / "projects"


def _path(slug: str) -> Path:
    return _BASE / slug / "run_log.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write(slug: str, data: dict):
    _path(slug).write_text(json.dumps(data))


def start(slug: str):
    now = _now()
    with _lock:
        _write(slug, {
            "status": "running",
            "phase": "starting",
            "model": None,
            "run_started_at": now,
            "phase_started_at": now,
            "log": [],
        })


def log(slug: str, message: str, phase: str | None = None, model: str | None = None):
    with _lock:
        p = _path(slug)
        data = json.loads(p.read_text()) if p.exists() else {"status": "running", "log": []}
        now = _now()
        if phase is not None:
            data["phase"] = phase
            data["phase_started_at"] = now
        if model is not None:
            data["model"] = model
        data["log"] = (data.get("log", []) + [message])[-150:]
        p.write_text(json.dumps(data))
    print(message)


def done(slug: str):
    with _lock:
        p = _path(slug)
        data = json.loads(p.read_text()) if p.exists() else {}
        data["status"] = "idle"
        data["phase"] = "complete"
        p.write_text(json.dumps(data))


def error(slug: str, message: str):
    with _lock:
        p = _path(slug)
        data = json.loads(p.read_text()) if p.exists() else {"log": []}
        data["status"] = "error"
        data["phase"] = "error"
        data["log"] = (data.get("log", []) + [f"ERROR: {message}"])[-150:]
        p.write_text(json.dumps(data))
    print(f"[ERROR] {message}")


def get_status(slug: str) -> dict:
    p = _path(slug)
    if p.exists():
        return json.loads(p.read_text())
    # Fallback: if run_log.json was never written (race/write failure),
    # check run_state.json so we don't falsely return idle mid-run.
    run_state_path = _BASE / slug / "run_state.json"
    if run_state_path.exists():
        state = json.loads(run_state_path.read_text())
        if state.get("status") == "running":
            return {"status": "running", "phase": "starting", "model": None,
                    "phase_started_at": None, "log": []}
    return {"status": "idle", "phase": None, "model": None, "log": []}
