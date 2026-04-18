---
editor_options: 
  markdown: 
    wrap: sentence
---

# DSCI_575_project_rleeth_sapolr

DSCI 575 Final Project Repository for Randall Lee and Paul Raadnui

## Project Overview

The final deliverable of this project is a context-aware product search assistant that returns relevant Amazon products based on natural language queries.

## Overview of the dataset

The dataset we chose to work on is from "All_Beauty" category and it could be downloaded from the following websites.

Dataset Website: <https://amazon-reviews-2023.github.io/>

Hugging Face: <https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023>

## EDA

We performed the following EDA to inspect the datasets: - **Dataset size inspection:** Counted the number of records in both datasets (reviews and metadata).
- **Field inspection:** Listed all available fields in the reviews and metadata datasets.
- **Sample record inspection:** Printed example records from both datasets to understand the data structure and relationships between fields.
- **Missing value analysis:** Calculated the percentage of missing values for each field to determine data completeness.
- **Rating distribution analysis:** Visualized the distribution of review ratings to understand overall sentiment patterns in the dataset.

## Data Preprocessing

We performed the following text preprocessing in the text_tokenizer function in the bm25.py script: - **Lowercasing**\
All text was converted to lowercase to ensure that all tokens are treated as the same word.
This reduces unnecessary vocabulary duplication and improves matching between queries and documents.
- **Punctuation Removal**\
Punctuation characters were removed using a regular expression.
This ensures that all tokens are treated consistently and prevents punctuation from being included as part of tokens.
- **Whitespace Tokenization**\
After normalization, text was split into tokens using whitespace.
- **Stopword Removal**\
Common English stopwords (e.g., *the*, *and*, *is*, *to*) were removed to reduce noise in the tokenized corpus.
These words appear frequently but provide little semantic value for distinguishing relevant documents.

## Retrieval Workflow

The system implements the below two retrieval workflows:

### BM25 Retrieval

BM25 performs keyword-based retrieval using the tokenized corpus

Workflow:

1.  **Tokenization**
    -   Documents are tokenized using the preprocessing steps described above.
2.  **Index Construction**
    -   A BM25 index is created using `BM25Okapi` from the tokenized documents.
3.  **Query Processing**
    -   The user query is tokenized using the same tokenizer.
4.  **Scoring**
    -   BM25 computes relevance scores for each document.
5.  **Product Aggregation**
    -   Since multiple reviews may belong to the same product (`asin`), scores are aggregated by product.
    -   The maximum BM25 score among reviews for each product is used.
    -   The top-k products are returned.

------------------------------------------------------------------------

### Semantic Search

Semantic search retrieves products using vector similarity

Workflow:

1.  **Embedding Generation**
    -   Documents are converted to embeddings using the `all-MiniLM-L6-v2` sentence-transformer model.
2.  **Vector Indexing**
    -   Embeddings are indexed using **FAISS**.
3.  **Query Embedding**
    -   The user query is embedded using the same embedding model.
4.  **Similarity Search**
    -   FAISS retrieves review-level documents based on vector distance.
5.  **Product Aggregation**
    -   Results are grouped by `asin`.
    -   For each product, the lowest FAISS distance score (best semantic match) is kept.
    -   The top-k unique products are returned.

### Semantic RAG Pipeline Workflow

``` mermaid
flowchart TD

A[User Query] --> B[Retriever - FAISS vector store]
B --> C[Retrieve Top-K relevant documents]

C --> D[Build Context]

D --> E[Build Prompt]
E --> F[Final Prompt = System Prompt + Context + Query]

F --> G[Feed to LLM - meta-llama/Meta-Llama-3-8B-Instruct]

G --> H[Generated Response]

H --> I[Post-processing]
I --> J[Final Recommendation]
```

## Model Choice

We use Meta-Llama-3-8B-Instruct for the RAG pipeline.

**Rationale:**

We initially experimented with smaller local models such as Qwen3.5-2B **but ultimately chose a hosted model due to deployment requirements. Since our application is deployed using Streamlit,** relying on a remote API allows us to avoid hardware limitations and ensures more stable and scalable performance.

**Model Size Consideration:**

The Llama 3 8B model contains approximately 8 billion parameters, making it significantly more powerful than smaller models like Qwen3.5-2B.
This increased model size results in:

\- Improved language understanding

\- More coherent and fluent responses

\- Better alignment with user queries

While larger models typically require more computational resources, using a hosted API allows us to leverage these capabilities without incurring the cost of local infrastructure.

### Hybrid Retrieval (BM25 + Semantic)

The hybrid retrieval combines keyword-based BM25 and semantic search:

**Workflow**:

1\.
Retrieve top-k results from BM25

2\.
Retrieve top-k results from FAISS semantic search

3\.
Combine results using a weighted EnsembleRetriever from LangChain, which merges results from BM25 and semantic retrievers based on weighted scores (0.4 BM25, 0.6 semantic)

4\.
Aggregate by product (asin)

5\.
Return top-k ranked products

This approach improves retrieval by:

\- Capturing exact keyword matches (BM25)

\- Capturing semantic similarity (embeddings)

### Hybrid RAG Pipeline Workflow

``` mermaid
flowchart TD

A[User Query]

B[BM25 Retriever]

C[FAISS Retriever]

D[Combine Results]

E[Build Context]

F[Prompt Template]

G[LLM]

H[Final Answer]

A --> B

A --> C

B --> D

C --> D

D --> E --> F --> G --> H
```

## Context Building

The context includes:

-   Product ASIN

-   Product title

-   Product rating

-   Product review text

This context is formatted into a structured block before being passed to the LLM.

## Prompt Template

The prompt includes:

-   A system instruction guiding the LLM to act as an Amazon product recommendation assistant

-   Retrieved context from relevant reviews

-   The user query

The prompt enforces strict output constraints:

-   Recommend exactly one product

-   Use only the provided context (no external knowledge)

-   Output must be valid JSON

-   The recommendation reason must contain exactly two complete sentences

This ensures consistent, structured, and grounded responses from the LLM.

## Running the project locally

Follow the steps below to set up the project and run it locally 1.
Clone the repository

Run the following commands in your terminal to clone the repository to your local machine:

``` bash
git clone <https://github.com/UBC-MDS/DSCI_575_project_rleeth_sapolr.git>
cd <DSCI_575_project_rleeth_sapolr>
```

2.  Install the project environment

Navigate to the root of the project dirctory and run:

``` bash
conda env create -f environment_local.yml
conda activate dsci-575-project
```

## API Key Setup

To run the RAG pipeline, you must provide a Hugging Face API token.

### Option 1 (recommended): .env file

Create a `.env` file in the project root:

HUGGINGFACEHUB_API_TOKEN=your_token_here

### Option 2: Streamlit secrets

Create a `.streamlit/secrets.toml` file:

HUGGINGFACEHUB_API_TOKEN = "your_token_here"

## Running the App Locally

``` bash
# Make sure you're in the project root directory
# Run the Streamlit app
streamlit run app/app.py
```

The application will be available at `http://localhost:8501/` (or the port shown in your terminal).

The deployed application is also available on <https://dsci-575-project-rleeth-sapolr.streamlit.app/>
