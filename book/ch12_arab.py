"""Chapter 12 — the eclipse across the Arab world: local circumstances for Arab cities and detailed strip maps
of the path of totality (computed from NASA's Besselian elements), in the manner of eclipse-guide path maps.
"""
import numpy as np

import mapkit as MK
from common import (A, BLUE, INK, INK2, LINE, MUTED, NAVY, PAPER, RED, ROOT, SUN, SUN_DEEP, TITLE, canvas, card,
                    footer, halo, header, number_badge, page, para, plt, save, wrap, write_catalogue)
from eclipse2027 import besselian, circumstances as C, i18n as I

CH = 12
B = besselian.elements()
SRC = "المصدر: حسابات المؤلف من عناصر بِسِل المنشورة لدى ناسا (إسبيناك، ΔT = ٧٦ ث)"
SEA, LANDC, OTHER = "#a9cbe8", "#efe6cf", "#e4dcc6"

# country, UTC offset on 2 August 2027, cities (Arabic name, lat, lon)
ARAB = [
    ("المغرب", 1, [("طنجة", 35.7595, -5.8340), ("تطوان", 35.5785, -5.3684), ("العرائش", 35.1932, -6.1557),
                   ("الحسيمة", 35.2517, -3.9372), ("الناظور", 35.1681, -2.9335), ("وجدة", 34.6814, -1.9086),
                   ("فاس", 34.0181, -5.0078), ("الرباط", 34.0209, -6.8416), ("الدار البيضاء", 33.5731, -7.5898),
                   ("مراكش", 31.6295, -7.9811)]),
    ("الجزائر", 1, [("وهران", 35.6969, -0.6331), ("تلمسان", 34.8783, -1.3150), ("الشلف", 36.1650, 1.3340),
                    ("البليدة", 36.4700, 2.8300), ("الجزائر العاصمة", 36.7538, 3.0588), ("سطيف", 36.1900, 5.4100),
                    ("باتنة", 35.5559, 6.1741), ("قسنطينة", 36.3650, 6.6147), ("عنابة", 36.9000, 7.7667),
                    ("بسكرة", 34.8500, 5.7300), ("تبسة", 35.4042, 8.1242)]),
    ("تونس", 1, [("تونس العاصمة", 36.8065, 10.1815), ("بنزرت", 37.2744, 9.8739), ("سوسة", 35.8256, 10.6084),
                 ("القيروان", 35.6781, 10.0963), ("صفاقس", 34.7406, 10.7603), ("قابس", 33.8815, 10.0982),
                 ("جربة", 33.8756, 10.8575)]),
    ("ليبيا", 2, [("طرابلس", 32.8872, 13.1913), ("مصراتة", 32.3754, 15.0925), ("سرت", 31.2089, 16.5887),
                  ("أجدابيا", 30.7554, 20.2263), ("بنغازي", 32.1167, 20.0667), ("درنة", 32.7648, 22.6391),
                  ("طبرق", 32.0836, 23.9764), ("سبها", 27.0377, 14.4283), ("الكفرة", 24.1833, 23.2833)]),
    ("مصر", 3, [("مرسى مطروح", 31.3543, 27.2373), ("سيوة", 29.2032, 25.5195), ("الإسكندرية", 31.2001, 29.9187),
                ("القاهرة", 30.0444, 31.2357), ("الباويطي", 28.3490, 28.8650), ("المنيا", 28.1099, 30.7503),
                ("أسيوط", 27.1783, 31.1859), ("سوهاج", 26.5591, 31.6957), ("جرجا", 26.3380, 31.8910),
                ("قنا", 26.1551, 32.7160), ("الأقصر", 25.6872, 32.6396), ("أسوان", 24.0889, 32.8998),
                ("الغردقة", 27.2579, 33.8116), ("مرسى علم", 25.0676, 34.8790), ("الخارجة", 25.4390, 30.5586)]),
    ("السودان", 2, [("وادي حلفا", 21.7972, 31.3711), ("دنقلا", 19.1653, 30.4833), ("بورتسودان", 19.6158, 37.2164),
                    ("الخرطوم", 15.5007, 32.5599)]),
    ("السعودية", 3, [("تبوك", 28.3835, 36.5662), ("ينبع", 24.0895, 38.0618), ("المدينة المنورة", 24.5247, 39.5692),
                     ("جدة", 21.4858, 39.1925), ("مكة المكرمة", 21.3891, 39.8579), ("الطائف", 21.2703, 40.4158),
                     ("الباحة", 20.0129, 41.4677), ("أبها", 18.2164, 42.5053), ("خميس مشيط", 18.3000, 42.7333),
                     ("جازان", 16.8892, 42.5511), ("نجران", 17.4917, 44.1322), ("الرياض", 24.7136, 46.6753),
                     ("الدمام", 26.4207, 50.0888)]),
    ("اليمن", 3, [("صعدة", 16.9400, 43.7600), ("الحديدة", 14.7978, 42.9545), ("صنعاء", 15.3694, 44.1910),
                  ("تعز", 13.5795, 44.0209), ("عدن", 12.7855, 45.0187), ("المكلا", 14.5425, 49.1242)]),
    ("جيبوتي", 3, [("جيبوتي", 11.5721, 43.1456)]),
    ("الصومال", 3, [("بوصاصو", 11.2842, 49.1816), ("بربرة", 10.4396, 45.0143), ("هرجيسا", 9.5600, 44.0650),
                    ("مقديشو", 2.0469, 45.3182)]),
    ("الأردن", 3, [("العقبة", 29.5320, 35.0063), ("عمّان", 31.9454, 35.9284)]),
    ("فلسطين", 3, [("غزة", 31.5017, 34.4668), ("القدس", 31.7683, 35.2137)]),
    ("لبنان", 3, [("بيروت", 33.8938, 35.5018)]),
    ("سوريا", 3, [("دمشق", 33.5138, 36.2765), ("حلب", 36.2021, 37.1343)]),
    ("العراق", 3, [("بغداد", 33.3152, 44.3661), ("الموصل", 36.3400, 43.1300), ("البصرة", 30.5085, 47.7804)]),
    ("الكويت", 3, [("الكويت", 29.3759, 47.9774)]),
    ("البحرين", 3, [("المنامة", 26.2285, 50.5860)]),
    ("قطر", 3, [("الدوحة", 25.2854, 51.5310)]),
    ("الإمارات", 4, [("أبوظبي", 24.4539, 54.3773), ("دبي", 25.2048, 55.2708)]),
    ("عُمان", 4, [("مسقط", 23.5880, 58.3829), ("صلالة", 17.0151, 54.0924)]),
    ("موريتانيا", 0, [("نواكشوط", 18.0735, -15.9582)]),
]


def compute():
    rows = []
    for country, utc, cities in ARAB:
        la = np.array([c[1] for c in cities])
        lo = np.array([c[2] for c in cities])
        r = C.local_circumstances(B, la, lo)
        for k, (name, a, b) in enumerate(cities):
            rows.append(dict(country=country, utc=utc, name=name, lat=a, lon=b,
                             **{key: float(np.ravel(v)[k]) for key, v in r.items() if np.ndim(v)}))
    return rows


def T(h, utc):
    return I.fmt_time(h + utc) if np.isfinite(h) else "—"


