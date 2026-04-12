from __future__ import annotations

import gzip
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REVIEWS_PATH = ROOT / "data" / "raw" / "All_Beauty.jsonl"
META_PATH = ROOT / "data" / "raw" / "meta_All_Beauty.jsonl"
OUTPUT_PATH = ROOT / "data" / "processed" / "sample_documents.jsonl.gz"

SAMPLE_SIZE = 10000
RANDOM_SEED = 42


def load_jsonl(path: Path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main():
    reviews = load_jsonl(REVIEWS_PATH)
    meta = load_jsonl(META_PATH)

    meta_by_parent_asin = {
        item.get("parent_asin"): item
        for item in meta
        if item.get("parent_asin") is not None
    }

    filtered = []
    for review in reviews:
        parent_asin = review.get("parent_asin")
        review_text = (review.get("text") or "").strip()

        if not parent_asin or not review_text:
            continue
        if parent_asin not in meta_by_parent_asin:
            continue

        product_metadata = meta_by_parent_asin[parent_asin]

        filtered.append(
            {
                "asin": parent_asin,
                "product_review": review_text,
                "product_title": product_metadata.get("title", "Unknown product"),
                "product_rating": review.get("rating", "N/A"),
            }
        )

    random.seed(RANDOM_SEED)

    if len(filtered) > SAMPLE_SIZE:
        sampled = random.sample(filtered, SAMPLE_SIZE)
    else:
        sampled = filtered

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with gzip.open(OUTPUT_PATH, "wt", encoding="utf-8") as f:
        for row in sampled:
            f.write(json.dumps(row) + "\n")

    size_mb = OUTPUT_PATH.stat().st_size / (1024 * 1024)
    print(f"Saved {len(sampled)} rows to {OUTPUT_PATH}")
    print(f"File size: {size_mb:.2f} MB")


if __name__ == "__main__":
    main()