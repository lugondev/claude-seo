# E-E-A-T Scoring Rubric (100 Points)

Score content against Google's E-E-A-T framework, adapted for AI citation readiness.

## Experience -- 25 Points

First-hand knowledge and direct involvement with the topic.

| Signal | Points | How to Check |
|---|---|---|
| First-person accounts ("I tested...", "We implemented...") | 5 | Look for specific personal experience narratives |
| Original research or data not available elsewhere | 5 | Check for unique datasets, surveys, benchmarks |
| Case studies with specific results | 4 | Look for named companies + concrete metrics |
| Screenshots, photos, or evidence of direct use | 3 | Check for authentic (not stock) visual evidence |
| Specific examples from personal experience | 4 | Unique, non-generic examples |
| Process demonstrations (not just outcomes) | 4 | Step-by-step from actual experience |

**Weak signals:** Only summarizes other sources, generic advice, hedging language ("reportedly", "supposedly").

## Expertise -- 25 Points

Demonstrated knowledge depth and professional competence.

| Signal | Points | How to Check |
|---|---|---|
| Author credentials visible (bio, degrees, certs) | 5 | Check for author page or byline with credentials |
| Technical depth appropriate to topic | 5 | Thorough treatment vs surface-level coverage |
| Methodology explanation | 4 | Describes how conclusions were reached |
| Data-backed claims (stats, research citations) | 4 | Claims supported by evidence |
| Industry terminology used correctly | 3 | Accurate specialized language |
| Author page with professional background | 4 | Dedicated page with bio, links |

**Weak signals:** Claims without evidence, surface-level coverage, misused terminology, no visible author.

## Authoritativeness -- 25 Points

Recognition by others as a credible source.

| Signal | Points | How to Check |
|---|---|---|
| Inbound citations from authoritative sources | 5 | Look for mentions from major publications |
| Author quoted in press/media | 4 | Media mentions, interviews |
| Industry awards or recognition | 3 | Relevant awards listed |
| Speaker at conferences/events | 3 | Speaking credentials |
| Published in respected outlets | 4 | Tier-1 publications or industry outlets |
| Comprehensive topic coverage (topical authority) | 3 | Site covers topic thoroughly, not one-off |
| Brand on Wikipedia or encyclopedic refs | 3 | Wikipedia article exists |

**Weak signals:** Single-topic site with no depth, no external validation, self-proclaimed "expert".

## Trustworthiness -- 25 Points

Accuracy, transparency, and safety of the content.

| Signal | Points | How to Check |
|---|---|---|
| Factual accuracy (no errors found) | 5 | Spot-check key claims |
| Sources cited for claims | 5 | Links or references to supporting evidence |
| Editorial/review process mentioned | 3 | "Reviewed by", editorial policy page |
| Clear disclosure (ads, affiliates, conflicts) | 3 | Disclosure statements present |
| HTTPS and security headers | 3 | Check protocol and basic security |
| Contact information available | 3 | Email, phone, or contact form |
| Privacy policy and terms present | 3 | Legal pages exist |

**Weak signals:** Unverifiable claims, no sources, hidden affiliations, HTTP-only.

## YMYL × Schema Interaction

For YMYL pages (health, finance, legal, news), structured data amplifies E-E-A-T signals. Missing schema = trust penalty.

### Required Schema for YMYL Pages

| Schema | Applies to | Critical for |
|---|---|---|
| `author` → `Person` with `sameAs` (LinkedIn, website) | All YMYL | Experience + Expertise |
| `reviewedBy` → `Person` with credentials | Health, finance, legal | Trustworthiness |
| `lastReviewedDate` | Health, finance, legal | Freshness + Trust |
| `citation` | Research-backed claims | Authoritativeness |

### Scoring Deduction

- Missing author schema on YMYL page → **-5 points** from E-E-A-T total
- Missing `reviewedBy` on medical/financial advice → **-10 points**
- No `lastReviewedDate` on time-sensitive YMYL content → **-5 points**
- Author lacks credential links (`sameAs`) → **-3 points**

### Interaction Rule

> Structured data without genuine authority is hollow. Authority without structured data is harder for RAG to extract. For YMYL, both must be present -- score them together, not independently.

---

## Composition

| Component | Weight | Max |
|---|---|---|
| Experience | 25% | 25 |
| Expertise | 25% | 25 |
| Authoritativeness | 25% | 25 |
| Trustworthiness | 25% | 25 |
| **Total** | | **100** |

## Interpretation

| Score | Rating | Meaning |
|---|---|---|
| 85-100 | Exceptional | Strong AI citation candidate across platforms |
| 70-84 | Good | Solid foundation, specific improvements will increase citability |
| 55-69 | Average | Multiple E-E-A-T gaps reducing AI visibility |
| 40-54 | Below Average | Significant content quality and trust issues |
| 0-39 | Poor | Fundamental content strategy overhaul needed |
