"""Pydantic models for theme CRUD and uploads."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

BackgroundKind = Literal["image", "gif", "video"]

ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/webp", "image/gif"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm"}
MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_VIDEO_BYTES = 100 * 1024 * 1024


class TypographyStyle(BaseModel):
    font: str = "Inter"
    font_size: int = 28
    color: str = "#FFFFFF"
    weight: str = "BOLD"
    cursor: str | None = None


class TypographySpec(BaseModel):
    heading: TypographyStyle = Field(
        default_factory=lambda: TypographyStyle(
            font_size=48, color="#FFFFFF", cursor="#FFFFFF"
        )
    )
    subheading: TypographyStyle = Field(
        default_factory=lambda: TypographyStyle(font_size=36, color="#FFFFFF", cursor="#FFEB3B")
    )
    paragraph: TypographyStyle = Field(
        default_factory=lambda: TypographyStyle(font_size=28, color="#000000", cursor="#FFEB3B")
    )
    code: TypographyStyle = Field(
        default_factory=lambda: TypographyStyle(
            font="Courier New", font_size=22, color="#abb2bf", weight="NORMAL", cursor=None
        )
    )


class PaletteSpec(BaseModel):
    card_fill: str = "#FFFFFF"
    card_stroke: str = "#888888"
    accent: str = "#FFEB3B"
    emphasis_red: str = "#FC6255"
    label_color: str = "#FFEB3B"
    code_bg: str = "#282c34"
    code_bg_deep: str = "#21252b"
    code_border: str = "#3e4451"
    code_text: str = "#abb2bf"
    code_keyword: str = "#c678dd"
    code_func: str = "#e06c75"
    code_string: str = "#98c379"
    code_number: str = "#d19a66"
    code_cursor: str = "#528bff"
    code_highlight: str = "#528bff"
    code_error_highlight: str = "#e06c75"
    code_run_green: str = "#98c379"
    code_run_green_dark: str = "#6e9455"


class ThemeCreateBody(BaseModel):
    name: str
    description: str = ""
    style_pack: str = "course_clean"
    background_kind: BackgroundKind = "image"
    background_loop: bool = True
    typography: TypographySpec = Field(default_factory=TypographySpec)
    palette: PaletteSpec | None = None


class ThemeUpdateBody(BaseModel):
    name: str | None = None
    description: str | None = None
    style_pack: str | None = None
    background_kind: BackgroundKind | None = None
    background_loop: bool | None = None
    typography: TypographySpec | None = None
    palette: PaletteSpec | None = None


class ThemeSummary(BaseModel):
    id: str
    name: str
    description: str
    style_pack: str
    background_kind: BackgroundKind
    background_loop: bool
    preview_url: str
    is_builtin: bool = False


class ThemeDetail(ThemeSummary):
    typography: TypographySpec
    palette: PaletteSpec | None = None
    created_at: str
    updated_at: str
