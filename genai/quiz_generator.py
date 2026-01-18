import json
from genai.gemini_client import get_gemini_model

QUIZ_PROMPT = """
You are a university examiner.

Generate a quiz using ONLY the notes below.

Rules:
- Total 5 questions
- Mix MCQ, Short Answer, Conceptual
- Questions must be directly related to the notes
- Avoid vague or repeated questions

Output strictly in JSON:

[
  {{
    "type": "MCQ",
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "answer": "B",
    "concept": "..."
  }}
]

Lecture Notes:
{notes}
"""

def generate_quiz(notes: str):
    model = get_gemini_model()

    prompt = QUIZ_PROMPT.format(notes=notes)

    response = model.generate_content(prompt)

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by model",
            "raw_output": response.text
        }
