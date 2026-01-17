import streamlit as st
import sys
import os
from pathlib import Path
import tempfile

# ---------------- PATH FIX ----------------
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from services.speech_to_text import speech_to_text
from preprocessing.clean_text import clean_transcript
from services.note_generator import generate_study_materials

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

.glass-box {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 30px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

.section-heading {
    font-size: 28px;
    font-weight: 700;
    margin: 30px 0 10px 0;
    color: #7dd3fc;
    border-left: 5px solid #7dd3fc;
    padding-left: 12px;
}

.subtext {
    font-size: 15px;
    color: #cfcfcf;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📘 User Guide")
st.sidebar.markdown("""
### 👋 Welcome!
This tool converts **lecture audio** into structured study material:

• 🧭 Topic detection  
• 📝 Full text notes  
• 📄 Smart summary  
• 🧠 Flashcards  

---
### 🛠 How to Use
1. Upload a **.wav / .mp3** lecture  
2. Wait for processing  
3. Start revising  

---
💡 Tip: Clear audio improves accuracy
""")

# ---------------- MAIN TITLE ----------------
st.markdown("<h1 style='text-align:center;'>🎙 Lecture Voice-to-Notes Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;' class='subtext'>AI-powered study assistant</p>", unsafe_allow_html=True)
st.markdown("---")

# ---------------- UPLOAD ----------------
st.markdown("<div class='section-heading'>📤 Upload Lecture Audio</div>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>Upload a .wav or .mp3 lecture recording</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=["wav", "mp3"],
    label_visibility="collapsed"
)

# ---------------- PROCESS ----------------
if uploaded_file:
    try:
        # Use safe temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_file.read())
            temp_audio_path = tmp.name

        with st.spinner("🔊 Transcribing lecture audio..."):
            transcript = speech_to_text(temp_audio_path)

        with st.spinner("🧹 Cleaning transcript..."):
            cleaned_text = clean_transcript(transcript)

        with st.spinner("🧠 Generating study materials..."):
            result = generate_study_materials(cleaned_text)

        st.success("✅ Study materials generated successfully!")

        # =========================
        # 🧭 TOPIC
        # =========================
        st.markdown("<div class='section-heading'>🧭 Topic</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.write(result["topic"])
            st.markdown("</div>", unsafe_allow_html=True)

        # =========================
        # 📝 TEXT NOTES
        # =========================
        st.markdown("<div class='section-heading'>📝 Text Notes (Full Lecture)</div>", unsafe_allow_html=True)
        st.markdown("<p class='subtext'>Complete audio-to-text conversion</p>", unsafe_allow_html=True)

        with st.container():
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.text(result["text_notes"])
            st.markdown("</div>", unsafe_allow_html=True)

        # =========================
        # 📄 SMART SUMMARY
        # =========================
        st.markdown("<div class='section-heading'>📄 Smart Summary</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
            st.write(result["smart_summary"])
            st.markdown("</div>", unsafe_allow_html=True)

        # =========================
        # 🧠 FLASHCARDS
        # =========================
        st.markdown("<div class='section-heading'>🧠 Flashcards</div>", unsafe_allow_html=True)

        if result["flashcards"]:
            for i, card in enumerate(result["flashcards"], start=1):
                with st.expander(f"📌 Flashcard {i}"):
                    st.markdown(f"**❓ Question:** {card['Q']}")
                    st.markdown(f"**✅ Answer:** {card['A']}")
        else:
            st.info("No flashcards generated.")

    except Exception as e:
        st.error(f"❌ Error occurred: {e}")

    finally:
        if "temp_audio_path" in locals():
            os.remove(temp_audio_path)
