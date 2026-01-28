🎙️ Voice to Notes System

An AI-powered Lecture Voice-to-Notes Generator that converts spoken lectures into clean text, structured notes, summaries, flashcards, and quizzes.
Built to help students focus on listening instead of writing during lectures.

Features :-

🎧 Speech-to-Text Conversion from lecture audio
🧹 Text Cleaning & Preprocessing
📝 Structured Study Notes Generation
✨ Smart Summaries
🃏 AI-Generated Flashcards

VOICE TO NOTES SYSTEM
│
├── configs/                     # Configuration files
│
├── data/
│   ├── raw_audio/               # Input lecture audio (.wav)
│   ├── transcripts/             # Speech-to-text output
│   ├── processed_text/          # Cleaned & processed text
│   └── outputs/                 # Generated notes, summaries, quizzes
│
├── genai/
│   ├── gemini_client.py         # Gemini API client
│   ├── flashcard_generator.py   # GenAI flashcards
│   ├── topic_generator.py       # Topic extraction
│
├── interface/
│   └── app.py                   # Streamlit UI
│
├── models/
│   └── summarization_model.py   # Summarization logic
│
├── preprocessing/
│   ├── clean_text.py            # Text cleaning
│   └── segment_text.py          # Text segmentation
│
├── services/
│   ├── speech_to_text.py        # Audio → Text
│   └── note_generator.py        # Notes generation
│
├── utils/                       # Helper utilities
│
├── tests/                       # Unit tests
│
├── main.py                      # Main pipeline runner
├── requirements.txt             # Dependencies
├── README.md                    # Project documentation
└── .env                         # API keys (not committed)

⚙️ Tech Stack :-

Python 3.9+
Google Speech-to-Text / Whisper
Google Gemini API (GenAI)
Streamlit
NLTK / Regex
JSON
PyTest


🔑 Environment Setup :-
1️⃣ Clone the Repository
git clone https://github.com/your-username/voice-to-notes-system.git
cd voice-to-notes-system

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Setup Environment Variables

Create a .env file:
GEMINI_API_KEY=your_api_key_here

▶️ How to Run
🔹 Run Full Pipeline
python main.py
🔹 Run Web Interface
streamlit run interface/app.py

🧠 Workflow :-

Upload or provide lecture audio
Convert audio → text
Clean & preprocess transcript

Generate:
Study Notes
Smart Summary
Flashcards
Quiz Questions
Display results via Streamlit UI

📌 Use Cases
University lecture note generation
Online course content summarization
Exam preparation
Self-study automation
Accessibility support for learners

🚧 Future Enhancements :-

📹 Video lecture support
🌍 Multilingual transcription
☁️ Cloud deployment
📱 Mobile-friendly UI
🧩 Export to PDF / Notion

👨‍💻 Author :-

Sai Vivek Duvva
AI & Python Developer
IBM SkillsBuild Internship Project

⭐ Support
If you like this project, give it a ⭐ on GitHub!
Feel free to fork, improve, and contribute.
