def format_result(result):
    doc, score = result
    
    metadata = getattr(doc, "metadata", {})
    page_content = getattr(doc, "page_content", "")

    return {
        "title": metadata.get("product_title", "N/A"),
        "asin": metadata.get("asin", "N/A"),
        "score": float(score)
    }

def results_to_html(results):
    lines = []
    for i, r in enumerate(results, 1):
        title = r["title"][:90] + "..." if len(r["title"]) > 90 else r["title"]
        lines.append(f"{i}. {title}<br><small>ASIN: {r['asin']} | Score: {r['score']:.3f}</small>")
    return "<br><br>".join(lines)