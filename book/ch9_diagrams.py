"""Chapter 9 — scientific diagrams that accompany each introductory experiment (setup, principle, expected data)."""
import numpy as np

from common import (A, BLUE, GREEN, INK, INK2, LINE, MUTED, NAVY, ORANGE, PAPER, RED, SUN, SUN_DEEP, TITLE, Circ,
                    arabic_ticks, arrow, canvas, card, footer, halo, header, mirror_y, page, plt, save, style_axes,
                    sun_disk, wrap)
from eclipse2027 import besselian, circumstances as C, i18n as I

CH = 9
UTC = 3
B = besselian.elements()
LUXOR = ("الأقصر", 25.6872, 32.6396)
SKY = "#dfeaf7"
GROUND = "#d9c7a6"


def _sun_geometry():
    ts, eph = besselian.ephemeris()
    d = eph["earth"].at(ts.utc(2027, 8, 2, 10)).observe(eph["sun"]).distance().km
    return d, 2 * np.arcsin(696000 / d)  # distance (km), apparent diameter (rad)


SUN_DIST, SUN_ANG = _sun_geometry()


def _obscuration(la, lo, t):
    return np.array([float(C.instant(B, tt - besselian.T0_UT_HOURS, [la], [lo])["obscuration"][0]) for tt in t])


def _contacts(la, lo):
    r = C.local_circumstances(B, np.array([la]), np.array([lo]))
    return {k: float(np.ravel(v)[0]) for k, v in r.items()}


def lab(ax, x, y, text, size=9.5, color=INK, ha="center", va="center", bold=False, **kw):
    return ax.text(x, y, text, ha=ha, va=va, fontsize=size, color=color, fontweight="bold" if bold else "normal",
                   path_effects=halo(3), zorder=20, **kw)


def crescent(ax, x, y, r, dx, dy, z=5, sun=SUN, bg=PAPER, outline=True):
    """Partially eclipsed Sun: Sun disk with a Moon disk (background colour) offset by (dx, dy) in Sun radii."""
    s = sun_disk(ax, x, y, r, z=z, glow=False, color=sun)
    m = Circ(ax, (x + dx * r, y + dy * r * ax._asp), r * 1.03, fc=bg, ec=MUTED if outline else "none", lw=0.6,
             ls="--", zorder=z + 0.1)
    ax.add_patch(m)
    return s


def title_bar(ax, y, text, color=NAVY):
    ax.text(0.965, y, text, ha="right", va="center", fontsize=11.5, fontweight="bold", color=color, fontfamily=TITLE)


def principle_box(ax, x, y, w, h, title, text, width=60, fc="#f1efea"):
    """Card with a title and wrapped text; h is a minimum, the box grows upward to fit the text (y = bottom)."""
    hin = ax.get_position().height * ax.figure.get_figheight()
    body = wrap(text, width)
    lines = body.count("\n") + 1
    need = (0.78 + lines * 0.255) / hin
    h = max(h, need)
    card(ax, x, y, w, h, fc=fc, ec="none")
    ax.text(x + w - 0.015, y + h - 0.12 / hin, title, ha="right", va="top", fontsize=10.5, fontweight="bold", color=NAVY,
            fontfamily=TITLE)
    ax.text(x + w - 0.015, y + h - 0.45 / hin, body, ha="right", va="top", fontsize=9.4, linespacing=1.3)
    return h


