from faster_whisper import WhisperModel

model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe("sample_lecture.wav")

for segment in segments:
    print(segment.text)
