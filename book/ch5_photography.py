"""Chapter 5 — photographing the eclipse (Arabic infographics, computed tables)."""
import numpy as np

from ch4_observing import list_card as _list_card
from common import (A, BLUE, BODY, CARD, Circ, GREEN, INK, INK2, LINE, MUTED, NAVY, ORANGE, PAPER, RED, SUN, SUN_DEEP,
                    TITLE, arabic_ticks, canvas, card, corona, footer, halo, header, mirror_y, moon_disk, number_badge,
                    page, para, plt, save, style_axes, sun_disk, wrap, write_catalogue)
from eclipse2027 import besselian, circumstances as C, i18n as I

CH = 5
UTC = 3
B = besselian.compute()

# Espenak's brightness exponents Q for eclipse phenomena (NASA eclipse bulletins)
Q = [("جزئي (مرشح ND 5.0)", 8), ("جزئي (مرشح ND 4.0)", 11), ("حبات بيلي", 12), ("الكروموسفير", 10),
     ("الألسنة الشمسية", 9), ("الهالة ٠٫١ نصف قطر", 7), ("الهالة ٠٫٢ نصف قطر", 5), ("الهالة ٠٫٥ نصف قطر", 3),
     ("الهالة ١٫٠ نصف قطر", 1), ("الهالة ٢٫٠ نصف قطر", 0), ("الهالة ٤٫٠ أنصاف أقطار", -1), ("الهالة ٨٫٠ أنصاف أقطار", -3),
     ("ضوء الأرض على القمر", -11)]
SHUTTERS = [1 / 8000, 1 / 4000, 1 / 2000, 1 / 1000, 1 / 500, 1 / 250, 1 / 125, 1 / 60, 1 / 30, 1 / 15, 1 / 8, 1 / 4,
            1 / 2, 1, 2, 4, 8, 15, 30]


def shutter_label(t):
    s = min(SHUTTERS, key=lambda x: abs(np.log(x / t)))
    return ("١/" + A(int(round(1 / s)))) if s < 1 else (A(int(s)) + " ث")


def list_card(*a, **k):
    import ch4_observing
    ch4_observing.CH = CH
    _list_card(*a, **k)


def fig_exposure_table(fnum):
    isos = [100, 200, 400, 800, 1600]
    fig = page(8.6, 7.4)
    ax = canvas(fig)
    header(fig, f"جدول التعريض للكسوف عند الفتحة \u2066f/{fnum:g}\u2069",
           "زمن الغالق المقترح لكل ظاهرة وحساسية (ISO) — صوّر بلقطات متعددة حول هذه القيم")
    xs = [0.95] + list(np.linspace(0.62, 0.10, len(isos)))
    y0 = 0.84
    ax.text(xs[0], y0, "الظاهرة", ha="right", fontsize=10.5, fontweight="bold", color=BLUE[10])
    for x, iso in zip(xs[1:], isos):
        ax.text(x, y0, "ISO " + A(iso), ha="center", fontsize=10.5, fontweight="bold", color=BLUE[10])
    for i, (name, q) in enumerate(Q):
        y = y0 - 0.058 * (i + 1)
        if i % 2 == 0:
            ax.add_patch(plt.Rectangle((0.03, y - 0.026), 0.94, 0.052, fc="#f1efea", ec="none", transform=ax.transAxes))
        filt = "جزئي" in name
        ax.text(xs[0], y, name, ha="right", va="center", fontsize=9.6, color=SUN_DEEP if filt else INK)
        for x, iso in zip(xs[1:], isos):
            t = fnum ** 2 / (iso * 2 ** q)
            ax.text(x, y, shutter_label(t), ha="center", va="center", fontsize=9.8)
    footer(fig, "المعادلة: الزمن = (رقم الفتحة)² ÷ (ISO × ٢^Q)، وقيم Q من نشرات الكسوف لإسبيناك (ناسا). الصفان الأولان بمرشح شمسي فقط.")
    save(fig, CH, f"exposure_table_f{int(fnum * 10)}", f"جدول أزمنة التعريض المقترحة لظواهر الكسوف عند الفتحة \u2066f/{fnum:g}\u2069 (محسوب).", "chart")