# ------------------------------------------------------------------ 1 pinhole crescents
def diag_pinhole():
    fig = page(8.6, 7.4)
    ax = canvas(fig)
    header(fig, "مخطط التجربة ١: كيف يصنع الثقب صورة الشمس؟", "الثقب الصغير (Pinhole) يكوّن صورة مقلوبة للشمس نفسها، لا لشكل الثقب")
    y0 = 0.62
    ax.add_patch(plt.Rectangle((0.0, 0.40), 1, 0.40, fc="#f6f3ec", ec="none", zorder=0))
    # Sun (right), pinhole plate (middle), screen (left)
    xs, xp, xc = 0.86, 0.45, 0.22
    r = 0.07
    crescent(ax, xs, y0, r, -0.55, 0.35, bg="#f6f3ec")
    lab(ax, xs, y0 - 0.14, "الشمس المكسوفة جزئيًا\n(Partially eclipsed Sun)", 9)
    ax.plot([xp, xp], [0.45, y0 - 0.008], color=INK, lw=4, solid_capstyle="butt")
    ax.plot([xp, xp], [y0 + 0.008, 0.78], color=INK, lw=4, solid_capstyle="butt")
    lab(ax, xp, 0.80 - 0.0, "لوح فيه ثقب (Pinhole plate)", 9, va="bottom")
    ax.plot([xc, xc], [0.45, 0.78], color="#9aa6b8", lw=6)
    lab(ax, xc, 0.42, "الشاشة البيضاء (Screen)", 9, va="top")
    # rays: top of sun -> pinhole -> bottom of image, and vice versa
    hs = r * ax._asp
    k = (xp - xc) / (xs - xp)
    hi = hs * k * 1.0
    for sy, col in [(y0 + hs, SUN_DEEP), (y0 - hs, BLUE[9])]:
        iy = y0 - (sy - y0) * k
        ax.plot([xs, xp, xc], [sy, y0, iy], color=col, lw=1.2, zorder=3)
    ri = r * k
    crescent(ax, xc - ri - 0.01, y0, ri, 0.55, -0.35, bg="#f6f3ec")
    lab(ax, xc - 0.02, y0 + hi + 0.06, "صورة مقلوبة (Inverted image)", 8.8)
    arrow(ax, xc, 0.50, xp, 0.50, color=INK2, style="<|-|>", ms=10)
    lab(ax, (xc + xp) / 2, 0.525, "المسافة L", 9.5, bold=True)
    lab(ax, (xs + xp) / 2, y0 + 0.02, "θ ≈ " + A(f"{np.degrees(SUN_ANG):.2f}") + "°", 9.5, color=RED, bold=True)
    # table of image sizes
    title_bar(ax, 0.375, "قطر الصورة d = L × θ ≈ L ÷ " + A(f"{1 / SUN_ANG:.0f}"))
    Ls = [(0.5, "نصف متر"), (1.0, "متر"), (2.0, "متران"), (4.0, "٤ أمتار (ارتفاع شجرة)")]
    for i, (L, n) in enumerate(Ls):
        x = 0.83 - i * 0.235
        card(ax, x - 0.105, 0.245, 0.21, 0.10, fc="white")
        lab(ax, x, 0.32, n, 9.2, bold=True)
        lab(ax, x, 0.27, "d ≈ " + A(f"{L * SUN_ANG * 1000:.1f}") + " مم", 9.6, color=NAVY)
    principle_box(ax, 0.035, 0.02, 0.93, 0.15, "لماذا لا يظهر شكل الثقب؟",
                  "كل نقطة من قرص الشمس ترسل حزمة ضيقة عبر الثقب فترسم بقعة صغيرة على الشاشة، ومجموع هذه البقع يرسم الشمس كلها. "
                  "ويظهر شكل الثقب فقط إذا كان الثقب كبيرًا مقارنةً بالصورة؛ لذلك اجعل قطر الثقب أصغر من جزء من مئة من المسافة L.",
                  width=110)
    save(fig, CH, "diag_pinhole", "مخطط علمي لتجربة كاميرا الثقب: مسار الأشعة والصورة المقلوبة وقطر الصورة (محسوب).")


