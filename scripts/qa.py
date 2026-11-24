"""Layout QA without eyeballs: catch clipped text and text-on-text collisions."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
from PIL import Image

import design
from catalogue import ALL_CONCEPTS
from design import DRAWERS, BG

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

original_txt = design.txt


def collect():
    artists = []

    def spy(*args, **kwargs):
        artist = original_txt(*args, **kwargs)
        artists.append(artist)
        return artist

    design.txt = spy
    return artists


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clipped, collisions, sizes = [], [], set()
    for concept in ALL_CONCEPTS:
        artists = collect()
        fig, ax = design.new_canvas(concept, 1, 1)
        payload = dict(concept["visual"])
        payload.setdefault("subtitle", concept["subtitle"])
        DRAWERS[payload["kind"]](ax, payload)
        design.txt = original_txt
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        w, h = fig.canvas.get_width_height()
        sizes.add((w, h))
        boxes = []
        for artist in artists:
            b = artist.get_window_extent(renderer)
            label = artist.get_text().replace("\n", " ")[:36]
            if b.x0 < -1 or b.y0 < -1 or b.x1 > w + 1 or b.y1 > h + 1:
                clipped.append((concept["slug"], label, tuple(round(v) for v in b.bounds)))
            boxes.append((b, label))
        for i, (a, la) in enumerate(boxes):
            for b, lb in boxes[i + 1:]:
                ix = max(0, min(a.x1, b.x1) - max(a.x0, b.x0))
                iy = max(0, min(a.y1, b.y1) - max(a.y0, b.y0))
                overlap = ix * iy
                smaller = min(a.width * a.height, b.width * b.height)
                if smaller and overlap / smaller > 0.45:
                    collisions.append((concept["slug"], la, lb, round(overlap / smaller, 2)))
        plt.close(fig)

    pngs = []
    for dirpath, _, files in os.walk(os.path.join(root, "images")):
        pngs.extend(os.path.join(dirpath, f) for f in files if f.endswith(".png"))
    with Image.open(pngs[0]) as im:
        img_size = im.size
    total_mb = sum(os.path.getsize(p) for p in pngs) / 1024 / 1024

    print(f"PNG count: {len(pngs)} | canvas: {img_size} | total: {total_mb:.1f} MB")
    print(f"Render sizes: {sizes}")
    print(f"Clipped text: {len(clipped)}")
    for row in clipped[:20]:
        print("  ", row)
    print(f"Text collisions: {len(collisions)}")
    for row in collisions[:30]:
        print("  ", row)
    return 1 if clipped or collisions else 0


if __name__ == "__main__":
    sys.exit(main())
