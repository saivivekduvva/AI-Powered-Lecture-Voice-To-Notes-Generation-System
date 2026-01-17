from services.speech_to_text import speech_to_text

def test_stt():
    assert callable(speech_to_text)
