from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.pages import router as pages_router

app = FastAPI(title="Script Goblin")

_BASE = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(_BASE / "static")), name="static")
app.include_router(pages_router)