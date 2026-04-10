from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi
import re

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

def build_bm25(documents: list[Document]):

    texts = [doc.page_content for doc in documents]

    tokenized_corpus = [
        text_tokenizer(text)
        for text in texts
    ]

    bm25 = BM25Okapi(tokenized_corpus)

    return bm25

def bm25_search(bm25, documents: list[Document], query: str, k=5):

    tokenized_query = text_tokenizer(query)

    scores = bm25.get_scores(tokenized_query)

    ranked_idx = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:k]

    results = [
        (documents[i], scores[i])
        for i in ranked_idx
    ]

    return results
