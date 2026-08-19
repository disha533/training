# from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from web.routers import chat

app = FastAPI(title="Expense Manager Chat")

app.include_router(chat.router)

app.mount("/", StaticFiles(directory="web/static", html=True), name="static")


# STATIC_DIR = Path(__file__).parent / "static"
