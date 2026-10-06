"""Chapter 1 — scientific background (Arabic infographics)."""
import numpy as np

from common import (A, Circ, BLUE, BODY, CARD, CAT, CORONA, GREEN, INK, INK2, LINE, MUTED, NAVY, NAVY2, ORANGE,
                    PAPER, RED, SUN, SUN_DEEP, TITLE, Circle, Ellipse, MPoly, Rectangle, arabic_ticks, arrow,
                    canvas, card, corona, wrap, eclipse_phase, footer, halo, header, mirror_y, moon_disk, number_badge,
                    page, para, plt, prominences, save, style_axes, sun_disk, write_catalogue)
from eclipse2027 import besselian, circumstances as C, engine as E, i18n as I

CH = 1
SRC = "المصدر: حسابات المؤلف من تقويم JPL DE421"


# ------------------------------------------------------------------ 1 cosmic coincidence
def fig_coincidence():
    fig = page(8, 5.2, NAVY)
    ax = canvas(fig)
    header(fig, "مصادفة كونية: لماذا يغطي القمرُ الشمسَ تمامًا؟",
           "قطر الشمس أكبر من قطر القمر بنحو ٤٠٠ مرة، وهي أبعد عنا بنحو ٤٠٠ مرة أيضًا", color="white",
           sub_color="#c9d3e3")
    # cone from eye to sun through moon
    ex, ey = 0.88, 0.50
    sx, sr = 0.10, 0.13
    mx, mr = 0.66, 0.0115 * 4.0
    sh = sr * ax._asp
    ax.fill([ex, sx, sx], [ey, ey + sh, ey - sh], color="#ffffff", alpha=0.06, zorder=1)
    ax.plot([ex, sx], [ey, ey + sh], color="#c9d3e3", lw=0.8, ls="--", zorder=2)
    ax.plot([ex, sx], [ey, ey - sh], color="#c9d3e3", lw=0.8, ls="--", zorder=2)
    sun_disk(ax, sx, ey, sr)
    mr = sr * (ex - mx) / (ex - sx)
    moon_disk(ax, mx, ey, mr, color="#9aa6b8")
    ax.add_patch(Circ(ax, (ex, ey), 0.018, fc="#6da7ec", ec="white", lw=1, zorder=5))
    ax.text(ex, ey - 0.06, "الراصد على الأرض", ha="center", color="white", fontsize=10)
    ax.text(mx, ey - mr * ax._asp - 0.05, "القمر", ha="center", color="white", fontsize=11, fontweight="bold")
    ax.text(sx, ey - sh - 0.06, "الشمس", ha="center", color="white", fontsize=12, fontweight="bold")
    rows = [("قطر الشمس", "١٫٣٩ مليون كم"), ("قطر القمر", "٣٤٧٥ كم"), ("النسبة", "≈ ٤٠٠ : ١"),
            ("بُعد الشمس", "١٤٩٫٦ مليون كم"), ("بُعد القمر", "٣٨٤٤٠٠ كم"), ("النسبة", "≈ ٣٩٠ : ١")]
    for i, (k, v) in enumerate(rows):
        yy = 0.16 - (i % 3) * 0.05
        xx = 0.95 if i < 3 else 0.62
        ax.text(xx, yy, k, ha="right", color="#c9d3e3", fontsize=9.5)
        ax.text(xx - 0.13, yy, v, ha="right", color="white", fontsize=9.5, fontweight="bold")
    ax.text(0.55, 0.78, "القطر الزاوي لكليهما ≈ نصف درجة (٠٫٥°)", ha="center", color=SUN, fontsize=12,
            fontweight="bold", fontfamily=TITLE)
    save(fig, CH, "cosmic_coincidence", "تتطابق الأقطار الزاوية للشمس والقمر تقريبًا لأن نسبة القطرين تقارب نسبة البعدين.")


# ------------------------------------------------------------------ 2 scale distances
def fig_scale():
    fig = page(8, 4.6)
    ax = canvas(fig)
    header(fig, "المقياس الحقيقي: الأرض والقمر والشمس",
           "لو صغّرنا المسافة بين الأرض والقمر إلى ٣ سم لصارت الشمس على بعد ١٢ مترًا تقريبًا")
    y = 0.42
    ax.plot([0.06, 0.94], [y, y], color=LINE, lw=1)
    # earth & moon at right (to scale with each other: diameters 12742 & 3475 km, distance 384400)
    scale = 0.30 / 384400
    ex = 0.90
    ax.add_patch(Circ(ax, (ex, y), 12742 * scale / 2 * 6, fc="#3987e5", ec="none", zorder=3))
    ax.add_patch(Circ(ax, (ex - 384400 * scale, y), 3475 * scale / 2 * 6, fc="#9aa6b8", ec="none", zorder=3))
    ax.annotate("", (ex - 384400 * scale, y + 0.10), (ex, y + 0.10),
                arrowprops=dict(arrowstyle="<->", color=INK2, lw=1))
    ax.text(ex - 384400 * scale / 2, y + 0.12, "٣٨٤٤٠٠ كم (متوسط بُعد القمر)", ha="center", fontsize=9.5, color=INK2)
    ax.text(ex, y - 0.08, "الأرض", ha="center", fontsize=10)
    ax.text(ex - 384400 * scale, y - 0.08, "القمر", ha="center", fontsize=10)
    ax.text(0.05, y, "◄", ha="left", va="center", fontsize=16, color=SUN_DEEP, fontfamily=["DejaVu Sans"])
    para(ax, 0.50, 0.30, "الشمس على المقياس نفسه تقع خارج الصفحة: على بعد ≈ ١٢٠ ضعف عرض هذا الشكل، "
         "وقطرها أكبر من مدار القمر كله بنحو مرتين تقريبًا (١٫٣٩ مليون كم مقابل قطر مدار يبلغ ٧٦٩ ألف كم).",
         width=70, size=10, ha="center")
    ax.text(0.40, y + 0.03, "(رُسمت الأرض والقمر أكبر ٦ مرات من حجمهما الحقيقي على هذا المقياس كي يظهرا)",
            ha="center", fontsize=8, color=MUTED)
    save(fig, CH, "true_scale", "المقياس الحقيقي للمسافات بين الأرض والقمر والشمس.")


# ------------------------------------------------------------------ 3 apparent sizes through 2027
def fig_apparent_sizes():
    ts, eph = besselian.ephemeris()
    days = np.arange(0, 366, 0.25)
    t = ts.utc(2027, 1, 1 + days)
    e = eph["earth"].at(t)
    ds = e.observe(eph["sun"]).distance().km
    dm = e.observe(eph["moon"]).distance().km
    sun_arcmin = np.degrees(2 * np.arcsin(696000 / ds)) * 60
    moon_arcmin = np.degrees(2 * np.arcsin(1737.4 / dm)) * 60
    fig = page(8.4, 5.2)
    header(fig, "القطر الظاهري للشمس والقمر خلال عام ٢٠٢٧",
           "حين يكون القمر أكبر ظاهريًا من الشمس يكون الكسوف كليًا؛ وحين يصغر عنها يكون حلقيًا")
    ax = fig.add_axes([0.06, 0.14, 0.86, 0.64])
    ax.plot(days, moon_arcmin, color=BLUE[8], lw=1.6, label="القمر")
    ax.plot(days, sun_arcmin, color=SUN_DEEP, lw=2.2, label="الشمس")
    ax.fill_between(days, sun_arcmin, moon_arcmin, where=moon_arcmin > sun_arcmin, color=BLUE[2], alpha=0.6)
    ax.fill_between(days, sun_arcmin, moon_arcmin, where=moon_arcmin < sun_arcmin, color=ORANGE[1], alpha=0.7)
    d_aug = (np.datetime64("2027-08-02") - np.datetime64("2027-01-01")).astype(int) + 10 / 24
    i = int(np.argmin(abs(days - d_aug)))
    ax.plot(days[i], moon_arcmin[i], "o", ms=8, color=RED, zorder=5)
    ax.annotate(f"٢ أغسطس: القمر {A(f'{moon_arcmin[i]:.1f}')}′ والشمس {A(f'{sun_arcmin[i]:.1f}')}′\nالقمر قرب الحضيض ⇐ كسوف كلي طويل",
                (days[i], moon_arcmin[i]), xytext=(days[i] + 22, 33.75), fontsize=8.8,
                arrowprops=dict(arrowstyle="-", color=RED), ha="left", color=INK,
                bbox=dict(fc="white", ec=LINE, boxstyle="round,pad=0.3"))
    d_feb = (np.datetime64("2027-02-06") - np.datetime64("2027-01-01")).astype(int) + 16 / 24
    j = int(np.argmin(abs(days - d_feb)))
    ax.plot(days[j], moon_arcmin[j], "o", ms=7, color=SUN_DEEP, zorder=5)
    ax.annotate("٦ فبراير: كسوف حلقي\n(القمر أصغر من الشمس)", (days[j], moon_arcmin[j]),
                xytext=(days[j] + 18, 29.05), fontsize=8.8, arrowprops=dict(arrowstyle="-", color=SUN_DEEP),
                bbox=dict(fc="white", ec=LINE, boxstyle="round,pad=0.3"))
    months = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر",
              "نوفمبر", "ديسمبر"]
    ax.set_xticks(np.cumsum([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30]) + 15)
    ax.set_xticklabels(months, fontsize=8.5)
    ax.set_ylabel("القطر الظاهري (دقيقة قوسية)")
    style_axes(ax)
    arabic_ticks(ax, x=False)
    mirror_y(ax)
    ax.set_ylim(28.7, 34.3)
    ax.legend(loc="upper left", frameon=True, fontsize=9.5, ncol=2, framealpha=0.95)
    footer(fig, SRC + " (مركز الأرض)")
    save(fig, CH, "apparent_diameters_2027", "تغير القطر الظاهري للشمس والقمر على مدار ٢٠٢٧ (محسوب).", "chart")


