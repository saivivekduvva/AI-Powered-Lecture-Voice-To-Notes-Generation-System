def segment_text(text: str, max_words: int = 200) -> list:
    words = text.split()
    segments = []

    for i in range(0, len(words), max_words):
        segment = " ".join(words[i:i + max_words])
        segments.append(segment)

    return segments
