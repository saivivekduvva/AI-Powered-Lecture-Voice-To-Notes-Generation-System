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
try:
    from services.speech_to_text import speech_to_text
    from preprocessing.clean_text import clean_transcript
    from services.note_generator import generate_study_materials
    from genai.flashcard_generator import generate_flashcards
except ImportError:
    pass 

# ---------------- SESSION STATE ----------------
if "processed" not in st.session_state:
    st.session_state.processed = False
if "view" not in st.session_state:
    st.session_state.view = "Notes"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Lecture Intelligence",
    page_icon="🎙️",
    layout="wide"
)

# ---------------- THEME VARIABLES ----------------
if st.session_state.dark_mode:
    BG = "#0b0e14"       
    FG = "#f8fafc"       
    CARD = "#161b22"     
    ACCENT = "#7c3aed"   
    BORDER = "rgba(255, 255, 255, 0.1)"
else:
    BG = "#f8fafc"
    FG = "#0f172a"
    CARD = "#ffffff"
    ACCENT = "#6366f1"
    BORDER = "rgba(0, 0, 0, 0.05)"

# ---------------- UI STYLING ----------------
st.markdown(f"""
<style>
/* ---------- GLOBAL ---------- */
.stApp {{
    background-color: {BG};
    color: {FG};
    font-family: 'Inter', system-ui, sans-serif;
}}

/* ---------- CENTER FIX ---------- */
.block-container {{
    max-width: 1100px !important;
    margin: auto !important;
    padding-top: 1.2rem !important;
}}

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {{
    background: {BG} !important;
    border-right: 1px solid {BORDER};
}}

.sidebar-box {{
    background: {CARD};
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
    border: 1px solid {BORDER};
}}

/* ---------- TITLE ---------- */
.main-title {{
    font-size: 3.2rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(135deg, #818cf8, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
}}

/* ---------- FILE UPLOAD ---------- */
[data-testid="stFileUploader"] {{
    background-color: {CARD} !important;
    padding: 30px !important;
    border-radius: 20px !important;
    border: 2px dashed {ACCENT} !important;
    transition: 0.3s ease;
}}

/* ---------- NAVIGATION ROW ALIGNMENT ---------- */
.nav-container {{
    max-width: 600px;
    margin: 40px auto 10px auto; /* Centers the navigation bar */
}}

/* Force Streamlit buttons in the nav to align */
div.stButton > button {{
    width: 100% !important;
    height: 45px !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    background-color: {CARD} !important;
    color: {FG} !important;
    border: 1px solid {BORDER} !important;
    margin-bottom: 0px !important; /* Removes staggered heights */
    transition: all 0.2s ease;
}}

.active-tab button {{
    background-color: {ACCENT} !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 20px {ACCENT}88 !important;
    transform: translateY(-2px);
}}

/* ---------- CONTENT CARD ---------- */
.content-card {{
    background: {CARD};
    border-radius: 24px;
    padding: 40px;
    max-width: 900px;
    margin: 20px auto;
    border: 1px solid {BORDER};
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
}}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 📘 Lecture Intelligence")
    st.markdown(f'<div class="sidebar-box">🎧 Upload audio<br>🧠 AI processing<br>📚 Study assets</div>', unsafe_allow_html=True)
    st.toggle("🌙 Dark Mode", key="dark_mode")
    st.divider()
    if st.button("🗑️ Reset Workspace", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# ---------------- HEADER ----------------
st.markdown("<h1 class='main-title'>Lecture Intelligence</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; opacity:0.7; color:{FG};'>Advanced Transcription & Study Asset Synthesizer</p>", unsafe_allow_html=True)

# ---------------- FILE UPLOAD ----------------
_, mid, _ = st.columns([1, 2, 1])
with mid:
    uploaded_file = st.file_uploader("", type=["wav", "mp3"])

# ---------------- PROCESSING ----------------
if uploaded_file:
    if not st.session_state.processed:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_file.read())
            audio_path = tmp.name
        
        with st.status("💎 Processing...", expanded=True):
            try:
                transcript = speech_to_text(audio_path)
                cleaned = clean_transcript(transcript)
                notes = generate_study_materials(cleaned)
                flashcards = generate_flashcards(notes.get("text_notes", ""))
                st.session_state.data = {"notes": notes, "flashcards": flashcards}
                st.session_state.processed = True
                os.remove(audio_path)
            except Exception as e:
                st.error(f"Error: {e}")
        st.rerun()

    # ---------------- ALIGNED NAVIGATION ----------------
    data = st.session_state.data
    st.markdown(f"<h3 style='text-align:center; margin-top:30px;'>📖 {data['notes'].get('topic','Overview')}</h3>", unsafe_allow_html=True)
    
    # Wrapped in a container for centered alignment
    st.markdown("<div class='nav-container'>", unsafe_allow_html=True)
    nav_cols = st.columns(3)
    
    views = [("Notes", "📄"), ("Summary", "💡"), ("Flashcards", "🃏")]
    
    for i, (v_name, icon) in enumerate(views):
        with nav_cols[i]:
            is_active = "active-tab" if st.session_state.view == v_name else ""
            st.markdown(f"<div class='{is_active}'>", unsafe_allow_html=True)
            if st.button(f"{icon} {v_name}", key=f"nav_{v_name}", use_container_width=True):
                st.session_state.view = v_name
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- CONTENT DISPLAY ----------------
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    if st.session_state.view == "Notes":
        st.markdown("### 📝 Detailed Study Notes")
        st.write(data["notes"].get("text_notes", ""))
    elif st.session_state.view == "Summary":
        st.markdown("### ⚡ Smart Summary")
        st.write(data["notes"].get("smart_summary", ""))
    elif st.session_state.view == "Flashcards":
        for card in data.get("flashcards", []):
            with st.expander(f"🔹 {card.get('concept','Concept')}"):
                st.write(f"**Q:** {card.get('question','')}")
                st.write(f"**A:** {card.get('answer','')}")
    st.markdown("</div>", unsafe_allow_html=True)