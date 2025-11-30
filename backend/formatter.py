# backend/formatter.py
def format_output(transcript, summary, tasks, followups, highlights, meta=None):
    return {
        "meta": meta or {},
        "transcript": transcript,
        "summary": summary,
        "tasks": tasks,
        "followups": followups,
        "highlights": highlights,
    }
