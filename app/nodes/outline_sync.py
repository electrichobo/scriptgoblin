from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage

from app.config import VERIFIER_MODEL
from app.llm.model_router import get_verifier
from app.llm.structured_output import parse_structured
from app.services import run_logger
from app.state.graph_state import ScreenplayState
from app.state.models import ScreenplayOutline

_PROMPTS = Path(__file__).resolve().parents[1] / "prompts"


def outline_sync_node(state: ScreenplayState) -> dict:
    brief = state["brief"]
    draft = state["draft"]

    system = (_PROMPTS / "outline_sync.md").read_text()
    human = (
        f"Title: {brief['title']}\n\n"
        f"Extract the scene structure from this screenplay:\n\n{draft}"
    )

    slug = state["slug"]
    run_logger.log(slug, "[outline_sync] extracting outline from rewritten draft...", phase="outline_sync", model=VERIFIER_MODEL)
    llm = get_verifier()
    result = parse_structured(
        llm,
        ScreenplayOutline,
        [SystemMessage(content=system), HumanMessage(content=human)],
    )
    run_logger.log(slug, f"[outline_sync] done — {len(result.scenes)} scenes")

    return {"outline": result.model_dump()}