# ------------------------------------------------------------------ 4 shadow geometry
def fig_shadows():
    fig = page(8.6, 4.8, NAVY)
    ax = canvas(fig)
    header(fig, "ظلّ القمر: الظل الكامل وشبه الظل والظل المضاد", color="white")
    sy = 0.48
    sx, sr = 0.0, 0.17
    sun_disk(ax, sx - 0.05, sy, sr, glow=False)
    mx, mr = 0.50, 0.035
    # umbra cone: tangent lines from sun edges crossing
    tip = 0.80
    ax.fill([mx, mx, tip], [sy + mr, sy - mr, sy], color="#000000", alpha=0.85, zorder=3)
    ax.fill([tip, 0.97, 0.97], [sy, sy + 0.06, sy - 0.06], color="#556070", alpha=0.6, zorder=2)
    ax.fill([mx, mx, 0.97, 0.97], [sy + mr, sy - mr, sy - 0.28, sy + 0.28], color="#7d8a9e", alpha=0.35, zorder=1)
    for s in (1, -1):
        pass
    moon_disk(ax, mx, sy, mr, color="#9aa6b8", z=5)
    lab = dict(color="white", fontsize=10.5, ha="center")
    ax.text(0.66, sy - 0.012, "الظل الكامل", **lab, zorder=6, fontweight="bold")
    ax.text(0.90, sy - 0.012, "الظل المضاد", **lab, zorder=6)
    ax.text(0.82, sy + 0.20, "شبه الظل", **lab)
    ax.text(0.82, sy - 0.22, "شبه الظل", **lab)
    ax.text(mx, sy + 0.07, "القمر", **lab)
    notes = [("داخل الظل الكامل", "كسوف كلي"), ("داخل الظل المضاد", "كسوف حلقي"), ("داخل شبه الظل", "كسوف جزئي")]
    for i, (a, b) in enumerate(notes):
        ax.text(0.95 - i * 0.27, 0.07, a + " ← " + b, ha="right", color=SUN, fontsize=9.5)
    save(fig, CH, "shadow_geometry", "مخروطا ظل القمر: الظل الكامل وشبه الظل والظل المضاد، وأنواع الكسوف المقابلة.")


# ------------------------------------------------------------------ 5 eclipse types
def fig_types():
    fig = page(8.6, 4.4, NAVY)
    ax = canvas(fig)
    header(fig, "أنواع الكسوف الشمسي الأربعة", color="white")
    items = [("كلي", 0.0, 1.03, "يحجب القمر قرص الشمس كله\nفتظهر الهالة"),
             ("حلقي", 0.0, 0.93, "القمر أبعد وأصغر ظاهريًا\nفتبقى حلقة من النار"),
             ("هجين", 0.0, 1.0, "حلقي في بعض أجزاء المسار\nوكلي في أجزاء أخرى"),
             ("جزئي", 0.55, 1.0, "لا يمر الظل المركزي بالأرض\nفيُحجب جزء من الشمس فقط")]
    for k, (name, off, ratio, desc) in enumerate(items):
        cx = 0.86 - k * 0.24
        cy = 0.52
        r = 0.055
        if name == "كلي":
            corona(ax, cx, cy, r, seed=5, strength=0.7)
        sun = sun_disk(ax, cx, cy, r, glow=name != "كلي")
        if name == "هجين":
            corona(ax, cx, cy, r, seed=8, strength=0.35)
        m = moon_disk(ax, cx + off * 2 * r, cy, r * ratio, color=NAVY, clip=sun)
        ax.text(cx, cy - r * ax._asp - 0.12, name, ha="center", color="white", fontsize=14, fontweight="bold",
                fontfamily=TITLE, zorder=8)
        ax.text(cx, cy - r * ax._asp - 0.15, desc, ha="center", va="top", color="#c9d3e3", fontsize=8.8, linespacing=1.5)
    save(fig, CH, "eclipse_types", "أنواع الكسوف الشمسي: الكلي والحلقي والهجين والجزئي.")


# ------------------------------------------------------------------ 6 solar vs lunar
def fig_solar_vs_lunar():
    fig = page(8.6, 5.0)
    ax = canvas(fig)
    header(fig, "الكسوف والخسوف: ما الفرق؟")
    for row, (title, order, desc) in enumerate([
        ("كسوف الشمس", ["sun", "moon", "earth"], "يقع القمر بين الشمس والأرض، ويحدث عند المحاق (ولادة الهلال).\n"
                                                  "يُرى من شريط ضيق على الأرض، ويدوم الكلي دقائق معدودة."),
        ("خسوف القمر", ["sun", "earth", "moon"], "تقع الأرض بين الشمس والقمر، ويحدث عند البدر.\n"
                                                  "يُرى من نصف الكرة الأرضية الليلي كله، ويدوم الكلي ساعة أو أكثر.")]):
        y = 0.62 - row * 0.36
        card(ax, 0.03, y - 0.16, 0.94, 0.32, fc=CARD)
        ax.text(0.95, y + 0.11, title, ha="right", fontsize=14, fontweight="bold", fontfamily=TITLE, color=INK)
        para(ax, 0.95, y + 0.05, desc, width=44, size=9.4, linespacing=1.45)
        xs = {"sun": 0.08, "moon": 0.26, "earth": 0.40}
        if order[1] == "earth":
            xs = {"sun": 0.08, "earth": 0.26, "moon": 0.40}
        sun_disk(ax, xs["sun"], y, 0.05)
        ax.add_patch(Circ(ax, (xs["earth"], y), 0.035, fc="#3987e5", zorder=4))
        ax.add_patch(Circ(ax, (xs["moon"], y), 0.015 if order[1] == "moon" else 0.015,
                            fc="#9aa6b8" if order[1] == "moon" else "#a0452b", zorder=4))
        ax.text(xs["sun"], y - 0.10, "الشمس", ha="center", fontsize=9)
        ax.text(xs["earth"], y - 0.10, "الأرض", ha="center", fontsize=9)
        ax.text(xs["moon"], y + 0.05, "القمر", ha="center", fontsize=9)
    save(fig, CH, "solar_vs_lunar", "الفرق بين كسوف الشمس وخسوف القمر من حيث ترتيب الأجرام ومدة الظاهرة.")


# ------------------------------------------------------------------ 7 orbit inclination
def fig_inclination():
    fig = page(8.6, 5.0, NAVY)
    ax = canvas(fig)
    header(fig, "لماذا لا يحدث كسوف كل شهر؟",
           "مدار القمر مائل بنحو ٥٫١° على مستوى مدار الأرض (دائرة البروج)", color="white", sub_color="#c9d3e3")
    cx, cy = 0.5, 0.42
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(cx + 0.38 * np.cos(th), cy + 0.10 * np.sin(th), color=SUN, lw=1.4, label="البروج")
    ax.plot(cx + 0.38 * np.cos(th), cy + 0.10 * np.sin(th) + 0.10 * np.cos(th) * 0.9, color="#9ec5f4", lw=1.4)
    ax.add_patch(Circ(ax, (cx, cy), 0.025, fc="#3987e5", zorder=5))
    ax.text(cx, cy + 0.075, "الأرض", ha="center", color="white", fontsize=10, zorder=6)
    for s, name in [(1, "العقدة الصاعدة"), (-1, "العقدة الهابطة")]:
        nx = cx + s * 0.38 * np.cos(np.arctan2(0, 1) + (0 if s > 0 else np.pi))
        ny = cy
        th0 = np.pi / 2 * (1 - s) + np.pi / 2
    # nodes where the two curves cross: cos(th)=0 -> th=pi/2, 3pi/2
    for thn, name in [(np.pi / 2, "عقدة"), (3 * np.pi / 2, "عقدة")]:
        x = cx + 0.38 * np.cos(thn)
        y = cy + 0.10 * np.sin(thn)
        ax.plot(x, y, "o", ms=9, mfc=RED, mec="white", zorder=6)
        ax.text(x + 0.03, y + (0.035 if thn < np.pi else -0.06), name, color="white", fontsize=10)
    ax.text(0.93, 0.66, "مدار القمر", color="#9ec5f4", ha="right", fontsize=10.5)
    ax.text(0.93, 0.61, "مستوى مدار الأرض حول الشمس", color=SUN, ha="right", fontsize=10.5)
    para(ax, 0.5, 0.17, "لا يقع الكسوف إلا إذا كان المحاق قريبًا من إحدى العقدتين، أي حين يكون القمر على "
         "مستوى البروج تقريبًا؛ وفي بقية الشهور يمر ظل القمر فوق الأرض أو تحتها.", width=78, size=9.6,
         color="#e6ebf2", ha="center")
    save(fig, CH, "orbit_inclination", "ميل مدار القمر وعقدتاه: شرط حدوث الكسوف.")


