def format_result(result):
    """
    Format a result tuple into a dictionary.
    Args:
        result (tuple[Document, float]): A tuple containing a Document and a score.
    Returns:
        dict: A dictionary containing the title, ASIN, and score.
    """
    doc, score = result
    
    metadata = getattr(doc, "metadata", {})
    page_content = getattr(doc, "page_content", "")

    return {
        "title": metadata.get("product_title", "N/A"),
        "asin": metadata.get("asin", "N/A"),
        "score": float(score)
    }

def results_to_html(results):
    """
    Convert a list of results to an HTML string.
    Args:
        results (list[dict]): A list of dictionaries containing the title, ASIN, and score.
    Returns:
        str: An HTML string containing the results.
    """
    lines = []
    for i, r in enumerate(results, 1):
        title = r["title"][:90] + "..." if len(r["title"]) > 90 else r["title"]
        lines.append(f"{i}. {title}<br><small>ASIN: {r['asin']} | Score: {r['score']:.3f}</small>")
    return "<br><br>".join(lines)