🎙️ Lecture Voice-to-Notes Generator
AI-Powered Lecture Transcription, Smart Summaries & Semantic Flashcards

An AI-based system that converts lecture audio into accurate text notes, generates smart summaries, and creates semantic flashcards to improve student learning and revision efficiency.

This project is built specifically for students, educators, and self-learners who want to transform long lectures into structured, exam-ready study material.

🚀 Features

🎧 Lecture Audio Transcription

Converts lecture audio (.wav, .mp3) into clean, readable text

Powered by GPU-accelerated Whisper (faster-whisper)

📝 Notes Generation

Produces verbatim lecture notes

Maintains topic flow and explanations

🧠 Smart Summary

AI-generated summaries in simple student-friendly language

Highlights key concepts and important points

🧩 Semantic Flashcards

Concept-based flashcards for active recall

Designed for quick revision and exam preparation

⚡ GPU Optimized

Uses CUDA-enabled NVIDIA GPUs

Significantly faster than CPU-based transcription

🌐 Web Interface

Built with Streamlit

Simple, clean, and beginner-friendly UI


Lecture-Voice-to-Notes-Generator/
│
├── app.py                     # Streamlit application
├── transcription/
│   └── whisper_model.py       # Faster-Whisper GPU transcription
│
├── note_generator/
│   ├── notes.py               # Raw notes generation
│   ├── summary.py             # Smart summary generation
│   └── flashcards.py          # Semantic flashcard generator
│
├── utils/
│   └── file_handler.py        # File upload & processing utilities
│
├── requirements.txt
├── .gitignore
└── README.md


🛠️ Tech Stack

Python 3.10

Streamlit

faster-whisper

PyTorch

Sentence Transformers

CUDA (for GPU acceleration)

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/Lecture-Voice-to-Notes-Generator.git
cd Lecture-Voice-to-Notes-Generator

2️⃣ Create Virtual Environment (Python 3.10 Recommended)
python -m venv venv


Activate:

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

🎮 GPU Configuration (Optional but Recommended)

Make sure:

NVIDIA GPU is installed

CUDA is properly set up

PyTorch supports CUDA

Check GPU availability:

python -c "import torch; print(torch.cuda.is_available())"

▶️ Run the Application
streamlit run app.py


Then open the URL shown in your browser.

📌 How It Works

Upload a lecture audio file

Audio is transcribed using Whisper

Raw notes are generated from transcription

AI creates:

Smart Summary

Semantic Flashcards

Output is displayed in an easy-to-read format

🎯 Use Cases

College & University Students

Online Course Learners

Educators creating study materials

Exam & revision preparation

Productivity & note automation

📈 Future Improvements

Topic-wise timestamps

PDF / DOC export

Multilingual lecture support

Highlighting important exam questions

Cloud deployment

🤝 Contributing

Contributions are welcome!

Fork the repository

Create a new branch

Make your changes

Submit a pull request

📄 License

This project is licensed under the MIT License.

⭐ Acknowledgements

OpenAI & Whisper Community

Hugging Face

Streamlit Team