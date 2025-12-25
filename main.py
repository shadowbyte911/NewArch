import chromadb
import ollama
from ollama import Client
from pydantic import BaseModel
from typing import Literal
import json


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

MODEL_NAME = "llama3.2"
EMBEDDING_MODEL = "mxbai-embed-large"
MEMORY_PATH = "./newarch_memory"


llm_client = Client(host="http://localhost:11434", timeout=None)
db_client = chromadb.PersistentClient(path=MEMORY_PATH)
collection = db_client.get_or_create_collection(name="episodic_memory")


# -------------------------------------------------------------------
# Data Models
# -------------------------------------------------------------------

class UserIntent(BaseModel):
    intent: Literal["statement", "question", "greeting"]
    requires_memory: bool


# -------------------------------------------------------------------
# Utility Functions
# -------------------------------------------------------------------

def embed(text: str):
    return llm_client.embeddings(
        model=EMBEDDING_MODEL,
        prompt=text
    )["embedding"]


# -------------------------------------------------------------------
# Core Engine
# -------------------------------------------------------------------

def ask_newarch(user_input: str) -> str:
    """
    Main cognitive loop with gated memory retrieval.
    """

    perception_prompt = (
        f"Classify the intent of the following input and decide whether "
        f"episodic memory is required.\n"
        f"Respond in JSON only.\n\n"
        f"Input: \"{user_input}\""
    )

    perception_raw = llm_client.generate(
        model=MODEL_NAME,
        prompt=perception_prompt,
        format="json",
        keep_alive=-1
    )

    try:
        perception = UserIntent.model_validate_json(perception_raw["response"])
    except Exception:
        perception = UserIntent(
            intent="question",
            requires_memory=True
        )

    memory_context = "None"

    if perception.requires_memory:
        query_embedding = embed(user_input)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=1
        )

        if results["distances"][0] and results["distances"][0][0] < 0.1:
            memory_context = results["documents"][0][0]

    system_prompt = f"""
    You are NewArch, a memory-augmented AI system.

    Intent: {perception.intent}
    Retrieved Memory: {memory_context}

    Use memory only when it is relevant.
    If insufficient information is available, respond cautiously.
    """

    response = llm_client.generate(
        model=MODEL_NAME,
        system=system_prompt,
        prompt=user_input,
        keep_alive=-1
    )

    return response["response"].strip()


# -------------------------------------------------------------------
# CLI Interface
# -------------------------------------------------------------------

if __name__ == "__main__":
    print("NewArch initialized. Type 'exit' to quit.")

    while True:
        user_input = input("\nUser: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        answer = ask_newarch(user_input)
        print(f"\nAssistant: {answer}")
