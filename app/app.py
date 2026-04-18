from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import streamlit as st

# Make project root importable when running: streamlit run app/app.py
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

# Project imports
from src.bm25 import bm25_search, build_bm25
from src.semantic import semantic_search
from src.data_loader import load_documents
from src.rag_pipeline import RAGPipeline

st.set_page_config(page_title="Beauty Product Search", layout="wide")

@st.cache_resource
def load_bm25_index():
    documents = load_documents()
    return build_bm25(documents)


@st.cache_resource
def load_resources():
    documents = load_documents()
    bm25 = load_bm25_index()
    return documents, bm25
    
@st.cache_resource
def load_rag_pipeline():
    return RAGPipeline(top_k=3)

# ---------- Helpers ----------
def truncate_text(text: str, max_chars: int = 200) -> str:
    text = (text or "").strip()
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "..."


def format_result(result: tuple[Document, float]) -> dict[str, Any]:
    doc, score = result
    metadata = getattr(doc, "metadata", {}) or {}

    return {
        "title": metadata.get("product_title", "N/A"),
        "asin": metadata.get("asin", "N/A"),
        "review_text": truncate_text(
            metadata.get("product_review") or getattr(doc, "page_content", ""),
            max_chars=200,
        ),
        "rating": metadata.get("product_rating", "N/A"),
        "score": float(score),
    }


def deduplicate_results(
    results: list[dict[str, Any]],
    key: str = "asin",
    top_k: int = 3,
) -> list[dict[str, Any]]:
    seen = set()
    unique_results = []

    for r in results:
        value = r.get(key)
        if value not in seen:
            seen.add(value)
            unique_results.append(r)
        if len(unique_results) == top_k:
            break

    return unique_results


def normalize_scores(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not results:
        return results

    scores = [r["score"] for r in results]
    min_score, max_score = min(scores), max(scores)

    if max_score == min_score:
        for r in results:
            r["norm_score"] = 1.0
        return results

    for r in results:
        r["norm_score"] = (r["score"] - min_score) / (max_score - min_score)

    return results


def hybrid_search_results(
    bm25_raw: list[tuple[Document, float]],
    semantic_raw: list[tuple[Document, float]],
    top_k: int = 3,
) -> list[dict[str, Any]]:
    bm25_formatted = normalize_scores([format_result(r) for r in bm25_raw])
    semantic_formatted = normalize_scores([format_result(r) for r in semantic_raw])

    fused: dict[str, dict[str, Any]] = {}

    for r in bm25_formatted:
        asin = r["asin"]
        if asin not in fused:
            fused[asin] = {**r, "hybrid_score": 0.0}
        fused[asin]["hybrid_score"] += 0.5 * r["norm_score"]

    for r in semantic_formatted:
        asin = r["asin"]
        if asin not in fused:
            fused[asin] = {**r, "hybrid_score": 0.0}
        fused[asin]["hybrid_score"] += 0.5 * r["norm_score"]

    results = list(fused.values())
    results.sort(key=lambda x: x["hybrid_score"], reverse=True)

    for r in results:
        r["score"] = r["hybrid_score"]

    return results[:top_k]


def render_rating(rating: Any) -> str:
    try:
        rating_float = float(rating)
        stars = "⭐" * max(1, min(5, round(rating_float)))
        return f"{stars} ({rating_float:.1f})"
    except (TypeError, ValueError):
        return str(rating)

# ---------- UI ----------
st.title("Interactive Beauty Product Search")
st.write("Search with BM25, Semantic Search, Hybrid retrieval, or use RAG mode.")

tab_search, tab_rag = st.tabs(["Search", "RAG"])

with tab_search:
    st.subheader("Search Only")
    mode = st.radio(
        "Search mode",
        ["BM25", "Semantic", "Hybrid"],
        horizontal=True,
    )
    
    query = st.text_input(
        "Enter your query",
        placeholder="e.g. makeup to cover up pimples",
    )
    
    top_k = st.slider("Number of results", min_value=1, max_value=3, value=3)
    
    search_clicked = st.button("Search", type="primary")
    
    if search_clicked:
        if not query.strip():
            st.warning("Please enter a query.")
            st.stop()
    
        documents, bm25 = load_resources()
    
        with st.spinner("Searching..."):
            if mode == "BM25":
                raw_results = bm25_search(bm25, documents, query, k=10)
                results = deduplicate_results(
                    [format_result(r) for r in raw_results],
                    top_k=top_k,
                )
    
            elif mode == "Semantic":
                raw_results = semantic_search(
                    documents,
                    query,
                    k=10,
                    sample_size=10000,
                    reload_index=False,
                )
                results = deduplicate_results(
                    [format_result(r) for r in raw_results],
                    top_k=top_k,
                )
    
            else:
                bm25_raw = bm25_search(bm25, documents, query, k=10)
                semantic_raw = semantic_search(
                    documents,
                    query,
                    k=10,
                    sample_size=10000,
                    reload_index=False,
                )
                results = hybrid_search_results(bm25_raw, semantic_raw, top_k=top_k)

        st.subheader(f"Top {len(results)} Results")
    
        if not results:
            st.info("No results found.")
        else:
            for idx, result in enumerate(results, start=1):
                with st.container(border=True):
                    st.markdown(f"### {idx}. {result['title']}")
                    col1, col2 = st.columns([3, 2])
    
                    with col1:
                        st.write(f"**Review:** {result['review_text']}")
                        st.write(f"**ASIN:** {result['asin']}")
    
                    with col2:
                        st.write(f"**Rating:** {render_rating(result['rating'])}")
                        st.write(f"**Retrieval score:** {result['score']:.4f}")
                        
# Add RAG mode                        
with tab_rag:
    st.subheader("RAG Mode")

    rag_query = st.text_input(
        "Enter your product question",
        placeholder="e.g. something to keep your face moisturized all day",
        key="rag_query",
    )

    rag_clicked = st.button("Generate Recommendation", type="primary", key="rag_button")

    if rag_clicked:
        if not rag_query.strip():
            st.warning("Please enter a query.")
            st.stop()

        rag = load_rag_pipeline()

        with st.spinner("Generating answer..."):
            answer = rag.ask(rag_query)

        st.markdown("## Recommended Product")

        if isinstance(answer, dict):
            with st.container(border=True):
                st.write(f"**Product Title:** {answer.get('product_title', 'N/A')}")
                st.write(f"**ASIN:** {answer.get('product_asin', 'N/A')}")
                st.write(f"**Rating:** {answer.get('product_rating', 'N/A')}")
                st.write(f"**Review:** {truncate_text(answer.get('product_review', ''), 300)}")
                st.write(f"**Reason:** {answer.get('reason_for_recommendation', 'N/A')}")
        else:
            st.write(answer)