import json
import re
from genai.gemini_client import get_gemini_model

QUIZ_PROMPT = """
You are a university examiner.

Generate EXACTLY 5 quiz questions from the notes below.

RULES:
- Mix MCQ and short answer
- Questions must be clear and exam-oriented
- Avoid vague wording
- Output ONLY valid JSON
- NO explanations or extra text

FORMAT:
[
  {
    "type": "MCQ",
    "question": "Question text",
    "options": ["A", "B", "C", "D"],
    "answer": "B",
    "concept": "Concept name"
  }
]

Lecture Notes:
{notes}
"""

def generate_quiz(notes: str):
    model = get_gemini_model()
    response = model.generate_content(QUIZ_PROMPT.format(notes=notes))
    raw = response.text.strip()

    try:
        # 🔹 Extract JSON array safely
        json_text = re.search(r"\[.*\]", raw, re.S).group()
        data = json.loads(json_text)

        # 🔹 Validate structure
        valid_questions = []
        for q in data:
            if not isinstance(q, dict):
                continue
            if "question" not in q or "answer" not in q:
                continue
            valid_questions.append(q)

        return valid_questions

    except Exception:
        # 🔒 ALWAYS return list
        return []
