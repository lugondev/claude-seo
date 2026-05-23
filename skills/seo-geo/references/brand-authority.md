# Brand Authority & AI Crawler Audit

## Brand Mention Correlation Data

Source: [Ahrefs Research -- "What Influences AI Citations"](https://ahrefs.com/blog/ai-seo-study/), December 2025. YouTube correlation (0.737) and backlink weakness (0.266) from same study.

| Platform | Correlation with AI Visibility | Priority |
|---|---|---|
| YouTube mentions | **0.737** (strongest) | 🔴 Critical |
| Reddit mentions | High | 🔴 Critical |
| Wikipedia/Wikidata presence | High | 🔴 Critical |
| LinkedIn company profile | Moderate | 🟡 Important |
| Crunchbase listing | Moderate | 🟡 Important |
| GitHub presence | Moderate (for tech) | 🟡 Important |
| Quora answers | Low-Moderate | 🔵 Nice-to-have |
| Stack Overflow | Low-Moderate (for tech) | 🔵 Nice-to-have |
| Product Hunt | Low-Moderate (for SaaS) | 🔵 Nice-to-have |
| G2/Trustpilot reviews | Low-Moderate | 🔵 Nice-to-have |
| Traditional backlinks/DR | **0.266** (weak!) | ⚪ Overrated |

> **Key insight:** Brand mentions are **3× stronger** than backlinks for AI visibility. Prioritize platform presence over link building.

## Brand Mention Audit Procedure

### Critical Platforms (always check)

1. **YouTube** -- Search the web for `"brand name" site:youtube.com`
   - Check: Channel exists? Relevant content? Video descriptions contain URLs?

2. **Reddit** -- Search the web for `"brand name" site:reddit.com`
   - Check: Mentioned in discussions? Brand participates authentically? Sentiment positive?

3. **Wikipedia** -- Fetch `https://en.wikipedia.org/wiki/Brand_Name`
   - Check: Article exists? Accurate? Notable enough for Wikipedia?

### Important Platforms (check if relevant)

4. **LinkedIn** -- Search the web for `"brand name" site:linkedin.com`
5. **Crunchbase** -- Search the web for `"brand name" site:crunchbase.com`
6. **GitHub** -- Search the web for `"brand name" site:github.com` (for tech brands)

### Rate Limit Guard

> If any platform returns 429/blocked or is inaccessible, gracefully skip and log as `[Unverified -- Platform Blocked]`. Do not fail the entire audit because one platform is unreachable.

---

## AI Crawler Access Audit

### 14 AI Crawler User Agents

Check `/robots.txt` for each of these crawlers:

| Crawler | Owner | Purpose |
|---|---|---|
| `GPTBot` | OpenAI | Training data |
| `OAI-SearchBot` | OpenAI | ChatGPT web search |
| `ChatGPT-User` | OpenAI | ChatGPT browsing |
| `ClaudeBot` | Anthropic | Training data |
| `anthropic-ai` | Anthropic | General crawling |
| `PerplexityBot` | Perplexity | Search & citation |
| `CCBot` | Common Crawl | Open dataset |
| `Bytespider` | ByteDance | TikTok/Douyin AI |
| `cohere-ai` | Cohere | Training data |
| `Google-Extended` | Google | Gemini training |
| `GoogleOther` | Google | Non-search crawling |
| `Applebot-Extended` | Apple | Apple Intelligence |
| `FacebookBot` | Meta | Meta AI |
| `Amazonbot` | Amazon | Alexa/AI features |

### How to Check

1. Fetch `https://domain.com/robots.txt`
2. For each crawler, determine status:
   - **ALLOWED** -- no block rule, or explicit `Allow`
   - **BLOCKED** -- explicit `Disallow: /` for this UA
   - **PARTIALLY_BLOCKED** -- some paths blocked
   - **BLOCKED_BY_WILDCARD** -- blocked by `User-agent: *` with no specific override
   - **NOT_MENTIONED** -- no specific rule (inherits wildcard)

### Recommendations

- **Allow** `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot` -- these drive citation traffic
- **Allow** `ClaudeBot`, `Applebot-Extended` -- emerging citation sources
- Consider blocking `GPTBot`, `Google-Extended`, `CCBot` only if concerned about training data usage
- **Never block all AI crawlers** -- this eliminates AI visibility entirely

## Sentiment Audit

Brand mentions alone are not enough -- **sentiment** determines whether citations help or harm.

> **Data:** AI Overviews surface negative sentiment in 2.3% of brand mentions. Review management reduces negative citations by 47%.

### Audit Steps

1. **Search brand + negative modifiers** -- `"brand name" scam`, `"brand name" bad`, `"brand name" problem` on Reddit, Quora, Trustpilot
2. **Classify sentiment** per platform:
   - **Positive** -- endorsement, recommendation, positive review
   - **Neutral** -- factual mention without judgment
   - **Negative** -- complaint, warning, negative review
3. **Prioritize response:** Negative sentiment on high-correlation platforms (YouTube 0.737, Reddit) needs immediate attention
4. **Track over time:** Sentiment ratio is a leading indicator -- declining sentiment precedes citation loss

### Review Management

- Respond to negative reviews on G2, Trustpilot, Reddit (where authentic)
- Flag fake negative reviews for platform removal
- Proactively generate positive sentiment via case studies, testimonials, community participation

---

### llms.txt Check

1. Fetch `https://domain.com/llms.txt`
2. Check if exists and contains:
   - Site description
   - Priority pages listed
   - Update frequency
3. Also check `https://domain.com/llms-full.txt` for extended version
