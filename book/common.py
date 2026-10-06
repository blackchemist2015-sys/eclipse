"""Shared design system for the Arabic book graphics.

Every figure is drawn with matplotlib (>= 3.11, which shapes Arabic and
applies the bidi algorithm natively) at print resolution, and registered in
a catalogue (figure number, Arabic caption, file) used to build the index.
"""
import json
import os
import sys
import textwrap

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
os.environ.setdefault("ECLIPSE_LANG", "ar")

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import patheffects as pe  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle, Wedge, Ellipse, Polygon as MPoly  # noqa: E402,F401

from eclipse2027 import i18n as I  # noqa: E402

I.set_lang("ar")
I.load_fonts()

OUT = os.path.join(ROOT, "book", "figures")
DPI = 220

# ----------------------------------------------------------------- palette
NAVY = "#0f1b2d"       # night sky / totality
NAVY2 = "#1b2c47"
SUN = "#f7b733"        # photosphere
SUN_DEEP = "#e88a2c"
CORONA = "#e9f1ff"
RED = "#b3261e"        # warnings / central line
GREEN = "#1f7a4d"      # safe
INK, INK2, MUTED = "#1f1f1d", "#4a4a46", "#8a8984"
PAPER = "#fbfaf7"
CARD = "#ffffff"
LINE = "#e4e2dc"
BLUE = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
        "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
ORANGE = ["#fdf1e4", "#fbe1c4", "#f8cf9f", "#f4ba78", "#efa351", "#e88a2c", "#d4711a", "#b55a12"]
CAT = ["#2a78d6", "#e88a2c", "#1f7a4d", "#b3261e", "#7a4fc2", "#6d6d68"]

TITLE = I.AR_TITLE_FONT
BODY = I.AR_BODY_FONT
SANS = I.AR_FONT

plt.rcParams.update({
    "font.family": SANS, "font.size": 10, "axes.edgecolor": MUTED, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 100,
})

A = I.ar_digits          # Eastern Arabic digits


CATALOGUE = []
_counters = {}

CHAPTERS = {
    1: "الأساس العلمي للكسوف",
    2: "الكسوف في تاريخ مصر",
    3: "كسوف ٢ أغسطس ٢٠٢٧",
    4: "الرصد الآمن",
    5: "تصوير الكسوف",
    6: "خرائط إضافية",
}


# ----------------------------------------------------------------- page scaffolding
def page(w=8.0, h=5.6, bg=PAPER):
    fig = plt.figure(figsize=(w, h), facecolor=bg)
    return fig


def header(fig, title, subtitle=None, y=0.965, size=17, color=INK, sub_color=INK2):
    fig.text(0.965, y, title, ha="right", va="top", fontfamily=TITLE, fontweight="bold", fontsize=size, color=color)
    if subtitle:
        fig.text(0.965, y - 0.065 * 5.6 / fig.get_figheight() * (size / 17) - 0.005, subtitle, ha="right", va="top",
                 fontfamily=BODY, fontsize=size * 0.62, color=sub_color)


def footer(fig, note="", color=MUTED):
    if note:
        fig.text(0.965, 0.018, note, ha="right", va="bottom", fontsize=7.2, color=color, fontfamily=SANS)


def wrap(text, width):
    """Wrap Arabic text by characters (logical order); each line is shaped separately."""
    out = []
    for para in text.split("\n"):
        out.extend(textwrap.wrap(para, width) or [""])
    return "\n".join(out)


def para(fig_or_ax, x, y, text, width=60, size=10.5, color=INK, family=None, transform=None, ha="right",
         va="top", linespacing=1.6, **kw):
    target = fig_or_ax
    tr = transform or (target.transFigure if hasattr(target, "transFigure") else target.transAxes)
    return target.text(x, y, wrap(text, width), ha=ha, va=va, fontsize=size, color=color,
                       fontfamily=family or BODY, transform=tr, linespacing=linespacing,
                       multialignment="right" if ha != "center" else "center", **kw)


def card(ax, x, y, w, h, fc=CARD, ec=LINE, lw=1.0, r=0.02, z=1, alpha=1.0):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw,
                       transform=ax.transAxes, zorder=z, alpha=alpha)
    ax.add_patch(p)
    return p


def canvas(fig, rect=(0, 0, 1, 1)):
    ax = fig.add_axes(rect)
    w, h = fig.get_size_inches()
    ax._asp = (w * rect[2]) / (h * rect[3])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return ax


def asp(ax):
    return getattr(ax, "_asp", 1.0)


def Circ(ax, xy, r, **kw):
    """A true circle on a canvas whose x and y units differ (axes fraction on a non-square figure)."""
    return Ellipse(xy, 2 * r, 2 * r * asp(ax), **kw)


def halo(w=2.5, c="white"):
    return [pe.withStroke(linewidth=w, foreground=c)]


def save(fig, chapter, slug, caption, kind="infographic"):
    n = _counters.get(chapter, 0) + 1
    _counters[chapter] = n
    d = os.path.join(OUT, f"ch{chapter}")
    os.makedirs(d, exist_ok=True)
    fname = f"fig_{chapter}_{n:02d}_{slug}.png"
    path = os.path.join(d, fname)
    fig.savefig(path, dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)
    CATALOGUE.append(dict(chapter=chapter, number=f"{chapter}-{n}", number_ar=A(f"{n}") + "-" + A(f"{chapter}"),
                          file=os.path.relpath(path, os.path.join(ROOT, "book")), caption=caption, kind=kind))
    print(f"[{chapter}-{n}] {fname}")
    return path


