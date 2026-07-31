"""Telegram Bot API notifications."""

from __future__ import annotations

import logging

import requests

logger = logging.getLogger(__name__)


class TelegramService:
    """Send generated YouTube packages to a Telegram chat."""

    def __init__(self, bot_token: str, chat_id: str) -> None:
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    def send_message(self, message: str) -> None:
        """Send a text message to Telegram and raise if delivery fails."""
        logger.info("Sending Telegram notification")
        try:
            response = requests.post(
                self.api_url,
                json={"chat_id": self.chat_id, "text": message, "disable_web_page_preview": False},
                timeout=30,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.exception("Telegram notification failed")
            raise RuntimeError(f"Telegram notification failed: {exc}") from exc
        logger.info("Telegram notification sent")
