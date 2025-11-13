#!/usr/bin/env python3
"""Common utilities for RSS feed parsing."""

from datetime import datetime

import feedparser
from dateutil import parser as date_parser


def parse_pub_date(date_str: str) -> datetime:
    """Parse publication date from various RSS formats."""
    return date_parser.parse(date_str).replace(tzinfo=None)


def get_audio_url(entry: dict) -> str:
    """Extract audio URL from RSS entry enclosures."""
    if hasattr(entry, "enclosures") and entry.enclosures:
        return entry.enclosures[0].get("href", "")
    return ""


def get_audio_format(entry: dict) -> str:
    """Extract audio format from RSS entry enclosures."""
    if hasattr(entry, "enclosures") and entry.enclosures:
        return entry.enclosures[0].get("type", "unknown")
    return "unknown"


def get_duration_seconds(entry: dict) -> int:
    """Extract duration in seconds from RSS entry."""
    if hasattr(entry, "itunes_duration"):
        duration = entry.itunes_duration
        if isinstance(duration, str) and duration.isdigit():
            return int(duration)
    return 0


def parse_feed(rss_url: str) -> feedparser.FeedParserDict:
    """Parse RSS feed and return feed object."""
    return feedparser.parse(rss_url)
