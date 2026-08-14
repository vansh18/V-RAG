from retrieval.retriever import retrieve
from generation.baseline import generate_answer
from dotenv import load_dotenv
load_dotenv()

question = "What is the background of DOJ Guidance 2011-4?"

retrieved_docs = retrieve(question)
answer = generate_answer(question, retrieved_docs)

print(answer)