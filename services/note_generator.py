from models.summarization_model import load_summarizer
from preprocessing.segment_text import segment_text

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
    # 1️⃣ TOPIC (SHORT SUMMARY)
    # =========================
    topic_input = transcript[:600] if len(transcript) > 50 else transcript

    topic = summarizer(
        topic_input,
        max_length=20,
        min_length=8,
        do_sample=False
    )[0]["summary_text"]

    # =========================
    # 2️⃣ TEXT NOTES (FULL TRANSCRIPT)
    # =========================
    text_notes = "• " + transcript.replace(". ", ".\n• ")

    # =========================
    # 3️⃣ SMART SUMMARY
    # =========================
    summary_segments = segment_text(transcript, max_words=220)

    summary_chunks = []
    for seg in summary_segments:
        if len(seg.split()) < 30:
            continue

        result = summarizer(
            seg,
            max_length=90,
            min_length=45,
            do_sample=False
        )
        summary_chunks.append(result[0]["summary_text"])

    smart_summary = " ".join(summary_chunks).strip()

    # =========================
    # 4️⃣ FLASHCARDS
    # =========================
    flashcards = []
    sentences = smart_summary.split(". ")

    for s in sentences:
        if len(s.split()) < 8:
            continue

        lower_s = s.lower()

        if " is " in lower_s and len(flashcards) < 5:
            term = s.split(" is ")[0].strip()
            flashcards.append({
                "Q": f"What is {term}?",
                "A": s.strip()
            })

        elif any(word in lower_s for word in ["difference", "compare", "versus"]) and len(flashcards) < 5:
            flashcards.append({
                "Q": "What comparison is discussed?",
                "A": s.strip()
            })

    if not flashcards and smart_summary:
        flashcards.append({
            "Q": "Summarize the key idea of this lecture.",
            "A": smart_summary
        })

    return {
        "topic": topic,
        "text_notes": text_notes,
        "smart_summary": smart_summary,
        "flashcards": flashcards[:5]
    }
