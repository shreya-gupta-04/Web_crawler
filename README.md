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
## 📁 Project File Structure Overview

### CORE APPLICATION
- **app.py** — Flask web server  
- **crawler/crawl.py** — Web crawling engine  
- **indexer/indexer.py** — TF-IDF search engine  
- **storage/database.py** — SQLite database manager  
- **templates/index.html** — Web user interface  


### CONFIGURATION
- **requirements.txt** — Python dependencies  
- **run.sh** — Quick start script  
- **crawler.db** — Generated SQLite database (created at runtime)

### System Architecture Diagram
```
┌─────────────────────────────────────────────────────────────────────┐
│                              WEB UI                                 │
│                    http://localhost:5000                            │
│                                                                     │
│  [Crawl Tab]   [Search Tab]   [Browse Tab]                          │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼ AJAX
┌─────────────────────────────────────────────────────────────────────┐
│                     FLASK SERVER (app.py)                           │
│ Routes:                                                             │
│  POST /api/crawl     GET /api/search                                │
│  GET  /api/pages     GET /api/stats                                 │
│  POST /api/reset                                                      │
└─────────────────────────────────────────────────────────────────────┘
      │                       │                          │
      ▼                       ▼                          ▼
┌──────────────┐    ┌──────────────────┐      ┌──────────────────────┐
│ WebCrawler   │    │ TFIDFIndexer     │      │ Database (SQLite)    │
│              │    │                  │      │                      │
│ • BFS Crawl  │    │ • Tokenize       │      │ • pages table        │
│ • Parse HTML │    │ • TF-IDF Scores  │      │ • words table        │
│ • Extract URLs│   │ • Ranking        │      │ • word_page table    │
└──────────────┘    └──────────────────┘      └──────────────────────┘
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
5. **Activate Virtual Environment**
  $ source .venv/bin/activate

6. **Start the Server**
  $ python3 app.py

 7. **Open Your Browser**
  Go to: http://localhost:5000

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

## 📊 How It Works

### 1. Crawling Flow
```
URL Input
    ↓
Add to Frontier
    ↓
Fetch Page
    ↓
Parse HTML
    ↓
Extract Title, Text, Links
    ↓
Store in Database
    ↓
Add New Links to Frontier
    ↓
Repeat until max_pages or queue empty
```
### 2. Search Flow
```
Query Input
    ↓
Tokenize (lowercase, remove special chars)
    ↓
Remove Stopwords
    ↓
Look up each term in inverted index
    ↓
Calculate TF-IDF scores
    ↓
Rank by relevance
    ↓
Return top K results
```
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
- Ranks search results by cumulative TF-IDF scores

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/crawl` | Start crawling a domain |
| GET | `/api/search` | Search by keyword |
| GET | `/api/pages` | Get all crawled pages |
| GET | `/api/stats` | Get crawler statistics |
| POST | `/api/reset` | Clear all data |

### Database Schema
pages table
├── id
├── url
├── title
├── text
└── crawled_at

words table
├── id
├── word
└── document_frequency

word_page table
├── word_id
├── page_id
└── term_frequency


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

## Performance

- **Crawl Speed**: Limited by delay parameter (politeness)
- **Memory**: Pages stored in memory then to database
- **Search Speed**: O(1) word lookup in inverted index
- **Database Size**: Depends on page count and content

## Testing
### Test with Demo Site
1. Go to `http://localhost:5000`
2. Enter: `quotes.toscrape.com`
3. Set max pages: 30
4. Click "Start Crawling"
5. Try searches: "philosophy", "wisdom", "success"


## What You'll Learn

✓ Web crawling architecture  
✓ BFS algorithms  
✓ HTML parsing with BeautifulSoup  
✓ SQLite database design  
✓ TF-IDF search ranking  
✓ Flask web development  
✓ URL normalization  
✓ HTTP headers and requests  


