# pSEO Templates & URL Structure

Practical patterns for template engines (Nunjucks-style) and URL generation in programmatic SEO. Pairs with the "Template Engine Planning" and "URL Pattern Strategy" sections in SKILL.md.

---

## Part 1 -- Template Syntax (Nunjucks-style)

### Variable Interpolation

```nunjucks
{{ variable }}
{{ object.property }}
{{ array[0] }}
```

```html
<h1>{{ service }} in {{ city }}</h1>
<p>Average cost: ${{ price | formatNumber }}</p>
```

### Loops

```nunjucks
{% for item in items %}
  <li>{{ item.name }}</li>
{% endfor %}
```

**FAQ block with embedded microdata:**

```html
{% for qa in faqs %}
<div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question">
  <h3 itemprop="name">{{ qa.question }}</h3>
  <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
    <p itemprop="text">{{ qa.answer }}</p>
  </div>
</div>
{% endfor %}
```

### Conditionals

```nunjucks
{% if rating >= 4.5 %}
  <span class="badge-excellent">Excellent</span>
{% elif rating >= 3.5 %}
  <span class="badge-good">Good</span>
{% else %}
  <span class="badge-fair">Fair</span>
{% endif %}
```

### Common Filters

```nunjucks
{{ text | upper }}              <!-- UPPERCASE -->
{{ text | lower }}              <!-- lowercase -->
{{ text | capitalize }}         <!-- Capitalize first -->
{{ text | truncate(100) }}      <!-- Truncate to 100 chars -->
{{ number | formatNumber }}     <!-- 1,234.56 -->
{{ date | formatDate }}         <!-- Jan 1, 2025 -->
{{ url | slugify }}             <!-- my-url-slug -->
```

Custom filter implementation:

```javascript
filters: {
  formatNumber: (n) => n.toLocaleString('en-US'),
  slugify: (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''),
  truncate: (s, l) => s.length > l ? s.slice(0, l) + '...' : s,
}
```

### Layout Inheritance

```html
<!-- layouts/base.html -->
<!DOCTYPE html>
<html>
<head>
  <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>
  {% block content %}{% endblock %}
</body>
</html>

<!-- pages/location.html -->
{% extends "layouts/base.html" %}
{% block title %}{{ service }} in {{ city }}{% endblock %}
{% block content %}
  <h1>{{ service }} in {{ city }}</h1>
  {% include "partials/service-list.html" %}
{% endblock %}
```

### Full Location Page Template

```html
{% extends "layouts/base.html" %}

{% block title %}{{ service }} in {{ city }}, {{ state }} - {{ brand }}{% endblock %}

{% block meta %}
<meta name="description" content="Find the best {{ service | lower }} in {{ city }}. {{ rating | formatNumber }} stars from {{ reviewCount }} reviews.">
{% endblock %}

{% block content %}
<article>
  <h1>{{ service }} in {{ city }}, {{ state }}</h1>

  <div class="intro">
    <p>{{ introText }}</p>
    <div class="stats">
      <span>⭐ {{ rating }}/5.0</span>
      <span>💬 {{ reviewCount }} reviews</span>
      <span>📍 {{ businessCount }} providers</span>
    </div>
  </div>

  <h2>Top {{ service }} Providers in {{ city }}</h2>
  <ul class="providers">
  {% for provider in topProviders %}
    <li>
      <h3>{{ provider.name }}</h3>
      <p>{{ provider.description | truncate(120) }}</p>
      <span class="price">From ${{ provider.price | formatNumber }}</span>
    </li>
  {% endfor %}
  </ul>

  {% if faqs.length > 0 %}
  <h2>Frequently Asked Questions</h2>
  {% for faq in faqs %}
  <div class="faq-item">
    <h3>{{ faq.question }}</h3>
    <p>{{ faq.answer }}</p>
  </div>
  {% endfor %}
  {% endif %}

  <h2>Related Services in {{ city }}</h2>
  <nav class="related">
  {% for related in relatedServices %}
    <a href="{{ related.url }}">{{ related.title }}</a>
  {% endfor %}
  </nav>
</article>
{% endblock %}
```

### Template Best Practices

1. Descriptive variable names in `camelCase` or `snake_case`.
2. Filter chaining: `{{ text | truncate(100) | capitalize }}`.
3. Whitespace control: `{%- for -%}` strips surrounding whitespace.
4. Safe output: most engines auto-escape HTML by default.
5. Comments: `{# this is a comment #}`.

---

## Part 2 -- URL Structure

### Recommended URL Patterns

| Use Case | Pattern | Example |
|---|---|---|
| Location service | `/{service}/{location}/` | `/plumber/austin-tx/` |
| Comparison | `/{item-a}-vs-{item-b}/` | `/notion-vs-coda/` |
| Integration | `/{a}-{b}-integration/` | `/slack-asana-integration/` |
| Glossary | `/glossary/{term}/` or `/what-is/{term}/` | `/glossary/api/` |
| Statistics | `/{topic}-statistics/` or `/stats/{topic}-{year}/` | `/remote-work-statistics/` |
| Multi-variable | `/{category}/{subcategory}/{location}/` | `/healthcare/dentist/austin-tx/` |

> **Service vs Location order:** `/{service}/{location}/` is usually better because the service is the broader category. Pick one convention site-wide.

### Generation Rules

1. **Lowercase only** -- `/plumber/austin-tx/` not `/Plumber/Austin-TX/`
2. **Hyphens, not underscores or spaces** -- `/new-york-plumber/`
3. **<75 characters** -- truncate or use abbreviations for long names
4. **Strip special chars** -- accents, punctuation, symbols
5. **Pick a trailing-slash convention** -- always `/` (recommended) or never; don't mix

