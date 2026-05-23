#!/usr/bin/env python3
"""
GEO Checker -- Generative Engine Optimization audit for LOCAL PROJECT FILES.

Scans HTML / JSX / TSX files in a project for AI citation readiness signals
(structured data, headings, author attribution, FAQ blocks, statistics,
direct-answer patterns, entity recognition). Returns a per-file score and an
overall project score.

Usage:
    python geo_checker.py <project_path>

Output:
    Per-file scores plus a JSON summary on stdout. Exit 0 if average >= 60,
    else 1. No URL fetch -- safe to run offline.
"""
import sys
import re
import json
from pathlib import Path

# Best-effort utf-8 on Windows consoles
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass


SKIP_DIRS = {
    "node_modules", ".next", "dist", "build", ".git", ".github",
    "__pycache__", ".vscode", ".idea", "coverage", "test", "tests",
    "__tests__", "spec", "docs", "documentation",
}

SKIP_FILES = {
    "jest.config", "webpack.config", "vite.config", "tsconfig",
    "package.json", "package-lock", "yarn.lock", ".eslintrc",
    "tailwind.config", "postcss.config", "next.config",
}


def is_page_file(file_path: Path) -> bool:
    """Heuristic: is this file likely a public-facing page (not a config/test)?"""
    name = file_path.stem.lower()
    if any(skip in name for skip in SKIP_FILES):
        return False
    if name.endswith(".test") or name.endswith(".spec"):
        return False
    if name.startswith("test_") or name.startswith("spec_"):
        return False

    page_indicators = [
        "page", "index", "home", "about", "contact", "blog",
        "post", "article", "product", "service", "landing",
    ]
    parts = [p.lower() for p in file_path.parts]
    if "pages" in parts or "app" in parts or "routes" in parts:
        return True
    if any(ind in name for ind in page_indicators):
        return True
    if file_path.suffix.lower() == ".html":
        return True
    return False


def find_web_pages(project_path: Path) -> list:
    """Find candidate public web pages (HTML/JSX/TSX), capped at 30."""
    patterns = ["**/*.html", "**/*.htm", "**/*.jsx", "**/*.tsx"]
    files = []
    for pattern in patterns:
        for f in project_path.glob(pattern):
            if any(skip in f.parts for skip in SKIP_DIRS):
                continue
            if is_page_file(f):
                files.append(f)
    return files[:30]


