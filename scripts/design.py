"""One visual language for every diagram in the playbook.

Canvas: 16 x 9 inches, 170 dpi. Coordinates are inches, aspect ratio is equal,
so circles are circles and corner radii stay consistent at every size.
"""

import os
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

BG = "#080E1A"
GRID = "#142139"
PANEL = "#111C30"
PANEL_DARK = "#0C1526"
BORDER = "#2A3C59"
TEXT = "#EDF3FB"
MUTED = "#98AAC6"
CYAN = "#38BDF8"
TEAL = "#2DD4BF"
AMBER = "#FBBF24"
ROSE = "#FB7185"
VIOLET = "#A78BFA"
GREEN = "#34D399"
BLUE = "#60A5FA"

ACCENTS = [CYAN, TEAL, AMBER, VIOLET, GREEN, BLUE, ROSE]
COLOR_KEYS = {
    "cyan": CYAN, "teal": TEAL, "amber": AMBER, "rose": ROSE,
    "violet": VIOLET, "green": GREEN, "blue": BLUE,
}

HEAD_FONT = "Segoe UI"
MONO_FONT = "Cascadia Code"
REPO = "vue-frontend-optimization-visual-playbook"


def tint(color, alpha):
    return to_rgba(color, alpha)


def wrap(text, chars):
    return "\n".join(textwrap.wrap(str(text), width=chars, break_long_words=False,
                                   break_on_hyphens=False)) or ""


def txt(ax, x, y, s, size=12, color=TEXT, weight="normal", ha="left", va="top",
        font=HEAD_FONT, alpha=1.0, spacing=1.22, zorder=6, rotation=0):
    return ax.text(x, y, s, fontsize=size, color=color, fontfamily=font,
                   fontweight=weight, ha=ha, va=va, alpha=alpha,
                   linespacing=spacing, zorder=zorder, rotation=rotation)


def panel(ax, x, y, w, h, fill=PANEL, border=BORDER, radius=0.13, lw=1.0,
          alpha=1.0, zorder=2):
    patch = FancyBboxPatch((x, y), w, h,
                           boxstyle=f"round,pad=0,rounding_size={radius}",
                           facecolor=fill, edgecolor=border, linewidth=lw,
                           alpha=alpha, zorder=zorder)
    ax.add_patch(patch)
    return patch


def stripe(ax, x, y, w, h, color, radius=0.05):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle=f"round,pad=0,rounding_size={radius}",
                                facecolor=color, edgecolor="none", zorder=3))


def arrow(ax, x1, y1, x2, y2, color=CYAN, lw=1.7, rad=0.0, scale=14):
    patch = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                            mutation_scale=scale, linewidth=lw, color=color,
                            connectionstyle=f"arc3,rad={rad}", zorder=4)
    ax.add_patch(patch)
    return patch


def badge(ax, cx, cy, label, color=CYAN, r=0.23, size=10.5):
    ax.add_patch(Circle((cx, cy), r, facecolor=color, edgecolor="none", zorder=7))
    txt(ax, cx, cy + 0.005, str(label), size=size, color=BG, weight="bold",
        ha="center", va="center", zorder=8)


def note_strip(ax, note, y=1.02):
    if not note:
        return
    panel(ax, 0.6, y, 14.8, 0.68, fill=tint(TEAL, 0.07), border=tint(TEAL, 0.30),
          radius=0.10, zorder=2)
    stripe(ax, 0.6, y, 0.11, 0.68, TEAL, radius=0.04)
    txt(ax, 0.95, y + 0.34, wrap(note, 150), size=11.2, color="#BEEBE2",
        va="center", zorder=6)


