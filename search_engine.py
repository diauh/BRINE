"""
search_engine.py
----------------
This file contains the actual "search engine".

How it works:
  1. TF-IDF        -> converts text into numbers (vectors)
  2. Cosine Similarity -> measures how close two vectors are
  3. Ranking       -> highest similarity first
  4. Category filter -> keeps only documents of the chosen category
"""

import json
import os
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocessing import preprocess_text


# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "documents.json")

ALL_CATEGORIES = "All Categories"

CATEGORIES = [
    "Ocean Animals",
    "Deep Sea Life",
    "Ocean Habitats",
    "Ocean Depths",
    "Underwater Wonders",
]


# ----------------------------------------------------------------------
# Loading the dataset
# ----------------------------------------------------------------------
def load_documents(file_path=DATASET_PATH):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def build_searchable_text(document):
    """Combine all searchable fields into one string."""
    keywords_text = " ".join(document.get("keywords", []))
    return " ".join([
        document.get("title", ""),
        document.get("category", ""),
        keywords_text,
        document.get("description", ""),
    ])


# ----------------------------------------------------------------------
# The Search Engine class
# ----------------------------------------------------------------------
class SearchEngine:
    """Builds the TF-IDF model once, then answers any number of queries."""

    def __init__(self, file_path=DATASET_PATH):
        self.documents = load_documents(file_path)

        self.processed_documents = [
            preprocess_text(build_searchable_text(doc)) for doc in self.documents
        ]

        self.vectorizer = TfidfVectorizer()
        self.document_matrix = self.vectorizer.fit_transform(self.processed_documents)

    def search(self, query, category=ALL_CATEGORIES, top_k=10):
        query = (query or "").strip()

        if category not in CATEGORIES:
            category = ALL_CATEGORIES
        category_filter = None if category == ALL_CATEGORIES else category

        # Browse mode: no query, only a category
        if not query:
            browse_documents = [
                doc for doc in self.documents
                if category_filter is None or doc["category"] == category_filter
            ]
            return [self._make_result(doc, None) for doc in browse_documents]

        processed_query = preprocess_text(query)

        if not processed_query:
            return []

        query_vector = self.vectorizer.transform([processed_query])
        similarity_scores = cosine_similarity(query_vector, self.document_matrix)[0]

        results = []
        for index, score in enumerate(similarity_scores):
            document = self.documents[index]

            if category_filter is not None and document["category"] != category_filter:
                continue

            if score <= 0.15:
                continue

            results.append(self._make_result(document, round(float(score) * 100, 1)))

        results.sort(key=lambda item: item["relevance"], reverse=True)

        return results[:top_k]

    def random_document(self):
        return random.choice(self.documents)

    @staticmethod
    def _make_result(document, relevance):
        return {
            "id": document["id"],
            "title": document["title"],
            "category": document["category"],
            "description": document["description"],
            "keywords": document.get("keywords", []),
            "relevance": relevance,
        }


# ----------------------------------------------------------------------
# Manual test:  python search_engine.py
# ----------------------------------------------------------------------
if __name__ == "__main__":
    engine = SearchEngine()

    test_queries = [
        "largest animal in the ocean",
        "fish that produces light",
        "transparent headed fish",
        "underwater forests",
        "deepest ocean location",
        "animals that use echolocation",
        "coastal forests",
        "animals living near hot vents",
        "ocean layers without sunlight",
        "underwater mountains",
    ]

    for q in test_queries:
        print("\nQUERY:", q)
        for r in engine.search(q)[:3]:
            print(f"   {r['title']:<28} {r['relevance']}%")