# ------------------------------------------------------------------ 8 eclipse seasons 2027 (computed)
def fig_seasons_2027():
    from skyfield import almanac
    from skyfield.framelib import ecliptic_frame
    ts, eph = besselian.ephemeris()
    t, ph = almanac.find_discrete(ts.utc(2027, 1, 1), ts.utc(2028, 1, 1), almanac.moon_phases(eph))
    rows = []
    for ti, p in zip(t, ph):
        if p not in (0, 2):
            continue
        lat, lon, _ = eph["earth"].at(ti).observe(eph["moon"]).apparent().frame_latlon(ecliptic_frame)
        rows.append((ti.utc_datetime(), p, lat.degrees))
    fig = page(8.6, 5.2)
    header(fig, "مواسم الكسوف في عام ٢٠٢٧",
           "عرض القمر عن دائرة البروج عند كل محاق (●) وكل بدر (○)؛ الكسوف والخسوف لا يقعان إلا داخل الشريط")
    ax = fig.add_axes([0.07, 0.14, 0.85, 0.64])
    ax.axhspan(-1.58, 1.58, color=BLUE[1], alpha=0.6, lw=0)
    ax.axhline(0, color=MUTED, lw=0.8)
    import datetime as dt
    d0 = dt.datetime(2027, 1, 1, tzinfo=dt.timezone.utc)
    for d, p, la in rows:
        x = (d - d0).total_seconds() / 86400
        ok = abs(la) < (1.58 if p == 0 else 1.6)
        ax.plot(x, la, "o", ms=8, mfc=(SUN_DEEP if p == 0 else "white") if ok else (INK2 if p == 0 else "white"),
                mec=SUN_DEEP if ok else INK2, mew=1.5, zorder=4)
    events = [(36.7, "كسوف حلقي — ٦ فبراير"), (50.8, "خسوف شبه ظلي — ٢٠ فبراير"), (198.7, "خسوف شبه ظلي — ١٨ يوليو"),
              (213.4, "كسوف كلي — ٢ أغسطس"), (228.0, "خسوف شبه ظلي — ١٧ أغسطس")]
    lat_at = {}
    for d, p, la in rows:
        lat_at[round((d - d0).total_seconds() / 86400)] = la
    for k, (x, lab) in enumerate(events):
        la = min(lat_at.items(), key=lambda kv: abs(kv[0] - x))[1]
        ax.text(x, la + 0.42, A(k + 1), ha="center", fontsize=8.5, color="white", fontweight="bold",
                bbox=dict(boxstyle="circle,pad=0.2", fc=RED if "كلي" in lab else BLUE[9], ec="none"))
        ax.text(0.985, 0.97 - k * 0.075, A(k + 1) + ". " + lab, transform=ax.transAxes, ha="right", va="top",
                fontsize=8.6, color=RED if "كلي" in lab else INK)
    ax.set_ylim(-5.6, 3.6)
    ax.set_ylabel("عرض القمر البروجي (°)")
    months = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر",
              "نوفمبر", "ديسمبر"]
    ax.set_xticks(np.cumsum([0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30]) + 15)
    ax.set_xticklabels(months, fontsize=8.5)
    style_axes(ax)
    arabic_ticks(ax, x=False)
    mirror_y(ax)
    ax.text(330, -1.2, "حدّ الكسوف\n±١٫٥٨°", fontsize=8.5, color=BLUE[9], ha="center")
    footer(fig, SRC + "؛ قائمة الكسوفات والخسوفات محسوبة بالبرنامج نفسه.")
    save(fig, CH, "eclipse_seasons_2027", "مواسم الكسوف في ٢٠٢٧: موسم فبراير وموسم يوليو–أغسطس (محسوب).", "chart")


# ------------------------------------------------------------------ 9 contacts diagram
def fig_contacts():
    fig = page(8.6, 4.2, NAVY)
    ax = canvas(fig)
    header(fig, "التماسات الأربعة: مراحل الكسوف الكلي", color="white")
    labels = [("التماس الأول", "بداية الكسوف الجزئي", -1.0), ("", "", -0.55), ("التماس الثاني", "بداية الكلية", -0.005),
              ("الذروة", "منتصف الكلية", 0.0), ("التماس الثالث", "نهاية الكلية", 0.005), ("", "", 0.55),
              ("التماس الرابع", "نهاية الكسوف", 1.0)]
    for k, (a, b, f) in enumerate(labels):
        cx = 0.92 - k * 0.14
        cy = 0.50
        r = 0.05
        sun = sun_disk(ax, cx, cy, r, glow=False)
        if abs(f) < 0.01:
            corona(ax, cx, cy, r, seed=k, extent=0.35, strength=0.8)
        # moon moves from west (right in the sky as seen facing south) to east: right→left
        moon_disk(ax, cx - f * 2.05 * r, cy, r * 1.035, color=NAVY, clip=sun)
        if f == 0.005:
            ax.add_patch(Circ(ax, (cx - r * 0.75, cy - r * 0.66 * ax._asp), r * 0.12, fc="white", zorder=7))
        if f == -0.005:
            ax.add_patch(Circ(ax, (cx + r * 0.75, cy + r * 0.66 * ax._asp), r * 0.12, fc="white", zorder=7))
        ax.text(cx, cy - r * ax._asp - 0.07, a, ha="center", color="white", fontsize=9.5, fontweight="bold")
        ax.text(cx, cy - r * ax._asp - 0.13, b, ha="center", color="#c9d3e3", fontsize=8.5)
    arrow(ax, 0.95, 0.82, 0.05, 0.82, color="#9ec5f4")
    ax.text(0.5, 0.85, "اتجاه الزمن", ha="center", color="#9ec5f4", fontsize=9.5)
    save(fig, CH, "four_contacts", "التماسات الأربعة للكسوف الكلي من البداية إلى النهاية.")


# ------------------------------------------------------------------ 10 phenomena timeline
def fig_phenomena_timeline():
    fig = page(7.4, 8.4)
    ax = canvas(fig)
    header(fig, "ماذا ترى قبيل الكلية وخلالها وبعدها؟", "تسلسل الظواهر حول التماسين الثاني والثالث (الأوقات تقريبية)")
    ev = [("قبل ١٥ دقيقة", "تخفت الإضاءة وتبهت الألوان وتبرد النسمة", False),
          ("قبل دقيقة", "الأحزمة الظلية تتراقص على الأرض والجدران الفاتحة", False),
          ("قبل ٢٠ ثانية", "ظل القمر يندفع من الأفق الغربي كعاصفة مظلمة", False),
          ("قبل ٥ ثوانٍ", "حبات بيلي: نقاط ضوء على حافة القمر", False),
          ("التماس الثاني", "الخاتم الماسي، ثم تبدأ الكلية — انزع النظارة الآن فقط", True),
          ("أول ثوانٍ الكلية", "الكروموسفير الوردي والألسنة الشمسية عند الحافة", True),
          ("طوال الكلية", "الهالة كاملة؛ الزهرة والمشتري والنجوم اللامعة؛ غروب على كل الأفق", True),
          ("التماس الثالث", "وميض الخاتم الماسي الثاني — أعد النظارة فورًا", False),
          ("بعده بدقيقة", "عودة الأحزمة الظلية وانحسار الظل نحو الشرق", False)]
    top, bot = 0.84, 0.08
    step = (top - bot) / (len(ev) - 1)
    ax.plot([0.70, 0.70], [bot, top], color=LINE, lw=3, zorder=1)
    for i, (when, what, tot) in enumerate(ev):
        y = top - i * step
        col = NAVY if tot else BLUE[6]
        if tot:
            card(ax, 0.04, y - step / 2 + 0.005, 0.92, step - 0.01, fc="#e9eef7", ec="none", z=0)
        ax.add_patch(Circ(ax, (0.70, y), 0.016, fc=col, ec="white", lw=1.5, zorder=3))
        ax.text(0.95, y, when, ha="right", va="center", fontsize=10.5, fontweight="bold", color=col)
        ax.text(0.66, y, wrap(what, 40), ha="right", va="center", fontsize=10, color=INK, linespacing=1.4)
    footer(fig, "يختلف التوقيت من موقع لآخر؛ راجع بطاقة مدينتك في الفصل الثالث.")
    save(fig, CH, "phenomena_timeline", "تسلسل الظواهر المرئية قبل الكلية وخلالها وبعدها.")


