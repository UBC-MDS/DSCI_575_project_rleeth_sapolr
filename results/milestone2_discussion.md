# Milestone 2 Discussion

## **1.2 Model Choice and Rationale**

For this project, we selected the meta-llama/Meta-Llama-3-8B-Instruct model. We tested the RAG implementation with several local models (mainly Qwen3.5-2B) but ultimately decided to choose an online hosted model. This decision was primarily driven by deployment requirements, as the application is hosted on Streamlit and therefore benefits from using a remote model rather than relying on local hardware.

The Llama 3 8B model contains approximately 8 billion parameters, making it significantly more powerful than smaller models such as Qwen3.5-2B. This increase in model size leads to improved language understanding, more coherent responses, and better alignment with user queries. While larger models typically require more computational resources, using a hosted API allows us to leverage these capabilities without being constrained by local hardware limitations.

Another advantage of this model is that it is instruction-tuned, which makes it well suited for retrieval-augmented generation (RAG). In this system, the model takes in product reviews and metadata and generates recommendations based only on that context. Instruction-tuned models are generally better at following structured prompts and producing consistent outputs in the required format. Using an online model also improves scalability and responsiveness for the deployed application, since it does not rely on local hardware and can handle queries more reliably through a hosted endpoint.

Overall, Meta-Llama-3-8B-Instruct provides a strong balance between response quality, instruction-following capability, and deployment practicality. Its ability to generate high-quality, context-aware responses makes it a suitable choice for a RAG-based product recommendation system deployed as a web application.

## **2.3 System Prompt Exploration and Variants**

## Prompt Design and Iteration

When we were developing the system prompt, we experimented with different variants to improve the quality and consistency of the generated recommendations and output format. The main challenges we experienced was ensuring that the model followed the required output format, stayed grounded in the provided context, and avoided generating unnecessary reasoning or extra text.

### Initial Prompt

The initial prompt we used was provided in the Milestone 2 guide and focused on instructing the model to act as an Amazon shopping assistant and answer using only the provided context. While this worked reasonably well, the model often: - Included additional explanations beyond the required format\
- Repeated parts of the prompt\
- Generated verbose or inconsistent outputs that was not formatted with the required product metadata Sample prompt:

``` text
You are a helpful Amazon shopping assistant.
Answer the question using ONLY the following context (real product reviews + metadata).
Always cite the product ASIN when possible.

context:
query:

Answer based on the Amazon datasets:
```

### Structured Output Prompt

We then introduced a stricter format by explicitly specifying the expected output structure in the prompt to include the metadata (Product Title, ASIN, Rating, Review, and Reason). This improved consistency, but the model still occasionally: - Added extra text before or after the answer\
- Produced reasoning-style outputs or step-by-step explanations\
- When using the Qwen3.5-2B model, the output still showed the thought process of the large language model

Sample prompt:

``` text
You are a helpful Amazon shopping assistant.
Answer the question using ONLY the following context (real product reviews + metadata).
Always cite the product ASIN when possible.

context:
query:

Recommend ONE product using the context.
Do not add additional explanations or repeat the prompt.
Stop after the recommendation.

Return the answer exactly in this format:

Product Title:
Product ASIN:
Product Rating:
Product Review:
Reason for Recommendation: Write 2 natural sentences describing the product’s key benefits using evidence from the review and rating.

END
```

------------------------------------------------------------------------

### Final Prompt (Selected - Online Model: Llama 3 8B)

After switching to the online model (Meta-Llama-3-8B-Instruct), we further refined the prompt to enforce stricter structure and reduce formatting issues. Instead of relying on labeled text output, we moved to a JSON format, which proved to be more reliable for this model.

Sample prompt:

``` text
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

{
  "product_title": "",
  "product_asin": "",
  "product_rating": "",
  "product_review": "",
  "reason_for_recommendation": ""
}
```

### Key Findings

This final version produced the most reliable results, with: - Consistent and structured outputs\
- Better adherence to the required format\
- More natural and concise recommendations

------------------------------------------------------------------------

### Key Findings

-   Providing a strict output format significantly improves consistency\
-   JSON output works better than labeled text for some models (e.g., Llama)\
-   Adding explicit constraints (e.g., no extra text, fixed structure) helps reduce unwanted generation behavior\
-   Different models require different prompt strategies (e.g., handling `<think>` in Qwen vs enforcing JSON for Llama)

Overall, iterative prompt refinement was essential in achieving stable and usable outputs for the RAG-based recommendation system.

## **5.1 RAG Evaluation**

### **Manual / Qualitative Evaluation for Hybrid RAG Workflow**

| Query | Accuracy | Completeness | Fluency |
|----------------|----------------|------------------------|----------------|
| fit me concealer | Yes | No | Yes |
| something to keep your face moisturized all day | Yes | Yes | Yes |
| makeup to cover up pimples | No | No | Yes |
| best sunscreen for scuba diving in tropical regions | Yes | Yes | Yes |
| good cleanser for busy working professionals who do not have time | Yes | Yes | Yes |

Key observations:

The hybrid RAG system tends to perform well for descriptive queries since it successfully retrieves relevant products and the response is clear and easy to read. However, when certain keywords need to be matched such as "fit me concealer" which is a specific product name, it struggles to return the intended item.

2 Limitations of Hybrid RAG workflow:

One limitation of the Hybrid RAG system is that it sometimes retrieves semantically similar but incorrect products, especially for keyword-based queries such as "fit me concealer" as discussed previously. Another limitation is that the model still does not fully address all conditions for complex queries such as "make up to cover up pimples" since the model still suggests pimple patches instead of actual makeup.

Suggestions for improving workflow's performance:

I would suggest to refine the hybrid retriever by adjusting the weights between BM25 and semantic search to see if the model improves the suggestion or not, especially those with specific keywords/ specific conditions. Also, the prompt could be improved to enforce keyword matching if needed to ensure more accurate and complete responses. Also, more HuggingFace models with different capacities could be used to see if there is a major improvement in product suggestions.
