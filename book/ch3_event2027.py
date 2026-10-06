"""Chapter 3 — the total solar eclipse of 2 August 2027 (computed infographics)."""
import numpy as np

import mapkit as MK
from common import (A, BLUE, BODY, CAT, Circ, GREEN, INK, INK2, LINE, MUTED, NAVY, ORANGE, PAPER, RED, SUN, SUN_DEEP,
                    TITLE, arabic_ticks, canvas, card, corona, footer, halo, header, mirror_y, moon_disk, page, para,
                    plt, save, style_axes, sun_disk, wrap, write_catalogue)
from eclipse2027 import besselian, circumstances as C, engine as E, i18n as I
from eclipse2027.places import CITIES, COUNTRIES, EGYPT_CITIES

CH = 3
SRC = "المصدر: حسابات المؤلف من تقويم JPL DE421"
B = besselian.compute()
T0 = besselian.T0_UT_HOURS
UTC = 3


def circ_city(la, lo):
    r = C.local_circumstances(B, np.array([la]), np.array([lo]))
    return {k: float(np.ravel(v)[0]) for k, v in r.items()}


def greatest():
    t = np.linspace(-1.0, 1.0, 4001)
    la, lo = C.central_line(B, t)
    r = C.local_circumstances(B, la, lo)
    i = int(np.nanargmax(r["duration_s"]))
    e = E.eclipse_near(E.jd_from_date(2027, 8, 2, 10), "de421")
    return dict(lat=la[i], lon=lo[i], dur=r["duration_s"][i], t=r["tmax"][i], alt=r["sun_alt_deg"][i], gamma=e.gamma,
                mag=float(r["magnitude"][i]))


# ------------------------------------------------------------------ 1 key numbers
def fig_key_numbers(G):
    t = np.linspace(-1.75, 2.0, 2000)
    la, lo = C.central_line(B, t)
    ok = np.isfinite(la)
    t_on, t_off = t[ok][0] + T0, t[ok][-1] + T0
    t2 = np.linspace(-1.5, 1.8, 300)
    _, _, ln, on, ls, os_ = C.path_limits(B, t2)
    w = 6371 * np.radians(1) * np.hypot(ln - ls, (on - os_) * np.cos(np.radians(0.5 * (ln + ls))))
    fig = page(8.6, 6.4, NAVY)
    ax = canvas(fig)
    header(fig, "كسوف ٢ أغسطس ٢٠٢٧ في أرقام", "قيم محسوبة لهذا الكتاب من تقويم JPL DE421", color="white",
           sub_color="#c9d3e3")
    tiles = [(I.fmt_dur(G["dur"], long=True), "أطول مدة للكلية", "في صعيد مصر"),
             (A(f"{np.nanmax(w):.0f}") + " كم", "أقصى عرض لمسار الكلية", "قرب خط عرض ٢٢° شمالًا"),
             (A(f"{G['alt']:.0f}") + "°", "ارتفاع الشمس عند أطول كلية", "الشمس شبه عمودية"),
             (A("11") + " دولة", "يمر بها مسار الكلية", "من إسبانيا إلى الصومال"),
             (I.fmt_time(t_on, seconds=False) + " – " + I.fmt_time(t_off, seconds=False), "عمر الظل على الأرض (ت.ع)",
              "≈ " + A(f"{(t_off - t_on):.1f}") + " ساعة"),
             (A(f"{G['mag']:.3f}"), "قدر الكسوف عند الذروة", "القمر أكبر ظاهريًا من الشمس بنحو " + A(f"{(G['mag'] - 1) * 100:.0f}") + "٪")]
    for k, (big, lab, sub) in enumerate(tiles):
        col, row = k % 3, k // 3
        x = 0.68 - col * 0.32
        y = 0.50 - row * 0.32
        card(ax, x - 0.0, y - 0.0, 0.29, 0.27, fc="#18294a", ec="#2a3d5c", r=0.015)
        ax.text(x + 0.27, y + 0.18, big, ha="right", va="center", color=SUN, fontsize=17 if len(big) < 14 else 12.5,
                fontweight="bold", fontfamily=TITLE)
        ax.text(x + 0.27, y + 0.09, lab, ha="right", va="center", color="white", fontsize=10.5)
        ax.text(x + 0.27, y + 0.04, sub, ha="right", va="center", color="#9aa6b8", fontsize=8.8)
    save(fig, CH, "key_numbers", "أبرز أرقام كسوف ٢ أغسطس ٢٠٢٧ (محسوبة).")


