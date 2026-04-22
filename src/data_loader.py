from __future__ import annotations

import json
import gzip
from pathlib import Path
from typing import Any

from langchain_core.documents import Document

ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

REVIEWS_PATH = RAW_DIR / "All_Beauty.jsonl"
META_PATH = RAW_DIR / "meta_All_Beauty.jsonl"
SAMPLE_DOCS_PATH = PROCESSED_DIR / "sample_documents.jsonl.gz"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """
    Load a JSONL file into a list of dictionaries.
    Each line in the file is parsed as a JSON object and added to a list.
    Args:
        path (Path): Path to the JSONL file.
    Returns:
        list[dict[str, Any]]: List of parsed JSON objects.
    """
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def load_gz_jsonl(path: Path) -> list[dict[str, Any]]:
    """
    Load a gzip-compressed JSONL file into a list of dictionaries.
    Each line in the file is parsed as a JSON object and added to a list.
    Args:
        path (Path): Path to the gzip-compressed JSONL file.
    Returns:
        list[dict[str, Any]]: List of parsed JSON objects.
    """
    data = []
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data

def save_documents_to_gz_jsonl(documents: list[Document], path: Path) -> None:
    """
    Save a list of documents to a gzip-compressed JSONL file.
    Each document is converted to a JSON object and written to the file.
    Args:
        documents (list[Document]): List of documents to save.
        path (Path): Path to the gzip-compressed JSONL file.
    Returns:
        None
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt", encoding="utf-8") as f:
        for doc in documents:
            row = {
                "asin": doc.metadata.get("asin"),
                "product_review": doc.metadata.get("product_review"),
                "product_title": doc.metadata.get("product_title"),
                "product_rating": doc.metadata.get("product_rating"),
            }
            f.write(json.dumps(row) + "\n")


def load_raw_data() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Load raw review and metadata data from the JSONL files.
    Args:
        None
    Returns:
        tuple[list[dict[str, Any]], list[dict[str, Any]]]: Tuple of lists of review and metadata dictionaries.
    """
    reviews = load_jsonl(REVIEWS_PATH)
    meta = load_jsonl(META_PATH)
    return reviews, meta


def build_documents_from_rows(rows: list[dict[str, Any]]) -> list[Document]:
    """
    Build a list of documents from a list of dictionaries.
    Each dictionary is converted to a Document object and added to the list.
    Args:
        rows (list[dict[str, Any]]): List of dictionaries to convert to documents.
    Returns:
        list[Document]: List of Document objects.
    """
    documents: list[Document] = []

    for row in rows:
        review_text = (row.get("product_review") or "").strip()
        if not review_text:
            continue

        documents.append(
            Document(
                page_content=review_text,
                metadata={
                    "asin": row.get("asin", "N/A"),
                    "product_review": review_text,
                    "product_title": row.get("product_title", "Unknown product"),
                    "product_rating": row.get("product_rating", "N/A"),
                },
            )
        )

    return documents


def build_documents_from_raw(max_products: int | None = None) -> list[Document]:
    """
    Build a list of documents from raw review and metadata data.
    Args:
        max_products (int | None): Maximum number of products to include.
    Returns:
        list[Document]: List of Document objects.
    """
    reviews, meta = load_raw_data()

    meta_by_parent_asin = {
        item.get("parent_asin"): item
        for item in meta
        if item.get("parent_asin") is not None
    }

    documents: list[Document] = []
    seen_asins: set[str] = set()
    for review in reviews:
        parent_asin = review.get("parent_asin")
        if not parent_asin or parent_asin not in meta_by_parent_asin:
            continue

        if max_products is not None and parent_asin not in seen_asins:
            if len(seen_asins) >= max_products:
                break

        product_metadata = meta_by_parent_asin[parent_asin]
        review_text = (review.get("text") or "").strip()

        if not review_text:
            continue

        documents.append(
            Document(
                page_content=review_text,
                metadata={
                    "asin": parent_asin,
                    "product_review": review_text,
                    "product_title": product_metadata.get("title", "Unknown product"),
                    "product_rating": review.get("rating", "N/A"),
                },
            )
        )
        seen_asins.add(parent_asin)
    save_documents_to_gz_jsonl(documents, SAMPLE_DOCS_PATH)
    return documents


def load_documents() -> list[Document]:
    """
    Load documents from the gzip-compressed JSONL file or raw review and metadata data.
    Args:
        None
    Returns:
        list[Document]: List of Document objects.
    """
    if SAMPLE_DOCS_PATH.exists():
        rows = load_gz_jsonl(SAMPLE_DOCS_PATH)
        return build_documents_from_rows(rows)

    if REVIEWS_PATH.exists() and META_PATH.exists():
        return build_documents_from_raw(max_products=10000)

    raise FileNotFoundError(
        f"Could not find sample file {SAMPLE_DOCS_PATH} "
        f"or raw files {REVIEWS_PATH} and {META_PATH}."
    )