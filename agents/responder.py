from generation.llm import get_chat_model
from agents.prompts import RESPONDER_PROMPT
from generation.formatter import format_documents
from agents.schemas import ResponderOutput

def responder(question, retrieved_docs, previous_output=None, additional_docs=None, revision_instructions=None,):

    formatted_context = format_documents(retrieved_docs)
    formatted_additional_context = format_documents(additional_docs or [])

    model = get_chat_model()
    structured_model = model.with_structured_output(ResponderOutput)

    chain = RESPONDER_PROMPT | structured_model 

    return chain.invoke(
        {
            "question": question,
            "context": formatted_context,
            "additional_context": formatted_additional_context,
            "previous_output": previous_output,
            "revision_instructions": revision_instructions,
        }
    )