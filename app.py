import streamlit as st
from src.jd_analyzer import analyze_job_description

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

if "ready_to_analyze" not in st.session_state:
    st.session_state.ready_to_analyze = False

if "jd_analysis" not in st.session_state:
    st.session_state.jd_analysis = None

if st.button("Analyze Resume"):
    if not resume_text.strip():
        st.warning("Please enter your resume content before analyzing.")
    elif not jd_text.strip():
        st.warning("Please enter the job description before analyzing.")
    else:
        st.session_state.ready_to_analyze = True
        with st.spinner("Analyzing job description with Gemini..."):
            try:
                st.session_state.jd_analysis = analyze_job_description(jd_text)
            except Exception as e:
                st.session_state.jd_analysis = None
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