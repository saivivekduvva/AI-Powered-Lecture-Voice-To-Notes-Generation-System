import os
import sys
import tempfile
from pathlib import Path

# ---------------- PATH FIX ----------------
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# ---------------- IMPORTS ----------------
from services.speech_to_text import speech_to_text
from preprocessing.clean_text import clean_transcript
from services.note_generator import generate_study_materials
from genai.flashcard_generator import generate_flashcards
from utils.file_io import save_text, save_json
from utils.logger import get_logger

# ---------------- LOGGER ----------------
logger = get_logger()

# ---------------- CONFIG ----------------
# Default audio path for local testing
AUDIO_PATH = "data/raw_audio/sample_lecture.wav"

TRANSCRIPT_DIR = Path("data/transcripts")
PROCESSED_DIR = Path("data/processed_text")
OUTPUT_DIR = Path("data/outputs")

# Ensure output directories exist
for folder in [TRANSCRIPT_DIR, PROCESSED_DIR, OUTPUT_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

def main():
    logger.info("🚀 Starting Lecture Intelligence Asset Synthesizer")

    # 1. SPEECH TO TEXT
    try:
        if not Path(AUDIO_PATH).exists():
            logger.error(f"Audio file not found at {AUDIO_PATH}")
            return

        logger.info("🎙️ Running Speech-to-Text")
        transcript = speech_to_text(AUDIO_PATH)

        if not transcript or not isinstance(transcript, str):
            raise ValueError("Empty or invalid transcript generated")

        save_text(TRANSCRIPT_DIR / "sample_lecture.txt", transcript)

    except Exception as e:
        logger.error(f"Speech-to-Text failed: {e}")
        return 

    # 2. TRANSCRIPT CLEANING
    try:
        logger.info("🧹 Cleaning transcript for AI processing")
        cleaned_text = clean_transcript(transcript)

        if not cleaned_text:
            raise ValueError("Cleaned transcript is empty")

        save_text(PROCESSED_DIR / "sample_lecture_cleaned.txt", cleaned_text)

    except Exception as e:
        logger.error(f"Transcript cleaning failed: {e}")
        return

    # 3. STUDY MATERIALS (Notes & Summary)
    try:
        logger.info("📝 Generating study notes and smart summary")
        notes_data = generate_study_materials(cleaned_text)

        if not isinstance(notes_data, dict):
            raise ValueError("Notes generator returned invalid format")

        # Save individual assets
        save_text(OUTPUT_DIR / "topic.txt", notes_data.get("topic", "Untitled Lecture"))
        save_text(OUTPUT_DIR / "text_notes.txt", notes_data.get("text_notes", ""))
        save_text(OUTPUT_DIR / "smart_summary.txt", notes_data.get("smart_summary", ""))
        
        logger.info(f"Generated assets for topic: {notes_data.get('topic')}")

    except Exception as e:
        logger.error(f"Notes generation failed: {e}")
        return

    # 4. FLASHCARDS
    logger.info("🃏 Synthesizing study flashcards")
    try:
        flashcards = generate_flashcards(notes_data.get("text_notes", ""))

        if isinstance(flashcards, list) and flashcards:
            save_json(OUTPUT_DIR / "flashcards.json", flashcards)
            logger.info(f"Successfully generated {len(flashcards)} flashcards")
        else:
            logger.warning("Flashcards generation returned empty data")
            save_text(OUTPUT_DIR / "flashcards_error.txt", "No flashcards generated.")

    except Exception as e:
        logger.error(f"Flashcards generation failed: {e}")
        save_text(OUTPUT_DIR / "flashcards_error.txt", str(e))

    logger.info("✅ All lecture assets synthesized successfully")

if __name__ == "__main__":
    main()