# ------------------------------------------------------------------ tables (eclipse-guide style)
def table_pages(rows, total, title, sub, slug, per=30):
    sel = [r for r in rows if (r["duration_s"] > 0) == total and r["magnitude"] > 0]
    order = [c for c, _, _ in ARAB]
    sel.sort(key=lambda r: (order.index(r["country"]), -r["duration_s"], -r["obscuration"]))
    # paginate into pages of similar length, preferring breaks between countries
    npg = int(np.ceil(len(sel) / per))
    per = int(np.ceil(len(sel) / npg))
    pages, cur = [], []
    for r in sel:
        if len(cur) >= per - 3 and cur[-1]["country"] != r["country"] and len(pages) < npg - 1:
            pages.append(cur)
            cur = []
        cur.append(r)
    if cur:
        pages.append(cur)
    if total:
        cols = [(0.965, "المدينة"), (0.79, "بداية الجزئي"), (0.665, "بداية الكلي"), (0.54, "الذروة"), (0.415, "نهاية الكلي"),
                (0.30, "نهاية الجزئي"), (0.185, "مدة الكلية"), (0.085, "الارتفاع")]
    else:
        cols = [(0.965, "المدينة"), (0.79, "بداية الكسوف"), (0.64, "الذروة"), (0.49, "نهاية الكسوف"), (0.35, "القدر"),
                (0.22, "الاحتجاب"), (0.09, "الارتفاع")]
    for p, chunk in enumerate(pages, 1):
        nrows = len(chunk) + len({r["country"] for r in chunk})
        H = 2.0 + 0.27 * nrows
        fig = page(9.0, H)
        ax = canvas(fig)
        header(fig, title + (f" ({A(p)} من {A(len(pages))})" if len(pages) > 1 else ""), sub)
        top = 1 - 1.30 / H
        ax.add_patch(plt.Rectangle((0.02, top - 0.17 / H), 0.96, 0.34 / H, fc=NAVY, ec="none"))
        for x, c in cols:
            ax.text(x, top, c, ha="right", va="center", fontsize=8.8, color="white", fontweight="bold")
        rh = 0.27 / H
        y = top - 0.17 / H - rh / 2
        last = None
        k = 0
        for r in chunk:
            if r["country"] != last:
                ax.add_patch(plt.Rectangle((0.02, y - rh / 2), 0.96, rh, fc="#d8e6f6", ec="none"))
                tz = "ت.ع" + ("" if r["utc"] == 0 else f"{'+' if r['utc'] > 0 else '−'}{A(abs(r['utc']))}")
                ax.text(0.965, y, f"{r['country']}  (التوقيت المحلي: {tz})", ha="right", va="center", fontsize=9,
                        fontweight="bold", color=NAVY)
                last = r["country"]
                y -= rh
                k = 0
            if k % 2:
                ax.add_patch(plt.Rectangle((0.02, y - rh / 2), 0.96, rh, fc="#f4f1ea", ec="none"))
            u = r["utc"]
            if total:
                vals = [r["name"], T(r["c1"], u), T(r["c2"], u), T(r["tmax"], u), T(r["c3"], u), T(r["c4"], u),
                        I.fmt_dur(r["duration_s"]), A(f"{r['sun_alt_deg']:.0f}") + "°"]
            else:
                vals = [r["name"], T(r["c1"], u), T(r["tmax"], u), T(r["c4"], u), A(f"{r['magnitude']:.3f}"),
                        I.pct(r["obscuration"] * 100, 1 if r["obscuration"] > 0.995 else 0),
                        A(f"{r['sun_alt_deg']:.0f}") + "°"]
            for (x, _), v in zip(cols, vals):
                ax.text(x, y, v, ha="right", va="center", fontsize=8.6,
                        color=RED if (total and x == 0.185) else INK, fontweight="bold" if x == 0.965 else "normal")
            y -= rh
            k += 1
        footer(fig, SRC + ". الأوقات بالتوقيت المحلي لكل دولة (بما فيه التوقيت الصيفي)، والثواني مقرّبة؛ الراصد عند مستوى سطح البحر.")
        save(fig, CH, f"{slug}_{p}", title + " (محسوب).")


# ------------------------------------------------------------------ strip maps of the path
STRIPS = [
    ("مضيق جبل طارق وشمال المغرب", -8.5, 1.5, 32.6, 38.2),
    ("الجزائر", -1.5, 9.5, 32.0, 38.0),
    ("تونس وغرب ليبيا", 7.0, 17.5, 29.5, 38.0),
    ("ليبيا", 15.0, 26.5, 25.5, 33.5),
    ("غرب مصر: سيوة والواحات", 23.8, 31.6, 24.8, 31.8),
    ("وادي النيل: من المنيا إلى أسوان", 29.6, 35.0, 23.3, 29.0),
    ("البحر الأحمر وغرب السعودية", 33.0, 44.5, 15.8, 26.5),
    ("جنوب السعودية واليمن والقرن الأفريقي", 40.0, 52.5, 7.0, 19.5),
]


# road-map palette (in the manner of web road maps; all data are open: Natural Earth)
RM_WATER, RM_LAND, RM_URBAN = "#aadaff", "#f4f1ea", "#e6e1d6"
RM_MAJOR, RM_MAJOR_EDGE, RM_ROAD, RM_ROAD_EDGE = "#fdd17a", "#e3a33a", "#ffffff", "#cfc3ad"
SEAS = [("البحر المتوسط", 17.0, 35.4), ("البحر المتوسط", 3.0, 37.6), ("البحر المتوسط", 27.5, 33.0),
        ("المحيط الأطلسي", -7.4, 34.2), ("البحر الأحمر", 37.6, 21.6), ("البحر الأحمر", 34.8, 25.6),
        ("خليج عدن", 47.5, 12.3), ("بحر العرب", 51.0, 15.2)]


