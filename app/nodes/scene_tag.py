from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage

from app.config import TAGGER_MODEL
from app.llm.model_router import get_tagger
from app.llm.structured_output import parse_structured
from app.services import run_logger
from app.state.graph_state import ScreenplayState
from app.state.models import SceneTags

_PROMPTS = Path(__file__).resolve().parents[1] / "prompts"


def scene_tag_node(state: ScreenplayState) -> dict:
    brief = state["brief"]
    outline = state["outline"]
    draft = state["draft"]

    scenes = outline.get("scenes", [])
    scene_list = "\n".join(
        f"Scene {s['number']}: {s['location']} — {s['time_of_day']}"
        for s in scenes
    )

    system = (_PROMPTS / "scene_tagger.md").read_text()
    human = (
        f"Title: {brief['title']}\n"
        f"Total scenes: {len(scenes)}\n\n"
        f"Scene index:\n{scene_list}\n\n"
        f"Full screenplay:\n{draft}"
    )

    slug = state["slug"]
    run_logger.log(slug, f"[tagger] tagging {len(scenes)} scenes...", phase="tagger", model=TAGGER_MODEL)
    llm = get_tagger()
    result = parse_structured(
        llm,
        SceneTags,
        [SystemMessage(content=system), HumanMessage(content=human)],
    )
    run_logger.log(slug, f"[tagger] done — {len(result.scenes)} scenes tagged")

    return {"scene_tags": result.model_dump()}
