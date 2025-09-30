from langchain_groq import ChatGroq

# =============================
# GROQ LLM
# =============================
llm = ChatGroq(
    model="gemma2-9b-it",
    groq_api_key="",
    temperature=0.7,
    max_tokens=500,
    timeout=30
)
