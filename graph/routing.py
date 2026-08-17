from graph.state import VRAGState
from config import MAX_REVISION_ROUNDS


def route_after_prosecutor(state: VRAGState):

    investigation_request = (
        state["prosecutor_output"].investigation_request
    )

    if investigation_request is not None:
        return "investigation_node"

    return "judge_node"


def route_after_judge(state: VRAGState):

    judge_decision = state["judge_output"].decision

    if judge_decision == "Accept":
        return "end"

    elif state["revision_count"] >= MAX_REVISION_ROUNDS:
        return "end"

    else:
        return "responder_node"