# ------------------------------------------------------------------ 11-14 illustrations
def fig_diamond_ring():
    fig = page(6.5, 5.0, "#05080f")
    ax = canvas(fig)
    header(fig, "الخاتم الماسي", "آخر وميض من قرص الشمس قبيل الكلية مباشرة", color="white", sub_color="#c9d3e3")
    cx, cy, r = 0.5, 0.45, 0.17
    corona(ax, cx, cy, r, seed=11, strength=0.8)
    ax.add_patch(Circ(ax, (cx, cy), r * 1.01, fc="#05080f", ec="#ffe9b0", lw=1.8, zorder=4))
    bx, by = cx + r * np.cos(np.radians(40)), cy + r * np.sin(np.radians(40))
    for k, a in [(0.16, 0.08), (0.10, 0.16), (0.06, 0.35), (0.03, 0.8), (0.015, 1.0)]:
        ax.add_patch(Circ(ax, (bx, by), k, fc="white", alpha=a, ec="none", zorder=5))
    for ang in np.linspace(0, np.pi, 4, endpoint=False):
        ax.plot([bx - 0.12 * np.cos(ang), bx + 0.12 * np.cos(ang)], [by - 0.12 * np.sin(ang), by + 0.12 * np.sin(ang)],
                color="white", lw=0.8, alpha=0.6, zorder=5)
    para(ax, 0.5, 0.16, "تحذير: الخاتم الماسي جزء من الشمس الساطعة؛ لا تنزع النظارة إلا بعد اختفائه تمامًا.",
         width=70, size=9.6, color="#ffcf70", ha="center")
    save(fig, CH, "diamond_ring", "رسم توضيحي لظاهرة الخاتم الماسي.")


def fig_bailys_beads():
    fig = page(6.5, 5.0, "#05080f")
    ax = canvas(fig)
    header(fig, "حبات بيلي", "ضوء الشمس ينفذ عبر الوديان على حافة القمر", color="white", sub_color="#c9d3e3")
    cx, cy, r = 0.5, 0.30, 0.42
    th = np.linspace(np.radians(55), np.radians(125), 400)
    ax.plot(cx + r * np.cos(th), cy + r * np.sin(th) + 0.006, color="#ffd27a", lw=3, alpha=0.6)
    rng = np.random.default_rng(4)
    prof = 0.004 * np.sin(th * 90) + 0.003 * np.sin(th * 37 + 1) + rng.normal(0, 0.0008, th.size)
    ax.fill_between(cx + r * np.cos(th), cy - 0.3, cy + (r + prof) * np.sin(th), color="#05080f", zorder=3)
    for a in np.radians([66, 74, 83, 90, 101, 112]):
        x, y = cx + r * np.cos(a), cy + r * np.sin(a) + 0.008
        for k, al in [(0.02, 0.2), (0.01, 0.6), (0.005, 1.0)]:
            ax.add_patch(Circ(ax, (x, y), k, fc="white", alpha=al, zorder=4))
    ax.text(0.5, 0.45, "حافة القمر الجبلية", ha="center", color="#8a96a8", fontsize=10, zorder=5)
    ax.text(0.5, 0.12, "سُمّيت باسم الفلكي البريطاني فرانسيس بيلي الذي وصفها عام ١٨٣٦", ha="center",
            color="#c9d3e3", fontsize=9)
    save(fig, CH, "bailys_beads", "رسم توضيحي لحبات بيلي عند حافة القمر.")


def fig_corona_anatomy():
    fig = page(7.5, 6.0, "#05080f")
    ax = canvas(fig)
    header(fig, "تشريح الهالة الشمسية (الإكليل)", "لا تُرى بالعين المجردة إلا أثناء الكسوف الكلي",
           color="white", sub_color="#c9d3e3")
    cx, cy, r = 0.48, 0.44, 0.11
    corona(ax, cx, cy, r, seed=21, n=34)
    ax.add_patch(Circ(ax, (cx, cy), r, fc="#05080f", ec="#ff6f91", lw=2.5, zorder=4))
    prominences(ax, cx, cy, r, seed=3)
    notes = [((cx + r * 2.6, cy + 0.02), (0.84, 0.68), "الشرائط الإكليلية\n(تمتد ملايين الكيلومترات)"),
             ((cx, cy + r * 1.5), (0.74, 0.80), "الريش القطبية"),
             ((cx - r * 1.15, cy - r * 0.2), (0.10, 0.30), "الإكليل الداخلي\n(≈ ١–٢ مليون درجة)"),
             ((cx + r * 0.95, cy - r * 0.35), (0.90, 0.20), "الكروموسفير والألسنة\n(وردية اللون)")]
    for (x, y), (tx, ty), lab in notes:
        ax.annotate(lab, (x, y), (tx, ty), color="white", fontsize=9.5, ha="center",
                    arrowprops=dict(arrowstyle="-", color="#9aa6b8", lw=0.8))
    save(fig, CH, "corona_anatomy", "أجزاء الهالة الشمسية التي تظهر أثناء الكلية.")


def fig_sun_structure():
    fig = page(8.6, 5.4, NAVY)
    ax = canvas(fig)
    header(fig, "بنية الشمس من اللب إلى الهالة", color="white")
    axs = fig.add_axes([0.02, 0.04, 0.50, 0.50 * 8.6 / 5.4 * 0.95])
    axs.set_xlim(-1, 1)
    axs.set_ylim(-1, 1)
    axs.set_aspect("equal")
    axs.axis("off")
    layers = [(0.98, "#ffe0a3", "الهالة (الإكليل)", "١–٣ ملايين كلفن"), (0.80, "#ff8fa3", "الكروموسفير", "≈ ٤٠٠٠–٢٠٠٠٠ كلفن"),
              (0.76, SUN, "الفوتوسفير (السطح المرئي)", "≈ ٥٨٠٠ كلفن"), (0.70, "#f4a742", "منطقة الحمل", "≈ ٢ مليون كلفن"),
              (0.48, "#ef7d2c", "منطقة الإشعاع", "≈ ٧ ملايين كلفن"), (0.20, "#d84f1e", "اللب (الاندماج النووي)", "≈ ١٥ مليون كلفن")]
    for i, (r, c, name, temp) in enumerate(layers):
        axs.add_patch(Wedge((0, 0), r, 30, 330, fc=c, ec=NAVY, lw=1, alpha=0.35 if i == 0 else 1))
        yy = 0.80 - i * 0.11
        rr = r - (0.09 if i == 0 else 0.03)
        ang = np.radians(20 - i * 8)
        x0, y0 = fig.transFigure.inverted().transform(axs.transData.transform((rr * np.cos(ang), rr * np.sin(ang))))
        ax.plot([x0, 0.60], [y0, yy], color="#9aa6b8", lw=0.6)
        ax.plot(x0, y0, "o", ms=3, color="white")
        ax.text(0.95, yy, name, ha="right", va="center", color="white", fontsize=11, fontweight="bold")
        ax.text(0.95, yy - 0.045, temp, ha="right", va="center", color="#c9d3e3", fontsize=9.2)
    save(fig, CH, "sun_structure", "طبقات الشمس ودرجات حرارتها التقريبية.")


from matplotlib.patches import Wedge  # noqa: E402