def fig_brightness_ladder():
    fig = page(8.4, 5.6)
    header(fig, "سلّم السطوع: من الهلال إلى الهالة الخارجية", "كل درجة في Q تعني ضعف السطوع؛ الفرق بين الحبات والهالة الخارجية ≈ ٣٢ ألف ضعف")
    ax = fig.add_axes([0.06, 0.08, 0.58, 0.74])
    items = Q[2:]
    ys = np.arange(len(items))
    ax.barh(ys, [q + 12 for _, q in items], color=[SUN_DEEP if q >= 9 else BLUE[8 - min(7, max(0, (5 - q) // 2))] for _, q in items],
            height=0.6)
    ax.set_yticks(ys)
    ax.set_yticklabels([n for n, _ in items], fontsize=9.6)
    ax.yaxis.tick_right()
    ax.invert_xaxis()
    for y, (_, q) in zip(ys, items):
        ax.text(q + 12.2, y, "Q = " + A(q).replace("-", "−"), va="center", ha="right", fontsize=8.6)
    ax.set_xticks([])
    style_axes(ax, grid=False)
    ax.spines["bottom"].set_visible(False)
    footer(fig, "قيم Q من جداول التعريض لفريد إسبيناك (ناسا).")
    save(fig, CH, "brightness_ladder", "الفرق الكبير في سطوع ظواهر الكسوف الكلي (قيم Q).", "chart")


def fig_image_size():
    ts, eph = besselian.ephemeris()
    d = eph["earth"].at(ts.utc(2027, 8, 2, 10)).observe(eph["sun"]).distance().km
    ang = 2 * np.arcsin(696000 / d)
    f = np.linspace(50, 2500, 200)
    fig = page(8.4, 5.0)
    header(fig, "حجم قرص الشمس على المستشعر", "قطر صورة الشمس (مم) ≈ البعد البؤري ÷ ١٠٩")
    ax = fig.add_axes([0.08, 0.14, 0.80, 0.62])
    ax.plot(f, f * ang, color=BLUE[9], lw=2.4)
    for ff in (200, 400, 600, 800, 1200, 2000):
        ax.plot(ff, ff * ang, "o", color=RED)
        ax.text(ff, ff * ang + 0.8, A(f"{ff * ang:.1f}") + " مم", ha="center", fontsize=9)
    ax.axhline(24, color=MUTED, ls="--", lw=1)
    ax.text(150, 24.5, "ارتفاع مستشعر الإطار الكامل (٢٤ مم)", fontsize=8.8, color=INK2)
    ax.axhline(15.6, color=MUTED, ls=":", lw=1)
    ax.text(150, 16.1, "ارتفاع مستشعر APS-C (≈ ١٥٫٦ مم)", fontsize=8.8, color=INK2)
    ax.set_xlabel("البعد البؤري (مم)")
    ax.set_ylabel("قطر صورة الشمس (مم)")
    style_axes(ax)
    arabic_ticks(ax, fmt="{:.0f}")
    mirror_y(ax)
    footer(fig, "القطر الظاهري للشمس يوم الكسوف محسوب من تقويم JPL DE421.")
    save(fig, CH, "sun_image_size", "قطر صورة الشمس على المستشعر حسب البعد البؤري (محسوب).", "chart")


def fig_framing():
    ts, eph = besselian.ephemeris()
    d = eph["earth"].at(ts.utc(2027, 8, 2, 10)).observe(eph["sun"]).distance().km
    ang = 2 * np.arcsin(696000 / d)
    sensors = [("الإطار الكامل", 36, 24), ("APS-C", 23.5, 15.6)]
    fls = [300, 500, 800, 1200]
    fig = plt.figure(figsize=(8.6, 6.4), facecolor=PAPER)
    header(fig, "كيف يبدو الإطار؟", "قرص القمر المظلم والهالة حتى ٣ أنصاف أقطار شمسية على مستشعرين وأربعة أبعاد بؤرية")
    for i, (sn, w, h) in enumerate(sensors):
        for j, fl in enumerate(fls):
            ax = fig.add_axes([0.73 - j * 0.235, 0.47 - i * 0.40, 0.21, 0.30])
            ax.set_xlim(-w / 2, w / 2)
            ax.set_ylim(-h / 2, h / 2)
            ax.set_aspect("equal")
            ax.set_facecolor("#05080f")
            ax.set_xticks([])
            ax.set_yticks([])
            r = fl * ang / 2
            for k, a in [(3.0, 0.08), (2.0, 0.15), (1.4, 0.3), (1.12, 0.6)]:
                ax.add_patch(plt.Circle((0, 0), r * k, fc=SUN if False else "#e9f1ff", alpha=a, lw=0))
            ax.add_patch(plt.Circle((0, 0), r * 1.03, fc="#05080f", lw=0))
            ax.set_title(f"{sn} — {A(fl)} مم", fontsize=9)
    footer(fig, "اختر بعدًا بؤريًا يترك هامشًا حول الهالة الخارجية؛ ٤٠٠–٨٠٠ مم مناسبة لمعظم الكاميرات. (محسوب)")
    save(fig, CH, "framing_guide", "مقارنة تأطير الشمس المكسوفة على مستشعرين وأبعاد بؤرية مختلفة (محسوب).")


def fig_drift():
    fls = np.array([50, 100, 200, 300, 400, 600, 800, 1200])
    pix = 4.0e-3   # 4 µm pixels
    rate = 15.0 * np.cos(np.radians(17.76)) / 3600.0  # deg per s along the diurnal circle
    tmax = pix / (fls * np.radians(rate))
    fig = page(8.4, 5.0)
    header(fig, "على حامل ثابت: كم ثانية قبل أن تتحرك الشمس؟", "أطول تعريض قبل أن تنزاح الصورة بمقدار بكسل واحد (٤ ميكرون)")
    ax = fig.add_axes([0.08, 0.14, 0.80, 0.62])
    ax.bar([A(f) for f in fls], tmax, color=BLUE[8], width=0.6)
    for k, t in enumerate(tmax):
        ax.text(k, t + 0.02, A(f"{t:.2f}") + " ث", ha="center", fontsize=8.8)
    ax.set_xlabel("البعد البؤري (مم)")
    ax.set_ylabel("أطول تعريض (ثانية)")
    style_axes(ax)
    arabic_ticks(ax, x=False)
    mirror_y(ax)
    footer(fig, "حُسبت من سرعة الحركة الظاهرية للشمس (≈ ١٥″ في الثانية مضروبة في جيب تمام الميل). للتعريضات الأطول استعمل حاملًا متتبعًا.")
    save(fig, CH, "tripod_drift_limit", "أطول زمن تعريض على حامل ثابت قبل ظهور أثر حركة الشمس (محسوب).", "chart")


def fig_sun_path_plan(name, la, lo, slug):
    from skyfield.api import wgs84
    ts, eph = besselian.ephemeris()
    c = {k: float(np.ravel(v)[0]) for k, v in C.local_circumstances(B, np.array([la]), np.array([lo])).items()}
    times = np.linspace(c["c1"], c["c4"], 13)
    obs = eph["earth"] + wgs84.latlon(la, lo)

    def proj(alt, az):   # zenith-centred sky view looking up: north up, east left
        z = 90 - alt
        return -z * np.sin(np.radians(az)), z * np.cos(np.radians(az))

    fig = page(7.6, 7.8)
    header(fig, f"خطة صورة متتابعة من {name}", "مواقع الشمس ومراحل الكسوف كل ١٤ دقيقة تقريبًا كما تُرى عند النظر إلى الأعلى (محسوبة)")
    ax = fig.add_axes([0.06, 0.08, 0.88, 0.76])
    ax.set_aspect("equal")
    ax.axis("off")
    for zz in (10, 20, 30):
        ax.add_patch(plt.Circle((0, 0), zz, fc="none", ec=LINE, lw=0.8))
        ax.text(0, -zz - 1.2, A(90 - zz) + "°", ha="center", va="top", fontsize=8, color=MUTED)
    ax.plot(0, 0, "+", color=MUTED, ms=10)
    ax.text(0.8, 0.8, "سمت الرأس", fontsize=8.5, color=MUTED)
    for lab, (x, y) in [("شمال", (0, 33)), ("جنوب", (0, -34.5)), ("شرق", (-34, 0)), ("غرب", (34, 0))]:
        ax.text(x, y, lab, ha="center", va="center", fontsize=11, fontweight="bold", color=INK2)
    R = 1.2   # drawn solar radius (deg) — enlarged for legibility
    for i_t, th in enumerate(times):
        t = ts.ut1(2027, 8, 2, 0, 0, th * 3600)
        o = obs.at(t)
        sa, sz, _ = o.observe(eph["sun"]).apparent().altaz()
        ma, mz, _ = o.observe(eph["moon"]).apparent().altaz()
        x, y = proj(sa.degrees, sz.degrees)
        mx, my = proj(ma.degrees, mz.degrees)
        k = R / 0.262
        sun = plt.Circle((x, y), R, fc=SUN, ec="none", zorder=3)
        ax.add_patch(sun)
        m = plt.Circle((x + (mx - x) * k, y + (my - y) * k), R * 1.03, fc="#2b3445", ec="none", zorder=4)
        ax.add_patch(m)
        m.set_clip_path(sun)
        below = i_t % 2 == 0
        ax.text(x, y - R - 0.5 if below else y + R + 0.5, I.fmt_time(th + UTC, seconds=False), ha="center",
                va="top" if below else "bottom", fontsize=8.5)
    ax.set_xlim(-36, 36)
    ax.set_ylim(-36, 36)
    footer(fig, "الدوائر: الارتفاع فوق الأفق. القرص مكبَّر نحو ٥ مرات للتوضيح ومواقعه بالمقياس الحقيقي. اختر عدسة تغطي هذا المجال.")
    save(fig, CH, slug, f"مسار الشمس ومراحل الكسوف في سماء {name} لتخطيط صورة متتابعة (محسوب).", "chart")


def fig_fov_needed():
    rows = [("الأقصر", 25.6872, 32.6396), ("سوهاج", 26.5591, 31.6957), ("أسيوط", 27.1783, 31.1859),
            ("مرسى علم", 25.0676, 34.879), ("أسوان", 24.0889, 32.8998), ("القاهرة", 30.0444, 31.2357)]
    from skyfield.api import wgs84
    ts, eph = besselian.ephemeris()
    fig = page(8.4, 5.0)
    header(fig, "أي عدسة تجمع الشمس والمعبد في لقطة واحدة؟", "الشمس مرتفعة جدًا: يلزم مجال رؤية رأسي يمتد من الأفق إلى الشمس")
    ax = fig.add_axes([0.06, 0.12, 0.60, 0.66])
    alts = []
    for n, la, lo in rows:
        c = {k: float(np.ravel(v)[0]) for k, v in C.local_circumstances(B, np.array([la]), np.array([lo])).items()}
        t = ts.ut1(2027, 8, 2, 0, 0, c["tmax"] * 3600)
        a, z, _ = (eph["earth"] + wgs84.latlon(la, lo)).at(t).observe(eph["sun"]).apparent().altaz()
        alts.append(a.degrees)
    need = np.array(alts) + 5
    f_ff = 12 / np.tan(np.radians(need / 2))   # vertical FOV of a full-frame sensor in portrait (36 mm tall)/2 = 18
    f_ff = 18 / np.tan(np.radians(need / 2))
    ax.barh(range(len(rows)), need, color=BLUE[8], height=0.6)
    for k, (v, f) in enumerate(zip(need, f_ff)):
        ax.text(v + 1, k, f"{A(f'{v:.0f}')}° ← عدسة ≤ {A(f'{f:.0f}')} مم (إطار كامل عموديًا)", va="center", ha="right",
                fontsize=9)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=10.5)
    ax.yaxis.tick_right()
    ax.invert_xaxis()
    ax.set_xlim(150, 0)
    ax.set_xticks([])
    style_axes(ax, grid=False)
    ax.spines["bottom"].set_visible(False)
    footer(fig, "مجال الرؤية = ارتفاع الشمس + ٥° هامشًا؛ البعد البؤري محسوب لمستشعر ٣٦×٢٤ مم مثبت عموديًا. أي عدسة ≥ ٩٠° تحتاج عين السمكة.")
    save(fig, CH, "wide_angle_needed", "مجال الرؤية الرأسي والعدسة اللازمة لتصوير الشمس مع المعالم الأرضية (محسوب).", "chart")


def fig_filter_timeline(name, la, lo, slug):
    c = {k: float(np.ravel(v)[0]) for k, v in C.local_circumstances(B, np.array([la]), np.array([lo])).items()}
    d = c["duration_s"]
    t2 = c["c2"] + UTC
    plan = [(-60, "الهلال ما زال ساطعًا: أبقِ المرشحات مكانها", SUN_DEEP),
            (-15, "انزع مرشح الكاميرا (لا تنظر عبر محدد الرؤية)", SUN),
            (-5, "حبات بيلي ثم الخاتم الماسي: تصوير متتابع سريع", "white"),
            (0, "التماس الثاني: بداية الكلية — انزع نظارتك", "white"),
            (10, "الألسنة والكروموسفير الوردي: تعريضات قصيرة", "#ff8fa3"),
            (30, "الهالة: سلسلة تعريضات من الأقصر إلى الأطول", CORONA_C),
            (d / 2, "منتصف الكلية: ارفع عينيك عن الكاميرا واستمتع", SUN),
            (d - 15, "استعد للخاتم الماسي الثاني", "white"),
            (d, "التماس الثالث: نهاية الكلية — نظارتك فورًا", "white"),
            (d + 15, "أعد مرشح الكاميرا", SUN)]
    fig = page(7.6, 7.2, NAVY)
    ax = canvas(fig)
    header(fig, f"دقائق الكلية في {name}: خطة التصوير", f"الكلية {I.fmt_dur(d, long=True)} — الأوقات بتوقيت مصر الصيفي (محسوبة)",
           color="white", sub_color="#c9d3e3")
    top, bot = 0.82, 0.08
    step = (top - bot) / (len(plan) - 1)
    ax.plot([0.66, 0.66], [bot, top], color="#2a3d5c", lw=3)
    for k, (tt, lab, col) in enumerate(plan):
        y = top - k * step
        inside = 0 <= tt <= d
        ax.add_patch(Circ(ax, (0.66, y), 0.014, fc=col, ec=NAVY, lw=1.5, zorder=3))
        rel = "ت٢" if tt == 0 else ("ت٣" if tt == d else (("ت٢ − " + A(int(-tt)) + " ث") if tt < 0 else
                                                          (("ت٢ + " + A(int(tt)) + " ث") if tt < d else ("ت٣ + " + A(int(tt - d)) + " ث"))))
        ax.text(0.95, y + 0.012, I.fmt_time(t2 + tt / 3600), ha="right", va="center", color="white", fontsize=11,
                fontweight="bold")
        ax.text(0.95, y - 0.022, rel, ha="right", va="center", color="#9aa6b8", fontsize=8.5)
        ax.text(0.62, y, lab, ha="right", va="center", color=col, fontsize=10.2)
        if inside and k < len(plan) - 1:
            ax.plot([0.66, 0.66], [y, y - step], color=CORONA_C, lw=3, zorder=2)
    footer(fig, "انظر بعينيك دون نظارة فقط بين التماسين الثاني والثالث.", color="#8a96a8")
    save(fig, CH, slug, f"خطة التصوير خلال دقائق الكلية في {name} (محسوبة).")


CORONA_C = "#cfe0ff"


def main():
    list_card("معدّات تصوير الكسوف", "من الهاتف إلى التلسكوب",
              ["حامل ثلاثي متين (ويُفضَّل حامل متتبع للتعريضات الطويلة)", "عدسة مقرّبة ٣٠٠–٨٠٠ مم للهالة والألسنة",
               "عدسة واسعة أو عين سمكة للمشهد العام والأفق", "مرشح شمسي معتمد أمام كل عدسة مقرّبة (للمراحل الجزئية)",
               "مفتاح تحكم عن بُعد أو تطبيق تصوير آلي", "بطاريات وبطاقات ذاكرة إضافية",
               "غطاء أو مظلة لحماية الكاميرا من حرارة الشمس", "مصباح أحمر خافت لقراءة الإعدادات أثناء الظلام"],
              "equipment", "قائمة معدات تصوير الكسوف.", cols=2)
    fig_exposure_table(5.6)
    fig_exposure_table(8)
    fig_exposure_table(11)
    fig_brightness_ladder()
    fig_image_size()
    fig_framing()
    fig_drift()
    fig_filter_timeline("الأقصر", 25.6872, 32.6396, "totality_plan_luxor")
    fig_filter_timeline("سوهاج", 26.5591, 31.6957, "totality_plan_sohag")
    for n, la, lo, sl in [("الأقصر", 25.6872, 32.6396, "sequence_plan_luxor"), ("القاهرة", 30.0444, 31.2357, "sequence_plan_cairo"),
                          ("أسوان", 24.0889, 32.8998, "sequence_plan_aswan"), ("الغردقة", 27.2579, 33.8116, "sequence_plan_hurghada")]:
        fig_sun_path_plan(n, la, lo, sl)
    fig_fov_needed()
    list_card("التصوير بالهاتف الذكي", "نتائج جيدة بأدوات بسيطة",
              ["ثبّت الهاتف على حامل صغير ولا تصوّر باليد", "ضع مرشحًا شمسيًا أمام عدسة الهاتف في المراحل الجزئية",
               "أثناء الكلية انزع المرشح وصوّر المشهد الواسع: الأفق والناس والسماء", "استخدم الوضع اليدوي (Pro) وثبّت التركيز على اللانهاية",
               "جرّب التصوير بفاصل زمني (Time-lapse) لظل القمر وهو يقترب", "لا تحاول تكبير الشمس رقميًا؛ الصور الواسعة أجمل"],
              "smartphone_tips", "نصائح تصوير الكسوف بالهاتف الذكي.")
    list_card("ضبط الكاميرا قبل يوم الكسوف", "قائمة تحقق للمصوّر",
              ["صوّر بصيغة RAW وأوقف تحسينات المعالجة الآلية", "التركيز يدويًا على حافة الشمس عبر المرشح ثم ثبّته بشريط لاصق",
               "أوقف مثبت الصورة إذا كانت الكاميرا على حامل", "استخدم ISO منخفضًا (١٠٠–٤٠٠) للحصول على أقل ضوضاء",
               "جرّب تسلسل التعريضات المتعدد (Bracketing) مسبقًا", "زامن ساعة الكاميرا مع التوقيت الدقيق",
               "تدرّب على الخطة كاملة في الأيام السابقة وفي التوقيت نفسه"],
              "camera_setup", "قائمة ضبط الكاميرا والتحضير للتصوير.")
    list_card("أخطاء شائعة في تصوير الكسوف", "تعلّم من تجارب الآخرين",
              ["نسيان نزع المرشح عند بداية الكلية — فتضيع صور الهالة", "نسيان إعادة المرشح بعد الكلية — فيتضرر المستشعر",
               "الاعتماد على التركيز التلقائي في الظلام", "قضاء الدقائق كلها خلف الكاميرا دون مشاهدة",
               "استعمال الفلاش: لا فائدة منه ويزعج الآخرين", "حامل ضعيف يهتز مع الرياح أو اللمس"],
              "common_mistakes", "أخطاء شائعة في تصوير الكسوف وكيف تتجنبها.", dark=True)
    list_card("من الصور الخام إلى صورة الهالة", "خطوات معالجة صور الكسوف الكلي",
              ["اختر سلسلة التعريضات المتعددة الحادة للهالة", "حاذِ الصور بدقة على قرص القمر",
               "ادمجها بتقنية المدى الديناميكي العالي (HDR)", "أبرز تفاصيل الشرائط بمرشحات شعاعية بلطف",
               "صحّح الألوان وأزل الضوضاء", "احتفظ بالملفات الأصلية مع بيانات الوقت والموقع"],
              "processing_workflow", "خطوات معالجة صور الهالة الشمسية.")
    list_card("اختيار موقع التصوير", "خطوات عملية قبل يوم الكسوف",
              ["حدد خط المركز ثم ابحث بصور الأقمار الصناعية عن ساحات مفتوحة أو أسطح مبانٍ أو استراحات طرق",
               "تأكد بالصور الأرضية أن الأفق نحو الشمس خالٍ من الأشجار والأسوار والأعمدة",
               "اختر ثلاثة أو أربعة مواقع بديلة متقاربة، فقد تكون صور الخرائط قديمة",
               "زر الموقع مسبقًا إن أمكن، وتأكد أنه ليس ملكية خاصة",
               "توقّع الزحام: الأماكن المنظمة قد تجمع آلاف الناس، والفنادق تُحجز قبل أشهر",
               "اخرج مبكرًا جدًا؛ الانتظار في الموقع أفضل من الانتظار في زحام الطريق"],
              "site_selection", "خطوات اختيار موقع التصوير (مقتبسة بتصرف من Allan Hall, 2017).")
    list_card("حين تكون الشمس فوق رأسك", "تحدٍّ خاص بمصر: الشمس على ارتفاع ٧٨–٨٢° وقت الكلية",
              ["الأفضل للتصوير عادةً ارتفاع ٤٥–٦٠°؛ أما قرب سمت الرأس فيصعب التوجيه",
               "الحوامل الاستوائية تتعثر قرب سمت الرأس؛ جرّب الحامل قبل الحدث على الشمس في الساعة نفسها",
               "استخدم رأس حامل يميل إلى ٩٠° أو حاملًا سمتيًا متينًا",
               "محدد الرؤية يصبح غير مريح: اعتمد على الشاشة الخلفية والعرض الحي",
               "للمشاهدة: استلقِ على حصيرة بدل إمالة الرقبة دقائق طويلة",
               "للمشهد الواسع: عدسة عين السمكة أو واسعة جدًا تجمع الأفق والشمس معًا"],
              "zenith_challenge", "تحديات تصوير الكسوف والشمس قرب سمت الرأس في صعيد مصر.")
    list_card("إطلاق الغالق دون اهتزاز", "لمسة الإصبع تكفي لإفساد صورة مكبّرة",
              ["استخدم جهاز تحكم عن بُعد سلكيًا أو لاسلكيًا", "أو مؤقّت الفواصل (Intervalometer) لسلسلة لقطات آلية",
               "أو المؤقّت الذاتي للكاميرا (ثانيتان على الأقل)", "فعّل قفل المرآة في كاميرات DSLR",
               "أو تحكّم بالكاميرا من الحاسوب أو تطبيق الهاتف", "قد تستمر الاهتزازات ثواني بعد اللمس: انتظرها"],
              "vibration_free", "طرق إطلاق الغالق دون اهتزاز (مقتبسة بتصرف من Allan Hall, 2017).", cols=2)
    list_card("اصنع حامل مرشح من الورق المقوّى", "حل بسيط للكاميرات المدمجة والهواتف والمناظير",
              ["قصّ قطعتين متساويتين من الورق المقوّى وافتح في كل منهما نافذة بالحجم نفسه",
               "قصّ قطعة من رقائق المرشح الشمسي المعتمد أكبر من النافذة",
               "ثبّت الرقيقة على القطعة الأولى بشريط لاصق من جميع الجهات",
               "ألصق القطعة الثانية فوقها لتحبس الرقيقة بينهما",
               "افحصها أمام مصباح: لا يجوز أن يتسرب أي ضوء من ثقب أو حافة",
               "التجاعيد البسيطة لا تضر ما دام كل الضوء يمر عبر المرشح"],
              "diy_filter_card", "خطوات صنع حامل لرقائق المرشح الشمسي (مقتبسة بتصرف من Allan Hall, 2017).")
    list_card("أي كاميرا تناسبك؟", "مزايا كل نوع وقيوده في تصوير الكسوف",
              ["كاميرا DSLR: تحكم يدوي كامل، تُركّب على التلسكوب مباشرة، وتدعم التحكم عن بُعد",
               "الكاميرا عديمة المرآة: الإمكانات نفسها تقريبًا بوزن أخف؛ تحقق من توافر أدوات التحكم عن بُعد",
               "الكاميرا الجسرية: عدسة مقرّبة مدمجة لكنها لا تُفك؛ اختبر التركيز عبر المرشح مسبقًا",
               "الكاميرا المدمجة: خفيفة، تُركّب على عينية التلسكوب بمحوّل بسيط",
               "الهاتف أو الجهاز اللوحي: ثبّته بحامل ومرشح، واستعمل المؤقّت أو العدسة المقرّبة إن وجدت",
               "أي كاميرا مع لوحَي الثقب: صوّر صورة الشمس المُسقطة على اللوح الأبيض بأمان تام"],
              "camera_types", "مقارنة أنواع الكاميرات لتصوير الكسوف (مقتبسة بتصرف من Allan Hall, 2017).")
    write_catalogue("ch5")


if __name__ == "__main__":
    main()
