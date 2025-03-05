from fastapi import FastAPI
from devops_bot import qa_chain  # Importing your chatbot logic

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the DevOps Chatbot API!"}

@app.get("/ask")
def ask_devops(question: str):
    response = qa_chain.run(question)
    return {"question": question, "response": response}

