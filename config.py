"""Configuration management for the autonomous YouTube AI Agent."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    gemini_api_key: str
    gemini_model: str
    youtube_api_key: str
    youtube_region_code: str
    youtube_category_id: str
    youtube_max_results: int
    google_docs_credentials_path: str
    google_docs_folder_id: str | None
    telegram_bot_token: str
    telegram_chat_id: str
    default_niche: str
    output_dir: str
    log_level: str


def _required(name: str) -> str:
    """Return a required environment variable or raise a helpful error."""
    value = os.getenv(name, "").strip()
    invalid_values = {"", "changeme", "change_me", "replace_me", "none", "null"}
    if value.lower() in invalid_values or value.startswith("your_"):
        raise RuntimeError(f"{name} is required. Copy .env.example to .env and add a real value.")
    return value


def _int_env(name: str, default: int) -> int:
    """Read an integer environment variable with validation."""
    raw_value = os.getenv(name, str(default)).strip()
    try:
        return int(raw_value)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer, got {raw_value!r}.") from exc


def load_settings(env_file: str | Path = ".env") -> Settings:
    """Load settings from .env and environment variables."""
    load_dotenv(env_file)
    return Settings(
        gemini_api_key=_required("GEMINI_API_KEY"),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip(),
        youtube_api_key=_required("YOUTUBE_API_KEY"),
        youtube_region_code=os.getenv("YOUTUBE_REGION_CODE", "IN").strip(),
        youtube_category_id=os.getenv("YOUTUBE_CATEGORY_ID", "28").strip(),
        youtube_max_results=_int_env("YOUTUBE_MAX_RESULTS", 10),
        google_docs_credentials_path=_required("GOOGLE_DOCS_CREDENTIALS_PATH"),
        google_docs_folder_id=os.getenv("GOOGLE_DOCS_FOLDER_ID", "").strip() or None,
        telegram_bot_token=_required("TELEGRAM_BOT_TOKEN"),
        telegram_chat_id=_required("TELEGRAM_CHAT_ID"),
        default_niche=os.getenv(
            "DEFAULT_NICHE",
            "AI tools, technology, productivity, and online earning",
        ).strip(),
        output_dir=os.getenv("OUTPUT_DIR", "outputs").strip(),
        log_level=os.getenv("LOG_LEVEL", "INFO").strip(),
    )
