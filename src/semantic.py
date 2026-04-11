from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os

def semantic_search(documents, query, k=5, sample_size=None, reload_index=False):
    
    embedding_model = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    
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
        docs = documents if sample_size is None else documents[:sample_size]

        vectorstore = FAISS.from_documents(
            docs,
            embedding_model
        )

        vectorstore.save_local(index_path)

    results = vectorstore.similarity_search_with_score(query, k=len(documents))

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