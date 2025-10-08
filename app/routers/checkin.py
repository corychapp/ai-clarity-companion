from fastapi import APIRouter
from fastapi import Query

router = APIRouter()

@router.get("/daily-checkin")
async def daily_checkin(user_id: str = Query(...)):
    prompts = [
        "What emotion is loudest right now? Name it in one word.",
        "If today improved by one small notch, what would be different by tonight?",
        "What 10-minute action would move you 1° toward what matters?"
    ]
    return {"user_id": user_id, "prompts": prompts}