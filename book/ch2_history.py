"""Chapter 2 — eclipses in Egypt's history (Arabic infographics and computed maps)."""
import json
import os

import numpy as np

import mapkit as MK
from common import (A, BLUE, BODY, CARD, Circ, GREEN, INK, INK2, LINE, MUTED, NAVY, ORANGE, PAPER, RED, ROOT, SUN,
                    SUN_DEEP, TITLE, arabic_ticks, arrow, canvas, card, corona, footer, halo, header, mirror_y,
                    moon_disk, number_badge, page, para, plt, save, style_axes, sun_disk, wrap, write_catalogue)
from eclipse2027 import circumstances as C, engine as E, i18n as I
from history_calc import GREG_MONTHS, HIJRI_MONTHS, hijri_from_jd, scan_historic, summarize

CH = 2
SRC = "المصدر: حسابات المؤلف"


def is_total(r, n):
    return r["sites"][n]["dur"] > 0 and r["kind"] != "annular"


def is_annular(r, n):
    return r["sites"][n]["dur"] > 0 and r["kind"] == "annular"


def date_ar(y, m, d, julian=False):
    s = f"{A(d)} {GREG_MONTHS[m - 1]} {A(y)}"
    return s + (" (بالتقويم اليولياني)" if julian else "")


def hijri_ar(jd):
    y, m, d = hijri_from_jd(jd)
    return f"{A(d)} {HIJRI_MONTHS[m - 1]} {A(y)} هـ"


# ------------------------------------------------------------------ timeline
def fig_timeline(next_luxor=None):
    fig = page(7.4, 10.4)
    ax = canvas(fig)
    header(fig, "الكسوف في مصر عبر العصور", "محطات مختارة من الأسطورة إلى الحساب الدقيق")
    ev = [("مصر القديمة", "أسطورة «رع» و«أبوفيس»: الأفعى التي تتربص بمركب الشمس، وقد رأى فيها بعض الباحثين صدى للظواهر التي تحجب الشمس."),
          ("نحو ١٠٢١م", "ابن الهيثم في القاهرة يكتب «مقالة في صورة الكسوف» ويدرس صورة الشمس المكسوفة عبر ثقب صغير."),
          ("٩٧٧ و٩٧٨م", "ابن يونس يرصد كسوفين للشمس من القاهرة ويدوّنهما في «الزيج الحاكمي الكبير»."),
          ("١٧ مايو ١٨٨٢", "كسوف كلي في سوهاج؛ بعثات أوروبية تصوّر الهالة، ويظهر مذنّب قرب الشمس سُمّي «توفيق»."),
          ("٣٠ أغسطس ١٩٠٥", "كسوف كلي يعبر صعيد مصر وأسوان."),
          ("٢٩ مارس ٢٠٠٦", "كسوف كلي في السلوم يجذب آلاف الزوار والعلماء إلى الساحل الشمالي الغربي."),
          ("٢ أغسطس ٢٠٢٧", "من أطول الكسوفات الكلية في القرن الحادي والعشرين: ٦ دقائق و٢٣ ثانية في صعيد مصر."),
          ]
    if next_luxor:
        ev.append(next_luxor)
    top, bot = 0.82, 0.07
    step = (top - bot) / (len(ev) - 1)
    ax.plot([0.74, 0.74], [bot, top], color=LINE, lw=3, zorder=1)
    for i, (when, what) in enumerate(ev):
        y = top - i * step
        hl = "٢٠٢٧" in when
        ax.add_patch(Circ(ax, (0.74, y), 0.018, fc=RED if hl else BLUE[8], ec="white", lw=1.5, zorder=3))
        ax.text(0.95, y, when, ha="right", va="center", fontsize=11, fontweight="bold", color=RED if hl else BLUE[10],
                fontfamily=TITLE)
        ax.text(0.70, y, wrap(what, 40), ha="right", va="center", fontsize=10.8, color=INK, linespacing=1.45,
                fontfamily=BODY)
    footer(fig, "التواريخ الميلادية قبل ١٥٨٢ بالتقويم اليولياني.")
    save(fig, CH, "timeline", "خط زمني لمحطات الكسوف في تاريخ مصر.")


# ------------------------------------------------------------------ text cards
def text_card(title, sub, paras, slug, caption, dark=False, icon=None, h=None):
    W = 62
    lines = [wrap(p, W).count("\n") + 1 for p in paras]
    LH, GAP = 0.31, 0.22
    body = sum(n * LH + GAP for n in lines)
    h = max(h or 0, 1.55 + body + (1.3 if icon else 0.4))
    fig = page(7.4, h, NAVY if dark else PAPER)
    ax = canvas(fig)
    header(fig, title, sub, color="white" if dark else INK, sub_color="#c9d3e3" if dark else INK2)
    y = 1 - 1.45 / h
    for p, n in zip(paras, lines):
        para(ax, 0.94, y, p, width=W, size=10.6, color="#e6ebf2" if dark else INK, linespacing=1.7)
        y -= (n * LH + GAP) / h
    if icon:
        icon(ax)
    save(fig, CH, slug, caption)


