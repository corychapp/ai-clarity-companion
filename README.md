# AI Clarity Companion (Portfolio MVP)

An empathetic journaling & clarity assistant that:
- Reflects back feelings with a supportive, coaching tone
- Remembers prior sessions via vector memory (ChromaDB)
- Guides a single tiny next action to build momentum

## Why this project?
It demonstrates:
- **AI pipeline design** (model routing, guardrails, memory retrieval)
- **Backend engineering** with **FastAPI**
- **Vector memory** with **ChromaDB**
- **Empathetic prompt design** for wellbeing/coaching contexts
- A tiny **Streamlit** UI for a complete demo

---

## Run Options (Free-first)
This project works **without paying for the OpenAI API**.

### A) Free Local Model (Recommended): **Ollama**
1. Install Ollama: https://ollama.com/download
2. Pull a small model: `ollama pull llama3.2`
3. Start the server (usually autostarts): it serves at `http://localhost:11434`

Then in a terminal:
```bash
pip install -r requirements.txt
export MODEL_BACKEND=ollama
export OLLAMA_MODEL=llama3.2
uvicorn app.main:app --reload
# in another terminal
streamlit run demo/app.py
```

### B) Optional: OpenAI API
If you have an API key:
```bash
export OPENAI_API_KEY=sk-...
export MODEL_BACKEND=openai
export OPENAI_MODEL=gpt-4o-mini
uvicorn app.main:app --reload
streamlit run demo/app.py
```

### C) Mock mode (no model at all — for quick UI demo)
```bash
export MODEL_BACKEND=mock
uvicorn app.main:app --reload
streamlit run demo/app.py
```

> **Note:** ChromaDB will download a small sentence-transformer on first run
> to embed text for search (internet required once). It stores persistent data in `.chroma/`.

---

## Endpoints (MVP)
- `POST /chat` → empathetic chat w/ memory recall
- `POST /save_note` → store reflection text in SQLite + Chroma
- `GET /daily-checkin?user_id=...` → 3 guided prompts for clarity

## Data
- SQLite tables: `users`, `messages`
- Chroma collections: `notes_{user_id}`

## Safety & Ethics
- Coaching tone only (non-clinical). No diagnosis or crisis advice.
- If crisis language is detected, we respond with a **supportive handoff** encouraging contacting local emergency services or crisis hotlines.

## Demo Script (60–90 sec)
1. Type: “I’m anxious about work tomorrow.” → assistant validates + 1 next step.
2. Add a note (“I’ll try a 10-min wind-down tonight”), then ask about it later:
   “Did I mention a bedtime routine last week?” → recalls from memory.
3. Click **Daily Check-In** → see 3 structured prompts.
4. Wrap by mentioning: FastAPI + vector memory + empathetic guardrails.

---

## Project Structure
```
ai-clarity-companion/
  app/
    main.py
    deps.py
    models.py
    memory.py
    prompts.py
    routers/
      chat.py
      notes.py
      checkin.py
  demo/
    app.py
  requirements.txt
  README.md
```

Happy hacking!