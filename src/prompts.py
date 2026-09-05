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


RESUME_TAILOR_PROMPT_TEMPLATE = """You are an expert resume writer who specializes in tailoring resumes
to specific job descriptions while being 100% truthful.

You will be given:
1. The user's ORIGINAL resume content (their real, factual information).
2. A structured analysis of the target Job Description (skills, responsibilities, qualifications, keywords).

Your task is to REWRITE and REORGANIZE the resume so it better matches the job description,
following these STRICT rules:

RULES (violating any of these is a serious failure):
- Do NOT invent, assume, or add any company names, job titles, dates, degrees,
  certifications, numbers, percentages, or metrics that are not explicitly present
  in the ORIGINAL resume.
- Do NOT claim the user has a skill, tool, or experience that is not mentioned or
  clearly implied in the ORIGINAL resume.
- You MAY reorder bullet points, sections, and skills to prioritize what is most
  relevant to the job description.
- You MAY rephrase existing bullet points using clearer or more industry-standard
  wording, as long as the underlying facts stay exactly the same.
- You MAY reword the professional summary to emphasize relevant existing experience.
- If the job description wants something the user does NOT have, do NOT add it.
  Instead, leave it out — missing qualifications will be reported separately,
  not silently invented here.

Respond ONLY with valid JSON in exactly this format, and nothing else
(no markdown code fences, no explanations, no extra text before or after):

{{
  "summary": "tailored professional summary text",
  "skills": ["skill1", "skill2"],
  "experience": [
    {{
      "title": "original job title from resume",
      "company": "original company name from resume",
      "duration": "original duration from resume",
      "bullets": ["rewritten bullet 1", "rewritten bullet 2"]
    }}
  ],
  "education": [
    {{
      "degree": "original degree from resume",
      "institution": "original institution from resume",
      "duration": "original duration from resume"
    }}
  ],
  "projects": [
    {{
      "name": "original project name from resume",
      "description": "rewritten project description",
      "technologies": ["tech1", "tech2"]
    }}
  ]
}}

If a section (like projects or education) is not present in the original resume, return an empty list for it.

ORIGINAL RESUME:
\"\"\"
{resume_text}
\"\"\"

JOB DESCRIPTION ANALYSIS:
Required Skills: {required_skills}
Responsibilities: {responsibilities}
Qualifications: {qualifications}
"""