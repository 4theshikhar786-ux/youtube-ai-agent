"""Gemini API wrapper for content generation."""

from __future__ import annotations

import logging

import google.generativeai as genai

logger = logging.getLogger(__name__)


class GeminiClient:
    """Small production-friendly wrapper around Gemini text generation."""

    def __init__(self, api_key: str, model_name: str) -> None:
        logger.info("Initializing Gemini model: %s", model_name)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate text with Gemini and return a stripped response."""
        logger.info("Generating content with Gemini")
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"temperature": temperature},
            )
        except Exception as exc:
            logger.exception("Gemini content generation failed")
            raise RuntimeError(f"Gemini content generation failed: {exc}") from exc

        text = getattr(response, "text", "").strip()
        if not text:
            logger.error("Gemini returned an empty response")
            raise RuntimeError("Gemini returned an empty response.")
        return text
