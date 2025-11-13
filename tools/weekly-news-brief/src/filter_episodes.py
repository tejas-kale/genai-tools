#!/usr/bin/env python3
"""Filters podcast episodes using Gemini AI to identify newsworthy content."""

import json
from pathlib import Path

import llm

FILTER_PROMPT_TEMPLATE = """You are a news editor selecting podcast episodes for a weekly news briefing.

I have {total} podcast episodes from the past week. I need you to select the 12-15 most
newsworthy episodes that cover important current events.

SELECTION CRITERIA:
- Focus on actual news events (politics, economics, society, international affairs)
- Avoid: pure opinion pieces, lifestyle content, sports-only episodes
- Prioritise: breaking news, significant developments, in-depth analysis
- Balance across regions: Germany, India, and international stories

EPISODE LIST:
{episode_list}

INSTRUCTIONS:
Return ONLY a JSON object with this structure:
{{
  "selected_episodes": [
    {{
      "guid": "episode-guid-here",
      "reason": "Brief 1-sentence reason for selection"
    }}
  ],
  "rejected_count": 18,
  "selection_summary": "1-2 sentences about the week's news themes"
}}

Select 12-15 episodes total. Return ONLY valid JSON, no other text."""


def format_episode_for_filtering(episode: dict) -> dict:
    """Format episode metadata for Gemini filtering."""
    return {
        "guid": episode["guid"],
        "podcast": episode["podcast_name"],
        "category": episode["podcast_category"],
        "title": episode["episode_title"],
        "description": episode["episode_description"][:500],
        "date": episode["pub_date"][:10],
    }


def filter_with_gemini(
    episodes: list[dict],
    model_id: str = "gemini-2.5-flash",
) -> dict:
    """Use Gemini to filter episodes to most newsworthy."""
    episode_list = [format_episode_for_filtering(ep) for ep in episodes]
    episode_json = json.dumps(episode_list, indent=2)

    prompt = FILTER_PROMPT_TEMPLATE.format(
        total=len(episodes),
        episode_list=episode_json,
    )

    model = llm.get_model(model_id)
    response = model.prompt(prompt)
    response_text = response.text()

    if response_text.startswith("```json"):
        response_text = response_text.split("```json")[1].split("```")[0].strip()
    elif response_text.startswith("```"):
        response_text = response_text.split("```")[1].split("```")[0].strip()

    return json.loads(response_text)


def filter_episodes(
    metadata_path: str = "data/episode_metadata.json",
    output_path: str = "data/filtered_episodes.json",
    model_id: str = "gemini-2.5-flash",
) -> dict:
    """Filter episodes and save selected ones."""
    with open(metadata_path) as f:
        metadata = json.load(f)

    episodes = metadata["episodes"]

    filter_result = filter_with_gemini(episodes, model_id)

    selected_guids = {ep["guid"] for ep in filter_result["selected_episodes"]}
    selected_episodes = [ep for ep in episodes if ep["guid"] in selected_guids]

    output_data = {
        "filter_date": metadata["fetch_date"],
        "model_used": model_id,
        "total_episodes_considered": len(episodes),
        "episodes_selected": len(selected_episodes),
        "selection_summary": filter_result.get("selection_summary", ""),
        "episodes": selected_episodes,
        "selection_reasons": {
            ep["guid"]: ep["reason"] for ep in filter_result["selected_episodes"]
        },
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)

    return output_data


if __name__ == "__main__":
    result = filter_episodes()
    print(f"Considered {result['total_episodes_considered']} episodes")
    print(f"Selected {result['episodes_selected']} episodes")
    print(f"\nSummary: {result['selection_summary']}")
    print("\nSaved to: data/filtered_episodes.json")
