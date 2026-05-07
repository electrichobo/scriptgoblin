# Script Goblin

Script Goblin is a local-first screenplay development app built for narrative and branded writing workflows. It combines a FastAPI web interface, a LangGraph backend, and a remote Ollama server running on Unraid to support structured screenplay generation, revision, scene tagging, human review, and final export.

## What Script Goblin is for

This app is designed to help with:

- screenplay ideation and outline generation,
- draft writing and rewrite loops,
- story evaluation,
- scene tagging,
- human production review,
- application of production notes,
- verification that notes were applied,
- export of final screenplay materials.

The goal is not to replace a writer or director. The goal is to create a calm, practical workflow tool that helps move a screenplay from idea to structured draft to reviewable output.

## Current setup

Script Goblin is being developed on the main PC, with model inference handled remotely by Ollama on the Unraid server.

### Development machine

- Main PC: Windows
- Project location: `E:\Script Goblin`

### Model host

- Ollama runs on the Unraid server
- The project connects to Ollama over the network
- Available models are already confirmed through the `/api/tags` endpoint
- Ollama connectivity is checked live on the dashboard

### Working approach

- Files and project data live on the main PC.
- Ollama inference happens on the Unraid server.
- The web app runs locally on the main PC.
- LangGraph controls the workflow and state.

## What has already been done

The following work is already complete:

- The base project scaffold has been created in `E:\Script Goblin`.
- The Python virtual environment has been installed.
- Required Python packages have been installed.
- The remote Ollama server has been verified as reachable from the main PC.
- Available Ollama models have been confirmed.
- The web app direction has been chosen: FastAPI + Jinja templates.
- The full web shell is complete and running: dashboard, project creation, project detail, and human review pages.
- Project management is complete: create, view, delete projects; store briefs and notes as JSON files.
- The LangGraph pipeline is partially built: outline node and draft node are implemented and confirmed working end-to-end.
- The outline produces structured scene cards (purpose, objective, turning point, beats) rendered as a sequence outline.
- The draft is rendered in the browser with proper screenplay formatting (scene headings, action, character, dialogue, parenthetical, transitions).
- The human review page has been redesigned: two-column layout with the formatted script on the left and overall notes + per-scene margin notes on the right.
- Script format and runtime selection are implemented: Short, Feature, TV Hour, TV Half-Hour, Advert, Web Series, and Custom.
- A Story Notes field allows specifying characters, an existing story shell, or other specific requirements at project creation.
- Static file serving is in place; the app has a screenplay-aesthetic visual design (dark shell, white paper pages, Courier typeface).

## What the app will become

Script Goblin will eventually be a small full-stack workflow app with:

- a project dashboard,
- project creation,
- screenplay brief entry,
- draft generation,
- evaluation and revision loops,
- scene tags,
- human notes and approvals,
- status tracking,
- exports.

The app will stay intentionally simple in the interface and practical in the workflow.

## Current architecture

### Front end

- FastAPI web server
- Jinja2 templates
- Plain HTML with a screenplay-aesthetic CSS layer (`app/static/style.css`)
- Minimal inline JS only where necessary (format selector toggle, delete confirmation)

### Backend

- LangGraph for workflow orchestration
- State-driven node graph (`ScreenplayState` TypedDict)
- Interrupt/resume support for human review (planned — Phase 4)
- Structured outputs for outline (Pydantic models via `with_structured_output`)

### Model layer

- Ollama on Unraid, `192.168.1.169:11434`
- Remote HTTP access from the main PC
- Model selection by environment variable (set in `.env`)
- Connectivity checked live on dashboard load

### Storage

- Local project folders under `E:\Script Goblin\projects`
- JSON files for briefs, run state, outline (structured), and notes
- Plain text files for draft versions

### Key modules

| Path | Purpose |
|---|---|
| `app/web.py` | FastAPI app entry point, static file mount |
| `app/config.py` | Env var loading (Ollama URL, model names) |
| `app/routes/pages.py` | All web routes |
| `app/services/project_store.py` | Project CRUD, file I/O, format presets |
| `app/state/graph_state.py` | `ScreenplayState` TypedDict |
| `app/state/models.py` | Pydantic models: `ScreenplayOutline`, `StoryEval`, `SceneTags`, `VerifyReport` |
| `app/llm/ollama_client.py` | `ChatOllama` factory, Ollama connectivity check |
| `app/llm/model_router.py` | Role-based model selection (writer, tagger, verifier) |
| `app/llm/structured_output.py` | `parse_structured()` helper |
| `app/graphs/screenplay_graph.py` | LangGraph graph builder |
| `app/nodes/outline.py` | Generates structured scene outline |
| `app/nodes/draft.py` | Generates screenplay draft from outline |
| `app/utils/screenplay_parser.py` | Converts raw screenplay text to formatted HTML |
| `app/prompts/` | System prompt files per role |
| `app/templates/` | Jinja2 HTML templates |
| `app/static/style.css` | App and screenplay CSS |

