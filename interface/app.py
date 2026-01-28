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

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Lecture Lens",
    page_icon="🔍",
    layout="wide"
)

# ---------------- DYNAMIC UI STYLING ----------------
st.markdown("""
<style>
/* 1. DEFINE DYNAMIC VARIABLES */
:root {
    --bg-main: #f8fafc;
    --bg-sidebar: #f1f5f9;
    --bg-card: #ffffff;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --accent: #4f46e5;
    --border: rgba(0, 0, 0, 0.08);
    --profile-shadow: rgba(0, 0, 0, 0.05);
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg-main: #0f1117;
        --bg-sidebar: #161922;
        --bg-card: #1d212b;
        --text-main: #f1f5f9;
        --text-muted: #94a3b8;
        --accent: #818cf8;
        --border: rgba(255, 255, 255, 0.1);
        --profile-shadow: rgba(16, 185, 129, 0.2);
    }
}

/* 2. APPLY VARIABLES */
.stApp {
    background-color: var(--bg-main);
    color: var(--text-main);
}

[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border);
}

/* Profile Card Styling */
.profile-card {
    background: var(--bg-card);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    border: 1px solid var(--border);
    margin-bottom: 25px;
}

.avatar-circle {
    width: 70px;
    height: 70px;
    background: var(--bg-main);
    border-radius: 50%;
    margin: 0 auto 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid #10b981;
    box-shadow: 0 0 15px var(--profile-shadow);
}

.status-text {
    color: #10b981;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Project Name Styling */
.project-branding {
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--text-main);
}

.main-title {
    font-size: 3.5rem;
    font-weight: 900;
    text-align: center;
    letter-spacing: -0.04em;
    background: linear-gradient(to bottom right, var(--text-main), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

/* Nav Buttons */
div.stButton > button {
    background-color: var(--bg-card) !important;
    color: var(--text-muted) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    height: 44px;
    transition: all 0.2s ease;
}

.active-nav button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2) !important;
}

/* Content Area */
.content-area {
    background: var(--bg-card);
    border-radius: 20px;
    padding: 40px;
    border: 1px solid var(--border);
}

/* Reset Button Sidebar */
.reset-btn-container button {
    background: transparent !important;
    color: var(--text-muted) !important;
    border: 1px solid var(--border) !important;
    margin-top: 20px;
}
.reset-btn-container button:hover {
    color: #ef4444 !important;
    border-color: #ef4444 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("""
        <div style="display:flex; align-items:center; margin-bottom:25px; padding-left:5px;">
            <div style="width:18px; height:18px; background:var(--accent); border-radius:4px; margin-right:12px;"></div>
            <span class="project-branding">Lecture Lens</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Profile Card
    st.markdown(f"""
    <div class="profile-card">
        <div class="avatar-circle"><span style="font-size:32px;">👤</span></div>
        <div style="font-weight:700; font-size:1rem; color:var(--text-main);">Admin Node</div>
        <div class="status-text">Active Session</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown('<div class="reset-btn-container">', unsafe_allow_html=True)
    if st.button("Clear Workspace", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- MAIN UI ----------------
st.markdown("<h1 class='main-title'>Lecture Lens</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:var(--text-muted); margin-bottom:40px;'>Neural Transcription & Knowledge Synthesis</p>", unsafe_allow_html=True)

_, mid, _ = st.columns([1, 2, 1])
with mid:
    uploaded_file = st.file_uploader("", type=["wav", "mp3"], label_visibility="collapsed")

# ---------------- PROCESSING ----------------
if uploaded_file:
    if not st.session_state.processed:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(uploaded_file.read())
            audio_path = tmp.name
        
        with st.status("Analyzing Audio Sequence...", expanded=True):
            try:
                transcript = speech_to_text(audio_path)
                cleaned = clean_transcript(transcript)
                notes = generate_study_materials(cleaned)
                flashcards = generate_flashcards(notes.get("text_notes", ""))
                st.session_state.data = {"notes": notes, "flashcards": flashcards}
                st.session_state.processed = True
                os.remove(audio_path)
            except Exception as e:
                st.error(f"Analysis Failed: {e}")
        st.rerun()

    # ---------------- DASHBOARD ----------------
    data = st.session_state.data
    st.markdown(f"<h3 style='text-align:center; margin-top:30px; letter-spacing:-0.02em;'>{data['notes'].get('topic','Content Analysis')}</h3>", unsafe_allow_html=True)
    
    nav_cols = st.columns(3)
    views = ["Notes", "Summary", "Flashcards"]
    st.divider()
    
    for i, v_name in enumerate(views):
        with nav_cols[i]:
            is_active = "active-nav" if st.session_state.view == v_name else ""
            st.markdown(f"<div class='{is_active}'>", unsafe_allow_html=True)
            if st.button(v_name, key=f"nav_{v_name}", use_container_width=True):
                st.session_state.view = v_name
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # Content Display
    st.markdown("<div class='content-area'>", unsafe_allow_html=True)
    if st.session_state.view == "Notes":
        st.markdown("### Comprehensive Notes")
        st.write(data["notes"].get("text_notes", ""))
    elif st.session_state.view == "Summary":
        st.markdown("### Core Insights")
        st.write(data["notes"].get("smart_summary", ""))
    elif st.session_state.view == "Flashcards":
        st.markdown("### Review Deck")
        for card in data.get("flashcards", []):
            with st.expander(card.get('concept','Key Concept')):
                st.write(f"**Question:** {card.get('question','')}")
                st.write(f"**Answer:** {card.get('answer','')}")
    st.markdown("</div>", unsafe_allow_html=True)