# ------------------------------------------------------------------ shadow speed & umbra geometry (computed)
def fig_shadow_speed():
    B = besselian.compute()
    t = np.linspace(-1.68, 1.93, 900)
    la, lo = C.central_line(B, t)
    ok = np.isfinite(la)
    t, la, lo = t[ok], la[ok], lo[ok]
    R = 6371.0
    dla = np.gradient(np.radians(la), t)
    dlo = np.gradient(np.unwrap(np.radians(lo)), t)
    v = R * np.hypot(dla, dlo * np.cos(np.radians(la)))  # km/h
    fig = page(8.6, 5.0)
    header(fig, "سرعة ظل القمر على سطح الأرض", "يندفع الظل بأسرع ما يكون عند طرفي المسار، ويتباطأ حيث الشمس عالية فوق الرأس")
    ax = fig.add_axes([0.08, 0.14, 0.84, 0.64])
    ax.plot(lo, v / 3600, color=BLUE[9], lw=2.2)
    i = int(np.argmin(abs(lo - 32.64)))
    ax.plot(lo[i], v[i] / 3600, "o", color=RED, ms=8)
    ax.annotate(f"الأقصر ≈ {A(f'{v[i]/3600:.2f}')} كم/ث\n(≈ {A(f'{v[i]:,.0f}')} كم/ساعة)", (lo[i], v[i] / 3600),
                xytext=(lo[i] - 10, 1.9), fontsize=9.5, ha="center", arrowprops=dict(arrowstyle="-", color=RED))
    ax.set_ylabel("سرعة الظل (كم/ثانية)")
    ax.set_xlabel("خط الطول (°)")
    ax.set_ylim(0, 3.2)
    ax.text(0.5, 0.92, "قرب طرفي المسار (شروق الشمس وغروبها) تتجاوز السرعة ٢٠ كم/ث فتخرج عن حدود الرسم",
            transform=ax.transAxes, ha="center", fontsize=8.8, color=MUTED)
    style_axes(ax)
    arabic_ticks(ax)
    mirror_y(ax)
    footer(fig, SRC)
    save(fig, CH, "shadow_speed", "سرعة ظل القمر على امتداد مسار الكلية (محسوبة).", "chart")


def fig_umbra_cone():
    r = besselian.raw_elements(np.array([0.1]))
    zm = r["z"][0] * besselian.EARTH_RADIUS_KM if "z" in r else None
    B = besselian.compute()
    e = B.at(0.1)
    tanf2 = B.tan_f2
    umbra_len = 1737.4 / np.sin(np.arctan(tanf2))
    ts, eph = besselian.ephemeris()
    tt = ts.ut1(2027, 8, 2, 10, 5, 0)
    from skyfield.api import wgs84
    d_luxor = (eph["earth"] + wgs84.latlon(25.6872, 32.6396)).at(tt).observe(eph["moon"]).distance().km
    fig = page(8.6, 4.6, NAVY)
    ax = canvas(fig)
    header(fig, "طول مخروط الظل يوم ٢ أغسطس ٢٠٢٧", "طول الظل أكبر من بعد القمر عن الأقصر، فيصل الظل إلى الأرض ويكون الكسوف كليًا",
           color="white", sub_color="#c9d3e3")
    y = 0.40
    x_moon, x_tip = 0.90, 0.06
    x_earth = x_moon - (x_moon - x_tip) * d_luxor / umbra_len
    ax.fill([x_moon, x_moon, x_tip], [y + 0.05, y - 0.05, y], color="black", alpha=0.85)
    moon_disk(ax, x_moon, y, 0.05, color="#9aa6b8")
    ax.plot([x_earth, x_earth], [y - 0.18, y + 0.18], color="#3987e5", lw=3)
    ax.text(x_earth, y + 0.21, "سطح الأرض (الأقصر)", ha="center", color="#9ec5f4", fontsize=10)
    ax.annotate("", (x_tip, y - 0.12), (x_moon, y - 0.12), arrowprops=dict(arrowstyle="<->", color="white"))
    ax.text((x_tip + x_moon) / 2, y - 0.17, f"طول الظل ≈ {A(f'{umbra_len:,.0f}')} كم", ha="center", color="white", fontsize=10.5)
    ax.annotate("", (x_earth, y + 0.12), (x_moon, y + 0.12), arrowprops=dict(arrowstyle="<->", color=SUN))
    ax.text((x_earth + x_moon) / 2, y + 0.135, f"بعد القمر عن الأقصر ≈ {A(f'{d_luxor:,.0f}')} كم", ha="center", color=SUN, fontsize=10)
    ax.text((x_tip + x_earth) / 2, y - 0.06, f"الفائض ≈ {A(f'{umbra_len - d_luxor:,.0f}')} كم", ha="center", color="white", fontsize=9.5)
    footer(fig, SRC, color="#8a96a8")
    save(fig, CH, "umbra_length", "مقارنة طول مخروط ظل القمر ببعده عن الأقصر لحظة الكسوف (محسوب).")


def fig_gamma():
    B = besselian.compute()
    ec = E.eclipse_near(E.jd_from_date(2027, 8, 2, 10), "de421")
    fig = page(7.0, 5.6, NAVY)
    ax = canvas(fig)
    header(fig, "مقدار «غاما»: أين يمر محور الظل؟", f"في كسوف ٢٠٢٧ يمر محور الظل على بُعد {A(f'{abs(ec.gamma):.3f}')} من نصف قطر الأرض عن مركزها",
           color="white", sub_color="#c9d3e3")
    cx, cy, R = 0.5, 0.50, 0.17
    ax.add_patch(Circ(ax, (cx, cy), R, fc="#1f4e8c", ec="#9ec5f4", lw=1.5))
    R = R * ax._asp
    ax.plot([0.05, 0.95], [cy + ec.gamma * R] * 2, color=RED, lw=2)
    ax.plot(cx, cy, "o", color="white")
    ax.annotate("", (cx + 0.06, cy + ec.gamma * R), (cx + 0.06, cy), arrowprops=dict(arrowstyle="<->", color=SUN))
    ax.text(cx + 0.08, cy + ec.gamma * R / 2, "غاما = " + A(f"{ec.gamma:.3f}"), color=SUN, fontsize=11, va="center")
    ax.text(0.94, cy + ec.gamma * R + 0.02, "مسار محور الظل", color="#ff9b94", ha="right", fontsize=10)
    para(ax, 0.5, 0.15, "كلما اقتربت غاما من الصفر مرّ الظل قرب مركز قرص الأرض وطالت الكلية؛ "
         "وإذا تجاوزت قيمتها المطلقة ≈ ١ فاتَ المحورُ الأرضَ ولا يقع كسوف مركزي.", width=70, size=9.6,
         color="#e6ebf2", ha="center")
    save(fig, CH, "gamma", "معامل غاما لكسوف ٢٠٢٧ وموقع محور الظل بالنسبة لمركز الأرض (محسوب).")


def fig_magnitude_vs_obscuration():
    ratio = 1.035
    mag = np.linspace(0, 1, 200)
    ob = C.obscuration(mag, ratio)
    fig = page(8.6, 5.0)
    header(fig, "القدر ونسبة الاحتجاب: مقياسان مختلفان", "القدر = الجزء المغطى من قطر الشمس؛ الاحتجاب = الجزء المغطى من مساحة قرصها")
    ax = fig.add_axes([0.40, 0.17, 0.52, 0.59])
    ax.plot(mag, ob * 100, color=BLUE[9], lw=2.2)
    ax.plot(mag, mag * 100, color=MUTED, lw=1, ls="--")
    ax.set_xlabel("قدر الكسوف")
    ax.set_ylabel("نسبة الاحتجاب (٪)")
    style_axes(ax)
    arabic_ticks(ax)
    mirror_y(ax)
    ax.plot(0.9464, C.obscuration(np.array([0.9464]), ratio)[0] * 100, "o", color=RED)
    ax.annotate("القاهرة: قدر ٠٫٩٤٦ ⇐ احتجاب ٩٤٫٨٪", (0.9464, 94.8), xytext=(0.30, 85), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=RED))
    axd = fig.add_axes([0.03, 0.18, 0.30, 0.55])
    axd.set_xlim(-1.6, 1.6)
    axd.set_ylim(-1.6, 1.6)
    axd.set_aspect("equal")
    axd.axis("off")
    s = Circle((0, 0), 1, fc=SUN)
    axd.add_patch(s)
    m = Circle((1 + 1.035 - 2 * 0.5, 0), 1.035, fc=NAVY)
    axd.add_patch(m)
    m.set_clip_path(s)
    axd.annotate("", (-1, -1.25), (0, -1.25), arrowprops=dict(arrowstyle="<->", color=INK))
    axd.text(-0.5, -1.5, "القدر ٠٫٥", ha="center", fontsize=9)
    axd.text(0, 1.25, "الاحتجاب ≈ ٣٩٪ فقط", ha="center", fontsize=9)
    footer(fig, "حُسبت النسبة لقطر قمر يعادل ١٫٠٣٥ من قطر الشمس كما في كسوف ٢٠٢٧.")
    save(fig, CH, "magnitude_vs_obscuration", "العلاقة بين قدر الكسوف ونسبة احتجاب قرص الشمس (محسوبة).", "chart")


