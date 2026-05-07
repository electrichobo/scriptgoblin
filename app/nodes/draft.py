from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage

from app.llm.model_router import get_writer
from app.state.graph_state import ScreenplayState

_PROMPTS = Path(__file__).resolve().parents[1] / "prompts"


def _outline_to_text(outline: dict) -> str:
    scenes = outline.get("scenes", [])
    lines = []
    for s in scenes:
        lines.append(f"SCENE {s['number']}: {s['location']} — {s['time_of_day']}")
        lines.append(f"  Purpose:       {s['purpose']}")
        lines.append(f"  Objective:     {s['objective']}")
        lines.append(f"  Turning Point: {s['turning_point']}")
        for beat in s.get("beats", []):
            lines.append(f"  - {beat}")
        lines.append("")
    return "\n".join(lines)


def draft_node(state: ScreenplayState) -> dict:
    brief = state["brief"]
    runtime = brief.get("target_runtime_minutes", 100)
    format_label = brief.get("format_label", "Screenplay")
    outline_text = _outline_to_text(state["outline"])

    system = (_PROMPTS / "story_writer.md").read_text()
    human = (
        "Write a complete screenplay draft from the outline below.\n\n"
        f"Title: {brief['title']}\n"
        f"Format: {format_label}\n"
        f"Target runtime: {runtime} minutes (~{runtime} pages)\n"
        f"Genre: {brief['genre']}\n"
        f"Theme: {brief['theme']}\n"
        f"Tone: {brief['tone']}\n\n"
        f"Outline:\n{outline_text}\n"
        f"Write every scene in the outline. "
        f"Keep total length appropriate for a {runtime}-minute {format_label.lower()}. "
        "Do not add a preamble or closing remarks — output screenplay text only."
    )

    story_notes = brief.get("story_notes", "").strip()
    if story_notes:
        human += f"\n\nAdditional story notes:\n{story_notes}"

    production_notes = state.get("human_notes", {}).get("overall_notes", "").strip()
    if production_notes:
        human += f"\n\nProduction notes from previous draft — apply these throughout:\n{production_notes}"

    print(f"[draft] generating for '{brief['title']}' ({runtime} min, {len(state['outline'].get('scenes', []))} scenes)...")
    llm = get_writer()
    response = llm.invoke([SystemMessage(content=system), HumanMessage(content=human)])
    print(f"[draft] done — {len(response.content)} chars")
    return {
        "draft": response.content,
        "current_stage": "drafted",
        "story_loops": state.get("story_loops", 0) + 1,
    }
