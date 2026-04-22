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

-   Users can enter queries such as "makeup to cover up pimples"
-   In Search mode, the app would return top matching products with product titles, reviews, ASINs, ratings, and retrieval scores.
    -   Example results from "makeup to cover up pimples" query under BM25 search mode:

        **Top 3 Results**

        **1. Privacy Uv Face Powder SPF50 ++++ 3.5g New Package**

        **Review:** Tiny but good! I like it more than cover up. Natural look 👍

        **ASIN:** B079LFDTKQ

        **Rating:** ⭐⭐⭐⭐⭐ (5.0)

        **Retrieval score:** 10.1476

        **2. Flawless Finish Foundation, Colour Changing Foundation, All-Day Flawless Foundation Makeup, Covering Imperfections Liquid Complete Foundation, Suitable for ALL Skin Types**

        **Review:** I do like this make up, but it certainly doesn’t cover for me the way it showed in the advertisement.

        **ASIN:** B07VNQ4G13

        **Rating:** ⭐⭐⭐⭐ (4.0)

        **Retrieval score:** 9.6734

        **3. Full Coverage Cream Compact Foundation, Waterproof Long Wearing Matte Face Cream Foundation for Face Makeup, Oil- Control,Smooth and No Caking, Natural**

        **Review:** Very Heavy! Does not mix well with other makeup. Once I placed my powered on top of this it seemed to turn a shade of gray and made it look like I was attempting to cover up bruising ...... Very Stran...

        **ASIN:** B01MZ62E1V

        **Rating:** ⭐⭐ (2.0)

        **Retrieval score:** 9.5053
-   In RAG mode, the app would generate a recommendation that includes product title, ASIN, rating, review, and reason for recommendation.
    -   Example results from "makeup to cover up pimples" query under hybrid mode:

        **Recommended Product**

        **Product Title:** Dermacol Make-up Cover - Waterproof Hypoallergenic Foundation 30g 100% Original Guaranteed (221)

        **ASIN:** B077W5YRNG

        **Rating:** 5.0

        **Review:** I love this stuff. It is great for acne coverage. Love love.

        **Reason:** I recommend this makeup because it is great for acne coverage. It is also water proof and hypoallergenic which will help prevent any irritation to the skin around the pimples.

Step 3: Improve Documentation and Code Quality

### Documentation Update

-   Summary of `README` improvements

### Code Quality Changes

-   Summary of cleanups

## Step 4: Cloud Deployment Plan

We plan to deploy it using AWS which could separate storage, indexing, application serving, and update pipelines.

1.  Data Storage: Where will you store the following?

    -   raw data

    -   processed data

    -   vector index

    -   BM25 index

    For data storage, we plan to store raw Amazon review and product data in object storage such as Amazon S3 since it is suitable for storing large datasets. Processed data should also be stored in Amazon S3 and it should probably be stored in a structured format as Parquet to allow for efficient downstream loading. Vector index and BM25 index are relatively smaller in size compared to others. We could also store them in Amazon S3 but we would need to make sure to load them into EC2 when the app starts to allow for faster retrievals.

2.  Compute

    -   Where will your app run?

    -   How will you handle multiple users (concurrency)?

    -   How will you handle LLM inference (API vs hosted model)?

    The app deployed in Streamlit could run on an EC2 instance. EC2 would be suitable because it is easy to set up and it should be good enough to handle this Amazon dataset. When the server starts, it would load processed data, BM25, and FAISS indexes from S3. Then, users can access the app via EC2 public IP.

    One EC2 instance should be able to handle a few users at a time. However, if there are multiple users, we probably need to upgrade to a bigger EC2 instance. Or, we can run multiple instances with a load balancer.

    For LLM inference, we would use an API instead of hosting a model because there is no need for GPUs. Also, it would be faster and lighter to implement using API.

3.  Streaming/Updates

    -   How will you incorporate new products in production?

    -   How will your pipeline stay up to date?

    When there are new products in production, we would upload new data to S3 and keep all versions of our data in S3. In other words, we would use a versioned structure to ensure data are not overwritten and allow for reproducibility and traceability. When new products come in, we would rerun the preprocessing script to clean data, generate embeddings, and update BM25 and FAISS indexes. Once these steps are done, the app will be reloaded based on these newly processed data. To reduce risk, we should also implement a validation system to check if the updated version is valid before having the app load based on updated data.

    In order to keep our pipeline stay up to date, we would need to schedule a frequent update based on how frequent new data come in. For instance, if new products come in weekly, we would schedule our update to be weekly as well.
