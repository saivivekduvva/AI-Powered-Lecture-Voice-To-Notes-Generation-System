from pathlib import Path

from services.speech_to_text import speech_to_text
from preprocessing.clean_text import clean_transcript
from services.note_generator import generate_study_materials

from genai.flashcard_generator import generate_flashcards
from genai.quiz_generator import generate_quiz

from utils.file_io import save_text, save_json
from utils.logger import get_logger

# ---------------- LOGGER ----------------
logger = get_logger()

# ---------------- CONFIG ----------------
AUDIO_PATH = "data/raw_audio/sample_lecture.wav"

TRANSCRIPT_DIR = Path("data/transcripts")
PROCESSED_DIR = Path("data/processed_text")
OUTPUT_DIR = Path("data/outputs")

# Ensure output directories exist
TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    logger.info("🚀 Starting Lecture Voice-to-Notes Generator")

    # ---------------- SPEECH TO TEXT ----------------
    try:
        logger.info("🎙️ Running Speech-to-Text")
        transcript = speech_to_text(AUDIO_PATH)

        if not transcript or not isinstance(transcript, str):
            raise ValueError("Empty or invalid transcript")

        save_text(TRANSCRIPT_DIR / "sample_lecture.txt", transcript)

    except Exception as e:
        logger.error(f"Speech-to-Text failed: {e}")
        return  # ❌ Cannot proceed without transcript

    # ---------------- CLEANING ----------------
    try:
        logger.info("🧹 Cleaning transcript")
        cleaned_text = clean_transcript(transcript)

        if not cleaned_text:
            raise ValueError("Cleaned transcript is empty")

        save_text(PROCESSED_DIR / "sample_lecture_cleaned.txt", cleaned_text)

    except Exception as e:
        logger.error(f"Transcript cleaning failed: {e}")
        return

    # ---------------- NOTES GENERATION ----------------
    try:
        logger.info("📝 Generating notes and summaries")
        notes_data = generate_study_materials(cleaned_text)

        if not isinstance(notes_data, dict):
            raise ValueError("Notes generator returned invalid format")

        save_text(OUTPUT_DIR / "topic.txt", notes_data.get("topic", ""))
        save_text(OUTPUT_DIR / "text_notes.txt", notes_data.get("text_notes", ""))
        save_text(OUTPUT_DIR / "smart_summary.txt", notes_data.get("smart_summary", ""))

    except Exception as e:
        logger.error(f"Notes generation failed: {e}")
        return

    # ---------------- FLASHCARDS (SAFE) ----------------
    logger.info("🃏 Generating GenAI flashcards")
    try:
        flashcards = generate_flashcards(notes_data.get("text_notes", ""))

        if isinstance(flashcards, list) and flashcards:
            save_json(OUTPUT_DIR / "flashcards.json", flashcards)
            logger.info("Flashcards generated successfully")
        else:
            logger.warning("Flashcards generation returned empty or invalid data")
            save_text(OUTPUT_DIR / "flashcards_error.txt", str(flashcards))

    except Exception as e:
        logger.error(f"Flashcards generation failed: {e}")
        save_text(OUTPUT_DIR / "flashcards_error.txt", str(e))

    # ---------------- QUIZ (ULTRA SAFE & ISOLATED) ----------------
    logger.info("🧠 Generating GenAI quiz")
    try:
        quiz = generate_quiz(notes_data.get("text_notes", ""))

        if isinstance(quiz, list) and quiz:
            save_json(OUTPUT_DIR / "quiz.json", quiz)
            logger.info("Quiz generated successfully")
        else:
            logger.warning("Quiz generation returned empty or invalid data")
            save_text(OUTPUT_DIR / "quiz_error.txt", str(quiz))

    except Exception as e:
        logger.error(f"Quiz generation failed: {e}")
        save_text(OUTPUT_DIR / "quiz_error.txt", str(e))

    logger.info("✅ Project executed successfully")


if __name__ == "__main__":
    main()