def new_canvas(concept, index, total):
    fig = plt.figure(figsize=(16, 9), dpi=170, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.set_aspect("equal")
    ax.axis("off")

    for x in [0.25 + i * 0.43 for i in range(37)]:
        for y in [0.95 + i * 0.43 for i in range(19)]:
            ax.plot(x, y, marker=".", markersize=1.0,
                    color=GRID, zorder=0)

    kicker = concept["kicker"].upper().replace(" ", "  ")
    txt(ax, 0.6, 8.55, kicker, size=10.5, color=CYAN, weight="bold", zorder=6)
    title_size = 30 if len(concept["title"]) <= 42 else 26
    txt(ax, 0.6, 7.92, wrap(concept["title"], 58), size=title_size,
        color=TEXT, weight="bold", spacing=1.05, zorder=6)
    txt(ax, 0.6, 7.12, wrap(concept["subtitle"], 118), size=13.4,
        color=MUTED, spacing=1.2, zorder=6)

    ax.plot([0.6, 15.4], [6.82, 6.82], color=BORDER, lw=1.0, zorder=1)
    ax.plot([0.6, 2.3], [6.82, 6.82], color=CYAN, lw=3.0, zorder=2)

    label = concept["chapter"].upper()
    box_w = min(5.6, max(2.7, len(label) * 0.085 + 0.6))
    panel(ax, 15.4 - box_w, 8.28, box_w, 0.52, fill=tint(CYAN, 0.08),
          border=tint(CYAN, 0.35), radius=0.16, zorder=3)
    txt(ax, 15.4 - box_w / 2, 8.54, label, size=9.6, color=CYAN,
        weight="bold", ha="center", va="center", zorder=6)

    ax.plot([0.6, 15.4], [0.78, 0.78], color=BORDER, lw=0.8, zorder=1)
    txt(ax, 0.6, 0.4, f"{REPO.upper()}  ·  VISUAL STORY", size=8.6,
        color=MUTED, weight="bold", zorder=6)
    txt(ax, 15.4, 0.4, f"{index:03d} / {total:03d}", size=9.2, color=CYAN,
        weight="bold", ha="right", zorder=6)
    return fig, ax


# ---------------------------------------------------------------------------
# Visual templates
# ---------------------------------------------------------------------------

def draw_flow(ax, v):
    steps = v["steps"]
    n = len(steps)
    gap = 0.42
    w = (14.8 - (n - 1) * gap) / n
    y, h = 2.35, 3.15
    for i, (title, detail) in enumerate(steps):
        x = 0.6 + i * (w + gap)
        color = ACCENTS[i % len(ACCENTS)]
        panel(ax, x, y, w, h, fill=PANEL, border=tint(color, 0.5), zorder=2)
        stripe(ax, x, y + h - 0.09, w, 0.09, color, radius=0.04)
        badge(ax, x + w - 0.34, y + h - 0.36, i + 1, color=color, r=0.22, size=9.5)
        txt(ax, x + 0.24, y + h - 0.55, wrap(title, max(12, int(w * 5.2))),
            size=13.2, color=color, weight="bold", zorder=6)
        txt(ax, x + 0.24, y + h - 1.25, wrap(detail, max(15, int(w * 6.1))),
            size=10.8, color=MUTED, zorder=6)
        if i < n - 1:
            arrow(ax, x + w + 0.04, y + h / 2, x + w + gap - 0.04, y + h / 2,
                  color=MUTED, lw=1.5, scale=12)
    note_strip(ax, v.get("note"))


def draw_compare(ax, v):
    y, h, w = 1.85, 4.55, 7.15
    for x, label, items, color in [
        (0.6, v["before_label"], v["before"], ROSE),
        (8.25, v["after_label"], v["after"], GREEN),
    ]:
        panel(ax, x, y, w, h, fill=PANEL, border=tint(color, 0.45), zorder=2)
        stripe(ax, x, y + h - 0.72, w, 0.72, tint(color, 0.16), radius=0.10)
        txt(ax, x + 0.3, y + h - 0.23, label, size=13.5, color=color,
            weight="bold", va="center", zorder=6)
        avail = h - 1.15
        step = avail / max(1, len(items))
        for i, item in enumerate(items):
            iy = y + h - 1.0 - i * step
            ax.add_patch(Circle((x + 0.40, iy - 0.09), 0.065,
                                facecolor=color, edgecolor="none", zorder=6))
            txt(ax, x + 0.68, iy, wrap(item, 64), size=11.3,
                color=TEXT if i % 2 == 0 else "#CBD8E8", zorder=6, spacing=1.25)
    note_strip(ax, v.get("verdict"))


def draw_code(ax, v):
    y, h, w = 1.82, 4.58, 7.15
    for x, label, lines, color in [
        (0.6, v["before_label"], v["before"], ROSE),
        (8.25, v["after_label"], v["after"], GREEN),
    ]:
        panel(ax, x, y, w, h, fill=PANEL_DARK, border=tint(color, 0.45), zorder=2)
        stripe(ax, x, y + h - 0.62, w, 0.62, tint(color, 0.16), radius=0.10)
        txt(ax, x + 0.3, y + h - 0.20, label, size=13.2, color=color,
            weight="bold", va="center", zorder=6)
        n = min(len(lines), 13)
        step = min(0.31, 3.35 / max(1, n))
        for i, line in enumerate(lines[:13]):
            stripped = line.strip()
            c = MUTED if stripped.startswith(("//", "#", "<!--")) else TEXT
            if stripped.startswith("-"):
                c = ROSE
            elif stripped.startswith("+"):
                c = GREEN
            txt(ax, x + 0.28, y + h - 0.88 - i * step, line,
                size=10.0 if n > 10 else 10.9, color=c, font=MONO_FONT,
                zorder=6, spacing=1.0)
    note_strip(ax, v.get("note"))


def draw_layers(ax, v):
    items = v["items"]
    n = len(items)
    row_h = min(0.84, 5.05 / n)
    y0 = 6.4
    for i, item in enumerate(items):
        tag, title, detail = item
        color = ACCENTS[i % len(ACCENTS)]
        y = y0 - (i + 1) * row_h
        panel(ax, 0.6, y, 14.8, row_h - 0.12, fill=PANEL,
              border=tint(color, 0.35), radius=0.11, zorder=2)
        stripe(ax, 0.6, y, 0.1, row_h - 0.12, color, radius=0.04)
        txt(ax, 0.92, y + (row_h - 0.12) / 2, tag, size=11.2, color=color,
            weight="bold", va="center", zorder=6)
        txt(ax, 3.5, y + (row_h - 0.12) / 2, title, size=12.6, color=TEXT,
            weight="bold", va="center", zorder=6)
        txt(ax, 7.25, y + (row_h - 0.12) / 2, wrap(detail, 74), size=10.8,
            color=MUTED, va="center", zorder=6, spacing=1.15)
    note_strip(ax, v.get("note"))


def draw_tree(ax, v):
    rows = v["rows"]
    panel(ax, 0.6, 1.75, 14.8, 4.7, fill=PANEL_DARK, border=BORDER, zorder=2)
    step = min(0.52, 4.3 / max(1, len(rows)))
    for i, row in enumerate(rows):
        indent, line, note = row
        color = ACCENTS[min(indent, len(ACCENTS) - 1)]
        y = 6.12 - i * step
        ax.add_patch(Rectangle((0.92 + indent * 0.3, y - 0.16), 0.11, 0.11,
                               facecolor=color, edgecolor="none", zorder=6))
        txt(ax, 1.22 + indent * 0.3, y, line, size=11.3, color=TEXT,
            font=MONO_FONT, zorder=6, spacing=1.0)
        if note:
            txt(ax, 8.0, y, wrap(note, 55), size=10.5, color=MUTED,
                zorder=6, spacing=1.1)
        if i < len(rows) - 1:
            ax.plot([1.25, 1.25], [y - 0.06, y - step + 0.12],
                    color=BORDER, lw=0.8, zorder=3)
    note_strip(ax, v.get("note"))


def draw_metrics(ax, v):
    cards = v["cards"]
    n = max(1, len(cards))
    gap = 0.28
    w = (14.8 - (n - 1) * gap) / n
    for i, (value, label) in enumerate(cards):
        x = 0.6 + i * (w + gap)
        color = ACCENTS[i % len(ACCENTS)]
        panel(ax, x, 5.05, w, 1.35, fill=PANEL, border=tint(color, 0.45), zorder=2)
        stripe(ax, x, 6.35, w, 0.05, color, radius=0.02)
        txt(ax, x + 0.28, 5.92, value, size=25, color=color, weight="bold", zorder=6)
        txt(ax, x + 0.28, 5.42, wrap(label, 26), size=10.6, color=MUTED, zorder=6)

    panel(ax, 0.6, 1.8, 14.8, 2.95, fill=PANEL_DARK, border=BORDER, zorder=2)
    txt(ax, 0.9, 4.35, "IMPACT SNAPSHOT", size=10.6, color=CYAN,
        weight="bold", zorder=6)
    bars = v["bars"]
    base = 2.35
    max_val = max([b[1] for b in bars] + [1])
    count = len(bars)
    slot = 11.4 / max(1, count)
    for i, bar in enumerate(bars):
        label, value = bar[0], bar[1]
        key = bar[2] if len(bar) > 2 else None
        color = COLOR_KEYS.get(key, ACCENTS[i % len(ACCENTS)])
        bx = 3.0 + i * slot + slot * 0.18
        bw = slot * 0.62
        bh = max(0.12, 1.72 * value / max_val)
        panel(ax, bx, base, bw, bh, fill=tint(color, 0.55),
              border=tint(color, 0.8), radius=0.06, zorder=3)
        txt(ax, bx + bw / 2, base + bh + 0.12, str(value), size=10.4,
            color=color, weight="bold", ha="center", zorder=6)
        txt(ax, bx + bw / 2, base - 0.18, wrap(label, 18), size=9.8,
            color=MUTED, ha="center", zorder=6)
    note_strip(ax, v.get("note"))


def draw_cycle(ax, v):
    steps = v["steps"]
    n = len(steps)
    cx, cy = 8.0, 4.1
    rx, ry = 3.94, 1.7 if n <= 4 else 1.9
    positions = []
    for i in range(n):
        a = 1.5708 - i * 2 * 3.14159 / n
        positions.append((cx + rx * __import__("math").cos(a),
                          cy + ry * __import__("math").sin(a)))
    for i in range(n):
        x1, y1 = positions[i]
        x2, y2 = positions[(i + 1) % n]
        arrow(ax, x1 + (x2 - x1) * 0.25, y1 + (y2 - y1) * 0.25,
              x1 + (x2 - x1) * 0.68, y1 + (y2 - y1) * 0.68,
              color=tint(CYAN, 0.65), lw=1.6, rad=-0.12, scale=12)
    ax.add_patch(Circle((cx, cy), 1.02, facecolor=tint(CYAN, 0.10),
                        edgecolor=CYAN, lw=1.5, zorder=3))
    txt(ax, cx, cy + 0.12, wrap(v["center"], 16), size=13.2, color=CYAN,
        weight="bold", ha="center", va="center", zorder=6)
    for i, (title, detail) in enumerate(steps):
        x, y = positions[i]
        color = ACCENTS[i % len(ACCENTS)]
        panel(ax, x - 1.42, y - 0.56, 2.84, 1.12, fill=PANEL,
              border=tint(color, 0.55), radius=0.14, zorder=4)
        badge(ax, x - 1.15, y + 0.32, i + 1, color=color, r=0.16, size=8.5)
        txt(ax, x + 0.3, y + 0.34, wrap(title, 20), size=11.8, color=color,
            weight="bold", ha="center", va="center", zorder=7)
        txt(ax, x, y - 0.12, wrap(detail, 32), size=9.6, color=MUTED,
            ha="center", va="center", zorder=7, spacing=1.1)
    note_strip(ax, v.get("note"))


def draw_matrix(ax, v):
    xlabel, ylabel = v["axes"]
    x0, y0, w, h = 2.4, 1.6, 12.6, 4.75
    panel(ax, x0, y0, w, h, fill=PANEL_DARK, border=BORDER, zorder=2)
    ax.plot([x0 + w / 2, x0 + w / 2], [y0, y0 + h], color=BORDER, lw=1.2, zorder=3)
    ax.plot([x0, x0 + w], [y0 + h / 2, y0 + h / 2], color=BORDER, lw=1.2, zorder=3)
    centers = [
        (x0 + w * 0.25, y0 + h * 0.75),
        (x0 + w * 0.75, y0 + h * 0.75),
        (x0 + w * 0.25, y0 + h * 0.25),
        (x0 + w * 0.75, y0 + h * 0.25),
    ]
    for i, (title, detail) in enumerate(v["quadrants"][:4]):
        cx, cy = centers[i]
        color = ACCENTS[i % len(ACCENTS)]
        txt(ax, cx, cy + 0.42, wrap(title, 24), size=13.4, color=color,
            weight="bold", ha="center", va="center", zorder=6)
        txt(ax, cx, cy - 0.5, wrap(detail, 38), size=10.6, color=MUTED,
            ha="center", va="center", zorder=6, spacing=1.2)
    txt(ax, 1.35, y0 + h / 2, wrap(ylabel, 20), size=11.2, color=CYAN,
        weight="bold", ha="center", va="center", rotation=90, zorder=6)
    txt(ax, x0 + w / 2, 1.16, wrap(xlabel, 60), size=11.2, color=CYAN,
        weight="bold", ha="center", va="center", zorder=6)
    note_strip(ax, v.get("note"))


def draw_timeline(ax, v):
    rows = v["rows"]
    panel(ax, 0.6, 1.75, 14.8, 4.7, fill=PANEL_DARK, border=BORDER, zorder=2)
    track_x, track_w = 4.0, 10.9
    step = min(0.62, 4.25 / max(1, len(rows)))
    for i, row in enumerate(rows):
        label, start, width, color_key = row
        color = COLOR_KEYS.get(color_key, ACCENTS[i % len(ACCENTS)])
        y = 6.08 - (i + 1) * step + 0.14
        txt(ax, 0.92, y + 0.16, wrap(label, 22), size=10.7, color=TEXT,
            va="center", zorder=6)
        panel(ax, track_x, y + 0.04, track_w, 0.34, fill=tint(MUTED, 0.10),
              border="none", radius=0.08, zorder=3)
        panel(ax, track_x + track_w * start, y + 0.04, max(0.12, track_w * width),
              0.34, fill=tint(color, 0.68), border=tint(color, 0.9),
              radius=0.08, zorder=4)
        txt(ax, track_x + track_w + 0.16, y + 0.21, f"{int(width * 100)}%",
            size=9.6, color=color, weight="bold", va="center", zorder=6)
    for tick in range(5):
        tx = track_x + track_w * tick / 4
        ax.plot([tx, tx], [1.98, 2.12], color=BORDER, lw=0.8, zorder=3)
        txt(ax, tx, 1.79, f"{tick * 25}", size=8.6, color=MUTED,
            ha="center", zorder=6)
    note_strip(ax, v.get("note"))


def draw_decision(ax, v):
    panel(ax, 0.6, 5.5, 14.8, 1.05, fill=tint(CYAN, 0.09),
          border=tint(CYAN, 0.45), zorder=2)
    txt(ax, 3.7, 6.02, wrap(v["question"], 82), size=15.5, color=TEXT,
        weight="bold", va="center", zorder=6)
    branches = v["branches"]
    n = len(branches)
    for i, (label, title, detail) in enumerate(branches[:4]):
        if n <= 2:
            bw, bx = 6.6, 1.0 + i * 7.4
            by, bh = 2.25, 2.65
        else:
            bw, bx = 6.6, 1.0 + (i % 2) * 7.4
            by, bh = 3.5 - (i // 2) * 2.0, 1.65
        color = ACCENTS[i % len(ACCENTS)]
        panel(ax, bx, by, bw, bh, fill=PANEL, border=tint(color, 0.45), zorder=2)
        badge(ax, bx + 0.55, by + bh - 0.42, label[:2], color=color, r=0.28, size=9)
        txt(ax, bx + 1.05, by + bh - 0.25, wrap(label, 30), size=12.6,
            color=color, weight="bold", va="center", zorder=6)
        txt(ax, bx + 0.42, by + bh - 0.95, wrap(title, 42), size=11.8,
            color=TEXT, weight="bold", zorder=6)
        txt(ax, bx + 0.42, by + bh - 1.45, wrap(detail, 50), size=10.6,
            color=MUTED, zorder=6, spacing=1.2)
        arrow(ax, 8.0, 5.48, bx + bw / 2, by + bh + 0.06,
              color=tint(color, 0.7), lw=1.4, scale=12)
    note_strip(ax, v.get("note"))


def draw_bullets(ax, v):
    items = v["items"]
    n = len(items)
    cols = 3 if n <= 3 or n >= 5 else 2
    rows = (n + cols - 1) // cols
    gap = 0.32
    total_h = 5.0
    ch = (total_h - (rows - 1) * gap) / rows
    cw = (14.8 - (cols - 1) * gap) / cols
    for i, (title, detail) in enumerate(items):
        r, c = divmod(i, cols)
        x = 0.6 + c * (cw + gap)
        y = 6.55 - (r + 1) * ch - r * gap
        color = ACCENTS[i % len(ACCENTS)]
        panel(ax, x, y, cw, ch, fill=PANEL, border=tint(color, 0.40), zorder=2)
        badge(ax, x + 0.52, y + ch - 0.52, i + 1, color=color, r=0.28, size=10.5)
        txt(ax, x + 0.32, y + ch - 1.02, wrap(title, 27), size=13.4,
            color=color, weight="bold", zorder=6)
        txt(ax, x + 0.32, y + ch - 1.72, wrap(detail, 40), size=10.9,
            color=MUTED, zorder=6, spacing=1.22)
    note_strip(ax, v.get("note"))


def draw_anatomy(ax, v):
    center_title, center_detail = v["center"]
    nodes = v["nodes"]
    panel(ax, 5.85, 3.28, 4.3, 1.55, fill=tint(CYAN, 0.10),
          border=CYAN, radius=0.18, zorder=4)
    txt(ax, 8.0, 4.32, wrap(center_title, 26), size=15.0, color=CYAN,
        weight="bold", ha="center", va="center", zorder=7)
    txt(ax, 8.0, 3.76, wrap(center_detail, 38), size=10.4, color=MUTED,
        ha="center", va="center", zorder=7)

    n = len(nodes)
    for i, (label, detail) in enumerate(nodes[:6]):
        color = ACCENTS[i % len(ACCENTS)]
        if n <= 4:
            x = 0.6 if i % 2 == 0 else 11.1
            y = 5.1 if i < 2 else 2.05
        else:
            x = 0.6 if i % 2 == 0 else 11.1
            y = 5.45 - (i // 2) * 1.7
        panel(ax, x, y, 4.3, 1.3, fill=PANEL, border=tint(color, 0.45), zorder=3)
        stripe(ax, x, y + 1.22, 4.3, 0.08, color, radius=0.03)
        txt(ax, x + 0.28, y + 0.98, wrap(label, 30), size=12.2, color=color,
            weight="bold", zorder=6)
        txt(ax, x + 0.28, y + 0.56, wrap(detail, 42), size=10.3,
            color=MUTED, zorder=6, spacing=1.15)
        sx = x + 4.3 if x < 5 else x
        sy = y + 0.65
        arrow(ax, sx, sy, 8.0 if x < 5 else 8.0, 4.05,
              color=tint(color, 0.6), lw=1.3, scale=11)
    note_strip(ax, v.get("note"))


def draw_hero(ax, v):
    txt(ax, 0.65, 6.35, "A visual, prompt-driven story from slow app to shipped app.",
        size=21, color=TEXT, weight="bold", zorder=6)
    txt(ax, 0.65, 5.72, wrap(v.get("subtitle", ""), 110), size=13.5,
        color=MUTED, zorder=6)
    for i, (title, detail) in enumerate(v["pillars"]):
        x = 0.6 + i * 5.0
        color = [CYAN, VIOLET, AMBER][i % 3]
        panel(ax, x, 2.25, 4.75, 2.85, fill=PANEL, border=tint(color, 0.5), zorder=2)
        stripe(ax, x, 5.03, 4.75, 0.07, color, radius=0.03)
        badge(ax, x + 0.62, 4.55, i + 1, color=color, r=0.3, size=11)
        txt(ax, x + 0.3, 3.75, wrap(title, 26), size=15.0, color=color,
            weight="bold", zorder=6)
        txt(ax, x + 0.3, 3.1, wrap(detail, 40), size=11.2, color=MUTED,
            zorder=6, spacing=1.2)
    if v.get("strip"):
        panel(ax, 0.6, 1.15, 14.8, 0.78, fill=tint(TEAL, 0.07),
              border=tint(TEAL, 0.3), radius=0.12, zorder=2)
        txt(ax, 0.95, 1.54, v["strip"], size=11.5, color="#BEEBE2",
            va="center", zorder=6)


DRAWERS = {
    "flow": draw_flow,
    "compare": draw_compare,
    "code": draw_code,
    "layers": draw_layers,
    "tree": draw_tree,
    "metrics": draw_metrics,
    "cycle": draw_cycle,
    "matrix": draw_matrix,
    "timeline": draw_timeline,
    "decision": draw_decision,
    "bullets": draw_bullets,
    "anatomy": draw_anatomy,
    "hero": draw_hero,
}


def render(concept, path, index, total):
    fig, ax = new_canvas(concept, index, total)
    payload = dict(concept["visual"])
    payload.setdefault("subtitle", concept["subtitle"])
    DRAWERS[payload["kind"]](ax, payload)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=170, facecolor=BG, edgecolor="none")
    plt.close(fig)
