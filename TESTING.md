# Testing Guide

## 1. Test Crawler
python3 crawler/crawl.py
Enter URL: https://example.com
Check storage/pages.json

## 2. Test Indexer
python3 -c "from indexer.indexer import *; ..."

## 3. Test Search
Run: python3 app.py
Go to: http://localhost:5000
Try searches: 'python', 'about', 'home'

## 4. Edge Cases
Invalid URL
Max depth = 0
Large crawl
