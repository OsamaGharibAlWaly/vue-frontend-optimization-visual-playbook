"""Render every concept as one high-resolution diagram and write a manifest."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data_00_story  # noqa: F401
import data_01_foundations_a  # noqa: F401
import data_01_foundations_b  # noqa: F401
import data_02_opt_phase1  # noqa: F401
import data_02_opt_phase2  # noqa: F401
import data_02_opt_phase3  # noqa: F401
import data_02_opt_phase4  # noqa: F401
import data_03_scaling_p1  # noqa: F401
import data_03_scaling_p2  # noqa: F401
import data_03_scaling_p3  # noqa: F401
import data_04_security_p1  # noqa: F401
import data_04_security_p2  # noqa: F401
import data_05_proof  # noqa: F401
from catalogue import ALL_CONCEPTS
from design import render


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    grouped = {}
    for concept in ALL_CONCEPTS:
        grouped.setdefault(concept["folder"], []).append(concept)

    total = len(ALL_CONCEPTS)
    manifest = []
    for folder, items in grouped.items():
        for number, concept in enumerate(items, 1):
            rel = f"images/{folder}/{number:02d}-{concept['slug']}.png"
            render(concept, os.path.join(root, rel), number, len(items))
            manifest.append({
                "folder": folder,
                "number": number,
                "count": len(items),
                "chapter": concept["chapter"],
                "title": concept["title"],
                "slug": concept["slug"],
                "image": rel.replace("\\", "/"),
                "subtitle": concept["subtitle"],
                "takeaway": concept["takeaway"],
                "prompt": concept["prompt"],
                "visual": concept["visual"]["kind"],
            })
            print(f"{rel} ({number}/{len(items)})")

    with open(os.path.join(root, "images", "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)

    print(f"\nRendered {total} diagrams across {len(grouped)} section folders.")


if __name__ == "__main__":
    main()
