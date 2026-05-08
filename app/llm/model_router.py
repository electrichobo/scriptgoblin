from app.config import HEAVY_MODEL, HELPER_MODEL, TAGGER_MODEL, VERIFIER_MODEL, WRITER_MODEL
from app.llm.ollama_client import get_client

# A feature screenplay is ~12k–20k tokens; allow room for system prompt + output.
_SCREENPLAY_CTX = 32768


def get_writer():
    return get_client(WRITER_MODEL, num_ctx=_SCREENPLAY_CTX)


def get_tagger():
    return get_client(TAGGER_MODEL)


def get_verifier():
    return get_client(VERIFIER_MODEL)


def get_heavy():
    return get_client(HEAVY_MODEL, num_ctx=_SCREENPLAY_CTX)


def get_helper():
    return get_client(HELPER_MODEL)
