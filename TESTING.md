# Testing Guide - Web Crawler

## Quick Test

### Option 1: Run with Script (Easiest)
```bash
cd /Users/shreya/Desktop/Web_crawler
chmod +x run.sh
./run.sh
```

### Option 2: Manual Start
```bash
cd /Users/shreya/Desktop/Web_crawler
source .venv/bin/activate
python3 app.py
```

Then open: `http://localhost:5000`

---

## Testing Workflow

### 1. Test Crawling

**Step 1: Go to "Crawl" tab**
- URL: `quotes.toscrape.com`
- Max Pages: `30`
- Delay: `2`
- Click "Start Crawling"

**Expected Results:**
- Loading spinner shows (2-3 minutes)
- Success message appears
- Statistics show:
  - Pages Crawled: ~30
  - Unique Words: 1000+
  - Indexed: ✅

### 2. Test Search

**Step 1: Go to "Search" tab**
- Try search: `philosophy`
- Should show 3-5 results

**Try These Searches:**
```
philosophy
wisdom
love
success
truth
```

**Expected Results:**
- Results ranked by relevance
- Highest scoring results first
- Clickable links work
- Relevance % shown

### 3. Test Browse

**Step 1: Go to "Browse" tab**
- Should show all 30 pages
- Each with title, URL, preview

**Step 2: Click Refresh**
- Reloads page list
- No errors

### 4. Test Reset

**Step 1: Click "Clear All" button**
- Confirm dialog appears
- Click OK

**Expected Results:**
- All data cleared
- Browse tab is empty
- Search returns no results
- Stats reset to 0

---

## Unit Tests

### Test Crawler

```python
from crawler.crawl import WebCrawler

# Test with small number of pages
crawler = WebCrawler(
    seed_url="http://quotes.toscrape.com",
    max_pages=5,
    delay=1
)

pages = crawler.crawl()
print(f"Crawled {len(pages)} pages")

# Check data structure
for page in pages:
    assert 'url' in page
    assert 'title' in page
    assert 'text' in page
    print(f"✅ {page['title']}")
```

### Test Database

```python
from storage.database import Database

db = Database("test.db")

# Insert page
page_id = db.insert_page(
    "http://test.com",
    "Test Page",
    "This is test content"
)
print(f"✅ Inserted page {page_id}")

# Retrieve page
page = db.get_page("http://test.com")
print(f"✅ Retrieved: {page['title']}")

# Insert word
word_id = db.insert_word("test")
print(f"✅ Inserted word {word_id}")

# Clear
db.clear_database()
print("✅ Database cleared")
```

### Test Indexer

```python
from indexer.indexer import TFIDFIndexer

indexer = TFIDFIndexer()

docs = [
    {'id': 1, 'title': 'Python Tutorial', 'text': 'Learn Python basics'},
    {'id': 2, 'title': 'Web Crawler', 'text': 'Build web crawler with Python'},
    {'id': 3, 'title': 'JavaScript', 'text': 'Learn JavaScript for web'}
]

# Build index
indexer.index_documents(docs)
print(f"✅ Indexed {len(docs)} documents")

# Search
results = indexer.search("Python", top_k=5)
print(f"✅ Found {len(results)} results")
for result in results:
    print(f"  - {result['title']}: {result['score']:.3f}")
```

---

## Test Scenarios

### Scenario 1: Fresh Start
1. Clear database (if exists)
2. Crawl quotes.toscrape.com (10 pages)
3. Search: "love"
4. Verify results

### Scenario 2: Multiple Crawls
1. Crawl quotes.toscrape.com (10 pages)
2. Crawl again (should add more pages or skip duplicates)
3. Verify total page count
4. Search should still work

### Scenario 3: Large Crawl
1. Crawl with 100 pages
2. Watch for memory issues
3. Verify search speed (should be fast)
4. Clear and verify cleanup

### Scenario 4: Error Handling
1. Try invalid URL (should show error)
2. Try 0 max pages (should fail gracefully)
3. Try negative delay (should reject)

---

## Performance Benchmarks

### Expected Performance

**Crawling:**
- 50 pages: ~2-3 minutes (with 2s delay)
- 100 pages: ~4-5 minutes

**Search:**
- Should return results in <100ms
- Even with 1000+ pages

**Database:**
- Insert page: <10ms
- Search: <50ms

### Optimization Tips

1. **Faster Crawling:**
   - Reduce delay to 1s
   - Increase max_pages

2. **Faster Search:**
   - Use specific keywords
   - Avoid stopwords (the, a, and)

3. **Better Results:**
   - Crawl 50+ pages
   - Search with 2-3 word phrases

---

## Troubleshooting

### Issue: Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Then restart
python3 app.py
```

### Issue: Import Errors
```bash
# Verify virtual environment
source .venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Issue: Slow Crawling
```python
# Reduce delay in UI or code
crawler = WebCrawler(
    seed_url="http://example.com",
    max_pages=50,
    delay=0.5  # Reduced from 2
)
```

### Issue: Database Locked
```bash
# Stop Flask app
# Delete crawler.db
rm crawler.db

# Restart Flask app
python3 app.py
```

---

## Browser Compatibility

✅ Tested on:
- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

✅ Mobile:
- iOS Safari
- Chrome Mobile
- Firefox Mobile

---

## Load Testing

### Simulate 100 Requests
```python
import requests
import time

url = "http://localhost:5000/api/search?q=philosophy"

start = time.time()
for i in range(100):
    response = requests.get(url)
    print(f"Request {i+1}: {response.status_code}")
end = time.time()

print(f"Average time: {(end-start)/100:.3f}s")
```

### Expected Results
- All requests should succeed (200 status)
- Average response time: <100ms
- No timeouts

---

## Verification Checklist

- [ ] App starts without errors
- [ ] Web UI loads at http://localhost:5000
- [ ] Crawl tab works
- [ ] Search returns results
- [ ] Browse shows crawled pages
- [ ] Clear button removes data
- [ ] No console errors
- [ ] Database file created
- [ ] Can crawl same domain twice
- [ ] Statistics update correctly

---

## Clean Up

### Remove Test Database
```bash
rm crawler.db
```

### Remove Virtual Environment (if needed)
```bash
rm -rf .venv
```

### Reset Project
```bash
# Clear all data
rm -f crawler.db *.json

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

---

**Happy testing! 🎉**