# ------------------------------------------------------------------ 2 countries timeline
def fig_country_crossings():
    import geopandas as gpd
    from shapely.geometry import Point
    countries = MK.geo("countries_region")
    t = np.linspace(-1.75, 2.0, 4000)
    la, lo = C.central_line(B, t)
    ok = np.isfinite(la)
    t, la, lo = t[ok], la[ok], lo[ok]
    r = C.local_circumstances(B, la, lo)
    seq = []
    names_ar = {"ESP": "إسبانيا", "GIB": "جبل طارق", "MAR": "المغرب", "DZA": "الجزائر", "TUN": "تونس", "LBY": "ليبيا",
                "EGY": "مصر", "SAU": "السعودية", "YEM": "اليمن", "SOM": "الصومال", "SOL": "أرض الصومال", "SDN": "السودان"}
    cur = None
    sub = countries[countries.ADM0_A3.isin(names_ar)]
    for i in range(0, len(t), 4):
        p = Point(lo[i], la[i])
        hit = sub[sub.contains(p)]
        code = hit.ADM0_A3.iloc[0] if len(hit) else None
        if code != cur:
            if cur is not None:
                seq[-1]["t1"] = t[i] + T0
            if code is not None:
                seq.append(dict(code=code, t0=t[i] + T0, t1=None, dur=r["duration_s"][i], alt=r["sun_alt_deg"][i]))
            cur = code
    fig = page(8.6, 5.6)
    header(fig, "رحلة الظل عبر اليابسة", "متى يعبر خط المركز كل دولة (بالتوقيت العالمي) ومدة الكلية عنده")
    ax = fig.add_axes([0.07, 0.12, 0.70, 0.66])
    for k, s in enumerate(seq):
        t1 = s["t1"] or s["t0"] + 0.01
        ax.barh(k, (t1 - s["t0"]) * 60, left=(s["t0"] - 8) * 60, color=RED if s["code"] == "EGY" else BLUE[7], height=0.6)
        ax.text((t1 - 8) * 60 + 2, k, I.fmt_time(s["t0"], seconds=False) + " | " + I.fmt_dur(s["dur"]), va="center",
                fontsize=8.6, ha="left")
    ax.set_yticks(range(len(seq)))
    ax.set_yticklabels([names_ar[s["code"]] for s in seq], fontsize=10.5)
    ax.yaxis.tick_right()
    ax.invert_yaxis()
    ax.set_xticks(np.arange(30, 240, 30))
    ax.set_xticklabels([I.fmt_time(8 + m / 60, seconds=False) for m in np.arange(30, 240, 30)])
    ax.set_xlabel("التوقيت العالمي")
    style_axes(ax)
    footer(fig, SRC + "؛ المدة عند نقطة دخول خط المركز إلى الدولة.")
    save(fig, CH, "shadow_country_crossings", "توقيت عبور خط المركز لكل دولة ومدة الكلية عنده (محسوب).", "chart")


