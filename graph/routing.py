from graph.state import VRAGState


def route_after_prosecutor(state: VRAGState):

    investigation_request = (
        state["prosecutor_output"].investigation_request
    )

    if investigation_request is not None:
        return "investigation_node"

    return "judge_node"