def icon_ra(ax):
    sun_disk(ax, 0.16, 0.18, 0.06)
    t = np.linspace(0, 3 * np.pi, 200)
    ax.plot(0.06 + 0.22 * t / (3 * np.pi), 0.10 + 0.03 * np.sin(t * 2), color="#7d5ba6", lw=5, solid_capstyle="round")


def fig_ibn_haytham_camera():
    fig = page(8.0, 5.0)
    ax = canvas(fig)
    header(fig, "ابن الهيثم وصورة الكسوف", "الضوء المار من ثقب صغير يرسم هلال الشمس المكسوفة مقلوبًا على الجدار")
    sun = sun_disk(ax, 0.88, 0.50, 0.05)
    moon_disk(ax, 0.86, 0.52, 0.05, color=PAPER, clip=sun)
    ax.add_patch(plt.Rectangle((0.50, 0.15), 0.012, 0.62, fc=INK2, transform=ax.transAxes))
    ax.add_patch(plt.Rectangle((0.50, 0.455), 0.012, 0.03, fc=PAPER, transform=ax.transAxes, zorder=3))
    for dy in (+0.09, -0.09):
        ax.plot([0.85, 0.15], [0.50 + dy * 0.9, 0.47 - dy * 2.4], color=SUN_DEEP, lw=0.8, alpha=0.7)
    ax.add_patch(plt.Rectangle((0.10, 0.15), 0.01, 0.62, fc="#d8d4ca", transform=ax.transAxes))
    s2 = sun_disk(ax, 0.17, 0.47, 0.045, glow=False)
    moon_disk(ax, 0.19, 0.45, 0.045, color=PAPER, clip=s2)
    ax.text(0.506, 0.82, "ثقب صغير", ha="center", fontsize=10)
    ax.text(0.17, 0.82, "صورة مقلوبة", ha="center", fontsize=10)
    ax.text(0.88, 0.82, "الشمس المكسوفة", ha="center", fontsize=10)
    para(ax, 0.5, 0.14, "درس الحسن بن الهيثم (ت. نحو ١٠٤٠م) هذه الظاهرة في القاهرة، ووضع فيها رسالته «مقالة في صورة "
         "الكسوف»، وهي أصل فكرة «الحجرة المظلمة» (الكاميرا).", width=80, size=9.6, ha="center")
    save(fig, CH, "ibn_al_haytham_camera", "مبدأ الحجرة المظلمة الذي درسه ابن الهيثم لرصد صورة الكسوف.")


# ------------------------------------------------------------------ maps of individual historical eclipses
def eclipse_map(ec, title, sub, slug, caption, bounds=(23.5, 37.5, 21.5, 32.5), backend_note="", pts=None,
                world=False):
    lon0, lon1, lat0, lat1 = bounds
    fig = plt.figure(figsize=(8.0, 7.4) if not world else (9.5, 5.8), facecolor=PAPER)
    ax = fig.add_axes([0.04, 0.09, 0.86, 0.72] if not world else [0.04, 0.10, 0.86, 0.67])
    MK.base(ax, lon0, lon1, lat0, lat1, labels=False)
    MK.field(ax, ec.B, lon0, lon1, lat0, lat1, n=300 if not world else 420)
    MK.path(ax, ec.B)
    if pts is None:
        pts = MK.EGYPT_PTS if not world else [p for p in MK.EGYPT_PTS if p[0] in ("القاهرة", "أسوان")]
    MK.cities(ax, ec.B, pts, lon0, lon1, lat0, lat1, size=8.5)
    header(fig, title, sub)
    kind = {"total": "كلي", "annular": "حلقي", "hybrid": "هجين", "partial": "جزئي"}[ec.kind]
    note = f"النوع: {kind} | ذروة الكسوف {I.fmt_time(ec.hour_ut, seconds=False)} بالتوقيت العالمي | غاما {A(f'{ec.gamma:.3f}')}"
    if ec.backend == "erfa":
        note += f" | ΔT ≈ {A(f'{ec.delta_t:,.0f}')} ث"
    fig.text(0.965, 0.835 if world else 0.845, note, ha="right", fontsize=8.6, color=INK2)
    footer(fig, (SRC + (" بنظرية ERFA (Moon98/EPV00) ومعادلات ΔT لإسبيناك ومييس؛ المواقع تقريبية بسبب عدم اليقين في ΔT."
                        if ec.backend == "erfa" else " من تقويم JPL DE421.")) + backend_note)
    save(fig, CH, slug, caption, "map")


