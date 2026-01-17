def generate_quiz(text: str) -> str:
    """
    Generates a simple quiz based on the lecture text.
    CPU-only, rule-based implementation.
    """
    if not text or not text.strip():
        return "No quiz questions available."

    questions = [
        "1. Explain the main concept discussed in the lecture.",
        "2. What problem does the lecture aim to solve?",
        "3. Mention two important takeaways.",
        "4. How can this concept be applied in real life?"
    ]

    return "\n".join(questions)
