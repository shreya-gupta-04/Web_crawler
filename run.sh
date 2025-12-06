#!/bin/bash

# Web Crawler Quick Start Script

echo "🚀 Web Crawler - Quick Start"
echo "============================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: python3 -m venv .venv"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Check if requirements are installed
echo "📚 Checking dependencies..."
pip install -q -r requirements.txt

# Start Flask app
echo ""
echo "✅ Starting Flask application..."
echo "🌐 Open browser at: http://localhost:5000"
echo ""
echo "Available domains to test:"
echo "  - quotes.toscrape.com (recommended)"
echo "  - books.toscrape.com"
echo "  - insecure.example.com"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 app.py