def write_catalogue(name):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"catalogue_{name}.json"), "w", encoding="utf-8") as f:
        json.dump(CATALOGUE, f, ensure_ascii=False, indent=1)


# ----------------------------------------------------------------- drawing kit
def sun_disk(ax, x, y, r, z=3, glow=True, color=SUN):
    if glow:
        for k, a in [(1.5, 0.10), (1.25, 0.18)]:
            ax.add_patch(Circ(ax, (x, y), r * k, fc=color, ec="none", alpha=a, zorder=z - 0.5))
    c = Circ(ax, (x, y), r, fc=color, ec="none", zorder=z)
    ax.add_patch(c)
    return c


def moon_disk(ax, x, y, r, z=4, color=NAVY, clip=None, ec="none"):
    c = Circ(ax, (x, y), r, fc=color, ec=ec, zorder=z)
    ax.add_patch(c)
    if clip is not None:
        c.set_clip_path(clip)
    return c


def corona(ax, x, y, r, z=2, seed=3, n=26, color=CORONA, strength=1.0, extent=1.0):
    """Procedural corona: soft glow plus tapered streamers (extent scales the outer glow and streamers)."""
    rng = np.random.default_rng(seed)
    for k, a in [(3.2, 0.05), (2.4, 0.08), (1.8, 0.14), (1.35, 0.30), (1.12, 0.55)]:
        k = 1 + (k - 1) * extent
        ax.add_patch(Circ(ax, (x, y), r * k, fc=color, ec="none", alpha=a * strength, zorder=z))
    for i in range(n):
        ang = rng.uniform(0, 2 * np.pi)
        # streamers concentrate near the solar equator (horizontal) at solar maximum-ish
        if rng.random() < 0.6:
            ang = rng.choice([0, np.pi]) + rng.normal(0, 0.45)
        L = r * (1 + rng.uniform(0.6, 2.6) * extent)
        wdt = rng.uniform(0.10, 0.28)
        a0 = ang - wdt / 2
        a1 = ang + wdt / 2
        k = asp(ax)
        pts = [(x + r * np.cos(a0), y + k * r * np.sin(a0)), (x + L * np.cos(ang), y + k * L * np.sin(ang)),
               (x + r * np.cos(a1), y + k * r * np.sin(a1))]
        ax.add_patch(MPoly(pts, closed=True, fc=color, ec="none", alpha=0.10 * strength, zorder=z))


def prominences(ax, x, y, r, z=5, seed=1, n=5):
    rng = np.random.default_rng(seed)
    for _ in range(n):
        ang = rng.uniform(0, 2 * np.pi)
        h = r * rng.uniform(0.04, 0.10)
        w = rng.uniform(0.05, 0.12)
        th = np.linspace(ang - w, ang + w, 20)
        rr = r + h * np.sin(np.linspace(0, np.pi, 20))
        k = asp(ax)
        ax.fill(np.r_[x + r * np.cos(th), (x + rr * np.cos(th))[::-1]],
                np.r_[y + k * r * np.sin(th), (y + k * rr * np.sin(th))[::-1]], color="#ff4d6d", alpha=0.9, zorder=z, lw=0)


def check_icon(ax, x, y, s=0.03, ok=True, z=6, transform=None):
    tr = transform or ax.transAxes
    ax.add_patch(Circ(ax, (x, y), s, fc=GREEN if ok else RED, ec="white", lw=1.5, zorder=z, transform=tr))
    ax.text(x, y, "✓" if ok else "✗", ha="center", va="center", color="white", fontsize=s * 420,
            fontfamily=["DejaVu Sans"], fontweight="bold", zorder=z + 1, transform=tr)


def arrow(ax, x0, y0, x1, y1, color=INK2, lw=1.4, z=5, style="-|>", ms=12, transform=None, **kw):
    from matplotlib.patches import FancyArrowPatch
    a = FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style, mutation_scale=ms, color=color, lw=lw, zorder=z,
                        transform=transform or ax.transAxes, **kw)
    ax.add_patch(a)
    return a


def number_badge(ax, x, y, n, color=BLUE[8], r=0.022, z=6):
    ax.add_patch(Circ(ax, (x, y), r, fc=color, ec="white", lw=1.2, zorder=z, transform=ax.transAxes))
    ax.text(x, y, A(n), ha="center", va="center", color="white", fontsize=r * 480, fontweight="bold",
            zorder=z + 1, transform=ax.transAxes, fontfamily=SANS)


def eclipse_phase(ax, x, y, r, f, z=3, sky=NAVY, total_corona=True, seed=3):
    """Draw the Sun at phase f in [-1, 1]: -1/1 = no overlap, 0 = centred (total)."""
    sun = sun_disk(ax, x, y, r, z=z, glow=abs(f) > 0.02)
    if abs(f) < 0.02 and total_corona:
        corona(ax, x, y, r, z=z - 1, seed=seed)
    moon_disk(ax, x + f * 2.05 * r, y + f * 0.35 * r * asp(ax), r * 1.03, z=z + 0.5, color=sky, clip=sun)
    return sun


def style_axes(ax, grid=True):
    ax.grid(grid, color=LINE, lw=0.7)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=9)


def arabic_ticks(ax, x=True, y=True, fmt="{:g}"):
    if x:
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: A(fmt.format(v)).replace("-", "−")))
    if y:
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: A(fmt.format(v)).replace("-", "−")))


def mirror_y(ax):
    """Put the y axis on the right, as Arabic readers expect."""
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.spines["right"].set_visible(True)
    ax.spines["left"].set_visible(False)
