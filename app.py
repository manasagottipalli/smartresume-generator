import streamlit as st
from src.gemini_client import generate_text

st.set_page_config(page_title="Resume Generator", page_icon="📄")

st.title("Resume Generator")

name = st.text_input("Name")
job_title = st.text_input("Job Title")


def generate_resume(name: str, job_title: str) -> str:
    """
    Sends a prompt to Gemini asking it to generate a professional resume
    for the given name and job title, formatted in Markdown.
    """
    prompt = f"""Generate a professional, well-structured resume in Markdown format
for the following person:

Name: {name}
Job Title: {job_title}

Include these sections: Professional Summary, Experience, Projects, Skills, and Education.
Use realistic placeholder text (e.g. [Company Name], [Start Date], [Your Email Address])
where specific personal details are not provided, since none were given.
"""
    return generate_text(prompt)


def clean_resume_text(text: str) -> str:
    """
    Cleans up common placeholder formatting inconsistencies in the
    generated resume text, making placeholders clearer for the user.
    """
    replacements = {
        "[Add Email Address]": "[Your Email Address]",
        "[Add Phone Number]": "[Your Phone Number]",
        "[Add LinkedIn]": "[Your LinkedIn Profile]",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


if st.button("Generate Resume"):
    if name and job_title:
        with st.spinner("Generating your resume..."):
            resume = generate_resume(name, job_title)
            cleaned = clean_resume_text(resume)
        st.markdown(cleaned)
    else:
        st.warning("Please enter both Name and Job Title.")