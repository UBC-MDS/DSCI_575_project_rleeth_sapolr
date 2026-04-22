from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate

from src.semantic import create_faiss_index
from src.data_loader import load_documents
from src.hybrid import create_hybrid_retriever

from dotenv import load_dotenv
import streamlit as st
import os
import json
import re

load_dotenv()

token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not token:
    try:
        token = st.secrets["HUGGINGFACEHUB_API_TOKEN"]
    except Exception:
        token = None

if not token:
    raise ValueError(
        "Missing HUGGINGFACEHUB_API_TOKEN. "
        "Set it in a local .env file or in Streamlit secrets."
    )
    
class RAGPipeline:

    def __init__(self, model_name="Qwen/Qwen3.5-2B", top_k=3):

        self.documents = load_documents()

        # Create vector store
        vectorstore = create_faiss_index(self.documents, 10000, reload_index=False)
        
        # Semantic retriever
        self.semantic_retriever = vectorstore.as_retriever(
            search_kwargs={"k": top_k}
        )
        
        # Hybrid retriever
        self.hybrid_retriever = create_hybrid_retriever(
            self.documents,
            vectorstore,
            top_k=top_k,
            weights=(0.4, 0.6),
        )

        llm_endpoint = HuggingFaceEndpoint(
            repo_id="meta-llama/Meta-Llama-3-8B-Instruct",
            task="text-generation",          
            max_new_tokens=150,
            huggingfacehub_api_token=token,
            provider="auto"           
        )

        self.llm = ChatHuggingFace(llm=llm_endpoint)

        self.semantic_chain = self._build_chain(self.semantic_retriever)
        self.hybrid_chain = self._build_chain(self.hybrid_retriever)

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

    def _build_chain(self, retriever):
        format_context = RunnableLambda(self.build_context)

        rag_chain = (
            {
                "context": retriever | format_context,
                "input": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

        return rag_chain

    def ask(self, query, mode="hybrid"):
        if mode == "semantic":
            response = self.semantic_chain.invoke(query)
        elif mode == "hybrid":
            response = self.hybrid_chain.invoke(query)
        else:
            raise ValueError("mode must be either 'semantic' or 'hybrid'")
    
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return match.group(0)
    
        return response