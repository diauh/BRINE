"""
preprocessing.py
----------------
All text cleaning for BRINE happens in this file.

The SAME function (preprocess_text) is used for:
  1. the 30 documents in documents.json
  2. the user's search query

This is important: if both sides are cleaned in the same way,
the TF-IDF comparison is fair.
"""

import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


# ----------------------------------------------------------------------
# STEP 0: Make sure the small NLTK data packages exist.
# They are downloaded only the first time the project runs.
# ----------------------------------------------------------------------
def download_nltk_resources():
    resources = [
        ("tokenizers/punkt", "punkt"),
        ("tokenizers/punkt_tab", "punkt_tab"),
        ("corpora/stopwords", "stopwords"),
    ]
    for path, package in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            try:
                nltk.download(package, quiet=True)
            except Exception:
                pass


download_nltk_resources()


# Created once and reused
STEMMER = PorterStemmer()

try:
    STOP_WORDS = set(stopwords.words("english"))
except LookupError:
    STOP_WORDS = set()


# ----------------------------------------------------------------------
# Helper: lowercase + remove punctuation / special characters
# ----------------------------------------------------------------------
def clean_text(text):
    text = str(text).lower()                       # 1. lowercase
    text = re.sub(r"[^a-z0-9\s]", " ", text)       # 2. remove punctuation
    text = re.sub(r"\s+", " ", text).strip()       # tidy up extra spaces
    return text


# ----------------------------------------------------------------------
# MAIN FUNCTION used everywhere in the project
# ----------------------------------------------------------------------
def preprocess_text(text):
    """
    Clean one piece of text and return it as a string of stemmed words.
    """
    if text is None:
        return ""

    text = clean_text(text)

    try:
        tokens = word_tokenize(text)
    except LookupError:
        tokens = text.split()

    tokens = [word for word in tokens if word not in STOP_WORDS and len(word) > 1]
    tokens = [STEMMER.stem(word) for word in tokens]

    return " ".join(tokens)


if __name__ == "__main__":
    sample = "The Blue Whales are swimming quickly through the oceans!"
    print("Original :", sample)
    print("Processed:", preprocess_text(sample))