import json
from src.gemini_client import generate_text
from src.prompts import RESUME_TAILOR_PROMPT_TEMPLATE


def tailor_resume(resume_text: str, jd_analysis: dict) -> dict:
    prompt = RESUME_TAILOR_PROMPT_TEMPLATE.format(
        resume_text=resume_text,
        required_skills=jd_analysis.get("required_skills", []),
        responsibilities=jd_analysis.get("responsibilities", []),
        qualifications=jd_analysis.get("qualifications", []),
    )

    raw_response = generate_text(prompt)

    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError(
            "Gemini did not return valid JSON for resume tailoring. "
            "Raw response was:\n" + raw_response
        )

    data.setdefault("summary", "")
    data.setdefault("skills", [])
    data.setdefault("experience", [])
    data.setdefault("education", [])
    data.setdefault("projects", [])

    return data