def strip_map(k, title, lon0, lon1, lat0, lat1, rows):
    from matplotlib import patheffects as pe
    W = 8.6
    asp = (lon1 - lon0) * np.cos(np.radians(0.5 * (lat0 + lat1))) / (lat1 - lat0)
    mh = 7.2 if asp < 1.2 else W * 0.92 / asp
    H = mh + 1.75
    fig = plt.figure(figsize=(W, H), facecolor=PAPER)
    ax = fig.add_axes([0.04, 0.8 / H, 0.92, mh / H])
    ax.set_facecolor(RM_WATER)
    sl = (slice(lon0 - 2, lon1 + 2), slice(lat0 - 2, lat1 + 2))
    ctr = MK.geo("countries_region").cx[sl[0], sl[1]]
    ctr.plot(ax=ax, color=RM_LAND, edgecolor="none", zorder=1)
    ctr.boundary.plot(ax=ax, color="#9c8fb0", linewidth=1.0, linestyle=(0, (4, 2)), zorder=3)
    MK.geo("urban_region").cx[sl[0], sl[1]].plot(ax=ax, color=RM_URBAN, edgecolor="none", zorder=1.5)
    MK.geo("lakes10_region").cx[sl[0], sl[1]].plot(ax=ax, color=RM_WATER, edgecolor="none", zorder=1.6)
    try:
        MK.geo("rivers_region").cx[sl[0], sl[1]].plot(ax=ax, color=RM_WATER, linewidth=1.6, zorder=1.7)
    except Exception:
        pass
    roads = MK.geo("roads_region").cx[sl[0], sl[1]]
    major = roads[roads["type"].isin(["Major Highway"])]
    minor = roads[roads["type"].isin(["Secondary Highway", "Road"])]
    for g, edge, fill, w in ((minor, RM_ROAD_EDGE, RM_ROAD, 1.0), (major, RM_MAJOR_EDGE, RM_MAJOR, 1.7)):
        if len(g):
            g.plot(ax=ax, color=edge, linewidth=w + 0.9, zorder=2)
            g.plot(ax=ax, color=fill, linewidth=w, zorder=2.1)
    shields = []          # route numbers exist in the open data for Europe only, so none are drawn
    # --- the eclipse path (computed)
    LON, LAT = np.meshgrid(np.linspace(lon0, lon1, 420), np.linspace(lat0, lat1, 320))
    r = C.local_circumstances(B, LAT.ravel(), LON.ravel())
    d = r["duration_s"].reshape(LON.shape)
    d = np.where(d > 0, d, np.nan)
    if np.isfinite(d).any():
        ax.contourf(LON, LAT, d, levels=[0, 1e5], colors=["#4a5a78"], alpha=0.16, zorder=4)
        lv = [v for v in (60, 120, 180, 240, 300, 330, 360, 375) if v < np.nanmax(d)]
        cs = ax.contour(LON, LAT, d, levels=lv, colors="#1f1f1d", linewidths=0.6, zorder=4.2)
        MK.tag_clabels(ax.clabel(cs, fmt=lambda v: I.fmt_dur(v), fontsize=6.8))
    t = np.linspace(-1.75, 2.0, 1500)
    la, lo, ln, on, ls, os_ = C.path_limits(B, t)
    ax.plot(on, ln, color="#1b2a8f", lw=1.9, zorder=6)
    ax.plot(os_, ls, color="#1b2a8f", lw=1.9, zorder=6)
    ax.plot(lo, la, color=RED, lw=1.2, zorder=6)
    ax.set_xlim(lon0, lon1)
    ax.set_ylim(lat0, lat1)
    ax.set_aspect(1 / np.cos(np.radians(0.5 * (lat0 + lat1))))
    ax.apply_aspect()

    def along(xs, ys, txt, frac, color, size, dy=0.0):
        """Label written along a line, rotated to follow it on the page."""
        m = (xs > lon0) & (xs < lon1) & (ys > lat0) & (ys < lat1)
        idx = np.where(m)[0]
        if len(idx) < 10:
            return None
        j = idx[int(frac * (len(idx) - 1))]
        j2 = min(j + 5, len(xs) - 1)
        p1 = ax.transData.transform((xs[j], ys[j]))
        p2 = ax.transData.transform((xs[j2], ys[j2]))
        ang = np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]))
        if ang > 90:
            ang -= 180
        elif ang < -90:
            ang += 180
        return ax.text(xs[j], ys[j] + dy, txt, rotation=ang, rotation_mode="anchor", ha="center", va="bottom",
                       fontsize=size, color=color, fontweight="bold", zorder=8, clip_on=True,
                       path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])
    lines = [along(on, ln, "الحد الشمالي للكلية", 0.30, "#1b2a8f", 9.5),
             along(os_, ls, "الحد الجنوبي للكلية", 0.70, "#1b2a8f", 9.5),
             along(lo, la, "خط المركز", 0.86, RED, 8.5)]
    # white time lines across the path every 4 minutes, labelled on the central line
    T0 = besselian.T0_UT_HOURS
    tt = np.arange(np.ceil(-1.75 * 15) / 15, 2.0, 1 / 15)
    tt = tt[np.isfinite(C.central_line(B, tt)[0])]      # path_limits drops times with no central line
    lac, loc, lnt, ont, lst, ost = C.path_limits(B, tt)
    cr = C.local_circumstances(B, lac, loc)
    labels = []
    for j in range(len(tt)):
        if lon0 + 0.03 * (lon1 - lon0) < loc[j] < lon1 - 0.03 * (lon1 - lon0) and lat0 < lac[j] < lat1:
            ax.plot([ont[j], ost[j]], [lnt[j], lst[j]], color="white", lw=1.4, zorder=5.5, solid_capstyle="butt")
            ax.plot(loc[j], lac[j], "o", ms=3.2, color="#1f1f1d", zorder=6.5)
            txt = (f"{I.fmt_time(tt[j] + T0, seconds=False)} ت.ع\n{I.fmt_dur(float(cr['duration_s'][j]))}\n"
                   f"{A(f'{float(cr['sun_alt_deg'][j]):.0f}')}°")
            labels.append(ax.annotate(txt, (loc[j], lac[j]), xytext=(4, 4), textcoords="offset points", fontsize=7.4,
                                      fontweight="bold", color="#1f1f1d", ha="left", va="bottom", zorder=9,
                                      linespacing=1.0, path_effects=[pe.withStroke(linewidth=2.2, foreground="white")]))
    # country and sea names
    names = []
    for _, row in ctr.iterrows():
        pt = row.geometry.intersection(__import__("shapely").geometry.box(lon0, lat0, lon1, lat1))
        if pt.is_empty or pt.area < 0.06 * (lon1 - lon0) * (lat1 - lat0):
            continue
        c = pt.representative_point()
        names.append(ax.text(c.x, c.y, row["NAME_AR"], fontsize=15, color="#5b5650", style="italic", fontweight="bold",
                             ha="center", va="center", zorder=3.5, alpha=0.75, gid="admin",
                             path_effects=[pe.withStroke(linewidth=2.5, foreground="white")]))
    for n, x, y in SEAS:
        if lon0 + 0.5 < x < lon1 - 0.5 and lat0 + 0.3 < y < lat1 - 0.3:
            names.append(ax.text(x, y, n, fontsize=13, color="#2b5f9e", style="italic", fontweight="bold",
                                 ha="center", va="center", zorder=3.5, gid="admin"))
    first = [t_ for t_ in lines + labels if t_ is not None]
    MK.declutter(ax, first=first)
    # computed cities (red dot inside totality) with duration or obscuration
    shown = [rr for rr in rows if lon0 < rr["lon"] < lon1 and lat0 < rr["lat"] < lat1 and rr["magnitude"] > 0]
    for rr in sorted(shown, key=lambda q: -q["duration_s"]):
        inside = rr["duration_s"] > 0
        ax.plot(rr["lon"], rr["lat"], "o", ms=5, mfc=RED if inside else INK, mec="white", mew=0.9, zorder=9)
        val = I.fmt_dur(rr["duration_s"]) if inside else I.pct(rr["obscuration"] * 100, 0)
        MK.place_label(ax, f"{rr['name']}\n{val}", (rr["lon"], rr["lat"]), size=8.2, prefer=1, zorder=10,
                       fontweight="bold")
    # other towns from Natural Earth, Arabic over Latin name, largest first
    known = [(rr["lat"], rr["lon"]) for rr in shown]
    pl = MK.geo("places_region").cx[lon0:lon1, lat0:lat1]
    pl = pl.sort_values("POP_MAX", ascending=False)
    n_extra = 0
    for _, q in pl.iterrows():
        if n_extra >= 28:
            break
        x, y = q.geometry.x, q.geometry.y
        if any(abs(y - a) < 0.12 and abs(x - b) < 0.12 for a, b in known) or not isinstance(q["NAME_AR"], str):
            continue
        ax.plot(x, y, "o", ms=2.6, color="#6b6a65", zorder=8)
        if MK.place_label(ax, f"{q['NAME_AR']}\n{q['NAME']}", (x, y), size=6.6, color="#4a4a46", zorder=8) is not None:
            n_extra += 1
            known.append((y, x))
    MK.declutter(ax, first=first + shields)
    # scale bar (km) in the lower left
    km = 100 if (lon1 - lon0) < 9 else 200
    deg = km / (111.32 * np.cos(np.radians(lat0 + 0.08 * (lat1 - lat0))))
    x0, y0 = lon0 + 0.04 * (lon1 - lon0), lat0 + 0.05 * (lat1 - lat0)
    ax.plot([x0, x0 + deg], [y0, y0], color="#1f1f1d", lw=1.6, zorder=9, solid_capstyle="butt")
    for xx in (x0, x0 + deg / 2, x0 + deg):
        ax.plot([xx, xx], [y0, y0 + 0.012 * (lat1 - lat0)], color="#1f1f1d", lw=1.2, zorder=9)
    ax.text(x0 + deg / 2, y0 + 0.018 * (lat1 - lat0), f"{A(km)} كم", ha="center", va="bottom", fontsize=8, zorder=9,
            path_effects=[pe.withStroke(linewidth=2.2, foreground="white")])
    ax.text(lon1 - 0.01 * (lon1 - lon0), lat0 + 0.012 * (lat1 - lat0), f"خريطة {A(k)}", ha="right", va="bottom",
            fontsize=10, fontweight="bold", zorder=9, bbox=dict(boxstyle="square,pad=0.3", fc="white", ec="#1f1f1d", lw=0.6))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("")
    ax.set_ylabel("")
    for s_ in ax.spines.values():
        s_.set_color("#8a8984")
    header(fig, f"خريطة المسار {A(k)}: {title}",
           "حدّا الكلية بالأزرق وخط المركز بالأحمر؛ الخطوط السوداء الرفيعة تساوي مدة الكلية كل دقيقة، والخطوط البيضاء موضع الظل كل ٤ دقائق")
    footer(fig, "المسار: حسابات المؤلف (عناصر بِسِل لناسا). الطرق والمدن: Natural Earth. عند كل خط أبيض: الوقت (ت.ع)، "
           "ومدة الكلية وارتفاع الشمس على خط المركز.")
    save(fig, CH, f"strip_map_{k:02d}", f"خريطة مسار الكلية {A(k)}: {title} (محسوبة).", "map")


