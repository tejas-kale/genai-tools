#!/usr/bin/env python3
"""Validates podcast RSS feeds for availability and quality."""

import json
from datetime import datetime, timedelta
from pathlib import Path

from src.rss_utils import (
    get_audio_format,
    get_audio_url,
    get_duration_seconds,
    parse_feed,
    parse_pub_date,
)


def validate_feed(podcast: dict) -> dict:
    """Validate a single podcast RSS feed."""
    name = podcast["name"]
    rss_url = podcast["rss_url"]

    feed = parse_feed(rss_url)

    if feed.bozo and not feed.entries:
        return {
            "name": name,
            "status": "ERROR",
            "error": str(feed.bozo_exception),
            "recent_episodes": 0,
        }

    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_episodes = []
    audio_formats = set()
    durations = []

    for entry in feed.entries:
        if hasattr(entry, "published"):
            pub_date = parse_pub_date(entry.published)

            audio_url = get_audio_url(entry)
            if audio_url:
                audio_formats.add(get_audio_format(entry))

            duration = get_duration_seconds(entry)
            if duration > 0:
                durations.append(str(duration))

            if pub_date > seven_days_ago:
                recent_episodes.append(
                    {
                        "title": entry.get("title", "No title"),
                        "date": pub_date.strftime("%Y-%m-%d"),
                        "audio_format": get_audio_format(entry),
                    }
                )

    avg_duration = "N/A"
    if durations:
        try:
            total_seconds = sum(int(d) for d in durations if d.isdigit())
            avg_minutes = total_seconds / len(durations) / 60
            avg_duration = f"{avg_minutes:.0f} min"
        except (ValueError, TypeError):
            avg_duration = "N/A"

    result = {
        "name": name,
        "status": "OK",
        "publisher": feed.feed.get("title", "Unknown"),
        "recent_episodes": len(recent_episodes),
        "recent_episode_titles": [ep["title"] for ep in recent_episodes[:3]],
        "audio_formats": list(audio_formats),
        "avg_duration": avg_duration,
        "total_episodes": len(feed.entries),
    }

    if feed.bozo:
        result["warning"] = f"Encoding issue: {feed.bozo_exception}"

    return result


def main() -> None:
    """Validate all podcasts in config/podcasts.json."""
    config_path = Path("config/podcasts.json")
    with open(config_path) as f:
        podcasts_config = json.load(f)

    results = {}

    for category, podcasts in podcasts_config.items():
        if not podcasts:
            continue

        results[category] = []

        for podcast in podcasts:
            validation = validate_feed(podcast)
            results[category].append(validation)

    output_path = Path("config/podcast_validation.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    for category, validations in results.items():
        print(f"\n{category.upper().replace('_', ' ')}")
        print("=" * 60)

        for v in validations:
            print(f"\n{v['name']}")
            print(f"  Status: {v['status']}")

            if v["status"] == "OK":
                print(f"  Publisher: {v['publisher']}")
                print(f"  Recent episodes (7 days): {v['recent_episodes']}")
                print(f"  Audio formats: {', '.join(v['audio_formats'])}")
                print(f"  Avg duration: {v['avg_duration']}")
                print(f"  Total episodes in feed: {v['total_episodes']}")

                if "warning" in v:
                    print(f"  Warning: {v['warning']}")

                if v["recent_episode_titles"]:
                    print("  Latest episodes:")
                    for title in v["recent_episode_titles"]:
                        print(f"    - {title}")
            else:
                print(f"  Error: {v.get('error', 'Unknown error')}")

    print(f"\n\nValidation results saved to: {output_path}")


if __name__ == "__main__":
    main()
