from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage

from app.config import HEAVY_MODEL
from app.llm.model_router import get_heavy
from app.llm.structured_output import parse_structured
from app.services import run_logger
from app.state.graph_state import ScreenplayState
from app.state.models import StoryEval

_PROMPTS = Path(__file__).resolve().parents[1] / "prompts"


def story_eval_node(state: ScreenplayState) -> dict:
    brief = state["brief"]
    draft = state["draft"]
    loops = state.get("story_loops", 0)

    system = (_PROMPTS / "story_eval.md").read_text()
    human = (
        f"Evaluate the following screenplay draft.\n\n"
        f"Title: {brief['title']}\n"
        f"Format: {brief.get('format_label', 'Screenplay')}\n"
        f"Target runtime: {brief.get('target_runtime_minutes', 100)} minutes\n"
        f"Theme: {brief['theme']}\n\n"
        f"Draft:\n{draft}"
    )

    slug = state["slug"]
    run_logger.log(slug, f"[eval] evaluating draft (story_loops={loops})...", phase="story_eval", model=HEAVY_MODEL)
    llm = get_heavy()
    result = parse_structured(
        llm,
        StoryEval,
        [SystemMessage(content=system), HumanMessage(content=human)],
    )
    best = max(result.score, state.get("best_score", 0))
    run_logger.log(slug, f"[eval] score={result.score}, best={best}, should_rewrite={result.should_rewrite}")

    return {
        "eval_result": result.model_dump(),
        "best_score": best,
        "current_stage": "evaluated",
    }
