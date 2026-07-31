"""YouTube Data API integration for discovering trending topics."""

from __future__ import annotations

import logging

from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

from models import TrendingVideo


class YouTubeTrendService:
    """Fetch trending YouTube videos for a target region and category."""

    def __init__(self, api_key: str, region_code: str, category_id: str, max_results: int) -> None:
        self.region_code = region_code
        self.category_id = category_id
        self.max_results = max_results
        logger.info("Initializing YouTube Data API client for region=%s category=%s", region_code, category_id)
        self.youtube = build("youtube", "v3", developerKey=api_key)

    def fetch_trending_videos(self) -> list[TrendingVideo]:
        """Return the currently most popular videos for the configured market."""
        logger.info("Fetching trending YouTube videos")
        request = self.youtube.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            regionCode=self.region_code,
            videoCategoryId=self.category_id,
            maxResults=self.max_results,
        )
        try:
            response = request.execute()
        except Exception as exc:
            logger.exception("YouTube trending video lookup failed")
            raise RuntimeError(f"YouTube trending video lookup failed: {exc}") from exc
        videos: list[TrendingVideo] = []
        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            statistics = item.get("statistics", {})
            video_id = item.get("id", "")
            videos.append(
                TrendingVideo(
                    title=snippet.get("title", "Untitled"),
                    channel_title=snippet.get("channelTitle", "Unknown channel"),
                    video_id=video_id,
                    url=f"https://www.youtube.com/watch?v={video_id}",
                    view_count=int(statistics.get("viewCount", 0)),
                )
            )
        logger.info("Fetched %s trending YouTube videos", len(videos))
        return videos
