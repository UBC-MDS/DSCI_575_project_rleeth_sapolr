import requests
from pathlib import Path
import gzip
import shutil

def download_data(category: str):
    """
    Download and extract Amazon review and metadata files for a given category.
    This function retrieves compressed review and metadata files from the UCSD Amazon dataset, decompresses them on the fly, and saves them locally as JSONL files in the data/raw directory.
    Args:
        category (str): Product category name (e.g., "All_Beauty").
    Returns:
        None
    """
    review_url = f"https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/{category}.jsonl.gz"
    metadata_url = f"https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/meta_categories/meta_{category}.jsonl.gz"
    review_output_path = Path(f"../data/raw/{category}.jsonl")
    metadata_output_path = Path(f"../data/raw/meta_{category}.jsonl")

    # create raw folder if it doesn't exist
    review_output_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_output_path.parent.mkdir(parents=True, exist_ok=True)

    review_response = requests.get(review_url, stream=True)
    metadata_response = requests.get(metadata_url, stream=True)
   # decompress metadata while downloading
    with gzip.GzipFile(fileobj=metadata_response.raw) as gz:
        with open(metadata_output_path, "wb") as f:
            shutil.copyfileobj(gz, f)

    # decompress reviews while downloading
    with gzip.GzipFile(fileobj=review_response.raw) as gz:
        with open(review_output_path, "wb") as f:
            shutil.copyfileobj(gz, f)