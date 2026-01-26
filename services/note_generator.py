import re
from genai.topic_generator import generate_topic
from models.summarization_model import load_summarizer
from preprocessing.segment_text import segment_text

# Load summarizer once (CPU-based) to ensure it stays in memory
summarizer = load_summarizer()

def generate_notes(text: str) -> str:
    """
    Generate clean bullet-point notes from transcript using regex 
    to extract meaningful sentences.
    """
    # Split text into sentences based on punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Filter for sentences that have more than 6 words to avoid fragments
    notes = [
        f"• {s.strip()}"
        for s in sentences
        if len(s.split()) > 6
    ]
    
    return "\n".join(notes)


def generate_summary(text: str) -> str:
    """
    Generate a smart, deduplicated summary by segmenting text 
    and running it through the summarization model.
    """
    # Break long text into manageable chunks for the model
    summary_segments = segment_text(text, max_words=220)
    summary_chunks = []
    seen = set()

    for seg in summary_segments:
        # Skip segments that are too short to summarize effectively
        if len(seg.split()) < 40:
            continue

        result = summarizer(
            seg,
            max_length=85,
            min_length=40,
            do_sample=False
        )

        summary = result[0]["summary_text"].strip()
        
        # Simple deduplication: check first 60 characters
        key = summary[:60]
        if key not in seen:
            seen.add(key)
            summary_chunks.append(summary)

    return " ".join(summary_chunks)


def generate_study_materials(cleaned_text: str) -> dict:
    """
    Main orchestrator that returns a dictionary containing 
    the Topic, Detailed Notes, and Smart Summary.
    """
    cleaned_text = cleaned_text.strip()

    if not cleaned_text:
        return {
            "topic": "No content detected",
            "text_notes": "No notes could be generated.",
            "smart_summary": "No summary available."
        }

    # 1. Generate Topic Heading (using GenAI)
    topic = generate_topic(cleaned_text)

    # 2. Generate Detailed Bullet Points (CPU-based Regex)
    notes = generate_notes(cleaned_text)

    # 3. Generate Smart Summary (CPU-based Model)
    summary = generate_summary(cleaned_text)

    return {
        "topic": topic,
        "text_notes": notes,
        "smart_summary": summary
    }
