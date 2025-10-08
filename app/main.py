from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine
from app.models import User, Message
from app.routers import chat, notes, checkin

engine = create_engine("sqlite:///./app.db")

def create_db():
    SQLModel.metadata.create_all(engine)

def get_app():
    app = FastAPI(title="AI Clarity Companion", version="0.1.0")
    app.include_router(chat.router, tags=["chat"])
    app.include_router(notes.router, tags=["notes"])
    app.include_router(checkin.router, tags=["checkin"])
    return app

create_db()
app = get_app()