"""CLI entrypoint for the fully autonomous YouTube AI Agent."""

from __future__ import annotations

import argparse
import logging
import sys
from typing import TYPE_CHECKING

from logging_config import configure_logging

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from agent import YouTubeAIAgent


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the autonomous Gemini-powered YouTube AI Agent.")
    parser.add_argument("--niche", help="Video niche or audience to target. Defaults to DEFAULT_NICHE in .env.")
    return parser.parse_args()


def build_agent() -> tuple["YouTubeAIAgent", str]:
    """Create configured service clients and return the agent plus default niche."""
    from agent import YouTubeAIAgent
    from config import load_settings
    from docs_service import GoogleDocsService
    from gemini_client import GeminiClient
    from telegram_service import TelegramService
    from youtube_service import YouTubeTrendService

    settings = load_settings()
    agent = YouTubeAIAgent(
        gemini=GeminiClient(settings.gemini_api_key, settings.gemini_model),
        trends=YouTubeTrendService(
            api_key=settings.youtube_api_key,
            region_code=settings.youtube_region_code,
            category_id=settings.youtube_category_id,
            max_results=settings.youtube_max_results,
        ),
        docs=GoogleDocsService(
            service_account_file=settings.google_docs_credentials_path,
            folder_id=settings.google_docs_folder_id,
        ),
        telegram=TelegramService(settings.telegram_bot_token, settings.telegram_chat_id),
        output_dir=settings.output_dir,
    )
    return agent, settings.default_niche


def main() -> None:
    """Run the autonomous workflow."""
    configure_logging()
    args = parse_args()
    logger.info("Starting YouTube AI Agent CLI")
    try:
        agent, default_niche = build_agent()
        package, output_path = agent.run(args.niche or default_niche)
    except ModuleNotFoundError as exc:
        missing_package = exc.name or "a required dependency"
        logger.error("Missing dependency: %s", missing_package)
        print(f"Missing dependency: {missing_package}. Run: pip install -r requirements.txt", file=sys.stderr)
        raise SystemExit(1) from exc
    except RuntimeError as exc:
        logger.error("Configuration error: %s", exc)
        print(f"Configuration error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    logger.info("YouTube AI Agent completed successfully")
    print("YouTube AI Agent completed successfully.")
    print(f"Topic: {package.topic}")
    print(f"Google Doc: {package.google_doc_url}")
    print(f"Markdown: {output_path}")


if __name__ == "__main__":
    main()
