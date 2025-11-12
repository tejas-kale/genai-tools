#!/usr/bin/env python3
"""ABOUTME: Test script to verify Claude API access and authentication.
ABOUTME: Tests basic API connectivity with a simple prompt."""

import os
import sys

from anthropic import Anthropic


def test_claude_api() -> None:
    """Test Claude API connection with a simple message."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        print("❌ ANTHROPIC_API_KEY environment variable not set")
        print("\nTo set it, run:")
        print('  export ANTHROPIC_API_KEY="your-api-key-here"')
        print("\nGet your API key from: https://console.anthropic.com/")
        sys.exit(1)

    print("✓ ANTHROPIC_API_KEY found")
    print(f"  Key prefix: {api_key[:8]}...")

    try:
        client = Anthropic(api_key=api_key)
        print("\n✓ Claude client initialized")

        print("\n⏳ Testing API with simple prompt...")
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            messages=[{"role": "user", "content": "Say hello in one sentence."}],
        )

        response_text = message.content[0].text
        print(f"✓ API response received: {response_text}")

        print("\n✅ Claude API is working correctly!")
        print(f"   Model: {message.model}")
        print(f"   Tokens used: {message.usage.input_tokens} in, "
              f"{message.usage.output_tokens} out")

    except Exception as e:
        print(f"\n❌ API test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_claude_api()
