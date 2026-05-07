from langgraph.graph import END, StateGraph

from app.nodes.draft import draft_node
from app.nodes.outline import outline_node
from app.nodes.rewrite import rewrite_node
from app.nodes.story_eval import story_eval_node
from app.state.graph_state import ScreenplayState


def _route_after_eval(state: ScreenplayState) -> str:
    if state.get("eval_result", {}).get("should_rewrite", False):
        return "rewrite"
    return END


def build_graph():
    builder = StateGraph(ScreenplayState)

    builder.add_node("outline", outline_node)
    builder.add_node("draft", draft_node)
    builder.add_node("story_eval", story_eval_node)
    builder.add_node("rewrite", rewrite_node)

    builder.set_entry_point("outline")
    builder.add_edge("outline", "draft")
    builder.add_edge("draft", "story_eval")
    builder.add_conditional_edges(
        "story_eval",
        _route_after_eval,
        {"rewrite": "rewrite", END: END},
    )
    builder.add_edge("rewrite", "story_eval")

    return builder.compile()
