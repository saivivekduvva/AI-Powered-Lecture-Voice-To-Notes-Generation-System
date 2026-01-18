import json
import re
from genai.gemini_client import get_gemini_model

FLASHCARD_PROMPT = """
You are a student-friendly revision assistant.

Generate EXACTLY 5 SIMPLE flashcards from the lecture notes below.

RULES:
- Questions must be SHORT and DIRECT
- Avoid "why" and "how"
- Answers must be ONE LINE
- Use easy, exam-friendly language
- Output ONLY valid JSON

FORMAT:
[
  {{
    "question": "Short question",
    "answer": "One line answer",
    "concept": "Keyword"
  }}
]

Lecture Notes:
{notes}
"""

def generate_flashcards(notes: str):
    model = get_gemini_model()

    response = model.generate_content(
        FLASHCARD_PROMPT.format(notes=notes)
    )

    raw = response.text.strip()

    try:
        json_text = re.search(r"\[.*\]", raw, re.S).group()
        data = json.loads(json_text)

        # Validate structure
        valid_cards = []
        for c in data:
            if isinstance(c, dict) and "question" in c and "answer" in c:
                valid_cards.append(c)

        return valid_cards

    except Exception:
        return []
