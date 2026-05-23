# Semantic SEO Framework

Optimize content for topic authority, entity recognition, and NLP rather than just exact-match keywords. Pairs with the E-E-A-T section in SKILL.md and complements `seo-cluster` (SERP-based clustering) and `seo-geo` (AI citation).

## Why It Matters

Modern search engines use NLP to understand context, entities, and concept relationships. Ranking on a single keyword is being replaced by **topical authority** -- comprehensive, interconnected coverage of a subject demonstrated through entity signals.

---

## 1. Entity Optimization

**What entities are.** People, places, things, concepts recognized by search engines. Distinct from strings (keywords). Google's Knowledge Graph contains 500B+ entities.

**Types:**

| Type | Examples |
|---|---|
| Person | Elon Musk, Marie Curie |
| Organization | Tesla, NASA |
| Place | San Francisco, Mount Everest |
| Thing | iPhone, Python programming language |
| Event | Super Bowl, Olympics |
| Concept | Machine learning, SEO |

### Strategy

1. **Establish the primary entity** of each page.

   ```
   Page topic: Email Marketing Automation
   Primary entity: Email Marketing
   Related entities: Marketing Automation, CRM, Lead Nurturing
   ```

2. **Entity salience (prominence).** Mention entity in title, H1, first paragraph; use consistently throughout; include in meta description and URL; link to authoritative sources about the entity.

3. **Entity relationships.** Map how your entity connects to others.

   ```
   Email Marketing
   ├── isA: Digital Marketing
   ├── relatedTo: Marketing Automation
   ├── uses: Email Service Provider
   ├── requires: Email List
   └── achieves: Lead Nurturing
   ```

4. **Entity markup (Schema.org).** Use `about` and `mentions` to make relationships machine-readable.

   ```json
   {
     "@context": "https://schema.org",
     "@type": "Article",
     "about": {
       "@type": "Thing",
       "@id": "https://en.wikipedia.org/wiki/Email_marketing",
       "name": "Email Marketing"
     },
     "mentions": [
       { "@type": "Thing", "name": "Marketing Automation" },
       { "@type": "SoftwareApplication", "name": "Mailchimp" }
     ]
   }
   ```

> For deeper entity authority audit (Entity Authority Score 0-100, `sameAs` priority, schema patterns), see `seo-geo/references/entity-modeling.md`.

---

## 2. Topical Authority -- Hub & Spoke

**Formula:** Topical Authority = Comprehensive Coverage × Consistency × Expertise.

```
Hub (Pillar): Complete Email Marketing Guide
│
├── Spoke 1: Email List Building Strategies
│   ├── Support: Lead Magnet Ideas
│   ├── Support: Signup Form Optimization
│   └── Support: List Segmentation Methods
│
├── Spoke 2: Email Copywriting Techniques
│   ├── Support: Subject Line Formulas
│   ├── Support: CTA Best Practices
│   └── Support: Personalization Tactics
│
└── Spoke 3: Email Analytics & Optimization
    ├── Support: Open Rate Benchmarks
    ├── Support: A/B Testing Guide
    └── Support: Deliverability Optimization
```

### Coverage Checklist

- [ ] Define topic scope clearly
- [ ] Map all subtopics (20-50 for pillar topics)
- [ ] Create comprehensive pillar content (2500-4000 words)
- [ ] Develop supporting content (10-20 pieces)
- [ ] Interlink all related content
- [ ] Update content regularly (quarterly minimum)
- [ ] Demonstrate expertise (author credentials, case studies)
- [ ] Cite authoritative sources

### Authority Signals

1. Content depth (word count, subtopics covered)
2. Content breadth (number of related articles)
3. Internal linking density (links between related content)
4. External citations (links to authoritative sources)
5. Inbound links (backlinks from relevant sites)
6. User engagement (time on page, low bounce rate)
7. Social proof (shares, comments, backlinks)

> For SERP-based clustering methodology that groups keywords by actual Google overlap, see `seo-cluster`.