# ------------------------------------------------------------------ overview of the Arab world
def fig_overview(rows):
    lon0, lon1, lat0, lat1 = -18.0, 60.0, 0.0, 39.5
    fig = plt.figure(figsize=(9.6, 6.4), facecolor=PAPER)
    ax = fig.add_axes([0.03, 0.08, 0.90, 0.74])
    MK.base(ax, lon0, lon1, lat0, lat1, highlight=("EGY",), admin1=None)
    MK.field(ax, B, lon0, lon1, lat0, lat1, n=360, dur=False)
    MK.path(ax, B)
    for rr in rows:
        if rr["name"] in ("الرباط", "الجزائر العاصمة", "تونس العاصمة", "طرابلس", "بنغازي", "القاهرة", "الأقصر", "الخرطوم",
                          "جدة", "مكة المكرمة", "الرياض", "صنعاء", "عدن", "جيبوتي", "مقديشو", "عمّان", "دمشق",
                          "بغداد", "الكويت", "الدوحة", "أبوظبي", "مسقط", "نواكشوط", "طنجة", "أبها", "بوصاصو"):
            inside = rr["duration_s"] > 0
            ax.plot(rr["lon"], rr["lat"], "o", ms=4.5, mfc=RED if inside else INK, mec="white", zorder=8)
            val = ("كلي " + I.fmt_dur(rr["duration_s"])) if inside else I.pct(rr["obscuration"] * 100, 0)
            MK.place_label(ax, f"{rr['name']}\n{val}", (rr["lon"], rr["lat"]), size=7.6, prefer=1)
    MK.declutter(ax)
    header(fig, "الكسوف في العالم العربي", "مسار الكلية من المغرب إلى الصومال، ونسبة احتجاب الشمس في العواصم والمدن الكبرى")
    footer(fig, SRC + "؛ الحدود: Natural Earth.")
    save(fig, CH, "arab_world_overview", "الكسوف في العالم العربي: مسار الكلية ونسب الاحتجاب في العواصم (محسوب).", "map")


# ------------------------------------------------------------------ where to watch in Egypt (after Carter & Carter 2026)
SITES = [
    ("واحة سيوة وبحر الرمال الأعظم", 29.2032, 25.5195, "واحة نائية قرب الحدود الليبية؛ من أقل مواقع المسار احتمالًا للسحب، وأفقها الرملي مفتوح."),
    ("الواحات البحرية (الباويطي)", 28.3490, 28.8650, "منخفض غني بالآثار والعيون؛ قريب من خط المركز ويمكن بلوغه برًا من القاهرة."),
    ("المنيا وضفاف النيل", 28.1099, 30.7503, "قرب الحد الشمالي للمسار؛ أقرب وجهة لسكان القاهرة، فتوقّع الزحام."),
    ("بني حسن", 27.9333, 30.8833, "مقابر منحوتة في جروف الحجر الجيري شرق النيل، نادرًا ما تدخل في برامج السياحة."),
    ("تل العمارنة (أخت-آتون)", 27.6450, 30.8960, "عاصمة إخناتون وموطن عبادة قرص الشمس، في سهل صحراوي مفتوح."),
    ("أبيدوس (البلينا)", 26.1847, 31.9190, "من أقدس مواقع مصر القديمة؛ صحراء مفتوحة ومدة كلية من الأطول."),
    ("معبد دندرة (قنا)", 26.1418, 32.6702, "من أجمل المعابد حفظًا وفي سقفه دائرة البروج؛ أهدأ من الأقصر بمدة قريبة منها."),
    ("معابد الكرنك", 25.7188, 32.6573, "أكبر مجمع ديني بُني على الإطلاق؛ تُنتظر فعاليات منظمة وزحام كبير."),
    ("معبد الأقصر", 25.6996, 32.6390, "في قلب المدينة على محور الكباش؛ سهل الوصول وإطار معماري مهيب."),
    ("تمثالا ممنون (البر الغربي)", 25.7206, 32.6104, "مكان مفتوح عند حافة الأرض الزراعية؛ مقدمة رائعة للصور وأهدأ من وسط الأقصر."),
    ("معبد حتشبسوت (الدير البحري)", 25.7380, 32.6065, "مدرّجات في حضن الجبل وإطلالة واسعة؛ الظل نادر فاستعد للحرارة."),
    ("وادي الملوك", 25.7402, 32.6014, "المقابر لا تصلح للرصد، لكن الوادي الصحراوي المحيط ممتاز."),
    ("معبد إسنا", 25.2930, 32.5545, "معبد روماني في قلب المدينة على بعد ساعة جنوب الأقصر."),
    ("معبد إدفو", 24.9779, 32.8734, "من أكمل المعابد حفظًا؛ يقصده عدد أقل من الراصدين."),
    ("معبد كوم أمبو", 24.4520, 32.9285, "قرب الحد الجنوبي؛ مدة أقصر لكنه بعيد عن الزحام."),
    ("برنيس (البحر الأحمر)", 23.9466, 35.4740, "ميناء بطلمي قديم على ساحل البحر الأحمر قرب خط المركز؛ رطوبة أعلى قليلًا."),
]


def fig_sites(part):
    sel = SITES[:8] if part == 1 else SITES[8:]
    la = np.array([q[1] for q in sel])
    lo = np.array([q[2] for q in sel])
    r = C.local_circumstances(B, la, lo)
    H = 1.6 + 1.05 * len(sel)
    fig = page(8.6, H)
    ax = canvas(fig)
    header(fig, f"أين تشاهد الكسوف في مصر؟ ({A(part)} من ٢)",
           "مواقع مقترحة من الشمال الغربي إلى الجنوب الشرقي مع مواعيدها المحسوبة بتوقيت مصر الصيفي")
    y = 1 - 1.35 / H
    hh = 0.95 / H
    for k, (name, a, b, desc) in enumerate(sel):
        yc = y - hh / 2
        ax.add_patch(plt.Rectangle((0.03, yc - hh / 2 + 0.06 / H), 0.94, hh - 0.12 / H, fc="white", ec=LINE))
        ax.add_patch(plt.Rectangle((0.955, yc - hh / 2 + 0.06 / H), 0.015, hh - 0.12 / H, fc=SUN_DEEP, ec="none"))
        ax.text(0.94, yc + 0.22 / H, name, ha="right", va="center", fontsize=11, fontweight="bold", color=NAVY)
        d = float(r["duration_s"][k])
        stats = (f"الكلية {I.fmt_time(float(r['c2'][k]) + 3, seconds=False)}  |  المدة {I.fmt_dur(d)}  |  "
                 f"ارتفاع الشمس {A(f'{float(r['sun_alt_deg'][k]):.0f}')}°") if d > 0 else "خارج مسار الكلية"
        ax.text(0.40, yc + 0.22 / H, stats, ha="right", va="center", fontsize=9.2, color=RED)
        ax.text(0.94, yc - 0.16 / H, desc, ha="right", va="center", fontsize=9.4, color=INK2)
        y -= hh
    footer(fig, "اختيار المواقع ووصفها مقتبس بتصرف من دليل جيمي وجيل كارتر (٢٠٢٦)؛ المواعيد والمدد من حسابات المؤلف.")
    save(fig, CH, f"egypt_viewing_sites_{part}", f"مواقع مقترحة لرصد الكسوف في مصر مع مواعيدها ({A(part)} من ٢).")


