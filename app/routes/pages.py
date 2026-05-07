from pathlib import Path
import json

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.project_store import (
    create_project,
    get_project,
    list_projects,
    save_human_notes,
)

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[1]
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    projects = list_projects()
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"projects": projects},
    )


@router.get("/projects", response_class=HTMLResponse)
def projects_page(request: Request):
    projects = list_projects()
    return templates.TemplateResponse(
        request=request,
        name="projects.html",
        context={"projects": projects},
    )


@router.get("/projects/new", response_class=HTMLResponse)
def new_project_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="project_new.html",
        context={},
    )


@router.post("/projects/new")
def new_project_submit(
    title: str = Form(...),
    theme: str = Form(...),
    tone: str = Form(...),
    genre: str = Form(...),
):
    slug = create_project(
        title=title,
        theme=theme,
        tone=tone,
        genre=genre,
    )
    return RedirectResponse(url=f"/projects/{slug}", status_code=303)


@router.get("/projects/{slug}", response_class=HTMLResponse)
def project_detail(request: Request, slug: str):
    project = get_project(slug)
    return templates.TemplateResponse(
        request=request,
        name="project_detail.html",
        context={"project": project},
    )


@router.get("/projects/{slug}/review", response_class=HTMLResponse)
def review_page(request: Request, slug: str):
    project = get_project(slug)
    return templates.TemplateResponse(
        request=request,
        name="project_review.html",
        context={"project": project},
    )


@router.post("/projects/{slug}/review")
def review_submit(slug: str, notes_json: str = Form(...)):
    payload = json.loads(notes_json)
    save_human_notes(slug, payload)
    return RedirectResponse(url=f"/projects/{slug}", status_code=303)