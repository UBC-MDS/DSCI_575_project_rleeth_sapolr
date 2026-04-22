from langchain_community.retrievers import BM25Retriever

try:
    from langchain.retrievers import EnsembleRetriever
except ImportError:
    from langchain_classic.retrievers import EnsembleRetriever


def create_hybrid_retriever(documents, vectorstore, top_k=3, weights=(0.4, 0.6)):
    """
    Create a hybrid retriever using BM25 and semantic search.
    Args:
        documents (list[Document]): List of documents to index.
        vectorstore (FAISS): FAISS vector store.
        top_k (int): Number of top results to return.
        weights (tuple): Tuple of weights for BM25 and semantic search.
    Returns:
        EnsembleRetriever: Hybrid retriever.
    """
    # BM25 retriever
    bm25_retriever = BM25Retriever.from_documents(documents)
    bm25_retriever.k = top_k

    # Semantic retriever
    semantic_retriever = vectorstore.as_retriever(
        search_kwargs={"k": top_k}
    )

    # Hybrid retriever
    hybrid_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, semantic_retriever],
        weights=list(weights)
    )

    return hybrid_retriever