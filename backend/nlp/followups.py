# backend/nlp/followups.py
import re

def extract_followups(text: str):
    """
    Identify questions and pending clarifications.
    Returns list of strings.
    """
    lines = re.split(r"\n|(?<=[.!?])\s+", text)
    followups = []

    for l in lines:
        s = l.strip()
        if not s:
            continue
        if "?" in s:
            followups.append(s)
            continue

        # phrases indicating follow-up needed
        cues = [
            "need confirmation",
            "blocked by",
            "waiting on",
            "pending approval",
            "clarify",
            "to decide",
            "open question",
            "unknown",
        ]
        if any(cue in s.lower() for cue in cues):
            followups.append(s)

    # dedupe
    uniq = []
    seen = set()
    for f in followups:
        k = f.lower()
        if k not in seen:
            seen.add(k)
            uniq.append(f)
    return uniq