# ------------------------------------------------------------------ 3 snapshots of the shadow
def snapshot(ax, tt, lon0=-30, lon1=70, lat0=-12, lat1=52, n=200):
    MK.base(ax, lon0, lon1, lat0, lat1, highlight=("EGY",), admin1=None)
    LON, LAT = np.meshgrid(np.linspace(lon0, lon1, n), np.linspace(lat0, lat1, int(n * 0.66)))
    r = C.instant(B, tt - T0, LAT.ravel(), LON.ravel())
    ob = r["obscuration"].reshape(LON.shape)
    ax.contourf(LON, LAT, ob, levels=MK.OBS_LEVELS, cmap=MK.OBS_CMAP, norm=MK.OBS_NORM, alpha=0.6, zorder=2)
    ax.contour(LON, LAT, ob, levels=[0.5, 0.9], colors=ORANGE[-1], linewidths=0.5, zorder=3)
    um = r["umbra"].reshape(LON.shape).astype(float)
    if um.any():
        ax.contourf(LON, LAT, um, levels=[0.5, 1.5], colors=[NAVY], zorder=4)
    la, lo = C.central_line(B, np.linspace(-1.75, 2.0, 600))
    ax.plot(lo, la, color=RED, lw=0.8, ls=(0, (4, 3)), zorder=5)
    ax.set_xticks([])
    ax.set_yticks([])


def fig_snapshots_grid():
    times = np.arange(8.5, 11.76, 0.25)[:12]
    fig = plt.figure(figsize=(9.0, 8.2), facecolor=PAPER)
    header(fig, "ظل القمر يعبر العالم القديم", "مواقع الظل الكامل (أسود) وشبه الظل (برتقالي) كل ربع ساعة (التوقيت العالمي)")
    for k, tt in enumerate(times):
        col, row = 2 - k % 3, k // 3
        ax = fig.add_axes([0.02 + col * 0.325, 0.66 - row * 0.205, 0.31, 0.19])
        snapshot(ax, tt, n=140)
        ax.set_title(I.fmt_time(tt, seconds=False) + " ت.ع  (" + I.fmt_time(tt + UTC, seconds=False) + " بتوقيت مصر)",
                     fontsize=8.5, loc="right")
    footer(fig, SRC)
    save(fig, CH, "shadow_snapshots_grid", "مواقع ظل القمر كل ربع ساعة يوم ٢ أغسطس ٢٠٢٧ (محسوبة).", "map")


def fig_snapshot_frames():
    for tt in [8.5, 9.0, 9.5, 9.75, 10.0, 10.0833, 10.25, 10.5, 11.0, 11.5]:
        fig = plt.figure(figsize=(8.6, 5.6), facecolor=PAPER)
        ax = fig.add_axes([0.03, 0.06, 0.88, 0.76])
        snapshot(ax, tt, n=300)
        hh = I.fmt_time(tt + UTC, seconds=False)
        header(fig, f"ظل القمر الساعة {hh} بتوقيت مصر", f"{I.fmt_time(tt, seconds=False)} بالتوقيت العالمي — الظل الكامل بالأسود وشبه الظل بالبرتقالي")
        footer(fig, SRC)
        save(fig, CH, f"shadow_{int(tt * 100):04d}", f"موقع ظل القمر الساعة {hh} بتوقيت مصر (محسوب).", "map")


# ------------------------------------------------------------------ Egyptian cities charts
def egypt_rows():
    rows = []
    for n, g, la, lo, own in EGYPT_CITIES:
        c = circ_city(la, lo)
        rows.append(dict(name=I.place(n), gov=I.governorate(g), la=la, lo=lo, own=own, **c))
    return rows


def fig_city_durations(rows):
    tot = sorted([r for r in rows if r["duration_s"] > 0], key=lambda r: r["duration_s"])
    fig = page(8.0, 1.4 + 0.27 * len(tot))
    header(fig, "مدة الكلية في مدن مصر", "المدن الواقعة داخل المسار مرتبةً حسب مدة الكلية")
    ax = fig.add_axes([0.05, 0.05, 0.66, 1 - 1.4 / fig.get_figheight()])
    ys = np.arange(len(tot))
    ax.barh(ys, [r["duration_s"] / 60 for r in tot], color=BLUE[9], height=0.66)
    for y, r in zip(ys, tot):
        ax.text(r["duration_s"] / 60 + 0.06, y, I.fmt_dur(r["duration_s"]), va="center", ha="right", fontsize=8.6)
    ax.set_yticks(ys)
    ax.set_yticklabels([f"{r['name']} ({r['gov']})" for r in tot], fontsize=9.5)
    ax.yaxis.tick_right()
    ax.invert_xaxis()
    ax.set_xlim(7.3, 0)
    style_axes(ax)
    arabic_ticks(ax, y=False)
    footer(fig, SRC)
    save(fig, CH, "egypt_cities_totality", "مدة الكلية في المدن المصرية الواقعة داخل المسار (محسوبة).", "chart")


