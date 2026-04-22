# Final Discussion

## Step 1: Improve Your Workflow

### Dataset Scaling

-   Number of products used
-   Changes to sampling strategy (if any)

### LLM Experiment

-   Models compared (name, family, size)
-   Results and discussions
    -   Prompt used (copy it here)
    -   Results
-   Which model you chose and why

## Step 2: Additional Feature (state which option you chose)

### Option 4 (Deploy your application)

Key Summary

-   We have already deployed our application in milestone 2. We chose to deploy on Streamlit, so users can interact with the beauty product search system without running the code locally. Our website is essentially interactive beauty product search with 2 main tabs. The first tab is only for searching based on a query while the other tab is by using RAG pipeline where users can enter a question about a product to get product recommendation based on retrieved reviews.
-   First, the search tab allows for 3 different search modes: BM25, semantic, and hybrid. In each search, the default number of results is 3, but the users can choose to display 1, 2, or 3. For BM25, this is optimized for keyword matching mostly where products with matching keywords will be likely to be returned after searching. For semantic search, this captures semantic meaning of the query and return products which have similar semantic meaning. Lastly, hybrid search is essentially a search which combines results from both BM25 and semantic search together.
-   In the RAG tab, users could enter a product question and have the RAG mode generate recommendation based on retrieved reviews. The 2 search modes are semantic and hybrid which leverages both BM25 and semantic approaches.
-   In order to accelerate the search, we used @st.cache_resource to cache expensive resources such as loaded documents, BM25 index, FAISS vector score, and RAG pipeline.
-   Product reviews are truncated for readability while still preserving enough text to explain why a product was retrieved or recommended.

Key Examples

-   Users can enter queries such as "makeup to cover up pimples" or "something to keep your face moisturized all day"
-   In Search mode, the app would return top matching products with product titles, reviews, ASINs, ratings, and retrieval scores.
-   In RAG mode, the app would generate a recommendation that includes product title, ASIN, rating, review, and reason for recommendation.

## Step 3: Improve Documentation and Code Quality

### Documentation Update

-   Summary of `README` improvements

### Code Quality Changes

-   Summary of cleanups

## Step 4: Cloud Deployment Plan

(See Step 4 above for required subsections)
