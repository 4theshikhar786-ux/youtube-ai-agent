"""Data models used by the YouTube AI Agent."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TrendingVideo:
    """A trending YouTube video returned by the YouTube Data API."""

    title: str
    channel_title: str
    video_id: str
    url: str
    view_count: int = 0


@dataclass(frozen=True)
class YouTubePackage:
    """Complete content package generated for a YouTube video."""

    niche: str
    trending_references: list[TrendingVideo]
    topic: str
    script: str
    title: str
    description: str
    hashtags: list[str] = field(default_factory=list)
    thumbnail_prompt: str = ""
    google_doc_url: str | None = None
