"""SQLite-backed global theme library with uploaded backgrounds."""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.theme_schema import (
    ALLOWED_IMAGE_TYPES,
    ALLOWED_VIDEO_TYPES,
    MAX_IMAGE_BYTES,
    MAX_VIDEO_BYTES,
    PaletteSpec,
    ThemeCreateBody,
    ThemeDetail,
    ThemeSummary,
    ThemeUpdateBody,
    TypographySpec,
)

MANIM_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATA_DIR = Path(
    os.environ.get("MANIMATIONS_DATA_DIR", Path.home() / "manimations-studio")
)
BUILTIN_ORANGE_ID = "builtin_orange"
BUILTIN_REPO_BG = MANIM_ROOT / "background" / "orange_theme_BG.png"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_typography_dict() -> dict:
    return TypographySpec().model_dump()


def default_palette_dict() -> dict:
    return PaletteSpec().model_dump()


class ThemeStore:
    def __init__(self, data_dir: Path | None = None):
        self.data_dir = Path(data_dir or DEFAULT_DATA_DIR)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.themes_dir = self.data_dir / "themes"
        self.themes_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "studio.db"
        self._init_db()
        self._seed_builtin()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS themes (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    style_pack TEXT NOT NULL DEFAULT 'course_clean',
                    background_kind TEXT NOT NULL DEFAULT 'image',
                    background_filename TEXT,
                    background_repo_path TEXT,
                    background_loop INTEGER NOT NULL DEFAULT 1,
                    typography_json TEXT NOT NULL,
                    palette_json TEXT,
                    is_builtin INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def _seed_builtin(self) -> None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id FROM themes WHERE id = ?", (BUILTIN_ORANGE_ID,)
            ).fetchone()
            if row:
                return
            now = _now_iso()
            conn.execute(
                """
                INSERT INTO themes (
                    id, name, description, style_pack, background_kind,
                    background_filename, background_repo_path, background_loop,
                    typography_json, palette_json, is_builtin, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    BUILTIN_ORANGE_ID,
                    "Orange Course",
                    "Default orange gradient background with course typography.",
                    "course_clean",
                    "image",
                    None,
                    "background/orange_theme_BG.png",
                    1,
                    json.dumps(default_typography_dict()),
                    json.dumps(default_palette_dict()),
                    1,
                    now,
                    now,
                ),
            )

    def _theme_dir(self, theme_id: str) -> Path:
        return self.themes_dir / theme_id

    def _background_file(self, theme_id: str, filename: str | None) -> Path | None:
        if not filename:
            return None
        return self._theme_dir(theme_id) / filename

    def resolve_background_path(self, row: sqlite3.Row | dict) -> Path:
        data = dict(row)
        repo_path = data.get("background_repo_path")
        if repo_path:
            path = MANIM_ROOT / repo_path
            if path.is_file():
                return path
        filename = data.get("background_filename")
        if filename:
            uploaded = self._background_file(data["id"], filename)
            if uploaded and uploaded.is_file():
                return uploaded
        return BUILTIN_REPO_BG

    def _row_to_summary(self, row: sqlite3.Row) -> ThemeSummary:
        data = dict(row)
        return ThemeSummary(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            style_pack=data["style_pack"],
            background_kind=data["background_kind"],
            background_loop=bool(data["background_loop"]),
            preview_url=f"/api/themes/{data['id']}/background",
            is_builtin=bool(data["is_builtin"]),
        )

    def _row_to_detail(self, row: sqlite3.Row) -> ThemeDetail:
        data = dict(row)
        palette_raw = data.get("palette_json")
        return ThemeDetail(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            style_pack=data["style_pack"],
            background_kind=data["background_kind"],
            background_loop=bool(data["background_loop"]),
            preview_url=f"/api/themes/{data['id']}/background",
            is_builtin=bool(data["is_builtin"]),
            typography=TypographySpec(**json.loads(data["typography_json"])),
            palette=PaletteSpec(**json.loads(palette_raw)) if palette_raw else None,
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )

    def list_themes(self) -> list[ThemeSummary]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM themes ORDER BY is_builtin DESC, name COLLATE NOCASE"
            ).fetchall()
        return [self._row_to_summary(r) for r in rows]

    def get_theme(self, theme_id: str) -> ThemeDetail | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM themes WHERE id = ?", (theme_id,)
            ).fetchone()
        return self._row_to_detail(row) if row else None

    def get_theme_row(self, theme_id: str) -> dict | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM themes WHERE id = ?", (theme_id,)
            ).fetchone()
        return dict(row) if row else None

    def theme_exists(self, theme_id: str) -> bool:
        return self.get_theme_row(theme_id) is not None

    def theme_for_render(self, theme_id: str) -> dict[str, Any]:
        row = self.get_theme_row(theme_id or BUILTIN_ORANGE_ID)
        if not row:
            row = self.get_theme_row(BUILTIN_ORANGE_ID)
        assert row is not None
        bg_path = self.resolve_background_path(row)
        typography = json.loads(row["typography_json"])
        palette = json.loads(row["palette_json"]) if row.get("palette_json") else None
        return {
            "id": row["id"],
            "style_pack": row["style_pack"],
            "background": {
                "kind": row["background_kind"],
                "path": str(bg_path.resolve()),
                "loop": bool(row["background_loop"]),
            },
            "typography": typography,
            "palette": palette or default_palette_dict(),
        }

    @staticmethod
    def _detect_kind(content_type: str, filename: str) -> str:
        if content_type in ALLOWED_VIDEO_TYPES or filename.lower().endswith(
            (".mp4", ".webm")
        ):
            return "video"
        if content_type == "image/gif" or filename.lower().endswith(".gif"):
            return "gif"
        return "image"

    @staticmethod
    def _validate_upload(content_type: str, size: int, kind: str) -> None:
        if kind == "video":
            if content_type not in ALLOWED_VIDEO_TYPES and not content_type.startswith(
                "video/"
            ):
                raise ValueError(f"Unsupported video type: {content_type}")
            if size > MAX_VIDEO_BYTES:
                raise ValueError("Video must be 100MB or smaller")
        else:
            if content_type not in ALLOWED_IMAGE_TYPES:
                raise ValueError(f"Unsupported image type: {content_type}")
            if size > MAX_IMAGE_BYTES:
                raise ValueError("Image must be 10MB or smaller")

    def create_theme(
        self,
        body: ThemeCreateBody,
        file_bytes: bytes | None = None,
        content_type: str = "",
        filename: str = "",
    ) -> ThemeDetail:
        theme_id = str(uuid.uuid4())[:8]
        now = _now_iso()
        bg_kind = body.background_kind
        bg_filename = None
        bg_repo = None

        if file_bytes:
            bg_kind = self._detect_kind(content_type, filename)
            self._validate_upload(content_type, len(file_bytes), bg_kind)
            ext = Path(filename).suffix.lower() or (
                ".mp4" if bg_kind == "video" else ".png"
            )
            bg_filename = f"background{ext}"
            tdir = self._theme_dir(theme_id)
            tdir.mkdir(parents=True, exist_ok=True)
            (tdir / bg_filename).write_bytes(file_bytes)

        palette_json = (
            body.palette.model_dump_json() if body.palette else json.dumps(default_palette_dict())
        )

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO themes (
                    id, name, description, style_pack, background_kind,
                    background_filename, background_repo_path, background_loop,
                    typography_json, palette_json, is_builtin, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)
                """,
                (
                    theme_id,
                    body.name.strip(),
                    body.description.strip(),
                    body.style_pack,
                    bg_kind,
                    bg_filename,
                    bg_repo,
                    int(body.background_loop),
                    body.typography.model_dump_json(),
                    palette_json,
                    now,
                    now,
                ),
            )
        detail = self.get_theme(theme_id)
        assert detail is not None
        return detail

    def update_theme(
        self,
        theme_id: str,
        body: ThemeUpdateBody,
        file_bytes: bytes | None = None,
        content_type: str = "",
        filename: str = "",
    ) -> ThemeDetail:
        row = self.get_theme_row(theme_id)
        if not row:
            raise FileNotFoundError(f"Theme not found: {theme_id}")
        if bool(row["is_builtin"]) and body.name is not None:
            pass  # allow typography/palette edits on builtin? block name change only
        if bool(row["is_builtin"]) and file_bytes:
            raise ValueError("Cannot replace background on built-in theme")

        updates: dict[str, Any] = {"updated_at": _now_iso()}
        if body.name is not None:
            updates["name"] = body.name.strip()
        if body.description is not None:
            updates["description"] = body.description.strip()
        if body.style_pack is not None:
            updates["style_pack"] = body.style_pack
        if body.background_loop is not None:
            updates["background_loop"] = int(body.background_loop)
        if body.typography is not None:
            updates["typography_json"] = body.typography.model_dump_json()
        if body.palette is not None:
            updates["palette_json"] = body.palette.model_dump_json()
        if body.background_kind is not None:
            updates["background_kind"] = body.background_kind

        if file_bytes:
            bg_kind = self._detect_kind(content_type, filename)
            self._validate_upload(content_type, len(file_bytes), bg_kind)
            ext = Path(filename).suffix.lower() or (
                ".mp4" if bg_kind == "video" else ".png"
            )
            bg_filename = f"background{ext}"
            tdir = self._theme_dir(theme_id)
            tdir.mkdir(parents=True, exist_ok=True)
            for old in tdir.glob("background.*"):
                old.unlink(missing_ok=True)
            (tdir / bg_filename).write_bytes(file_bytes)
            updates["background_kind"] = bg_kind
            updates["background_filename"] = bg_filename
            updates["background_repo_path"] = None

        cols = ", ".join(f"{k} = ?" for k in updates)
        vals = list(updates.values()) + [theme_id]
        with self._connect() as conn:
            conn.execute(f"UPDATE themes SET {cols} WHERE id = ?", vals)

        detail = self.get_theme(theme_id)
        assert detail is not None
        return detail

    def delete_theme(self, theme_id: str) -> None:
        row = self.get_theme_row(theme_id)
        if not row:
            raise FileNotFoundError(f"Theme not found: {theme_id}")
        if bool(row["is_builtin"]):
            raise ValueError("Cannot delete built-in theme")
        with self._connect() as conn:
            conn.execute("DELETE FROM themes WHERE id = ?", (theme_id,))
        tdir = self._theme_dir(theme_id)
        if tdir.exists():
            shutil.rmtree(tdir)

    def background_media_type(self, theme_id: str) -> str:
        row = self.get_theme_row(theme_id)
        if not row:
            raise FileNotFoundError(f"Theme not found: {theme_id}")
        kind = row["background_kind"]
        if kind == "video":
            return "video/mp4"
        if kind == "gif":
            return "image/gif"
        return "image/png"
