# Setup Guide

Follow these steps to run the autonomous YouTube AI Agent with Gemini, YouTube Data API, Google Docs API, and Telegram Bot API.

## 1. Create a Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Create your `.env` file

Copy the example configuration:

```bash
cp .env.example .env
```

Then edit `.env` and fill in the required API key and credential values.

## 3. Configure Gemini API

1. Open Google AI Studio.
2. Create a Gemini API key.
3. Put the key in `GEMINI_API_KEY` inside `.env`.
4. Keep `GEMINI_MODEL=gemini-1.5-flash` or switch to another Gemini text model available to your account.

## 4. Configure YouTube Data API

1. Open Google Cloud Console.
2. Create or select a project.
3. Enable **YouTube Data API v3**.
4. Create an API key.
5. Put it in `YOUTUBE_API_KEY` inside `.env`.
6. Set trend search options:
   - `YOUTUBE_REGION_CODE=IN` for India.
   - `YOUTUBE_CATEGORY_ID=28` for Science & Technology.
   - `YOUTUBE_MAX_RESULTS=10` for ten trend references.

## 5. Configure Google Docs API

1. Enable **Google Docs API** and **Google Drive API** in the same Google Cloud project.
2. Create a service account.
3. Download its JSON key.
4. Save the file as `service-account.json` in the project root, or update `GOOGLE_DOCS_CREDENTIALS_PATH` with the actual path.
5. Optional: create a Drive folder for generated docs, share it with the service account email, and put the folder ID in `GOOGLE_DOCS_FOLDER_ID`.

## 6. Configure Telegram Bot API

1. Open Telegram and create a bot with BotFather.
2. Copy the bot token to `TELEGRAM_BOT_TOKEN` inside `.env`.
3. Send a message to the bot, or add it to your group/channel.
4. Find your chat ID and set `TELEGRAM_CHAT_ID` inside `.env`.


## Required credentials checklist

Before running `python main.py`, confirm `.env` contains:

- `GEMINI_API_KEY` — Gemini API key from Google AI Studio.
- `YOUTUBE_API_KEY` — YouTube Data API v3 key from Google Cloud Console.
- `GOOGLE_DOCS_CREDENTIALS_PATH` — local path to the Google service account JSON file.
- `TELEGRAM_BOT_TOKEN` — Telegram bot token from BotFather.
- `TELEGRAM_CHAT_ID` — Telegram chat that receives the final result.

## 7. Run the agent

```bash
python main.py
```

Run with a custom niche:

```bash
python main.py --niche "personal finance for Indian students"
```

The agent will fetch trending YouTube videos, generate the full Hindi content package with Gemini, create a Google Doc, save a markdown backup, and send the result to Telegram.