# ------------------------------------------------------------------ 2 temperature
def diag_temperature():
    name, la, lo = LUXOR
    t = np.linspace(8.4, 11.8, 700)
    ob = _obscuration(la, lo, t)
    # first-order thermal response: dT/dt = (T_eq - T)/tau, T_eq = T0 - A*ob
    tau, amp, T0 = 0.25, 5.0, 40.0
    T = np.empty_like(t)
    T[0] = T0
    for i in range(1, len(t)):
        dt = t[i] - t[i - 1]
        T[i] = T[i - 1] + dt * ((T0 - amp * ob[i]) - T[i - 1]) / tau
    c = _contacts(la, lo)
    fig = page(8.8, 6.8)
    ax = canvas(fig, (0.0, 0.0, 0.40, 0.86))
    header(fig, "مخطط التجربة ٢: قياس انخفاض الحرارة", "تجهيز علمي صحيح للقياس، والمنحنى المتوقع من نموذج مبسّط")
    ax.add_patch(plt.Rectangle((0.05, 0.10), 0.9, 0.05, fc=GROUND, ec="none"))
    lab(ax, 0.5, 0.075, "أرض مكشوفة بعيدة عن الجدران (Open ground)", 8.5)
    ax.plot([0.5, 0.5], [0.15, 0.55], color=INK2, lw=3)
    for k in range(6):
        ax.add_patch(plt.Rectangle((0.36, 0.55 + k * 0.035), 0.28, 0.022, fc="white", ec=INK2, lw=0.8))
    ax.add_patch(plt.Rectangle((0.47, 0.57), 0.06, 0.15, fc=RED, ec="none", alpha=0.85, zorder=3))
    lab(ax, 0.5, 0.80, "صندوق تهوية أبيض\n(Radiation shield)", 8.8, bold=True)
    lab(ax, 0.82, 0.64, "مقياس حرارة\n(Thermometer)", 8.4, color=RED)
    arrow(ax, 0.72, 0.64, 0.54, 0.64, color=RED, ms=8)
    arrow(ax, 0.16, 0.15, 0.16, 0.60, color=INK2, style="<|-|>", ms=9)
    lab(ax, 0.16, 0.38, A("1.5") + " م", 9, bold=True)
    sun_disk(ax, 0.88, 0.93, 0.045)
    ax2 = fig.add_axes([0.50, 0.33, 0.42, 0.45])
    ax2.plot(t + UTC, T, color=RED, lw=2.2, label="الحرارة المتوقعة (°م)")
    ax3 = ax2.twinx()
    ax3.fill_between(t + UTC, 0, ob * 100, color=BLUE[2], alpha=0.5)
    ax3.set_ylim(0, 300)
    ax3.set_yticks([])
    for s in ax3.spines.values():
        s.set_visible(False)
    imin = int(np.argmin(T))
    lag = (t[imin] - c["tmax"]) * 60
    ax2.annotate("أدنى حرارة بعد الذروة\nبنحو " + A(f"{lag:.0f}") + " دقيقة", (t[imin] + UTC, T[imin]),
                 xytext=(t[imin] + UTC + 0.35, T[imin] + 1.6), fontsize=8.6, arrowprops=dict(arrowstyle="-", color=INK2))
    ax2.axvline(c["tmax"] + UTC, color=NAVY, ls="--", lw=1)
    ax2.text(c["tmax"] + UTC - 0.03, T0 + 0.4, "ذروة الكسوف", ha="right", fontsize=8.4, color=NAVY)
    ax2.set_ylim(T0 - amp - 0.6, T0 + 1.0)
    xt = np.arange(11.5, 14.76, 0.5)
    ax2.set_xticks(xt)
    ax2.set_xticklabels([I.fmt_time(x, seconds=False) for x in xt], fontsize=8)
    ax2.set_ylabel("درجة الحرارة (°م) — Temperature")
    style_axes(ax2)
    arabic_ticks(ax2, x=False, fmt="{:.0f}")
    mirror_y(ax2)
    ax2.set_title(f"منحنى نموذجي في {name} (الأزرق: نسبة الاحتجاب)", fontsize=9.5)
    fig.text(0.965, 0.06, wrap("المتغير المستقل (Independent variable): نسبة احتجاب الشمس. المتغير التابع (Dependent variable): "
                                "درجة حرارة الهواء. ثبّت كل ما عداهما: المكان والارتفاع والظل. وقِس في اليوم السابق في الوقت نفسه "
                                "ليكون «يومًا ضابطًا» (Control day) تقارن به.", 70), ha="right", va="bottom", fontsize=9,
             linespacing=1.4)
    footer(fig, "نموذج توضيحي مبسّط: استجابة حرارية من الرتبة الأولى بثابت زمني ١٥ دقيقة وانخفاض أقصى ٥ °م؛ الاحتجاب محسوب من عناصر ناسا.")
    save(fig, CH, "diag_temperature", "مخطط علمي لتجربة قياس الحرارة: التجهيز والمنحنى المتوقع (نموذج مبسّط).")


