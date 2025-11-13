#!/usr/bin/env python3
"""ABOUTME: Runs the fetch and filter pipeline together.
ABOUTME: Fetches RSS feeds and filters episodes with Gemini."""

from src.fetch_feeds import fetch_all_feeds
from src.filter_episodes import filter_episodes


def main() -> None:
    """Run fetch and filter pipeline."""
    print("Step 1/2: Fetching RSS feeds...")
    fetch_data = fetch_all_feeds()
    print(f"  Fetched {fetch_data['total_episodes']} episodes\n")

    print("Step 2/2: Filtering episodes with Gemini...")
    filter_data = filter_episodes()
    print(f"  Selected {filter_data['episodes_selected']} episodes")
    print(f"\n  Summary: {filter_data['selection_summary']}")

    print("\n\nPipeline complete!")
    print("  Episodes metadata: data/episode_metadata.json")
    print("  Filtered episodes: data/filtered_episodes.json")


if __name__ == "__main__":
    main()
