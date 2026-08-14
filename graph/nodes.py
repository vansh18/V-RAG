from graph.state import VRAGState
from agents.responder import responder
from agents.prosecutor import prosecutor
from retrieval.retriever import retrieve
from config import INVESTIGATION_K


def responder_node(state: VRAGState):

    output = responder(
        state["question"],
        state["retrieved_documents"]
    )

    return {
        "responder_output": output
    }

def prosecutor_node(state: VRAGState):

    output = prosecutor(
        state["question"],
        state["responder_output"],
        state["retrieved_documents"]
    )

    return {
        "prosecutor_output": output
    }

def investigation_node(state: VRAGState):

    investigation_request = (
        state["prosecutor_output"].investigation_request
    )

    if investigation_request is None:
        return {
            "additional_documents": state["additional_documents"]
        }

    query = investigation_request.search_query

    new_documents = retrieve(
        query,
        INVESTIGATION_K
    )

    updated_documents = (
        state["additional_documents"] + new_documents
    )

    return {
        "additional_documents": updated_documents
    }