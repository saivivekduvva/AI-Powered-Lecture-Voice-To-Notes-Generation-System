import streamlit as st
import sys
import os
from pathlib import Path
import tempfile

# ---------------- PATH FIX ----------------
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# ---------------- IMPORTS ----------------
from services.speech_to_text import speech_to_text
from preprocessing.clean_text import clean_transcript
from services.note_generator import generate_study_materials

from genai.flashcard_generator import generate_flashcards
from genai.quiz_generator import generate_quiz

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Lecture Voice-to-Notes",
    page_icon="🎙",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    font-family: 'Segoe UI', sans-serif;
}

.glass {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 22px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    margin-bottom: 20px;
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    margin: 20px 0;
    color: #7dd3fc;
    border-left: 5px solid #7dd3fc;
    padding-left: 12px;
}

.small-text {
    color: #cfcfcf;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📘 User Guide")
st.sidebar.markdown("""
### What this does
Convert lecture audio into:
- 🧭 Topic
- 📝 Notes
- 📄 Smart summary
- 🧠 Flashcards (GenAI)
- 🧪 Quiz (GenAI)

---

### How to use
1. Upload **.wav / .mp3**
2. Wait for processing
3. Revise instantly

---

💡 Clear audio = better results
""")

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>🎙 Lecture Voice-to-Notes Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;' class='small-text'>AI-powered academic assistant using GenAI</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- UPLOAD ----------------
st.markdown("<div class='section-title'>📤 Upload Lecture Audio</div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload lecture audio",
    type=["wav", "mp3"],
    label_visibility="collapsed"
)

# ---------------- PROCESS ----------------
if uploaded_file:
    try:
        # Save temp audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_file.read())
            temp_audio_path = tmp.name

        # Speech to text
        with st.spinner("🔊 Transcribing audio..."):
            transcript = speech_to_text(temp_audio_path)

        # Clean text
        with st.spinner("🧹 Cleaning transcript..."):
            cleaned_text = clean_transcript(transcript)

        # Notes & summary
        with st.spinner("🧠 Generating notes & summary..."):
            notes = generate_study_materials(cleaned_text)

        # Flashcards (SAFE)
        with st.spinner("🧠 Generating GenAI flashcards..."):
            raw_flashcards = generate_flashcards(notes["text_notes"])

            if isinstance(raw_flashcards, list):
                flashcards = [
                    c for c in raw_flashcards
                    if isinstance(c, dict)
                    and "question" in c
                    and "answer" in c
                ]
            else:
                flashcards = []

        # Quiz (SAFE)
        quiz = []
        with st.spinner("🧪 Generating GenAI quiz..."):
            try:
                q = generate_quiz(notes["text_notes"])
                if isinstance(q, list):
                    quiz = q
            except Exception:
                quiz = []

        st.success("✅ Study materials generated successfully!")

        # ---------------- TABS ----------------
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🧭 Topic",
            "📝 Notes",
            "📄 Summary",
            "🧠 Flashcards",
            "🧪 Quiz (GenAI)"
        ])

        # ---------- TOPIC ----------
        with tab1:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            st.write(notes.get("topic", ""))
            st.markdown("</div>", unsafe_allow_html=True)

        # ---------- NOTES ----------
        with tab2:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            st.text(notes.get("text_notes", ""))
            st.markdown("</div>", unsafe_allow_html=True)

        # ---------- SUMMARY ----------
        with tab3:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            st.write(notes.get("smart_summary", ""))
            st.markdown("</div>", unsafe_allow_html=True)

        # ---------- FLASHCARDS ----------
        with tab4:
            if flashcards:
                for i, card in enumerate(flashcards, 1):
                    with st.expander(f"📌 Flashcard {i}"):
                        st.markdown(f"**❓ Question**: {card.get('question', '')}")
                        st.markdown(f"**✅ Answer**: {card.get('answer', '')}")

                        if card.get("concept"):
                            st.markdown(f"🧠 *Concept*: {card['concept']}")
            else:
                st.info("⚠️ Flashcards could not be generated for this lecture.")

        # ---------- QUIZ ----------
        with tab5:
            if quiz:
                for i, q in enumerate(quiz, 1):
                    with st.expander(f"🧪 Question {i}"):
                        st.markdown(f"**❓ {q.get('question', '')}**")

                        if q.get("type") == "MCQ":
                            for opt in q.get("options", []):
                                st.markdown(f"- {opt}")
                            st.markdown(f"✅ **Answer**: {q.get('answer', '')}")
                        else:
                            st.markdown(f"✍ **Answer**: {q.get('answer', '')}")

                        if q.get("concept"):
                            st.markdown(f"🧠 *Concept*: {q['concept']}")
            else:
                st.info("⚠️ Quiz could not be generated for this lecture.")

    except Exception as e:
        st.error(f"❌ Error: {e}")

    finally:
        if "temp_audio_path" in locals():
            os.remove(temp_audio_path)
