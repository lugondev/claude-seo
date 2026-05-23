# Platform-Specific Optimization Rubrics

Scoring rubrics for each major AI answer engine. Apply the relevant platform rubric based on the site's target audience.

---

## Platform 1: Google AI Overviews (AIO)

### How AIO Selects Sources
> Source: [Zyppy / SparkToro AIO study](https://sparktoro.com/blog/), 2025; [ConvertMate 2026 data](https://convertmate.io/)

- **2025 data:** 92% of AIO citations came from pages ranking in **top 10 organic results**
- **2026 data:** 83% of AIO citations now come from pages **outside top 10** -- AIO is increasingly citing deeper results when content is well-structured
- **Directional synthesis:** Top-10 ranking still matters, but structured, answer-ready content can earn citations from any position. Treat both data points as directional -- AIO source selection is evolving rapidly.
- 47% of citations come from pages ranking **below position 5** -- AIO favors clarity over raw rank
- Featured snippet optimization has ~70% overlap with AIO optimization
- AIO prefers **concise, factual, unambiguous answers**

### Optimization Checklist
1. **Question-Based Headings** -- H2/H3 phrased as questions matching "People Also Ask"
2. **Direct Answer in First Paragraph** -- clear 1-2 sentence answer immediately after heading
3. **Tables and Structured Comparisons** -- AIO heavily cites tables
4. **Ordered/Unordered Lists** -- step-by-step = ordered, features = unordered
5. **FAQ Sections** -- 5-10 real questions with H3 headings
6. **Definitions** -- "**[Term]** is [concise definition]." format
7. **Statistics with Sources** -- "According to [Source], [statistic]."
8. **Publication Date** -- visible published + last-updated dates
9. **Author Byline** -- name + credentials + link to author page
10. **Page Depth** -- keep target pages within 3 clicks of homepage

### Scoring (0-100)

| Criterion | Points |
|---|---|
| Ranks in top 10 for target queries | 20 |
| Question-based headings present | 10 |
| Direct answers after headings | 15 |
| Tables for comparison data | 10 |
| Lists for processes/features | 10 |
| FAQ section with 5+ questions | 10 |
| Statistics with citations | 10 |
| Publication/updated date visible | 5 |
| Author byline with credentials | 5 |
| Clean URL + heading hierarchy | 5 |

---

## Platform 2: ChatGPT Web Search

### How ChatGPT Selects Sources
> Source: [Brand24 / Ahrefs ChatGPT citation analysis](https://ahrefs.com/blog/ai-seo-study/), 2025

- Uses **Bing's search index** (not Google)
- Top citation sources: **Wikipedia (47.9%)**, Reddit (11.3%), YouTube, news outlets
- Heavily weights **entity recognition** -- structured entity (Wikipedia, Wikidata, Crunchbase) = much higher citation chance
- Prefers **comprehensive, authoritative** single sources over multiple thin pages

### Optimization Checklist
1. **Wikipedia Presence** -- verify article exists and is accurate
2. **Wikidata Entity** -- create/verify with key properties (instance of, official website, founding date)
3. **Bing Webmaster Tools** -- verify site registered, sitemap submitted
4. **Bing Index Coverage** -- `site:domain.com` on Bing to verify indexing
5. **Reddit Authority** -- authentic brand participation in relevant subreddits
6. **YouTube Presence** -- channel with relevant content, descriptions with URLs
7. **Authoritative Backlinks** -- .edu, .gov, major publications
8. **Entity Consistency** -- brand name, founding date, leadership consistent across platforms
9. **Comprehensive Content** -- target pages **2000+ words** with thorough coverage
10. **Clear Attribution** -- "About" sections, company descriptions

### Scoring (0-100)

| Criterion | Points |
|---|---|
| Wikipedia article exists and is accurate | 20 |
| Wikidata entity with 5+ properties | 10 |
| Bing index coverage of key pages | 10 |
| Reddit brand mentions (positive) | 10 |
| YouTube channel with relevant content | 10 |
| Authoritative backlinks (.edu, .gov, press) | 15 |
| Entity consistency across platforms | 10 |
| Content comprehensiveness (2000+ words) | 10 |
| Bing Webmaster Tools configured | 5 |

---

## Platform 3: Perplexity AI

### How Perplexity Selects Sources
> Source: [Detailed.com Perplexity citation analysis](https://detailed.com/perplexity-sources/), 2025

- Top citation sources: **Reddit (46.7%)**, Wikipedia, YouTube, major publications
- **Heaviest community validation weight** of all platforms
- Prefers recent content -- publication date is a strong ranking signal
- Cites **5-15 sources per answer** -- more opportunity for mid-authority sites

### Optimization Checklist
1. **Active Reddit Presence** -- authentic participation in relevant subreddits
2. **Reddit AMAs/Threads** -- participate in detailed discussions
3. **Forum/Community Presence** -- Hacker News, Stack Overflow, Quora, niche forums
4. **Discussion-Friendly Content** -- opinion pieces, research findings, original data
5. **Freshness Signals** -- clear dates, regular updates
6. **Multiple Source Validation** -- claims supported by other sources
7. **YouTube Video Content** -- with titles, descriptions, and transcripts
8. **Quotable Passages** -- standalone paragraphs making one clear point
9. **Original Data/Research** -- surveys, benchmarks, case studies
10. **Perplexity Pages** -- check if Perplexity has created a curated "Page"

### Scoring (0-100)

| Criterion | Points |
|---|---|
| Active Reddit presence in relevant subreddits | 20 |
| Forum/community mentions (HN, SO, Quora) | 10 |
| Content freshness (updated within 6 months) | 10 |
| Original research/data published | 15 |
| YouTube content with transcripts | 10 |
| Quotable, standalone paragraphs | 10 |
| Multi-source claim validation | 10 |
| Discussion-generating content | 10 |
| Wikipedia/Wikidata presence | 5 |

---

## Platform 4: Google Gemini

### Key Differences
- Draws heavily from **YouTube** and **Knowledge Panels**
- Prefers **40-60 word concise blocks** (shorter than other platforms)
- Values **Schema.org** structured data heavily
- Google Business Profile (GBP) matters for local queries

### Scoring (0-100)

| Criterion | Points |
|---|---|
| YouTube channel with relevant videos | 20 |
| Knowledge Panel exists | 15 |
| Schema.org structured data (Organization + sameAs) | 15 |
| Google Business Profile optimized | 10 |
| Concise answer blocks (40-60 words) | 15 |
| Consistent entity info across Google products | 10 |
| Content freshness | 10 |
| Author E-E-A-T signals | 5 |

---

## Platform 5: Bing Copilot

### Key Differences
- Built on **Bing infrastructure** -- Bing SEO is foundational
- Responds well to **IndexNow** submissions
- Values **LinkedIn** profiles and connections
- Uses **meta descriptions** more directly than other platforms

### Scoring (0-100)

| Criterion | Points |
|---|---|
| IndexNow configured and active | 15 |
| Bing Webmaster Tools verified | 15 |
| LinkedIn company/personal profiles optimized | 15 |
| Meta descriptions well-crafted | 10 |
| Bing index coverage complete | 10 |
| Schema.org structured data | 10 |
| Content quality and depth | 15 |
| Brand consistency across Bing-visible platforms | 10 |

---

## Cross-Platform Summary

### Universal Actions (Help ALL Platforms)
1. Wikipedia/Wikidata entity presence
2. YouTube channel with relevant content
3. Comprehensive, well-structured content with clear headings
4. Schema.org structured data (Organization + sameAs)
5. Fast page load and clean HTML
6. Author pages with credentials and sameAs links
7. Regular content updates with visible dates

### Platform-Specific Priority Matrix

| Priority | Google AIO | ChatGPT | Perplexity | Gemini | Copilot |
|---|---|---|---|---|---|
| #1 | Top-10 ranking | Wikipedia | Reddit presence | YouTube | IndexNow |
| #2 | Q&A structure | Entity graph | Original research | Knowledge Panel | Bing WMT |
| #3 | Tables/lists | Bing SEO | Freshness | Schema.org | LinkedIn |
| #4 | Featured snippets | Reddit | Community forums | GBP | Meta descriptions |
