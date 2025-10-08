import os, requests
from typing import List, Dict

# Simple model router: 'ollama' (free, local), 'openai' (optional), or 'mock'
MODEL_BACKEND = os.getenv("MODEL_BACKEND", "mock").lower()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def generate_reply(messages: List[Dict[str, str]]) -> str:
    if MODEL_BACKEND == "ollama":
        return _ollama_generate(messages)
    if MODEL_BACKEND == "openai" and OPENAI_API_KEY:
        return _openai_generate(messages)
    return _mock_generate(messages)

def _ollama_generate(messages: List[Dict[str,str]]) -> str:
    # Convert to a single prompt; Ollama chat endpoint exists but simple prompt is fine for demo.
    sys = "\n".join([m["content"] for m in messages if m["role"] == "system"])
    usr = "\n".join([m["content"] for m in messages if m["role"] == "user"])
    prompt = (sys + "\n\nUser: " + usr + "\nAssistant:").strip()
    try:
        r = requests.post("http://localhost:11434/api/generate",
                          json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
                          timeout=120)
        r.raise_for_status()
        data = r.json()
        return data.get("response", "").strip() or "(no response)"
    except Exception as e:
        return f"(ollama error: {e})"

def _openai_generate(messages: List[Dict[str,str]]) -> str:
    # Lightweight call via REST to avoid SDK dependency.
    import json, requests
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"model": OPENAI_MODEL, "messages": messages}
    try:
        r = requests.post("https://api.openai.com/v1/chat/completions",
                          headers=headers, json=payload, timeout=120)
        r.raise_for_status()
        j = r.json()
        return j["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"(openai error: {e})"

def _mock_generate(messages: List[Dict[str,str]]) -> str:
    # Very small fake coach for demos when no model is available.
    user = " ".join([m["content"] for m in messages if m["role"] == "user"])
    base = "Thanks for sharing. It sounds like this is genuinely important to you."
    # tiny heuristic
    if any(w in user.lower() for w in ["anxious","stuck","overwhelmed","tired"]):
        feeling = "You're carrying a lot right now."
    else:
        feeling = "You’re looking for momentum."
    step = "What would a 10-minute, 1-degree step look like today?"
    return f"{base} {feeling} One tiny experiment: write down one worry, one wish, and one next step. {step}"