def fig_city_obscuration(rows):
    par = sorted([r for r in rows if r["duration_s"] <= 0], key=lambda r: r["obscuration"])
    fig = page(8.0, 1.4 + 0.30 * len(par))
    header(fig, "مدن خارج المسار: كم تختفي الشمس؟", "نسبة احتجاب قرص الشمس عند الذروة — لا تنزع النظارة مطلقًا في هذه المدن")
    ax = fig.add_axes([0.05, 0.05, 0.66, 1 - 1.4 / fig.get_figheight()])
    ys = np.arange(len(par))
    ax.barh(ys, [r["obscuration"] * 100 for r in par], color=SUN_DEEP, height=0.66)
    for y, r in zip(ys, par):
        ax.text(r["obscuration"] * 100 + 0.3, y, I.pct(r["obscuration"] * 100), va="center", ha="right", fontsize=8.6)
    ax.set_yticks(ys)
    ax.set_yticklabels([f"{r['name']} ({r['gov']})" for r in par], fontsize=9.5)
    ax.yaxis.tick_right()
    ax.invert_xaxis()
    ax.set_xlim(104, 80)
    style_axes(ax)
    arabic_ticks(ax, y=False)
    footer(fig, SRC)
    save(fig, CH, "egypt_cities_partial", "نسبة احتجاب الشمس في المدن المصرية الواقعة خارج مسار الكلية (محسوبة).", "chart")


def fig_gantt(rows):
    pick = ["الإسكندرية", "القاهرة", "الفيوم", "بني سويف", "المنيا", "أسيوط", "سوهاج", "قنا", "الأقصر", "إسنا", "إدفو",
            "أسوان", "أبو سمبل", "الغردقة", "سفاجا", "القصير", "مرسى علم", "برنيس", "الخارجة", "سيوة", "شرم الشيخ"]
    sel = [r for p in pick for r in rows if r["name"] == p]
    fig = page(8.8, 7.0)
    header(fig, "جدول اليوم: من بداية الكسوف إلى نهايته", "الشريط البرتقالي = الكسوف الجزئي، والأزرق الداكن = الكلية (بتوقيت مصر الصيفي)")
    ax = fig.add_axes([0.04, 0.09, 0.74, 0.74])
    for k, r in enumerate(sel):
        ax.barh(k, (r["c4"] - r["c1"]) * 60, left=(r["c1"] + UTC - 11) * 60, color=ORANGE[3], height=0.55)
        if r["duration_s"] > 0:
            w = max((r["c3"] - r["c2"]) * 60, 1.2)
            ax.barh(k, w, left=(r["c2"] + UTC - 11) * 60 - (w - (r["c3"] - r["c2"]) * 60) / 2, color=NAVY, height=0.75)
            ax.text((r["c3"] + UTC - 11) * 60 + 2.5, k, I.fmt_dur(r["duration_s"]), va="center", fontsize=7.6, color=NAVY)
    ax.set_yticks(range(len(sel)))
    ax.set_yticklabels([r["name"] for r in sel], fontsize=9.5)
    ax.yaxis.tick_right()
    ax.invert_yaxis()
    xt = np.arange(0, 241, 30)
    ax.set_xticks(xt)
    ax.set_xticklabels([I.fmt_time(11 + m / 60, seconds=False) for m in xt])
    ax.set_xlim(0, 240)
    style_axes(ax)
    footer(fig, SRC)
    save(fig, CH, "egypt_cities_gantt", "مخطط زمني لمراحل الكسوف في مدن مصرية مختارة (محسوب).", "chart")