# ------------------------------------------------------------------ Saros
def fig_saros_explained():
    fig = page(8.6, 5.0)
    ax = canvas(fig)
    header(fig, "دورة ساروس: لماذا تتكرر الكسوفات؟", "بعد ١٨ سنة و١١ يومًا و٨ ساعات تقريبًا تعود الشمس والقمر والعقدة إلى الهيئة نفسها")
    rows = [("٢٢٣ شهرًا اقترانيًا", "× ٢٩٫٥٣٠٥٩ يوم", "= ٦٥٨٥٫٣٢ يوم", "تكرار المحاق"),
            ("٢٤٢ شهرًا عقديًا", "× ٢٧٫٢١٢٢٢ يوم", "= ٦٥٨٥٫٣٦ يوم", "عودة القمر إلى العقدة"),
            ("٢٣٩ شهرًا حضيضيًا", "× ٢٧٫٥٥٤٥٥ يوم", "= ٦٥٨٥٫٥٤ يوم", "تكرار بُعد القمر (وحجمه الظاهري)")]
    for i, r in enumerate(rows):
        y = 0.70 - i * 0.15
        card(ax, 0.04, y - 0.055, 0.92, 0.11)
        for k, txt in enumerate(r):
            ax.text(0.93 - k * 0.235, y, txt, ha="right", va="center", fontsize=11 if k < 3 else 9.5,
                    color=INK if k < 3 else BLUE[9], fontweight="bold" if k == 2 else "normal")
    para(ax, 0.5, 0.27, "الثلث اليومي الزائد (٨ ساعات) يجعل الأرض تدور ثلث دورة إضافية، فينزاح مسار الكسوف التالي "
         "في السلسلة نحو ١٢٠° غربًا. وكسوف ٢ أغسطس ٢٠٢٧ هو العضو رقم ٣٨ في سلسلة ساروس ١٣٦.",
         width=80, size=10, ha="center")
    save(fig, CH, "saros_cycle", "الأشهر الثلاثة التي تتوافق في دورة ساروس.")


def saros136():
    dates = [(1901, 5, 18), (1919, 5, 29), (1937, 6, 8), (1955, 6, 20), (1973, 6, 30), (1991, 7, 11),
             (2009, 7, 22), (2027, 8, 2), (2045, 8, 12)]
    out = []
    for y, m, d in dates:
        ec = E.eclipse_near(E.jd_from_date(y, m, d, 12), "de421")
        t = np.linspace(-3.2, 3.2, 1500)
        la, lo = C.central_line(ec.B, t)
        okk = np.isfinite(la)
        r = C.local_circumstances(ec.B, la[okk], lo[okk])
        k = int(np.nanargmax(r["duration_s"]))
        out.append(dict(date=(y, m, d), ec=ec, lat=la, lon=lo, dur=r["duration_s"][k], glat=la[okk][k], glon=lo[okk][k]))
    return out


def fig_saros136_map(S):
    import geopandas as gpd
    from common import ROOT
    world = gpd.read_file(f"{ROOT}/data/countries_world.geojson")
    fig = page(9.5, 5.6)
    header(fig, "عائلة واحدة من الكسوفات: سلسلة ساروس ١٣٦ (١٩٠١–٢٠٤٥)",
           "كل كسوف ينزاح نحو ١٢٠° غربًا عن سابقه ويقع بعده بـ ١٨ سنة و١١ يومًا")
    ax = fig.add_axes([0.03, 0.08, 0.94, 0.74])
    world.plot(ax=ax, color="#f1efea", edgecolor="#cfccc4", lw=0.3)
    ax.set_facecolor("#e8eef3")
    cols = plt.cm.viridis(np.linspace(0.05, 0.85, len(S)))
    for s, c in zip(S, cols):
        lo = s["lon"].copy()
        jump = np.where(np.abs(np.diff(lo)) > 180)[0]
        lo[jump] = np.nan
        lw = 3.2 if s["date"][0] == 2027 else 1.8
        ax.plot(lo, s["lat"], color=RED if s["date"][0] == 2027 else c, lw=lw)
        y, m, d = s["date"]
        ax.text(s["glon"], s["glat"] + 3, A(y), color=RED if y == 2027 else INK, fontsize=9, ha="center",
                fontweight="bold", path_effects=halo())
    ax.set_xlim(-180, 180)
    ax.set_ylim(-40, 60)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xticks([])
    ax.set_yticks([])
    footer(fig, SRC + "؛ خطوط المركز لأعضاء السلسلة ضمن نطاق التقويم.")
    save(fig, CH, "saros136_paths", "خطوط مركز كسوفات سلسلة ساروس ١٣٦ من ١٩٠١ إلى ٢٠٤٥ (محسوبة).", "map")


def fig_saros136_durations(S):
    fig = page(8.6, 5.0)
    header(fig, "مدة الكلية العظمى لأعضاء ساروس ١٣٦", "بلغت السلسلة ذروتها عام ١٩٥٥ (أطول كسوف في القرن العشرين) وتتناقص مدتها ببطء")
    ax = fig.add_axes([0.08, 0.14, 0.84, 0.62])
    yrs = [s["date"][0] for s in S]
    durs = [s["dur"] / 60 for s in S]
    bars = ax.bar(range(len(S)), durs, color=[RED if y == 2027 else BLUE[7] for y in yrs], width=0.65)
    for i, (y, d) in enumerate(zip(yrs, durs)):
        ax.text(i, d + 0.1, I.fmt_dur(d * 60), ha="center", fontsize=8.5)
    ax.set_xticks(range(len(S)))
    ax.set_xticklabels([A(y) for y in yrs])
    ax.set_ylabel("المدة (دقيقة)")
    ax.set_ylim(0, 8)
    style_axes(ax)
    arabic_ticks(ax, x=False)
    mirror_y(ax)
    footer(fig, SRC)
    save(fig, CH, "saros136_durations", "مدة الكلية العظمى لكسوفات ساروس ١٣٦ (محسوبة).", "chart")


# ------------------------------------------------------------------ statistics 1901–2050 (computed)
def eclipse_catalogue():
    import json
    import os
    from common import ROOT
    cache = os.path.join(ROOT, "results", "solar_eclipses_1901_2050.json")
    if os.path.exists(cache):
        return json.load(open(cache))
    eclipses = E.solar_eclipses(1901, 2050)
    rows = []
    for ec in eclipses:
        t = np.linspace(-3.4, 3.4, 1400)
        la, lo = C.central_line(ec.B, t)
        okk = np.isfinite(la)
        dur, glat, glon = 0.0, None, None
        if okk.any() and ec.kind in ("total", "hybrid", "annular"):
            r = C.local_circumstances(ec.B, la[okk], lo[okk])
            if ec.kind != "annular":
                k = int(np.nanargmax(r["duration_s"]))
                dur, glat, glon = float(r["duration_s"][k]), float(la[okk][k]), float(lo[okk][k])
            else:
                k = len(la[okk]) // 2
                glat, glon = float(la[okk][k]), float(lo[okk][k])
        rows.append(dict(date=list(ec.date), hour=ec.hour_ut, kind=ec.kind, gamma=ec.gamma,
                         lat=[None if not np.isfinite(v) else float(v) for v in la[::7]],
                         lon=[None if not np.isfinite(v) else float(v) for v in lo[::7]],
                         dur=dur, glat=glat, glon=glon))
    json.dump(rows, open(cache, "w"))
    return rows


KIND_AR = {"total": "كلي", "annular": "حلقي", "hybrid": "هجين", "partial": "جزئي"}
KIND_COL = {"total": BLUE[10], "annular": SUN_DEEP, "hybrid": "#7a4fc2", "partial": "#9a9890"}


def fig_counts(cat):
    from collections import Counter
    c = Counter(r["kind"] for r in cat)
    fig = page(8.6, 5.0)
    header(fig, f"{A(len(cat))} كسوفًا للشمس بين ١٩٠١ و٢٠٥٠", "توزيع الكسوفات حسب النوع، وعددها في كل عقد")
    ax = fig.add_axes([0.58, 0.14, 0.36, 0.62])
    kinds = ["total", "annular", "hybrid", "partial"]
    vals = [c[k] for k in kinds]
    ax.barh(range(4), vals, color=[KIND_COL[k] for k in kinds], height=0.6)
    ax.set_yticks(range(4))
    ax.set_yticklabels([KIND_AR[k] for k in kinds], fontsize=11)
    for i, v in enumerate(vals):
        ax.text(v + 2, i, A(v), va="center", ha="right", fontsize=10)
    ax.invert_xaxis()
    ax.yaxis.tick_right()
    style_axes(ax, grid=False)
    ax.set_xticks([])
    ax.spines["bottom"].set_visible(False)
    ax2 = fig.add_axes([0.06, 0.14, 0.46, 0.62])
    dec = np.arange(1900, 2050, 10)
    for j, k in enumerate(kinds):
        h = [sum(1 for r in cat if r["kind"] == k and d <= r["date"][0] < d + 10) for d in dec]
        bottom = [sum(sum(1 for r in cat if r["kind"] == kk and d <= r["date"][0] < d + 10) for kk in kinds[:j]) for d in dec]
        ax2.bar(range(len(dec)), h, bottom=bottom, color=KIND_COL[k], width=0.75, edgecolor=PAPER, lw=0.8)
    ax2.set_xticks(range(0, len(dec), 3))
    ax2.set_xticklabels([A(d) for d in dec[::3]], fontsize=8.5)
    ax2.set_ylabel("العدد في العقد")
    style_axes(ax2)
    arabic_ticks(ax2, x=False)
    footer(fig, SRC + "؛ عدد الكسوفات في السنة بين ٢ و٥.")
    save(fig, CH, "eclipse_statistics", "إحصاء كسوفات الشمس ١٩٠١–٢٠٥٠ حسب النوع والعقد (محسوب).", "chart")


