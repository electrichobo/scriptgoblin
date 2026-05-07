from pathlib import Path

from fastapi import FastAPI

from app.routes.pages import router as pages_router

app = FastAPI(title="Script Goblin")

BASE_DIR = Path(__file__).resolve().parent
app.include_router(pages_router)