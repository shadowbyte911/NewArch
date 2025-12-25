# NewArch

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

