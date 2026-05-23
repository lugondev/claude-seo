# pSEO Scale Architecture

Patterns for generating and managing 100k+ programmatic pages reliably. Covers batch processing, parallel workers, checkpoint/resume, validation, storage, and CDN deployment.

## Pipeline Overview

```
Data Source → Batch Chunking → Parallel Generate → Quality Validate
                                       ↓                  ↓
                                 Checkpoint        Output Writer
                                       ↓                  ↓
                                  Storage  ←  Index/Sitemap Gen
                                       ↓
                                  CDN Deploy
```

## Batch Processing -- 1000 Rows / Chunk

Why 1000?

- Memory efficient (prevents OOM on large datasets)
- Progress visible (checkpoint every 1000)
- Retry scope limited (only reprocess 1000 on failure)
- Optimal for parallel distribution

```javascript
class BatchProcessor {
  constructor({ chunkSize = 1000 } = {}) {
    this.chunkSize = chunkSize;
    this.checkpoint = new CheckpointManager();
  }

  async process(data, processor) {
    const chunks = this.chunk(data, this.chunkSize);
    const results = [];

    for (let i = 0; i < chunks.length; i++) {
      const id = `chunk_${i}`;
      if (this.checkpoint.isComplete(id)) {
        console.log(`Skip chunk ${i} (already complete)`);
        continue;
      }
      console.log(`Processing chunk ${i}/${chunks.length} (${chunks[i].length} items)`);
      try {
        const out = await processor(chunks[i], i);
        results.push(...out);
        this.checkpoint.markComplete(id, out);
      } catch (e) {
        this.checkpoint.markFailed(id, e);
        throw e;
      }
    }
    return results;
  }

  chunk(arr, n) {
    const out = [];
    for (let i = 0; i < arr.length; i += n) out.push(arr.slice(i, i + n));
    return out;
  }
}
```

## Parallel Workers -- 4-8 Pool

Default worker count: `min(8, os.cpus().length)`. Going past 8 rarely pays off because template rendering is CPU-bound but the bottleneck shifts to file I/O.

```javascript
const { Worker } = require('worker_threads');
const os = require('os');

class WorkerPool {
  constructor(workerScript, { maxWorkers = Math.min(8, os.cpus().length) } = {}) {
    this.workerScript = workerScript;
    this.maxWorkers = maxWorkers;
  }

  async execute(tasks) {
    return new Promise((resolve, reject) => {
      const results = [];
      let completed = 0;
      const queue = tasks.slice();
      const workers = [];

      for (let i = 0; i < Math.min(this.maxWorkers, tasks.length); i++) {
        const w = new Worker(this.workerScript);
        workers.push(w);
        w.on('message', (r) => {
          results.push(r);
          completed++;
          if (queue.length) w.postMessage(queue.shift());
          else w.terminate();
          if (completed === tasks.length) resolve(results);
        });
        w.on('error', reject);
        w.postMessage(queue.shift());
      }
    });
  }
}
```