# August climate for twenty cities in the path (Espenak 2024, Table 11: weatherspark.com and timeanddate.com)
CLIMATE = [("قادس", 36.53, -6.29, 29, 13), ("ملقة", 36.72, -4.42, 29, 10), ("جبل طارق", 36.14, -5.35, 27, 16),
           ("طنجة", 35.7595, -5.834, 30, 42), ("تطوان", 35.5785, -5.3684, 30, 25), ("وهران", 35.6969, -0.6331, 31, 35),
           ("البليدة", 36.47, 2.83, 33, 8), ("باتنة", 35.5559, 6.1741, 34, 7), ("تبسة", 35.4042, 8.1242, 33, 7),
           ("صفاقس", 34.7406, 10.7603, 33, 2), ("بنغازي", 32.1167, 20.0667, 31, 23), ("أسيوط", 27.1783, 31.1859, 36, 0),
           ("قنا", 26.1551, 32.716, 41, 0), ("الأقصر", 25.6872, 32.6396, 40, 0), ("جدة", 21.4858, 39.1925, 38, 27),
           ("مكة المكرمة", 21.3891, 39.8579, 41, 4), ("أبها", 18.2164, 42.5053, 28, 13), ("أبو عريش", 16.9689, 42.8325, 39, 33),
           ("صنعاء", 15.3694, 44.191, 28, 23), ("بوصاصو", 11.2842, 49.1816, 37, 76)]


def fig_weather():
    la = np.array([c[1] for c in CLIMATE])
    lo = np.array([c[2] for c in CLIMATE])
    dur = C.local_circumstances(B, la, lo)["duration_s"]
    n = len(CLIMATE)
    fig = page(8.8, 8.6)
    header(fig, "الطقس في أغسطس على امتداد المسار", "متوسط الغيوم ودرجة الحرارة العظمى في أغسطس، ومدة الكلية في عشرين مدينة")
    ax = fig.add_axes([0.08, 0.10, 0.40, 0.74])
    bx = fig.add_axes([0.50, 0.10, 0.18, 0.74])
    ys = np.arange(n)[::-1]
    cloud = np.array([c[4] for c in CLIMATE])
    cols = [("#1f7a4d" if v < 10 else "#e8a33a" if v < 30 else RED) for v in cloud]
    ax.barh(ys, cloud, color=cols, height=0.62)
    for y_, v in zip(ys, cloud):
        ax.text(v + 1.5, y_, A(v) + "٪", va="center", ha="left", fontsize=8.4)
    ax.set_xlim(0, 90)
    ax.set_yticks([])
    ax.invert_xaxis()
    ax.set_title("متوسط الغيوم ٪", fontsize=9.5)
    for s_ in ("top", "left", "right"):
        ax.spines[s_].set_visible(False)
    ax.set_xticks([])
    temp = np.array([c[3] for c in CLIMATE])
    bx.barh(ys, temp, color=[SUN_DEEP if t >= 38 else "#efa351" for t in temp], height=0.62)
    for y_, t in zip(ys, temp):
        bx.text(t - 1, y_, A(t) + "°", va="center", ha="right", fontsize=8.4, color="white", fontweight="bold")
    bx.set_xlim(0, 45)
    bx.set_yticks([])
    bx.set_xticks([])
    bx.set_title("الحرارة العظمى °م", fontsize=9.5)
    for s_ in ("top", "left", "right", "bottom"):
        bx.spines[s_].set_visible(False)
    for y_, (name, *_), d in zip(ys, CLIMATE, dur):
        fig.text(0.965, 0.10 + (y_ + 0.5) / n * 0.74, name, ha="right", va="center", fontsize=9.6, fontweight="bold")
        fig.text(0.79, 0.10 + (y_ + 0.5) / n * 0.74, I.fmt_dur(d) if d > 0 else "—", ha="right", va="center", fontsize=9,
                 color=NAVY)
    fig.text(0.79, 0.865, "مدة الكلية", ha="right", fontsize=9.5)
    footer(fig, "الحرارة: weatherspark.com، والغيوم: timeanddate.com (منذ ٢٠٠٠)، كما جمعها فريد إسبيناك في دليله لكسوف ٢٠٢٧ (٢٠٢٤)؛ "
           "مدة الكلية من حسابات المؤلف.")
    save(fig, CH, "august_weather_path", "متوسط الغيوم والحرارة في أغسطس ومدة الكلية في عشرين مدينة على المسار.", "chart")


def fig_pros_cons():
    fig = page(8.6, 6.4)
    ax = canvas(fig)
    header(fig, "رصد الكسوف في مصر: المزايا والتحديات", "خلاصة عملية لمن يخطط لرحلته")
    pros = ["سماء صافية شبه مضمونة على معظم المسار في أغسطس", "كلية طويلة تتجاوز ست دقائق في الصعيد والواحات",
            "الشمس شبه عمودية فتظهر الهالة في سماء مظلمة تمامًا", "معابد وآثار فريدة تؤطّر الحدث"]
    cons = ["حرارة شديدة تتجاوز ٤٠°م في الصعيد وظل نادر", "غبار الصحراء والضباب الرقيق أحيانًا قرب الأفق",
            "زحام كبير وطلب مرتفع على الفنادق في الأقصر", "الشمس فوق الرأس: إجهاد الرقبة وصعوبة توجيه المعدات",
            "المواقع الصحراوية النائية تحتاج تخطيطًا للنقل والماء"]
    for x0, ttl, items, col in [(0.50, "المزايا", pros, "#1f7a4d"), (0.02, "التحديات", cons, RED)]:
        ax.add_patch(plt.Rectangle((x0, 0.08), 0.46, 0.74, fc="white", ec=LINE))
        ax.add_patch(plt.Rectangle((x0, 0.76), 0.46, 0.06, fc=col, ec="none"))
        ax.text(x0 + 0.44, 0.79, ttl, ha="right", va="center", color="white", fontsize=13, fontweight="bold", fontfamily=TITLE)
        for i, t in enumerate(items):
            ax.text(x0 + 0.44, 0.69 - i * 0.12, "● " + t, ha="right", va="center", fontsize=9.8, color=INK, wrap=True)
    footer(fig, "مقتبس بتصرف من دليل جيمي وجيل كارتر لكسوف ٢٠٢٧ (٢٠٢٦).")
    save(fig, CH, "egypt_pros_cons", "مزايا رصد الكسوف في مصر وتحدياته.")


def fig_travel():
    tips = [("الحرارة", "اشرب الماء باستمرار، والبس قبعة عريضة وملابس فاتحة، واحمل مظلة؛ فالحرارة تتجاوز ٤٠°م ظهرًا."),
            ("المعدات", "احمِ الكاميرا والهاتف من الشمس المباشرة؛ الحرارة ترفع ضوضاء المستشعر وتُفرغ البطاريات."),
            ("الوضعية", "الشمس شبه عمودية: استلقِ على حصيرة أو كرسي مائل بدل إمالة الرقبة دقائق طويلة."),
            ("الحجز المبكر", "الأقصر محور الحدث: مطار دولي وفنادق ورحلات نيلية، لكنها تمتلئ مبكرًا جدًا."),
            ("بدائل هادئة", "المنيا والواحات الغربية أقل زحامًا وأصفى سماءً، لكنها تحتاج رحلات برية طويلة وتخطيطًا."),
            ("الطقس", "راقب نشرات الهيئة العامة للأرصاد الجوية؛ الغبار هو المتغير الأهم لا السحب."),
            ("بعد الكسوف", "رحلة نيلية بين الأقصر وأسوان، أو الصحراء البيضاء، أو شواطئ البحر الأحمر، وسماء مظلمة لرصد النجوم.")]
    H = 1.6 + 0.78 * len(tips)
    fig = page(8.6, H)
    ax = canvas(fig)
    header(fig, "نصائح السفر والإقامة يوم الكسوف", "ما تعلّمه مطاردو الكسوف عن الرصد في الصحراء والصيف المصري")
    y = 1 - 1.4 / H
    for i, (h, t) in enumerate(tips):
        ax.add_patch(plt.Circle((0.94, y), 0.022, transform=ax.transAxes, fc=NAVY))
        ax.text(0.94, y, A(i + 1), ha="center", va="center", color="white", fontsize=10, fontweight="bold")
        ax.text(0.90, y + 0.12 / H, h, ha="right", va="center", fontsize=11, fontweight="bold", color=NAVY)
        ax.text(0.90, y - 0.2 / H, t, ha="right", va="center", fontsize=9.6, color=INK)
        y -= 0.78 / H
    footer(fig, "مقتبس بتصرف من دليل جيمي وجيل كارتر (٢٠٢٦) ودليل فريد إسبيناك (٢٠٢٤).")
    save(fig, CH, "travel_tips_egypt", "نصائح عملية للسفر والرصد في مصر يوم الكسوف.")

