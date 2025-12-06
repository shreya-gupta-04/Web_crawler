# Web Crawler - Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          WEB BROWSER                                 │
│                    (http://localhost:5000)                           │
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │  Crawl Tab   │  │ Search Tab   │  │ Browse Tab   │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
└─────────────────────────────────────────────────────────────────────┘
                              ↓ AJAX
┌─────────────────────────────────────────────────────────────────────┐
│                      FLASK WEB SERVER (app.py)                       │
│                                                                       │
│  POST /api/crawl    →  Start crawler                                │
│  GET  /api/search   →  Search pages                                 │
│  GET  /api/pages    →  List all pages                               │
│  GET  /api/stats    →  Get statistics                               │
│  POST /api/reset    →  Clear database                               │
└─────────────────────────────────────────────────────────────────────┘
        ↓                              ↓                      ↓
┌──────────────────┐    ┌─────────────────────┐    ┌─────────────────┐
│  WebCrawler      │    │  TFIDFIndexer       │    │  Database       │
│  (crawler.py)    │    │  (indexer.py)       │    │  (database.py)  │
│                  │    │                     │    │                 │
│ • URLFrontier    │    │ • Tokenization      │    │ • SQL queries   │
│ • HTMLParser     │    │ • TF-IDF scoring    │    │ • Indexing      │
│ • URL frontier   │    │ • Ranking           │    │ • Storage       │
│ • Link extraction│    │                     │    │                 │
└──────────────────┘    └─────────────────────┘    └─────────────────┘
        ↓                        ↓                         ↓
┌──────────────────────────────────────────────────────────────────────┐
│                        crawler.db (SQLite)                            │
│                                                                        │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────────┐        │
│  │   pages     │    │    words     │    │    word_page     │        │
│  ├─────────────┤    ├──────────────┤    ├──────────────────┤        │
│  │ id          │    │ id           │    │ word_id          │        │
│  │ url         │    │ word         │    │ page_id          │        │
│  │ title       │    │ doc_freq     │    │ term_frequency   │        │
│  │ text        │    └──────────────┘    └──────────────────┘        │
│  │ crawled_at  │                                                      │
│  └─────────────┘                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### Crawling Process
```
User Input (URL, max_pages, delay)
           ↓
    WebCrawler.__init__()
           ↓
    crawler.crawl()
           ↓
    ┌──────────────────────────────┐
    │  While queue not empty:      │
    │  1. Get URL from frontier    │
    │  2. Fetch page (requests)    │
    │  3. Parse HTML (BeautifulSoup)│
    │  4. Extract title/text/links │
    │  5. Store in memory          │
    │  6. Add links to frontier    │
    │  7. Sleep (politeness)       │
    └──────────────────────────────┘
           ↓
    Store all pages in SQLite
           ↓
    Build TF-IDF index
           ↓
    Save index to database
           ↓
    Return statistics
```

### Search Process
```
User Query (e.g., "python")
           ↓
    indexer.search(query)
           ↓
    Tokenize & clean query
           ↓
    Remove stopwords
           ↓
    ┌──────────────────────────────┐
    │  For each token:             │
    │  1. Look up in index         │
    │  2. Get matching pages       │
    │  3. Get TF-IDF scores       │
    │  4. Sum scores              │
    └──────────────────────────────┘
           ↓
    Sort by total score
           ↓
    Return top K results
           ↓
    Display in browser
```

---

## Component Interaction

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (HTML/CSS/JS)               │
│                                                          │
│  - Form input collection                               │
│  - AJAX API calls                                      │
│  - Dynamic UI updates                                  │
│  - Results display                                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓ JSON requests/responses
                     
┌─────────────────────────────────────────────────────────┐
│                  Flask Application                       │
│                                                          │
│  - Route handling                                      │
│  - Request validation                                  │
│  - Business logic orchestration                        │
│  - Response formatting                                 │
└────────────────────┬────────────────────────────────────┘
                     │
          ┌──────────┴──────────┬──────────────┐
          ↓                     ↓              ↓
          
  ┌──────────────┐    ┌──────────────┐   ┌──────────────┐
  │  Crawler     │    │  Indexer     │   │  Database    │
  │              │    │              │   │              │
  │ • Fetch URLs │    │ • Tokenize   │   │ • CRUD ops   │
  │ • Parse HTML │    │ • Score docs │   │ • Queries    │
  │ • Extract    │    │ • Rank       │   │ • Index      │
  │   content    │    │              │   │              │
  └──────┬───────┘    └──────┬───────┘   └──────┬───────┘
         │                   │                  │
         └───────────────────┴──────────────────┘
                     ↓
            SQLite Database (crawler.db)
```

---

## Class Hierarchy

```
URLFrontier
├── queue (deque)
├── visited (set)
└── Methods:
    ├── add(url)
    ├── get_next()
    └── has_next()

HTMLParser
├── base_url (str)
├── domain (str)
└── Methods:
    ├── parse(html)
    ├── _extract_text()
    ├── _extract_links()
    └── _is_internal_link()

WebCrawler
├── seed_url (str)
├── max_pages (int)
├── delay (float)
├── frontier (URLFrontier)
├── parser (HTMLParser)
├── crawled_pages (list)
└── Methods:
    ├── crawl()
    └── save_to_json()

Database
├── db_path (str)
└── Methods:
    ├── init_db()
    ├── insert_page()
    ├── insert_word()
    ├── link_word_to_page()
    ├── search_pages_by_word()
    └── clear_database()

TFIDFIndexer
├── inverted_index (dict)
├── document_frequency (dict)
├── total_docs (int)
└── Methods:
    ├── index_documents()
    ├── search()
    ├── _tokenize()
    ├── _calculate_tf()
    ├── _calculate_idf()
    └── save_to_db()
```

---

## Algorithm Flow Charts

### TF-IDF Ranking Algorithm
```
                 Query: "Python web"
                        ↓
            Tokenize: ["python", "web"]
                        ↓
    ┌───────────────────────────────────┐
    │  For each document in corpus:     │
    │                                   │
    │  For each query term:             │
    │    • Count term occurrences       │
    │    • Calculate TF                 │
    │    • Calculate IDF                │
    │    • Calculate TF-IDF             │
    │    • Add to document score        │
    └───────────────────────────────────┘
                        ↓
        Rank documents by total score
                        ↓
        Return top K documents
```

### BFS Crawling Algorithm
```
    Initialize: frontier = [seed_url], visited = {}
                        ↓
    ┌─────────────────────────────────────┐
    │  While frontier not empty AND       │
    │        page_count < max_pages:      │
    │                                     │
    │  1. url = frontier.get_next()       │
    │  2. Fetch URL                       │
    │  3. Parse HTML                      │
    │  4. For each link in page:          │
    │       if internal and not visited:  │
    │         frontier.add(link)          │
    │  5. page_count++                    │
    │  6. sleep(delay)                    │
    └─────────────────────────────────────┘
                        ↓
    Return crawled pages
```

---

## URL Frontier Visualization

```
Initial State:
    frontier = [seed_url]
    visited = {seed_url}

Step 1:
    Get "page1"
    frontier = []
    visited = {seed_url, page1}
    Found links: [page2, page3, page4]
    Add to frontier

Step 2:
    frontier = [page2, page3, page4]
    visited = {seed_url, page1, page2, page3, page4}
    
Step 3:
    Get "page2"
    frontier = [page3, page4]
    visited = {seed_url, page1, page2, page3, page4}
    Found links: [page5, page6] (page3, page4 already visited)
    Add to frontier

Step 4:
    frontier = [page3, page4, page5, page6]
    ... continues until frontier empty or max_pages reached
```

---

## Database Schema Diagram

```
┌─────────────────────────────────────────────────────┐
│                    pages table                      │
├─────────────────────────────────────────────────────┤
│  PK: id (INTEGER)                                   │
│  UNIQUE: url (TEXT)                                 │
│        : title (TEXT)                               │
│        : text (TEXT)                                │
│        : crawled_at (TIMESTAMP)                     │
└─────────────────────────────────────────────────────┘
                       │
                       │ FK
                       ↓
┌──────────────────────────────────────┐
│      word_page (Junction Table)      │
├──────────────────────────────────────┤
│ PK: (word_id, page_id)               │
│    : term_frequency (REAL)           │
└──────────────────────────────────────┘
            ↑
            │ FK
            │
┌─────────────────────────────────────────────────────┐
│                  words table                        │
├─────────────────────────────────────────────────────┤
│  PK: id (INTEGER)                                   │
│  UNIQUE: word (TEXT)                                │
│        : document_frequency (INTEGER)               │
└─────────────────────────────────────────────────────┘
```

---

## Page 1 → Page 2 Mapping Example

```
Page 1 (URL: example.com)
├── Words extracted: ["python", "tutorial", "learning", ...]
├── TF-IDF calculations performed
└── Stored in database as:
    
    INSERT INTO pages: {url: "example.com", title: "Python", text: "..."}
    INSERT INTO words: {word: "python", doc_freq: 1}
    INSERT INTO word_page: {word_id: 1, page_id: 1, tf_idf: 0.45}
    
Page 2 (URL: example.com/advanced)
├── Words extracted: ["python", "advanced", "framework", ...]
├── TF-IDF calculations performed
└── Stored in database as:
    
    INSERT INTO pages: {url: "example.com/advanced", ...}
    INSERT INTO word_page: {word_id: 1, page_id: 2, tf_idf: 0.52}
    UPDATE words SET doc_freq = 2 WHERE word = "python"
```

---

## Search Result Ranking Example

```
Query: "python"

Inverted Index Lookup:
├── word: "python"
├── pages containing "python":
│   ├── Page 1: TF-IDF = 0.45
│   ├── Page 2: TF-IDF = 0.52 ← Highest
│   ├── Page 3: TF-IDF = 0.38
│   └── Page 4: TF-IDF = 0.41

Ranking (Sorted by TF-IDF):
1. Page 2 (0.52) ← Show first
2. Page 1 (0.45)
3. Page 4 (0.41)
4. Page 3 (0.38)

Display Results:
┌─────────────────────────────┐
│ 1. Python Advanced Framework │
│    Score: 52%               │
├─────────────────────────────┤
│ 2. Python Tutorial          │
│    Score: 45%               │
├─────────────────────────────┤
│ 3. Learning Python Basics   │
│    Score: 41%               │
└─────────────────────────────┘
```

---

**This architecture implements a complete search engine system! 🎯**
