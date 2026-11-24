"""Shared concept registry and tiny payload helpers for the visual playbook."""

ALL_CONCEPTS = []


def flow(steps, note=None):
    return {"kind": "flow", "steps": steps, "note": note}


def compare(before, after, verdict=None, before_label="BEFORE — WHAT HURTS",
            after_label="AFTER — WHAT SHIPS"):
    return {"kind": "compare", "before": before, "after": after,
            "verdict": verdict, "before_label": before_label, "after_label": after_label}


def code(before, after, note=None, before_label="BEFORE", after_label="AFTER",
         language="vue"):
    return {"kind": "code", "before": before, "after": after, "note": note,
            "before_label": before_label, "after_label": after_label, "language": language}


def layers(items, note=None):
    return {"kind": "layers", "items": items, "note": note}


def tree(rows, note=None):
    return {"kind": "tree", "rows": rows, "note": note}


def metrics(cards, bars, note=None):
    return {"kind": "metrics", "cards": cards, "bars": bars, "note": note}


def cycle(steps, center="LOOP", note=None):
    return {"kind": "cycle", "steps": steps, "center": center, "note": note}


def matrix(axes, quadrants, note=None):
    return {"kind": "matrix", "axes": axes, "quadrants": quadrants, "note": note}


def timeline(rows, note=None):
    return {"kind": "timeline", "rows": rows, "note": note}


def decision(question, branches, note=None):
    return {"kind": "decision", "question": question, "branches": branches, "note": note}


def bullets(items, note=None):
    return {"kind": "bullets", "items": items, "note": note}


def anatomy(center, nodes, note=None):
    return {"kind": "anatomy", "center": center, "nodes": nodes, "note": note}


def hero(pillars, strip=None):
    return {"kind": "hero", "pillars": pillars, "strip": strip}


class catalogue:
    """Collect concepts for one folder and give them stable numbers."""

    def __init__(self, folder, chapter, intro=""):
        self.folder = folder
        self.chapter = chapter
        self.intro = intro
        self.items = []

    def add(self, slug, title, kicker, subtitle, visual, takeaway, prompt):
        concept = {
            "folder": self.folder,
            "chapter": self.chapter,
            "chapter_intro": self.intro,
            "slug": slug,
            "title": title,
            "kicker": kicker,
            "subtitle": subtitle,
            "visual": visual,
            "takeaway": takeaway,
            "prompt": prompt,
        }
        self.items.append(concept)
        ALL_CONCEPTS.append(concept)
        return concept