# ------------------------------------------------------------------ famous sites inside and outside the path (computed)
LANDMARKS = [("معبد الكرنك", 25.7188, 32.6573), ("وادي الملوك", 25.7402, 32.6014), ("معبد الأقصر", 25.6995, 32.6391),
             ("معبد دندرة", 26.1418, 32.6703), ("معبد سيتي الأول بأبيدوس", 26.1850, 31.9190), ("أخميم", 26.5627, 31.7473),
             ("معبد إسنا", 25.2934, 32.5543), ("معبد إدفو", 24.9779, 32.8734), ("معبد كوم أمبو", 24.4521, 32.9284),
             ("تل العمارنة", 27.6450, 30.8970), ("الواحات البحرية", 28.3490, 28.8650), ("معبد الوحي بسيوة", 29.2006, 25.5469),
             ("مرسى علم", 25.0676, 34.8790),
             ("أهرامات الجيزة", 29.9792, 31.1342), ("سقارة", 29.8713, 31.2165), ("قلعة قايتباي بالإسكندرية", 31.2140, 29.8856),
             ("معبد فيلة بأسوان", 24.0254, 32.8844), ("أبو سمبل", 22.3372, 31.6258), ("الغردقة", 27.2579, 33.8116),
             ("شرم الشيخ", 27.9158, 34.3300), ("دير سانت كاترين", 28.5559, 33.9760)]


def fig_landmarks():
    la = np.array([q[1] for q in LANDMARKS])
    lo = np.array([q[2] for q in LANDMARKS])
    r = C.local_circumstances(B, la, lo)
    rows = [(n, float(r["duration_s"][k]), float(r["obscuration"][k]) * 100) for k, (n, _, _) in enumerate(LANDMARKS)]
    inside = sorted([q for q in rows if q[1] > 0], key=lambda q: -q[1])
    outside = sorted([q for q in rows if q[1] <= 0], key=lambda q: -q[2])
    n = len(inside) + len(outside)
    H = 2.6 + 0.30 * n
    fig = page(8.6, H)
    header(fig, "معالم مصر داخل مسار الكلية وخارجه",
           "مدة الكلية عند المعالم الواقعة في المسار، ونسبة تغطية الشمس عند المعالم خارجه (محسوبة)")
    top, bot = 1 - 1.35 / H, 0.75 / H
    gap = 0.55 / H
    h_in = (top - bot - gap) * len(inside) / n
    h_out = (top - bot - gap) * len(outside) / n
    a1 = fig.add_axes([0.06, top - h_in, 0.58, h_in])
    a2 = fig.add_axes([0.06, bot, 0.58, h_out])
    y = np.arange(len(inside))[::-1]
    a1.barh(y, [q[1] / 60 for q in inside], color=BLUE[8], height=0.62)
    for yi, q in zip(y, inside):
        a1.text(q[1] / 60 + 0.08, yi, I.fmt_dur(q[1]), va="center", ha="left", fontsize=8.6, color=NAVY)
    a1.set_yticks(y)
    a1.set_yticklabels([q[0] for q in inside], fontsize=9.2)
    a1.yaxis.tick_right()
    a1.set_xlim(0, 7.6)
    a1.set_xticks(range(0, 8))
    a1.set_xticklabels([A(v) for v in range(0, 8)], fontsize=8)
    a1.set_title("داخل المسار: مدة الكلية (دقائق)", loc="right", fontsize=10.5, fontweight="bold", color=NAVY)
    y2 = np.arange(len(outside))[::-1]
    a2.barh(y2, [q[2] for q in outside], color=SUN_DEEP, height=0.62)
    for yi, q in zip(y2, outside):
        a2.text(q[2] + 1, yi, I.pct(q[2]), va="center", ha="left", fontsize=8.6, color=INK2)
    a2.set_yticks(y2)
    a2.set_yticklabels([q[0] for q in outside], fontsize=9.2)
    a2.yaxis.tick_right()
    a2.set_xlim(0, 118)
    a2.set_xticks([0, 25, 50, 75, 100])
    a2.set_xticklabels([A(v) + "٪" for v in (0, 25, 50, 75, 100)], fontsize=8)
    a2.set_title("خارج المسار: جزئي فقط — لا هالة ولا ظلام، والنظارة طوال الوقت", loc="right", fontsize=10.5, fontweight="bold",
                 color=SUN_DEEP)
    for ax in (a1, a2):
        for s_ in ("top", "left"):
            ax.spines[s_].set_visible(False)
        ax.tick_params(axis="y", length=0)
        ax.grid(axis="x", color=LINE, lw=0.7)
        ax.set_axisbelow(True)
    footer(fig, SRC + ". إن كانت رحلتك النيلية تنتهي في أسوان فتأكد أن برنامجها يتوقف يوم الكسوف داخل المسار قرب الأقصر.")
    save(fig, CH, "egypt_landmarks_in_out", "معالم مصر الشهيرة داخل مسار الكلية وخارجه: مدة الكلية أو نسبة التغطية (محسوبة).",
         "chart")


# ------------------------------------------------------------------ heat on eclipse day
def heat_index_c(t_c, rh):
    """NOAA heat index (Rothfusz regression with the usual adjustments), °C in and out."""
    T = t_c * 9 / 5 + 32
    simple = 0.5 * (T + 61.0 + (T - 68.0) * 1.2 + rh * 0.094)
    hi = (-42.379 + 2.04901523 * T + 10.14333127 * rh - 0.22475541 * T * rh - 6.83783e-3 * T * T
          - 5.481717e-2 * rh * rh + 1.22874e-3 * T * T * rh + 8.5282e-4 * T * rh * rh - 1.99e-6 * T * T * rh * rh)
    adj_lo = np.where((rh < 13) & (T >= 80) & (T <= 112), -((13 - rh) / 4) * np.sqrt(np.clip(17 - np.abs(T - 95), 0, None) / 17), 0)
    adj_hi = np.where((rh > 85) & (T >= 80) & (T <= 87), ((rh - 85) / 10) * ((87 - T) / 5), 0)
    hi = np.where((simple + T) / 2 < 80, simple, hi + adj_lo + adj_hi)
    return (hi - 32) * 5 / 9


