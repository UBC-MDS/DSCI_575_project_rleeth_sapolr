from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi
import re
from collections import defaultdict
from pathlib import Path
import pickle

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
BM25_PATH = PROCESSED_DIR / "bm25_index.pkl"


def text_tokenizer(text: str) -> list[str]:
    stopwords = {
    "the","a","an","and","is","are","to","of","in",
    "for","on","with","this","that","it","be"
    }
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in stopwords]
    return tokens

def build_bm25(documents: list[Document], force_rebuild: bool = False):
    if BM25_PATH.exists() and not force_rebuild:
        with open(BM25_PATH, "rb") as f:
            return pickle.load(f)

    texts = [doc.page_content for doc in documents]

    tokenized_corpus = [
        text_tokenizer(text)
        for text in texts
    ]
    bm25 = BM25Okapi(tokenized_corpus)

    BM25_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(BM25_PATH, "wb") as f:
        pickle.dump(bm25, f)

    return bm25

def bm25_search(bm25, documents: list[Document], query: str, k=5):

    tokenized_query = text_tokenizer(query)

    scores = bm25.get_scores(tokenized_query)

    product_scores = defaultdict(float)
    product_docs = {}

    for i, score in enumerate(scores):

        doc = documents[i]
        asin = doc.metadata["asin"]

        # keep the highest score among reviews for each product
        product_scores[asin] = max(product_scores[asin], score)
        if asin not in product_docs:
            product_docs[asin] = doc

    ranked_products = sorted(product_scores.items(), key=lambda x: x[1], reverse=True)[:k]

    results = [(product_docs[asin], score) for asin, score in ranked_products]
    return results
