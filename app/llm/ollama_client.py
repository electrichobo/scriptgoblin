import urllib.request

from langchain_ollama import ChatOllama

from app.config import OLLAMA_BASE_URL


def get_client(model: str) -> ChatOllama:
    return ChatOllama(model=model, base_url=OLLAMA_BASE_URL)


def check_ollama() -> dict:
    try:
        urllib.request.urlopen(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)
        return {"reachable": True, "url": OLLAMA_BASE_URL}
    except Exception:
        return {"reachable": False, "url": OLLAMA_BASE_URL}
