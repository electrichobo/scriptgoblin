from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage

from app.config import WRITER_MODEL
from app.llm.model_router import get_writer
from app.services import run_logger
from app.state.graph_state import ScreenplayState

_PROMPTS = Path(__file__).resolve().parents[1] / "prompts"


def rewrite_node(state: ScreenplayState) -> dict:
    brief = state["brief"]
    draft = state["draft"]
    eval_result = state.get("eval_result", {})
    loops = state.get("story_loops", 0)

    feedback = eval_result.get("feedback", "")
    notes = eval_result.get("notes", [])

    system = (_PROMPTS / "story_writer.md").read_text()
    human = (
        "Revise the screenplay draft based on the editorial notes below.\n\n"
        f"Title: {brief['title']}\n"
        f"Format: {brief.get('format_label', 'Screenplay')}\n"
        f"Target runtime: {brief.get('target_runtime_minutes', 100)} minutes\n\n"
        f"Editorial feedback:\n{feedback}\n\n"
        "Specific notes to address:\n"
        + "\n".join(f"- {n}" for n in notes)
        + "\n\nCurrent draft:\n"
        + draft
        + "\n\nRewrite the full screenplay addressing all notes. "
        "Output screenplay text only — no commentary."
    )

    production_notes = state.get("human_notes", {}).get("overall_notes", "").strip()
    if production_notes:
        human += f"\n\nProduction notes (also apply these):\n{production_notes}"

    locked_scenes = [
        sn["scene_number"]
        for sn in state.get("human_notes", {}).get("scene_notes", [])
        if sn.get("locked", False)
    ]
    if locked_scenes:
        nums = ", ".join(f"SCENE {n}" for n in sorted(locked_scenes))
        human += (
            f"\n\nLOCKED SCENES — {nums}: these scenes are approved and must be reproduced "
            "verbatim from the current draft. Do not alter a single word."
        )

    slug = state["slug"]
    run_logger.log(slug, f"[rewrite] rewriting draft (story_loops={loops})...", phase="rewrite", model=WRITER_MODEL)
    llm = get_writer()
    response = llm.invoke([SystemMessage(content=system), HumanMessage(content=human)])
    run_logger.log(slug, f"[rewrite] done — {len(response.content)} chars")

    return {
        "draft": response.content,
        "current_stage": "rewritten",
        "story_loops": loops + 1,
    }