**Worker script (renders one chunk's worth of pages):**

```javascript
// worker.js
const { parentPort } = require('worker_threads');
const Nunjucks = require('nunjucks');

parentPort.on('message', async (task) => {
  try {
    const pages = task.data.map(row => ({
      url: generateUrl(row),
      content: Nunjucks.renderString(task.template, row),
      metadata: extractMetadata(row),
    }));
    parentPort.postMessage({ chunkId: task.chunkId, pages, success: true });
  } catch (e) {
    parentPort.postMessage({ chunkId: task.chunkId, error: e.message, success: false });
  }
});
```

## Checkpoint / Resume

Persist progress so a 67-minute job survives crashes.

```javascript
const fs = require('fs');
const path = require('path');

class CheckpointManager {
  constructor(dir = './checkpoints') {
    this.dir = dir;
    this.file = path.join(dir, 'progress.json');
    this.state = fs.existsSync(this.file)
      ? JSON.parse(fs.readFileSync(this.file, 'utf8'))
      : { completed: [], failed: [], lastUpdate: null };
  }

  save() {
    fs.mkdirSync(this.dir, { recursive: true });
    fs.writeFileSync(this.file, JSON.stringify(this.state, null, 2));
  }

  isComplete(id)         { return this.state.completed.includes(id); }
  markComplete(id, out)  {
    if (!this.isComplete(id)) this.state.completed.push(id);
    fs.writeFileSync(path.join(this.dir, `${id}.json`), JSON.stringify(out, null, 2));
    this.state.lastUpdate = new Date().toISOString();
    this.save();
  }
  markFailed(id, e) {
    this.state.failed.push({ id, error: e.message, ts: new Date().toISOString() });
    this.save();
  }

  resume(total) {
    return Array.from({ length: total }, (_, i) => `chunk_${i}`)
      .filter(id => !this.isComplete(id));
  }
}
```

## Quality Validation per Batch

Run validation after each chunk and **fail fast** if too many pages are bad.

```javascript
class BatchQualityValidator {
  validate(pages) {
    const report = { total: pages.length, passed: 0, failed: 0, warnings: 0, issues: [] };

    for (const page of pages) {
      const v = this.checkPage(page);
      if (v.failed.length) {
        report.failed++;
        report.issues.push({ url: page.url, errors: v.failed });
      } else if (v.warnings.length) {
        report.warnings++;
        report.issues.push({ url: page.url, warnings: v.warnings });
      } else {
        report.passed++;
      }
    }
    return report;
  }

  checkPage(page) {
    const f = [], w = [];
    const words = page.content.split(/\s+/).length;
    if (words < 300) f.push(`Word count too low: ${words}`);

    const title = page.content.match(/<title>(.+?)<\/title>/)?.[1];
    if (!title) f.push('Missing title tag');
    else if (title.length < 30 || title.length > 60) w.push(`Title length: ${title.length} (ideal 50-60)`);

    if (!/meta name="description" content="(.+?)"/.test(page.content)) f.push('Missing meta description');

    const h1s = (page.content.match(/<h1/g) || []).length;
    if (h1s !== 1) f.push(`H1 count: ${h1s} (should be 1)`);

    return { failed: f, warnings: w };
  }
}
```

**Failure threshold rule:** if `failed > 10%` of the batch, abort the pipeline. Don't blindly push 1000 bad pages to production.

## Performance Benchmarks

Reference numbers for capacity planning (varies by template complexity, validation depth, disk speed):

| Pages | Workers | Time | Storage | Strategy |
|---|---|---|---|---|
| 1k | 1 | 3 min | File | Single process |
| 10k | 4 | 10 min | File | Worker pool |
| 100k | 6 | 67 min | DB | Batch + checkpoint |
| 1M+ | 8 | 11 hrs | DB + CDN | Distributed workers |

Per-page cost breakdown (single thread):

- Template rendering: ~0.1s
- Quality validation: ~0.05s
- File write: ~0.01s
- Total: ~0.16s/page = ~375 pages/min single-threaded
- 6 workers: ~1,500 pages/min actual (accounting for orchestration overhead)

## Storage Strategy

### File System (recommended for <100k pages)

```javascript
class FileSystemStorage {
  constructor(outputDir = './dist') { this.outputDir = outputDir; }

  async savePage(page) {
    const fp = path.join(this.outputDir, page.url, 'index.html');
    await fs.promises.mkdir(path.dirname(fp), { recursive: true });
    await fs.promises.writeFile(fp, page.content);
    return fp;
  }

  async saveBatch(pages) {
    return Promise.all(pages.map(p => this.savePage(p)));
  }

  async generateSitemap(pages, base = 'https://example.com') {
    const entries = pages.map(p => `
  <url>
    <loc>${base}${p.url}</loc>
    <lastmod>${new Date().toISOString().split('T')[0]}</lastmod>
    <changefreq>monthly</changefreq>
  </url>`).join('');

    const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${entries}
</urlset>`;
    await fs.promises.writeFile(path.join(this.outputDir, 'sitemap.xml'), xml);
  }
}
```

### Database (recommended for >100k pages)

SQLite or Postgres -- indexed on `url`, transactional batch insert, and supports incremental re-export to files.

```javascript
const sqlite3 = require('sqlite3');