def check_page(file_path: Path) -> dict:
    """Score a single page against 10 GEO signals."""
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return {"file": str(file_path.name), "passed": [], "issues": [f"Error: {e}"], "score": 0}

    issues, passed = [], []

    # 1. JSON-LD structured data
    if "application/ld+json" in content:
        passed.append("JSON-LD structured data found")
        if '"@type"' in content:
            if "Article" in content:
                passed.append("Article schema present")
            if "FAQPage" in content:
                passed.append("FAQ schema present")
            if "Organization" in content or "Person" in content:
                passed.append("Entity schema present")
    else:
        issues.append("No JSON-LD structured data (AI engines prefer structured content)")

    # 2. Heading hierarchy
    h1_count = len(re.findall(r"<h1[^>]*>", content, re.I))
    h2_count = len(re.findall(r"<h2[^>]*>", content, re.I))
    if h1_count == 1:
        passed.append("Single H1 heading (clear topic)")
    elif h1_count == 0:
        issues.append("No H1 heading - page topic unclear")
    else:
        issues.append(f"Multiple H1 headings ({h1_count}) - confusing for AI")
    if h2_count >= 2:
        passed.append(f"{h2_count} H2 subheadings (good structure)")
    else:
        issues.append("Add more H2 subheadings for scannable content")

    # 3. Author attribution
    author_patterns = ["author", "byline", "written-by", "contributor", 'rel="author"']
    if any(p in content.lower() for p in author_patterns):
        passed.append("Author attribution found")
    else:
        issues.append("No author info (AI prefers attributed content)")

    # 4. Publication date
    date_patterns = ["datePublished", "dateModified", "datetime=", "pubdate", "article:published"]
    if any(re.search(p, content, re.I) for p in date_patterns):
        passed.append("Publication date found")
    else:
        issues.append("No publication date (freshness matters for AI)")

    # 5. FAQ section
    faq_patterns = [r"<details", r"faq", r"frequently.?asked", r'"FAQPage"']
    if any(re.search(p, content, re.I) for p in faq_patterns):
        passed.append("FAQ section detected (highly citable)")

    # 6. Lists
    list_count = len(re.findall(r"<(ul|ol)[^>]*>", content, re.I))
    if list_count >= 2:
        passed.append(f"{list_count} lists (structured content)")

    # 7. Tables
    table_count = len(re.findall(r"<table[^>]*>", content, re.I))
    if table_count >= 1:
        passed.append(f"{table_count} table(s) (comparison data)")

    # 8. Entity recognition (Organization / LocalBusiness / Brand / rel=author)
    entity_patterns = [
        r'"@type"\s*:\s*"Organization"',
        r'"@type"\s*:\s*"LocalBusiness"',
        r'"@type"\s*:\s*"Brand"',
        r"itemtype.*schema\.org/(Organization|Person|Brand)",
        r'rel="author"',
    ]
    if any(re.search(p, content, re.I) for p in entity_patterns):
        passed.append("Entity/Brand recognition (E-E-A-T)")

    # 9. Original statistics / data density
    stat_patterns = [
        r"\d+%",
        r"\$[\d,]+",
        r"study\s+(shows|found)",
        r"according to",
        r"data\s+(shows|reveals)",
        r"\d+x\s+(faster|better|more)",
        r"(million|billion|trillion)",
    ]
    if sum(1 for p in stat_patterns if re.search(p, content, re.I)) >= 2:
        passed.append("Original statistics/data (citation magnet)")

    # 10. Direct-answer phrasing
    direct_patterns = [
        r"is defined as", r"refers to", r"means that",
        r"the answer is", r"in short,", r"simply put,", r"<dfn",
    ]
    if any(re.search(p, content, re.I) for p in direct_patterns):
        passed.append("Direct answer patterns (LLM-friendly)")

    total = len(passed) + len(issues)
    score = round((len(passed) / total) * 100) if total > 0 else 0
    return {"file": str(file_path.name), "passed": passed, "issues": issues, "score": score}


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    target_path = Path(target).resolve()

    print("\n" + "=" * 60)
    print("  GEO CHECKER - AI Citation Readiness Audit")
    print("=" * 60)
    print(f"Project: {target_path}")
    print("-" * 60)

    pages = find_web_pages(target_path)
    if not pages:
        print("\n[!] No public web pages found.")
        print("    Looking for: HTML, JSX, TSX files in pages/app directories")
        print("    Skipping: docs, tests, config files, node_modules")
        print("\n" + json.dumps({"script": "geo_checker", "pages_found": 0, "passed": True}, indent=2))
        sys.exit(0)

    print(f"Found {len(pages)} public pages to analyze\n")
    results = [check_page(p) for p in pages]

    for r in results:
        status = "[OK]" if r["score"] >= 60 else "[!]"
        print(f"{status} {r['file']}: {r['score']}%")
        if r["issues"] and r["score"] < 60:
            for issue in r["issues"][:2]:
                print(f"    - {issue}")

    avg_score = sum(r["score"] for r in results) / len(results) if results else 0
    print("\n" + "=" * 60)
    print(f"AVERAGE GEO SCORE: {avg_score:.0f}%")
    print("=" * 60)
    if avg_score >= 80:
        print("[OK] Excellent - Content well-optimized for AI citations")
    elif avg_score >= 60:
        print("[OK] Good - Some improvements recommended")
    elif avg_score >= 40:
        print("[!] Needs work - Add structured elements")
    else:
        print("[X] Poor - Content needs GEO optimization")

    output = {
        "script": "geo_checker",
        "project": str(target_path),
        "pages_checked": len(results),
        "average_score": round(avg_score),
        "passed": avg_score >= 60,
    }
    print("\n" + json.dumps(output, indent=2))
    sys.exit(0 if avg_score >= 60 else 1)


if __name__ == "__main__":
    main()
