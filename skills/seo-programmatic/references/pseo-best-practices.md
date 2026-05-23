# pSEO Best Practices

Quality guardrails for high-volume programmatic page generation. Pairs with the SKILL.md "Thin Content Safeguards" section -- this reference is the deeper how-to.

## Content Uniqueness

**Target:** >80% unique content per page. **HARD STOP** at <30% (scaled content abuse risk).

### Strategies

1. **Unique introductions** -- replace mad-libs templates with data-driven openers.

   ```javascript
   // Bad: same intro everywhere
   intro: `Welcome to our ${city} page.`

   // Good: data-driven, every page differs
   intro: `${city} has ${businessCount} ${service} providers with an average rating of ${rating}/5.0 based on ${reviewCount} local reviews.`
   ```

2. **Dynamic sections.** Local statistics, user-generated content (reviews), location-specific imagery, custom FAQs per page.

3. **Avoid template fingerprints.** Visible `[VARIABLE]` patterns or identical sentence structures across pages are detection targets.

   ```html
   <!-- Bad: obvious template -->
   <p>We offer [SERVICE] in [CITY].</p>

   <!-- Good: natural variation -->
   <p>{{ city }} residents can choose from {{ providerCount }} certified {{ service }} professionals, with prices starting at ${{ minPrice }}.</p>
   ```

## Minimum Content Standards

| Metric | Minimum | Ideal |
|---|---|---|
| Word count | 300 | 800+ |
| Readability | Grade 8 | Grade 10-12 |
| Unique content | 70% (warn) -- 80% (target) | 85%+ |
| Internal links | 3 | 5-10 |
| External links | 1 | 2-3 |

## Thin Content -- What Triggers Penalties

Google defines thin content as "little to no value, duplicate, or low-effort". Red flags:

- Word count <300
- Same content across pages except 1-2 words swapped
- No unique value proposition
- Auto-generated without human review
- No substantive information

### Solutions

**Add unique data per page:**

```markdown
<!-- Thin -->
# Plumber in Austin
We have plumbers in Austin.

<!-- Substantive -->
# Plumber in Austin, TX
Austin has 127 licensed plumbing contractors with an average response time
of 2.3 hours. The typical service call costs $125-$175. Top-rated providers
include ABC Plumbing (4.9/5, 234 reviews) and XYZ Plumbers (4.7/5, 189 reviews).

## Emergency Services
24/7 emergency plumbing available from 43 providers.

## Common Issues
- Water heater repair: $250-$800
- Drain cleaning: $100-$300
- Pipe replacement: $400-$2,000
```

**Other levers:** import user-generated content (reviews, forum threads, Q&A), add expert commentary per location (regulations, codes, seasonal considerations).

## Keyword Density

**Target:** 1-3% for primary keyword.

| Range | Meaning |
|---|---|
| 1-2% | Natural, safe |
| 3-4% | Maximum before risk |
| >5% | Keyword stuffing |

### Placement Priority

1. Title tag (first 3-5 words)
2. H1 heading
3. First paragraph (first 100 words)
4. Subheadings (H2/H3)
5. Image alt text
6. Internal anchor text
7. Meta description

### Implementation

```javascript
function keywordDensity(content, keyword) {
  const words = content.toLowerCase().split(/\s+/);
  const kw = keyword.toLowerCase().split(/\s+/);
  const total = words.length;
  let count = 0;
  for (let i = 0; i <= words.length - kw.length; i++) {
    if (words.slice(i, i + kw.length).join(' ') === keyword.toLowerCase()) count++;
  }
  return (count / total) * 100;
}
```

## Value-Add vs Doorway Pages

### Doorway Pages -- AVOID

```html
<h1>Plumber Austin</h1>
<p>Looking for plumber Austin? Click here.</p>
<a href="/contact">Contact Us</a>
```

Characteristics: sole purpose is funneling to a conversion page, no substantive content, duplicate template across locations, no unique value.

### Value-Add Pages -- CREATE

