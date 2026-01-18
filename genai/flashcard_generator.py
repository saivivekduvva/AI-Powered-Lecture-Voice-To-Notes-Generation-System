import json
from genai.gemini_client import get_gemini_model

FLASHCARD_PROMPT = """
You are an AI tutor helping students revise lectures.

Generate EXACTLY 5 high-quality semantic flashcards
based ONLY on the lecture notes below.

Rules:
- Questions must test understanding, not memorization
- Avoid vague or generic questions
- Each flashcard must have a clear concept

Return ONLY valid JSON in this format:

[
  {{
    "question": "Clear conceptual question",
    "answer": "Concise but complete answer",
    "concept": "Core idea being tested"
  }}
]

Lecture Notes:
{notes}
"""

def generate_flashcards(notes: str):
    model = get_gemini_model()

    prompt = FLASHCARD_PROMPT.format(notes=notes)

    response = model.generate_content(prompt)

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by model",
            "raw_output": response.text
        }
