from generation.llm import get_chat_model
from agents.prompts import PROSECUTOR_PROMPT
from generation.formatter import format_documents
from agents.schemas import ProsecutorOutput

def prosecutor(question, responder_output, retrieved_docs):

    formatted_context = format_documents(retrieved_docs)

    model = get_chat_model()
    structured_model = model.with_structured_output(ProsecutorOutput)

    chain = PROSECUTOR_PROMPT | structured_model 

    return chain.invoke(
        {
            "question": question,
            "responder_output": responder_output,
            "context": formatted_context,
        }
    )