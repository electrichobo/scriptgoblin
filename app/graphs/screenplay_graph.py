from langgraph.graph import END, START, StateGraph

from app.nodes.draft import draft_node
from app.nodes.outline import outline_node
from app.nodes.outline_sync import outline_sync_node
from app.nodes.rewrite import rewrite_node
from app.nodes.scene_tag import scene_tag_node
from app.nodes.story_eval import story_eval_node
from app.state.graph_state import ScreenplayState


def _route_start(state: ScreenplayState) -> str:
    has_draft = bool(state.get("draft", "").strip())
    notes = state.get("human_notes", {})
    has_notes = bool(
        notes.get("overall_notes", "").strip() or notes.get("scene_notes", [])
    )
    if has_draft and has_notes:
        return "rewrite"
    return "outline"


_MAX_STORY_LOOPS = 3


def _route_after_eval(state: ScreenplayState) -> str:
    eval_result = state.get("eval_result", {})
    score = eval_result.get("score", 10)
    loops = state.get("story_loops", 0)
    if score < 8 and loops < _MAX_STORY_LOOPS:
        return "rewrite"
    return END


def build_graph():
    builder = StateGraph(ScreenplayState)

    builder.add_node("outline", outline_node)
    builder.add_node("draft", draft_node)
    builder.add_node("tagger", scene_tag_node)
    builder.add_node("story_eval", story_eval_node)
    builder.add_node("rewrite", rewrite_node)
    builder.add_node("outline_sync", outline_sync_node)

    builder.add_conditional_edges(START, _route_start, {"outline": "outline", "rewrite": "rewrite"})
    builder.add_edge("outline", "draft")
    builder.add_edge("draft", "tagger")
    builder.add_edge("tagger", "story_eval")
    builder.add_conditional_edges(
        "story_eval",
        _route_after_eval,
        {"rewrite": "rewrite", END: END},
    )
    builder.add_edge("rewrite", "outline_sync")
    builder.add_edge("outline_sync", "tagger")

    return builder.compile()
