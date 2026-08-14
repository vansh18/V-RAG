from graph.state import VRAGState
from langgraph.graph import StateGraph, START, END
from graph.nodes import responder_node, prosecutor_node, investigation_node
from graph.routing import route_after_prosecutor


graph = StateGraph(VRAGState)

graph.add_node("responder_node", responder_node)
graph.add_node("prosecutor_node", prosecutor_node)
graph.add_node("investigation_node", investigation_node)

graph.add_edge(START, "responder_node")
graph.add_edge("responder_node", "prosecutor_node")
graph.add_conditional_edges(
    "prosecutor_node",
    route_after_prosecutor,
    {
        "investigation_node": "investigation_node",
        "judge_node": "judge_node",
    }
)
