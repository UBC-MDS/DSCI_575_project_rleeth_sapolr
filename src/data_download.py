import requests
from pathlib import Path

def download_data(category: str):
    review_url = f"https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/{category}.jsonl.gz"
    metadata_url = f"https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/meta_categories/meta_{category}.jsonl.gz"
    review_output_path = Path(f"../data/raw/{category}.jsonl.gz")
    metadata_output_path = Path(f"../data/raw/meta_{category}.jsonl.gz")

    # create raw folder if it doesn't exist
    review_output_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_output_path.parent.mkdir(parents=True, exist_ok=True)

    review_response = requests.get(review_url, stream=True)
    metadata_response = requests.get(metadata_url, stream=True)
    with open(metadata_output_path, "wb") as f:
        for chunk in metadata_response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    with open(review_output_path, "wb") as f:
        for chunk in review_response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
