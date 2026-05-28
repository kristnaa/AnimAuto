"""OpenAI integration for beat generation and edits."""

from __future__ import annotations

import json
import os
import re
from typing import Any

from openai import OpenAI

from app.script_parser import parse_script as deterministic_parse_script
from app.skill_context import (
    build_chat_system_prompt,
    build_script_system_prompt,
    normalize_project,
)

_CODE_DEMO_INTENT = re.compile(
    r"code\s*demo|write\s+(?:a\s+)?function|python\s+function|run\s+code|"
    r"add(?:ing)?\s+\d+\s+number|show\s+(?:me\s+)?code|snippet",
    re.I,
)


class OpenAIService:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY is not set")
        self.client = OpenAI(api_key=key)
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

    def generate_project(
        self,
        user_message: str,
        current_project: dict | None = None,
        chat_history: list[dict] | None = None,
    ) -> dict[str, Any]:
        messages: list[dict] = [{"role": "system", "content": build_chat_system_prompt()}]

        if current_project and current_project.get("beats"):
            messages.append(
                {
                    "role": "system",
                    "content": f"Current project state:\n{json.dumps(current_project, indent=2)}",
                }
            )

        for msg in chat_history or []:
            messages.append({"role": msg["role"], "content": msg["content"]})

        if _CODE_DEMO_INTENT.search(user_message):
            messages.append(
                {
                    "role": "system",
                    "content": (
                        "This request needs a code_demo beat: set type to code_demo, "
                        "layout to code_full_card, populate code_lines (Python source lines), "
                        "code_result (success or error), and code_output (stdout text). "
                        "Do not use card_lines for code."
                    ),
                }
            )

        messages.append({"role": "user", "content": user_message})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        raw = response.choices[0].message.content or "{}"
        data = json.loads(raw)

        if "project" in data and isinstance(data["project"], dict):
            data["project"] = normalize_project(data["project"])

        if current_project and "project" in data:
            merged = dict(current_project)
            incoming = data["project"]
            if incoming.get("name"):
                merged["name"] = incoming["name"]
            if incoming.get("style_pack"):
                merged["style_pack"] = incoming["style_pack"]
            if "use_camera" in incoming:
                merged["use_camera"] = incoming["use_camera"]
            if incoming.get("beats"):
                merged["beats"] = incoming["beats"]
            merged["id"] = current_project.get("id", merged.get("id"))
            data["project"] = merged
        elif "project" in data and current_project:
            data["project"]["id"] = current_project.get("id")

        return data

    def parse_script(self, script_text: str) -> dict[str, Any]:
        """Use OpenAI + skill context to produce beats, then compile via script parser when possible."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": build_script_system_prompt()},
                {
                    "role": "user",
                    "content": (
                        "Convert the following into a complete render-ready beat script.\n\n"
                        f"---\n{script_text}"
                    ),
                },
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        raw = response.choices[0].message.content or "{}"
        data = json.loads(raw)

        if data.get("script_markdown"):
            parsed = deterministic_parse_script(data["script_markdown"])
            for key in ("name", "style_pack", "use_camera"):
                if key in data:
                    parsed[key] = data[key]
            return parsed

        if "beats" in data:
            return normalize_project(data)

        if "project" in data and isinstance(data["project"], dict):
            project = data["project"]
            if project.get("script_markdown"):
                parsed = deterministic_parse_script(project["script_markdown"])
                for key in ("name", "style_pack", "use_camera"):
                    if key in project:
                        parsed[key] = project[key]
                return parsed
            return normalize_project(project)

        raise ValueError("AI response missing script_markdown or beats")

    def resolve_icon_descriptions(self, requests: list[dict[str, Any]]) -> dict[str, str]:
        """Map semantic icon descriptions to Iconify prefix:name refs."""
        from app.icon_resolver import ICONIFY_REF, ICON_RESOLVE_PROMPT

        payload = json.dumps({"icons": requests}, indent=2)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": ICON_RESOLVE_PROMPT},
                {"role": "user", "content": f"Resolve these icon requests:\n{payload}"},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        raw = response.choices[0].message.content or "{}"
        data = json.loads(raw)
        resolved = data.get("resolved") or {}
        if not isinstance(resolved, dict):
            return {}
        return {str(k): str(v) for k, v in resolved.items() if ICONIFY_REF.match(str(v))}
