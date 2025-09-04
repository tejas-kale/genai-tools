# Notebook Report Tool

Automatically generates analysis reports for Jupyter notebooks in pull requests using AI.

## Features

- Detects Jupyter notebooks in PRs
- Executes notebooks using uv environment
- Converts notebooks to Markdown with images
- Generates structured reports using OpenAI GPT-4
- Uploads reports to Confluence
- Commits reports back to the PR

## Setup

1. Copy `notebook-report.yml` to `.github/workflows/` in your repository
2. Configure the following secrets and variables:
   - `CONFLUENCE_AUTH`: Base64 encoded username:password for Confluence
   - `CONFLUENCE_SPACE_KEY`: Your Confluence space key (variable)
   - `CONFLUENCE_BASE_URL`: Your Confluence base URL (variable)

## Report Template

Generated reports include:
- Issue ID
- Date
- Problem Statement
- Key Findings
- Topics for Stakeholder Discussion
- Conclusion

## Requirements

- Repository with `pyproject.toml` and uv configuration
- GitHub Models access for GPT-4
- Confluence API access (optional)