def fig_heat_index():
    from matplotlib.colors import BoundaryNorm, ListedColormap
    t = np.arange(30, 47.01, 0.25)
    rh = np.arange(5, 80.01, 0.5)
    TT, RR = np.meshgrid(t, rh)
    HI = heat_index_c(TT, RR)
    fig = page(8.6, 6.6)
    header(fig, "الحرارة المحسوسة: الرطوبة تصنع الفرق",
           "ما يشعر به الجسم عند كل درجة حرارة ورطوبة نسبية (مؤشر الحرارة، Heat index) — محسوب بمعادلة الهيئة الأمريكية للمحيطات والغلاف الجوي")
    ax = fig.add_axes([0.11, 0.17, 0.68, 0.62])
    lv = [20, 27, 32, 41, 54, 80]
    cols = ["#fdf1c7", "#f8d27a", "#f0a041", "#d9622b", "#9e1f1f"]
    ax.contourf(TT, RR, HI, levels=lv, colors=cols)
    cs = ax.contour(TT, RR, HI, levels=[35, 40, 45, 50], colors="white", linewidths=0.7)
    ax.clabel(cs, fmt=lambda v: A(f"{v:.0f}") + "°", fontsize=8)
    # Luxor in August: dry desert heat (about 40-42 °C, relative humidity 10-20 %)
    ax.add_patch(plt.Rectangle((40, 10), 2, 10, fc="none", ec=NAVY, lw=1.8, zorder=5))
    ax.annotate("ظهيرة الأقصر في أغسطس\n(جاف: رطوبة ١٠–٢٠٪)", (41, 20), xytext=(36.2, 33), fontsize=9, color=NAVY,
                fontweight="bold", ha="center", path_effects=halo(),
                arrowprops=dict(arrowstyle="-", color=NAVY, lw=0.9), zorder=6)
    ax.annotate("الساحل الرطب (مثل جدة):\nحرارة أقل ورطوبة أعلى،\nوإحساس أشد", (37.5, 62), xytext=(33.0, 70), fontsize=9,
                color=NAVY, fontweight="bold", ha="center", path_effects=halo(), zorder=6)
    ax.set_xlabel("درجة حرارة الهواء (°م)")
    ax.set_ylabel("الرطوبة النسبية (٪)")
    ax.set_xticks(range(30, 48, 2))
    ax.set_xticklabels([A(v) for v in range(30, 48, 2)])
    ax.set_yticks(range(10, 81, 10))
    ax.set_yticklabels([A(v) for v in range(10, 81, 10)])
    # legend of danger bands
    lx = fig.add_axes([0.83, 0.25, 0.14, 0.46])
    lx.axis("off")
    bands = [("حذر", "٢٧–٣٢°"), ("حذر شديد", "٣٢–٤١°"), ("خطر", "٤١–٥٤°"), ("خطر بالغ", "فوق ٥٤°")]
    for k, ((nm, rg), c) in enumerate(zip(bands, cols[1:])):
        yy = 0.9 - k * 0.24
        lx.add_patch(plt.Rectangle((0.62, yy - 0.07), 0.3, 0.14, fc=c, ec="none", transform=lx.transAxes))
        lx.text(0.56, yy + 0.03, nm, ha="right", va="center", fontsize=9.2, fontweight="bold", color=INK)
        lx.text(0.56, yy - 0.05, rg, ha="right", va="center", fontsize=8.2, color=INK2)
    footer(fig, "مؤشر الحرارة: معادلة روثفوز (NOAA) محسوبة بالمؤلف؛ نطاق الأقصر من دليل أودن كسترل (٢٠٢٦) وبيانات المناخ. "
                "في الشمس المباشرة يزيد الإحساس بالحرارة عدة درجات أخرى.")
    save(fig, CH, "heat_index_chart", "مؤشر الحرارة المحسوسة بحسب درجة الحرارة والرطوبة، وموقع ظهيرة الأقصر في أغسطس (محسوب).",
         "chart")


def fig_heat_illness():
    fig = page(8.6, 6.4)
    ax = canvas(fig)
    header(fig, "الإجهاد الحراري وضربة الشمس: اعرف الفرق",
           "ساعات الانتظار في شمس أغسطس أخطر على الجسم من الكسوف نفسه — والوقاية أسهل من العلاج")
    cols = [(0.52, "الإجهاد الحراري", "Heat exhaustion", SUN_DEEP,
             ["تعرّق غزير وجلد بارد رطب", "ضعف ودوار وصداع", "غثيان وتشنّج العضلات", "نبض سريع ضعيف"],
             ["انقله إلى الظل أو مكان مكيّف", "فكّ الملابس الضيقة", "رشفات ماء أو محلول أملاح", "بلّل الجلد بالماء"]),
            (0.04, "ضربة الشمس", "Heat stroke — حالة طارئة", RED,
             ["حرارة الجسم مرتفعة جدًا", "جلد ساخن جاف وقد يتوقف التعرق", "ارتباك أو هذيان", "نبض سريع قوي، وقد يفقد الوعي"],
             ["اطلب الإسعاف فورًا", "برّده بكل وسيلة: ماء وظل وتهوية", "لا تعطه ماءً إن كان فاقد الوعي",
              "ابقَ معه حتى يصل الإسعاف"])]
    for x, t1, t2, c, signs, acts in cols:
        card(ax, x, 0.275, 0.44, 0.545, fc="white", ec=c, lw=1.6)
        ax.add_patch(plt.Rectangle((x, 0.74), 0.44, 0.08, fc=c, ec="none", transform=ax.transAxes))
        ax.text(x + 0.42, 0.78, t1, ha="right", va="center", fontsize=13, fontweight="bold", color="white")
        ax.text(x + 0.02, 0.78, t2, ha="left", va="center", fontsize=8.6, color="white")
        ax.text(x + 0.42, 0.70, "العلامات", ha="right", fontsize=10, fontweight="bold", color=c)
        for k, sg in enumerate(signs):
            ax.text(x + 0.42, 0.655 - k * 0.042, "• " + sg, ha="right", va="center", fontsize=9.4, color=INK)
        ax.text(x + 0.42, 0.475, "ماذا تفعل؟", ha="right", fontsize=10, fontweight="bold", color=c)
        for k, sg in enumerate(acts):
            ax.text(x + 0.42, 0.432 - k * 0.039, "• " + sg, ha="right", va="center", fontsize=9.4, color=INK)
    tips = ("الوقاية: اشرب قبل أن تعطش وعلى فترات منتظمة • أضف أملاحًا (مشروب أملاح أو وجبة مالحة) • "
            "قلّل الكافيين • البس ملابس فاتحة واسعة وقبعة عريضة • احمل ظلك معك (مظلة أو خيمة شمسية) • "
            "انتبه أكثر للأطفال وكبار السن ومرضى القلب ومن يتناول مدرّات البول")
    para(ax, 0.96, 0.225, tips, width=95, size=9.6, color=NAVY)
    footer(fig, "مبني على إرشادات المراكز الأمريكية لمكافحة الأمراض (CDC) كما يلخصها دليل أودن كسترل (٢٠٢٦)، بتصرف. ليس بديلًا عن المشورة الطبية.")
    save(fig, CH, "heat_illness_card", "علامات الإجهاد الحراري وضربة الشمس وما يجب فعله في كل منهما.")


