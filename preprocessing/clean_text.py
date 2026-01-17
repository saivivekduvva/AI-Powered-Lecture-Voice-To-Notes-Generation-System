import re

def clean_transcript(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\b(uh|um|hmm|you know)\b", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
