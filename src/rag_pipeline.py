from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from src.semantic import create_faiss_index
from app.app import load_resources


class RAGPipeline:

    SYSTEM_PROMPT = """
    You are a helpful Amazon shopping assistant.
    Answer the question using ONLY the following context (real product reviews + metadata).
    Always cite the product ASIN when possible.
    """

    def __init__(self, model_name="Qwen/Qwen3.5-2B", top_k=3):

        self.documents, self.bm25 = load_resources()

        vectorstore = create_faiss_index(self.documents, 10000, reload_index=False)
        self.retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})

        generator = pipeline(
            "text-generation",
            model=model_name,
            max_length=None,
            max_new_tokens=150,
            do_sample=False,
            return_full_text=False
        )

        self.llm = HuggingFacePipeline(pipeline=generator)

        self.rag_chain = self._build_chain()

    def build_context(self, docs):
        return "\n\n".join(
            f"Product ASIN: {doc.metadata.get('asin')}\n"
            f"Product Title: {doc.metadata.get('product_title')}\n"
            f"Product Rating: {doc.metadata.get('product_rating')}\n"
            f"Product Review: {doc.metadata.get('product_review')}\n"
            for doc in docs
        )

    def build_prompt(self, query, context):
        return f"""{self.SYSTEM_PROMPT}

    context:
    {context}

    question:
    {query}

    Recommend ONE product using the context.

    Return exactly in this format:

    Product Title:
    Product ASIN:
    Product Rating:
    Product Review:
    Reason for Recommendation: Write 2 natural sentences describing the product’s key benefits using evidence from the review and rating.

    END
    """

    def prompt_builder(self, inputs):
        return self.build_prompt(inputs["input"], inputs["context"])

    def _build_chain(self):

        format_context = RunnableLambda(self.build_context)
        prompt = RunnableLambda(self.prompt_builder)

        rag_chain = (
            {
                "context": self.retriever | format_context,
                "input": RunnablePassthrough()
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return rag_chain

    def ask(self, query):

        response = self.rag_chain.invoke(query)
        # 1. Remove <think> block
        if "<think>" in response and "</think>" in response:
            response = response.split("</think>")[-1]

        # 2. Keep only final structured answer
        if "Product Title:" in response:
            response = response.split("Product Title:")[1]
            response = "Product Title:" + response

        # 3. Trim after END
        if "END" in response:
            response = response.split("END")[0]

        return response