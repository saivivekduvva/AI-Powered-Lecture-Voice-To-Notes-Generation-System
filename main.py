from pathlib import Path

from services.speech_to_text import speech_to_text
from preprocessing.clean_text import clean_transcript
from services.note_generator import generate_study_materials
from services.quiz_generator import generate_quiz
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
    transcript = speech_to_text(AUDIO_PATH)
    save_text("data/transcripts/sample_lecture.txt", transcript)

    # ---------------- Cleaning ----------------
    cleaned_text = clean_transcript(transcript)
    save_text("data/processed_text/sample_lecture_cleaned.txt", cleaned_text)

    # ---------------- Notes & Quiz ----------------
    notes_data = generate_study_materials(cleaned_text)
    quiz = generate_quiz(cleaned_text)

    # ---------------- Save Outputs ----------------
    save_text("data/outputs/topic.txt", notes_data["topic"])
    save_text("data/outputs/text_notes.txt", notes_data["text_notes"])
    save_text("data/outputs/smart_summary.txt", notes_data["smart_summary"])
    save_json("data/outputs/flashcards.json", notes_data["flashcards"])
    save_text("data/outputs/quiz.txt", quiz)

    logger.info("Project executed successfully")


if __name__ == "__main__":
    main()
