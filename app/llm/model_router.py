from app.config import TAGGER_MODEL, VERIFIER_MODEL, WRITER_MODEL
from app.llm.ollama_client import get_client


def get_writer():
    return get_client(WRITER_MODEL)


def get_tagger():
    return get_client(TAGGER_MODEL)


def get_verifier():
    return get_client(VERIFIER_MODEL)
