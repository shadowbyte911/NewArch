## NewArch


NewArch is a **memory-augmented AI architecture experiment** focused on separating
**language ability**, **memory**, and **control logic** into explicit, inspectable components.

Instead of storing knowledge inside model weights, NewArch externalizes memory
and uses a gated retrieval pipeline to decide *when* and *how* memory should influence responses.

This project is intended as a **research and systems-design exploration**, not a production chatbot.

---

## Core Design Principles

- **Frozen Language Model**  
  The base LLM (Llama 3.2 via Ollama) is treated as a stable language and reasoning engine.
  It is never fine-tuned or overwritten.

- **Externalized Memory**  
  Knowledge and experiences are stored outside the model in structured, editable formats.

- **Gated Cognition**  
  Memory retrieval is optional and triggered only when required, reducing noise and false assumptions.

- **Interpretability**  
  Every decision (intent classification, memory usage) is explicit and debuggable.

---

## Architecture Overview
User Input ↓ Perception Module (Intent & Memory Need) ↓ Working Memory (Recent Context) ↓ Episodic Memory Retrieval (ChromaDB, gated) ↓ LLM Reasoning & Synthesis ↓ Response


### Components

- **Perception**
  - Classifies user intent (statement, question, greeting)
  - Decides whether episodic memory is required

- **Working Memory**
  - Maintains short-term conversational context (in RAM)

- **Episodic Memory**
  - Vector-based storage of past interactions (ChromaDB)
  - Retrieved only when relevant

- **Semantic Memory (Optional / External)**
  - Stable facts stored in editable JSON files
  - Updated via offline consolidation

- **Executive Control**
  - Routes information and enforces cautious reasoning when memory is uncertain

---

## Key Features

- Memory retrieval with similarity thresholds
- Confidence-aware responses
- No hallucinated long-term memory
- Fully offline operation after model download
- Simple, inspectable storage formats

---

## Installation

### Prerequisites
- Python 3.9+
- Ollama installed and running locally

Pull the required models:

```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
Install dependencies
pip install -r requirements.txt
Usage
Run the main interactive loop:

python main.py
Type exit or quit to stop the program.

Project Status
This project is experimental and under active iteration.

Planned improvements include:

Multi-memory retrieval consensus
Confidence-weighted episodic memories
Skill-based modular extensions (adapters / LoRA)
Memory consolidation heuristics
Tool and actuator integration
Disclaimer
This repository is a research prototype. It is not intended for production use or deployment without further safety and robustness work.

