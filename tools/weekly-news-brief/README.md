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
# Test Claude API access
uv run python test_claude_api.py

# Run full pipeline (when implemented)
uv run python src/main.py
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
2. **Episode Filtering**: Claude AI selects 12-15 newsworthy episodes
3. **Audio Download**: Fetch selected episode audio files
4. **Transcription**: Whisper.cpp converts audio to text (local, free)
5. **Summarisation**: Claude AI generates structured weekly briefing

## Configuration

### Whisper.cpp Setup

Whisper.cpp should be installed at `~/.local/share/llm/whisper.cpp/` with the base model:

```bash
# Location
~/.local/share/llm/whisper.cpp/build/bin/whisper-cli

# Model
~/.local/share/llm/whisper.cpp/models/ggml-base.bin
```

### Claude API

Set your API key:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Get your key from: https://console.anthropic.com/

### Podcast Sources

Configure podcast RSS feeds in `config/podcasts.json` (template to be added).

## Development Status

**Task 1: Environment Setup** ✅ COMPLETED
- [x] Install Whisper.cpp
- [x] Set up Python environment
- [x] Create test script for Claude API
- [x] Create project directory structure

**Next Steps**:
- Task 2: Podcast source research and configuration
- Task 3: Build RSS fetcher
- Task 4: Build episode filter with Claude
- Task 5: Build podcast downloader
- Task 6: Build transcription pipeline
- Task 7: Build summarisation pipeline
- Task 8: End-to-end integration
- Task 9: Manual testing & evaluation
- Task 10: Cost & performance analysis

## Documentation

- `PHASE_1.md`: Complete Phase 1 specification
- `NOTES.md`: Whisper.cpp integration notes

## License

Part of the genai-tools project.
