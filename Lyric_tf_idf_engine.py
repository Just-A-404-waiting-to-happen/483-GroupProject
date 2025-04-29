import pandas as pd
import collections
import math
import argparse
import csv
from typing import Dict, List, Set


class IRSystem:
    def __init__(self, csv_path: str):
        """Initialize with memory-efficient CSV processing"""
        self.df = collections.defaultdict(int)  # Document frequency
        self.doc_vectors = []  # Document vectors
        self.metadata = []  # Store artist/title for each doc
        self.num_documents = 0

        # First pass: build vocabulary and document frequencies
        self._build_vocabulary(csv_path)

        # Second pass: create document vectors
        self._build_vectors(csv_path)

    def _build_vocabulary(self, csv_path: str):
        """First pass to count document frequencies"""
        print("Building vocabulary...")
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    doc_text = f"{row.get('lyrics', '')}".lower()
                    terms = set(doc_text.split())
                    for term in terms:
                        self.df[term] += 1
                    self.num_documents += 1
                except Exception as e:
                    print(f"Skipping row due to error: {e}")

    def _build_vectors(self, csv_path: str):
        """Second pass to create document vectors"""
        print("Building document vectors...")
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Store metadata
                    self.metadata.append({
                        'artist': row.get('artist', ''),
                        'title': row.get('title', '')
                    })

                    # Process lyrics
                    doc_text = f"{row.get('lyrics', '')}".lower()
                    terms = doc_text.split()

                    # Calculate TF
                    tf_doc = collections.defaultdict(float)
                    for term in terms:
                        tf_doc[term] += 1

                    # Create document vector
                    doc_vector = {}
                    doc_length = 0.0
                    for term, tf in tf_doc.items():
                        weighted_tf = 1 + math.log(tf, 10) if tf > 0 else 0
                        doc_vector[term] = weighted_tf
                        doc_length += weighted_tf ** 2

                    # Normalize
                    doc_length = math.sqrt(doc_length)
                    if doc_length > 0:
                        for term in doc_vector:
                            doc_vector[term] /= doc_length

                    self.doc_vectors.append(doc_vector)
                except Exception as e:
                    print(f"Skipping row due to error: {e}")
                    self.doc_vectors.append({})  # Empty vector for failed docs

    def run_query(self, query: str) -> List[Dict]:
        """Run query and return results with metadata"""
        terms = query.lower().split()
        doc_ids = self._run_query(terms)
        return [{
            'doc_id': doc_id,
            'artist': self.metadata[doc_id]['artist'],
            'title': self.metadata[doc_id]['title'],
            'score': score
        } for doc_id, score in doc_ids]

    def _run_query(self, terms: List[str]) -> List[tuple]:
        """Internal query processing"""
        if not terms or not self.num_documents:
            return []

        # Create query vector
        query_tf = collections.defaultdict(int)
        for term in terms:
            query_tf[term] += 1

        query_vector = {}
        for term, tf in query_tf.items():
            weighted_tf = 1 + math.log(tf, 10) if tf > 0 else 0
            idf = math.log(self.num_documents / (self.df.get(term, 0) + 1), 10)
            query_vector[term] = weighted_tf * idf

        # Score documents
        scores = []
        for doc_idx, doc_vector in enumerate(self.doc_vectors):
            score = sum(
                doc_vector.get(term, 0) * weight
                for term, weight in query_vector.items()
            )
            scores.append((doc_idx, score))

        # Sort by score descending, doc_idx ascending
        scores.sort(key=lambda x: (-x[1], x[0]))

        return scores[:10]


def main(corpus: str):
    try:
        print("Initializing search system...")
        ir = IRSystem(corpus)
        print(f"Ready. Index contains {ir.num_documents} documents.")

        while True:
            query = input('Query (or "exit" to quit): ').strip()
            if query.lower() == 'exit':
                break
            results = ir.run_query(query)
            for result in results:
                print(f"{result['score']:.4f} | {result['artist']} - {result['title']}")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("CORPUS", help="Path to CSV file with song data")
    args = parser.parse_args()
    main(args.CORPUS)
