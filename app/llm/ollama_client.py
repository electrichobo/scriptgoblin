import json
import time
import urllib.request

from langchain_ollama import ChatOllama

from app.config import OLLAMA_BASE_URL

_last_model: str | None = None


def _ps_loaded_models() -> list[str]:
    try:
        resp = urllib.request.urlopen(f"{OLLAMA_BASE_URL}/api/ps", timeout=5)
        data = json.loads(resp.read())
        return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []


def _wait_for_unload(model: str, timeout: int = 90) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if model not in _ps_loaded_models():
            return
        time.sleep(2)
    # timed out — proceed anyway


def get_client(model: str) -> ChatOllama:
    global _last_model
    if _last_model and _last_model != model:
        _wait_for_unload(_last_model)
        time.sleep(30)
    _last_model = model
    return ChatOllama(model=model, base_url=OLLAMA_BASE_URL, keep_alive=0)


def check_ollama() -> dict:
    try:
        urllib.request.urlopen(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)
        return {"reachable": True, "url": OLLAMA_BASE_URL}
    except Exception:
        return {"reachable": False, "url": OLLAMA_BASE_URL}
