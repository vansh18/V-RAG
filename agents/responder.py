from generation.llm import get_chat_model
from agents.prompts import RESPONDER_PROMPT
from generation.formatter import format_documents
from agents.schemas import ResponderOutput

def responder(question, retrieved_docs):

    formatted_context = format_documents(retrieved_docs)

    model = get_chat_model()
    structured_model = model.with_structured_output(ResponderOutput)

    chain = RESPONDER_PROMPT | structured_model 

    return chain.invoke(
        {
            "context": formatted_context,
            "question": question,
        }
    )