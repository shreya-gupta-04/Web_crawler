# Web Crawler - Complete Implementation Guide

## 📋 Step-by-Step Implementation

Here's the complete roadmap for building this web crawler project:

---

## **Phase 1: Core Crawler Engine** ✅

### Step 1️⃣: URL Frontier & Visited Set
**File**: `crawler/crawl.py` - `URLFrontier` class

What it does:
- Manages a FIFO queue of URLs to crawl
- Tracks visited URLs to prevent duplicates
- Implements BFS (Breadth-First Search)

**Key Methods:**
```python
frontier = URLFrontier()
frontier.add(url)           # Add URL to queue
frontier.has_next()         # Check if more URLs exist
frontier.get_next()         # Get next URL to crawl
```

---

### Step 2️⃣: HTML Parser
**File**: `crawler/crawl.py` - `HTMLParser` class

What it extracts:
- **Page title**: From `<title>` tag
- **Text content**: All visible text, cleaned up
- **Internal links**: Only URLs from same domain

**Key Features:**
- Removes script/style elements
- Converts relative URLs to absolute
- Filters for internal links only
- Removes duplicates

---

### Step 3️⃣: Crawler Engine
**File**: `crawler/crawl.py` - `WebCrawler` class

Main crawling loop:
1. Start with seed URL in frontier
2. While frontier has URLs AND haven't reached max pages:
   - Get next URL from frontier
   - Fetch page with requests
   - Parse HTML with BeautifulSoup
   - Extract title, text, links
   - Store page data
   - Add new links to frontier
   - Sleep (politeness delay)

**Key Parameters:**
- `seed_url`: Starting URL (e.g., `http://quotes.toscrape.com`)
- `max_pages`: Stop after this many pages (default: 100)
- `delay`: Seconds to wait between requests (default: 2)

---

## **Phase 2: Storage & Indexing** ✅

### Step 4️⃣: SQLite Database
**File**: `storage/database.py` - `Database` class

Database schema (3 tables):

**Table 1: pages**
```sql
id (PRIMARY KEY)
url (UNIQUE)
title
text
crawled_at (TIMESTAMP)
```

**Table 2: words**
```sql
id (PRIMARY KEY)
word (UNIQUE)
document_frequency
```

**Table 3: word_page** (Junction table)
```sql
word_id (FOREIGN KEY)
page_id (FOREIGN KEY)
term_frequency (TF score)
```

**Key Methods:**
```python
db = Database("crawler.db")
db.insert_page(url, title, text)           # Store crawled page
db.get_all_pages()                         # Retrieve all pages
db.insert_word(word)                       # Add word to index
db.search_pages_by_word(word)              # Search by keyword
```

---

### Step 5️⃣: TF-IDF Indexer
**File**: `indexer/indexer.py` - `TFIDFIndexer` class

What it does:
- Tokenizes page text (lowercase, remove special chars)
- Filters stopwords (the, a, and, etc.)
- Calculates TF-IDF scores for each term
- Builds inverted index (word → pages)

**TF-IDF Formula:**
```
TF(term, doc) = count of term in doc / total words in doc
IDF(term) = log(total docs / docs containing term)
TF-IDF(term, doc) = TF × IDF
```

**Key Methods:**
```python
indexer = TFIDFIndexer()
indexer.index_documents(pages)     # Build index from pages
indexer.search(query, top_k=10)    # Search and rank results
indexer.save_to_db()               # Save index to database
```

---

## **Phase 3: Search & Web Interface** ✅

### Step 6️⃣: Flask Web Application
**File**: `app.py`

API Endpoints:
- `POST /api/crawl` - Start crawling
- `GET /api/search?q=query` - Search pages
- `GET /api/pages` - Get all pages
- `GET /api/stats` - Get statistics
- `POST /api/reset` - Clear database

**Main Flow:**
1. Receive crawl request with URL
2. Run crawler
3. Store pages in database
4. Build TF-IDF index
5. Return statistics

---

### Step 7️⃣: Web UI
**File**: `templates/index.html`

Three tabs:

**Crawl Tab**
- Input domain URL
- Set max pages & delay
- Submit to start crawling
- View statistics (pages, words, indexed status)

**Search Tab**
- Enter search query
- Display results sorted by relevance
- Show TF-IDF score for each result
- Clickable links to visit pages

**Browse Tab**
- View all crawled pages
- Refresh to reload
- Clear all data button

---

## **Phase 4: Testing** ✅

### Step 8️⃣: End-to-End Testing

**Test Website**: `quotes.toscrape.com` (allows crawling)

**Steps:**
1. Start Flask app: `python app.py`
2. Go to `http://localhost:5000`
3. Crawl tab: Enter `quotes.toscrape.com`, set max pages to 30
4. Click "Start Crawling"
5. Wait for completion
6. View statistics
7. Search tab: Try searches like:
   - "philosophy"
   - "wisdom"
   - "quotes"
8. Browse tab: View all crawled pages

---

## 📁 File Structure & Content