```html
<h1>Plumber Services in Austin, TX</h1>

<p>Austin has 127 licensed plumbing contractors. Average emergency response
time is 2.3 hours. Service calls typically cost $125-$175.</p>

<h2>Top-Rated Plumbers in Austin</h2>
<ul>
  <li>ABC Plumbing -- 4.9/5 (234 reviews)</li>
  <li>XYZ Plumbers -- 4.7/5 (189 reviews)</li>
</ul>

<h2>Common Plumbing Issues in Austin</h2>
<ul>
  <li>Hard water deposits (limestone aquifer)</li>
  <li>Tree root intrusion (native oak trees)</li>
  <li>Seasonal freeze protection</li>
</ul>

<h2>Austin Plumbing Codes</h2>
<p>Austin follows the 2018 International Plumbing Code with local amendments...</p>
```

Characteristics: educational content, local data/statistics, unique insights, actionable info, internal linking to related topics.

## Pre-Launch Checklist

```markdown
### Content Quality
- [ ] >300 words per page
- [ ] 80%+ unique content
- [ ] Readability grade 8-12
- [ ] No keyword stuffing (1-3% density)
- [ ] Substantive, actionable information

### Technical SEO
- [ ] Unique title tag (50-60 chars)
- [ ] Unique meta description (150-160 chars)
- [ ] Proper heading hierarchy (H1 > H2 > H3)
- [ ] Clean URL structure
- [ ] Internal linking (3-10 links)
- [ ] Schema markup (JSON-LD)
- [ ] Mobile-responsive
- [ ] Page speed <3s

### UX
- [ ] Clear value proposition
- [ ] Easy navigation
- [ ] Accessible (WCAG AA)
- [ ] No intrusive interstitials

### Google Compliance
- [ ] Not a doorway page
- [ ] Not auto-generated spam
- [ ] Not thin content
- [ ] Original research/data
- [ ] Proper attribution/citations
```

## Quality Validation Pipeline

```javascript
class PSEOQualityValidator {
  validate(page) {
    const r = { passed: [], failed: [], warnings: [] };

    const wc = page.content.split(/\s+/).filter(w => w).length;
    if (wc < 300) r.failed.push(`Word count too low: ${wc} (min 300)`);
    else if (wc < 500) r.warnings.push(`Word count low: ${wc}`);
    else r.passed.push(`Word count: ${wc}`);

    const uniq = this.calculateUniqueness(page);   // 0..1, n-gram diff vs corpus
    if (uniq < 0.70) r.failed.push(`Uniqueness ${(uniq*100).toFixed(0)}% (min 70%)`);
    else if (uniq < 0.80) r.warnings.push(`Uniqueness OK: ${(uniq*100).toFixed(0)}%`);

    const dens = this.keywordDensity(page.content, page.primaryKeyword);
    if (dens > 5) r.failed.push(`Keyword stuffing: ${dens.toFixed(1)}%`);
    else if (dens < 1) r.warnings.push(`Density low: ${dens.toFixed(1)}%`);

    const internal = page.links.filter(l => l.internal).length;
    if (internal < 3) r.warnings.push(`Few internal links: ${internal}`);

    return { passed: r.failed.length === 0, ...r };
  }
}
```

## Batch Sampling for Manual Review

```javascript
// Sample N random pages from the set for human review
function sampleForReview(pages, sampleSize = 50) {
  return pages
    .slice().sort(() => 0.5 - Math.random())
    .slice(0, sampleSize)
    .map(p => ({
      url: p.url,
      wordCount: countWords(p.content),
      uniqueness: calculateUniqueness(p),
      keywordDensity: keywordDensity(p.content, p.keyword),
      internalLinks: p.links.filter(l => l.internal).length,
      status: validatePage(p).passed ? 'PASS' : 'FAIL',
    }));
}
```

**Cadence:** review 5-10% of new programmatic pages before publishing. Progressive rollout: batches of 50-100 pages, monitor 2-4 weeks before expanding. Never publish 500+ programmatic pages simultaneously without explicit quality review.

## Common Mistakes

1. Over-optimization (keyword stuffing, unnatural linking)
2. Template visibility (`[VARIABLE]` patterns in live content)
3. Duplicate content (same intro across all pages)
4. Thin pages (<300 words, no unique value)
5. Broken links (dead internal/external)
6. Missing schema (no JSON-LD)
7. Poor UX (slow load, hard navigation)
8. No value-add (pure doorway pages)

## Post-Launch Success Metrics

- **Indexation rate:** >90% of pages indexed
- **Average position:** Top 20 for long-tail target queries
- **CTR:** >2% from search
- **Bounce rate:** <70%
- **Time on page:** >60 seconds
- **Conversion rate:** depends on goal (form, purchase, etc.)
