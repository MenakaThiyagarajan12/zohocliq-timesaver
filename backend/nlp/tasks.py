# backend/nlp/tasks.py
import re

def extract_tasks(text: str):
    """
    Detect simple task-like phrases using pattern heuristics.
    Returns list of dicts: {title, owner, due}
    """
    lines = re.split(r"\n|(?<=[.!?])\s+", text)
    tasks = []

    task_patterns = [
        r"\b(todo|task|action item|next step)\b[:\-]\s*(.+)",
        r"\b(we|let's|please)\s+(finish|complete|deliver|prepare|send|review)\s+(.+?)(?:\s+by\s+([A-Za-z0-9\-/:]+))?",
        r"\bassign\s+(.+?)\s+to\s+([A-Za-z][A-Za-z0-9_]+)(?:\s+by\s+([A-Za-z0-9\-/:]+))?",
    ]

    for line in lines:
        l = line.strip()
        if not l:
            continue
        for pat in task_patterns:
            m = re.search(pat, l, flags=re.IGNORECASE)
            if m:
                title = None
                owner = None
                due = None

                groups = [g for g in m.groups() if g]
                # crude mapping
                if pat.startswith(r"\b(todo"):
                    title = groups[-1]
                elif pat.startswith(r"\b(we|let's|please)"):
                    verb = groups[1]
                    obj = groups[2]
                    title = f"{verb} {obj}"
                    if len(groups) >= 4:
                        due = groups[3]
                else:  # assign ...
                    title = groups[0]
                    owner = groups[1]
                    if len(groups) >= 3:
                        due = groups[2]

                tasks.append({
                    "title": title.strip() if title else l,
                    "owner": owner,
                    "due": due,
                    "source": l
                })
                break

    # dedupe by title
    seen = set()
    unique = []
    for t in tasks:
        key = (t["title"].lower(), t.get("owner") or "", t.get("due") or "")
        if key not in seen:
            seen.add(key)
            unique.append(t)
    return unique