# ------------------------------------------------------------------ 3 light meter
def diag_light():
    name, la, lo = LUXOR
    t = np.linspace(8.5, 11.6, 1200)
    ob = _obscuration(la, lo, t)
    E0 = 110000.0
    E = np.maximum(E0 * (1 - ob), 5.0)
    c = _contacts(la, lo)
    fig = page(8.8, 6.6)
    ax = canvas(fig, (0.0, 0.0, 0.36, 0.86))
    header(fig, "مخطط التجربة ٣: قياس الضوء بالهاتف", "الضوء يهبط آلاف المرات؛ لذلك يُرسم على مقياس لوغاريتمي (Logarithmic scale)")
    ax.plot([0.5, 0.5], [0.12, 0.50], color=INK2, lw=3)
    ax.plot([0.5, 0.30], [0.12, 0.02], color=INK2, lw=2)
    ax.plot([0.5, 0.70], [0.12, 0.02], color=INK2, lw=2)
    ax.add_patch(plt.Rectangle((0.33, 0.50), 0.34, 0.035, fc=INK, ec="none"))
    ax.add_patch(Circ(ax, (0.40, 0.535), 0.012, fc=SUN, ec=INK))
    lab(ax, 0.5, 0.60, "الهاتف مستلقٍ والحساس نحو السماء\n(Ambient light sensor up)", 8.6, bold=True)
    arrow(ax, 0.40, 0.66, 0.40, 0.86, color=BLUE[9])
    lab(ax, 0.40, 0.89, "سمت الرأس (Zenith)", 8.8, color=BLUE[9])
    lab(ax, 0.5, 0.30, "حامل ثابت\n(Tripod)", 8.6)
    ax2 = fig.add_axes([0.44, 0.15, 0.50, 0.62])
    ax2.semilogy(t + UTC, E, color=NAVY, lw=2.2)
    for v, txt in [(1e5, "شمس الظهيرة ≈ ١٠٠ ألف لوكس"), (500, "مكتب مضاء ≈ ٥٠٠ لوكس"), (10, "شفق مدني ≈ ١٠ لوكس")]:
        ax2.axhline(v, color=MUTED, ls=":", lw=1)
        ax2.text(8.55 + UTC, v * 1.25, txt, fontsize=8, color=INK2)
    i99 = int(np.argmin(np.abs(ob[: np.argmax(ob)] - 0.99)))
    ax2.plot(t[i99] + UTC, E[i99], "o", color=SUN_DEEP)
    ax2.annotate("احتجاب ٩٩٪ وما زال الضوء\n≈ " + A(f"{E[i99]:,.0f}") + " لوكس: لا تنزع النظارة!", (t[i99] + UTC, E[i99]),
                 xytext=(t[i99] + UTC - 1.15, E[i99] * 0.07), fontsize=8.4, color=SUN_DEEP,
                 arrowprops=dict(arrowstyle="-", color=SUN_DEEP))
    ax2.axvspan(c["c2"] + UTC, c["c3"] + UTC, color=NAVY, alpha=0.15)
    ax2.set_ylim(2, 3e5)
    xt = np.arange(11.5, 14.76, 0.5)
    ax2.set_xticks(xt)
    ax2.set_xticklabels([I.fmt_time(x, seconds=False) for x in xt], fontsize=8)
    ax2.set_ylabel("شدة الإضاءة (لوكس) — Illuminance (lux)")
    ax2.set_yticks([10, 100, 1000, 1e4, 1e5])
    ax2.set_yticklabels([A("10"), A("100"), A("1,000"), A("10,000"), A("100,000")])
    style_axes(ax2)
    mirror_y(ax2)
    ax2.set_title(f"المنحنى المتوقع في {name}", fontsize=9.5)
    footer(fig, "الإضاءة ∝ مساحة القرص الظاهرة (تقريب يهمل إظلام الأطراف)، وأثناء الكلية يبقى ضوء الأفق بضعة لوكسات. الاحتجاب محسوب.")
    save(fig, CH, "diag_light_meter", "مخطط علمي لتجربة قياس الضوء: وضع الهاتف والمنحنى اللوغاريتمي المتوقع (محسوب).")


