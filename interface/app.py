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
# REMOVED: quiz_generator import

# ---------------- SESSION STATE ----------------
if "processed" not in st.session_state:
    st.session_state.processed = False
if "view" not in st.session_state:
    st.session_state.view = "Notes"

# REMOVED: Quiz Specific State (quiz_index, quiz_score, quiz_complete)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Lecture Intelligence",
    page_icon="🎙️",
    layout="wide"
)

# ---------------- PROFESSIONAL UI STYLING ----------------
st.markdown("""
<style>
/* Pro Mesh Gradient Background */
.stApp {
    background-color: #f8fafc;
    background-image: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(244, 63, 94, 0.08) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
        radial-gradient(at 0% 100%, rgba(244, 63, 94, 0.08) 0px, transparent 50%);
    background-attachment: fixed;
}

/* Seamless Glassmorphic Sidebar */
[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.3) !important;
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(226, 232, 240, 0.8);
}

.sidebar-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 10px;
}

.content-card {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    padding: 35px;
    border: 1px solid rgba(255, 255, 255, 0.6);
    box-shadow: 0 10px 40px -10px rgba(0,0,0,0.04);
    margin-bottom: 25px;
    color: #1e293b;
}

div.stButton > button {
    width: 100%;
    border-radius: 100px !important;
    padding: 10px 15px !important;
    background-color: white !important;
    color: #4f46e5 !important;
    font-weight: 600 !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    transition: all 0.2s ease-in-out;
    white-space: nowrap !important;
}

div.stButton > button:hover {
    transform: translateY(-1px);
    border-color: #4f46e5 !important;
    background-color: #f5f3ff !important;
    box-shadow: 0 8px 15px -3px rgba(79, 70, 229, 0.15);
}

.main-title {
    font-size: 3.2rem;
    font-weight: 900;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, #1e293b 30%, #4f46e5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 5px;
}

[data-testid="stFileUploader"] {
    background: rgba(255, 255, 255, 0.6);
    padding: 15px;
    border-radius: 18px;
    border: 2px dashed #cbd5e1;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("<p class='sidebar-header'>📖 User Guide</p>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 0.85rem; color: #475569; line-height: 1.6;">
    1. <b>Upload</b> an MP3 or WAV lecture file.<br>
    2. <b>Process:</b> Wait as AI transcribes and analyzes.<br>
    3. <b>Review:</b> Toggle between Notes, Summary, and Cards.<br>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("<p class='sidebar-header'>⚙️ Usage Status</p>", unsafe_allow_html=True)
    status_color = "#10b981" if st.session_state.processed else "#64748b"
    status_text = "Analysis Ready" if st.session_state.processed else "Waiting for Audio"
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 8px;">
        <div style="width: 10px; height: 10px; border-radius: 50%; background: {status_color};"></div>
        <span style="font-size: 0.85rem; color: #475569;">{status_text}</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    
    if st.button("🗑️ Reset Workspace"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ---------------- HEADER ----------------
st.markdown("<h1 class='main-title'>Lecture Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color: #64748b; font-size: 1.05rem; margin-bottom: 2.5rem;'>Advanced Transcription & Study Asset Synthesizer</p>", unsafe_allow_html=True)

# ---------------- CENTERED FILE UPLOAD ----------------
up_col1, up_col2, up_col3 = st.columns([1, 1.8, 1])
with up_col2:
    uploaded_file = st.file_uploader(
        "Upload Audio",
        type=["wav", "mp3"],
        label_visibility="collapsed"
    )

# ---------------- PROCESSING LOGIC ----------------
if uploaded_file:
    if not st.session_state.processed:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(uploaded_file.read())
                temp_audio_path = tmp.name

            with st.status("💎 Synthesizing your lecture assets...", expanded=True) as status:
                st.write("🎙️ Processing Audio Stream...")
                transcript = speech_to_text(temp_audio_path)
                
                st.write("🧹 Refining Content...")
                cleaned_text = clean_transcript(transcript)
                
                st.write("📝 Building Structured Notes...")
                notes = generate_study_materials(cleaned_text)
                
                st.write("🃏 Designing Flashcards...")
                flashcards = generate_flashcards(notes.get("text_notes", ""))
                
                # REMOVED: generate_quiz step
                
                status.update(label="✨ Intelligence Assets Ready!", state="complete")

            st.session_state.data = {
                "notes": notes,
                "flashcards": flashcards
            }
            st.session_state.processed = True
            
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            st.rerun()

        except Exception as e:
            st.error(f"Processing Error: {e}")

    # ---------------- ALIGNED NAVIGATION ----------------
    if st.session_state.processed:
        data = st.session_state.data

        st.markdown(
            f"<div style='text-align:center; margin-top: 15px;'><h3>📖 {data['notes'].get('topic', 'Topic Overview')}</h3></div>",
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # Adjusted columns for 3 buttons instead of 4
        nav_cols = st.columns([2, 1, 1, 1, 2], gap="small")

        with nav_cols[1]:
            if st.button("📄 Notes"):
                st.session_state.view = "Notes"
        with nav_cols[2]:
            if st.button("💡 Summary"):
                st.session_state.view = "Summary"
        with nav_cols[3]:
            if st.button("🃏 Cards"):
                st.session_state.view = "Flashcards"

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------------- CONTENT DISPLAY ----------------
        display_col1, display_col2, display_col3 = st.columns([1, 6, 1])

        with display_col2:
            if st.session_state.view == "Notes":
                st.markdown("<div class='content-card'>", unsafe_allow_html=True)
                st.markdown("### 📝 Detailed Study Notes")
                st.write(data['notes'].get("text_notes", "Data unavailable."))
                st.markdown("</div>", unsafe_allow_html=True)

            elif st.session_state.view == "Summary":
                st.markdown("<div class='content-card'>", unsafe_allow_html=True)
                st.markdown("### ⚡ Smart Summary")
                st.write(data['notes'].get("smart_summary", "Data unavailable."))
                st.markdown("</div>", unsafe_allow_html=True)

            elif st.session_state.view == "Flashcards":
                f_cards = data.get('flashcards', [])
                if f_cards:
                    for i, card in enumerate(f_cards, 1):
                        with st.expander(f"🔹 {card.get('concept', 'Key Concept')}"):
                            st.markdown(f"**Q:** {card.get('question', '')}")
                            st.markdown("---")
                            st.markdown(f"**A:** {card.get('answer', '')}")
                else:
                    st.info("Insufficient content to generate flashcards.")