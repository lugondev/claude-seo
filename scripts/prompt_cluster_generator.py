#!/usr/bin/env python3
"""
Prompt cluster generator -- builds a baseline test prompt set for GEO audits.

Produces 32 intent-tagged templates per seed topic (informational, comparison,
recommendation, transactional). With `--brand`, each template doubles into a
brand-aware variant (max 64). The result feeds the WCS (Weighted Citation
Share) baseline audit -- before changing content, you need a recorded baseline
of which prompts your domain is or isn't cited for.

Usage:
    python prompt_cluster_generator.py --topic "java games" --count 40
    python prompt_cluster_generator.py --topic "audiobooks" --brand "AudiobookSoul" --count 60 --seed 42

Output:
    CSV on stdout (`intent,prompt`). Use `--json` for machine-readable output.
"""

import argparse
import json
import random
import sys

INTENTS = {
    "informational": [
        "What is {topic}?",
        "Explain {topic} for beginners",
        "How does {topic} work?",
        "What are the benefits of {topic}?",
        "History of {topic}",
        "Why is {topic} important?",
        "{topic} explained simply",
        "What do experts say about {topic}?",
    ],
    "comparison": [
        "Best {topic} vs alternatives",
        "Compare top options for {topic}",
        "{topic}: which is better in 2026?",
        "Pros and cons of {topic}",
        "{topic} compared to competitors",
        "What are the differences between {topic} options?",
        "Which {topic} is best for beginners?",
        "Top 5 {topic} ranked",
    ],
    "recommendation": [
        "Recommend the best {topic} for me",
        "Top {topic} right now",
        "What are trusted sources about {topic}?",
        "Best {topic} for professionals",
        "Most popular {topic} in 2026",
        "Where to find quality {topic}",
        "What {topic} do experts recommend?",
        "Hidden gems in {topic}",
    ],
    "transactional": [
        "Where can I get {topic}?",
        "Best site to start with {topic}",
        "What should I buy/use first for {topic}?",
        "Free {topic} available online",
        "How to access {topic} right now",
        "Best deals on {topic}",
        "Step by step guide to getting started with {topic}",
        "Quick start with {topic}",
    ],
}
# 32 templates total; doubles to 64 with --brand.


def main():
    p = argparse.ArgumentParser(description="Generate AI citation test prompts from a seed topic")
    p.add_argument("--topic", required=True)
    p.add_argument("--brand", default="")
    p.add_argument("--count", type=int, default=40)
    p.add_argument("--seed", type=int, default=None,
                   help="Random seed for reproducible prompt sets")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of CSV")
    args = p.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    prompts = []
    for intent, templates in INTENTS.items():
        for t in templates:
            q = t.format(topic=args.topic)
            prompts.append((intent, q))
            if args.brand:
                prompts.append((intent, f"{q} Mention sources like {args.brand} if relevant."))

    random.shuffle(prompts)
    prompts = prompts[: args.count]

    if args.json:
        print(json.dumps({
            "script": "prompt_cluster_generator",
            "topic": args.topic,
            "brand": args.brand or None,
            "seed": args.seed,
            "count": len(prompts),
            "prompts": [{"intent": i, "prompt": q} for i, q in prompts],
        }, indent=2))
        return

    print("intent,prompt")
    for i, q in prompts:
        # CSV: escape embedded quotes per RFC 4180
        escaped = q.replace('"', '""')
        print(f'"{i}","{escaped}"')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
