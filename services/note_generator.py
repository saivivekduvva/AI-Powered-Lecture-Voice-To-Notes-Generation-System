from genai.topic_generator import generate_topic
from models.summarization_model import load_summarizer
from preprocessing.segment_text import segment_text
import re

# Load summarizer once (CPU-based)
summarizer = load_summarizer()


def generate_notes(text: str) -> str:
    """
    Generate clean bullet-point notes from transcript
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    notes = [
        f"• {s.strip()}"
        for s in sentences
        if len(s.split()) > 6
    ]
    return "\n".join(notes)


def generate_summary(text: str) -> str:
    """
    Generate smart, deduplicated summary
    """
    summary_segments = segment_text(text, max_words=220)
    summary_chunks = []
    seen = set()

    for seg in summary_segments:
        if len(seg.split()) < 40:
            continue

        result = summarizer(
            seg,
            max_length=85,
            min_length=40,
            do_sample=False
        )

        summary = result[0]["summary_text"].strip()
        key = summary[:60]

        if key not in seen:
            seen.add(key)
            summary_chunks.append(summary)

    return " ".join(summary_chunks)


def generate_study_materials(cleaned_text: str) -> dict:
    cleaned_text = cleaned_text.strip()

    if not cleaned_text:
        return {
            "topic": "No content detected",
            "text_notes": "",
            "smart_summary": ""
        }

    # =========================
    # 1️⃣ TOPIC (GenAI)
    # =========================
    topic = generate_topic(cleaned_text)

    # =========================
    # 2️⃣ NOTES (CPU)
    # =========================
    notes = generate_notes(cleaned_text)

    # =========================
    # 3️⃣ SUMMARY (CPU)
    # =========================
    summary = generate_summary(cleaned_text)

    return {
        "topic": topic,
        "text_notes": notes,
        "smart_summary": summary
    }