# ------------------------------------------------------------------ 4 sharp shadows
def diag_shadows():
    fig = page(8.8, 6.8)
    ax = canvas(fig)
    header(fig, "مخطط التجربة ٤: لماذا تصبح الظلال حادة؟", "عرض شبه الظل (Penumbra) يتناسب مع حجم مصدر الضوء الظاهري")
    h = 0.30  # metres from pencil to paper
    for k, (ttl, src_w, note) in enumerate([("قبل الكسوف: قرص كامل", SUN_ANG, "Full disk"),
                                             ("قرب الكلية: هلال رفيع", SUN_ANG * 0.06, "Thin crescent")]):
        x0 = 0.74 - k * 0.48
        ax.add_patch(plt.Rectangle((x0 - 0.21, 0.30), 0.42, 0.53, fc="#f6f3ec", ec="none"))
        lab(ax, x0, 0.855, ttl + f" ({note})", 10, bold=True)
        wsrc = 0.16 if k == 0 else 0.012
        ax.add_patch(plt.Rectangle((x0 - wsrc / 2, 0.78), wsrc, 0.025, fc=SUN, ec=SUN_DEEP))
        ax.plot([x0 - 0.02, x0 + 0.06], [0.58, 0.58], color=INK, lw=5)
        lab(ax, x0 + 0.13, 0.58, "حافة القلم", 8.5)
        ax.plot([x0 - 0.20, x0 + 0.20], [0.34, 0.34], color=INK2, lw=2)
        for sx in (x0 - wsrc / 2, x0 + wsrc / 2):
            yy = 0.34
            ex = (x0 - 0.02) + ((x0 - 0.02) - sx) * (0.58 - yy) / (0.78 - 0.58)
            ax.plot([sx, x0 - 0.02, ex], [0.78, 0.58, yy], color=SUN_DEEP, lw=0.9)
        e1 = (x0 - 0.02) + ((x0 - 0.02) - (x0 - wsrc / 2)) * 0.24 / 0.20
        e2 = (x0 - 0.02) + ((x0 - 0.02) - (x0 + wsrc / 2)) * 0.24 / 0.20
        lo_, hi_ = min(e1, e2), max(e1, e2)
        ax.add_patch(plt.Rectangle((lo_, 0.325), hi_ - lo_, 0.03, fc="#9aa6b8", ec="none"))
        ax.add_patch(plt.Rectangle((hi_, 0.325), x0 + 0.20 - hi_, 0.03, fc=INK2, ec="none", alpha=0.35))
        w_mm = h * src_w * 1000
        lab(ax, x0, 0.27, "عرض شبه الظل ≈ " + A(f"{w_mm:.2f}") + " مم", 9.5, color=RED if k == 0 else GREEN, bold=True)
    lab(ax, 0.5, 0.235, "الظل الكامل (Umbra) رمادي داكن | شبه الظل (Penumbra) رمادي فاتح — القلم على ارتفاع "
        + A("30") + " سم من الورقة", 9)
    principle_box(ax, 0.035, 0.02, 0.93, 0.12, "العلاقة: عرض شبه الظل = الارتفاع h × القطر الزاوي للمصدر α",
                  "قبل الكسوف قطر الشمس الزاوي " + A(f"{np.degrees(SUN_ANG):.2f}") + "°، فتكون حافة الظل مشوّشة. وقرب الكلية "
                  "يصبح عرض الهلال جزءًا صغيرًا من ذلك، فيحدّ الظل في الاتجاه العمودي على الهلال بينما يبقى مشوّشًا على طوله.",
                  width=112)
    save(fig, CH, "diag_sharp_shadows", "مخطط علمي لتجربة الظلال: الظل الكامل وشبه الظل وعرضه حسب حجم المصدر (محسوب).")


# ------------------------------------------------------------------ 5 shadow bands
def diag_shadow_bands():
    fig = page(8.8, 6.8)
    ax = canvas(fig)
    header(fig, "مخطط التجربة ٥: رصد الأحزمة الظلية (Shadow Bands)", "تجهيز التصوير والقياس، وكيف يصنعها اضطراب الهواء")
    # right: physics
    ax.add_patch(plt.Rectangle((0.52, 0.28), 0.45, 0.58, fc=SKY, ec="none"))
    for k in range(5):
        x0 = 0.56 + k * 0.08
        ax.plot([x0 + 0.02, x0 + 0.05], [0.84, 0.30], color=SUN, lw=1.4, alpha=0.9)
    xx = np.linspace(0.53, 0.96, 200)
    for yy, a in [(0.62, 0.012), (0.58, 0.010)]:
        ax.plot(xx, yy + a * np.sin(xx * 70), color=BLUE[8], lw=1.4)
    lab(ax, 0.745, 0.67, "خلايا هواء مضطربة (Turbulence)", 8.8, color=BLUE[10], bold=True)
    lab(ax, 0.745, 0.86, "ضوء الهلال الرفيع قبل الكلية بدقيقة", 8.8)
    for k in range(7):
        ax.add_patch(plt.Rectangle((0.54 + k * 0.06, 0.29), 0.028, 0.03, fc="white" if k % 2 else "#c4cfde", ec="none"))
    lab(ax, 0.745, 0.35, "خطوط مضيئة وداكنة على الأرض", 8.8)
    # left: setup
    ax.add_patch(plt.Polygon([(0.06, 0.30), (0.44, 0.30), (0.40, 0.44), (0.10, 0.44)], fc="white", ec=INK2))
    for k in range(5):
        ax.plot([0.12 + k * 0.06, 0.15 + k * 0.06], [0.31, 0.43], color="#c4cfde", lw=3)
    lab(ax, 0.25, 0.285, "ملاءة بيضاء ٢×٢ م (White sheet)", 8.6)
    ax.plot([0.08, 0.38], [0.455, 0.455], color=SUN_DEEP, lw=3)
    lab(ax, 0.23, 0.48, "عصا متر للقياس (Meter stick)", 8.6, color=SUN_DEEP)
    ax.plot([0.34, 0.34], [0.46, 0.70], color=INK2, lw=2)
    ax.add_patch(plt.Rectangle((0.32, 0.70), 0.05, 0.03, fc=INK, ec="none"))
    lab(ax, 0.30, 0.78, "هاتف يصوّر فيديو\n(Video, 60 fps)", 8.6, bold=True)
    arrow(ax, 0.10, 0.60, 0.10, 0.70, color=RED, ms=9)
    lab(ax, 0.10, 0.73, "شمال", 8.6, color=RED)
    principle_box(ax, 0.035, 0.02, 0.93, 0.12, "ما الذي تقيسه؟",
                  "١) اتجاه الخطوط واتجاه حركتها بالنسبة إلى الشمال. ٢) المسافة بين خطين متجاورين بمقارنتها بعصا المتر في الفيديو. "
                  "٣) سرعتها: المسافة التي يقطعها خط بين إطارين ÷ زمن الإطار. الأحزمة باهتة جدًا وسريعة، والمسافة بينها عادةً عشرات "
                  "السنتيمترات وسرعتها أمتار قليلة في الثانية، وسببها وميض ضوء الهلال الرفيع في الهواء المضطرب كوميض النجوم.",
                  width=112)
    save(fig, CH, "diag_shadow_bands", "مخطط علمي لتجربة الأحزمة الظلية: التجهيز وآلية تكوّنها في الهواء المضطرب.")


