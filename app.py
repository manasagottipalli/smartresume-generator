import streamlit as st
from src.jd_analyzer import analyze_job_description
from src.matcher import calculate_match
from src.resume_tailor import tailor_resume

st.set_page_config(page_title="SmartResume Generator", page_icon="📄")

st.title("📄 SmartResume Generator")
st.write("Customized resumes for every opportunity.")

# --- Step 1: Resume input ---
st.header("Step 1: Enter Your Resume")

st.write(
    "Paste your current resume content below. Include everything you'd "
    "normally put on a resume — summary, skills, experience, education, projects."
)

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

def update_resume_text():
    st.session_state.resume_text = st.session_state.resume_input

st.text_area(
    "Your Resume Content",
    height=300,
    placeholder="Example:\n\nJohn Doe\nSummary: ...\nSkills: Python, SQL...\nExperience: ...\nEducation: ...",
    key="resume_input",
    on_change=update_resume_text,
)

resume_text = st.session_state.resume_text

if resume_text.strip():
    st.success(f"Resume content saved ({len(resume_text)} characters).")
else:
    st.info("Waiting for resume content...")

# --- Step 2: Job Description input ---
st.header("Step 2: Enter the Job Description")

st.write(
    "Paste the full job description you're applying for. Include the "
    "responsibilities, required skills, and qualifications if listed."
)

if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""

def update_jd_text():
    st.session_state.jd_text = st.session_state.jd_input

st.text_area(
    "Job Description",
    height=300,
    placeholder="Example:\n\nWe are looking for a Software Engineer with experience in Python, SQL...",
    key="jd_input",
    on_change=update_jd_text,
)

jd_text = st.session_state.jd_text

if jd_text.strip():
    st.success(f"Job description saved ({len(jd_text)} characters).")
else:
    st.info("Waiting for job description...")

# --- Step 3: Analyze button ---
st.header("Step 3: Analyze")

if "jd_analysis" not in st.session_state:
    st.session_state.jd_analysis = None

if "match_result" not in st.session_state:
    st.session_state.match_result = None

if st.button("Analyze Resume"):
    if not resume_text.strip():
        st.warning("Please enter your resume content before analyzing.")
    elif not jd_text.strip():
        st.warning("Please enter the job description before analyzing.")
    else:
        with st.spinner("Analyzing job description with Gemini..."):
            try:
                st.session_state.jd_analysis = analyze_job_description(jd_text)
                st.session_state.match_result = calculate_match(resume_text, st.session_state.jd_analysis)
            except Exception as e:
                st.session_state.jd_analysis = None
                st.session_state.match_result = None
                st.error(f"Something went wrong during analysis: {e}")

# --- Step 4: Show analysis results ---
if st.session_state.jd_analysis:
    st.success("Analysis complete!")

    analysis = st.session_state.jd_analysis

    st.subheader("Required Skills")
    st.write(", ".join(analysis["required_skills"]) if analysis["required_skills"] else "None found.")

    st.subheader("Responsibilities")
    for item in analysis["responsibilities"]:
        st.write(f"- {item}")

    st.subheader("Qualifications")
    for item in analysis["qualifications"]:
        st.write(f"- {item}")

    st.subheader("Keywords")
    st.write(", ".join(analysis["keywords"]) if analysis["keywords"] else "None found.")

# --- Step 5: Show match score results ---
if st.session_state.match_result:
    st.subheader("Match Score")
    match = st.session_state.match_result

    st.metric(label="Resume–JD Match Score", value=f"{match['match_score']}%")
    st.caption(
        "⚠️ This is an app-generated estimate based on keyword overlap, "
        "NOT an official ATS score. Different companies use different ATS "
        "systems with their own scoring logic."
    )

    st.write("**Matched Keywords:**")
    st.write(", ".join(match["matched_keywords"]) if match["matched_keywords"] else "None matched.")

    st.write("**Missing Keywords:**")
    st.write(", ".join(match["missing_keywords"]) if match["missing_keywords"] else "None missing — great coverage!")

# --- Step 6: Generate tailored resume ---
if "tailored_resume" not in st.session_state:
    st.session_state.tailored_resume = None

if st.session_state.jd_analysis:
    st.header("Step 4: Generate Tailored Resume")

    st.caption(
        "The AI will reword and reorganize your existing resume content to better "
        "match this job — using only information you provided. It will never invent "
        "companies, dates, skills, or achievements you didn't mention."
    )

    if st.button("Generate Tailored Resume"):
        with st.spinner("Tailoring your resume with Gemini..."):
            try:
                st.session_state.tailored_resume = tailor_resume(resume_text, st.session_state.jd_analysis)
            except Exception as e:
                st.session_state.tailored_resume = None
                st.error(f"Something went wrong during tailoring: {e}")

# --- Step 7: Display tailored resume ---
if st.session_state.tailored_resume:
    st.success("Tailored resume generated!")

    tailored = st.session_state.tailored_resume

    st.subheader("Professional Summary")
    st.write(tailored["summary"])

    st.subheader("Skills")
    st.write(", ".join(tailored["skills"]) if tailored["skills"] else "None listed.")

    st.subheader("Experience")
    if tailored["experience"]:
        for job in tailored["experience"]:
            st.markdown(f"**{job['title']}** — {job['company']} ({job['duration']})")
            for bullet in job["bullets"]:
                st.write(f"- {bullet}")
    else:
        st.write("No experience listed.")

    st.subheader("Education")
    if tailored["education"]:
        for edu in tailored["education"]:
            st.markdown(f"**{edu['degree']}** — {edu['institution']} ({edu['duration']})")
    else:
        st.write("No education listed.")

    st.subheader("Projects")
    if tailored["projects"]:
        for project in tailored["projects"]:
            st.markdown(f"**{project['name']}**")
            st.write(project["description"])
            if project.get("technologies"):
                st.write("Technologies: " + ", ".join(project["technologies"]))
    else:
        st.write("No projects listed.")