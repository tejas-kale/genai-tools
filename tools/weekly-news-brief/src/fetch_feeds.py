#!/usr/bin/env python3
"""Fetches and parses podcast RSS feeds to extract episode metadata."""

import json
from datetime import datetime, timedelta
from pathlib import Path

try:
    from src.rss_utils import (
        get_audio_url,
        get_duration_seconds,
        parse_feed,
        parse_pub_date,
    )
except ImportError:
    from rss_utils import (
        get_audio_url,
        get_duration_seconds,
        parse_feed,
        parse_pub_date,
    )


def fetch_podcast_episodes(podcast: dict, days: int = 7) -> list[dict]:
    """Fetch episodes from a single podcast RSS feed."""
    feed = parse_feed(podcast["rss_url"])

    if feed.bozo and not feed.entries:
        return []

    cutoff_date = datetime.now() - timedelta(days=days)
    episodes = []

    for entry in feed.entries:
        if not hasattr(entry, "published"):
            continue

        pub_date = parse_pub_date(entry.published)

        if pub_date < cutoff_date:
            continue

        audio_url = get_audio_url(entry)
        if not audio_url:
            continue

        episode = {
            "podcast_name": podcast["name"],
            "podcast_category": podcast["category"],
            "episode_title": entry.get("title", "No title"),
            "episode_description": entry.get("summary", ""),
            "pub_date": pub_date.isoformat(),
            "audio_url": audio_url,
            "duration_seconds": get_duration_seconds(entry),
            "guid": entry.get("id", entry.get("link", "")),
        }
        episodes.append(episode)

    return episodes


def fetch_all_feeds(config_path: str = "config/podcasts.json") -> dict:
    """Fetch all podcast episodes and save to JSON."""
    with open(config_path) as f:
        podcasts_config = json.load(f)

    all_episodes = []

    for _category, podcasts in podcasts_config.items():
        for podcast in podcasts:
            episodes = fetch_podcast_episodes(podcast)
            all_episodes.extend(episodes)

    output_data = {
        "fetch_date": datetime.now().isoformat(),
        "episodes": all_episodes,
        "total_episodes": len(all_episodes),
    }

    output_path = Path("data/episode_metadata.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)

    return output_data


if __name__ == "__main__":
    data = fetch_all_feeds()
    print(f"Fetched {data['total_episodes']} episodes from past 7 days")
    print("Saved to: data/episode_metadata.json")
