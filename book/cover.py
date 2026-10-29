"""Full-page A4 cover for the Word edition (book/word/cover_full.jpg)."""
import os

import numpy as np

from common import A, NAVY, ROOT, SUN, TITLE, plt

OUT = os.path.join(ROOT, "book", "word", "cover_full.jpg")


def main():
    W, H = 8.27, 11.69                       # A4 in inches
    fig = plt.figure(figsize=(W, H), facecolor="#000000")
    # background: NASA corona photograph (public domain), darkened towards the edges
    img = plt.imread(os.path.join(ROOT, "data", "nasa_images", "corona.jpg")).astype(float) / 255.0
    h, w = img.shape[:2]
    side = min(h, w)
    img = img[(h - side) // 2:(h + side) // 2, (w - side) // 2:(w + side) // 2]
    yy, xx = np.mgrid[-1:1:complex(0, side), -1:1:complex(0, side)]
    vign = (np.clip(1.25 - 0.75 * np.hypot(xx, yy), 0, 1) * np.clip(0.55 + 1.2 * (yy + 0.55), 0, 1))[..., None]
    ax = fig.add_axes([-0.06, 0.10, 1.12, 1.12 * W / H])
    ax.imshow(img * vign)
    ax.axis("off")
    # title block
    fig.text(0.92, 0.935, "الكسوف الكلي للشمس", ha="right", va="top", color="white", fontsize=40, fontweight="bold",
             fontfamily=TITLE)
    fig.text(0.92, 0.865, "٢ أغسطس ٢٠٢٧", ha="right", va="top", color=SUN, fontsize=34, fontweight="bold", fontfamily=TITLE)
    fig.text(0.92, 0.815, "دليل علمي مصوّر لمصر والعالم العربي", ha="right", va="top", color="#e6ebf2", fontsize=16,
             path_effects=[__import__("matplotlib.patheffects").patheffects.withStroke(linewidth=4, foreground="#05080f")])
    # band with key numbers
    band = fig.add_axes([0, 0.07, 1, 0.13])
    band.set_facecolor(NAVY)
    band.set_xticks([])
    band.set_yticks([])
    for s in band.spines.values():
        s.set_visible(False)
    facts = [("٦ د ٢٣ ث", "أطول مدة للكلية"), ("٢٥٩ كم", "أقصى عرض للمسار"), ("٨٢°", "ارتفاع الشمس فوق صعيد مصر"),
             (A(280) + "+", "إنفوجرافيك وخريطة")]
    for k, (big, small) in enumerate(facts):
        x = 0.875 - k * 0.25
        band.text(x, 0.62, big, ha="center", va="center", color=SUN, fontsize=20, fontweight="bold", fontfamily=TITLE,
                  transform=band.transAxes)
        band.text(x, 0.25, small, ha="center", va="center", color="white", fontsize=10, transform=band.transAxes)
    fig.text(0.5, 0.035, "خرائط محسوبة • تاريخ الكسوف في مصر • الرصد الآمن • التصوير • تجارب علمية",
             ha="center", va="center", color="#9aa6b8", fontsize=11)
    fig.text(0.5, 0.012, "صورة الغلاف: هالة الشمس في كسوف ٢٠١٧ — NASA/Aubrey Gemignani", ha="center", va="center",
             color="#6c7d99", fontsize=7)
    fig.savefig(OUT, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
