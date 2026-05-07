from langgraph.graph import END, StateGraph

from app.nodes.draft import draft_node
from app.nodes.outline import outline_node
from app.state.graph_state import ScreenplayState


def build_graph():
    builder = StateGraph(ScreenplayState)
    builder.add_node("outline", outline_node)
    builder.add_node("draft", draft_node)
    builder.set_entry_point("outline")
    builder.add_edge("outline", "draft")
    builder.add_edge("draft", END)
    return builder.compile()