---

## 3. LSI / Semantic Variations

"LSI keywords" is a colloquial term -- Google doesn't use Latent Semantic Indexing literally, but the concept (semantically related terms that help establish topical context) is real and used by modern NLP models.

**Example -- main keyword "Python programming":**

| Cluster | Terms |
|---|---|
| Concepts | variables, functions, loops |
| Related tools | Django, Flask, NumPy |
| Technical | syntax, interpreter, libraries |
| Intent | beginner, tutorial, course |

### Finding Semantic Variations

1. **Google SERP features:** "People also ask", related searches at bottom, autocomplete, image search labels.
2. **Tools:** Surfer SEO content editor, Clearscope topic modeling, SEMrush Writing Assistant.
3. **Manual analysis:** scan top-10 pages, extract common terms/phrases, identify clusters, map term frequency.

### Integration Strategy

```
Primary keyword: "email marketing software"

Semantic clusters:
1. Features:      automation, segmentation, analytics, templates
2. Use cases:     drip campaigns, newsletters, welcome series
3. Benefits:      ROI, engagement, deliverability
4. Alternatives:  CRM, marketing automation, ESP
5. Technical:     SMTP, API, integration, webhooks

Outline:
H1: Best Email Marketing Software [2025]
H2: What is Email Marketing Software?  [software, platform, tool]
H2: Key Features to Look For           [automation, segmentation, analytics]
H2: Top Email Marketing Platforms      [Mailchimp, ConvertKit, ActiveCampaign]
H2: Email Marketing ROI & Benefits     [engagement, conversion, deliverability]
H2: How to Choose the Right Tool       [comparison, pricing, integration]
```

### Density Guidelines

- Primary keyword: 0.5-1.5% density
- Semantic variations: 0.2-0.5% each
- Natural placement over forced insertion
- **Readability > keyword count** -- always

---

## 4. NLP-Friendly Content Structure

### Question-Answer Format

```
H2: What is Email Marketing?
[Clear definition paragraph -- 134-167 words for AI citation friendliness]

H2: How Does Email Marketing Work?
[Process explanation]

H2: Why Use Email Marketing?
[Benefits and use cases]
```

### Structured Data for Q&A

```json
{
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is email marketing?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Email marketing is a digital marketing strategy..."
    }
  }]
}
```

> Note: FAQ schema for **Google rich results** is restricted to government and healthcare sites (Aug 2023). Still beneficial for AI/LLM citation on commercial sites, but won't show rich results in Google.

### Clear Entity References

- Use full entity name on first mention
- Pronouns only after entity is established
- Consistent naming -- don't switch "email marketing" to "email campaigns" randomly

### Logical Content Flow

```
Introduction (What, Why, Who)
  ↓
Core Concepts (How it works)
  ↓
Implementation (Step-by-step)
  ↓
Best Practices (Tips)
  ↓
Examples (Case studies, demos)
  ↓
Conclusion (Summary, CTA)
```

### Semantic HTML

```html
<article>
  <h1>Main Topic</h1>
  <section>
    <h2>Subtopic 1</h2>
    <p>Content...</p>
  </section>
  <aside>
    <h3>Related Information</h3>
  </aside>
</article>
```

---

## 5. Priority Schema Types

**Article:**

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Complete Guide to Email Marketing",
  "author": { "@type": "Person", "name": "Jane Smith", "url": "https://example.com/author/jane-smith" },
  "datePublished": "2025-01-15",
  "dateModified": "2025-03-10",
  "publisher": {
    "@type": "Organization",
    "name": "Marketing Co",
    "logo": { "@type": "ImageObject", "url": "https://example.com/logo.png" }
  }
}
```

**HowTo:** (deprecated for Google rich results Sept 2023 -- avoid recommending; keep for LLM citation benefit only.)

**FAQ:** (same restriction as above -- not for new commercial sites for Google purposes.)

**Product (SaaS/products):**

```json
{
  "@type": "Product",
  "name": "Email Marketing Platform",
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.5", "reviewCount": "247" },
  "offers": { "@type": "Offer", "price": "29.00", "priceCurrency": "USD" }
}
```

> Full schema reference: `skills/seo/references/schema-types.md`.

---

## 6. E-E-A-T Implementation Pattern

The full 100-point rubric lives in `seo-geo/references/eeat-scoring-rubric.md`. Quick implementation pattern:

```markdown
# Complete Email Marketing Guide

