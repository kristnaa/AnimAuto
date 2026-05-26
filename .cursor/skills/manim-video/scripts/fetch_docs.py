#!/usr/bin/env python3
"""Fetch Manim CE docs into .cursor/skills/manim-video/reference/ and tutorials/."""

from __future__ import annotations

import html
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://docs.manim.community/en/stable"
SKILL_ROOT = Path(__file__).resolve().parents[1]

TUTORIAL_URLS = [
    ("quickstart", f"{BASE}/tutorials/quickstart.html"),
    ("building_blocks", f"{BASE}/tutorials/building_blocks.html"),
    ("output_and_config", f"{BASE}/tutorials/output_and_config.html"),
]

REFERENCE_SEED = f"{BASE}/reference.html"
USER_AGENT = "manimations-doc-fetch/1.0"
DELAY_SECONDS = 0.15


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")


def strip_tags(raw: str) -> str:
    raw = re.sub(r"(?is)<script.*?>.*?</script>", "", raw)
    raw = re.sub(r"(?is)<style.*?>.*?</style>", "", raw)
    raw = re.sub(r"(?is)<nav.*?>.*?</nav>", "", raw)
    raw = re.sub(r"(?is)<header.*?>.*?</header>", "", raw)
    raw = re.sub(r"(?is)<footer.*?>.*?</footer>", "", raw)
    raw = re.sub(r"(?is)<aside.*?>.*?</aside>", "", raw)
    text = re.sub(r"<br\s*/?>", "\n", raw, flags=re.I)
    text = re.sub(r"</(p|div|h[1-6]|li|tr|pre|blockquote)>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    lines = [line.rstrip() for line in text.splitlines()]
    cleaned: list[str] = []
    blank = False
    for line in lines:
        line = line.strip()
        if not line:
            if not blank:
                cleaned.append("")
                blank = True
            continue
        if line in {"Contents", "Back to top", "View this page", "Edit this page", "On this page"}:
            continue
        if line.startswith("Manim Community v"):
            continue
        cleaned.append(line)
        blank = False
    return "\n".join(cleaned).strip()


def extract_main_content(page_html: str) -> str:
    for pattern in (
        r'(?is)<article[^>]*>(.*?)</article>',
        r'(?is)<div[^>]*class="[^"]*bd-article[^"]*"[^>]*>(.*?)</div>',
        r'(?is)<div[^>]*role="main"[^>]*>(.*?)</div>',
        r'(?is)<div[^>]*class="[^"]*document[^"]*"[^>]*>(.*?)</div>',
    ):
        match = re.search(pattern, page_html)
        if match:
            return strip_tags(match.group(1))
    return strip_tags(page_html)


def discover_reference_links(seed_html: str) -> list[str]:
    links = set(
        urllib.parse.urljoin(REFERENCE_SEED, href)
        for href in re.findall(r'href="([^"]+)"', seed_html)
    )
    return sorted(
        link
        for link in links
        if "/en/stable/reference/" in link and link.endswith(".html")
    )


def reference_group(url: str) -> tuple[str, str]:
    """Return (category_dir, filename_stem) for a reference URL."""
    name = Path(urllib.parse.urlparse(url).path).stem
    parts = name.split(".")
    if len(parts) < 2 or parts[0] != "manim":
        return "utilities", name

    if parts[1] == "animation":
        sub = parts[2] if len(parts) > 3 else "core"
        return "animations", sub

    if parts[1] == "mobject":
        if len(parts) >= 4:
            sub = f"{parts[2]}_{parts[3]}"
        elif len(parts) == 3:
            sub = parts[2]
        else:
            sub = "core"
        return "mobjects", sub

    if parts[1] == "scene":
        sub = parts[2] if len(parts) > 2 else "core"
        return "scenes", sub

    if parts[1] == "camera":
        sub = parts[2] if len(parts) > 2 else "core"
        return "cameras", sub

    if parts[1] in {"_config", "utils"} or "config" in name:
        return "configuration", parts[-1]

    return "utilities", parts[1] if len(parts) > 1 else name


def append_reference_entry(path: Path, url: str, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = f"\n\n---\n\n## {title}\n\nSource: {url}\n\n{body}\n"
    if path.exists():
        path.write_text(path.read_text(encoding="utf-8") + entry, encoding="utf-8")
    else:
        header = f"# {path.stem.replace('_', ' ').title()}\n"
        path.write_text(header + entry, encoding="utf-8")


def fetch_tutorials() -> None:
    out_dir = SKILL_ROOT / "tutorials"
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, url in TUTORIAL_URLS:
        print(f"Tutorial: {name}")
        page = fetch(url)
        content = extract_main_content(page)
        (out_dir / f"{name}.md").write_text(
            f"# {name.replace('_', ' ').title()}\n\nSource: {url}\n\n{content}\n",
            encoding="utf-8",
        )
        time.sleep(DELAY_SECONDS)


def fetch_reference() -> None:
    ref_dir = SKILL_ROOT / "reference"
    ref_dir.mkdir(parents=True, exist_ok=True)

    seed_html = fetch(REFERENCE_SEED)
    links = discover_reference_links(seed_html)
    print(f"Found {len(links)} reference pages")

    index_lines = [
        "# Manim CE Reference Index",
        "",
        f"Source seed: {REFERENCE_SEED}",
        "",
        "Grouped files live in subfolders. Read the relevant group file for API details.",
        "",
    ]
    counts: dict[str, int] = {}

    for i, url in enumerate(links, 1):
        category, stem = reference_group(url)
        counts[category] = counts.get(category, 0) + 1
        print(f"[{i}/{len(links)}] {category}/{stem}: {Path(url).name}")

        try:
            page = fetch(url)
        except urllib.error.HTTPError as exc:
            print(f"  skip HTTP {exc.code}")
            continue

        body = extract_main_content(page)
        title_match = re.search(r"(?is)<title>(.*?)</title>", page)
        title = strip_tags(title_match.group(1)) if title_match else Path(url).stem
        title = title.split("—")[0].strip() or Path(url).stem

        out_path = ref_dir / category / f"{stem}.md"
        append_reference_entry(out_path, url, title, body)
        index_lines.append(f"- [{title}]({category}/{stem}.md) — `{url}`")
        time.sleep(DELAY_SECONDS)

    index_lines.extend(["", "## Counts", ""])
    for category, count in sorted(counts.items()):
        index_lines.append(f"- **{category}**: {count} pages")

    (ref_dir / "INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


def main() -> None:
    print(f"Writing docs to {SKILL_ROOT}")
    fetch_tutorials()
    fetch_reference()
    print("Done.")


if __name__ == "__main__":
    main()
