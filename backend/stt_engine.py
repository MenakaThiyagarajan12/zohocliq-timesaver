# backend/stt_engine.py
def transcribe_audio(file_storage) -> str:
    """
    Stubbed transcription function. Replace with a real STT like:
    - Vosk (offline)
    - OpenAI Whisper (local/remote)
    - Google Cloud STT (remote)
    For demo: returns a placeholder or tries to read text if a .txt audio is uploaded.
    """
    filename = file_storage.filename.lower()
    if filename.endswith(".txt"):
        # If someone uploads a .txt pretending to be audio, read it as transcript
        return file_storage.read().decode("utf-8", errors="ignore")
    return "This is a demo transcript. Replace stt_engine.transcribe_audio with a real speech-to-text backend."
