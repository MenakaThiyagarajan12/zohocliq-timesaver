# backend/nlp/summarizer.py
import re

def _clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text

def summarize_text(text: str, max_sentences: int = 3) -> str:
    """
    Lightweight extractive summary:
    - Split into sentences
    - Score sentences by length + keyword presence
    - Return top N
    """
    text = _clean(text)
    if not text:
        return ""

    # naive sentence split
    sentences = re.split(r"(?<=[.!?])\s+", text)
    if len(sentences) <= max_sentences:
        return _clean(text)

    keywords = {"decision", "deadline", "action", "deliver", "issue", "risk", "plan", "update", "timeline", "next"}
    scores = []
    for s in sentences:
        length_score = min(len(s) / 120.0, 1.0)
        keyword_score = sum(1 for k in keywords if k in s.lower())
        scores.append((length_score + keyword_score * 1.5, s))

    top = sorted(scores, key=lambda x: x[0], reverse=True)[:max_sentences]
    summary = " ".join([s for _, s in top])
    return _clean(summary)
