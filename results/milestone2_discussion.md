# Milestone 2 Discussion

## **1.2 Model Choice and Rationale**

For this project, we selected the Qwen3.5-2B model. The model has around 2 billion parameters, which makes it large enough to generate useful responses while still being manageable to run locally. Since the system is designed to run on a laptop rather than on large GPUs, choosing a model that can operate efficiently on local hardware was an important consideration. The Qwen family of models is known for having good reasoning and instruction-following abilities while remaining lightweight enough for local use.

Another reason for choosing this model was the balance it offers between performance and computational requirements. Larger language models often produce higher quality responses, but they typically require much more memory and longer inference times. For this project, using a smaller model like Qwen3.5-2B allows the system to generate responses more quickly and with lower resource usage while still maintaining good response quality.

The model is also instruction-tuned, which makes it well suited for retrieval-augmented generation (RAG). In this system, the model receives product reviews and metadata retrieved from the dataset and must generate recommendations based on that information. Instruction-tuned models are generally better at following structured prompts and staying within the provided context, which helps produce responses that are more relevant and reduces the likelihood of hallucinated information.

Overall, Qwen3.5-2B offers a good balance between reasoning ability, response quality, and the ability to run locally. This makes it a practical choice for building a RAG-based product recommendation assistant.

## **2.3 System Prompt Exploration and Variants**
## Prompt Design and Iteration

When we were developing the system prompt, we experimented with different variants to improve the quality and consistency of the generated recommendations and output format. The main challenges we experienced was ensuring that the model followed the required output format, stayed grounded in the provided context, and avoided generating unnecessary reasoning or extra text.

### Initial Prompt
The initial prompt we used was provided in the Milestone 2 guide and focused on instructing the model to act as an Amazon shopping assistant and answer using only the provided context. While this worked reasonably well, the model often:
- Included additional explanations beyond the required format  
- Repeated parts of the prompt  
- Generated verbose or inconsistent outputs that was not formatted with the required product metadata
Sample prompt: """
    You are a helpful Amazon shopping assistant.
    Answer the question using ONLY the following context (real product reviews + metadata).
    Always cite the product ASIN when possible.
    context:
    query:
    Answer based on the Amazon datasets: """

### Structured Output Prompt
We then introduced a stricter format by explicitly specifying the expected output structure in the prompt to include the metadata (Product Title, ASIN, Rating, Review, and Reason). This improved consistency, but the model still occasionally:
- Added extra text before or after the answer  
- Produced reasoning-style outputs or step-by-step explanations  
- When using the Qwen3.5-2B model, the output still showed the thought process of the large language model
Sample prompt: """
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
"""

### Final Prompt (Selected)
The final prompt included stronger constraints, such as:
- Explicit instruction to avoid including any thinking process (`no_think`)  
- Clear formatting requirements  
- A concise instruction for generating a two-sentence recommendation  

This version produced the most reliable results, with:
- Consistent formatting across responses  
- More natural and user-friendly recommendation text  
- Reduced unnecessary reasoning or prompt repetition
Sample prompt: """
    `***/no_think. DO NOT include any thinking process***`
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
"""

### Key Findings
- Providing a strict output format significantly improves consistency  
- Adding explicit constraints (e.g., no reasoning, no extra text) helps reduce unwanted generation behavior  
- Smaller instruction-tuned models may still produce extra text, so prompt design alone is not always sufficient  

Overall, iterative prompt refinement was essential in achieving stable and usable outputs for the RAG-based recommendation system.