# ------------------------------------------------------------------ the morning decision: move or stay?
def fig_backup_plan():
    r = C.local_circumstances(B, np.array([25.6872]), np.array([32.6396]))
    c1 = float(r["c1"][0]) + 3
    fig = page(8.6, 8.0)
    ax = canvas(fig)
    header(fig, "الخطة البديلة: هل تنتقل صباح الكسوف أم تبقى؟",
           "قرار يُتخذ بهدوء قبل الرحلة لا تحت ضغط الصباح — مثال من الأقصر حيث تبدأ المرحلة الجزئية "
           + I.fmt_time(c1, seconds=False))
    steps = [("قبل الرحلة", "اختر موقعًا رئيسيًا وموقعين بديلين داخل البلد نفسه، تصلها طرق مختلفة، وحدّد مسبقًا ساعة القرار."),
             ("مساء ١ أغسطس", "اطّلع على التوقعات قصيرة المدى: قراءة أولية فقط، لا قرار نهائي."),
             ("صباح ٢ أغسطس", "صور الأقمار الصناعية المرئية تتاح بعد الشروق؛ والكسوف في مصر بعد الظهر فلديك وقت أطول للتقييم."),
             ("ساعة القرار", "التزم بها: الانتظار «لتحديث أخير» قد يُضيّع فرصة الانتقال كلها.")]
    y = 0.80
    for k, (h, t) in enumerate(steps):
        number_badge(ax, 0.94, y, k + 1, color=NAVY)
        ax.text(0.90, y + 0.012, h, ha="right", va="center", fontsize=11, fontweight="bold", color=NAVY)
        ax.text(0.90, y - 0.026, t, ha="right", va="center", fontsize=9.4, color=INK)
        if k < len(steps) - 1:
            ax.plot([0.94, 0.94], [y - 0.03, y - 0.075], color=LINE, lw=2, transform=ax.transAxes)
        y -= 0.10
    # the four questions
    card(ax, 0.05, 0.14, 0.90, 0.30, fc="white", ec=LINE)
    ax.text(0.93, 0.405, "قبل أن تتحرك اسأل نفسك أربعة أسئلة:", ha="right", fontsize=11, fontweight="bold", color=RED)
    qs = ["هل الموقع البديل أصفى فعلًا بحسب صور الأقمار الصناعية، لا بحسب الأمل؟",
          "هل الطريق إليه سالك، مع أن آلافًا غيرك قد يفكرون في الشيء نفسه؟",
          "هل ستصل قبل التماس الأول بهامش مريح؟",
          "ما خطتك إن تعطلت في الطريق؟"]
    for k, q in enumerate(qs):
        ax.text(0.91, 0.355 - k * 0.045, f"{A(k + 1)}. {q}", ha="right", va="center", fontsize=9.6, color=INK)
    ax.text(0.93, 0.17, "إن كانت إجابة أي سؤال غامضة أو سلبية فابقَ في مكانك: كسوف خلف سحب خفيفة أفضل من كلية تفوتك في زحام الطريق.",
            ha="right", va="center", fontsize=9.6, fontweight="bold", color=NAVY)
    ax.text(0.5, 0.085, "لا تخطط لعبور حدود دولية صباح الكسوف بحثًا عن طقس أفضل.", ha="center", fontsize=10,
            fontweight="bold", color=RED)
    footer(fig, "مبادئ مقتبسة بتصرف من دليل أودن كسترل (٢٠٢٦)؛ موعد التماس الأول في الأقصر من حسابات المؤلف.")
    save(fig, CH, "backup_plan_decision", "الخطة البديلة صباح الكسوف: خطوات القرار والأسئلة الأربعة قبل الانتقال.")


# ------------------------------------------------------------------ eclipse day hour by hour in Luxor (computed)
def fig_day_plan():
    from skyfield.api import wgs84
    la, lo = 25.6872, 32.6396
    r = C.local_circumstances(B, np.array([la]), np.array([lo]))
    c1, c2, mx, c3, c4 = (float(r[k][0]) + 3 for k in ("c1", "c2", "tmax", "c3", "c4"))
    ts, eph = besselian.ephemeris()
    hrs = np.arange(4.0, 8.0, 1 / 120)
    t = ts.ut1(2027, 8, 2, 0, 0, (hrs - 3) * 3600)
    alt = (eph["earth"] + wgs84.latlon(la, lo)).at(t).observe(eph["sun"]).apparent().altaz()[0].degrees
    sunrise = float(hrs[np.argmax(alt > -0.833)])
    ev = [(c1 - 2.5, "قبل التماس الأول بساعتين على الأقل", "الوصول إلى موقع الرصد: ثبّت الحامل، وزّع النظارات، واتفق مع مجموعتك على نقطة لقاء.", INK2),
          (sunrise, "الشروق", "أول صور الأقمار الصناعية المرئية: راجع السماء والتوقعات وطبّق خطة القرار.", INK2),
          (c1, "التماس الأول", "انبعاج صغير في حافة الشمس — بالنظارة فقط. اشرب الماء وجدّد واقي الشمس.", SUN_DEEP),
          (c2 - 0.5, "قبل الكلية بنحو ٣٠ دقيقة", "الضوء يبهت والظلال تحدّ والحرارة تبدأ في الانخفاض: انتقل من المتابعة إلى الاستعداد.", SUN_DEEP),
          (c2 - 5 / 60, "قبل الكلية بخمس دقائق", "أوقف اللقطات الروتينية، واضبط إعدادات الكلية، وذكّر الجميع: النظارة تبقى حتى يختفي الضوء.", SUN_DEEP),
          (c2, "بداية الكلية", "اختفاء آخر نقطة في الخاتم الماسي: انزع النظارة ومرشّح الكاميرا. انظر إلى الهالة والأفق.", NAVY),
          (c3 - 0.5 / 60, "قبل نهاية الكلية بـ٣٠ ثانية", "تنبيه اهتزاز هادئ في الهاتف بدل التحديق في الساعة.", NAVY),
          (c3, "نهاية الكلية", "أول وميض للضوء: النظارة والمرشّح فورًا، بلا تأخير ولو ثانية.", RED),
          (c4, "التماس الأخير", "تفقّد المكان لئلا تنسى مرشّحًا أو غطاء عدسة، وانتظر قليلًا حتى يخف زحام الطرق.", INK2)]
    ev.sort(key=lambda e: e[0])
    H = 1.9 + 0.72 * len(ev)
    fig = page(8.6, H)
    ax = canvas(fig)
    header(fig, "يوم الكسوف في الأقصر ساعةً بساعة",
           f"مواعيد محسوبة بتوقيت مصر الصيفي — الكلية {I.fmt_time(c2)} إلى {I.fmt_time(c3)} ({I.fmt_dur(float(r['duration_s'][0]))})")
    y0, step = 1 - 1.45 / H, 0.72 / H
    ax.plot([0.80, 0.80], [y0 + 0.2 / H, y0 - step * (len(ev) - 1) - 0.1 / H], color=LINE, lw=3, transform=ax.transAxes)
    for k, (tt, h, d, c) in enumerate(ev):
        y = y0 - k * step
        ax.add_patch(plt.Circle((0.80, y), 0.014, transform=ax.transAxes, fc=c, ec="white", lw=1.5, zorder=4))
        ax.text(0.83, y, I.fmt_time(tt, seconds=c in (NAVY, RED)) if "بساعتين" not in h else "≈ " + I.fmt_time(tt, seconds=False),
                ha="left", va="center", fontsize=11, fontweight="bold", color=c)
        ax.text(0.77, y + 0.13 / H, h, ha="right", va="center", fontsize=10.5, fontweight="bold", color=c)
        ax.text(0.77, y - 0.17 / H, d, ha="right", va="center", fontsize=9.1, color=INK)
    footer(fig, SRC + "؛ الشروق من تقويم JPL DE421. ترتيب الخطوات مستوحى بتصرف من «خطة الحقل» في دليل أودن كسترل (٢٠٢٦).")
    save(fig, CH, "eclipse_day_luxor", "يوم الكسوف في الأقصر ساعةً بساعة: المواعيد المحسوبة وما تفعله عند كل مرحلة.")



def main():
    rows = compute()
    fig_overview(rows)
    table_pages(rows, True, "مواعيد الكسوف الكلي في المدن العربية",
                "المدن الواقعة داخل مسار الكلية مرتبةً حسب الدولة ثم مدة الكلية", "arab_total_table", per=34)
    table_pages(rows, False, "مواعيد الكسوف الجزئي في المدن العربية",
                "المدن خارج مسار الكلية: نسبة تغطية الشمس عند الذروة", "arab_partial_table", per=34)
    for k, (title, lon0, lon1, lat0, lat1) in enumerate(STRIPS, 1):
        strip_map(k, title, lon0, lon1, lat0, lat1, rows)
    fig_weather()
    fig_sites(1)
    fig_sites(2)
    fig_pros_cons()
    fig_travel()
    fig_landmarks()
    fig_heat_index()
    fig_heat_illness()
    fig_backup_plan()
    fig_day_plan()
    write_catalogue("ch12")


if __name__ == "__main__":
    main()
