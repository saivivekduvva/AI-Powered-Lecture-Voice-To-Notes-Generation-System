from models.summarization_model import load_summarizer
from preprocessing.segment_text import segment_text
import re

# Load summarizer once (CPU-based model assumed)
summarizer = load_summarizer()


def generate_study_materials(transcript: str) -> dict:
    transcript = transcript.strip()

    if not transcript:
        return {
            "topic": "No content detected",
            "text_notes": "",
            "smart_summary": "",
            "flashcards": []
        }

    # =========================
    # 1️⃣ TOPIC (CLEAR & SHORT)
    # =========================
    topic_input = transcript[:700]

    topic_result = summarizer(
        topic_input,
        max_length=18,
        min_length=6,
        do_sample=False
    )

    topic = topic_result[0]["summary_text"].strip().rstrip(".")

    # =========================
    # 2️⃣ TEXT NOTES (CLEAN BULLETS)
    # =========================
    sentences = re.split(r'(?<=[.!?])\s+', transcript)
    text_notes = "\n".join(f"• {s.strip()}" for s in sentences if len(s.split()) > 5)

    # =========================
    # 3️⃣ SMART SUMMARY (DEDUPLICATED)
    # =========================
    summary_segments = segment_text(transcript, max_words=220)
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

        # Avoid repetition
        key = summary[:60]
        if key not in seen:
            seen.add(key)
            summary_chunks.append(summary)

    smart_summary = " ".join(summary_chunks)

    # =========================
    # 4️⃣ SEMANTIC FLASHCARDS
    # =========================
    flashcards = []
    summary_sentences = re.split(r'(?<=[.!?])\s+', smart_summary)

    for s in summary_sentences:
        if len(flashcards) >= 5:
            break

        words = s.split()
        if len(words) < 10:
            continue

        lower_s = s.lower()

        if " because " in lower_s:
            flashcards.append({
                "Q": "Why does this happen?",
                "A": s
            })

        elif any(k in lower_s for k in ["used for", "helps", "allows", "enables"]):
            flashcards.append({
                "Q": "What is the purpose discussed here?",
                "A": s
            })

        elif any(k in lower_s for k in ["difference", "compare", "versus"]):
            flashcards.append({
                "Q": "What comparison is explained?",
                "A": s
            })

        elif any(k in lower_s for k in ["important", "key", "critical", "main"]):
            flashcards.append({
                "Q": "Why is this concept important?",
                "A": s
            })

    # Fallback flashcard
    if not flashcards and smart_summary:
        flashcards.append({
            "Q": "What is the core idea of this lecture?",
            "A": smart_summary
        })

    return {
        "topic": topic,
        "text_notes": text_notes,
        "smart_summary": smart_summary,
        "flashcards": flashcards
    }
