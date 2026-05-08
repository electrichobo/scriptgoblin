import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.pages import router as pages_router


class _SuppressOK(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            # uvicorn passes status_code as the last positional arg (int)
            if record.args and record.args[-1] == 200:
                return False
        except (TypeError, IndexError):
            pass
        return True


logging.getLogger("uvicorn.access").addFilter(_SuppressOK())

app = FastAPI(title="Script Goblin")

_BASE = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(_BASE / "static")), name="static")
app.include_router(pages_router)