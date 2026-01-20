import streamlit as st
import sys
import os
from pathlib import Path
import tempfile

# ---------------- PATH FIX ----------------
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# ---------------- IMPORTS ----------------
from services.speech_to_text import speech_to_text
from preprocessing.clean_text import clean_transcript
from services.note_generator import generate_study_materials
from genai.flashcard_generator import generate_flashcards
from genai.quiz_generator import generate_quiz

# ---------------- SESSION GUARD ----------------
st.session_state.setdefault("processed", False)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Lecture Intelligence",
    page_icon="🎙️",
    layout="wide"
)

# ---------------- PROFESSIONAL THEME ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #1e293b;
}

.main .block-container {
    padding-top: 3rem;
    padding-bottom: 5rem;
    max-width: 1000px;
}

.content-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 32px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    margin-bottom: 24px;
}

.section-header {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 1rem;
}

.muted-text {
    color: #64748b;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("User Guide")
    st.markdown("""
    **Core Capabilities**
    - Speech to Text
    - Structured Notes
    - Smart Summary
    - Flashcards
    - Knowledge Quiz

    **How to Use**
    1. Upload lecture audio
    2. Wait for processing
    3. Review generated outputs
    """)

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center; font-weight:800;'>Lecture Intelligence System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;' class='muted-text'>AI-Powered Lecture Analysis</p>", unsafe_allow_html=True)

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Lecture Audio (.wav / .mp3)",
    type=["wav", "mp3"]
)

# ---------------- MAIN PROCESS ----------------
if uploaded_file:

    if st.session_state.processed:
        st.stop()

    try:
        # Save temp audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_file.read())
            temp_audio_path = tmp.name

        with st.status("Processing Lecture...", expanded=True):

            st.write("🔊 Transcribing audio...")
            transcript = speech_to_text(temp_audio_path)

            st.write("🧹 Cleaning transcript...")
            cleaned_text = clean_transcript(transcript)

            st.write("📝 Generating notes...")
            notes = generate_study_materials(cleaned_text)

            # ---------------- FLASHCARDS ----------------
            st.write("🃏 Generating flashcards...")
            try:
                flashcards = generate_flashcards(notes.get("text_notes", ""))
                if not isinstance(flashcards, list):
                    flashcards = []
            except Exception:
                flashcards = []

            # ---------------- QUIZ ----------------
            st.write("🧠 Generating quiz...")
            try:
                quiz = generate_quiz(notes.get("text_notes", ""))
                if not isinstance(quiz, list):
                    quiz = []
            except Exception:
                quiz = []

        st.session_state.processed = True

        # ---------------- TABS ----------------
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Topic",
            "Notes",
            "Summary",
            "Flashcards",
            "Quiz"
        ])

        with tab1:
            st.markdown("<div class='content-card'>", unsafe_allow_html=True)
            st.markdown("### Core Topic")
            st.write(notes.get("topic", "N/A"))
            st.markdown("</div>", unsafe_allow_html=True)

        with tab2:
            st.markdown("<div class='content-card'>", unsafe_allow_html=True)
            st.markdown("### Detailed Notes")
            st.write(notes.get("text_notes", ""))
            st.markdown("</div>", unsafe_allow_html=True)

        with tab3:
            st.markdown("<div class='content-card'>", unsafe_allow_html=True)
            st.markdown("### Smart Summary")
            st.write(notes.get("smart_summary", ""))
            st.markdown("</div>", unsafe_allow_html=True)

        with tab4:
            if flashcards:
                for i, card in enumerate(flashcards, 1):
                    with st.expander(f"Flashcard {i}: {card.get('concept', 'General')}"):
                        st.markdown(f"**Q:** {card.get('question', '')}")
                        st.divider()
                        st.markdown(f"**A:** {card.get('answer', '')}")
            else:
                st.info("Flashcards could not be generated.")

        with tab5:
            if quiz:
                for i, q in enumerate(quiz, 1):
                    with st.expander(f"Question {i}"):
                        st.markdown(f"**{q.get('question', '')}**")
                        if q.get("type") == "MCQ":
                            for opt in q.get("options", []):
                                st.write(f"• {opt}")
                        st.markdown(f"**Answer:** {q.get('answer', '')}")
            else:
                st.info("Quiz could not be generated.")

    except Exception as e:
        st.error(f"Processing failed: {e}")

    finally:
        if "temp_audio_path" in locals() and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
