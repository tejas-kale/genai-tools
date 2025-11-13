# Weekly Podcast News Briefing

A command-line tool that generates concise weekly news briefings from podcast transcripts across multiple regions (Germany, India, World).

## Overview

This tool provides high-quality summaries of important events by:
1. Fetching episodes from configured podcast RSS feeds
2. Using Claude AI to filter newsworthy episodes
3. Transcribing audio locally with Whisper.cpp (free, fast on M1)
4. Generating structured briefings with Claude AI

**Phase 1 Status**: Manual workflow validation
**Estimated Cost**: ~£0.12-0.14 per week

## Quick Start

### Prerequisites

- Python 3.11+
- macOS with M1/M2/M3 chip
- Whisper.cpp (installed at `~/.local/share/llm/whisper.cpp/`)
- ANTHROPIC_API_KEY environment variable

### Installation

Dependencies are managed by `uv` at the parent project level:

```bash
# From the project root
uv sync
```

### Usage

```bash
# Configure Gemini API key (one-time setup)
uv run llm keys set gemini
# Enter your Gemini API key when prompted

# Validate podcast RSS feeds
uv run python validate_podcasts.py

# Fetch and filter episodes
uv run python run_fetch_and_filter.py

# Or run steps individually:
# 1. Fetch episodes from RSS feeds
uv run python src/fetch_feeds.py

# 2. Filter episodes with Gemini
uv run python src/filter_episodes.py
```

## Project Structure

```
weekly-news-brief/
├── config/
│   └── podcasts.json          # Podcast sources (to be configured)
├── data/
│   ├── episode_metadata.json  # Raw episode data
│   ├── filtered_episodes.json # Claude-filtered episodes
│   └── transcripts/           # Whisper.cpp output
├── output/
│   └── briefings/             # Final markdown briefings
├── temp/
│   └── audio/                 # Downloaded podcast files
├── logs/
│   └── pipeline.log           # Execution logs
├── src/
│   ├── fetch_feeds.py         # RSS fetching
│   ├── filter_episodes.py     # Claude-based filtering
│   ├── download_audio.py      # Audio file download
│   ├── transcribe.py          # Whisper.cpp wrapper
│   ├── summarise.py           # Claude summarisation
│   └── main.py                # Main pipeline orchestrator
└── test_claude_api.py         # API verification script
```

## Pipeline Stages

1. **RSS Feed Fetching**: Collect episodes from configured podcasts
2. **Episode Filtering**: Gemini AI selects 12-15 newsworthy episodes
3. **Audio Download**: Fetch selected episode audio files
4. **Transcription**: Whisper.cpp converts audio to text (local, free)
5. **Summarisation**: Gemini AI generates structured weekly briefing

## Configuration

### Whisper.cpp Setup

Whisper.cpp should be installed at `~/.local/share/llm/whisper.cpp/` with the base model:

```bash
# Location
~/.local/share/llm/whisper.cpp/build/bin/whisper-cli

# Model
~/.local/share/llm/whisper.cpp/models/ggml-base.bin
```

### Gemini API

Configure your API key using the llm package:

```bash
uv run llm keys set gemini
# Enter your API key when prompted
```

Get your API key from: https://aistudio.google.com/apikey

The llm package stores keys securely in `~/.config/io.datasette.llm/keys.json`

### Podcast Sources

Podcast RSS feeds are configured in `config/podcasts.json`. Validation results available in `TASK_2_PODCAST_VALIDATION.md`.

**Current sources:**
- Indian news: 2 podcasts (The Hindu In Focus, ThePrint)
- World news: 4 podcasts (BBC, Today Explained, FT, NPR)
- Deep dive: 2 podcasts (The Daily, Today in Focus)
- German news: TBD

## Development Status

**Task 1: Environment Setup** ✅ COMPLETED
- [x] Install Whisper.cpp
- [x] Set up Python environment
- [x] Create test script for Claude API
- [x] Create project directory structure

**Task 2: Podcast Source Validation** ✅ COMPLETED
- [x] Validate RSS feeds
- [x] Check recent episodes availability
- [x] Verify audio formats
- [x] Document publishing schedules

**Task 3: RSS Feed Fetcher** ✅ COMPLETED
- [x] Parse podcast RSS feeds
- [x] Extract episode metadata (title, description, audio URL, date)
- [x] Filter episodes from past 7 days
- [x] Save to data/episode_metadata.json

**Task 4: Episode Filter with Gemini** ✅ COMPLETED
- [x] Configure llm package with Gemini support
- [x] Build AI-powered episode filtering
- [x] Select 12-15 newsworthy episodes
- [x] Save filtered episodes with selection reasons

**Next Steps**:
- Task 5: Build podcast downloader
- Task 6: Build transcription pipeline
- Task 7: Build summarisation pipeline
- Task 8: End-to-end integration
- Task 9: Manual testing & evaluation
- Task 10: Cost & performance analysis

## Documentation

- `PHASE_1.md`: Complete Phase 1 specification
- `NOTES.md`: Whisper.cpp integration notes
- `GEMINI_NOTES.md`: llm package and Gemini configuration guide
- `TASK_2_PODCAST_VALIDATION.md`: Podcast source validation results
- `TASKS_3_4_SUMMARY.md`: RSS fetching and episode filtering implementation

## License

Part of the genai-tools project.
