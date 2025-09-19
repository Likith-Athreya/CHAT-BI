import os
from langchain_groq import ChatGroq

def get_llm():
    return ChatGroq(
        model=os.getenv("GROQ_MODEL", "gemma2-9b-it"),
        temperature=0.1,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )