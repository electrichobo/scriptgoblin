from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage

from app.config import WRITER_MODEL
from app.llm.model_router import get_writer
from app.llm.structured_output import parse_structured
from app.services import run_logger
from app.state.graph_state import ScreenplayState
from app.state.models import ScreenplayOutline

_PROMPTS = Path(__file__).resolve().parents[1] / "prompts"


def outline_node(state: ScreenplayState) -> dict:
    brief = state["brief"]
    runtime = brief.get("target_runtime_minutes", 100)
    format_label = brief.get("format_label", "Screenplay")

    system = (_PROMPTS / "story_writer.md").read_text()
    human = (
        "Create a scene-by-scene outline for the following screenplay.\n\n"
        f"Title: {brief['title']}\n"
        f"Format: {format_label}\n"
        f"Target runtime: {runtime} minutes (~{runtime} pages)\n"
        f"Genre: {brief['genre']}\n"
        f"Theme: {brief['theme']}\n"
        f"Tone: {brief['tone']}\n\n"
        "For each scene provide:\n"
        "  number: scene number (integer)\n"
        "  location: INT./EXT. LOCATION (all caps)\n"
        "  time_of_day: DAY, NIGHT, DUSK, DAWN, etc.\n"
        "  purpose: what this scene accomplishes in the story (one sentence)\n"
        "  objective: what the POV character wants in this scene (one sentence)\n"
        "  turning_point: how the scene ends differently than it began (one sentence)\n"
        "  beats: 2-4 key story beats within the scene (short phrases)\n\n"
        f"Scale scene count to fit a {runtime}-minute runtime. "
        "Return structured output only — no prose outside the schema."
    )

    story_notes = brief.get("story_notes", "").strip()
    if story_notes:
        human += f"\n\nAdditional story notes (characters, existing story elements, specific requirements):\n{story_notes}"

    production_notes = state.get("human_notes", {}).get("overall_notes", "").strip()
    if production_notes:
        human += f"\n\nProduction notes from previous draft — incorporate these into the new outline:\n{production_notes}"

    slug = state["slug"]
    run_logger.log(slug, f"[outline] generating for '{brief['title']}' ({runtime} min)...", phase="outline", model=WRITER_MODEL)
    llm = get_writer()
    result = parse_structured(
        llm,
        ScreenplayOutline,
        [SystemMessage(content=system), HumanMessage(content=human)],
    )
    run_logger.log(slug, f"[outline] done — {len(result.scenes)} scenes")
    return {"outline": result.model_dump(), "current_stage": "outlined"}
