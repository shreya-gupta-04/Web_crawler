from flask import Flask, render_template, request, jsonify
import os
import sys
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crawler.crawl import WebCrawler
from storage.database import Database
from indexer.indexer import TFIDFIndexer

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Initialize database and indexer
db = Database(db_path="crawler.db")
indexer = TFIDFIndexer(db=db)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/crawl', methods=['POST'])
def crawl():
    """Start crawling a domain"""
    data = request.json
    seed_url = data.get('url', '').strip()
    max_pages = int(data.get('max_pages', 50))
    delay = float(data.get('delay', 2.0))
    
    if not seed_url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Ensure URL has scheme
    if not seed_url.startswith(('http://', 'https://')):
        seed_url = f'http://{seed_url}'
    
    try:
        logger.info(f"Starting crawl for: {seed_url}")
        
        # Start crawler
        crawler = WebCrawler(seed_url, max_pages=max_pages, delay=delay)
        pages = crawler.crawl()
        
        # Store in database
        page_count = 0
        for page in pages:
            page_id = db.insert_page(page['url'], page['title'], page['text'])
            if page_id:
                page_count += 1
        
        # Build index
        all_pages = db.get_all_pages()
        indexer.index_documents(all_pages)
        indexer.save_to_db()
        
        return jsonify({
            'success': True,
            'message': f'Successfully crawled {page_count} pages',
            'pages_crawled': page_count
        })
    
    except Exception as e:
        logger.error(f"Crawl error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/search', methods=['GET'])
def search():
    """Search for pages by keyword"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    try:
        results = indexer.search(query, top_k=20)
        
        return jsonify({
            'query': query,
            'results': results,
            'total': len(results)
        })
    
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/pages', methods=['GET'])
def get_pages():
    """Get all crawled pages"""
    try:
        pages = db.get_all_pages()
        return jsonify({
            'pages': pages,
            'total': len(pages)
        })
    except Exception as e:
        logger.error(f"Error getting pages: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get crawler statistics"""
    try:
        pages = db.get_all_pages()
        total_words = len(indexer.inverted_index)
        
        return jsonify({
            'total_pages': len(pages),
            'total_unique_words': total_words,
            'indexed': len(indexer.inverted_index) > 0
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset():
    """Clear all data"""
    try:
        db.clear_database()
        indexer.inverted_index = {}
        indexer.document_frequency = {}
        indexer.total_docs = 0
        
        return jsonify({'success': True, 'message': 'All data cleared'})
    except Exception as e:
        logger.error(f"Error resetting: {e}")
        return jsonify({'error': str(e)}), 500


@app.template_filter('truncate')
def truncate(text, length=150):
    """Truncate text for display"""
    if len(text) > length:
        return text[:length] + '...'
    return text


if __name__ == '__main__':
    app.run(debug=True, port=5000)
