from app.config import HEAVY_MODEL, HELPER_MODEL, TAGGER_MODEL, VERIFIER_MODEL, WRITER_MODEL
from app.llm.ollama_client import get_client


def get_writer():
    return get_client(WRITER_MODEL)


def get_tagger():
    return get_client(TAGGER_MODEL)


def get_verifier():
    return get_client(VERIFIER_MODEL)


def get_heavy():
    return get_client(HEAVY_MODEL)


def get_helper():
    return get_client(HELPER_MODEL)
