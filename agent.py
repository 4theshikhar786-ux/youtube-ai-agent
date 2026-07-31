"""Autonomous orchestration for YouTube video package generation."""

from __future__ import annotations

import logging
from dataclasses import replace

from docs_service import GoogleDocsService
from gemini_client import GeminiClient
from models import TrendingVideo, YouTubePackage
from telegram_service import TelegramService
from utils import build_markdown, ensure_hashtag_limit, format_trending_references, save_markdown
from youtube_service import YouTubeTrendService

logger = logging.getLogger(__name__)


class YouTubeAIAgent:
    """Fully autonomous YouTube AI Agent powered by Gemini and platform APIs."""

    def __init__(
        self,
        gemini: GeminiClient,
        trends: YouTubeTrendService,
        docs: GoogleDocsService,
        telegram: TelegramService,
        output_dir: str,
    ) -> None:
        self.gemini = gemini
        self.trends = trends
        self.docs = docs
        self.telegram = telegram
        self.output_dir = output_dir

    def _trending_context(self, videos: list[TrendingVideo]) -> str:
        """Return compact trend context for Gemini prompts."""
        return format_trending_references(videos[:10])

    def generate_topic(self, niche: str, videos: list[TrendingVideo]) -> str:
        """Generate a viral topic based on live trending YouTube videos."""
        logger.info("Generating viral topic for niche: %s", niche)
        return self.gemini.generate(
            f"""
            You are a YouTube growth strategist for Hindi creators.
            Niche: {niche}
            Current trending YouTube references:
            {self._trending_context(videos)}

            Create one original viral YouTube topic inspired by these trends.
            Requirements:
            - Useful for Indian/Hindi viewers
            - Curiosity-driven and specific
            - Under 18 words
            - Do not copy any trending title exactly
            Return only the topic.
            """,
            temperature=0.9,
        )

    def write_script(self, topic: str) -> str:
        """Write a long-form Hindi YouTube script."""
        logger.info("Generating 2000-word Hindi script")
        return self.gemini.generate(
            f"""
            Write a complete 2000-word Hindi YouTube script on this topic: {topic}

            Requirements:
            - Natural conversational Hindi with simple words.
            - Strong hook in the first 20 seconds.
            - Clear intro, story arc, sections, examples, transitions, and conclusion.
            - Retention boosters every 60-90 seconds.
            - Pattern interrupts and curiosity loops.
            - Practical takeaways for viewers.
            - Like, comment, subscribe, and share CTA.
            - No markdown table.
            """,
            temperature=0.75,
        )

    def generate_seo_title(self, topic: str) -> str:
        """Generate a click-worthy SEO title."""
        logger.info("Generating SEO title")
        return self.gemini.generate(
            f"Generate one SEO-optimized Hindi/English YouTube title for: {topic}. Keep it under 70 characters.",
            temperature=0.8,
        )

    def generate_seo_description(self, topic: str) -> str:
        """Generate an SEO-rich YouTube description."""
        logger.info("Generating SEO description")
        return self.gemini.generate(
            f"""
            Write an SEO-optimized YouTube description in Hindi for: {topic}.
            Include:
            - 2 compelling opening lines
            - keyword-rich summary
            - viewer benefit
            - CTA
            - 8 relevant keywords naturally included
            Keep it between 220 and 320 words.
            """,
            temperature=0.7,
        )

    def generate_hashtags(self, topic: str) -> list[str]:
        """Generate exactly 30 normalized YouTube hashtags."""
        logger.info("Generating hashtags")
        raw_hashtags = self.gemini.generate(
            f"Generate exactly 30 SEO hashtags for a Hindi YouTube video on: {topic}. Return one hashtag per line.",
            temperature=0.7,
        )
        return ensure_hashtag_limit(raw_hashtags, limit=30)

    def generate_thumbnail_prompt(self, topic: str) -> str:
        """Generate a detailed AI image prompt for the YouTube thumbnail."""
        logger.info("Generating thumbnail prompt")
        return self.gemini.generate(
            f"""
            Create a detailed thumbnail image prompt for this YouTube topic: {topic}.
            Include composition, subject, expression, props, background, colors,
            lighting, contrast, readable Hindi/English text overlay, and 16:9 YouTube style.
            Make it suitable for Midjourney, DALL-E, Gemini image tools, or Stable Diffusion.
            """,
            temperature=0.85,
        )

    def create_package(self, niche: str) -> YouTubePackage:
        """Generate the complete package before exports and notifications."""
        logger.info("Creating YouTube package")
        videos = self.trends.fetch_trending_videos()
        if not videos:
            raise RuntimeError("No trending videos returned by YouTube Data API.")
        topic = self.generate_topic(niche, videos)
        return YouTubePackage(
            niche=niche,
            trending_references=videos,
            topic=topic,
            script=self.write_script(topic),
            title=self.generate_seo_title(topic),
            description=self.generate_seo_description(topic),
            hashtags=self.generate_hashtags(topic),
            thumbnail_prompt=self.generate_thumbnail_prompt(topic),
        )

    def run(self, niche: str) -> tuple[YouTubePackage, str]:
        """Create content, save locally, export to Google Docs, and notify Telegram."""
        logger.info("Starting autonomous YouTube AI workflow")
        package = self.create_package(niche)
        initial_markdown = build_markdown(package)
        doc_url = self.docs.create_document(package.title, initial_markdown)
        package = replace(package, google_doc_url=doc_url)
        final_markdown = build_markdown(package)
        output_path = save_markdown(final_markdown, self.output_dir, package.topic)

        self.telegram.send_message(
            "✅ YouTube AI Agent completed a new content package.\n\n"
            f"Topic: {package.topic}\n"
            f"SEO Title: {package.title}\n"
            f"Google Doc: {package.google_doc_url}\n"
            f"Local Markdown: {output_path}"
        )
        logger.info("Autonomous YouTube AI workflow completed")
        return package, str(output_path)
