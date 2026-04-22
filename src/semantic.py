from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

def sample_documents_by_asin(documents, max_products):
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
    return create_faiss_index(documents, sample_size=sample_size, reload_index=False)