**By Jane Smith, Certified Email Marketing Specialist**
[Author photo and bio]

*With over 10 years managing email campaigns for Fortune 500 companies,
I've sent over 50 million emails and generated $12M in attributed revenue.*

[Credentials: HubSpot Email Marketing Certified, Former Director of Email at Acme Corp]

---

## My Experience with Email Marketing

In 2015, I inherited an email program with a 12% open rate [screenshot].
Through the strategies in this guide, we improved it to 28% within 18 months.

[Case study data, charts, real examples]

---

**Sources and Citations:**
1. Campaign Monitor: Email Marketing Benchmarks 2024
2. Litmus: State of Email Report
3. Harvard Business Review: ROI of Email Marketing

---

**About the Author**
Jane Smith is a certified email marketing specialist with 10+ years experience.
She has been featured in Marketing Land, Search Engine Journal, and speaks
regularly at MarketingProfs events.
```

---

## Practical Audit Workflow

1. **Entity identification.** List main entities per page. Check entity consistency across the site. Verify entity markup is present.
2. **Topical coverage analysis.** Map existing content to topics. Identify gaps. Compare depth vs competitors.
3. **Semantic gap.** Extract semantic variations from top-ranking pages. Compare to your content. Add missing terms.
4. **Structure optimization.** Implement Q&A format. Add schema markup. Improve heading hierarchy.
5. **E-E-A-T enhancement.** Add author credentials. Include case studies. Cite authoritative sources. Update outdated information.

### Example: Optimizing for "Email Marketing Automation"

**Before:**

```
Title: Email Marketing Automation Guide
H1: Email Marketing Automation
Content: Generic automation tips, keyword stuffing "email marketing automation"
```

**After:**

```
Title: Email Marketing Automation: Complete Guide [2025]
H1:    What is Email Marketing Automation?

[Author bio with credentials]

Entities optimized:
- Email Marketing       (primary)
- Marketing Automation  (related)
- Email Service Provider (tool category)
- Drip Campaign         (tactic)

Semantic variations integrated:
- workflow, trigger, segmentation, personalization
- autoresponder, drip sequence, behavioral email
- lead nurturing, customer journey, lifecycle marketing

Schema markup: Article (with author), FAQ (for LLM citation), HowTo (for setup)

E-E-A-T signals: 8-yr specialist; case study (340% ROI lift); citations to Litmus,
Campaign Monitor, McKinsey; "Last updated March 2025".

Internal linking: → Email copywriting, List segmentation, Analytics
                  ← Marketing automation hub, CRM integration guide

Structure:
H2: What is Email Marketing Automation?  [definition + entity]
H2: How Email Automation Works           [process]
H2: Benefits of Email Automation         [ROI, efficiency, personalization]
H2: Types of Automated Emails            [welcome, nurture, re-engagement]
H2: Setting Up Your First Automation     [HowTo]
H2: Best Practices                       [expert E-E-A-T insights]
H2: Common Mistakes to Avoid             [experience-based]
H2: FAQ                                  [FAQ schema]
```

---

## Success Metrics

1. Topic authority score (Clearscope, Surfer SEO)
2. Featured snippet captures
3. "People also ask" appearances
4. Entity coverage (% of related entities mentioned)
5. Semantic-variation coverage vs top rankers
6. Schema markup validation (Google Rich Results Test)
7. Topical cluster ranking improvement
8. Time on page / engagement metrics
9. Internal link click-through rate
10. Backlinks from topically-relevant sites