def fig_central_paths(cat, y0=2001, y1=2050):
    import geopandas as gpd
    from common import ROOT
    world = gpd.read_file(f"{ROOT}/data/countries_world.geojson")
    fig = page(9.5, 5.8)
    header(fig, f"مسارات الكسوفات المركزية {A(y0)}–{A(y1)}", "الكلية بالأزرق والحلقية بالبرتقالي والهجينة بالبنفسجي؛ لاحظ ندرة المرور بأي موقع بعينه")
    ax = fig.add_axes([0.03, 0.06, 0.94, 0.76])
    world.plot(ax=ax, color="#f1efea", edgecolor="#cfccc4", lw=0.3)
    ax.set_facecolor("#e8eef3")
    for r in cat:
        if not (y0 <= r["date"][0] <= y1) or r["kind"] == "partial":
            continue
        lo = np.array([np.nan if v is None else v for v in r["lon"]])
        la = np.array([np.nan if v is None else v for v in r["lat"]])
        lo[np.where(np.abs(np.diff(lo)) > 180)[0]] = np.nan
        is27 = r["date"][:3] == [2027, 8, 2]
        ax.plot(lo, la, color=RED if is27 else KIND_COL[r["kind"]], lw=2.6 if is27 else 1.1, alpha=1 if is27 else 0.85)
        if is27:
            ax.text(25, 32, "٢٠٢٧", color=RED, fontweight="bold", fontsize=11, path_effects=halo())
    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xticks([])
    ax.set_yticks([])
    footer(fig, SRC)
    save(fig, CH, f"central_paths_{y0}_{y1}", f"خطوط مركز جميع الكسوفات الكلية والحلقية والهجينة {A(y0)}–{A(y1)} (محسوبة).", "map")


# ------------------------------------------------------------------ sky during totality (computed)
BRIGHT_STARS = [  # name, RA hours, Dec deg (J2000), magnitude
    ("الشِّعرى اليمانية", 6.7525, -16.716, -1.46), ("سهيل", 6.3992, -52.696, -0.74), ("السماك الرامح", 14.2610, 19.182, -0.05),
    ("العيوق", 5.2782, 45.998, 0.08), ("رجل الجبار", 5.2423, -8.202, 0.13), ("الشعرى الشامية", 7.6550, 5.225, 0.34),
    ("منكب الجوزاء", 5.9195, 7.407, 0.5), ("الدبران", 4.5987, 16.509, 0.85), ("السماك الأعزل", 13.4199, -11.161, 0.97),
    ("رأس التوأم المؤخر", 7.7553, 28.026, 1.14), ("قلب الأسد", 10.1395, 11.967, 1.35), ("رأس التوأم المقدم", 7.5767, 31.888, 1.58),
    ("الفرد", 9.4598, -8.659, 1.98), ("ذنب الأسد", 11.8177, 14.572, 2.14), ("النسر الواقع", 18.6156, 38.784, 0.03),
]


def fig_sky_at_totality():
    from skyfield.api import Star, wgs84
    ts, eph = besselian.ephemeris()
    t = ts.ut1(2027, 8, 2, 10, 5, 19)
    obs = (eph["earth"] + wgs84.latlon(25.6872, 32.6396)).at(t)
    sun = obs.observe(eph["sun"]).apparent()
    sa, sz, _ = sun.altaz()
    fig = page(8.0, 8.0, "#06101f")
    header(fig, "سماء الأقصر لحظة ذروة الكلية", "١٣:٠٥ بتوقيت مصر الصيفي — الكواكب والنجوم الساطعة حول الشمس المحجوبة",
           color="white", sub_color="#c9d3e3")
    ax = fig.add_axes([0.10, 0.07, 0.80, 0.74], projection="polar")
    ax.set_facecolor("#0b1a33")
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(1)   # east to the left when looking up (sky chart convention)
    ax.set_rlim(0, 62)
    ax.set_yticks([20, 40, 60])
    ax.set_yticklabels([])
    ax.grid(color="#2a3d5c", lw=0.6)
    ax.set_xticks(np.radians([0, 90, 180, 270]))
    ax.set_xticklabels(["شمال", "شرق", "جنوب", "غرب"], color="#c9d3e3", fontsize=11)

    def plot(alt, az, **kw):
        ax.plot(np.radians(az), 90 - alt, **kw)

    plot(sa.degrees, sz.degrees, marker="o", ms=16, color="black", mec=CORONA, mew=2.5, zorder=5)
    ax.text(np.radians(sz.degrees), 90 - sa.degrees - 3.5, "الشمس", color=CORONA, ha="center", va="top", fontsize=11,
            path_effects=halo(2.5, "#0b1a33"))
    planets = [("venus", "الزهرة", "#fff4c2", 11), ("mercury", "عطارد", "#f0c987", 7), ("mars", "المريخ", "#ff8a65", 7),
               ("jupiter barycenter", "المشتري", "#ffe8c2", 9), ("saturn barycenter", "زحل", "#e8d8a8", 7)]
    offs = {"venus": (14, -16), "mercury": (16, 10), "mars": (0, 12), "jupiter barycenter": (-6, 14),
            "saturn barycenter": (0, 12)}
    for key, name, col, ms in planets:
        a, z, _ = obs.observe(eph[key]).apparent().altaz()
        if 90 - a.degrees < 60:
            plot(a.degrees, z.degrees, marker="o", ms=ms, color=col, zorder=6)
            ax.annotate(name, (np.radians(z.degrees), 90 - a.degrees), xytext=offs[key], textcoords="offset points",
                        color=col, fontsize=11.5, ha="center", zorder=7, fontweight="bold",
                        path_effects=halo(2.5, "#0b1a33"))
    for name, ra, dec, mag in BRIGHT_STARS:
        s = Star(ra_hours=ra, dec_degrees=dec)
        a, z, _ = obs.observe(s).apparent().altaz()
        if a.degrees > 30:
            plot(a.degrees, z.degrees, marker="*", ms=max(5, 12 - 2.5 * mag), color="white", zorder=6)
            ax.text(np.radians(z.degrees), 90 - a.degrees - 3.0, name, color="#c9d3e3", fontsize=9, ha="center",
                    va="top", path_effects=halo(2.5, "#0b1a33"))
    fig.text(0.5, 0.02, "مركز الدائرة سمت الرأس، والدائرة الخارجية على ارتفاع ٢٨° فوق الأفق. لاحظ أن الشمس تكاد تكون فوق الرأس (ارتفاعها ≈ ٨٢°).",
             ha="center", color="#c9d3e3", fontsize=9)
    save(fig, CH, "sky_during_totality_luxor", "خريطة سماء الأقصر لحظة ذروة الكلية: مواقع الكواكب والنجوم الساطعة (محسوبة).", "chart")


def fig_light_levels():
    fig = page(8.6, 5.0)
    header(fig, "كم تُظلم السماء؟", "شدة الإضاءة التقريبية (لوكس) على مقياس لوغاريتمي")
    ax = fig.add_axes([0.05, 0.12, 0.55, 0.66])
    items = [("ضوء الشمس المباشر ظهرًا", 1e5), ("نهار غائم", 1e4), ("مكتب مضاء", 500), ("كسوف جزئي ٩٩٪ (تقريبًا)", 1e3),
             ("بعد الغروب بنصف ساعة (الشفق المدني)", 3), ("أثناء الكسوف الكلي", 1), ("ضوء البدر", 0.2)]
    items.sort(key=lambda r: r[1])
    ax.barh(range(len(items)), [v for _, v in items], color=[NAVY if "الكلي" in n else BLUE[6] for n, _ in items], height=0.6)
    ax.set_xscale("log")
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels([n for n, _ in items], fontsize=9.5)
    ax.yaxis.tick_right()
    ax.invert_xaxis()
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: A(f"{v:g}")))
    style_axes(ax)
    footer(fig, "قيم تقريبية متوسطة لأغراض المقارنة؛ تختلف إضاءة الكلية بحسب حجم الظل والسحب والمسافة عن حافة المسار.")
    save(fig, CH, "light_levels", "مقارنة تقريبية لشدة الإضاءة أثناء الكسوف الكلي بمواقف يومية.", "chart")


