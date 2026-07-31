# Fully Autonomous YouTube AI Agent

A production-ready Python agent that discovers live trending YouTube videos, uses Gemini to create a complete Hindi content package, exports the result to Google Docs, and sends the final links to Telegram.

## Features

- Automatically searches current trending YouTube videos with the YouTube Data API
- Uses Gemini API for all AI generation
- Generates one viral YouTube topic inspired by live trends
- Writes a complete 2000-word Hindi script
- Generates an SEO-friendly title
- Generates an SEO-optimized description
- Generates 30 relevant hashtags
- Generates a detailed thumbnail prompt
- Saves a local markdown backup in `outputs/`
- Creates a Google Doc with the full output
- Sends the result to Telegram
- Loads secrets and runtime configuration from a local `.env` file

## Project Structure

```text
README.md
setup.md
requirements.txt
.env.example
.gitignore
main.py
agent.py
config.py
models.py
gemini_client.py
youtube_service.py
docs_service.py
telegram_service.py
utils.py
logging_config.py
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with real Gemini, YouTube, Google Docs, and Telegram credentials.
python main.py
```

For complete credential instructions, see [`setup.md`](setup.md).

## Required APIs

- **Gemini API** for topic, script, SEO, hashtag, and thumbnail prompt generation
- **YouTube Data API v3** for live trending video discovery
- **Google Docs API** and **Google Drive API** for document creation and optional folder placement
- **Telegram Bot API** for sending the final result notification

## Configuration

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

The example contains every setting the agent needs:

```env
GEMINI_API_KEY=
GEMINI_MODEL=gemini-1.5-flash
YOUTUBE_API_KEY=
YOUTUBE_REGION_CODE=IN
YOUTUBE_CATEGORY_ID=28
YOUTUBE_MAX_RESULTS=10
GOOGLE_DOCS_CREDENTIALS_PATH=service-account.json
GOOGLE_DOCS_FOLDER_ID=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
DEFAULT_NICHE=AI tools, technology, productivity, and online earning
OUTPUT_DIR=outputs
LOG_LEVEL=INFO
```


## Required API Keys and Where to Place Them

After copying `.env.example` to `.env`, place credentials in these variables:

- `GEMINI_API_KEY`: Gemini API key from Google AI Studio.
- `YOUTUBE_API_KEY`: YouTube Data API v3 key from Google Cloud Console.
- `GOOGLE_DOCS_CREDENTIALS_PATH`: path to the Google service account JSON file, for example `service-account.json`.
- `TELEGRAM_BOT_TOKEN`: Telegram bot token from BotFather.
- `TELEGRAM_CHAT_ID`: Telegram user, group, or channel chat ID that should receive the result.

## Usage

Run with the default niche from `.env`:

```bash
python main.py
```

Run with a custom niche:

```bash
python main.py --niche "personal finance for Indian students"
```

## Workflow

1. `YouTubeTrendService` fetches live trending videos for the configured region and category.
2. `YouTubeAIAgent` passes those trends to Gemini and generates a unique viral topic.
3. Gemini writes the 2000-word Hindi script, SEO title, SEO description, 30 hashtags, and thumbnail prompt.
4. The agent creates a Google Doc containing the generated package.
5. The agent saves a timestamped local markdown backup.
6. The agent sends the topic, title, Google Doc link, and local markdown path to Telegram.

## Output

Each run creates a timestamped markdown file containing:

1. Niche
2. Google Doc URL
3. Trending YouTube references
4. Viral YouTube topic
5. SEO title
6. SEO description
7. 30 hashtags
8. Thumbnail prompt
9. 2000-word Hindi script

## Production Notes

- Do not commit real `.env` files or service account JSON files.
- `.env`, `service-account.json`, and generated `outputs/` are ignored by git.
- Share your target Google Drive folder with the service account email if `GOOGLE_DOCS_FOLDER_ID` is set.
- The project is intentionally modular so each external API integration can be tested or replaced independently.