# ------------------------------------------------------------------ catalogue-based figures (1901-2050)
def catalogue():
    return json.load(open(os.path.join(ROOT, "results", "solar_eclipses_1901_2050.json")))


EGYPT_BBOX = (24.6, 36.9, 22.0, 31.7)


def egypt_central(cat):
    import geopandas as gpd
    from shapely.geometry import LineString
    eg = MK.geo("countries_region")
    poly = eg[eg.ADM0_A3 == "EGY"].geometry.iloc[0]
    out = []
    for r in cat:
        if r["kind"] == "partial":
            continue
        pts = [(lo, la) for la, lo in zip(r["lat"], r["lon"]) if la is not None and lo is not None]
        if len(pts) < 2:
            continue
        segs = []
        cur = [pts[0]]
        for p, q in zip(pts, pts[1:]):
            if abs(q[0] - p[0]) > 90:
                segs.append(cur)
                cur = [q]
            else:
                cur.append(q)
        segs.append(cur)
        if any(len(s) > 1 and LineString(s).buffer(1.0).intersects(poly) for s in segs):
            out.append(r)
    return out


def fig_egypt_paths(cat):
    import geopandas as gpd  # noqa: F401
    eg = egypt_central(cat)
    lon0, lon1, lat0, lat1 = 18, 42, 17, 36
    fig = plt.figure(figsize=(8.4, 7.4), facecolor=PAPER)
    ax = fig.add_axes([0.04, 0.07, 0.86, 0.76])
    MK.base(ax, lon0, lon1, lat0, lat1, admin1=None)
    rows = []
    cols = plt.cm.tab10(np.linspace(0, 1, 10))
    k = 0
    for r in eg:
        ec = E.eclipse_near(E.jd_from_date(*r["date"], r["hour"]), "de421")
        t = np.linspace(-3.4, 3.4, 1600)
        la, lo, ln, on, ls, os_ = C.path_limits(ec.B, t)
        y = r["date"][0]
        col = RED if y == 2027 else (SUN_DEEP if r["kind"] == "annular" else cols[k % 10])
        if y != 2027:
            k += 1
        poly_x = np.r_[on, os_[::-1]]
        poly_y = np.r_[ln, ls[::-1]]
        ax.fill(poly_x, poly_y, color=col, alpha=0.18, zorder=2)
        ax.plot(lo, la, color=col, lw=1.6 if y != 2027 else 2.4, zorder=3)
        m = (lo > lon0 + 1) & (lo < lon1 - 1) & (la > lat0 + 1) & (la < lat1 - 1)
        if m.any():
            j = np.where(m)[0][len(np.where(m)[0]) // 3]
            ax.text(lo[j], la[j] + 0.5, A(y) + ("\n(حلقي)" if r["kind"] == "annular" else ""), color=col, fontsize=9,
                    fontweight="bold", ha="center", path_effects=halo(), zorder=7)
        rows.append((r, ec))
    header(fig, "الكسوفات المركزية التي عبرت مصر ١٩٠١–٢٠٥٠", "مسارات الكسوف الكلي والحلقي فوق مصر وما حولها (محسوبة)")
    footer(fig, SRC + " من تقويم JPL DE421.")
    save(fig, CH, "central_paths_egypt_1901_2050", "مسارات الكسوفات الكلية والحلقية التي عبرت مصر ١٩٠١–٢٠٥٠ (محسوبة).", "map")
    return rows


def fig_egypt_table(rows):
    fig = page(8.4, 1.6 + 0.42 * len(rows))
    ax = canvas(fig)
    header(fig, "جدول الكسوفات المركزية فوق مصر ١٩٠١–٢٠٥٠")
    cols = ["التاريخ", "النوع", "أطول مدة داخل مصر", "أماكن مختارة داخل المسار"]
    xs = [0.95, 0.72, 0.58, 0.40]
    y = 0.86 - 0.35 / fig.get_figheight()
    for x, c in zip(xs, cols):
        ax.text(x, y, c, ha="right", fontsize=10, fontweight="bold", color=BLUE[10])
    eg = MK.geo("countries_region")
    poly = eg[eg.ADM0_A3 == "EGY"].geometry.iloc[0]
    from shapely.geometry import Point
    for i, (r, ec) in enumerate(rows):
        yy = y - (i + 1) * 0.42 / fig.get_figheight()
        if i % 2 == 0:
            ax.add_patch(plt.Rectangle((0.03, yy - 0.18 / fig.get_figheight()), 0.94, 0.38 / fig.get_figheight(),
                                       fc="#f1efea", ec="none", transform=ax.transAxes))
        t = np.linspace(-3.4, 3.4, 1500)
        la, lo = C.central_line(ec.B, t)
        okk = np.array([np.isfinite(a) and poly.contains(Point(b, a)) for a, b in zip(la, lo)])
        kind = {"total": "كلي", "annular": "حلقي", "hybrid": "هجين"}[r["kind"]]
        if okk.any():
            rr = C.local_circumstances(ec.B, la[okk], lo[okk])
            dur = I.fmt_dur(float(np.max(rr["duration_s"]))) if r["kind"] != "annular" else "—"
        else:
            dur = "(المسار على الحدود)"
        hits = [n for n, (a, b) in [("القاهرة", (30.04, 31.24)), ("الإسكندرية", (31.2, 29.92)), ("الأقصر", (25.69, 32.64)),
                                     ("أسوان", (24.09, 32.90)), ("سوهاج", (26.56, 31.70)), ("السلوم", (31.55, 25.16)),
                                     ("مرسى مطروح", (31.35, 27.24)), ("سيوة", (29.20, 25.52)), ("الغردقة", (27.26, 33.81)),
                                     ("شرم الشيخ", (27.92, 34.33)), ("العريش", (31.13, 33.80)), ("أبو سمبل", (22.34, 31.63)),
                                     ("الخارجة", (25.44, 30.56)), ("مرسى علم", (25.07, 34.88))]
                if C.local_circumstances(ec.B, np.array([a]), np.array([b]))["umbral_margin"][0] > 0]
        vals = [date_ar(*r["date"]), kind, dur, "، ".join(hits[:5]) or "—"]
        for x, v in zip(xs, vals):
            ax.text(x, yy, v, ha="right", va="center", fontsize=9.5, color=RED if r["date"][0] == 2027 else INK)
    footer(fig, SRC + " من تقويم JPL DE421.")
    save(fig, CH, "central_eclipses_egypt_table", "جدول الكسوفات المركزية فوق مصر ١٩٠١–٢٠٥٠ (محسوب).")


def fig_cairo_luxor_series(cat):
    rows = []
    for r in cat:
        if r["date"][0] < 1901:
            continue
        ec = E.eclipse_near(E.jd_from_date(*r["date"], r["hour"]), "de421")
        s = summarize(ec, {"القاهرة": (30.0444, 31.2357), "الأقصر": (25.6872, 32.6396)})
        rows.append((r, s))
    fig = page(9.0, 5.6)
    header(fig, "كل كسوف شمسي شوهد من القاهرة والأقصر ١٩٠١–٢٠٥٠", "نسبة احتجاب قرص الشمس عند الذروة (النقاط الحمراء = كسوف كلي)")
    for k, city in enumerate(["القاهرة", "الأقصر"]):
        ax = fig.add_axes([0.07, 0.48 - k * 0.38, 0.84, 0.30])
        xs, ys, cs = [], [], []
        for r, s in rows:
            v = s[city]
            if v["obsc"] <= 0:
                continue
            xs.append(r["date"][0] + (r["date"][1] - 0.5) / 12)
            ys.append(v["obsc"] * 100)
            cs.append(RED if v["dur"] > 0 else (SUN_DEEP if r["kind"] == "annular" and v["obsc"] > 0.8 else BLUE[7]))
        ax.vlines(xs, 0, ys, color=LINE, lw=1)
        ax.scatter(xs, ys, c=cs, s=26, zorder=3, edgecolor="white", lw=0.6)
        for x, y, c in zip(xs, ys, cs):
            if y > 85:
                ax.text(x, y + 6, A(int(x)), ha="center", fontsize=7.5, color=INK2)
        ax.set_ylim(0, 118)
        ax.set_xlim(1898, 2053)
        ax.set_ylabel(city, fontsize=11, fontweight="bold")
        style_axes(ax)
        arabic_ticks(ax, fmt="{:.0f}")
        mirror_y(ax)
        ax.text(0.01, 0.92, f"{A(len(xs))} كسوفًا", transform=ax.transAxes, fontsize=9, color=INK2)
    footer(fig, SRC + " من تقويم JPL DE421.")
    save(fig, CH, "cairo_luxor_all_eclipses", "نسبة الاحتجاب في القاهرة والأقصر لكل كسوف ١٩٠١–٢٠٥٠ (محسوبة).", "chart")
    return rows


# ------------------------------------------------------------------ historical scan figures
def fig_historic_timeline(hist):
    fig = page(9.0, 4.8)
    header(fig, "الكسوفات المركزية فوق أربع مدن مصرية منذ عام ١٠٠٠م", "كل نقطة كسوف كلي (أزرق) أو حلقي (برتقالي) مرّ مساره فوق المدينة")
    ax = fig.add_axes([0.06, 0.14, 0.76, 0.62])
    names = ["القاهرة", "الإسكندرية", "الأقصر", "أسوان"]
    extra = []
    for r in catalogue_central_sites():
        extra.append(r)
    for k, n in enumerate(names):
        ax.axhline(k, color=LINE, lw=1)
        for r in hist + extra:
            tot = is_total(r, n)
            ann = is_annular(r, n)
            if not (tot or ann):
                continue
            x = r["date"][0] + (r["date"][1] - 0.5) / 12
            ax.plot(x, k, "o", ms=9, color=RED if r["date"][0] == 2027 else (BLUE[9] if tot else SUN_DEEP),
                    mec="white", zorder=3)
            ax.text(x, k + 0.22, A(r["date"][0]), ha="center", fontsize=7.5, color=INK2, rotation=90 if False else 0)
    ax.set_yticks(range(4))
    ax.set_yticklabels(names, fontsize=11)
    ax.yaxis.tick_right()
    ax.set_ylim(-0.6, 3.7)
    ax.set_xlim(990, 2060)
    style_axes(ax, grid=False)
    arabic_ticks(ax, y=False, fmt="{:.0f}")
    footer(fig, SRC + ": قبل ١٩٠٠ بنظرية ERFA ومعادلات ΔT (تقريبية)، وبعدها من DE421. التقويم يولياني قبل ١٥٨٢.")
    save(fig, CH, "central_eclipses_four_cities_1000_2050", "الكسوفات الكلية والحلقية فوق القاهرة والإسكندرية والأقصر وأسوان منذ ١٠٠٠م (محسوبة).", "chart")


_CC = None


def catalogue_central_sites():
    global _CC
    if _CC is not None:
        return _CC
    cat = catalogue()
    out = []
    from history_calc import SITES
    for r in cat:
        if r["kind"] == "partial":
            continue
        ec = E.eclipse_near(E.jd_from_date(*r["date"], r["hour"]), "de421")
        s = summarize(ec)
        if any(v["dur"] > 0 for v in s.values()):
            out.append(dict(date=list(ec.date), kind=ec.kind, sites=s))
    _CC = out
    return out


def fig_wait_times(hist):
    names = ["القاهرة", "الإسكندرية", "الأقصر", "أسوان"]
    allr = hist + catalogue_central_sites()
    fig = page(8.4, 5.0)
    ax = canvas(fig)
    header(fig, "متى رأت مدن مصر الكسوف الكلي آخر مرة؟", "آخر كسوف كلي (قبل ٢٠٢٧) فوق كل مدينة، محسوبًا منذ عام ١٠٠٠م")
    for i, n in enumerate(names):
        tots = sorted([r for r in allr if is_total(r, n) and r["date"][0] < 2027], key=lambda r: r["date"])
        y = 0.72 - i * 0.16
        card(ax, 0.04, y - 0.06, 0.92, 0.12)
        ax.text(0.94, y, n, ha="right", va="center", fontsize=13, fontweight="bold", fontfamily=TITLE)
        if tots:
            last = tots[-1]
            d = last["date"]
            txt = f"آخر كلي: {date_ar(*d, julian=d[0] < 1582)} — مدته هناك {I.fmt_dur(last['sites'][n]['dur'], long=True)}"
            gap = 2027 - d[0]
        else:
            txt, gap = "لم يمر فوقها كسوف كلي منذ عام ١٠٠٠م", None
        ax.text(0.74, y, txt, ha="right", va="center", fontsize=9.8)
        will = n in ("الأقصر",)
        if will:
            ax.text(0.10, y, "٢٠٢٧ ✓", ha="center", va="center", fontsize=11, color=GREEN, fontweight="bold")
        elif n == "أسوان":
            ax.text(0.10, y, "٢٠٢٧: ٩٩٫٨٪", ha="center", va="center", fontsize=9.5, color=SUN_DEEP)
        else:
            ax.text(0.10, y, "٢٠٢٧: جزئي", ha="center", va="center", fontsize=9.5, color=INK2)
    footer(fig, SRC + "؛ قبل ١٩٠٠ بحساب تقريبي (ERFA + ΔT)، وبعدها من DE421.")
    save(fig, CH, "last_total_eclipse_cities", "آخر كسوف كلي شهدته القاهرة والإسكندرية والأقصر وأسوان (محسوب).")


# ------------------------------------------------------------------ monuments
MONUMENTS = [("معبد الكرنك", 25.7188, 32.6573), ("معبد الأقصر", 25.6995, 32.6391), ("وادي الملوك", 25.7402, 32.6014),
             ("الدير البحري", 25.7380, 32.6065), ("مدينة هابو", 25.7195, 32.6006), ("تمثالا ممنون", 25.7206, 32.6104),
             ("معبد دندرة", 26.1418, 32.6702), ("معبد أبيدوس", 26.1847, 31.9190), ("معبد إسنا", 25.2930, 32.5545),
             ("معبد إدفو", 24.9779, 32.8734), ("معبد كوم أمبو", 24.4520, 32.9285), ("تل العمارنة", 27.6450, 30.8960),
             ("الأشمونين", 27.7810, 30.8040), ("بني حسن", 27.9333, 30.8833), ("معبد فيلة", 24.0254, 32.8844),
             ("أبو سمبل", 22.3372, 31.6258), ("أهرامات الجيزة", 29.9792, 31.1342), ("سقارة", 29.8713, 31.2165),
             ("دير سانت كاترين", 28.5559, 33.9761), ("معبد آمون في سيوة", 29.2000, 25.5430)]


def fig_monuments_chart():
    from eclipse2027 import besselian
    B = besselian.compute()
    vals = []
    for n, la, lo in MONUMENTS:
        r = C.local_circumstances(B, np.array([la]), np.array([lo]))
        vals.append((n, float(r["duration_s"][0]), float(r["obscuration"][0])))
    vals.sort(key=lambda v: (v[1], v[2]))
    fig = page(8.4, 7.0)
    header(fig, "آثار مصر تحت ظل القمر", "مدة الكسوف الكلي يوم ٢ أغسطس ٢٠٢٧ عند أشهر المواقع الأثرية")
    ax = fig.add_axes([0.06, 0.08, 0.62, 0.78])
    ys = np.arange(len(vals))
    ax.barh(ys, [v[1] / 60 for v in vals], color=[BLUE[9] if v[1] > 0 else LINE for v in vals], height=0.62)
    for y, (n, d, o) in zip(ys, vals):
        ax.text((d / 60 if d > 0 else 0) + 0.08, y, I.fmt_dur(d) if d > 0 else ("جزئي " + I.pct(o * 100)), va="center",
                fontsize=8.8, color=INK if d > 0 else INK2, ha="right")
    ax.set_yticks(ys)
    ax.set_yticklabels([v[0] for v in vals], fontsize=10)
    ax.yaxis.tick_right()
    ax.invert_xaxis()
    ax.set_xlim(7.6, 0)
    ax.set_xlabel("مدة الكلية (دقيقة)")
    style_axes(ax)
    arabic_ticks(ax, y=False)
    footer(fig, SRC + " من تقويم JPL DE421؛ الراصد عند مستوى سطح البحر.")
    save(fig, CH, "monuments_durations", "مدة الكلية عند المواقع الأثرية المصرية في ٢٠٢٧ (محسوبة).", "chart")


def fig_monuments_map():
    from eclipse2027 import besselian
    B = besselian.compute()
    lon0, lon1, lat0, lat1 = 30.6, 33.6, 24.2, 27.0
    fig = plt.figure(figsize=(8.0, 8.4), facecolor=PAPER)
    ax = fig.add_axes([0.05, 0.06, 0.84, 0.80])
    MK.base(ax, lon0, lon1, lat0, lat1, labels=True)
    MK.field(ax, B, lon0, lon1, lat0, lat1, n=300)
    MK.path(ax, B, -1.7, 1.95)
    for n, la, lo in MONUMENTS:
        if lon0 < lo < lon1 and lat0 < la < lat1:
            ax.plot(lo, la, marker="^", ms=8, color="#7a4f1f", mec="white", zorder=8)
    # label only well-separated sites
    shown = []
    for n, la, lo in MONUMENTS:
        if lon0 < lo < lon1 and lat0 < la < lat1 and all(np.hypot(la - a, lo - b) > 0.17 for a, b in shown):
            shown.append((la, lo))
            r = C.local_circumstances(B, np.array([la]), np.array([lo]))
            ax.annotate(n + "\n" + I.fmt_dur(r["duration_s"][0]), (lo, la), xytext=(-6, 2), textcoords="offset points",
                        ha="right", fontsize=8.6, path_effects=halo(), zorder=9)
    header(fig, "المواقع الأثرية في مسار الكلية", "وادي النيل من المنيا إلى أسوان يوم ٢ أغسطس ٢٠٢٧")
    footer(fig, SRC + " من تقويم JPL DE421.")
    save(fig, CH, "monuments_map", "خريطة المواقع الأثرية في وادي النيل داخل مسار الكلية ومدتها (محسوبة).", "map")


def main():
    hist = scan_historic()
    luxor_next = None
    # dedicated maps
    eb = E.eclipse_near(E.jd_from_date(977, 12, 13, 8), "erfa")
    ec978 = E.eclipse_near(E.jd_from_date(978, 6, 8, 12), "erfa")
    e1882 = E.eclipse_near(E.jd_from_date(1882, 5, 17, 8), "erfa")
    e1905 = E.eclipse_near(E.jd_from_date(1905, 8, 30, 13), "de421")
    e2006 = E.eclipse_near(E.jd_from_date(2006, 3, 29, 10), "de421")

    fig_timeline()
    text_card("رع وأبوفيس: الشمس في الأسطورة المصرية", "قراءة في المعتقد لا في الحساب",
              ["كان «رع» إله الشمس في مصر القديمة يعبر السماء نهارًا في مركب، ثم يعبر العالم السفلي ليلًا. وفي طريقه تتربص به "
               "الأفعى العملاقة «أبوفيس» (عبب)، رمز الفوضى والظلام، محاولةً ابتلاع المركب.",
               "تصف النصوص الجنائزية انتصار رع كل صباح. ويرى بعض الباحثين في هذا الصراع صدى لظواهر سماوية تحجب الشمس، غير أن "
               "النصوص المصرية القديمة المعروفة لا تتضمن وصفًا صريحًا ومؤرخًا بدقة لكسوف شمسي بعينه.",
               "وفي هذا درس منهجي: الأسطورة تخبرنا بما شعر به الناس، أما الحساب الفلكي فيخبرنا بما حدث فعلًا وأين ومتى."],
              "myth_ra_apophis", "أسطورة رع وأبوفيس وعلاقتها المحتملة بالظواهر التي تحجب الشمس.", dark=True, icon=icon_ra)
    text_card("المصريون القدماء والسماء", "إرث فلكي سبق الكسوف إلى الحساب",
              ["وضع المصريون القدماء تقويمًا مدنيًا من ٣٦٥ يومًا: اثنا عشر شهرًا في كل منها ثلاثون يومًا، تُضاف إليها خمسة أيام.",
               "وقسّموا الليل بستة وثلاثين نجمًا أو مجموعة نجمية تُعرف بـ«العشريات» تشرق تباعًا، فكانت ساعة نجمية لقياس الوقت.",
               "وارتبط الشروق الاحتراقي لنجم الشعرى اليمانية (سبدت) قبيل الفجر ببدء فيضان النيل، فكان علامة على العام الجديد.",
               "ويضم معبد دندرة سقفًا فلكيًا شهيرًا (الزودياك الدائري، والأصل محفوظ في متحف اللوفر) — والمعبد نفسه يقع داخل مسار "
               "كلية ٢٠٢٧، حيث تدوم نحو ست دقائق وثلاث عشرة ثانية."],
              "ancient_egyptian_astronomy", "ملامح من علم الفلك في مصر القديمة.", h=6.6)
    fig_ibn_haytham_camera()
    s977 = summarize(eb)["القاهرة"]
    s978 = summarize(ec978)["القاهرة"]
    text_card("ابن يونس المصري: راصد كسوفات القاهرة", "علي بن عبد الرحمن بن يونس (ت. ٣٩٩هـ / ١٠٠٩م)",
              ["عمل ابن يونس فلكيًا في القاهرة زمن الخليفتين العزيز والحاكم بأمر الله، وصنّف «الزيج الحاكمي الكبير» الذي جمع فيه "
               "أرصاده وأرصاد من سبقه.",
               f"سجّل رصد كسوفين للشمس من القاهرة: الأول في {date_ar(977, 12, 13)} (يوافق تقريبًا {hijri_ar(eb.jd_ut)})، "
               f"والثاني في {date_ar(978, 6, 8)} (يوافق تقريبًا {hijri_ar(ec978.jd_ut)}).",
               f"يقدّر حسابنا الحديث احتجاب الشمس في القاهرة بنحو {I.pct(s977['obsc'] * 100, 0)} في الأول و{I.pct(s978['obsc'] * 100, 0)} في الثاني.",
               "وقد اعتمد فلكيو العصر الحديث على أرصاده — ضمن سجلات تاريخية أخرى — في قياس تباطؤ دوران الأرض عبر القرون (ΔT)."],
              "ibn_yunus", "ابن يونس وأرصاده لكسوفي ٩٧٧ و٩٧٨م في القاهرة.", h=6.4)
    eclipse_map(eb, "كسوف ١٣ ديسمبر ٩٧٧م كما رُصد من القاهرة", "رصده ابن يونس؛ المسار الكلي مرّ جنوب مصر",
                "eclipse_977", "خريطة كسوف ٩٧٧م الذي رصده ابن يونس من القاهرة (محسوبة تقريبيًا).",
                bounds=(10, 60, 0, 38), world=True)
    eclipse_map(ec978, "الكسوف الحلقي في ٨ يونيو ٩٧٨م", "رصده ابن يونس جزئيًا من القاهرة",
                "eclipse_978", "خريطة الكسوف الحلقي سنة ٩٧٨م (محسوبة تقريبيًا).", bounds=(-10, 60, 0, 45), world=True)
    eclipse_map(e1882, "كسوف سوهاج الكلي — ١٧ مايو ١٨٨٢", "عبر الظل صعيد مصر صباحًا وشوهد فيه «مذنب توفيق» قرب الشمس",
                "eclipse_1882_sohag", "خريطة كسوف ١٨٨٢ الكلي فوق سوهاج (محسوبة).")
    text_card("كسوف ١٨٨٢ ومذنّب «توفيق»", "حين التقطت عدسات القرن التاسع عشر هالة الشمس من صعيد مصر",
              ["في صباح ١٧ مايو ١٨٨٢ عبر ظل القمر صعيد مصر، فتوافدت بعثات علمية أوروبية إلى سوهاج لرصده وتصويره بالألواح الفوتوغرافية "
               "الحديثة آنذاك.",
               f"دامت الكلية في سوهاج — وفق حسابنا — نحو {I.fmt_dur(summarize(e1882, {'سوهاج': (26.5591, 31.6957)})['سوهاج']['dur'], long=True)}.",
               "وفي أثناء الكلية ظهر مذنّب لامع قريب جدًا من الشمس لم يكن معروفًا من قبل، وسُجّل في الصور، ثم سُمّي «مذنّب توفيق» "
               "نسبةً إلى الخديوي توفيق. ولم يُرَ المذنب مرة أخرى بعد ذلك.",
               "يظل هذا الحدث مثالًا على قيمة الكسوف الكلي: دقائق قليلة تكشف ما يخفيه ضوء الشمس الباهر."],
              "eclipse_1882_comet_tewfik", "كسوف ١٨٨٢ في سوهاج واكتشاف مذنب توفيق.", dark=True, h=6.2)
    eclipse_map(e1905, "كسوف ٣٠ أغسطس ١٩٠٥", "مر المسار الكلي فوق أسوان وجنوب صعيد مصر بعد الظهر",
                "eclipse_1905", "خريطة كسوف ١٩٠٥ الكلي فوق جنوب مصر (محسوبة).")
    eclipse_map(e2006, "كسوف السلوم الكلي — ٢٩ مارس ٢٠٠٦", "أقرب كسوف كلي إلى ذاكرة المصريين قبل ٢٠٢٧",
                "eclipse_2006_salloum", "خريطة كسوف ٢٠٠٦ الكلي فوق السلوم وشمال غرب مصر (محسوبة).",
                bounds=(19.0, 36.0, 21.5, 34.0))
    s06 = summarize(e2006, {"السلوم": (31.55, 25.16), "القاهرة": (30.0444, 31.2357)})
    text_card("كسوف السلوم ٢٠٠٦", "حدث علمي وسياحي على الساحل الشمالي الغربي",
              [f"في ظهيرة ٢٩ مارس ٢٠٠٦ مرّ ظل القمر فوق السلوم قرب الحدود الليبية، فدامت الكلية نحو "
               f"{I.fmt_dur(s06['السلوم']['dur'], long=True)} (حسابنا)، بينما شهدت القاهرة كسوفًا جزئيًا بنسبة {I.pct(s06['القاهرة']['obsc'] * 100, 0)}.",
               "أقيم في السلوم مخيم كبير استقبل آلاف الزوار والعلماء وهواة الفلك من أنحاء العالم، وكان تجربة مصرية ناجحة في تنظيم "
               "سياحة الكسوف.",
               "وتأتي سنة ٢٠٢٧ بفرصة أكبر: مدة أطول تقارب ثلاثة أضعاف، ومسار يمر بمدن كبرى ومواقع أثرية عالمية."],
              "eclipse_2006_story", "كسوف السلوم ٢٠٠٦ مقارنة بكسوف ٢٠٢٧.", h=5.6)
    cat = catalogue()
    rows = fig_egypt_paths(cat)
    fig_egypt_table(rows)
    fig_cairo_luxor_series(cat)
    fig_historic_timeline(hist)
    fig_wait_times(hist)
    fig_monuments_chart()
    fig_monuments_map()
    write_catalogue("ch2")


if __name__ == "__main__":
    main()
