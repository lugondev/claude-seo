# WCS / CSR Methodology

> **Evidence caveat:** AI citation optimization research is still emerging. Treat scoring rubrics and weights as **directional heuristics**, not proven methodology. Refresh quarterly against latest empirical data.

## North-star KPI -- Weighted Citation Share (WCS)

```
WCS = Σ(citation_presence × intent_weight × engine_weight × quality_weight)
```

| Variable | Values |
|---|---|
| `citation_presence` | 0 or 1 |
| `intent_weight` | informational=1, comparison=1.5, transactional=2 |
| `engine_weight` | Set by business priority (e.g. ChatGPT=1.0, Perplexity=0.8) |
| `quality_weight` | link cite=1.2, mention-only=1.0, weak-context=0.7 |

## Citation Survival Rate (CSR)

Pipeline model for understanding *where* visibility is lost. Each stage filters sources:

```
Query → Retrieved → Selected → Cited → Visited
         (RAG)      (context)   (output)  (click)
```

| Stage | Question | Optimization lever |
|---|---|---|
| **1. Retrieved** | Does the RAG pipeline find your page? | Crawlability, indexing, freshness, robots.txt AI UA access |
| **2. Selected** | Is your page chosen into the context window? | Passage answerability, entity coverage, factual density |
| **3. Cited** | Does the AI cite your page in the final answer? | Source authority, E-E-A-T, complementarity vs redundancy |
| **4. Visited** | Does the user click through after reading the AI answer? | Brand recognition, unique value signal, residual curiosity |

**CSR vs WCS:** WCS measures citation *output* (are you cited?). CSR diagnoses *where in the pipeline* you lose visibility. Use WCS for dashboards, CSR for debugging.

**Agentic search (emerging):** AI agents (ChatGPT Tasks, Operator) perform multi-step searches with tool use. Early signals suggest structured action pages ("How to book", "Where to buy") with `Offer` / `BuyAction` schema may improve agentic visibility. Track as experimental -- data is thin.

## Query-Type Segmentation

AI Overviews primarily affect **informational** queries. Always segment audit results:

| Query type | AI Overview impact | Audit priority |
|---|---|---|
| **Informational** | High (60-90% coverage) | Primary -- optimize for citation survival |
| **Comparison** | Medium-High | High -- AI loves structured comparisons |
| **Transactional** | Low (<25% coverage) | Lower -- Google protects ad revenue here |
| **Navigational** | Minimal | Skip -- users want specific sites |

> **Practical rule:** If >70% of your traffic is transactional, AI Overview impact is smaller than feared. Focus citation efforts on informational content clusters.

## GEO Composite Score (0-100)

| Category | Weight |
|---|---|
| AI Citability & Visibility | 20% |
| Brand Authority Signals | 15% |
| Content Quality & E-E-A-T | 20% |
| Technical Foundations | 15% |
| Structured Data | 10% |
| Platform Optimization | 10% |
| Entity Authority | 10% |

**Interaction note:** Structured Data and E-E-A-T are scored separately but interact -- structured data amplifies E-E-A-T signals in YMYL contexts. When auditing YMYL pages, check both together: schema markup without genuine authority is hollow; authority without structured data is harder for RAG to extract. *(Emerging hypothesis -- not yet empirically validated.)*

## Citability Grade Scale

| Grade | Score | Meaning |
|---|---|---|
| A | ≥80 | Strong citation candidate |
| B | ≥65 | Good with minor improvements |
| C | ≥50 | Average, needs work |
| D | ≥35 | Weak, significant gaps |
| F | <35 | Not citable |

## Minimum Monthly Dashboard

1. Citation rate by engine
2. WCS by topic cluster
3. Top cited URLs
4. Lost citation URLs
5. Competitor citation overlap
6. Brand mention share in AI answers (brand mentions ÷ total mentions in category)
7. AI share of voice (your citations ÷ total citations for target queries)
8. Citation quality distribution (link cite vs mention-only vs weak-context)

## Baseline First (Hard Rule)

Run baseline before changing content. **Never compare without baseline.** Use `scripts/prompt_cluster_generator.py` to build a reproducible prompt set (≥30 prompts, seed-locked for re-runs).

## Decay Warning

GEO gains decay **~30% over 6 months** as competitors optimize and models retrain. This is not a one-time fix. Diversify traffic sources, refresh audits quarterly.

## Quality Gates

- Max **50 pages** per full site audit
- Max **30s timeout** per page fetch
- Max **5 concurrent requests**
- **1-second delay** between sequential requests
- Respect `robots.txt`
- Skip pages with >80% content similarity (dedup)

## Guardrails

- Keep same prompt set during one experiment cycle
- Run tests at similar times to reduce variance
- Log engine / model / version when possible
- Save a dated baseline before any content change
