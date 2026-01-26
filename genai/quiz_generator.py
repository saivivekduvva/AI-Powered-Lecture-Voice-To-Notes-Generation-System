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
- No explanations
- No markdown
- No backticks

FORMAT:
[
  {
    "type": "MCQ",
    "question": "Question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option B",
    "concept": "Concept name"
  }
]

IMPORTANT:
Return ONLY the JSON array. Any text outside JSON will break the system.

Lecture Notes:
{notes}
"""

def generate_quiz(notes: str) -> dict:
    # ---------- GUARD ----------
    if not notes or len(notes.strip()) < 80:
        return {"status": "INSUFFICIENT_NOTES", "quiz": []}

    model = get_gemini_model()

    try:
        response = model.generate_content(
            QUIZ_PROMPT.format(notes=notes)
        )

        raw = response.text.strip()

        # ---------- CLEAN ----------
        raw = re.sub(r"```(?:json)?", "", raw).strip()

        # ---------- EXTRACT JSON ----------
        match = re.search(r"\[[\s\S]*\]", raw)
        if not match:
            return {"status": "JSON_NOT_FOUND", "quiz": []}

        json_text = match.group(0)

        try:
            data = json.loads(json_text)
        except json.JSONDecodeError:
            return {"status": "JSON_INVALID", "quiz": []}

        if not isinstance(data, list):
            return {"status": "JSON_NOT_LIST", "quiz": []}

        valid_questions = []

        for q in data:
            if not isinstance(q, dict):
                continue

            if "question" not in q or "answer" not in q:
                continue

            q_type = q.get("type", "SHORT").upper()
            q["type"] = "MCQ" if "MCQ" in q_type else "SHORT"

            if q["type"] == "MCQ":
                options = q.get("options", [])

                if not isinstance(options, list) or len(options) < 3:
                    continue

                # Normalize letter answers
                if q["answer"] in ["A", "B", "C", "D"]:
                    idx = ord(q["answer"]) - ord("A")
                    if idx < len(options):
                        q["answer"] = options[idx]

            valid_questions.append(q)

        # ---------- ENFORCE EXACTLY 5 ----------
        if len(valid_questions) < 5:
            return {"status": "INSUFFICIENT_VALID_QUESTIONS", "quiz": []}

        return {
            "status": "OK",
            "quiz": valid_questions[:5]
        }

    except Exception as e:
        print("Quiz generation error:", e)
        return {"status": "GENERATION_ERROR", "quiz": []}
