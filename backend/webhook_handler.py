# backend/webhook_handler.py
from nlp.summarizer import summarize_text
from nlp.tasks import extract_tasks
from nlp.followups import extract_followups
from nlp.highlights import extract_highlights
from formatter import format_output

def handle_cliq_webhook(payload: dict) -> dict:
    """
    Expected Zoho Cliq webhook payload (simplified example):
    {
      "channel": "general",
      "user": "alice",
      "message": "Meeting notes: ...",
      "timestamp": "2025-11-17T17:20:00Z"
    }
    """
    text = (payload.get("message") or "").strip()
    if not text:
        return {"error": "Empty message in webhook payload"}

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
        meta={
            "channel": payload.get("channel"),
            "user": payload.get("user"),
            "timestamp": payload.get("timestamp"),
            "source": "cliq_webhook",
        },
    )
    return output
