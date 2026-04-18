from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.retrievers import BM25Retriever
try:
    from langchain.retrievers import EnsembleRetriever
except ImportError:
    from langchain_classic.retrievers import EnsembleRetriever

from src.semantic import create_faiss_index
from app.app import load_resources

from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

token = os.getenv("HUGGINGFACEHUB_API_TOKEN")


class RAGPipeline:

    def __init__(self, model_name="Qwen/Qwen3.5-2B", top_k=3):

        self.documents, self.bm25 = load_resources()

        # Semantic retriever
        vectorstore = create_faiss_index(self.documents, 10000, reload_index=False)
        self.semantic_retriever = vectorstore.as_retriever(
            search_kwargs={"k": top_k}
        )

        # BM25 retriever
        self.bm25_retriever = BM25Retriever.from_documents(self.documents)
        self.bm25_retriever.k = top_k

        # Hybrid retriever
        self.hybrid_retriever = EnsembleRetriever(
            retrievers=[self.bm25_retriever, self.semantic_retriever],
            weights=[0.4, 0.6]
        )

        llm_endpoint = HuggingFaceEndpoint(
            repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
            task="text-generation",          
            max_new_tokens=150,
            huggingfacehub_api_token=token,
            provider="auto"           
        )

        self.llm = ChatHuggingFace(llm=llm_endpoint)

        self.rag_chain = self._build_chain()

    def build_context(self, docs):
        return "\n\n".join(
            f"Product ASIN: {doc.metadata.get('asin')}\n"
            f"Product Title: {doc.metadata.get('product_title')}\n"
            f"Product Rating: {doc.metadata.get('product_rating')}\n"
            f"Product Review: {doc.metadata.get('product_review')}\n"
            for doc in docs
        )

    prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful Amazon shopping assistant.

    You must answer using ONLY the information in the context.

    - Recommend ONE product.
    - Do NOT use outside knowledge.
    - Do NOT include any extra text.
    - Return ONLY valid JSON.

    Context:
    {context}

    Question:
    {input}

    Return exactly in this format:

    {{
    "product_title": "",
    "product_asin": "",
    "product_rating": "",
    "product_review": "",
    "reason_for_recommendation": ""
    }}
    IMPORTANT:
    - The reason_for_recommendation MUST be exactly 2 complete sentences.
    - Do NOT return phrases or fragments.
    """
    )

    def _build_chain(self):
        format_context = RunnableLambda(self.build_context)

        rag_chain = (
            {
                "context": self.hybrid_retriever | format_context,
                "input": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        return rag_chain

    def ask(self, query):

        response = self.rag_chain.invoke(query)

        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                return match.group(0)

        return response