def light_curve(la, lo, t):
    return np.array([float(C.instant(B, tt - T0, [la], [lo])["obscuration"][0]) for tt in t])


def fig_light_curves(rows):
    t = np.linspace(8.4, 11.7, 700)
    fig = page(8.8, 5.2)
    header(fig, "منحنى الضوء: كيف تختفي الشمس وتعود؟", "نسبة الجزء المرئي من قرص الشمس مع الزمن (بتوقيت مصر)")
    ax = fig.add_axes([0.07, 0.13, 0.78, 0.64])
    for (name, la, lo), col in zip([("الأقصر", 25.6872, 32.6396), ("أسوان", 24.0889, 32.8998), ("القاهرة", 30.0444, 31.2357),
                                   ("الإسكندرية", 31.2001, 29.9187)], [NAVY, BLUE[6], SUN_DEEP, ORANGE[4]]):
        ob = light_curve(la, lo, t)
        ax.plot(t + UTC, (1 - ob) * 100, color=col, lw=2, label=name)
    ax.set_ylabel("الجزء المرئي من الشمس (٪)")
    xt = np.arange(11.5, 14.76, 0.5)
    ax.set_xticks(xt)
    ax.set_xticklabels([I.fmt_time(x, seconds=False) for x in xt])
    style_axes(ax)
    arabic_ticks(ax, x=False)
    mirror_y(ax)
    ax.legend(loc="center left", bbox_to_anchor=(0.0, 0.42), frameon=False, fontsize=10)
    ax.annotate("الكلية في الأقصر:\nالضوء صفر ٪ لمدة ٦ دقائق و٢٠ ثانية", (13.09, 0), xytext=(14.05, 38), fontsize=9,
                arrowprops=dict(arrowstyle="-", color=NAVY))
    footer(fig, SRC + "؛ المقصود نسبة مساحة القرص الظاهرة، والإضاءة الفعلية تنخفض بنسبة مشابهة.")
    save(fig, CH, "light_curves", "منحنى نسبة قرص الشمس الظاهر مع الزمن في الأقصر وأسوان والقاهرة والإسكندرية (محسوب).", "chart")


def fig_why_9999_isnt_total():
    fig = page(8.6, 4.8, NAVY)
    ax = canvas(fig)
    header(fig, "لماذا لا تكفي ٩٩٪؟", "الفرق بين الكسوف الجزئي العميق والكلي ليس ١٪ بل عالم كامل", color="white", sub_color="#c9d3e3")
    for k, (lab, f, desc) in enumerate([("القاهرة ٩٤٫٨٪", 0.30, "نهار خافت، والشمس ما زالت تعمي العين"),
                                        ("أسوان ٩٩٫٨٪", 0.06, "هلال رفيع لكنه أسطع من البدر بآلاف المرات"),
                                        ("الأقصر ١٠٠٪", 0.0, "ليل في وضح النهار، والهالة تظهر بالعين المجردة")]):
        cx = 0.80 - k * 0.30
        sun = sun_disk(ax, cx, 0.50, 0.07, glow=k < 2)
        if k == 2:
            corona(ax, cx, 0.50, 0.07, extent=0.6)
        moon_disk(ax, cx + f * 0.14, 0.50, 0.07 * 1.035, color=NAVY, clip=sun)
        ax.text(cx, 0.24, lab, ha="center", color=SUN if k < 2 else "white", fontsize=13, fontweight="bold", fontfamily=TITLE)
        ax.text(cx, 0.16, wrap(desc, 26), ha="center", va="top", color="#c9d3e3", fontsize=9.2)
    save(fig, CH, "partial_vs_total", "مقارنة بين كسوف جزئي بنسبة ٩٤٫٨٪ و٩٩٫٨٪ والكسوف الكلي.")