class DatabaseStorage {
  constructor(dbPath = './pages.db') {
    this.db = new sqlite3.Database(dbPath);
    this.run = (...a) => new Promise((r, j) => this.db.run(...a, (e) => e ? j(e) : r()));
    this.init();
  }

  async init() {
    await this.run(`CREATE TABLE IF NOT EXISTS pages (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      url TEXT UNIQUE, title TEXT, content TEXT,
      meta_description TEXT, word_count INTEGER,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP)`);
    await this.run(`CREATE INDEX IF NOT EXISTS idx_url ON pages(url)`);
  }

  async saveBatch(pages) {
    await this.run('BEGIN TRANSACTION');
    try {
      for (const p of pages) {
        const wc = p.content.split(/\s+/).length;
        await this.run(
          `INSERT OR REPLACE INTO pages (url, title, content, meta_description, word_count)
           VALUES (?, ?, ?, ?, ?)`,
          [p.url, p.title, p.content, p.metaDescription, wc]
        );
      }
      await this.run('COMMIT');
    } catch (e) {
      await this.run('ROLLBACK');
      throw e;
    }
  }
}
```

## CDN / Cache Headers

```javascript
const cacheHeaders = {
  // Static pages: 1 day origin, 1 week CDN
  static: {
    'Cache-Control':     'public, max-age=86400, s-maxage=86400',
    'CDN-Cache-Control': 'max-age=604800',
    'Vary':              'Accept-Encoding',
  },
  // Dynamic pages: shorter
  dynamic: {
    'Cache-Control':     'public, max-age=3600, s-maxage=3600',
    'CDN-Cache-Control': 'max-age=86400',
    'Vary':              'Accept-Encoding',
  },
};
```

**Deployment skeleton (S3 + CloudFront):**

```javascript
async function deploy(distDir) {
  const files = glob.sync('**/*', { cwd: distDir, nodir: true });
  await Promise.all(files.map(f => s3.putObject({
    Bucket: BUCKET, Key: f,
    Body: fs.readFileSync(path.join(distDir, f)),
    ContentType: contentTypeFor(f),
    CacheControl: 'public, max-age=86400',
  }).promise()));
  await cloudfront.createInvalidation({
    DistributionId: DIST_ID,
    InvalidationBatch: { CallerReference: String(Date.now()), Paths: { Quantity: 1, Items: ['/*'] } },
  }).promise();
}
```

## Complete Pipeline (sketch)

```javascript
async function generatePSEOSite(dataFile, config) {
  const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
  console.log(`Loaded ${data.length} rows`);

  const storage  = new FileSystemStorage('./dist');
  const validator = new BatchQualityValidator();
  const processor = new BatchProcessor({ chunkSize: 1000 });

  const allPages = await processor.process(data, async (chunk, idx) => {
    const pool = new WorkerPool('./worker.js', { maxWorkers: 6 });
    const tasks = chunk.map(row => ({ data: row, template: config.template }));
    const pages = await pool.execute(tasks);

    const v = validator.validate(pages);
    console.log(`Chunk ${idx}: ${v.passed}/${v.total} passed`);
    if (v.failed > v.total * 0.1) throw new Error(`Too many failures in chunk ${idx}`);

    await storage.saveBatch(pages);
    return pages;
  });

  await storage.generateSitemap(allPages);
  console.log(`✓ Generated ${allPages.length} pages`);
}
```

## Operational Checklist

- [ ] Chunk size = 1000 (adjust if memory-constrained)
- [ ] 4-8 workers; not more (diminishing returns)
- [ ] Checkpoint after every chunk; resume on restart
- [ ] Quality validation per chunk; abort if failure rate >10%
- [ ] File system for <100k pages, DB for >100k pages
- [ ] CDN cache: 1 week for static pSEO pages
- [ ] Sitemap split at 50k URLs (protocol limit)
- [ ] `<lastmod>` reflects data update timestamp, not generation time
- [ ] Progressive rollout: publish batches of 50-100, monitor 2-4 weeks
