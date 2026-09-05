import re


def _normalize(text: str) -> str:
    """
    Lowercases text and strips extra punctuation/spacing so comparisons
    aren't thrown off by case or minor formatting differences.
    Example: "React.js" and "react js" should be treated as similar.
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def calculate_match(resume_text: str, jd_analysis: dict) -> dict:
    """
    Compares the resume text against the JD's required_skills and keywords.
    Returns a dictionary with:
      - match_score: percentage (0-100)
      - matched_keywords: list of JD terms found in the resume
      - missing_keywords: list of JD terms NOT found in the resume
    """
    normalized_resume = _normalize(resume_text)

    # Combine skills + keywords into one deduplicated list to check against
    combined_terms = list(dict.fromkeys(
        jd_analysis.get("required_skills", []) + jd_analysis.get("keywords", [])
    ))

    matched_keywords = []
    missing_keywords = []

    for term in combined_terms:
        normalized_term = _normalize(term)
        if normalized_term and normalized_term in normalized_resume:
            matched_keywords.append(term)
        else:
            missing_keywords.append(term)

    total_terms = len(combined_terms)
    match_score = round((len(matched_keywords) / total_terms) * 100) if total_terms > 0 else 0

    return {
        "match_score": match_score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
    }