# ------------------------------------------------------------------ 6 animal behaviour
def diag_animals():
    name, la, lo = LUXOR
    t = np.linspace(8.6, 11.6, 500)
    ob = _obscuration(la, lo, t)
    fig = page(8.8, 6.8)
    header(fig, "مخطط التجربة ٦: خطة رصد علمية لسلوك الحيوانات", "السؤال والفرضية والمتغيرات وورقة تسجيل منظمة")
    ax2 = fig.add_axes([0.06, 0.58, 0.84, 0.22])
    ax2.plot(t + UTC, (1 - ob) * 100, color=NAVY, lw=2)
    ax2.fill_between(t + UTC, 0, (1 - ob) * 100, color=BLUE[1], alpha=0.6)
    for a, b, lab_ in [(11.6, 12.6, "كل ١٠ دقائق"), (12.6, 13.3, "كل دقيقة"), (13.3, 14.4, "كل ١٠ دقائق")]:
        ax2.axvspan(a, b, color=SUN if lab_ == "كل دقيقة" else BLUE[0], alpha=0.25)
        ax2.text((a + b) / 2, 104, lab_, ha="center", fontsize=8.4)
    ax2.set_ylim(0, 115)
    ax2.set_ylabel("الضوء ٪", fontsize=8.5)
    xt = np.arange(11.5, 14.76, 0.5)
    ax2.set_xticks(xt)
    ax2.set_xticklabels([I.fmt_time(x, seconds=False) for x in xt], fontsize=8)
    style_axes(ax2)
    arabic_ticks(ax2, x=False, fmt="{:.0f}")
    mirror_y(ax2)
    ax = canvas(fig, (0, 0.04, 1, 0.48))
    boxes = [("السؤال (Question)", "هل تتصرف الطيور كأن الليل حلّ حين يخفت الضوء؟"),
             ("الفرضية (Hypothesis)", "تقل أصوات الطيور وتعود إلى أعشاشها قرب الكلية."),
             ("المتغيرات (Variables)", "المستقل: الضوء. التابع: عدد الأصوات والحركات. الضابط: المكان والراصد والوقت.")]
    for i, (h1, tx) in enumerate(boxes):
        x = 0.665 - i * 0.315
        principle_box(ax, x, 0.52, 0.30, 0.40, h1, tx, width=34, fc="#eef4fc")
    cols = ["الوقت (Time)", "الضوء ٪", "الأصوات/دقيقة", "الحركة (Activity)", "ملاحظات (Notes)"]
    xs = np.linspace(0.87, 0.13, len(cols))
    ax.add_patch(plt.Rectangle((0.04, 0.38), 0.92, 0.09, fc=NAVY, ec="none"))
    for x, cname in zip(xs, cols):
        ax.text(x, 0.425, cname, ha="center", va="center", fontsize=9, color="white", fontweight="bold")
    for r_ in range(3):
        y = 0.33 - r_ * 0.08
        ax.add_patch(plt.Rectangle((0.04, y - 0.04), 0.92, 0.08, fc="white" if r_ % 2 else "#f1efea", ec=LINE))
    ax.text(xs[0], 0.33, I.fmt_time(12.75, seconds=False), ha="center", va="center", fontsize=9, color=MUTED)
    ax.text(xs[1], 0.33, A("35"), ha="center", va="center", fontsize=9, color=MUTED)
    ax.text(xs[2], 0.33, A("12"), ha="center", va="center", fontsize=9, color=MUTED)
    ax.text(xs[3], 0.33, "تطير نحو الشجرة", ha="center", va="center", fontsize=9, color=MUTED)
    footer(fig, f"منحنى الضوء محسوب لمدينة {name}. كرّر الرصد في اليوم السابق في الوقت نفسه (يوم ضابط) لتفصل أثر الكسوف عن العادات اليومية.")
    save(fig, CH, "diag_animals", "مخطط علمي لتجربة سلوك الحيوانات: المنهج العلمي وجدول الرصد ومواعيد التسجيل (محسوب).")


