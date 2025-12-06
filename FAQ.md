# Web Crawler - FAQ & Best Practices

## Frequently Asked Questions

### Installation & Setup

**Q: How do I install and run the crawler?**
```bash
cd your_project_directory
source .venv/bin/activate
python3 app.py
# Open http://localhost:5000
```

**Q: Do I need to install anything?**
A: No, everything is already in `requirements.txt`. Just activate the virtual environment.

**Q: What if I get "command not found" errors?**
A: Make sure you've activated the virtual environment:
```bash
source .venv/bin/activate
```

---

### Crawling Questions

**Q: Why is crawling so slow?**
A: The 2-second delay is for politeness. Reduce it:
```python
crawler = WebCrawler(
    seed_url="http://example.com",
    delay=0.5  # 0.5 seconds instead of 2
)
```

**Q: Can I crawl multiple domains?**
A: No, one crawl at a time. The URLFrontier filters for internal links only (same domain). If you want to crawl multiple domains, run separate crawls.

**Q: What happens if a page fails to load?**
A: It's logged as an error and skipped. Crawling continues with the next URL.

**Q: Can I stop crawling midway?**
A: Yes, press Ctrl+C in the terminal. Data crawled so far is saved.

**Q: Does it support JavaScript-rendered content?**
A: No, only static HTML. For JavaScript content, you'd need Selenium or Puppeteer.

---

### Search Questions

**Q: Why aren't my search results showing?**
A: Make sure you've:
1. Crawled pages first (Crawl tab)
2. Waited for indexing to complete
3. Search returned results (check Browse tab)
4. Used valid keywords (not pure stopwords)

**Q: Can I search by domain or date?**
A: Not yet. Current search is text-based only. See ARCHITECTURE.md for advanced features.

**Q: Why are results different each time?**
A: Results should be consistent. If different, the database might be corrupt. Try clearing with the "Clear All" button.

**Q: Can I search for exact phrases?**
A: Not in current version. See Future Improvements section.

---

### Database Questions

**Q: Where is the database stored?**
A: `crawler.db` in the project root directory.

**Q: Can I use a different database?**
A: Currently only SQLite. To use PostgreSQL/MySQL, modify `storage/database.py`.

**Q: How big can the database grow?**
A: ~5-10MB for 100 pages, depends on page size. No hard limit.

**Q: Can I backup the database?**
A: Yes, simply copy `crawler.db` to another location.

**Q: Can multiple instances share the database?**
A: Not recommended (SQLite locks). Use PostgreSQL for multi-instance.

---

### Performance Questions

**Q: How many pages can I crawl?**
A: Limited only by time and memory. Tested with 500+ pages.

**Q: What's the maximum query time?**
A: Should be <100ms even for large indexes. If slower, rebuild index.

**Q: Why is indexing taking so long?**
A: Calculating TF-IDF for 1000+ words takes time. See COMPLETE_GUIDE.md for optimization.

**Q: Can I index in background?**
A: Modify `app.py` to use threading/celery tasks for indexing.

---

### Technical Questions

**Q: What Python version do I need?**
A: Python 3.7+. Tested on 3.9+.

**Q: What libraries are required?**
A: See `requirements.txt` - main ones are:
- requests (HTTP)
- beautifulsoup4 (HTML parsing)
- flask (Web server)

**Q: Can I deploy to production?**
A: Not as-is. You'd need:
- Production WSGI server (gunicorn)
- Load balancer (nginx)
- PostgreSQL instead of SQLite
- HTTPS/SSL
- Rate limiting

**Q: How do I modify the code?**
A: Each component is modular:
- Change crawling: Edit `crawler/crawl.py`
- Change search: Edit `indexer/indexer.py`
- Change UI: Edit `templates/index.html`

---

### Troubleshooting Questions

**Q: I get "connection refused" error**
A: Website might be down or blocking your IP. Check:
1. Internet connection
2. Website is accessible in browser
3. Try different delay
4. Check firewall

**Q: Database is locked**
A: Another process is accessing it. Kill Flask app:
```bash
# Find Flask process
ps aux | grep flask

# Kill it
kill -9 <PID>

# Restart
python3 app.py
```

**Q: Out of memory error**
A: Crawled too many pages. Solution:
```python
# Reduce max_pages
crawler = WebCrawler(seed_url="...", max_pages=50)

# Or clear database and start fresh
rm crawler.db
```

**Q: No search results for valid keyword**
A: Possible issues:
1. Keyword not in crawled pages (try different keyword)
2. Keyword is pure stopword (like "the", "a", "and")
3. Database not indexed properly (click Crawl again)

**Q: Flask won't start on port 5000**
A: Port already in use. Find and kill process:
```bash
lsof -i :5000
kill -9 <PID>
```

---

## Best Practices

### Crawling Best Practices

