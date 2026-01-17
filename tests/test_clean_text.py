from preprocessing.clean_text import clean_transcript

def test_clean():
    text = "uh this is um a test"
    cleaned = clean_transcript(text)
    assert "uh" not in cleaned
