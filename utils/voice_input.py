def voice_input_button():
    import streamlit as st
    from audio_recorder_streamlit import audio_recorder
    from pydub import AudioSegment
    import speech_recognition as sr
    import tempfile

    audio_bytes = audio_recorder(text="Speak now", icon_size="2x")
    if audio_bytes:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_path) as source:
            audio = recognizer.record(source)
            try:
                return recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                return "Could not understand audio"
            except sr.RequestError:
                return "Request failed"
