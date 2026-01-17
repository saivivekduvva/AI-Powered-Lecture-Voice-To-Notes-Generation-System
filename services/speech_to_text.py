from faster_whisper import WhisperModel
from pathlib import Path

# Load Whisper model in CPU-only mode
model = WhisperModel(
    "small",              # changed from "medium" → better for CPU
    device="cpu",
    compute_type="int8",  # optimized for CPU
    cpu_threads=4
)


def speech_to_text(audio_path: str) -> str:
    """
    Converts an audio file to text using a CPU-based Whisper model.
    """
    audio_path = str(Path(audio_path).resolve())

    segments, info = model.transcribe(audio_path)

    transcript = []
    for segment in segments:
        transcript.append(segment.text)

    return " ".join(transcript).strip()