# ------------------------------------------------------------------ 7 timing contacts
def diag_contacts():
    name, la, lo = LUXOR
    c = _contacts(la, lo)
    fig = page(8.8, 6.6)
    ax = canvas(fig)
    header(fig, f"مخطط التجربة ٧: توقيت التماسات الأربعة في {name}",
           "قارن رصدك (Observed) بالحساب (Calculated): الفرق O − C بالثانية")
    pts = [("c1", "التماس الأول C1", "بداية الكسوف الجزئي", -1.9), ("c2", "التماس الثاني C2", "بداية الكلية", -0.98),
           ("c3", "التماس الثالث C3", "نهاية الكلية", 0.98), ("c4", "التماس الرابع C4", "نهاية الكسوف", 1.9)]
    ax.plot([0.06, 0.94], [0.66, 0.66], color=LINE, lw=3)
    for i, (k, n, d, off) in enumerate(pts):
        x = 0.85 - i * 0.233
        r = 0.055
        ax.add_patch(Circ(ax, (x, 0.66), r, fc=SUN, ec="none", zorder=3))
        ax.add_patch(Circ(ax, (x + off * r, 0.66), r * 1.03, fc=NAVY, ec="none", zorder=4, alpha=0.88))
        lab(ax, x, 0.82, n, 9.8, bold=True)
        lab(ax, x, 0.775, d, 8.8, color=INK2)
        lab(ax, x, 0.54, I.fmt_time(c[k] + UTC), 11, color=RED, bold=True)
    lab(ax, 0.5, 0.48, "الأوقات المحسوبة بتوقيت مصر الصيفي (الراصد عند مستوى سطح البحر)", 8.8, color=INK2)
    cols = ["التماس", "الحساب C", "الرصد O", "O − C (ث)"]
    xs = [0.86, 0.64, 0.42, 0.18]
    ax.add_patch(plt.Rectangle((0.06, 0.36), 0.88, 0.065, fc=NAVY, ec="none"))
    for x, cn in zip(xs, cols):
        ax.text(x, 0.392, cn, ha="center", va="center", fontsize=9.5, color="white", fontweight="bold")
    for i, (k, n, d, off) in enumerate(pts):
        y = 0.32 - i * 0.055
        ax.add_patch(plt.Rectangle((0.06, y - 0.0275), 0.88, 0.055, fc="#f1efea" if i % 2 == 0 else "white", ec=LINE))
        ax.text(xs[0], y, n.split()[-1], ha="center", va="center", fontsize=9.5)
        ax.text(xs[1], y, I.fmt_time(c[k] + UTC), ha="center", va="center", fontsize=9.5)
        ax.text(xs[2], y, "……:……:……", ha="center", va="center", fontsize=9.5, color=MUTED)
    footer(fig, "نصيحة: صوّر الشمس بالفيديو (بمرشح) مع ساعة مضبوطة في الإطار، ثم استخرج اللحظة من الإطارات بدل الاعتماد على رد فعلك "
           "(نحو ٠٫٢–٠٫٣ ث).\n وتضاريس حافة القمر قد تغيّر التماسين الثاني والثالث ثانية أو ثانيتين.")
    save(fig, CH, "diag_contacts", f"مخطط علمي لتجربة توقيت التماسات في {name} مع جدول O − C (محسوب).")


