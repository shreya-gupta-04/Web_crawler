import math
import re
import logging
from typing import List, Dict, Set
from collections import Counter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TFIDFIndexer:
    """Build TF-IDF index and search"""
    
    # Common stopwords to exclude
    STOPWORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which',
        'who', 'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both',
        'few', 'more', 'some', 'such', 'no', 'nor', 'not', 'only', 'same',
        'so', 'than', 'too', 'very', 'just', 'here', 'there'
    }
    
    def __init__(self, db=None):
        self.db = db
        self.inverted_index = {}  # word -> list of (page_id, tf-idf score)
        self.document_frequency = {}  # word -> count of documents containing word
        self.total_docs = 0
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize and clean text"""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters, keep only alphanumeric and spaces
        text = re.sub(r'[^a-z0-9\s]', '', text)
        # Split on whitespace
        tokens = text.split()
        # Remove stopwords and empty tokens
        tokens = [t for t in tokens if t and t not in self.STOPWORDS]
        return tokens
    
    def _calculate_tf(self, term_count: int, doc_length: int) -> float:
        """Calculate Term Frequency"""
        if doc_length == 0:
            return 0
        return term_count / doc_length
    
    def _calculate_idf(self, docs_with_term: int, total_docs: int) -> float:
        """Calculate Inverse Document Frequency"""
        if docs_with_term == 0:
            return 0
        return math.log(total_docs / docs_with_term)
    
    def index_documents(self, documents: List[Dict]) -> Dict:
        """Build TF-IDF index from documents"""
        self.total_docs = len(documents)
        self.inverted_index = {}
        self.document_frequency = {}
        
        logger.info(f"Indexing {self.total_docs} documents...")
        
        # First pass: Count document frequencies
        doc_tokens = {}
        for doc in documents:
            doc_id = doc.get('id')
            text = doc.get('text', '') + ' ' + doc.get('title', '')
            tokens = self._tokenize(text)
            doc_tokens[doc_id] = tokens
            
            # Count unique tokens per document
            unique_tokens = set(tokens)
            for token in unique_tokens:
                self.document_frequency[token] = self.document_frequency.get(token, 0) + 1
        
        # Second pass: Calculate TF-IDF and build index
        for doc in documents:
            doc_id = doc.get('id')
            tokens = doc_tokens[doc_id]
            
            if not tokens:
                continue
            
            # Count term frequencies in document
            term_counts = Counter(tokens)
            doc_length = len(tokens)
            
            # Calculate TF-IDF for each term
            for term, count in term_counts.items():
                tf = self._calculate_tf(count, doc_length)
                idf = self._calculate_idf(self.document_frequency[term], self.total_docs)
                tf_idf = tf * idf
                
                if term not in self.inverted_index:
                    self.inverted_index[term] = []
                
                self.inverted_index[term].append({
                    'doc_id': doc_id,
                    'url': doc.get('url'),
                    'title': doc.get('title'),
                    'tf_idf': tf_idf,
                    'tf': tf
                })
            
            if doc_id % 10 == 0:
                logger.info(f"Indexed {doc_id} documents...")
        
        # Sort each term's documents by TF-IDF score
        for term in self.inverted_index:
            self.inverted_index[term].sort(key=lambda x: x['tf_idf'], reverse=True)
        
        logger.info(f"Indexing complete! Total unique terms: {len(self.inverted_index)}")
        return self.inverted_index
    
    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """Search for documents matching query"""
        query_tokens = self._tokenize(query)
        
        if not query_tokens:
            logger.warning("Query has no valid tokens after processing")
            return []
        
        # Get candidate documents and their scores
        doc_scores = {}
        
        for token in query_tokens:
            if token in self.inverted_index:
                for result in self.inverted_index[token]:
                    doc_id = result['doc_id']
                    if doc_id not in doc_scores:
                        doc_scores[doc_id] = {
                            'url': result['url'],
                            'title': result['title'],
                            'score': 0,
                            'matching_terms': []
                        }
                    doc_scores[doc_id]['score'] += result['tf_idf']
                    doc_scores[doc_id]['matching_terms'].append(token)
        
        # Sort by score
        results = sorted(
            doc_scores.values(),
            key=lambda x: x['score'],
            reverse=True
        )[:top_k]
        
        logger.info(f"Found {len(results)} results for query: '{query}'")
        return results
    
    def save_to_db(self):
        """Save index to database"""
        if not self.db:
            logger.warning("No database connection available")
            return
        
        logger.info("Saving index to database...")
        for term, results in self.inverted_index.items():
            word_id = self.db.insert_word(term)
            if word_id:
                for result in results:
                    self.db.link_word_to_page(word_id, result['doc_id'], result['tf_idf'])
                self.db.update_document_frequency(word_id)
        logger.info("Index saved to database")
