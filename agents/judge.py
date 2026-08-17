from generation.llm import get_chat_model
from agents.prompts import JUDGE_PROMPT
from generation.formatter import format_documents
from agents.schemas import JudgeOutput

def judge(question, responder_output, prosecutor_output, retrieved_docs, additional_docs):

    formatted_original_docs = format_documents(retrieved_docs)
    formatted_additional_docs = format_documents(additional_docs)

    model = get_chat_model()
    structured_model = model.with_structured_output(JudgeOutput)

    chain = JUDGE_PROMPT | structured_model

    return chain.invoke(
        {
            "question": question,
            "responder_output": responder_output,
            "prosecutor_output": prosecutor_output,
            "original_context": formatted_original_docs,
            "additional_context": formatted_additional_docs
        }
    )