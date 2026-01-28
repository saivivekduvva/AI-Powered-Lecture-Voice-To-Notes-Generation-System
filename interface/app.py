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
    page_title="Lecture Intelligence",
    page_icon="🎙️",
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
    --accent: #6366f1;
    --border: rgba(0, 0, 0, 0.05);
    --profile-shadow: rgba(99, 102, 241, 0.1);
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg-main: #0b0e14;
        --bg-sidebar: #11141b;
        --bg-card: #161b22;
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        --accent: #7c3aed;
        --border: rgba(255, 255, 255, 0.08);
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

/* Profile Card Styling (Reference Match) */
.profile-card {
    background: var(--bg-card);
    border-radius: 20px;
    padding: 24px;
    text-align: center;
    border: 1px solid var(--border);
    margin-bottom: 30px;
    transition: transform 0.3s ease;
}

.avatar-circle {
    width: 80px;
    height: 80px;
    background: var(--bg-main);
    border-radius: 50%;
    margin: 0 auto 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 3px solid #10b981;
    box-shadow: 0 0 15px var(--profile-shadow);
}

.status-pill {
    background: rgba(16, 185, 129, 0.1);
    color: #10b981;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}

/* Title Gradient */
.main-title {
    font-size: 3.2rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(135deg, #6366f1, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Nav Buttons */
div.stButton > button {
    background-color: var(--bg-card) !important;
    color: var(--text-main) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    height: 48px;
    transition: 0.2s;
}

.active-nav button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
}

/* Content Area */
.content-area {
    background: var(--bg-card);
    border-radius: 24px;
    padding: 35px;
    border: 1px solid var(--border);
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

/* Reset Button Sidebar */
.reset-btn button {
    background: #ef4444 !important;
    color: white !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("""
        <div style="display:flex; align-items:center; margin-bottom:20px;">
            <div style="width:20px; height:20px; background:linear-gradient(45deg, #6366f1, #ec4899); border-radius:4px; margin-right:10px;"></div>
            <span style="font-weight:800; font-size:1.1rem;">Lecture Intelligence</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Profile Card
    st.markdown(f"""
    <div class="profile-card">
        <div class="avatar-circle"><span style="font-size:40px;">👤</span></div>
        <div style="font-weight:700; font-size:1.1rem;">System Administrator</div>
        <span class="status-pill">● Session Active</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    if st.button("🗑️ Reset Workspace", use_container_width=True):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- MAIN UI ----------------
st.markdown("<h1 class='main-title'>Lecture Intelligence</h1>", unsafe_allow_html=True)

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

    # ---------------- DASHBOARD ----------------
    data = st.session_state.data
    st.markdown(f"<h3 style='text-align:center; margin-top:30px;'>📖 {data['notes'].get('topic','Module Overview')}</h3>", unsafe_allow_html=True)
    
    nav_cols = st.columns(3)
    views = [("Notes", "📄"), ("Summary", "💡"), ("Flashcards", "🃏")]
    
    for i, (v_name, icon) in enumerate(views):
        with nav_cols[i]:
            is_active = "active-nav" if st.session_state.view == v_name else ""
            st.markdown(f"<div class='{is_active}'>", unsafe_allow_html=True)
            if st.button(f"{icon} {v_name}", key=f"nav_{v_name}", use_container_width=True):
                st.session_state.view = v_name
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # Content Display
    st.markdown("<div class='content-area'>", unsafe_allow_html=True)
    if st.session_state.view == "Notes":
        st.markdown("### 📝 Detailed Study Notes")
        st.write(data["notes"].get("text_notes", ""))
    elif st.session_state.view == "Summary":
        st.markdown("### ⚡ Smart Summary")
        st.write(data["notes"].get("smart_summary", ""))
    elif st.session_state.view == "Flashcards":
        st.markdown("### 🃏 Flashcards")
        for card in data.get("flashcards", []):
            with st.expander(f"🔹 {card.get('concept','Concept')}"):
                st.write(f"**Q:** {card.get('question','')}")
                st.write(f"**A:** {card.get('answer','')}")
    st.markdown("</div>", unsafe_allow_html=True)