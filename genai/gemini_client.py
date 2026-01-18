import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def get_gemini_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GEMINI_API_KEY not found. Check your .env file."
        )

    genai.configure(api_key=api_key)

    return genai.GenerativeModel(
        model_name="gemini-flash-lite-latest"
    )
