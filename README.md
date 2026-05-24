![Claude SEO](screenshots/cover-image.jpeg)

# Claude SEO - SEO Audit Skill for Claude Code

SEO analysis skill for Claude Code. 25 sub-skills (21 core + 1 orchestrator + 1 framework integration + 2 extension mirrors) and 18 sub-agents covering technical SEO, on-page analysis, content quality (E-E-A-T), schema markup, image optimization, sitemap architecture, AI search optimization (GEO), local SEO, maps intelligence, semantic topic clustering, search experience optimization (SXO), SEO drift monitoring, e-commerce SEO, international SEO, FLOW framework integration, Google SEO APIs, PDF report generation, and strategic planning.

[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://claude.ai/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Fork of [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo)** — this fork removes community branding from AI context files and integrates additional methodology depth from `seo-for-ai` and `seo-optimization` skill sets. See [What's different in this fork](#whats-different-in-this-fork) below.

## Table of Contents

- [What's different in this fork](#whats-different-in-this-fork)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands](#commands)
- [Features](#features)
- [Architecture](#architecture)
- [Limitations](#limitations)
- [Requirements](#requirements)
- [Uninstall](#uninstall)
- [Extensions](#extensions)
- [Ecosystem](#ecosystem)
- [Documentation](#documentation)
- [Credits](#credits)
- [License](#license)
- [Contributing](#contributing)

## What's different in this fork

### Branding cleanup
All community/personal branding removed from SKILL.md files, agent context files, and scripts. Credits remain in [CONTRIBUTORS.md](CONTRIBUTORS.md) and [CHANGELOG.md](CHANGELOG.md) where they belong.

### GEO methodology depth (`seo-geo`)
- **Weighted Citation Share (WCS)** — north-star KPI formula with intent/engine/quality weights
- **Citation Survival Rate (CSR)** — 4-stage pipeline (Track → Measure → Analyze → Optimize)
- **Baseline guard** — hard rule: no content changes without a recorded WCS baseline
- **Platform rubrics** — 100-point scoring for Google AIO, ChatGPT, Perplexity, Gemini, Bing Copilot
- **Entity modeling** — Entity Authority Score 0-100, `sameAs` priority list, schema patterns
- **E-E-A-T scoring rubric** — 100-point rubric with YMYL × schema interaction
- **Brand authority signals** — AI crawler UA list (14 bots), correlation data, sentiment audit
- **3 helper scripts**: `geo_checker.py`, `llms_txt_generator.py`, `prompt_cluster_generator.py`

### Active link building (`seo-backlinks`)
- **6 campaign types** — guest post, resource page, broken link, HARO, digital PR, directories
- **Outreach templates** — 5 email templates with personalization, A/B testing, response handling
- **Directory submissions** — Tier 1 (DA 80+), Tier 2 (DA 50-79), 8 niche verticals

### Programmatic SEO depth (`seo-programmatic`)
- **Best practices** — content uniqueness strategy (>80% target, HARD STOP <30%), pre-launch checklist
- **Templates & URLs** — full Nunjucks syntax, `PSEOURLGenerator` class with dedup and length cap
- **Scale architecture** — `BatchProcessor` (1000-row chunks), `WorkerPool` (4-8 threads), `CheckpointManager`, per-batch quality validation with 10%-failure abort

### Semantic SEO (`seo-content`)
- **Entity optimization** — types, salience, relationships, `about`/`mentions` schema markup
- **Topical authority hub-spoke** — coverage checklist, authority signals, SERP-based clustering
- **Semantic/LSI variations** — integration strategy with density guidelines
- **NLP-friendly structure** — Q&A format, semantic HTML, logical content flow
- **5-step audit workflow** with before/after example

---

## Installation

### Manual Install (Unix/macOS/Linux)

```bash
git clone --depth 1 https://github.com/lugondev/claude-seo.git
bash claude-seo/install.sh
```

<details>
<summary>One-liner (curl, review then run)</summary>

```bash
curl -fsSL https://raw.githubusercontent.com/lugondev/claude-seo/main/install.sh > install.sh
cat install.sh        # review
bash install.sh       # run when satisfied
rm install.sh
```

</details>

### Windows (PowerShell)

```powershell
git clone --depth 1 https://github.com/lugondev/claude-seo.git
powershell -ExecutionPolicy Bypass -File claude-seo\install.ps1
```

> **Why git clone instead of `irm | iex`?** Claude Code's own security guardrails flag `irm ... | iex` as a supply chain risk. The git clone approach lets you inspect `claude-seo\install.ps1` before running it.

## Quick Start

```bash
# Start Claude Code
claude

# Run a full site audit
/seo audit https://example.com

# Analyze a single page
/seo page https://example.com/about

# Check schema markup
/seo schema https://example.com

# Generate a sitemap
/seo sitemap generate

# Optimize for AI search
/seo geo https://example.com
```

## Commands

| Command | Description |
|---------|-------------|
| `/seo audit <url>` | Full website audit with parallel subagent delegation |
| `/seo page <url>` | Deep single-page analysis |
| `/seo sitemap <url>` | Analyze existing XML sitemap |
| `/seo sitemap generate` | Generate new sitemap with industry templates |
| `/seo schema <url>` | Detect, validate, and generate Schema.org markup |
| `/seo images <url>` | Image optimization analysis |
| `/seo technical <url>` | Technical SEO audit (9 categories) |
| `/seo content <url>` | E-E-A-T and content quality analysis |
| `/seo geo <url>` | AI Overviews / Generative Engine Optimization |
| `/seo plan <type>` | Strategic SEO planning (saas, local, ecommerce, publisher, agency) |
| `/seo programmatic <url>` | Programmatic SEO analysis and planning |
| `/seo competitor-pages <url>` | Competitor comparison page generation |
| `/seo local <url>` | Local SEO analysis (GBP, citations, reviews, map pack) |
| `/seo maps [command]` | Maps intelligence (geo-grid, GBP audit, reviews, competitors) |
| `/seo hreflang <url>` | Hreflang/i18n SEO audit and generation |
| `/seo google [command] [url]` | Google SEO APIs (GSC, PageSpeed, CrUX, Indexing, GA4) |
| `/seo google report [type]` | Generate PDF/HTML report with charts |
| `/seo backlinks <url>` | Backlink profile analysis (free: Moz, Bing, Common Crawl) |
| `/seo cluster <seed-keyword>` | SERP-based semantic clustering and content architecture |
| `/seo sxo <url>` | Search Experience Optimization: page-type, user stories, personas |
| `/seo drift baseline <url>` | Capture SEO baseline for change monitoring |
| `/seo drift compare <url>` | Compare current state to stored baseline |
| `/seo drift history <url>` | Show drift history over time |
| `/seo ecommerce <url>` | E-commerce SEO: product schema, marketplace intelligence |
| `/seo firecrawl [command] <url>` | Full-site crawling and site mapping (extension) |
| `/seo dataforseo [command]` | Live SEO data via DataForSEO (extension) |
| `/seo image-gen [use-case] <desc>` | AI image generation for SEO assets (extension) |

## Features

### Core Web Vitals
- **LCP** (Largest Contentful Paint): Target < 2.5s
- **INP** (Interaction to Next Paint): Target < 200ms
- **CLS** (Cumulative Layout Shift): Target < 0.1

> INP replaced FID on March 12, 2024.

### E-E-A-T Analysis
Updated to September 2025 Quality Rater Guidelines:
- **Experience**: First-hand knowledge signals
- **Expertise**: Author credentials and depth
- **Authoritativeness**: Industry recognition
- **Trustworthiness**: Contact info, security, transparency

100-point scoring rubric with YMYL × schema interaction (`seo-geo/references/eeat-scoring-rubric.md`).

### AI Search Optimization (GEO)
- **WCS (Weighted Citation Share)** — north-star KPI across Google AIO, ChatGPT, Perplexity, Gemini, Bing Copilot
- **Platform-specific rubrics** — 100-point scoring per AI engine with optimization checklists
- **Entity modeling** — Entity Authority Score, `sameAs` priority (Wikidata, Wikipedia, LinkedIn), schema patterns
- **Citability rubric** — 5-dimension passage scoring: Answer Block 30%, Self-Containment 25%, Structure 20%, Statistical Density 15%, Uniqueness 10%
- **Helper scripts**: `geo_checker.py` (offline GEO signal scanner), `llms_txt_generator.py`, `prompt_cluster_generator.py`

### Programmatic SEO at Scale
- Template engine: Nunjucks-style syntax with layout inheritance and filter chaining
- `PSEOURLGenerator` — slug sanitizer, length cap (<75 chars), dedup enforcement
- `BatchProcessor` — 1000-row chunks with checkpoint/resume
- `WorkerPool` — 4-8 threads, per-batch quality validation (abort if >10% fail)
- Quality gates: WARNING at 100+ pages, HARD STOP at 500+ or <30% unique content
- Performance benchmarks: ~1,500 pages/min at 6 workers

### Semantic SEO
- Entity optimization with `about`/`mentions` schema markup
- Topical authority hub-spoke model with coverage checklist
- Semantic variation integration (primary 0.5–1.5%, semantic 0.2–0.5%)
- NLP-friendly content structure: Q&A format, semantic HTML, logical flow

### Link Building
- 6 campaign types: guest post, resource page, broken link, HARO, digital PR, directories
- 5 outreach email templates with A/B testing and follow-up sequences
- Directory submissions: Tier 1 (DA 80+), Tier 2 (DA 50–79), 8 niche verticals
- KPI tracking: DR growth, referring domains, organic traffic lift

### Schema Markup
- Detection: JSON-LD (preferred), Microdata, RDFa
- Validation against Google's supported types
- Deprecation awareness:
  - HowTo: Deprecated (Sept 2023)
  - FAQ: Restricted to gov/health sites (Aug 2023)
  - SpecialAnnouncement: Deprecated (July 2025)

### Google SEO APIs
- **PageSpeed Insights + CrUX**: Lab and field Core Web Vitals data
- **Search Console**: Top queries, URL inspection, sitemap status
- **Indexing API**: Notify Google of new/updated/removed URLs
- **GA4**: Organic traffic, top landing pages, device/country breakdown
- **PDF Reports**: A4 reports with charts via WeasyPrint and matplotlib

4-tier credential system:

| Tier | Auth | APIs |
|------|------|------|
| 0 | API key | PSI, CrUX, CrUX History |
| 1 | + OAuth/SA | + GSC, URL Inspection, Indexing |
| 2 | + GA4 config | + GA4 organic traffic |
| 3 | + Ads token | + Keyword Planner |

### Local SEO and Maps Intelligence
- Google Business Profile optimization
- NAP consistency auditing
- Citation and review analysis
- Geo-grid rank tracking and competitor radius mapping

## Architecture

```
~/.claude/skills/seo/          # Main orchestrator
~/.claude/skills/seo-*/        # 25 sub-skills (auto-discovered)
~/.claude/agents/seo-*.md      # 18 sub-agents (auto-discovered)
~/.claude/skills/seo/scripts/  # Python helper scripts
```

See `schema/templates.json` for ready-to-use JSON-LD snippets. Full release history in [CHANGELOG.md](CHANGELOG.md).

## Limitations

Sites that render content client-side without SSR will produce false-negative findings on content, schema, headings, and meta in most subagents. The orchestrator and most subagents fetch raw HTML rather than executing JavaScript.

The `seo-visual` subagent uses Playwright when available and can verify visible content matches what the raw-HTML subagents see; expect divergence on SPA targets.

## Requirements

- Python 3.10+
- Claude Code CLI
- Optional: Playwright for screenshots
- Optional: Google API credentials for enriched data (see `/seo google setup`)

## Uninstall

```bash
git clone --depth 1 https://github.com/lugondev/claude-seo.git
bash claude-seo/uninstall.sh
```

<details>
<summary>One-liner (curl)</summary>

```bash
curl -fsSL https://raw.githubusercontent.com/lugondev/claude-seo/main/uninstall.sh | bash
```

</details>

## Extensions

Optional add-ons that integrate external data sources via MCP servers. See [MCP Integration Guide](docs/MCP-INTEGRATION.md) for setup details.

### DataForSEO

Live SERP data, keyword research, backlinks, on-page analysis, content analysis, business listings, AI visibility checking, and LLM mention tracking. 22 commands across 9 API modules.

```bash
./extensions/dataforseo/install.sh
```

```bash
/seo dataforseo serp best coffee shops
/seo dataforseo keywords seo tools
/seo dataforseo backlinks example.com
/seo dataforseo ai-mentions your brand
```

See [DataForSEO Extension](extensions/dataforseo/README.md) for full documentation.

### Banana (AI Image Generation)

Generate SEO images (OG previews, blog heroes, product photos, infographics) using the
[Claude Banana](https://github.com/AgriciDaniel/banana-claude) Creative Director pipeline.

```bash
./extensions/banana/install.sh
```

```bash
/seo image-gen og "Professional SaaS dashboard"
/seo image-gen hero "AI-powered content creation"
/seo image-gen batch "Product photography" 3
```

See [Banana Extension](extensions/banana/README.md) for full documentation.

### Firecrawl (Site Crawling)

Full-site crawling and URL discovery using the [Firecrawl](https://www.firecrawl.dev/) MCP server.

```bash
./extensions/firecrawl/install.sh
```

```bash
/seo firecrawl crawl https://example.com
/seo firecrawl map https://example.com
```

See [Firecrawl Extension](extensions/firecrawl/README.md) for full documentation.

## Ecosystem

Claude SEO is part of a family of Claude Code skills that work together:

| Skill | What it does | How it connects |
|-------|-------------|-----------------|
| [Claude SEO](https://github.com/lugondev/claude-seo) | SEO analysis, audits, schema, GEO | Core. Analyzes sites and generates action plans. |
| [Claude Blog](https://github.com/AgriciDaniel/claude-blog) | Blog writing, optimization, scoring | Companion. Writes content optimized by SEO findings. |
| [Claude Banana](https://github.com/AgriciDaniel/banana-claude) | AI image generation via Gemini | Shared. Generates images for SEO assets and blog posts. |
| [AI Marketing Claude](https://github.com/zubair-trabzada/ai-marketing-claude) | Copywriting, emails, social, ads, funnels, CRO | Community. Post-audit marketing action from SEO findings. |
| [FLOW](https://github.com/AgriciDaniel/flow) | Evidence-led SEO framework (41 AI prompts, CC BY 4.0) | Knowledge base. Powers `seo-flow` prompts. |

**Workflow example:**
1. `/seo audit https://example.com` to identify content gaps and technical issues
2. `/seo backlinks https://example.com` to analyze link profile and competitor gaps
3. `/seo geo https://example.com` to measure WCS and optimize for AI citation
4. `/seo image-gen hero "blog topic"` to generate hero images (banana extension)

## Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Commands Reference](docs/COMMANDS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [MCP Integration](docs/MCP-INTEGRATION.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## Credits

Original project by [Agrici Daniel](https://agricidaniel.com/about) — see [CONTRIBUTORS.md](CONTRIBUTORS.md) for the full list of upstream contributors.

This fork is maintained by [lugondev](https://github.com/lugondev).

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting PRs.