# ------------------------------------------------------------------ 8 Sun size
def diag_sun_size():
    L = 1.0
    d_mm = L * SUN_ANG * 1000
    fig = page(8.8, 6.8)
    ax = canvas(fig)
    header(fig, "مخطط التجربة ٨: قياس قطر الشمس بالمثلثات المتشابهة", "Similar triangles: D ÷ R = d ÷ L")
    xs, xp, xi = 0.88, 0.40, 0.10
    ys, hs = 0.62, 0.20
    hi = 0.05
    ax.add_patch(plt.Polygon([(xs, ys + hs / 2), (xs, ys - hs / 2), (xp, ys)], fc=SUN, alpha=0.25, ec=SUN_DEEP))
    ax.add_patch(plt.Polygon([(xp, ys), (xi, ys + hi), (xi, ys - hi)], fc=BLUE[2], alpha=0.6, ec=BLUE[9]))
    ax.plot([xs, xs], [ys - hs / 2, ys + hs / 2], color=SUN_DEEP, lw=4)
    ax.plot([xi, xi], [ys - hi, ys + hi], color=BLUE[9], lw=4)
    ax.plot([xp, xp], [ys + 0.008, 0.80], color=INK, lw=4)
    ax.plot([xp, xp], [0.44, ys - 0.008], color=INK, lw=4)
    lab(ax, xs + 0.05, ys, "D", 13, bold=True, color=SUN_DEEP)
    lab(ax, xs, ys + hs / 2 + 0.05, "قطر الشمس (Sun diameter)", 8.8)
    lab(ax, xi - 0.04, ys, "d", 13, bold=True, color=BLUE[9])
    lab(ax, xi + 0.01, ys - hi - 0.07, "قطر الصورة\n(Image diameter)", 8.8)
    lab(ax, xp, 0.83, "الثقب (Pinhole)", 9)
    arrow(ax, xp + 0.01, 0.40, xs, 0.40, color=SUN_DEEP, style="<|-|>", ms=9)
    lab(ax, (xp + xs) / 2, 0.37, "R = بعد الشمس ≈ " + A(f"{SUN_DIST / 1e6:.1f}") + " مليون كم (٢ أغسطس ٢٠٢٧)", 8.8, color=SUN_DEEP)
    arrow(ax, xi, 0.40, xp - 0.01, 0.40, color=BLUE[9], style="<|-|>", ms=9)
    lab(ax, (xi + xp) / 2, 0.37, "L = طول الأنبوب", 8.8, color=BLUE[9])
    D = d_mm / 1000 / L * SUN_DIST
    steps = [("قِس", f"L = {A('1.00')} م ، d = {A(f'{d_mm:.1f}')} مم"),
             ("احسب القطر الزاوي", "θ = d ÷ L = " + A(f"{d_mm / 1000 / L:.5f}") + " راديان = " + A(f"{np.degrees(SUN_ANG):.3f}") + "°"),
             ("احسب قطر الشمس", "D = θ × R ≈ " + A(f"{D / 1e6:.2f}") + " مليون كم ≈ " + A(f"{D / 12742:.0f}") + " × قطر الأرض"),
             ("قدّر الخطأ", "خطأ ± ٠٫٥ مم في d يعني ± " + A(f"{0.5 / d_mm * 100:.0f}") + "٪ في النتيجة؛ أنبوب أطول يقلل الخطأ")]
    for i, (h1, tx) in enumerate(steps):
        y = 0.26 - i * 0.058
        ax.add_patch(Circ(ax, (0.94, y), 0.016, fc=NAVY))
        ax.text(0.94, y, A(i + 1), ha="center", va="center", color="white", fontsize=8.5)
        ax.text(0.91, y, h1 + ":", ha="right", va="center", fontsize=9.8, fontweight="bold", color=NAVY)
        ax.text(0.70, y, tx, ha="right", va="center", fontsize=9.8)
    footer(fig, "القيم المثالية محسوبة: القطر الظاهري للشمس يوم الكسوف وبُعدها من تقويم JPL DE421؛ قطر الشمس الحقيقي ١٫٣٩ مليون كم.")
    save(fig, CH, "diag_sun_size", "مخطط علمي لقياس قطر الشمس بكاميرا الثقب: المثلثات المتشابهة ومثال محلول (محسوب).")


DIAGRAMS = {"pinhole_crescents": diag_pinhole, "temperature_drop": diag_temperature, "light_meter": diag_light,
            "sharp_shadows": diag_shadows, "shadow_bands": diag_shadow_bands, "animal_behavior": diag_animals,
            "timing_contacts": diag_contacts, "sun_size": diag_sun_size}
