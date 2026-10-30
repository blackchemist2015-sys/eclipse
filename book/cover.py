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
    fig.text(0.5, 0.875, "٢ أغسطس ٢٠٢٧", ha="center", va="top", color="#ff4d3d", fontsize=30, fontweight="bold",
             fontfamily=TITLE, path_effects=halo)
    fig.text(0.5, 0.825, "دليل علمي مصوّر بالخرائط لكسوف أغسطس ٢٠٢٧", ha="center", va="top", color="#9ec5f4",
             fontsize=17, path_effects=halo)
    # ---- large map rendered separately, then blended into the photograph with a soft top fade
    B = besselian.elements()
    MX0, MX1, MY0, MY1 = 0.0, 1.0, 0.06, 0.60              # page area of the map
    mw, mh = W * (MX1 - MX0), H * (MY1 - MY0)
    lat0, lat1 = 20.3, 33.6
    lon_span = mw / mh * (lat1 - lat0) / np.cos(np.radians(27))
    lon0, lon1 = 31.0 - lon_span / 2, 31.0 + lon_span / 2
    mf = plt.figure(figsize=(mw, mh), dpi=150)
    mf.patch.set_alpha(0)
    ax = mf.add_axes([0, 0, 1, 1])
    ax.patch.set_alpha(0)
    countries = MK.geo("countries_region").cx[lon0 - 3:lon1 + 3, lat0 - 3:lat1 + 3]
    countries.plot(ax=ax, color="#10233f", edgecolor="#5d7aa3", linewidth=0.6, alpha=0.72)
    egy = countries[countries["ADM0_A3"] == "EGY"]
    egy.plot(ax=ax, color="#d9a441", edgecolor=GOLD, linewidth=2.0, alpha=0.88, zorder=3)
    t = np.linspace(-1.4, 1.6, 900)
    la, lo, ln, on, ls, os_ = C.path_limits(B, t)
    ok = np.isfinite(on) & np.isfinite(os_)
    ax.fill(np.r_[on[ok], os_[ok][::-1]], np.r_[ln[ok], ls[ok][::-1]], color="#2a78d6", alpha=0.42, zorder=4, lw=0)
    ax.plot(on[ok], ln[ok], color="#8fc0ff", lw=1.4, zorder=5)
    ax.plot(os_[ok], ls[ok], color="#8fc0ff", lw=1.4, zorder=5)
    ax.plot(lo, la, color="#ff3b30", lw=2.2, ls=(0, (6, 3)), zorder=5)
    ax.set_xlim(lon0, lon1)
    ax.set_ylim(lat0, lat1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.plot(LUXOR[1], LUXOR[0], marker="*", ms=24, color="#ff3b30", mec="white", mew=1.2, zorder=8)
    tx = dict(color="white", fontsize=15, fontweight="bold", path_effects=halo, zorder=9)
    ax.text(LUXOR[1] - 0.45, LUXOR[0] + 0.05, "الأقصر  ٦ د ٢٠ ث", ha="right", va="center", **tx)
    ax.text(29.0, 27.6, "مصر", ha="center", va="center", color="#2a1a04", fontsize=40, fontweight="bold",
            fontfamily=TITLE, zorder=7)
    k = int(np.nanargmin(np.abs(lo - 24.6)))
    ax.text(24.6, la[k] + 0.55, "مسار الكسوف الكلي", ha="center", va="bottom", color="#cfe3ff", fontsize=14,
            fontweight="bold", rotation=-24, path_effects=halo, zorder=9)
    mf.canvas.draw()
    rgba = np.asarray(mf.canvas.buffer_rgba()).astype(float) / 255.0
    plt.close(mf)
    ramp = np.clip(np.linspace(0, 1, rgba.shape[0]) / 0.28, 0, 1)[:, None]   # fade in over the top 28 %
    rgba[..., 3] *= ramp
    bg.imshow(rgba, extent=(MX0, MX1, MY0, MY1), aspect="auto", zorder=5)
    # Luxor Temple silhouette on the right, pointing to Luxor
    tax = fig.add_axes([0.66, 0.085, 0.30, 0.14])
    tax.set_xlim(-4.3, 3.4)
    tax.set_ylim(-0.3, 3.6)
    tax.set_aspect("equal")
    tax.axis("off")
    luxor_temple(tax, 0, 0, 1.0, color="#0b1426")
    tax.text(-0.4, 3.45, "معبد الأقصر", ha="center", va="bottom", color=GOLD, fontsize=14, fontweight="bold",
             path_effects=halo, zorder=22)
    # ---- facts line and credit
    facts = "أطول كلية ٦ دقائق و٢٣ ثانية  •  الشمس على ارتفاع ٨٢° فوق الصعيد  •  عرض المسار ٢٥٩ كم"
    fig.text(0.5, 0.05, facts, ha="center", va="center", color=GOLD, fontsize=12.5, fontweight="bold", path_effects=halo)
    fig.text(0.5, 0.025, "الخلفية: هالة الشمس في كسوف ٢٠١٧ — NASA/Aubrey Gemignani | المسار محسوب من عناصر ناسا",
             ha="center", va="center", color="#8a96a8", fontsize=7.5)
    fig.savefig(OUT, dpi=150, facecolor="#000000")
    plt.close(fig)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
