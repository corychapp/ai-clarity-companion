from fastapi import APIRouter
from pydantic import BaseModel
from app.memory import add_note
from datetime import datetime
import uuid

router = APIRouter()

class NoteIn(BaseModel):
    user_id: str
    text: str

@router.post("/save_note")
async def save_note(payload: NoteIn):
    nid = str(uuid.uuid4())
    meta = {"type": "journal", "ts": datetime.utcnow().isoformat()}
    add_note(payload.user_id, nid, payload.text, meta)
    return {"ok": True, "note_id": nid}