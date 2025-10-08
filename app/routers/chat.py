from fastapi import APIRouter
from pydantic import BaseModel
from app.prompts import SYSTEM_BASE, REFLECTION_SUFFIX
from app.memory import search_notes
from app.deps import generate_reply

router = APIRouter()


class ChatIn(BaseModel):
    user_id: str
    message: str


@router.post("/chat")
async def chat(payload: ChatIn):
    # Retrieve a few prior notes to use as context
    notes = search_notes(payload.user_id, payload.message, k=3)
    context_blurbs = "\n".join(
        [f"- {t}" for (t, _m) in notes]) if notes else ""

    system = SYSTEM_BASE
    if context_blurbs:
        system += f"\n\nRelevant prior notes (bullets):\n{context_blurbs}\n"
    system += REFLECTION_SUFFIX

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": payload.message},
    ]
    reply = generate_reply(messages)
    # notes is [(text, metadata), ...]
    recall = [{"text": t, **(m or {})} for (t, m) in notes]
    return {"reply": reply, "context_used": bool(notes), "recall": recall}
