from dotenv import load_dotenv
import os

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
WRITER_MODEL = os.getenv("WRITER_MODEL", "fluffy/l3-8b-stheno-v3.2:latest")
TAGGER_MODEL = os.getenv("TAGGER_MODEL", "gemma4:26b")
VERIFIER_MODEL = os.getenv("VERIFIER_MODEL", "qwen3.6:35b")