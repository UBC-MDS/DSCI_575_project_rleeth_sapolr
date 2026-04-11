# Milestone 1 Discussion

## **Results**

## Results

| Query | BM25 Results | Semantic Results |
|------|-------------|-----------------|
| ultra facial barrier-hydrating cleanser | 1. Neutrogena Cleanser<br>ASIN: B00U2VQZC4 (17.79) | 1. GOMAY Cleanser<br>ASIN: B09ZDQ626L (0.63)<br><br>2. REBONCEL Cleanser<br>ASIN: B09X23VTSQ (0.66)<br><br>3. Hylunia Body Wash<br>ASIN: B07YNDWRCB (0.71)<br><br>4. Black Wolf Face Wash<br>ASIN: B08GMW3HNG (0.72)<br><br>5. CELIMAX Essence<br>ASIN: B084WP4XS8 (0.73) |
| something to keep your face moisturized all day | 1. BaeBlu Serum<br>ASIN: B01N0AUU5M (19.39)<br><br>2. Vitamin E Cream<br>ASIN: B07TVFCPGP (18.89)<br><br>3. Lip Balm<br>ASIN: B00K1M5VW4 (17.99)<br><br>4. Caviar Cream<br>ASIN: B003D76010 (17.71)<br><br>5. Day Cream<br>ASIN: B005NOIPF0 (17.46) | 1. OZNaturals Mask<br>ASIN: B00L4HJX7O (0.64)<br><br>2. Hyaluronic Serum<br>ASIN: B087D1YQ2H (0.71)<br><br>3. Cellular Cream<br>ASIN: B07W1WJZFG (0.73)<br><br>4. CELIMAX Essence<br>ASIN: B084WP4XS8 (0.74)<br><br>5. Mica Moisturizer<br>ASIN: B0BKRVDTKP (0.75) |
| makeup to cover up pimples | 1. UCANBE Concealer<br>ASIN: B07FPDV8Z5 (16.83)<br><br>2. Boo-Boo Concealer<br>ASIN: B07FX823ZQ (16.46)<br><br>3. Tattoo Concealer<br>ASIN: B07KVRCC6W (15.13)<br><br>4. Waterproof Concealer<br>ASIN: B07Q3BSDC8 (14.63)<br><br>5. Cover Makeup<br>ASIN: B07QQJXJ35 (14.00) | 1. Finishing Spray <br>ASIN: B00BX4E5Y4 (0.71)<br><br>2. Pimple Patch <br>ASIN: B00R2JOSDC (0.72)<br><br>3. Sponge <br>ASIN: B01MRX18Y5 (0.73)<br><br>4. Acne Patch <br>ASIN: B09C7MPYKW (0.78)<br><br>5. Spot Patch <br>ASIN: B078MW6W48 (0.79) |
| best sunscreen for scuba diving in tropical regions | 1. Tropical Sands Sunscreen<br>ASIN: B0184F8LNK (23.84)<br><br>2. Mirror <br>ASIN: B002JAXW6S (23.04)<br><br>3. Honu Sunscreen<br>ASIN: B07MHRJXMS (21.83)<br><br>4. Hair Ties <br>ASIN: B00NPD9SBG (21.70)<br><br>5. Headband <br>ASIN: B0758FDX1W (20.07) | 1. Tropical Sands Sunscreen<br>ASIN: B0184F8LNK (0.60)<br><br>2. Banana Boat Sunscreen<br>ASIN: B00JAXN7JO (0.77)<br><br>3. Panama Jack Lip Balm<br>ASIN: B08G5YVHQP (0.81)<br><br>4. Mineral Sunscreen<br>ASIN: B097CDGX7J (0.85)<br><br>5. Caribbean Sunscreen<br>ASIN: B07L44VWMQ (0.86) |
| good cleanser for busy working professionals | 1. Wig <br>ASIN: B07WR5Y77V (20.60)<br><br>2. Bidet <br>ASIN: B074KD4PX2 (18.96)<br><br>3. Shampoo Set <br>ASIN: B07R1K1SBD (18.04)<br><br>4. Foot Tool <br>ASIN: B00ZSUMHUS (17.08)<br><br>5. Chiropractic Tool <br>ASIN: B0010VSH3K (16.85) | 1. YOUTH LAB Cleanser<br>ASIN: B01EUR8IPW (0.79)<br><br>2. Snail Cleanser<br>ASIN: B01JB2WLCM (0.80)<br><br>3. Dry Tissue Cleanser<br>ASIN: B083BGJ4P9 (0.81)<br><br>4. EASYDEW Cleanser<br>ASIN: B07YS9W97B (0.81)<br><br>5. Cleaner <br>ASIN: B001DESQ2Q (0.83) |
-   Which method performs better for this query? Why?

    The semantic method tends to perform better for most of these queries. We can see from the results table that BM25 method tends to look for specific words observed in the query and return products which have the exact matching words. However, we can see that the semantic method captures the meaning of each query and look for products which have similar meaning but might not necessarily contain specific words. From the east queries, we do not observe significant differences since both methods perform well. However, we can see from the examples from the medium and complex queries that some products suggested by BM25 are not related to the queries such as wigs suggested by BM25 for the query "good cleanser for busy working professionals who do not have time". On the other hand, the semantic method suggests YOUTH LAB Daily Cleanser which aligns with the original query.

