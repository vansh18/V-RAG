from typing import TypedDict, Optional
from langchain_core.documents import Document

from agents.schemas import (
    ResponderOutput,
    ProsecutorOutput,
    # JudgeOutput,
)

class VRAGState(TypedDict):

    question: str
    retrieved_documents: list[Document]
    responder_output: Optional[ResponderOutput]
    prosecutor_output: Optional[ProsecutorOutput]
    additional_documents: list[Document]
    # judge_output: Optional[JudgeOutput]
    revision_count: int