def fig_what_changes():
    fig = page(8.6, 5.6)
    ax = canvas(fig)
    header(fig, "ما الذي يتغير من حولك أثناء الكلية؟")
    items = [("🌡", "تنخفض الحرارة بضع درجات مئوية"), ("💨", "قد تتغير الرياح وتهدأ فجأة"), ("🌅", "غروب على مدى ٣٦٠° حول الأفق"),
             ("✦", "تظهر الزهرة والكواكب اللامعة"), ("🐦", "تصمت الطيور وتعود الحيوانات إلى مأواها"), ("🌸", "تنغلق بعض الأزهار"),
             ("〰", "تتراقص الأحزمة الظلية على الجدران"), ("👁", "تتسع حدقات العين مع الظلام المفاجئ")]
    for i, (ico, txt) in enumerate(items):
        col, row = i % 2, i // 2
        x = 0.95 - col * 0.46
        y = 0.74 - row * 0.17
        card(ax, x - 0.44, y - 0.06, 0.44, 0.12)
        number_badge(ax, x - 0.04, y, i + 1, color=BLUE[8 if i % 2 else 6])
        ax.text(x - 0.08, y, txt, ha="right", va="center", fontsize=10.5)
    footer(fig, "ملاحظات شائعة سجلها الراصدون في كسوفات سابقة؛ تصلح موضوعًا لتجارب الطلاب الميدانية.")
    save(fig, CH, "what_changes", "تغيرات بيئية يلاحظها الراصدون أثناء الكسوف الكلي.")


def fig_facts_cards():
    for title, rows, slug, cap in [
        ("بطاقة تعريف: القمر", [("القطر", "٣٤٧٥ كم"), ("متوسط البعد", "٣٨٤٤٠٠ كم"), ("أقرب بعد (الحضيض)", "≈ ٣٥٦٥٠٠ كم"),
                                ("أبعد بعد (الأوج)", "≈ ٤٠٦٧٠٠ كم"), ("الشهر الاقتراني", "٢٩٫٥٣ يومًا"), ("ميل المدار", "≈ ٥٫١°"),
                                ("يبتعد عن الأرض", "≈ ٣٫٨ سم سنويًا")], "moon_facts", "بطاقة حقائق عن القمر."),
        ("بطاقة تعريف: الشمس", [("القطر", "≈ ١٫٣٩ مليون كم"), ("متوسط البعد", "١٤٩٫٦ مليون كم"), ("حرارة السطح", "≈ ٥٨٠٠ كلفن"),
                                ("حرارة اللب", "≈ ١٥ مليون كلفن"), ("حرارة الهالة", "١–٣ ملايين كلفن"), ("زمن وصول ضوئها", "≈ ٨ دقائق و٢٠ ثانية"),
                                ("العمر", "≈ ٤٫٦ مليار سنة")], "sun_facts", "بطاقة حقائق عن الشمس.")]:
        fig = page(6.0, 6.0, NAVY)
        ax = canvas(fig)
        header(fig, title, color="white")
        if "القمر" in title:
            moon_disk(ax, 0.20, 0.82, 0.07, color="#9aa6b8")
        else:
            sun_disk(ax, 0.20, 0.82, 0.07)
        for i, (k, v) in enumerate(rows):
            y = 0.66 - i * 0.09
            ax.plot([0.06, 0.94], [y - 0.04, y - 0.04], color="#2a3d5c", lw=0.8)
            ax.text(0.94, y, k, ha="right", va="center", color="#c9d3e3", fontsize=11)
            ax.text(0.06, y, v, ha="left", va="center", color="white", fontsize=11.5, fontweight="bold")
        save(fig, CH, slug, cap)


def fig_future():
    fig = page(8.6, 4.6, NAVY)
    ax = canvas(fig)
    header(fig, "هل ستبقى الكسوفات الكلية إلى الأبد؟", color="white")
    para(ax, 0.95, 0.82, "يبتعد القمر عن الأرض نحو ٣٫٨ سم كل عام، وهو ما تقيسه بدقة أشعة الليزر المرتدة من عاكسات "
         "تركها رواد أبولو على سطحه. ومع ابتعاده يصغر قرصه الظاهري تدريجيًا، فتقلّ الكسوفات الكلية وتكثر الحلقية، "
         "حتى يأتي يوم — بعد مئات الملايين من السنين وفق التقديرات — لا يقدر فيه القمر على حجب الشمس كلها.",
         width=72, size=11, color="#e6ebf2")
    for k, (lab, rr) in enumerate([("اليوم", 1.0), ("بعد ~٣٠٠ مليون سنة", 0.985), ("بعد ~٦٠٠ مليون سنة", 0.97)]):
        cx = 0.80 - k * 0.30
        sun = sun_disk(ax, cx, 0.22, 0.045, glow=False)
        if k == 0:
            corona(ax, cx, 0.22, 0.045, extent=0.4, strength=0.8)
        moon_disk(ax, cx, 0.22, 0.045 * (1.03 if k == 0 else rr - 0.03), color=NAVY, clip=sun)
        ax.text(cx, 0.07, lab, ha="center", color="white", fontsize=9.5)
    footer(fig, "الأرقام الزمنية تقديرات تقريبية تتوقف على تطور مدار القمر وحجم الشمس الظاهري.", color="#8a96a8")
    save(fig, CH, "future_of_eclipses", "ابتعاد القمر التدريجي ومستقبل الكسوفات الكلية.")


def fig_top_view_seasons():
    fig = page(8.0, 6.0, NAVY)
    ax = canvas(fig)
    header(fig, "خط العقد ومواسم الكسوف", "مرتين كل عام تقريبًا يتجه خط العقد نحو الشمس فيبدأ موسم كسوف يدوم نحو ٣٤ يومًا",
           color="white", sub_color="#c9d3e3")
    cx, cy = 0.5, 0.42
    sun_disk(ax, cx, cy, 0.05)
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(cx + 0.36 * np.cos(th), cy + 0.30 * np.sin(th), color="#2a3d5c", lw=1)
    for k, ang in enumerate(np.radians([0, 90, 180, 270])):
        ex, ey = cx + 0.36 * np.cos(ang), cy + 0.30 * np.sin(ang)
        ax.add_patch(Circ(ax, (ex, ey), 0.022, fc="#3987e5", zorder=4))
        dx, dy = 0.07 * np.cos(np.radians(35)), 0.07 * np.sin(np.radians(35))
        ax.plot([ex - dx, ex + dx], [ey - dy, ey + dy], color=RED, lw=1.6, zorder=5)
        aligned = k in (0, 2)
        ax.text(ex, ey - 0.07, "موسم كسوف" if aligned else "لا كسوف", ha="center",
                color=SUN if aligned else "#8a96a8", fontsize=10, fontweight="bold" if aligned else "normal")
    ax.text(0.94, 0.10, "الخط الأحمر: خط العقد (يدور ببطء دورة كاملة كل ١٨٫٦ سنة)", ha="right", color="#ff9b94", fontsize=9.5)
    footer(fig, "رسم تخطيطي غير مقيس؛ يبين ثبات اتجاه خط العقد تقريبًا أثناء دوران الأرض حول الشمس.", color="#8a96a8")
    save(fig, CH, "node_line_seasons", "اتجاه خط العقد وتفسير حدوث موسمين للكسوف كل عام.")


def main():
    fig_coincidence()
    fig_scale()
    fig_apparent_sizes()
    fig_shadows()
    fig_types()
    fig_solar_vs_lunar()
    fig_inclination()
    fig_top_view_seasons()
    fig_seasons_2027()
    fig_contacts()
    fig_phenomena_timeline()
    fig_diamond_ring()
    fig_bailys_beads()
    fig_corona_anatomy()
    fig_sun_structure()
    fig_facts_cards()
    fig_shadow_speed()
    fig_umbra_cone()
    fig_gamma()
    fig_magnitude_vs_obscuration()
    fig_saros_explained()
    S = saros136()
    fig_saros136_map(S)
    fig_saros136_durations(S)
    cat = eclipse_catalogue()
    fig_counts(cat)
    fig_central_paths(cat, 1951, 2000)
    fig_central_paths(cat, 2001, 2050)
    fig_sky_at_totality()
    fig_light_levels()
    fig_what_changes()
    fig_future()
    write_catalogue("ch1")


if __name__ == "__main__":
    main()
