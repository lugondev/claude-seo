# AI Citability Scoring Rubric

Agent-executable methodology for scoring content passages on AI citation readiness.

> **Research basis:** Princeton, Georgia Tech, IIT Delhi (2024) -- "Generative Engine Optimization" paper.

## Core Insight

AI models cite specific passage types. The optimal citable passage is:

- **134–167 words** long (self-contained block)
- **Self-contained** -- makes sense without reading the rest of the page
- **Fact-rich** -- contains named entities, statistics, specific claims
- **Directly answers** a predictable question

## 5-Dimension Scoring

Score each content block (paragraph or section) on these 5 dimensions:

### 1. Answer Block Quality (30%)

| Signal | Points | How to Check |
|---|---|---|
| Definition pattern ("X is...", "X refers to...") | 8 | Look for `is defined as`, `refers to`, `means that` |
| Answer in first 60 words of the block | 7 | Count words before the first clear answer statement |
| Question-style heading above block | 8 | Check if H2/H3 is phrased as a question |
| Quotable claim (specific, attributable) | 7 | "According to [X]", "[N]% of...", "In [Year]..." |

### 2. Self-Containment (25%)

| Signal | Points | How to Check |
|---|---|---|
| Block length 134–167 words | 8 | Word count of the passage |
| Low pronoun density (<2% of words) | 6 | Count "it", "they", "this", "these", "those" vs total words |
| Named entities ≥3 | 6 | Count proper nouns, brand names, specific terms |
| No dangling references ("as mentioned above") | 5 | Search for "above", "below", "previously", "as noted" |

### 3. Structural Readability (20%)

| Signal | Points | How to Check |
|---|---|---|
| Average sentence length 10–20 words | 7 | Count words per sentence |
| Contains list or numbered items | 5 | Look for `<ul>`, `<ol>`, numbered patterns |
| Uses bold/emphasis for key terms | 4 | Look for `<strong>`, `<b>`, `<em>` |
| Clear paragraph breaks | 4 | No wall-of-text blocks >5 sentences |

### 4. Statistical Density (15%)

| Signal | Points | How to Check |
|---|---|---|
| Percentages present | 4 | Regex: `\d+%` |
| Dollar/currency amounts | 3 | Regex: `\$[\d,]+` or currency symbols |
| Year references | 3 | Regex: `\b20\d{2}\b` |
| Named sources ("According to [Source]") | 5 | Look for "according to", "study by", "research from" |

### 5. Uniqueness Signals (10%)

| Signal | Points | How to Check |
|---|---|---|
| First-person research ("Our data shows", "We tested") | 4 | Look for "our", "we" + research/data/test verbs |
| Case study with specific results | 3 | Look for named companies + metrics |
| Specific tool/product mentions | 3 | Look for proper nouns with versions or specifics |

## Cross-Source Features (Contextual -- Not Scored)

These factors affect citation likelihood but depend on competing content for the same query. Evaluate qualitatively during audit:

| Feature | Question | Implication |
|---|---|---|
| **Redundancy** | Does this page say the same thing as 10 other pages? | High redundancy = low citation probability (AI picks one) |
| **Complementarity** | Does this page add unique info not found elsewhere? | Unique data/perspective increases citation likelihood |
| **Consensus** | Does this page agree with majority of authoritative sources? | Consensus aligns with AI's preference for safe answers; contrarian claims need strong evidence |

> **When to use:** During audit Step 2, after scoring individual passages. If a page scores well on 5 dimensions but offers nothing unique vs competitors, citation likelihood is still low.

## Grading Scale

| Grade | Score | Interpretation |
|---|---|---|
| **A** | ≥80 | Strong citation candidate |
| **B** | ≥65 | Good with minor improvements |
| **C** | ≥50 | Average, needs work |
| **D** | ≥35 | Weak, significant gaps |
| **F** | <35 | Not citable |

## AI System Citation Preferences

| AI System | Preferred Block Length | Preferred Style | Key Signal |
|---|---|---|---|
| ChatGPT | Long-form (2000+ words) | Comprehensive, authoritative | Entity graph, Wikipedia |
| Perplexity | Medium (500-1500 words) | Discussion-validated, recent | Reddit presence, freshness |
| Claude | Medium (800-2000 words) | Well-structured, nuanced | Technical depth, citations |
| Gemini | Short (40-60 word blocks) | Concise, factual | YouTube, Knowledge Panel |
| Copilot | Medium (metadata-rich) | Bing-optimized, structured | IndexNow, meta descriptions |

## How to Apply

When auditing a page:

1. Fetch the target page
2. Identify the top 5 content blocks (paragraphs/sections)
3. Score each block across the 5 dimensions
4. Report: average score, grade distribution, top 3 / bottom 3 blocks
5. Recommend specific improvements for blocks scoring below 50
