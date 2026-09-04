import streamlit as st

st.set_page_config(page_title="SmartResume Generator", page_icon="📄")

st.title("📄 SmartResume Generator")
st.write("Customized resumes for every opportunity.")

st.header("Step 1: Enter Your Resume")

st.write(
    "Paste your current resume content below. Include everything you'd "
    "normally put on a resume — summary, skills, experience, education, projects."
)

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

def update_resume_text():
    # This runs automatically whenever the text area's value changes and commits
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