```
Web_crawler/
├── crawler/
│   └── crawl.py                 # 3 classes: URLFrontier, HTMLParser, WebCrawler
├── storage/
│   └── database.py              # 1 class: Database (SQLite manager)
├── indexer/
│   └── indexer.py               # 1 class: TFIDFIndexer (search engine)
├── templates/
│   └── index.html               # Web UI (3 tabs, responsive design)
├── app.py                        # Flask app with 5 API endpoints
├── requirements.txt             # Python dependencies
├── README.md                     # Documentation
└── SETUP_GUIDE.md              # This file
```

---

## 🔧 Core Concepts Explained

### 1. URL Frontier (FIFO Queue)
```
Start: frontier = [seed_url]
Step 1: Get url1 from frontier → frontier = []
Step 2: Extract links from url1 → frontier = [url2, url3, url4]
Step 3: Get url2 from frontier → frontier = [url3, url4]
...
(Breadth-First order)
```

### 2. Visited Set
```
Prevents: https://example.com/page1 (first time)
After crawl: visited = {url1, url2, url3}
If same URL appears again: Skip (not added to frontier)
```

### 3. HTML Parsing
```python
HTML:
<html>
  <title>My Page</title>
  <body>
    <h1>Hello World</h1>
    <a href="/page2">Link</a>
  </body>
</html>

Extract:
title = "My Page"
text = "Hello World"
links = ["http://example.com/page2"]
```

### 4. TF-IDF Ranking
```
Document 1: "Python Python Python" (3 mentions)
Document 2: "Python JavaScript" (1 mention)
Total documents: 2

TF(Python, Doc1) = 3/3 = 1.0
TF(Python, Doc2) = 1/2 = 0.5
IDF(Python) = log(2/2) = 0
TF-IDF score: 1.0 × 0 = 0 (common word, low relevance)

Document 1: "TensorFlow" (1 mention)
Document 2: No "TensorFlow"
TF(TensorFlow, Doc1) = 1/total = 0.1
IDF(TensorFlow) = log(2/1) = 0.693
TF-IDF score: 0.1 × 0.693 = 0.0693 (rare word, higher relevance)
```

### 5. Politeness Delay
```python
Time 0s: Fetch url1
Time 2s: Fetch url2 (waited 2 seconds)
Time 4s: Fetch url3 (waited 2 seconds)
...
```

---

## 💡 Key Learning Points

✅ **URL Management**: How to handle URLs systematically  
✅ **Web Scraping**: Fetching and parsing HTML  
✅ **Graph Traversal**: BFS algorithm for crawling  
✅ **Database Design**: Schema with relationships  
✅ **Information Retrieval**: TF-IDF ranking  
✅ **Web Development**: Flask API and frontend  
✅ **Politeness**: Respecting server resources  

---

## 🚀 Usage Examples

### Example 1: Simple Crawl
```python
from crawler.crawl import WebCrawler
from storage.database import Database

crawler = WebCrawler("http://example.com", max_pages=20, delay=1)
pages = crawler.crawl()
```

### Example 2: Search After Crawl
```python
from indexer.indexer import TFIDFIndexer

indexer = TFIDFIndexer()
indexer.index_documents(pages)
results = indexer.search("your query")

for result in results:
    print(f"{result['title']}: {result['score']}")
```

### Example 3: Database Query
```python
from storage.database import Database

db = Database()
pages = db.get_all_pages()
print(f"Crawled {len(pages)} pages")

results = db.search_pages_by_word("python")
print(f"Found {len(results)} pages with 'python'")
```

---

## ⚠️ Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| Connection refused | Check internet connection |
| HTTP errors (404, 403) | Website may not allow crawling |
| Slow crawling | Adjust delay (lower = faster) |
| Memory issues | Reduce max_pages |
| No search results | Ensure pages were crawled first |
| Database locked | Stop Flask app and restart |

---

## 📊 Performance Tips

1. **Faster crawling**: Reduce `delay` parameter
2. **More results**: Increase `max_pages`
3. **Better search**: Use specific keywords, not stopwords
4. **Smaller DB**: Crawl limited pages, then search
5. **Cleaner data**: Adjust stopwords in `TFIDFIndexer`

---

## 🎯 Next Steps / Advanced Features

- [ ] Multi-threaded crawling (faster)
- [ ] JavaScript rendering (Selenium/Puppeteer)
- [ ] robots.txt parsing
- [ ] Sitemaps support
- [ ] Advanced queries (AND, OR, NOT)
- [ ] Phrase search
- [ ] PageRank algorithm
- [ ] Duplicate detection
- [ ] Cache pages
- [ ] Incremental crawling

---

## 📚 References

- [Google Web Crawler Architecture](https://en.wikipedia.org/wiki/Web_crawler)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/)
- [TF-IDF Explained](https://en.wikipedia.org/wiki/Tf%E2%80%93idf)
- [SQLite Tutorial](https://www.sqlite.org/docs.html)
- [Flask Web Framework](https://flask.palletsprojects.com/)

---

**Now you have everything to build a professional web crawler! 🎉**
