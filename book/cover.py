"""Full-page A4 cover for the Word edition (book/word/cover_full.jpg).

NASA corona photograph (public domain) as a full-bleed background, the computed path of totality over a map
on which Egypt is highlighted, and a drawn silhouette of the Luxor Temple pylon.
"""
import os

import numpy as np
from matplotlib import patheffects as pe
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle

import mapkit as MK
from common import ROOT, SUN, TITLE, plt
from eclipse2027 import besselian, circumstances as C

OUT = os.path.join(ROOT, "book", "word", "cover_full.jpg")
GOLD = "#f2b544"
LUXOR = (25.6996, 32.6390)        # Luxor Temple


def luxor_temple(ax, x0, y0, s, color="#0b0e14", edge=GOLD):
    """Silhouette of the Luxor Temple entrance: two pylon towers, gateway, obelisk and seated colossi."""
    kw = dict(fc=color, ec=edge, lw=1.1, zorder=20)
    # pylon towers (battered walls)
    for sgn in (-1, 1):
        xa, xb = x0 + sgn * 0.55 * s, x0 + sgn * 2.55 * s
        ax.add_patch(Polygon([(xa, y0), (xb, y0), (xb - sgn * 0.22 * s, y0 + 2.2 * s), (xa, y0 + 2.2 * s)], **kw))
        ax.add_patch(Rectangle((min(xa, xb - sgn * 0.22 * s), y0 + 2.2 * s), abs(xb - xa) - 0.22 * s, 0.12 * s, **kw))
    # gateway
    ax.add_patch(Rectangle((x0 - 0.55 * s, y0), 1.1 * s, 1.55 * s, fc=color, ec=edge, lw=1.1, zorder=19))
    ax.add_patch(Rectangle((x0 - 0.32 * s, y0), 0.64 * s, 1.1 * s, fc="#05070b", ec=edge, lw=0.8, zorder=21))
    # obelisk (left of the gate, as at Luxor)
    xo = x0 - 3.2 * s
    ax.add_patch(Polygon([(xo - 0.2 * s, y0), (xo + 0.2 * s, y0), (xo + 0.13 * s, y0 + 3.0 * s), (xo, y0 + 3.25 * s),
                          (xo - 0.13 * s, y0 + 3.0 * s)], **kw))
    # seated colossi in front of the towers
    for xc in (x0 - 1.15 * s, x0 + 1.15 * s):
        ax.add_patch(Rectangle((xc - 0.22 * s, y0), 0.44 * s, 0.55 * s, **kw))
        ax.add_patch(Rectangle((xc - 0.16 * s, y0 + 0.55 * s), 0.32 * s, 0.55 * s, **kw))
        ax.add_patch(Polygon([(xc - 0.13 * s, y0 + 1.1 * s), (xc + 0.13 * s, y0 + 1.1 * s), (xc, y0 + 1.35 * s)], **kw))
    # ground line
    ax.plot([x0 - 4.0 * s, x0 + 3.2 * s], [y0, y0], color=edge, lw=1.3, zorder=21)


