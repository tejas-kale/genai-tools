# GenAI Tools

This repository is a collection of tools based on generative AI models that I built for personal use. The `tools` directory contains all the tools in individual directories. Each of the tool directories contains a `README.md` file that provides detailed information about the motivation, functionality, and usage of the tool.

## Installation

All tools can be installed from the root of this repository using `uv`:

```bash
# Clone the repository
git clone https://github.com/tejaskale/genai-tools.git
cd genai-tools

# Install all tools
uv tool install .
```

This will install all available CLI tools:
- `artomd` - Convert arXiv papers from HTML to Markdown format

## Tools Overview

### ArxivToMD Tool (`artomd`)
CLI tool for converting arXiv papers from HTML to Markdown format with images, tables, and hyperlinked references.

```bash
# Basic usage
artomd https://arxiv.org/html/2509.06283v2

# Specify output directory and enable verbose logging
artomd https://arxiv.org/html/2509.06283v2 --output ./papers --verbose
```

### VibeVoice Tool
Text-to-speech conversion utility using Microsoft's VibeVoice package. Designed for Google Colab execution.

### NotebookReport Tool
GitHub Actions workflow for automated Jupyter notebook analysis in pull requests.

## AI Disclaimer
The development of these tools involved usage of several AI-coding assistants including GitHub Copilot, Claude Code, and OpenAI Codex.