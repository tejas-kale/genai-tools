# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based repository containing generative AI tools organized under the `tools/` directory. The project uses uv for dependency management and contains three main tool categories:

- **VibeVoice**: Text-to-speech conversion utility using Microsoft's VibeVoice package
- **NotebookReport**: GitHub Actions workflow for automated Jupyter notebook analysis in PRs
- **ArxivToMD**: CLI tool for converting arXiv papers from HTML to Markdown format

## Development Commands

### Environment Setup
```bash
# Install dependencies
uv sync

# Install development dependencies
uv sync --group dev
```

### Code Quality and Linting
```bash
# Run ruff linting with auto-fix
ruff check --fix

# Run ruff formatting
ruff format

# Run pre-commit hooks manually
pre-commit run --all-files

# Install pre-commit hooks
pre-commit install
```

### Package Management
```bash
# Add new dependency
uv add <package-name>

# Add development dependency
uv add --group dev <package-name>

# Remove dependency
uv remove <package-name>
```

## Code Style Guidelines (from .github/copilot-instructions.md)

- Keep code terse and concise
- Remove unnecessary comments
- Use concise variable names
- **AVOID print statements wherever possible** - only use when necessary for user feedback
- **DO NOT use try-catch blocks unless explicitly specified** - let code fail so Tejas can debug issues
- **NEVER use emojis in print statements or output**
- Place Python imports at the top of modules (first cell for notebooks)
- Use double quotes for strings
- Explain any regular expressions used

## Project Structure

```
genai-tools/
├── tools/
│   ├── vibevoice/          # Text-to-speech conversion tool
│   │   ├── nbs/            # Jupyter notebooks for Colab execution
│   │   ├── assets/         # Audio samples and resources
│   │   └── sample_texts/   # Example input texts
│   ├── notebookreport/     # GitHub Actions notebook analysis
│   │   └── notebook-report.yml  # Workflow configuration
│   └── arxiv_to_md/        # arXiv paper to Markdown converter
│       ├── cli.py          # CLI interface
│       ├── converter.py    # Core conversion logic
│       └── __init__.py     # Package initialization
├── notes/                  # Documentation and notes
├── pyproject.toml         # Project configuration and dependencies (unified)
└── .pre-commit-config.yaml # Git hooks configuration
```

## Tool-Specific Information

### VibeVoice Tool
- Primary notebook: `tools/vibevoice/nbs/vibevoice_create.ipynb`
- Designed for Google Colab with A100 GPU
- Requires voice samples from Microsoft VibeVoice repository
- Supports Markdown and EPUB input formats
- Uses OpenAI GPT models for text formatting
- Outputs MP3 audio files

### NotebookReport Tool
- GitHub Actions workflow for PR analysis
- Automatically processes changed `.ipynb` files
- Executes notebooks and generates analysis reports
- Integrates with OpenAI GPT-4 for report generation
- Optional Confluence integration for report storage

### ArxivToMD Tool
- CLI tool for converting arXiv papers from HTML to Markdown format
- Complete content extraction with images, tables, and hyperlinked references
- Downloads and organizes all figures/images with proper captions
- Converts HTML tables to Markdown format
- Creates hyperlinked citation system between in-text citations and bibliography
- Preserves LaTeX mathematical equations
- Robust error handling with progress indicators and logging
- Available as standalone tool installable via `uv tool install`

## Dependencies

The project uses several key dependencies:
- `ebooklib` for EPUB file processing
- `torch` and `transformers` for AI model inference
- `pydub` for audio processing
- `litellm` for LLM API interactions
- `jupyter` and `nbconvert` for notebook processing
- `beautifulsoup4` for HTML parsing
- `requests` for HTTP requests
- `click` for CLI interface

## Ruff Configuration

Ruff is configured with specific rules for Python 3.11+:
- Line length: 88 characters
- Enforces pycodestyle, pyflakes, isort, pep8-naming rules
- Ignores line length errors (handled by formatter)
- Uses double quotes and space indentation