def fig_c2_along_nile(rows):
    sel = [r for r in rows if r["duration_s"] > 0]
    fig = page(8.4, 5.2)
    header(fig, "الظل يجتاح وادي النيل", "توقيت بداية الكلية (التماس الثاني) في المدن داخل المسار، حسب خط العرض")
    ax = fig.add_axes([0.08, 0.13, 0.80, 0.64])
    ax.scatter([r["c2"] + UTC for r in sel], [r["la"] for r in sel], s=[r["duration_s"] / 4 for r in sel], c=BLUE[9],
               alpha=0.8, edgecolor="white")
    for r in sel:
        ax.text(r["c2"] + UTC + 0.004, r["la"] + 0.05, r["name"], fontsize=8.2)
    xt = np.arange(12.70, 13.30, 0.05)
    ax.set_xticks(xt)
    ax.set_xticklabels([I.fmt_time(x, seconds=False) for x in xt], fontsize=8)
    ax.set_ylabel("خط العرض (° شمالًا)")
    style_axes(ax)
    arabic_ticks(ax, x=False)
    mirror_y(ax)
    footer(fig, SRC + "؛ حجم الدائرة يتناسب مع مدة الكلية.")
    save(fig, CH, "c2_times_egypt", "توقيت بداية الكلية في المدن المصرية حسب خط العرض (محسوب).", "chart")


def fig_sun_position(rows):
    from skyfield.api import wgs84
    ts, eph = besselian.ephemeris()
    fig = page(8.4, 5.6)
    header(fig, "أين أنظر؟ موقع الشمس لحظة الذروة", "ارتفاع الشمس واتجاهها في مدن مصرية — الشمس قريبة جدًا من سمت الرأس")
    ax = fig.add_axes([0.08, 0.12, 0.80, 0.66])
    for r in rows:
        if not r["own"]:
            continue
        t = ts.ut1(2027, 8, 2, 0, 0, r["tmax"] * 3600)
        a, z, _ = (eph["earth"] + wgs84.latlon(r["la"], r["lo"])).at(t).observe(eph["sun"]).apparent().altaz()
        ax.plot(z.degrees, a.degrees, "o", ms=7, color=NAVY if r["duration_s"] > 0 else SUN_DEEP, mec="white")
        ax.annotate(r["name"], (z.degrees, a.degrees), xytext=(4, 4), textcoords="offset points", fontsize=8,
                    path_effects=halo())
    ax.set_xlabel("الاتجاه (السمت) بالدرجات: ١٨٠ = الجنوب")
    ax.set_ylabel("الارتفاع فوق الأفق (°)")
    style_axes(ax)
    arabic_ticks(ax, fmt="{:.0f}")
    mirror_y(ax)
    footer(fig, SRC + "؛ الأزرق داخل المسار والبرتقالي خارجه.")
    save(fig, CH, "sun_position_cities", "ارتفاع الشمس واتجاهها لحظة الذروة في المدن المصرية (محسوب).", "chart")


def fig_countries_best():
    best = []
    for key, (cname, codes, utc, tz, *_b) in COUNTRIES.items():
        if key == "gibraltar":
            continue
        rr = []
        for n, la, lo in CITIES[key]:
            c = circ_city(la, lo)
            rr.append((c["duration_s"], n))
        d, n = max(rr)
        best.append((I.AR_COUNTRIES[key], I.place(n), d))
    best.sort(key=lambda r: r[2])
    fig = page(8.4, 5.4)
    header(fig, "أطول كلية في مدينة رئيسية بكل دولة", "مقارنة بين الدول التي يعبرها المسار")
    ax = fig.add_axes([0.06, 0.10, 0.58, 0.70])
    ys = np.arange(len(best))
    ax.barh(ys, [b[2] / 60 for b in best], color=[RED if b[0] == "مصر" else BLUE[7] for b in best], height=0.62)
    for y, b in zip(ys, best):
        ax.text(b[2] / 60 + 0.05, y, I.fmt_dur(b[2]), va="center", ha="right", fontsize=8.8)
    ax.set_yticks(ys)
    ax.set_yticklabels([f"{b[0]} — {b[1]}" for b in best], fontsize=9.5)
    ax.yaxis.tick_right()
    ax.invert_xaxis()
    ax.set_xlim(7.2, 0)
    style_axes(ax)
    arabic_ticks(ax, y=False)
    footer(fig, SRC + "؛ من قائمة مدن مختارة لكل دولة.")
    save(fig, CH, "countries_best_city", "أطول مدة للكلية في مدينة رئيسية من كل دولة على المسار (محسوبة).", "chart")


