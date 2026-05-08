import threading
from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services import run_logger
from app.services.project_store import (
    FORMAT_PRESETS,
    create_project,
    delete_project,
    get_latest_outputs,
    get_project,
    list_projects,
    save_human_notes,
    save_run_outputs,
    update_run_state,
)
from app.utils.screenplay_parser import screenplay_to_html

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[1]
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
templates.env.filters["screenplay"] = screenplay_to_html


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    from app.llm.ollama_client import check_ollama
    projects = list_projects()
    ollama = check_ollama()
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"projects": projects, "ollama": ollama},
    )


@router.get("/projects")
def projects_page():
    return RedirectResponse(url="/", status_code=302)


@router.get("/projects/new", response_class=HTMLResponse)
def new_project_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="project_new.html",
        context={"format_presets": FORMAT_PRESETS},
    )


@router.post("/projects/new")
def new_project_submit(
    title: str = Form(...),
    theme: str = Form(...),
    tone: str = Form(...),
    genre: str = Form(...),
    format: str = Form(...),
    story_notes: str = Form(""),
    custom_runtime_minutes: int | None = Form(None),
):
    try:
        slug = create_project(
            title=title,
            theme=theme,
            tone=tone,
            genre=genre,
            format=format,
            story_notes=story_notes,
            custom_runtime_minutes=custom_runtime_minutes,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return RedirectResponse(url=f"/projects/{slug}", status_code=303)


@router.get("/projects/{slug}", response_class=HTMLResponse)
def project_detail(request: Request, slug: str):
    project = get_project(slug)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    outputs = get_latest_outputs(slug)
    scene_tags_by_number = {
        tag["scene_number"]: tag
        for tag in outputs.get("scene_tags", {}).get("scenes", [])
    }
    return templates.TemplateResponse(
        request=request,
        name="project_detail.html",
        context={"project": project, "outputs": outputs, "scene_tags_by_number": scene_tags_by_number},
    )


def _invoke_graph(slug: str):
    from app.graphs.screenplay_graph import build_graph

    project = get_project(slug)
    existing = get_latest_outputs(slug)
    try:
        graph = build_graph()
        result = graph.invoke({
            "slug": slug,
            "brief": project["brief"],
            "outline": existing.get("outline") or {},
            "draft": existing.get("draft") or "",
            "eval_result": {},
            "scene_tags": {},
            "human_notes": project["notes"],
            "current_stage": "running",
            "story_loops": project["run_state"].get("story_loops", 0),
            "note_loops": project["run_state"].get("note_loops", 0),
            "errors": [],
        })
        save_run_outputs(
            slug=slug,
            outline=result["outline"],
            draft=result["draft"],
            eval_result=result.get("eval_result"),
            scene_tags=result.get("scene_tags"),
            story_loops=result["story_loops"],
        )
        run_logger.done(slug)
    except Exception as e:
        update_run_state(slug, {"status": "error"})
        run_logger.error(slug, str(e))


def _start_run(slug: str):
    update_run_state(slug, {"status": "running"})
    run_logger.start(slug)
    thread = threading.Thread(target=_invoke_graph, args=(slug,), daemon=True)
    thread.start()


@router.post("/projects/{slug}/run")
def run_project(slug: str):
    project = get_project(slug)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    _start_run(slug)
    return RedirectResponse(url=f"/projects/{slug}", status_code=303)


@router.get("/projects/{slug}/status")
def project_status(slug: str):
    return JSONResponse(content=run_logger.get_status(slug))


@router.get("/projects/{slug}/review", response_class=HTMLResponse)
def review_page(request: Request, slug: str):
    project = get_project(slug)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    outputs = get_latest_outputs(slug)
    scene_notes = {
        sn["scene_number"]: {"note": sn.get("note", ""), "locked": sn.get("locked", False)}
        for sn in project["notes"].get("scene_notes", [])
    }
    return templates.TemplateResponse(
        request=request,
        name="project_review.html",
        context={
            "project": project,
            "outputs": outputs,
            "scene_notes": scene_notes,
        },
    )


@router.post("/projects/{slug}/review")
async def review_submit(request: Request, slug: str):
    project = get_project(slug)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    form_data = await request.form()
    overall_notes = str(form_data.get("overall_notes", "")).strip()

    scene_notes = []
    for key, value in form_data.items():
        if key.startswith("scene_note_"):
            try:
                scene_num = int(key.replace("scene_note_", ""))
                note_text = str(value).strip()
                locked = str(form_data.get(f"scene_lock_{scene_num}", "")) == "on"
                if note_text or locked:
                    scene_notes.append({"scene_number": scene_num, "note": note_text, "locked": locked})
            except ValueError:
                pass
    scene_notes.sort(key=lambda x: x["scene_number"])

    save_human_notes(slug, {"overall_notes": overall_notes, "scene_notes": scene_notes})
    _start_run(slug)
    return RedirectResponse(url=f"/projects/{slug}", status_code=303)


@router.post("/projects/{slug}/delete")
def delete_project_route(slug: str):
    project = get_project(slug)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    delete_project(slug)
    return RedirectResponse(url="/projects", status_code=303)
