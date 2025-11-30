# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from webhook_handler import handle_cliq_webhook
from stt_engine import transcribe_audio
from formatter import format_output
from nlp.summarizer import summarize_text
from nlp.tasks import extract_tasks
from nlp.followups import extract_followups
from nlp.highlights import extract_highlights

app = Flask(__name__)
CORS(app)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "app": "cliq-timesaver"}), 200

@app.route("/webhook/cliq", methods=["POST"])
def cliq_webhook():
    payload = request.json or {}
    result = handle_cliq_webhook(payload)
    return jsonify(result), 200

@app.route("/process/audio", methods=["POST"])
def process_audio():
    if "file" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    audio_file = request.files["file"]
    # Optional: save file if needed
    # audio_path = os.path.join(Config.UPLOAD_DIR, secure_filename(audio_file.filename))
    # audio_file.save(audio_path)

    # Transcribe (stubbed / simple)
    transcript = transcribe_audio(audio_file)

    # NLP pipeline
    summary = summarize_text(transcript)
    tasks = extract_tasks(transcript)
    followups = extract_followups(transcript)
    highlights = extract_highlights(transcript)

    # Format for frontend
    output = format_output(
        transcript=transcript,
        summary=summary,
        tasks=tasks,
        followups=followups,
        highlights=highlights,
    )
    return jsonify(output), 200

@app.route("/process/text", methods=["POST"])
def process_text():
    data = request.json or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Text is required"}), 400

    summary = summarize_text(text)
    tasks = extract_tasks(text)
    followups = extract_followups(text)
    highlights = extract_highlights(text)

    output = format_output(
        transcript=text,
        summary=summary,
        tasks=tasks,
        followups=followups,
        highlights=highlights,
    )
    return jsonify(output), 200

if __name__ == "__main__":
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