# ------------------------------------------------------------------ city cards
def fig_city_card(r):
    tot = r["duration_s"] > 0
    fig = page(7.0, 8.6, NAVY if tot else PAPER)
    ax = canvas(fig)
    fg = "white" if tot else INK
    fg2 = "#c9d3e3" if tot else INK2
    header(fig, f"{r['name']} — بطاقة الكسوف", f"محافظة {r['gov']} | {I.fmt_lat(r['la'], 2)}  {I.fmt_lon(r['lo'], 2)}",
           color=fg, sub_color=fg2)
    big = I.fmt_dur(r["duration_s"], long=True) if tot else I.pct(r["obscuration"] * 100)
    ax.text(0.5, 0.78, big, ha="center", color=SUN if tot else SUN_DEEP, fontsize=26, fontweight="bold", fontfamily=TITLE)
    ax.text(0.5, 0.735, "مدة الكسوف الكلي" if tot else "نسبة احتجاب الشمس (كسوف جزئي)", ha="center", color=fg2, fontsize=11)
    # phase strip
    fs = [-1.0, -0.5, 0.0, 0.5, 1.0]
    labels = ["بداية الكسوف", "", "الذروة", "", "النهاية"]
    times = [r["c1"], (r["c1"] + r["tmax"]) / 2, r["tmax"], (r["tmax"] + r["c4"]) / 2, r["c4"]]
    sep = 1 - r["magnitude"] * 2 / (1 + r["ratio"])  # offset fraction at maximum
    for k, f in enumerate(fs):
        cx = 0.86 - k * 0.18
        cy = 0.57
        rr = 0.05
        ff = f if f != 0 else (0 if tot else max(sep, 0.04))
        sun = sun_disk(ax, cx, cy, rr, glow=False)
        if tot and k == 2:
            corona(ax, cx, cy, rr, extent=0.45)
        moon_disk(ax, cx - ff * 2.05 * rr * (1 if abs(f) == 1 else 0.9), cy, rr * 1.03,
                  color=NAVY if tot else PAPER, clip=sun)
        ax.text(cx, cy - rr * ax._asp - 0.035, I.fmt_time(times[k] + UTC, seconds=False), ha="center", color=fg,
                fontsize=10, fontweight="bold")
        if labels[k]:
            ax.text(cx, cy - rr * ax._asp - 0.07, labels[k], ha="center", color=fg2, fontsize=8.5)
    # table
    rows = [("بداية الكسوف الجزئي", I.fmt_time(r["c1"] + UTC)),
            ("بداية الكلية", I.fmt_time(r["c2"] + UTC) if tot else "—"),
            ("ذروة الكسوف", I.fmt_time(r["tmax"] + UTC)),
            ("نهاية الكلية", I.fmt_time(r["c3"] + UTC) if tot else "—"),
            ("نهاية الكسوف الجزئي", I.fmt_time(r["c4"] + UTC)),
            ("ارتفاع الشمس عند الذروة", A(f"{r['sun_alt_deg']:.0f}") + "°"),
            ("قدر الكسوف", A(f"{r['magnitude']:.3f}"))]
    for k, (a, b) in enumerate(rows):
        y = 0.36 - k * 0.042
        ax.plot([0.10, 0.90], [y - 0.02, y - 0.02], color="#2a3d5c" if tot else LINE, lw=0.7)
        ax.text(0.90, y, a, ha="right", va="center", color=fg2, fontsize=10)
        ax.text(0.10, y, b, ha="left", va="center", color=fg, fontsize=10.5, fontweight="bold")
    note = ("انزع النظارة فقط بعد اختفاء آخر ضوء للشمس، وأعدها فور ظهور الخاتم الماسي الثاني" if tot else
            "خارج مسار الكلية: لا تنزع نظارة الكسوف في أي لحظة")
    ax.text(0.5, 0.045, note, ha="center", color=SUN if tot else RED, fontsize=9.5, fontweight="bold")
    ax.text(0.5, 0.015, "الأوقات بتوقيت مصر الصيفي (ت.ع +٣) | " + SRC, ha="center", color=fg2, fontsize=7)
    from eclipse2027.maps import slug
    en = [n for n, g, la, lo, own in EGYPT_CITIES if I.place(n) == r["name"]][0]
    save(fig, CH, f"city_card_{slug(en)}", f"بطاقة الكسوف لمدينة {r['name']} (محسوبة).")


