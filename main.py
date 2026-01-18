from pathlib import Path

from services.speech_to_text import speech_to_text
from preprocessing.clean_text import clean_transcript
from services.note_generator import generate_study_materials

from genai.flashcard_generator import generate_flashcards
from genai.quiz_generator import generate_quiz

from utils.file_io import save_text, save_json
from utils.logger import get_logger

logger = get_logger()

AUDIO_PATH = "data/raw_audio/sample_lecture.wav"

# Ensure output directories exist
Path("data/transcripts").mkdir(parents=True, exist_ok=True)
Path("data/processed_text").mkdir(parents=True, exist_ok=True)
Path("data/outputs").mkdir(parents=True, exist_ok=True)


def main():
    logger.info("Starting Lecture Voice-to-Notes Generator")

    # ---------------- Speech to Text ----------------
    logger.info("Running Speech-to-Text")
    transcript = speech_to_text(AUDIO_PATH)
    save_text("data/transcripts/sample_lecture.txt", transcript)

    # ---------------- Cleaning ----------------
    logger.info("Cleaning transcript")
    cleaned_text = clean_transcript(transcript)
    save_text("data/processed_text/sample_lecture_cleaned.txt", cleaned_text)

    # ---------------- Notes Generation ----------------
    logger.info("Generating notes and summaries")
    notes_data = generate_study_materials(cleaned_text)

    save_text("data/outputs/topic.txt", notes_data["topic"])
    save_text("data/outputs/text_notes.txt", notes_data["text_notes"])
    save_text("data/outputs/smart_summary.txt", notes_data["smart_summary"])

    # ---------------- GenAI Flashcards ----------------
    logger.info("Generating GenAI flashcards")
    flashcards = generate_flashcards(notes_data["text_notes"])

    if isinstance(flashcards, list):
        save_json("data/outputs/flashcards.json", flashcards)
    else:
        logger.warning("Flashcards generation returned invalid format")
        save_text("data/outputs/flashcards_error.txt", str(flashcards))

    # ---------------- GenAI Quiz (SAFE & ISOLATED) ----------------
    logger.info("Generating GenAI quiz")

    quiz = None
    try:
        quiz = generate_quiz(notes_data["text_notes"])
        if isinstance(quiz, list):
            save_json("data/outputs/quiz.json", quiz)
        else:
            logger.warning("Quiz returned non-JSON output")
            save_text("data/outputs/quiz_raw_output.txt", str(quiz))
    except Exception as e:
        logger.error(f"Quiz generation failed: {e}")
        save_text("data/outputs/quiz_error.txt", str(e))

    logger.info("Project executed successfully")


if __name__ == "__main__":
    main()