✅ **DO:**
- Use reasonable delays (1-5 seconds)
- Crawl during off-peak hours
- Respect robots.txt (implement checking)
- Use descriptive User-Agent headers
- Cache results locally
- Handle errors gracefully

❌ **DON'T:**
- Use 0 delay (too aggressive)
- Crawl thousands of pages rapidly
- Ignore rate limit errors (403, 429)
- Share crawlers across databases
- Delete database while crawler running

### Search Best Practices

✅ **DO:**
- Use 2-3 word queries for best results
- Crawl 50+ pages for good ranking
- Clear data between crawl sessions if needed
- Check spelling of search terms

❌ **DON'T:**
- Search on empty database
- Use pure stopwords only
- Expect phrase search (not implemented)
- Modify database directly

### Development Best Practices

✅ **DO:**
- Keep separate development/production DBs
- Test with small page counts first (5-10)
- Use version control (git)
- Log all crawling activity
- Document any modifications

❌ **DON'T:**
- Modify database.py without testing
- Use production database for testing
- Hard-code URLs or credentials
- Remove error handling
- Ignore logs

---

## Performance Optimization Tips

### Faster Crawling

```python
# Reduce delay
crawler = WebCrawler(
    seed_url="http://example.com",
    max_pages=100,
    delay=0.5  # Faster
)

# Or from UI: Set delay to 0.5
```

### Faster Search

```python
# Use specific keywords
"python framework" ✓ (more specific)
"python" ✗ (too common)

# Search fewer pages
# Clear old data before new crawl
```

### Faster Indexing

```python
# Already optimized, but you can:
# 1. Reduce page count
# 2. Increase stopword list (exclude more words)
```

### Faster UI

```javascript
// Already optimized with AJAX and async loading
// For further optimization:
// - Add pagination
// - Lazy load results
// - Cache client-side
```

---

## Common Use Cases

### Use Case 1: Search Your Own Website
```python
crawler = WebCrawler(
    seed_url="https://mywebsite.com",
    max_pages=100,
    delay=0.5
)
pages = crawler.crawl()
```

### Use Case 2: Compare Content Across Sites
```python
# Crawl site 1
crawler1 = WebCrawler("http://site1.com", max_pages=50)
pages1 = crawler1.crawl()

# Crawl site 2
crawler2 = WebCrawler("http://site2.com", max_pages=50)
pages2 = crawler2.crawl()

# Compare search results
```

### Use Case 3: Monitor Website Changes
```python
# Crawl weekly
import schedule

def crawl_website():
    crawler = WebCrawler("http://mysite.com", max_pages=100)
    crawler.crawl()

schedule.every().monday.at("10:30").do(crawl_website)
```

### Use Case 4: Find Related Content
```python
# Search for similar pages
results1 = indexer.search("topic1")
results2 = indexer.search("topic2")

# Find overlap
related = set(r['url'] for r in results1) & set(r['url'] for r in results2)
```

---

## Extending the Project

### Add Keyword Highlighting
```html
<!-- In search results -->
<span class="highlight">{{ keyword }}</span>
```

### Add Export to CSV
```python
import csv

def export_results(results, filename):
    with open(filename, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['url', 'title', 'score'])
        writer.writerows(results)
```

### Add Web UI for Statistics
```python
# In app.py
@app.route('/api/stats/detailed')
def detailed_stats():
    pages = db.get_all_pages()
    words = len(indexer.inverted_index)
    avg_page_size = sum(len(p['text']) for p in pages) / len(pages)
    return jsonify({
        'pages': len(pages),
        'words': words,
        'avg_size': avg_page_size
    })
```

### Add Filtering
```python
# Filter by date
results = [r for r in results if r['crawled_at'] > '2024-01-01']

# Filter by URL
results = [r for r in results if 'github.com' in r['url']]
```

---

## Scaling Tips

### For 1000+ Pages
```python
# 1. Use PostgreSQL instead of SQLite
# 2. Add caching (Redis)
# 3. Use multi-threading for crawling
# 4. Index in background (Celery)
# 5. Add pagination to results
```

### For Production Deployment
```
Web Crawler
    ↓
Gunicorn (4 workers)
    ↓
Nginx (load balancer)
    ↓
PostgreSQL (database)
    ↓
Redis (cache)
```

---

## Resources

- **Official Docs**: See README.md
- **Setup Guide**: See SETUP_GUIDE.md
- **Architecture**: See ARCHITECTURE.md
- **Testing**: See TESTING.md
- **Complete Guide**: See COMPLETE_GUIDE.md

---

## Getting Help

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Logs
- Flask: Terminal output (INFO level)
- Crawler: Terminal output with progress
- Database: SQLite operations logged

### Common Solutions
1. Restart Flask app
2. Clear database (`rm crawler.db`)
3. Check internet connection
4. Verify website is accessible
5. Read error messages carefully

---

**Still have questions? Check the documentation or review the source code!** 📚
