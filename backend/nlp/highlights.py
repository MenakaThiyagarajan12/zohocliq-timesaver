# backend/nlp/highlights.py
import re

def extract_highlights(text: str, max_items: int = 5):
    """
    Pull standout sentences mentioning decisions, deadlines, metrics, risks, and wins.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text)
    keywords = {
        "decision": 2.0,
        "decided": 2.0,
        "deadline": 2.0,
        "risk": 1.5,
        "issue": 1.2,
        "blocked": 1.4,
        "ship": 1.2,
        "release": 1.2,
        "metric": 1.0,
        "growth": 1.2,
        "increase": 1.0,
        "decrease": 1.0,
        "target": 1.0,
        "priority": 1.3,
        "budget": 1.1,
        "approval": 1.1,
        "win": 1.2,
        "success": 1.2,
    }
    scored = []
    for s in sentences:
        ls = s.strip()
        if not ls:
            continue
        score = 0.2 * min(len(ls) / 120.0, 1.0)
        for k, w in keywords.items():
            if k in ls.lower():
                score += w
        scored.append((score, ls))

    top = [s for _, s in sorted(scored, key=lambda x: x[0], reverse=True)[:max_items]]
    return top
