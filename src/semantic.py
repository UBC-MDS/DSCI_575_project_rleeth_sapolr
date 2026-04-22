from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

def sample_documents_by_asin(documents, max_products):
    """
    Sample documents by limiting to the first `max_products` unique ASINs.
    Includes all documents for selected ASINs while preventing new products after the limit.
    Args:
        documents (list[Document]): List of documents to sample.
        max_products (int): Maximum number of products to sample.
    Returns:
        list[Document]: List of sampled documents.
    """
    selected_docs = []
    seen_asins = set()

    for doc in documents:
        asin = doc.metadata["asin"]

        if asin not in seen_asins:
            if len(seen_asins) >= max_products:
                break
            seen_asins.add(asin)

        selected_docs.append(doc)

    return selected_docs

def create_faiss_index(documents, embedding_model, sample_size=None, reload_index=False):
    """
    Create or load a FAISS index for semantic search.
    Optionally samples documents by unique ASINs and caches the index for reuse.
    Args:
        documents (list[Document]): List of documents to index.
        embedding_model (HuggingFaceEmbeddings): Embedding model to use.
        sample_size (int | None): Maximum number of products to sample.
        reload_index (bool): Whether to reload the index.
    Returns:
        FAISS: FAISS index.
    """
    index_path = "../data/processed/faiss_index"

    # Load index if it exists
    if os.path.exists(index_path) and not reload_index:
        vectorstore = FAISS.load_local(
            index_path,
            embedding_model,
            allow_dangerous_deserialization=True
        )

    # Otherwise create and save it
    else:
        if sample_size is None:
            docs = documents
        else:
            docs = sample_documents_by_asin(documents, sample_size)

        vectorstore = FAISS.from_documents(
            docs,
            embedding_model
        )

        vectorstore.save_local(index_path)
    return vectorstore

def semantic_search(documents, query, k=5, sample_size=None, reload_index=False):
    """
    Perform semantic search and return top-k products based on similarity scores.
    Aggregates results at the ASIN level by selecting the best-scoring document per product.
    Args:
        documents (list[Document]): List of documents to search.
        query (str): The query to search for.
        k (int): Number of results to return.
        sample_size (int | None): Maximum number of products to sample.
        reload_index (bool): Whether to reload the index.
    Returns:
        list[tuple[Document, float]]: List of (document, score) pairs.
    """
    vectorstore = create_faiss_index(documents, sample_size, reload_index)

    results = vectorstore.similarity_search_with_score(query, k=len(vectorstore.docstore._dict))

    product_scores = {}
    product_docs = {}

    for doc, score in results:

        asin = doc.metadata["asin"]

        if asin not in product_scores or score < product_scores[asin]:
            product_scores[asin] = score
            product_docs[asin] = doc

    ranked_products = sorted(product_scores.items(), key=lambda x: x[1])[:k]

    results = [(product_docs[asin], score) for asin, score in ranked_products]
    return results
    
# To speed up Streamlit
def load_vectorstore(documents, sample_size=10000):
    """
    Load a cached FAISS vector store for faster semantic search.
    Reuses an existing index if available, otherwise creates one.
    Args:
        documents (list[Document]): List of documents to index.
        sample_size (int): Maximum number of products to sample.
    Returns:
        FAISS: FAISS index.
    """
    return create_faiss_index(documents, sample_size=sample_size, reload_index=False)