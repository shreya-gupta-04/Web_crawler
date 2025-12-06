# Web Crawler - Search Engine

A complete web crawler that mirrors Google's architecture at a tiny scale. Crawl any website, extract content, and search through it using TF-IDF ranking.

## Features

✅ **URL Frontier** - BFS-based URL queue for systematic crawling  
✅ **Visited Set** - Prevents re-crawling the same pages  
✅ **HTML Parsing** - Extracts titles, text, and internal links  
✅ **Politeness** - Configurable delays between requests  
✅ **SQLite Storage** - Persistent database for crawled data  
✅ **TF-IDF Search** - Intelligent relevance ranking  
✅ **Web UI** - Beautiful Flask interface for crawling and searching  

## Project Architecture

```
Web_crawler/
├── app.py                 # Flask web application
├── crawler/
│   └── crawl.py          # WebCrawler, URLFrontier, HTMLParser classes
├── indexer/
│   └── indexer.py        # TFIDFIndexer for search
├── storage/
│   └── database.py       # SQLite database manager
├── templates/
│   └── index.html        # Web UI
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip

### Quick Start

1. **Navigate to project directory:**
```bash
cd /Users/shreya/Desktop/Web_crawler
```

2. **Activate virtual environment:**
```bash
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
python app.py
```

The app will start at `http://localhost:5000`

## Usage

### Web Interface Tabs

**1. Crawl Tab**
- Enter domain (e.g., `quotes.toscrape.com`)
- Set max pages (default: 50)
- Set delay between requests (default: 2 seconds)
- Click "Start Crawling"
- View statistics after crawl

**2. Search Tab**
- Enter keywords to search
- Results ranked by TF-IDF relevance
- Click titles to visit pages

**3. Browse Tab**
- View all crawled pages
- Clear data if needed

### Python API

**Basic Crawling**
```python
from crawler.crawl import WebCrawler

crawler = WebCrawler(
    seed_url="http://quotes.toscrape.com",
    max_pages=50,
    delay=2.0
)
pages = crawler.crawl()
```

**Database Operations**
```python
from storage.database import Database

db = Database("crawler.db")
pages = db.get_all_pages()
results = db.search_pages_by_word("python")
```

**TF-IDF Search**
```python
from indexer.indexer import TFIDFIndexer

indexer = TFIDFIndexer()
indexer.index_documents(documents)
results = indexer.search("your query", top_k=10)
```

## How It Works

### 1. URL Frontier & Visited Set
- Uses deque (FIFO queue) for breadth-first crawling
- Maintains visited set to avoid duplicates
- Only crawls internal links (same domain)

### 2. HTML Parsing
- Extracts: page title, text content, internal links
- Removes script/style tags
- Handles relative URLs with `urljoin`

### 3. Politeness
- Configurable delays between requests
- Respects server resources
- Browser-like User-Agent headers

### 4. Storage
- SQLite database with 3 tables:
  - `pages`: url, title, text, crawl timestamp
  - `words`: unique terms, document frequency
  - `word_page`: term frequency & TF-IDF scores

### 5. TF-IDF Ranking
- **TF (Term Frequency)**: How often term appears in document
- **IDF (Inverse Document Frequency)**: How rare term is across all documents
- **TF-IDF Score**: tf(t,d) × log(N/df(t))
- Results ranked by relevance

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/crawl` | Start crawling a domain |
| GET | `/api/search` | Search by keyword |
| GET | `/api/pages` | Get all crawled pages |
| GET | `/api/stats` | Get crawler statistics |
| POST | `/api/reset` | Clear all data |

## Configuration

**Crawler Parameters**
```python
crawler = WebCrawler(
    seed_url="http://example.com",     # Starting URL
    max_pages=100,                      # Max pages to crawl
    delay=2.0                           # Delay in seconds
)
```

**Database Path**
```python
db = Database(db_path="/custom/path.db")
```

## Testing

### Test with Demo Site
1. Go to `http://localhost:5000`
2. Enter: `quotes.toscrape.com`
3. Set max pages: 30
4. Click "Start Crawling"
5. Try searches: "philosophy", "wisdom", "success"

## Performance

- **Crawl Speed**: Limited by delay parameter (politeness)
- **Memory**: Pages stored in memory then to database
- **Search Speed**: O(1) word lookup in inverted index
- **Database Size**: Depends on page count and content

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection error | Check internet, verify domain accessible |
| Database locked | Restart Flask app |
| Out of memory | Reduce max_pages, crawl smaller sites |

## What You'll Learn

✓ Web crawling architecture  
✓ BFS algorithms  
✓ HTML parsing with BeautifulSoup  
✓ SQLite database design  
✓ TF-IDF search ranking  
✓ Flask web development  
✓ URL normalization  
✓ HTTP headers and requests  

## Future Improvements

- [ ] Multi-threaded crawling
- [ ] JavaScript rendering support
- [ ] robots.txt parsing
- [ ] Advanced query syntax (AND, OR, NOT)
- [ ] Phrase search
- [ ] PageRank algorithm
- [ ] Duplicate detection
- [ ] Incremental crawling

---

**Happy crawling! 🚀**
