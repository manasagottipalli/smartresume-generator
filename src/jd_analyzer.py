import json
from src.gemini_client import generate_text
from src.prompts import JD_ANALYSIS_PROMPT_TEMPLATE


def analyze_job_description(jd_text: str) -> dict:
    """
    Sends the job description to Gemini and returns a dictionary with:
    required_skills, responsibilities, qualifications, keywords.
    """
    prompt = JD_ANALYSIS_PROMPT_TEMPLATE.format(jd_text=jd_text)
    raw_response = generate_text(prompt)

    # Gemini sometimes wraps JSON in markdown code fences like ```json ... ```
    # even when asked not to — this removes them safely if present.
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError(
            "Gemini did not return valid JSON for JD analysis. "
            "Raw response was:\n" + raw_response
        )

    # Make sure all expected keys exist, even if Gemini skipped an empty one
    for key in ["required_skills", "responsibilities", "qualifications", "keywords"]:
        data.setdefault(key, [])

    return data