## Planned model usage

The current model pool includes:

- `fluffy/l3-8b-stheno-v3.2:latest`
- `gemma2:9b`
- `gemma4:26b`
- `qwen2.5:7b`
- `qwen3.6:27b`
- `qwen3.6:35b`
- `phi4-mini:latest`

Planned usage:

- Writer / rewriter: `fluffy/l3-8b-stheno-v3.2:latest`
- Tagging: `qwen2.5:7b` or `gemma2:9b`
- Verification: `gemma2:9b` or `qwen2.5:7b`
- Heavier reasoning fallback: `qwen3.6:27b` or `qwen3.6:35b`
- Lightweight helper: `phi4-mini:latest`

## Roadmap

## Phase 1: Basic web shell — COMPLETE

Goal: get the app booting cleanly in the browser.

- FastAPI entrypoint, route handlers, and templates all working.
- Project creation, listing, and detail pages confirmed functional.

## Phase 2: Project management — COMPLETE

Goal: make the app useful before any LangGraph logic is added.

- Create new projects from the UI with brief, theme, tone, genre, format, runtime, and story notes.
- Store project briefs as JSON.
- List existing projects on the dashboard with live Ollama status.
- View project detail as a screenplay title page.
- Store and display human review notes.
- Delete projects.

## Phase 3: LangGraph backend — IN PROGRESS

Goal: turn Script Goblin into a real workflow engine.

Done:
- Graph state (`ScreenplayState`)
- Outline node (structured scene cards: purpose, objective, turning point, beats)
- Draft node (full screenplay from outline)
- Confirmed end-to-end: brief → outline → draft → saved → displayed

Remaining:
- Story evaluation node
- Rewrite loop (conditional edge based on eval score)
- Scene tag node
- Human review interrupt (LangGraph interrupt/resume)
- Note application node
- Verification node
- Export node

## Phase 4: Human-in-the-loop workflow

Goal: make the app pause for review and resume cleanly.

Tasks:

- add interrupt support,
- store thread/run state,
- resume with human notes,
- verify note application,
- keep a clear change history.

## Phase 5: Output and export

Goal: make final results easy to use.

Tasks:

- export final draft text,
- export structured notes,
- export scene tags,
- export revision history,
- export project snapshots.

## Phase 6: Polish

Goal: improve the experience once the core workflow is stable.

Tasks:

- revision history views,
- diff views,
- export download buttons,
- better error handling.

## Immediate next steps

The next step is finishing Phase 3 with a thin slice of the evaluation and rewrite loop:

1. Build `story_eval` node — calls verifier model, returns `StoryEval` (score, feedback, `should_rewrite`).
2. Build `rewrite` node — applies eval feedback to the draft.
3. Add conditional edge after `story_eval`: if `should_rewrite` and loops < cap, route to rewrite; otherwise continue.
4. Wire updated graph: `draft → story_eval → (rewrite → story_eval)* → END`.

After the eval loop is stable, proceed to scene tagging and then the human review interrupt.

## Checklist

### Setup

- [x] Create project scaffold in `E:\Script Goblin`
- [x] Create virtual environment
- [x] Install Python requirements
- [x] Verify Ollama endpoint from main PC
- [x] Confirm available models on the Unraid server

### Web shell

- [x] Create `app\web.py`
- [x] Create `app\routes\pages.py`
- [x] Create `app\services\project_store.py`
- [x] Create template files
- [x] Confirm `python -m uvicorn app.web:app --reload` starts without errors
- [x] Confirm `/` loads in browser
- [x] Confirm `/projects/new` works
- [x] Confirm project folder creation works

### Project management

- [x] Create new projects from the UI
- [x] Store project briefs (title, theme, tone, genre, format, runtime, story notes)
- [x] List existing projects on dashboard
- [x] View project status
- [x] Store human review notes (structured: overall + per-scene)
- [x] Delete projects

### LangGraph backend

- [x] Create graph state model (`ScreenplayState`)
- [x] Create screenplay graph file
- [x] Create outline node (structured scene cards)
- [x] Create draft node
- [ ] Create evaluation node
- [ ] Create rewrite loop
- [ ] Create scene tag node
- [ ] Create human review interrupt
- [ ] Create note application node
- [ ] Create verification node
- [ ] Create export node

### Project workflow

- [ ] Create first sample project
- [ ] Generate first outline
- [ ] Generate first draft
- [ ] Run first evaluation loop
- [ ] Tag scenes
- [ ] Enter human notes
- [ ] Resume graph after review
- [ ] Verify notes were applied
- [ ] Export final package

## Working principle

Keep it simple. Build one thin vertical slice at a time. If a step is not needed yet, do not build it yet.

## Notes

This project is intentionally local-first, file-based, and workflow-driven. The goal is clarity, reliability, and a low-friction creative process.

Ollama is fully stateless — it stores no per-project data between calls. Project deletion removes only the local project folder. Once LangGraph checkpointing is added (Phase 4), thread state will also need to be cleared on delete.
