JD_ANALYSIS_PROMPT_TEMPLATE = """You are an expert technical recruiter and resume analyst.

Analyze the following Job Description and extract structured information from it.

Respond ONLY with valid JSON in exactly this format, and nothing else
(no markdown code fences, no explanations, no extra text before or after):

{{
  "required_skills": ["skill1", "skill2"],
  "responsibilities": ["responsibility1", "responsibility2"],
  "qualifications": ["qualification1", "qualification2"],
  "keywords": ["keyword1", "keyword2"]
}}

Rules:
- "required_skills": technical and soft skills explicitly or clearly implied in the JD.
- "responsibilities": the main duties/tasks mentioned in the JD.
- "qualifications": degree requirements, years of experience, certifications mentioned.
- "keywords": a flat list of important terms an ATS system or recruiter would scan for
  (can overlap with skills, but should also include tools, technologies, and role-specific terms).
- Do not invent information that is not present in the JD.
- If a category has no relevant information, return an empty list for it.

Job Description:
\"\"\"
{jd_text}
\"\"\"
"""