### Slug Sanitizer

```javascript
function sanitize(str) {
  return String(str)
    .toLowerCase()
    .normalize('NFD')                    // handle accented chars
    .replace(/[̀-ͯ]/g, '')     // strip diacritics
    .replace(/[^a-z0-9\s-]/g, '')        // remove specials
    .replace(/\s+/g, '-')                // spaces to hyphens
    .replace(/-+/g, '-')                 // collapse hyphens
    .replace(/^-|-$/g, '');              // trim edges
}

sanitize("Austin, TX")            // → "austin-tx"
sanitize("React.js vs Vue.js")    // → "reactjs-vs-vuejs"
sanitize("What is API?")          // → "what-is-api"
```

### Slug Generator (with length cap and dedup)

```javascript
class PSEOURLGenerator {
  constructor({ maxLength = 75, baseUrl = '', trailingSlash = true } = {}) {
    this.maxLength = maxLength;
    this.baseUrl = baseUrl;
    this.trailingSlash = trailingSlash;
    this.usedUrls = new Set();
  }

  generate(data, pattern) {
    let url = pattern;
    Object.entries(data).forEach(([k, v]) => {
      url = url.replace(new RegExp(`{${k}}`, 'g'), v);
    });
    url = this.sanitize(url);
    url = this.enforceLength(url);
    url = this.normalize(url);

    if (this.usedUrls.has(url)) throw new Error(`Duplicate URL: ${url}`);
    this.usedUrls.add(url);
    return this.baseUrl + url;
  }

  sanitize(url) {
    return url
      .toLowerCase().normalize('NFD')
      .replace(/[̀-ͯ]/g, '')
      .replace(/[^a-z0-9\/\s-]/g, '')
      .replace(/\s+/g, '-').replace(/-+/g, '-')
      .replace(/\/-\//g, '/').replace(/^-|-$/g, '');
  }

  enforceLength(url) {
    if (url.length <= this.maxLength) return url;
    const parts = url.split('/');
    while (parts.join('/').length > this.maxLength && parts.length > 2) parts.pop();
    return parts.join('/');
  }

  normalize(url) {
    if (!url.startsWith('/')) url = '/' + url;
    if (this.trailingSlash && !url.endsWith('/')) url += '/';
    else if (!this.trailingSlash && url.endsWith('/')) url = url.slice(0, -1);
    return url;
  }
}

const g = new PSEOURLGenerator({ baseUrl: 'https://example.com' });
g.generate({ service: 'Plumber', city: 'Austin', state: 'TX' }, '/{service}/{city}-{state}');
// → 'https://example.com/plumber/austin-tx/'
```

### Duplicate Detection (pre-generation)

```javascript
function detectDuplicates(data, pattern) {
  const urls = {};
  data.forEach((item, i) => {
    const url = sanitize(applyPattern(pattern, item));
    if (urls[url] !== undefined) {
      console.warn(`Duplicate URL: ${url}`);
      console.warn(`  Item ${urls[url]}: ${JSON.stringify(data[urls[url]])}`);
      console.warn(`  Item ${i}: ${JSON.stringify(item)}`);
    } else {
      urls[url] = i;
    }
  });
  return Object.keys(urls).length === data.length;
}
```

### Canonical Map for Variations

```javascript
// Multiple URL forms point to the same canonical
const urlMap = {
  '/plumber/austin/':           '/plumber/austin-tx/',
  '/austin-plumber/':           '/plumber/austin-tx/',
  '/plumbing-austin-texas/':    '/plumber/austin-tx/',
};
function getCanonical(currentUrl) { return urlMap[currentUrl] || currentUrl; }
```

### URL Validation

```javascript
function validateUrl(url) {
  const rules = {
    lowercase:        /^[a-z0-9\/-]+$/.test(url),
    length:           url.length <= 75,
    noSpecialChars:   !/[^a-z0-9\/-]/.test(url),
    noDoubleSlash:    !url.includes('//'),
    noTrailingHyphen: !url.match(/-\//),
  };
  const failed = Object.keys(rules).filter(r => !rules[r]);
  return { valid: failed.length === 0, failed };
}
```

### Query Parameters

```javascript
// Bad: query params for content variation
url: '/plumber?city=austin&state=tx'

// Good: baked into path
url: '/plumber/austin-tx/'

// Filter/sort params are OK for UX, but canonical points to base
url:       '/plumber/austin-tx/?sort=rating&filter=emergency'
canonical: '/plumber/austin-tx/'
```

### Multi-Level Hierarchy Example

```javascript
const hierarchy = {
  healthcare: { dentist: ['austin-tx', 'miami-fl'], doctor: ['austin-tx', 'miami-fl'] },
  legal:      { lawyer: ['austin-tx', 'miami-fl'] },
};

const urls = [];
for (const cat in hierarchy) {
  for (const sub in hierarchy[cat]) {
    for (const loc of hierarchy[cat][sub]) {
      urls.push(`/${cat}/${sub}/${loc}/`);
    }
  }
}
// → /healthcare/dentist/austin-tx/, /healthcare/dentist/miami-fl/, ...
```

### Integration Matrix Example

```javascript
const tools = ['slack', 'asana', 'trello', 'notion'];
const urls = [];
for (const a of tools) for (const b of tools) {
  if (a !== b) urls.push(`/integrations/${a}-${b}/`);
}
```

## Summary

- URLs: short (<75 chars), hyphenated, lowercase, hierarchical, no parameters for primary content, dedup-validated at generation time.
- Templates: extend a base layout, escape by default, chain filters, use semantic HTML, embed schema microdata where it makes sense.
- Always pre-validate: duplicate detection, character sanity, length cap, trailing-slash consistency.
