import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

# Read the Gemini API key from the environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# The Gemini model we're using across the whole project (verified in Step 7)
GEMINI_MODEL = "gemini-3.6-flash"

# Fail early with a clear message if the key is missing, instead of a confusing error later
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Make sure you created a .env file "
        "with GEMINI_API_KEY=your_key_here"
    )