def fig_city_table(rows, total, page_no):
    sel = sorted([r for r in rows if (r["duration_s"] > 0) == total],
                 key=lambda r: (-r["duration_s"], -r["obscuration"]))
    H = 2.0 + 0.30 * len(sel)
    fig = page(8.6, H)
    ax = canvas(fig)
    header(fig, "جدول مواعيد الكسوف في المدن المصرية" + (" — داخل مسار الكلية" if total else " — خارج مسار الكلية"),
           "بتوقيت مصر الصيفي (التوقيت العالمي +٣)، محسوب لكل مدينة")
    cols = ["المدينة", "المحافظة", "البداية", "بداية الكلية", "الذروة", "نهاية الكلية", "النهاية",
            "المدة" if total else "الاحتجاب"]
    xs = [0.97, 0.80, 0.665, 0.56, 0.455, 0.35, 0.245, 0.12]
    y0 = 1 - 1.30 / H
    for x, c in zip(xs, cols):
        ax.text(x, y0, c, ha="right" if x > 0.7 else "center", fontsize=9.5, fontweight="bold", color=BLUE[10])
    for i, r in enumerate(sel):
        y = y0 - (i + 1) * 0.30 / H
        if i % 2 == 0:
            ax.add_patch(plt.Rectangle((0.02, y - 0.13 / H), 0.96, 0.26 / H, fc="#f1efea", ec="none",
                                       transform=ax.transAxes))
        vals = [r["name"], r["gov"], I.fmt_time(r["c1"] + UTC), I.fmt_time(r["c2"] + UTC) if total else "—",
                I.fmt_time(r["tmax"] + UTC), I.fmt_time(r["c3"] + UTC) if total else "—", I.fmt_time(r["c4"] + UTC),
                I.fmt_dur(r["duration_s"]) if total else I.pct(r["obscuration"] * 100)]
        for k, (x, v) in enumerate(zip(xs, vals)):
            ax.text(x, y, v, ha="right" if x > 0.7 else "center", va="center", fontsize=9.2,
                    fontweight="bold" if k in (0, 7) else "normal")
    footer(fig, SRC)
    save(fig, CH, f"egypt_timetable_{'total' if total else 'partial'}",
         "جدول مواعيد الكسوف في المدن المصرية " + ("داخل مسار الكلية" if total else "خارج مسار الكلية") + " (محسوب).")


def main():
    G = greatest()
    fig_key_numbers(G)
    fig_country_crossings()
    fig_countries_best()
    fig_snapshots_grid()
    fig_snapshot_frames()
    rows = egypt_rows()
    fig_city_table(rows, True, 1)
    fig_city_table(rows, False, 2)
    fig_city_durations(rows)
    fig_city_obscuration(rows)
    fig_gantt(rows)
    fig_light_curves(rows)
    fig_why_9999_isnt_total()
    fig_c2_along_nile(rows)
    fig_sun_position(rows)
    for r in rows:
        if r["own"]:
            fig_city_card(r)
    write_catalogue("ch3")


if __name__ == "__main__":
    main()