def main():
    W, H = 8.27, 11.69                                   # A4 in inches
    fig = plt.figure(figsize=(W, H), facecolor="#000000")
    # ---- full-bleed NASA corona photograph
    img = plt.imread(os.path.join(ROOT, "data", "nasa_images", "corona.jpg")).astype(float) / 255.0
    h, w = img.shape[:2]
    cw = int(h * W / H)                                  # portrait crop around the Moon
    x0 = (w - cw) // 2
    img = img[:, x0:x0 + cw]
    yy = np.linspace(0, 1, img.shape[0])[:, None, None]
    img = img * np.clip(1.15 - 0.55 * yy, 0, 1)         # darker towards the bottom for the map
    bg = fig.add_axes([0, 0, 1, 1])
    bg.imshow(img, extent=(0, 1, 0, 1), aspect="auto")
    bg.set_xlim(0, 1)
    bg.set_ylim(0, 1)
    bg.axis("off")
    halo = [pe.withStroke(linewidth=5, foreground="#000000")]
    # ---- title block
    fig.text(0.5, 0.955, "كسوف القرن", ha="center", va="top", color="white", fontsize=50, fontweight="bold",
             fontfamily=TITLE, path_effects=halo)
    fig.text(0.5, 0.875, "٢ أغسطس ٢٠٢٧", ha="center", va="top", color=GOLD, fontsize=30, fontweight="bold",
             fontfamily=TITLE, path_effects=halo)
    fig.text(0.5, 0.825, "دليل علمي مصوّر بالخرائط لكسوف أغسطس ٢٠٢٧", ha="center", va="top", color="#eef2f7",
             fontsize=17, path_effects=halo)
    # ---- map panel: path of totality, Egypt highlighted, Luxor
    B = besselian.elements()
    lon0, lon1, lat0, lat1 = 17.0, 43.0, 21.0, 32.8
    card = fig.add_axes([0.05, 0.085, 0.90, 0.33])
    card.axis("off")
    card.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.03", fc="#05080f", ec=GOLD,
                                  lw=1.2, alpha=0.82, transform=card.transAxes))
    ax = fig.add_axes([0.07, 0.10, 0.86, 0.30])
    countries = MK.geo("countries_region")
    ax.set_facecolor("#0d1a2b")
    countries.plot(ax=ax, color="#26303d", edgecolor="#55606e", linewidth=0.5)
    countries = countries.cx[lon0 - 3:lon1 + 3, lat0 - 3:lat1 + 3]
    egy = countries[countries["ADM0_A3"] == "EGY"]
    egy.plot(ax=ax, color="#c99a3a", edgecolor=GOLD, linewidth=1.6, zorder=3)
    t = np.linspace(-1.4, 1.6, 900)
    la, lo, ln, on, ls, os_ = C.path_limits(B, t)
    ok = np.isfinite(on) & np.isfinite(os_)
    ax.fill(np.r_[on[ok], os_[ok][::-1]], np.r_[ln[ok], ls[ok][::-1]], color="#0a0a0a", alpha=0.62, zorder=4, lw=0)
    ax.plot(on[ok], ln[ok], color="white", lw=0.8, zorder=5)
    ax.plot(os_[ok], ls[ok], color="white", lw=0.8, zorder=5)
    ax.plot(lo, la, color="#ff5a4a", lw=1.4, ls=(0, (5, 3)), zorder=5)
    ax.set_xlim(lon0, lon1)
    ax.set_ylim(lat0, lat1)
    ax.set_aspect(1 / np.cos(np.radians(27)))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.plot(LUXOR[1], LUXOR[0], marker="*", ms=17, color=GOLD, mec="black", zorder=8)
    tx = dict(color="white", fontsize=12, fontweight="bold", path_effects=halo, zorder=9)
    ax.text(LUXOR[1] + 0.35, LUXOR[0] - 0.05, "الأقصر  ٦ د ٢٠ ث", ha="left", va="center", **tx)
    ax.text(29.6, 26.6, "مصر", ha="center", va="center", color="#1a1205", fontsize=26, fontweight="bold",
            fontfamily=TITLE, zorder=7)
    ax.text(21.5, 30.0, "مسار الكلية", ha="center", va="center", color="white", fontsize=11, rotation=-22,
            path_effects=halo, zorder=9)
    # Luxor Temple silhouette, large, on the right of the map with a pointer to Luxor
    tax = fig.add_axes([0.66, 0.11, 0.27, 0.13])
    tax.set_xlim(-4.3, 3.4)
    tax.set_ylim(-0.3, 3.6)
    tax.set_aspect("equal")
    tax.axis("off")
    luxor_temple(tax, 0, 0, 1.0)
    tax.text(-0.4, 3.45, "معبد الأقصر", ha="center", va="bottom", color=GOLD, fontsize=13, fontweight="bold",
             path_effects=halo, zorder=22)
    ax.annotate("", (LUXOR[1] + 0.25, LUXOR[0] - 0.25), xytext=(37.4, 23.9),
                arrowprops=dict(arrowstyle="-", color=GOLD, lw=1.0, ls=(0, (2, 2))), zorder=8)
    # ---- facts line and credit
    facts = "أطول كلية ٦ دقائق و٢٣ ثانية  •  الشمس على ارتفاع ٨٢° فوق الصعيد  •  عرض المسار ٢٥٩ كم"
    fig.text(0.5, 0.055, facts, ha="center", va="center", color=GOLD, fontsize=12.5, fontweight="bold", path_effects=halo)
    fig.text(0.5, 0.025, "الخلفية: هالة الشمس في كسوف ٢٠١٧ — NASA/Aubrey Gemignani | المسار محسوب من عناصر ناسا",
             ha="center", va="center", color="#8a96a8", fontsize=7.5)
    fig.savefig(OUT, dpi=150, facecolor="#000000")
    plt.close(fig)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
