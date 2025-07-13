# app/langgraph_flow.py

from langgraph.graph import StateGraph, START
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver

from typing import List, TypedDict
from langchain_core.documents import Document

import os
from dotenv import load_dotenv

from datetime import datetime

today = datetime.now().strftime("%B %d, %Y")

load_dotenv()

chatbot_sessions = {}

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


groq_api_key = os.getenv("GROQ_API_KEY")

prompt = ChatPromptTemplate.from_template(f"""
You are PDFAgent, a helpful assistant that reads and understands PDF documents uploaded by the user.

Today's date is {today}.

Your role is to answer user questions using only the information provided in the `context` from the PDF.

### Behavior Instructions:
- If the user greets you (e.g., "hi", "hello", "hey"), respond with: "Hi! I'm PDFAgent. Ask me anything about the PDF you've uploaded."
- If the user asks a question related to the document, carefully read the `context` and give a concise and accurate answer.
- If the answer is not present in the PDF context, reply with: "Sorry, I couldn’t find that information in the uploaded document."
- Keep answers professional, clear, and easy to understand.
- Never make up information or answer outside the context.

---

Context:
{{context}}

Question:
{{question}}

---

PDFAgent’s response:
""")

llm = ChatGroq(groq_api_key=groq_api_key, 
               model="llama-3.3-70b-versatile")
memory = MemorySaver()

def create_langgraph_chatbot(session_id: str, vector_store):
    def retrieve(state: State):
        return {"context": vector_store.similarity_search(state["question"])}

    def generate(state: State):
        content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = prompt.invoke({"question": state["question"], "context": content})
        response = llm.invoke(messages)
        return {"answer": response.content}

    graph = (
        StateGraph(State)
        .add_node("retrieve", retrieve)
        .add_node("generate", generate)
        .add_edge(START, "retrieve")
        .add_edge("retrieve", "generate")
        .compile(checkpointer=memory)
    )

    chatbot_sessions[session_id] = graph
