# Entity Modeling Framework

Build and optimize knowledge graph entities for AI search visibility and knowledge panel presence.

## When to Use

- Building entity authority for knowledge panels
- Optimizing for AI answer engine entity recognition
- Establishing entity relationships between brands, products, people, topics
- Auditing existing entity signals on a site

## Core Concept

AI answer engines (ChatGPT, Perplexity, Gemini, Claude) rely on **entity graphs** -- structured knowledge about people, organizations, products, and topics -- to generate answers. Strong entity signals = higher citation probability.

## Entity Types

| Type | Examples | Key Signals |
|---|---|---|
| **Organization** | Companies, brands, nonprofits | `Organization` schema, Wikipedia, Wikidata QID, consistent NAP |
| **Person** | Authors, founders, experts | `Person` schema, `sameAs` links, byline consistency, E-E-A-T |
| **Product** | Software, physical goods | `Product`/`SoftwareApplication` schema, reviews, pricing |
| **Topic** | Industry terms, methodologies | `DefinedTerm` schema, authoritative definitions, pillar content |
| **Place** | Locations, service areas | `Place`/`LocalBusiness` schema, Google Business Profile |

## Entity Authority Score (0-100)

| Category | Weight | Checks |
|---|---|---|
| Schema markup coverage | 25% | JSON-LD for primary entity type present |
| `sameAs` links | 20% | Links to Wikipedia, Wikidata, LinkedIn, Crunchbase, social profiles |
| Consistent naming | 15% | Same entity name across all pages, no variations |
| External mentions | 15% | Brand mentioned on authoritative third-party sites |
| Content depth | 15% | Dedicated entity pages (About, Team, Product) with comprehensive info |
| Inter-entity links | 10% | Clear relationships: author → organization, product → brand |

### Grade Scale

| Grade | Score | Meaning |
|---|---|---|
| A | ≥80 | Strong entity -- likely in knowledge graph |
| B | ≥60 | Recognized entity -- partial knowledge graph presence |
| C | ≥40 | Weak entity -- AI engines may not confidently identify |
| D | ≥20 | Fragmented entity -- conflicting signals |
| F | <20 | No entity presence -- invisible to AI engines |

## Entity Audit Steps

### Step 1: Identify Primary Entities

List all entities the site needs to be known for:

```markdown
- Organization: [Company Name]
- People: [Founder], [Key Authors]
- Products: [Product 1], [Product 2]
- Topics: [Core Topic 1], [Core Topic 2]
```

### Step 2: Check Schema Coverage

For each entity, verify JSON-LD structured data exists:

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://example.com/#organization",
  "name": "Example Corp",
  "url": "https://example.com",
  "sameAs": [
    "https://www.wikidata.org/wiki/Q12345",
    "https://www.linkedin.com/company/example",
    "https://twitter.com/example"
  ]
}
```

### Step 3: Verify `sameAs` Links

Check that each entity has verified `sameAs` links to authoritative sources:

| Priority | Platform | Why |
|---|---|---|
| 1 | Wikidata | Primary knowledge graph source for AI engines |
| 2 | Wikipedia | High authority, directly used by AI |
| 3 | LinkedIn | Professional identity verification |
| 4 | Crunchbase | Business entity verification |
| 5 | Social profiles | Consistency signals |

### Step 4: Check Naming Consistency

Search the site for entity name variations and flag any inconsistencies -- AI engines build entity confidence from consistent naming.

### Step 5: Map Entity Relationships

Build a relationship map using `subjectOf`, `author`, `brand`, `manufacturer`:

```
Organization ─author→ Person (Author)
Organization ─brand→ Product
Person ─subjectOf→ Article
Product ─review→ Review
```

### Step 6: Score & Report

Compute Entity Authority Score using the weights above. Generate actionable recommendations sorted by impact.

## Pitfalls

- ❌ Creating entity schema without verifiable `sameAs` links (AI engines check)
- ❌ Claiming Wikidata QIDs that don't exist (will hurt trust)
- ❌ Inconsistent entity naming across pages
- ❌ Entity schema on one page only -- should be site-wide
- ❌ Ignoring inter-entity relationships (author ↔ organization)
