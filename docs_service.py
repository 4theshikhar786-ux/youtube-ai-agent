"""Google Docs export service."""

from __future__ import annotations

import logging

from google.oauth2 import service_account

logger = logging.getLogger(__name__)
from googleapiclient.discovery import build


class GoogleDocsService:
    """Create Google Docs from generated markdown content."""

    SCOPES = [
        "https://www.googleapis.com/auth/documents",
        "https://www.googleapis.com/auth/drive.file",
    ]

    def __init__(self, service_account_file: str, folder_id: str | None = None) -> None:
        logger.info("Initializing Google Docs service with credentials path: %s", service_account_file)
        try:
            credentials = service_account.Credentials.from_service_account_file(
                service_account_file,
                scopes=self.SCOPES,
            )
            self.docs = build("docs", "v1", credentials=credentials)
            self.drive = build("drive", "v3", credentials=credentials)
        except Exception as exc:
            logger.exception("Google Docs service initialization failed")
            raise RuntimeError(f"Google Docs service initialization failed: {exc}") from exc
        self.folder_id = folder_id

    def create_document(self, title: str, content: str) -> str:
        """Create a Google Doc, insert content, optionally move it, and return its URL."""
        logger.info("Creating Google Doc: %s", title)
        try:
            document = self.docs.documents().create(body={"title": title}).execute()
            document_id = document["documentId"]
            self.docs.documents().batchUpdate(
                documentId=document_id,
                body={"requests": [{"insertText": {"location": {"index": 1}, "text": content}}]},
            ).execute()

            if self.folder_id:
                self.drive.files().update(
                    fileId=document_id,
                    addParents=self.folder_id,
                    removeParents="root",
                    fields="id, parents",
                ).execute()
        except Exception as exc:
            logger.exception("Google Doc creation failed")
            raise RuntimeError(f"Google Doc creation failed: {exc}") from exc

        logger.info("Created Google Doc: %s", document_id)
        return f"https://docs.google.com/document/d/{document_id}/edit"
