from pathlib import Path
import json
import re
import shutil

BASE_DIR = Path(__file__).resolve().parents[2]
PROJECTS_DIR = BASE_DIR / "projects"

FORMAT_PRESETS = {
    "short":      {"label": "Short Film",              "runtime_minutes": 15},
    "feature":    {"label": "Feature Film",            "runtime_minutes": 100},
    "tv_hour":    {"label": "TV Hour",                 "runtime_minutes": 45},
    "tv_half":    {"label": "TV Half-Hour",            "runtime_minutes": 24},
    "advert":     {"label": "Advert / Commercial",     "runtime_minutes": 1},
    "webseries":  {"label": "Web Series Episode",      "runtime_minutes": 8},
    "custom":     {"label": "Custom Runtime",          "runtime_minutes": None},
}


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "project"


def list_projects():
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    items = []
    for path in PROJECTS_DIR.iterdir():
        if path.is_dir():
            run_state = path / "run_state.json"
            state = {}
            if run_state.exists():
                state = json.loads(run_state.read_text())
            items.append({"slug": path.name, "state": state})
    return sorted(items, key=lambda x: x["slug"])


def create_project(
    title: str,
    theme: str,
    tone: str,
    genre: str,
    format: str,
    story_notes: str = "",
    custom_runtime_minutes: int | None = None,
) -> str:
    if format not in FORMAT_PRESETS:
        raise ValueError(f"Unknown format '{format}'.")
    if format == "custom":
        if not custom_runtime_minutes or custom_runtime_minutes < 1:
            raise ValueError("A custom runtime must be at least 1 minute.")
        runtime = custom_runtime_minutes
    else:
        runtime = FORMAT_PRESETS[format]["runtime_minutes"]

    slug = slugify(title)
    root = PROJECTS_DIR / slug

    if root.exists():
        raise ValueError(f"A project with slug '{slug}' already exists.")

    for child in [
        "brief",
        "outlines",
        "drafts",
        "tags",
        "evals",
        "notes",
        "exports",
    ]:
        (root / child).mkdir(parents=True, exist_ok=True)

    brief = {
        "title": title,
        "theme": theme,
        "tone": tone,
        "genre": genre,
        "format": format,
        "format_label": FORMAT_PRESETS[format]["label"],
        "target_runtime_minutes": runtime,
        "story_notes": story_notes.strip(),
    }

    (root / "brief" / "project_brief.json").write_text(json.dumps(brief, indent=2))
    (root / "run_state.json").write_text(
        json.dumps(
            {
                "title": title,
                "slug": slug,
                "current_stage": "created",
                "story_loops": 0,
                "note_loops": 0,
                "status": "idle",
            },
            indent=2,
        )
    )

    return slug


def get_project(slug: str):
    root = PROJECTS_DIR / slug
    if not root.exists():
        return None

    run_state = (
        json.loads((root / "run_state.json").read_text())
        if (root / "run_state.json").exists()
        else {}
    )
    brief = (
        json.loads((root / "brief" / "project_brief.json").read_text())
        if (root / "brief" / "project_brief.json").exists()
        else {}
    )
    notes_path = root / "notes" / "human_notes_v1.json"
    notes = json.loads(notes_path.read_text()) if notes_path.exists() else {"notes": []}

    return {
        "slug": slug,
        "root": str(root),
        "run_state": run_state,
        "brief": brief,
        "notes": notes,
    }


def save_human_notes(slug: str, payload: dict):
    root = PROJECTS_DIR / slug
    (root / "notes").mkdir(parents=True, exist_ok=True)
    (root / "notes" / "human_notes_v1.json").write_text(json.dumps(payload, indent=2))


def update_run_state(slug: str, updates: dict):
    run_state_path = PROJECTS_DIR / slug / "run_state.json"
    state = json.loads(run_state_path.read_text())
    state.update(updates)
    run_state_path.write_text(json.dumps(state, indent=2))


def save_run_outputs(slug: str, outline: dict, draft: str, story_loops: int):
    root = PROJECTS_DIR / slug
    (root / "outlines" / f"outline_v{story_loops}.json").write_text(
        json.dumps(outline, indent=2)
    )
    (root / "drafts" / f"draft_v{story_loops}.txt").write_text(draft)
    update_run_state(slug, {
        "current_stage": "drafted",
        "story_loops": story_loops,
        "status": "idle",
    })


def get_latest_outputs(slug: str) -> dict:
    root = PROJECTS_DIR / slug
    outline = {}
    draft = ""

    outlines_dir = root / "outlines"
    if outlines_dir.exists():
        files = sorted(
            outlines_dir.glob("outline_v*.json"),
            key=lambda p: int(p.stem.split("v")[1]),
        )
        if files:
            outline = json.loads(files[-1].read_text())

    drafts_dir = root / "drafts"
    if drafts_dir.exists():
        files = sorted(
            drafts_dir.glob("draft_v*.txt"),
            key=lambda p: int(p.stem.split("v")[1]),
        )
        if files:
            draft = files[-1].read_text()

    return {"outline": outline, "draft": draft}


def delete_project(slug: str):
    root = PROJECTS_DIR / slug
    if not root.exists():
        raise ValueError(f"Project '{slug}' not found.")
    shutil.rmtree(str(root))