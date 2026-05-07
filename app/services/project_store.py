from pathlib import Path
import json
import re

BASE_DIR = Path(__file__).resolve().parents[2]
PROJECTS_DIR = BASE_DIR / "projects"


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


def create_project(title: str, theme: str, tone: str, genre: str) -> str:
    slug = slugify(title)
    root = PROJECTS_DIR / slug

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