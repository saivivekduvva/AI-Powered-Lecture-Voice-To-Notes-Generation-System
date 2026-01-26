import json
from genai.gemini_client import get_gemini_model

def generate_topic(text: str) -> str:
    model = get_gemini_model()
    prompt = f"""
You are an academic assistant.

Generate a SHORT, CLEAR lecture topic/title
based on the content below.

Rules:
- 5 to 8 words max
- NO sentences
- NO punctuation
- Capitalize Properly
- Abstract the main idea

Examples:
❌ Linear algebra deals with vectors...
✅ Fundamentals of Linear Algebra

CONTENT:
{text}
"""

    response = model.generate_content(prompt)
    return response.text.strip()
