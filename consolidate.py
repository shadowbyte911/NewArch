import chromadb
import json
import ollama


MEMORY_PATH = "./newarch_memory"
SEMANTIC_FILE = "semantic_facts.json"


client = chromadb.PersistentClient(path=MEMORY_PATH)
collection = client.get_or_create_collection(name="episodic_memory")


def consolidate_memories():
    """
    Summarizes episodic memories into stable semantic facts.
    """
    documents = collection.get().get("documents", [])

    if len(documents) < 2:
        return

    formatted = "\n- ".join(documents)

    prompt = f"""
    You are given a list of raw user experiences.
    Extract stable, high-confidence facts about the user.
    Write each fact as a short, declarative sentence.

    Experiences:
    - {formatted}
    """

    response = ollama.generate(
        model="llama3.2",
        prompt=prompt
    )

    facts = [
        line.strip("- ").strip()
        for line in response["response"].splitlines()
        if line.strip()
    ]

    with open(SEMANTIC_FILE, "w", encoding="utf-8") as f:
        json.dump({"facts": facts}, f, indent=4)


if __name__ == "__main__":
    consolidate_memories()
