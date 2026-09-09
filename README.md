# SmartResume Generator: Customized Resumes for Every Opportunity

An AI-powered resume generator built with **Streamlit** and the **Google Gemini API**. Given a name and job title, it generates a complete, well-structured, professional resume in seconds.

**Live Demo:** https://smartresume-generator-bz7u425zashauhbcxdsjby.streamlit.app/

## How It Works

1. Enter your **Name** and **Job Title**.
2. Click **Generate Resume**.
3. Gemini generates a complete resume — Professional Summary, Experience, Projects, Skills, and Education — formatted in Markdown and displayed instantly.

## Tech Stack

- **Language:** Python 3.11
- **Framework:** Streamlit
- **AI Model:** Google Gemini (`gemini-3.6-flash`), via the official `google-genai` SDK
- **Secrets Management:** `python-dotenv` locally, Streamlit Secrets in production

## Project Structure
smartresume-generator/
├── app.py # Streamlit app entry point
├── requirements.txt
├── src/
│ ├── config.py # Loads Gemini API key from environment
│ └── gemini_client.py # Reusable Gemini API client wrapper


## Running Locally


git clone https://github.com/manasagottipalli/smartresume-generator.git
cd smartresume-generator
python -m venv .venv
.venv\Scripts\activate        # On Windows
pip install -r requirements.txt


Create a `.env` file in the project root:
GEMINI_API_KEY=your_api_key_here


Then run:

streamlit run app.py


## Security

The Gemini API key is never hardcoded. It's loaded from a local `.env` file (excluded from version control) or from Streamlit's built-in Secrets manager when deployed.

## About

This project was built as part of a Generative AI virtual internship, demonstrating practical prompt engineering and secure API integration with a deployed, publicly accessible web application.