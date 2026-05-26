"""FastAPI backend for Manimations Studio."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Repo root on path for visual resolver
MANIM_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(MANIM_ROOT / "animations"))
sys.path.insert(0, str(MANIM_ROOT / "platform" / "backend"))

load_dotenv(MANIM_ROOT / "platform" / ".env")
load_dotenv(MANIM_ROOT / ".env")

from app.beat_compiler import compile_scene, generate_scene_code, patch_scene_code, starter_scene_code  # noqa: E402
from app.openai_service import OpenAIService  # noqa: E402
from app.project_store import ProjectStore  # noqa: E402
from app.renderer import render_scene  # noqa: E402
from app.script_parser import parse_script  # noqa: E402

store = ProjectStore()


def _resolve_and_prefetch(project: dict) -> dict:
    from visual_library import prefetch_beat_visuals  # noqa: E402
    from visual_resolver import resolve_project  # noqa: E402

    project = resolve_project(project)
    for beat in project.get("beats", []):
        prefetch_beat_visuals(beat)
    return project


def _resolve_icon_descriptions(beats: list[dict]) -> list[dict]:
    from app.icon_resolver import beats_need_icon_resolution, resolve_beat_icons  # noqa: E402

    if not beats_need_icon_resolution(beats):
        return beats
    try:
        ai = _openai()
        return resolve_beat_icons(beats, ai)
    except Exception:
        return beats


def _prepare_beats(beats: list[dict]) -> list[dict]:
    from app.icon_resolver import beats_need_icon_resolution, validate_icon_refs  # noqa: E402

    if beats_need_icon_resolution(beats):
        beats = _resolve_icon_descriptions(beats)
    else:
        beats = validate_icon_refs(beats)
    return beats


def _write_scene_code(project_id: str, code: str) -> Path:
    scene_path = store.scene_path(project_id)
    scene_path.write_text(patch_scene_code(code))
    return scene_path


def _render_project(
    project_id: str,
    project: dict,
    *,
    quality: str = "-ql",
    skip_compile: bool = False,
) -> Path:
    scene_path = store.scene_path(project_id)
    if skip_compile and scene_path.exists():
        source = scene_path.read_text()
        patched = patch_scene_code(source)
        if patched != source:
            scene_path.write_text(patched)
    if not skip_compile and not project.get("code_customized"):
        compile_scene(project, scene_path)
    elif not scene_path.exists():
        code = generate_scene_code(project) if project.get("beats") else starter_scene_code()
        scene_path.write_text(code)
    if quality == "-qh":
        mp4 = store.export_path(project_id)
    else:
        mp4 = store.render_path(project_id)
    render_scene(scene_path, output_mp4=mp4, quality=quality)
    return mp4


def _read_scene_code(project_id: str, project: dict) -> dict:
    scene_path = store.scene_path(project_id)
    if scene_path.exists():
        return {
            "code": scene_path.read_text(),
            "source": "file",
            "code_customized": project.get("code_customized", False),
        }
    if project.get("beats"):
        code = generate_scene_code(project)
    else:
        code = starter_scene_code()
    scene_path.write_text(code)
    return {"code": code, "source": "generated", "code_customized": False}

app = FastAPI(title="Manimations Studio", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def _openai() -> OpenAIService:
    try:
        return OpenAIService()
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


class ChatRequest(BaseModel):
    message: str


class CreateProjectRequest(BaseModel):
    name: str = "Untitled"


class RevertRequest(BaseModel):
    snapshot_id: str


class ScriptRequest(BaseModel):
    script: str
    use_ai: bool = False


class CodeRequest(BaseModel):
    code: str
    render: bool = True


class RenderRequest(BaseModel):
    code: str | None = None
    from_beats: bool = False


class PythonToolRequest(BaseModel):
    code: str


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "openai_configured": bool(os.environ.get("OPENAI_API_KEY")),
        "data_dir": str(store.data_dir),
    }


@app.get("/api/projects")
def list_projects():
    return store.list_projects()


@app.post("/api/projects")
def create_project(body: CreateProjectRequest):
    return store.create_project(body.name)


@app.get("/api/projects/{project_id}")
def get_project(project_id: str):
    try:
        return store.load_project(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/projects/{project_id}/snapshots")
def list_snapshots(project_id: str):
    try:
        return store.list_snapshots(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/projects/{project_id}/revert")
def revert_project(project_id: str, body: RevertRequest):
    try:
        project = store.revert(project_id, body.snapshot_id)
        return {"project": project, "message": "Reverted successfully"}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/projects/{project_id}/chat")
def chat(project_id: str, body: ChatRequest):
    try:
        project = store.load_project(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    ai = _openai()
    try:
        result = ai.generate_project(
            body.message,
            current_project=project,
            chat_history=project.get("chat", [])[-20:],
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI error: {exc}") from exc

    assistant_msg = result.get("message", "Updated your animation.")
    incoming = result.get("project", {})

    if incoming.get("beats"):
        project["beats"] = _prepare_beats(incoming["beats"])
    if incoming.get("name"):
        project["name"] = incoming["name"]
    if incoming.get("style_pack"):
        project["style_pack"] = incoming["style_pack"]
    if "use_camera" in incoming:
        project["use_camera"] = incoming["use_camera"]

    project["code_customized"] = False
    project = _resolve_and_prefetch(project)

    project.setdefault("chat", []).append({"role": "user", "content": body.message})
    project["chat"].append({"role": "assistant", "content": assistant_msg})
    store.save_project(project, snapshot=True)

    render_error = None
    preview_url = None
    try:
        _render_project(project_id, project, quality="-ql")
        preview_url = f"/api/projects/{project_id}/preview"
    except Exception as exc:
        render_error = str(exc)

    return {
        "message": assistant_msg,
        "project": project,
        "preview_url": preview_url,
        "render_error": render_error,
    }


@app.post("/api/projects/{project_id}/script")
def apply_script(project_id: str, body: ScriptRequest):
    try:
        project = store.load_project(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    try:
        if body.use_ai:
            ai = _openai()
            parsed = ai.parse_script(body.script)
            beats = parsed.get("beats", [])
        else:
            parsed = parse_script(body.script)
            beats = parsed.get("beats", [])
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        if body.use_ai:
            raise HTTPException(status_code=502, detail=f"OpenAI error: {exc}") from exc
        raise HTTPException(status_code=400, detail=f"Script parse error: {exc}") from exc

    if not beats:
        raise HTTPException(status_code=400, detail="No beats found in script")

    try:
        project["beats"] = _prepare_beats(beats)
        if parsed.get("name"):
            project["name"] = parsed["name"]
        if parsed.get("style_pack"):
            project["style_pack"] = parsed["style_pack"]
        if "use_camera" in parsed:
            project["use_camera"] = parsed["use_camera"]
        project["code_customized"] = False
        project = _resolve_and_prefetch(project)
        project.setdefault("chat", []).append(
            {"role": "user", "content": "[Script import]\n" + body.script[:500]}
        )
        project["chat"].append(
            {"role": "assistant", "content": f"Imported {len(beats)} beat(s) from script."}
        )
        store.save_project(project, snapshot=True)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to save project: {exc}") from exc

    render_error = None
    preview_url = None
    try:
        _render_project(project_id, project, quality="-ql")
        preview_url = f"/api/projects/{project_id}/preview"
    except Exception as exc:
        render_error = str(exc)

    return {
        "message": f"Imported {len(beats)} beat(s) from script.",
        "project": project,
        "preview_url": preview_url,
        "render_error": render_error,
    }


TEMPLATE_PATH = MANIM_ROOT / "platform" / "assets" / "beat-script-template.md"


@app.get("/api/beat-script-template")
def get_beat_script_template():
    if not TEMPLATE_PATH.exists():
        raise HTTPException(status_code=404, detail="Template file not found")
    content = TEMPLATE_PATH.read_text()
    return {
        "filename": "beat-script-template.md",
        "content": content,
    }


@app.get("/api/beat-script-template/download")
def download_beat_script_template():
    if not TEMPLATE_PATH.exists():
        raise HTTPException(status_code=404, detail="Template file not found")
    return FileResponse(
        TEMPLATE_PATH,
        media_type="text/markdown",
        filename="beat-script-template.md",
        headers={"Content-Disposition": 'attachment; filename="beat-script-template.md"'},
    )


@app.post("/api/projects/{project_id}/render")
def render_project(project_id: str, body: RenderRequest | None = None):
    try:
        project = store.load_project(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    body = body or RenderRequest()
    scene_path = store.scene_path(project_id)

    if body.code is not None:
        if "class " not in body.code or "construct" not in body.code:
            raise HTTPException(
                status_code=400,
                detail="Code must define a Scene class with a construct() method.",
            )
        _write_scene_code(project_id, body.code)
        project["code_customized"] = True
        store.save_project(project, snapshot=False)
        skip = True
    elif body.from_beats:
        if not project.get("beats"):
            raise HTTPException(status_code=400, detail="No beats to compile.")
        project = _resolve_and_prefetch(project)
        compile_scene(project, scene_path)
        project["code_customized"] = False
        store.save_project(project, snapshot=False)
        skip = True
    else:
        skip = project.get("code_customized", False)
        if not skip and project.get("beats"):
            project = _resolve_and_prefetch(project)
            store.save_project(project, snapshot=False)

    try:
        _render_project(project_id, project, quality="-ql", skip_compile=skip)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "preview_url": f"/api/projects/{project_id}/preview",
        "code_customized": project.get("code_customized", False),
    }


@app.get("/api/projects/{project_id}/code")
def get_project_code(project_id: str):
    try:
        project = store.load_project(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _read_scene_code(project_id, project)


@app.put("/api/projects/{project_id}/code")
def save_project_code(project_id: str, body: CodeRequest):
    try:
        project = store.load_project(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    if "class " not in body.code or "construct" not in body.code:
        raise HTTPException(
            status_code=400,
            detail="Code must define a Scene class with a construct() method.",
        )

    _write_scene_code(project_id, body.code)
    project["code_customized"] = True
    store.save_project(project, snapshot=True)

    render_error = None
    preview_url = None
    if body.render:
        try:
            _render_project(project_id, project, quality="-ql", skip_compile=True)
            preview_url = f"/api/projects/{project_id}/preview"
        except Exception as exc:
            render_error = str(exc)

    return {
        "message": "Code saved.",
        "code_customized": True,
        "preview_url": preview_url,
        "render_error": render_error,
    }


@app.post("/api/projects/{project_id}/code/regenerate")
def regenerate_project_code(project_id: str):
    """Rebuild scene code from beats JSON (discards manual edits)."""
    try:
        project = store.load_project(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    if not project.get("beats"):
        raise HTTPException(status_code=400, detail="No beats to regenerate from.")

    project = _resolve_and_prefetch(project)
    project["code_customized"] = False
    code = generate_scene_code(project)
    store.scene_path(project_id).write_text(code)
    store.save_project(project, snapshot=True)

    return {"code": code, "code_customized": False, "message": "Regenerated from beats."}


@app.post("/api/python/format")
def format_python(body: PythonToolRequest):
    import ast

    try:
        from app.beat_compiler import _format_python

        formatted = _format_python(body.code)
        ast.parse(formatted)
        return {"code": formatted}
    except SyntaxError as exc:
        raise HTTPException(status_code=400, detail=f"Syntax error: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/python/lint")
def lint_python(body: PythonToolRequest):
    import ast

    diagnostics: list[dict] = []
    try:
        ast.parse(body.code)
    except SyntaxError as exc:
        diagnostics.append(
            {
                "line": exc.lineno or 1,
                "column": exc.offset or 1,
                "end_line": exc.lineno or 1,
                "end_column": (exc.offset or 1) + 1,
                "message": exc.msg,
                "severity": "error",
            }
        )
    return {"diagnostics": diagnostics}


@app.post("/api/projects/{project_id}/export")
def export_project(project_id: str, body: RenderRequest | None = None):
    """Render 1080p60 and prepare HD download."""
    try:
        project = store.load_project(project_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    body = body or RenderRequest()
    scene_path = store.scene_path(project_id)
    if not project.get("beats") and not scene_path.exists() and body.code is None:
        raise HTTPException(status_code=400, detail="No beats or scene code to export.")

    if body.code is not None:
        if "class " not in body.code or "construct" not in body.code:
            raise HTTPException(
                status_code=400,
                detail="Code must define a Scene class with a construct() method.",
            )
        _write_scene_code(project_id, body.code)
        project["code_customized"] = True
        store.save_project(project, snapshot=False)
        skip = True
    elif body.from_beats:
        if not project.get("beats"):
            raise HTTPException(status_code=400, detail="No beats to compile.")
        project = _resolve_and_prefetch(project)
        compile_scene(project, scene_path)
        project["code_customized"] = False
        store.save_project(project, snapshot=False)
        skip = True
    else:
        skip = project.get("code_customized", False)
        if not skip and project.get("beats"):
            project = _resolve_and_prefetch(project)
            store.save_project(project, snapshot=False)

    try:
        _render_project(project_id, project, quality="-qh", skip_compile=skip)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "download_url": f"/api/projects/{project_id}/download",
        "quality": "1080p60",
    }


@app.get("/api/projects/{project_id}/preview")
def preview_video(project_id: str):
    mp4 = store.render_path(project_id)
    if not mp4.exists():
        raise HTTPException(status_code=404, detail="No preview yet")
    return FileResponse(mp4, media_type="video/mp4")


@app.get("/api/projects/{project_id}/download")
def download_video(project_id: str):
    mp4 = store.export_path(project_id)
    if not mp4.exists():
        raise HTTPException(
            status_code=404,
            detail="No HD export yet. Click Download 1080p60 first.",
        )
    project = store.load_project(project_id)
    safe_name = re.sub(r"[^\w\-]+", "_", project.get("name", "animation"))
    return FileResponse(
        mp4,
        media_type="video/mp4",
        filename=f"{safe_name}_1080p60.mp4",
        headers={"Content-Disposition": f'attachment; filename="{safe_name}_1080p60.mp4"'},
    )
