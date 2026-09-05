from google import genai
from src.config import GEMINI_API_KEY, GEMINI_MODEL

# Create one shared Gemini client using our API key from .env
_client = genai.Client(api_key=GEMINI_API_KEY)


def generate_text(prompt: str) -> str:
    """
    Sends a prompt to Gemini and returns the plain text reply.
    This is the single, reusable entry point every other module will use
    to talk to Gemini — keeping all API-calling logic in one place.
    """
    try:
        response = _client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        # We don't want the whole app to crash if Gemini has an issue —
        # instead, we return a clear error message the UI can display.
        raise RuntimeError(f"Gemini API call failed: {e}")