-   Are there cases where **BM25 fails** but **semantic search succeeds**?

    One of the examples is from "best sunscreen for scuba diving in tropical regions" query. We can see that BM25 suggests some of the top 5 products that are not related to the query at all such as Fog Free Shower/Travel Safety Mirror and Scunci No Slip Grip The Evolution Gel Ponytail Holders. However, we can see from the top 5 products suggested by semantic search that they are all related to sunscreen and words related to tropical regions such as reef, SPF, Caribbean, etc.

-   Are there cases where **semantic search fails**?

    One of the examples is from "makeup to cover up pimples" query. We can see that semantic search incorrectly retrieves related but irrelevant items such as acne patches and tools instead of makeup products for coverage. On the other hand, BM25 method actually returns makeup concealer which is the correct product to be suggested. This shows that the semantic search fails since it fails to distinguish products used to treat acne from cosmetic products used to cover pimples.

<!-- -->

-   Are the top results actually useful for the user’s intent?

    The top results are actually useful for the user's intent. We can see that either BM25 or semantic search can retrieve products related to the queries.

-   How does performance vary across query types (keyword vs semantic vs complex)?

    In the Easy (Keyword-based) group, we can see that the performance between BM25 and semantic search is pretty similar. BM25 search could retrieve products with exact keywords while semantic search could capture meaning of the query and suggest products with similar meanings.

    In the **medium (semantic-based) queries**, semantic search tends to outperform BM25. These queries do not have exact keywords, so BM25 might struggle a bit if keywords do not overlap whereas semantic search can capture the underlying intent and retrieve relevant products

    In the **complex queries**, both methods show limitations. BM25 often retrieves irrelevant results due to partial keyword matches or no matches, while semantic search captures general meaning but might not be able to fully satisfy all the conditions specified in the queries. For example, both methods still have room for improvement for "good cleanser for busy working professionals who do not have time" query. While the semantic search could recommend some cleansers, it fails to retrieve products targeted to actual working professionals and simply suggests cleansers for general people.

-   What are the strengths and weaknesses of each method?

    -   BM25

        -   Strengths

            -   It can match exact keywords which is useful when we want products with specific keywords such as SPF30 for sunscreen or serial numbers of products

            -   It is useful for products with specific names from certain brands. For example, "fit me concealer" which is a product from Maybelline can be accurately retrieved from BM25 search.

        -   Weaknesses

            -   It cannot fully understand the meaning or intent beyond keywords

            -   It may retrieve irrelevant products just because keywords overlap but they could be unrelated at all

            -   It often returns duplicate chunks from the same product (the same product with different reviews)

    -   Semantic search

        -   Strengths

            -   It can capture semantic meaning and work well with queries which might not have exact keywords.

            -   It is more robust when exact keywords are not present.

            -   It works well for queries which are more descriptive

        -   Weaknesses

            -   It struggles with exact products or brand matching

            -   It may retrieve semantically related but incorrect items

            -   It does not fully satisfy all the conditions in the queries

-   What types of queries are challenging for both methods?

    Both methods still struggle with queries which have multiple conditions such as "good cleanser for busy working professionals who do not have time". BM25 method struggles since there are only few exact keywords that it can match and retrieve relevant products while semantic search struggles because it can only retrieve products which have the most similar semantic meaning but not necessarily the ones which satisfy all the conditions.

-   Where might more advanced methods (e.g., RAG or reranking) help?

    More advanced methods such as RAG or reranking could help when we want to prioritize results that satisfy multiple conditions and when the queries are more complex. They would combine retrieval with reasoning and interpret users' intent more thoroughly instead of focusing on a certain condition. Also, hybrid approaches (BM25 and semantic search) could also be implemented to combine the strengths of both methods.
