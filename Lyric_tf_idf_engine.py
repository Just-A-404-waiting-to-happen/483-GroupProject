import collections
import math
import argparse


# noinspection PyPackageRequirements
class IRSystem:

    def __init__(self, f):
        # Use lnc to weight terms in the documents:
        #   l: logarithmic tf
        #   n: no df
        #   c: cosine normalization

        # Store the vecorized representation for each document
        #   and whatever information you need to vectorize queries in _run_query(...)

        # YOUR CODE GOES HERE

        self.documents = [line.replace('-', ' ').lower().split() for line in f]
        self.num_documents = len(self.documents)

        self.tf = []
        self.df = collections.defaultdict(int)
        # self.idf = {}

        for doc in self.documents:
            unique_term = set(doc)
            for term in unique_term:
                self.df[term] += 1

        self.doc_vectors = []
        for doc in self.documents:
            tf_doc = collections.defaultdict(float)
            for term in doc[1:]:
                tf_doc[term] += 1
            doc_vector = {}
            doc_length = 0.0
            for term, tf in tf_doc.items():
                # l : logrithmic
                weighted_tf = 1 + math.log(tf, 10) if tf > 0 else 0

                # c : cosine normalization
                doc_vector[term] = weighted_tf
                doc_length += weighted_tf ** 2
            doc_length = math.sqrt(doc_length)
            if doc_length > 0:
                for term in doc_vector:
                    doc_vector[term] /= doc_length
            self.doc_vectors.append(doc_vector)

    def run_query(self, query):
        terms = query.lower().split()
        return self._run_query(terms)

    def _run_query(self, terms):
        # Use ltn to weight terms in the query:
        #   l: logarithmic tf
        #   t: idf
        #   n: no normalization

        # Return the top-10 document for the query 'terms'
        result = []

        # YOUR CODE GOES HERE
        if not terms:
            return result

        query_tf = collections.defaultdict(int)
        for term in terms:
            query_tf[term] += 1

        query_vector = {}
        for term, tf in query_tf.items():
            # l : logarithmic
            weighted_tf = 1 + math.log(tf, 10) if tf > 0 else 0
            # debug
            print(f"Document term '{term}': tf={tf}, weighted_tf={weighted_tf:.4f}")
            idf = math.log(self.num_documents / (self.df.get(term, 0) + 1), 10) if self.df.get(term,0) > 0 else math.log(self.num_documents, 10)
            query_vector[term] = weighted_tf * idf
            #debug print(f"Vector: {query_vector[term]}")
        scores = []
        for doc_idx in range(self.num_documents):
            score = 0.0
            doc_vector = self.doc_vectors[doc_idx]
            for term, query_weight in query_vector.items():
                doc_weight = doc_vector.get(term, 0.0)
                score += doc_weight * query_weight
            scores.append((doc_idx, score))
        scores.sort(key=lambda x: (-x[1], x[0]))

        # debug
        print([(doc_idx, f"{score:.4f}") for doc_idx, score in scores[:10]])

        return [doc_idx for doc_idx, score in scores[:10]]

    def get_document_frequency(self, term):
        return self.df.get(term.lower(), 0)

    def get_top_terms(self, n=20):
        """Returns the top n terms with highest normalized weights across all documents"""
        term_weights = []

        for doc_idx, doc_vector in enumerate(self.doc_vectors):
            for term, weight in doc_vector.items():
                term_weights.append((term, doc_idx, weight))

        # Sort by weight descending, then by term ascending for ties
        term_weights.sort(key=lambda x: (-x[2], x[0]))

        return term_weights[:n]


def main(corpus):
    with open(corpus, 'r', encoding='utf-8') as file:
        ir = IRSystem(file)

    while True:
        query = input('Query: ').strip()
        if query == 'exit':
            break
        results = ir.run_query(query)
        print(results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("CORPUS",
                        help="Path to file with the corpus")
    args = parser.parse_args()
    main(args.CORPUS)
