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
- No markdown
- No backticks

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

def generate_quiz(notes: str) -> list:
    model = get_gemini_model()

    try:
        response = model.generate_content(
            QUIZ_PROMPT.format(notes=notes)
        )
        raw = response.text.strip()

        # 🧹 Remove markdown/code fences if Gemini adds them
        raw = re.sub(r"```json|```", "", raw).strip()

        # 🔎 Extract first JSON array safely
        match = re.search(r"\[\s*{.*?}\s*\]", raw, re.S)
        if not match:
            return []

        json_text = match.group()
        data = json.loads(json_text)

        if not isinstance(data, list):
            return []

        # ✅ Validate questions
        valid_questions = []
        for q in data:
            if not isinstance(q, dict):
                continue

            if "question" not in q or "answer" not in q:
                continue

            # MCQ validation
            if q.get("type") == "MCQ":
                if "options" not in q or not isinstance(q["options"], list):
                    continue
                if len(q["options"]) < 2:
                    continue

            valid_questions.append(q)

        return valid_questions

    except Exception:
        # 🔒 UI-safe fallback
        return []
