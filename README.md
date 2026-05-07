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
- Initial HTML template files have been created.
- The first backend web files have been drafted.
- The project structure now includes folders for:
  - `app`
  - `projects`
  - `tests`
  - `scratch`

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
- Plain HTML first
- CSS and JS later only if needed

### Backend

- LangGraph for workflow orchestration
- State-driven node graph
- Interrupt/resume support for human review
- Structured outputs for tagging and verification

### Model layer

- Ollama on Unraid, 192.168.1.169:11434
- Remote HTTP access from the main PC
- Model selection by environment variables

### Storage

- Local project folders under `E:\Script Goblin\projects`
- JSON files for briefs, notes, run state, tags, and outputs

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

## Phase 1: Basic web shell

Goal: get the app booting cleanly in the browser.

Tasks:

- finish the FastAPI entrypoint,
- finish the route handlers,
- confirm templates render,
- confirm project creation works,
- confirm project detail pages load.

## Phase 2: Project management

Goal: make the app useful before any LangGraph logic is added.

Tasks:

- create new projects from the UI,
- store project briefs,
- list existing projects,
- view project status,
- store human review notes.

## Phase 3: LangGraph backend

Goal: turn Script Goblin into a real workflow engine.

Tasks:

- define graph state,
- define node schemas,
- build the outline node,
- build the draft node,
- build the story evaluation node,
- build the rewrite loop,
- build the scene tag node,
- build the human review interrupt,
- build the note application node,
- build the verification node,
- build the export node.

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

- better layout and styling,
- more readable status indicators,
- revision history views,
- diff views,
- export download buttons,
- better error handling.

## Immediate next steps

The next steps are:

1. Fix the current FastAPI/Jinja wiring.
2. Confirm the home page loads without errors.
3. Confirm project creation works.
4. Confirm project detail pages load.
5. Add the LangGraph graph after the web shell is stable.

## Checklist

### Setup

- [x] Create project scaffold in `E:\Script Goblin`
- [x] Create virtual environment
- [x] Install Python requirements
- [x] Verify Ollama endpoint from main PC
- [x] Confirm available models on the Unraid server

### Web shell

- [ ] Create `app\web.py`
- [ ] Create `app\routes\pages.py`
- [ ] Create `app\services\project_store.py`
- [x] Create template files
- [ ] Confirm `python -m uvicorn app.web:app --reload` starts without errors
- [ ] Confirm `/` loads in browser
- [ ] Confirm `/projects/new` works
- [ ] Confirm project folder creation works

### LangGraph backend

- [ ] Create graph state model
- [ ] Create screenplay graph file
- [ ] Create outline node
- [ ] Create draft node
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