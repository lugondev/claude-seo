#!/usr/bin/env python3
"""
llms.txt generator -- builds an llms.txt from a site's sitemap.xml.

Walks the sitemap (handles `<sitemapindex>` recursion up to depth 2), filters
URLs to the target site, ranks them with a slug-priority heuristic, and emits
an llms.txt listing the top N URLs.

URL inputs are validated via `validate_url()` from `google_auth.py` (SSRF
protection: blocks loopback / private IPs / GCP metadata endpoint).

Usage:
    python llms_txt_generator.py --sitemap https://example.com/sitemap.xml \\
        --site https://example.com --limit 200
"""

import argparse
import json
import re
import sys
from xml.etree import ElementTree as ET

import requests

# Make google_auth importable when run from either scripts/ or the skill dir.
sys.path.insert(0, str((__import__("pathlib").Path(__file__).resolve().parent)))
from google_auth import validate_url  # noqa: E402

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def slug_priority(url: str) -> int:
    """Lower score = higher priority. Long-form content ranks above index pages."""
    path = re.sub(r"^https?://[^/]+", "", url).strip("/")
    if not path:
        return 100
    score = 50
    if any(k in path for k in ["blog", "guide", "how", "compare", "vs", "best", "faq"]):
        score -= 20
    if any(k in path for k in ["tag", "author", "page", "wp-json", "feed", "search", "utm_"]):
        score += 30
    score += min(path.count("/"), 5)
    return score


def fetch_urls_from_sitemap(url: str, depth: int = 0) -> list:
    """Fetch URLs from a sitemap. Handles both <urlset> and <sitemapindex> (recursive)."""
    if depth > 2:
        return []
    if not validate_url(url):
        print(f"Error: refused to fetch invalid/unsafe URL: {url}", file=sys.stderr)
        return []

    r = requests.get(url, timeout=20)
    r.raise_for_status()
    root = ET.fromstring(r.text)

    sub_sitemaps = root.findall(".//sm:sitemap/sm:loc", NS)
    if sub_sitemaps:
        all_urls = []
        for sm_loc in sub_sitemaps:
            if sm_loc.text:
                sub_url = sm_loc.text.strip()
                try:
                    all_urls.extend(fetch_urls_from_sitemap(sub_url, depth + 1))
                except Exception as e:
                    print(f"Warning: failed to fetch sub-sitemap {sub_url}: {e}", file=sys.stderr)
        return all_urls

    locs = [e.text.strip() for e in root.findall(".//sm:url/sm:loc", NS) if e.text]
    return locs


def main():
    p = argparse.ArgumentParser(description="Generate llms.txt from a sitemap")
    p.add_argument("--sitemap", required=True, help="Sitemap URL (https://example.com/sitemap.xml)")
    p.add_argument("--site", required=True, help="Site URL prefix; only URLs starting with this are kept")
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--json", action="store_true", help="Emit a JSON summary instead of llms.txt text")
    args = p.parse_args()

    if not validate_url(args.site):
        print(f"Error: invalid --site URL: {args.site}", file=sys.stderr)
        sys.exit(2)

    try:
        urls = fetch_urls_from_sitemap(args.sitemap)
    except Exception as e:
        print(f"Error: failed to fetch sitemap: {e}", file=sys.stderr)
        sys.exit(1)

    urls = [u for u in urls if u.startswith(args.site)]
    urls = sorted(set(urls), key=slug_priority)[: args.limit]

    if args.json:
        print(json.dumps({
            "script": "llms_txt_generator",
            "sitemap": args.sitemap,
            "site": args.site,
            "url_count": len(urls),
            "urls": urls,
        }, indent=2))
        return

    out = []
    out.append(f"# llms.txt for {args.site}")
    out.append("")
    out.append(f"# Generated from {args.sitemap}")
    out.append(f"# {len(urls)} URLs included")
    out.append("")
    out.append("# Preferred citation pages")
    for u in urls:
        out.append(u)
    print("\n".join(out))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
