"""Utility helpers for the autonomous YouTube AI Agent."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Iterable

from models import TrendingVideo, YouTubePackage


def slugify(value: str, max_length: int = 80) -> str:
    """Return a filesystem-friendly slug for generated output files."""
    value = value.strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    value = re.sub(r"[\s_-]+", "-", value, flags=re.UNICODE).strip("-")
    return value[:max_length].strip("-") or "youtube-video-idea"


def parse_numbered_lines(text: str) -> list[str]:
    """Extract clean items from numbered, bulleted, or plain line-based text."""
    items: list[str] = []
    for line in text.splitlines():
        cleaned = re.sub(r"^\s*(?:[-*•]|\d+[.)])\s*", "", line).strip()
        if cleaned:
            items.append(cleaned)
    return items


def ensure_hashtag_limit(raw_text: str, limit: int = 30) -> list[str]:
    """Normalize hashtag text and keep exactly the requested number when possible."""
    tags = []
    for item in parse_numbered_lines(raw_text):
        for token in item.split():
            cleaned = token.strip().strip(",")
            if cleaned:
                tags.append(cleaned if cleaned.startswith("#") else f"#{cleaned.lstrip('#')}")
    return list(dict.fromkeys(tags))[:limit]


def format_markdown_section(title: str, body: str | Iterable[str]) -> str:
    """Build a markdown section from a string or iterable of lines."""
    if isinstance(body, str):
        content = body.strip()
    else:
        content = "\n".join(str(item).strip() for item in body if str(item).strip())
    return f"## {title}\n\n{content}\n"


def format_trending_references(videos: list[TrendingVideo]) -> str:
    """Render trending videos as markdown bullet references."""
    lines = [
        f"- {video.title} — {video.channel_title} ({video.view_count:,} views): {video.url}"
        for video in videos
    ]
    return "\n".join(lines) if lines else "No trending videos found."


def build_markdown(package: YouTubePackage) -> str:
    """Convert the generated package into a clean markdown document."""
    sections = [
        "# YouTube Automation AI Agent Output\n",
        format_markdown_section("Niche", package.niche),
        format_markdown_section("Trending YouTube References", format_trending_references(package.trending_references)),
        format_markdown_section("Viral YouTube Topic", package.topic),
        format_markdown_section("SEO Title", package.title),
        format_markdown_section("SEO Description", package.description),
        format_markdown_section("30 Hashtags", package.hashtags),
        format_markdown_section("Thumbnail Prompt", package.thumbnail_prompt),
        format_markdown_section("2000-Word Hindi Script", package.script),
    ]
    if package.google_doc_url:
        sections.insert(2, format_markdown_section("Google Doc", package.google_doc_url))
    return "\n".join(sections)


def save_markdown(content: str, output_dir: str | Path, topic: str) -> Path:
    """Save markdown content in the output directory and return the file path."""
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_path = directory / f"{timestamp}-{slugify(topic)}.md"
    file_path.write_text(content.strip() + "\n", encoding="utf-8")
    return file_path
