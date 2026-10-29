"""Appendix — every solar eclipse 2024–2045, computed here, with emphasis on Egypt, Africa and the Middle East.

Inspired by Appendix A of Littmann & Espenak, «Totality» (2024); the maps here are our own, computed from
DE421, and Espenak's published values (data/reference/espenak_2024_2045.json) are used only as a cross-check.
"""
import datetime as dt
import json
import os

import numpy as np

import mapkit as MK
from common import (A, BLUE, GREEN, INK, INK2, LINE, MUTED, NAVY, ORANGE, PAPER, RED, ROOT, SUN, SUN_DEEP, TITLE,
                    canvas, footer, halo, header, page, plt, save, wrap, write_catalogue)
from eclipse2027 import circumstances as C, engine as E, i18n as I

CH = 11
SRC = "المصدر: حسابات المؤلف من تقويم JPL DE421"
Y0, Y1 = 2024, 2045
KIND_AR = {"total": "كلي", "annular": "حلقي", "hybrid": "هجين", "partial": "جزئي"}
KIND_COL = {"total": RED, "annular": SUN_DEEP, "hybrid": "#7a4fc2", "partial": "#6d6d68"}
MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
REGION = (-20.0, 65.0, -36.0, 43.0)      # Africa and the Middle East
EGYPT_SITES = [("القاهرة", 30.0444, 31.2357), ("الإسكندرية", 31.2001, 29.9187), ("الأقصر", 25.6872, 32.6396),
               ("أسوان", 24.0889, 32.8998)]
REGION_CITIES = [("القاهرة", 30.04, 31.24), ("الرياض", 24.71, 46.68), ("بغداد", 33.31, 44.37), ("طهران", 35.69, 51.39),
                 ("الدار البيضاء", 33.57, -7.59), ("لاغوس", 6.52, 3.38), ("نيروبي", -1.29, 36.82), ("دبي", 25.20, 55.27),
                 ("الخرطوم", 15.50, 32.56), ("كيب تاون", -33.92, 18.42), ("كينشاسا", -4.32, 15.31), ("تونس", 36.81, 10.18)]


def pct(v):
    """Percent with one decimal near 100 so that 99.8 % is never shown as 100 %."""
    return I.pct(v * 100, 1 if v >= 0.995 else 0)


def date_ar(y, m, d):
    return f"{A(d)} {MONTHS[m - 1]} {A(y)}"


# ------------------------------------------------------------------ data
def reference():
    p = os.path.join(ROOT, "data", "reference", "espenak_2024_2045.json")
    ref = json.load(open(p, encoding="utf-8"))["eclipses"]
    return {dt.datetime.strptime(r["date"], "%Y %b %d").date(): r for r in ref}


def compute():
    cache = os.path.join(ROOT, "results", "eclipses_2024_2045.json")
    if os.path.exists(cache):
        rows = json.load(open(cache, encoding="utf-8"))
    else:
        rows = []
        for jd in E.new_moons(Y0, Y1 + 1):
            ec = None
            from eclipse2027.besselian import ephemeris
            ts, eph = ephemeris()
            t = ts.ut1_jd(jd)
            e = eph["earth"].at(t)
            if e.observe(eph["sun"]).apparent().separation_from(e.observe(eph["moon"]).apparent()).degrees > 1.8:
                continue
            ec = E.eclipse_near(jd, "de421")
            if ec.kind == "none":
                continue
            rows.append(summarize(ec))
        json.dump(rows, open(cache, "w", encoding="utf-8"), ensure_ascii=False)
    ref = reference()
    for r in rows:
        d = dt.date(*r["date"])
        best = min(ref, key=lambda k: abs((k - d).days))
        r["ref"] = ref[best] if abs((best - d).days) <= 1 else None
        r["saros"] = r["ref"]["saros"] if r["ref"] else None
    return rows


def summarize(ec):
    B = ec.B
    tg = ec.hour_ut - B.t0_hours
    out = dict(date=list(ec.date), hour=ec.hour_ut, kind=ec.kind, gamma=ec.gamma, t0=B.t0_hours)
    out["B"] = dict(x=list(B.x), y=list(B.y), d=list(B.d), mu=list(B.mu), l1=list(B.l1), l2=list(B.l2),
                    tan_f1=B.tan_f1, tan_f2=B.tan_f2)
    la, lo = C.central_line(B, np.array([tg]))
    if np.isfinite(la[0]):
        r = C.local_circumstances(B, la, lo)
        out.update(ge_lat=float(la[0]), ge_lon=float(lo[0]), ge_dur=float(r["duration_s"][0]), ge_alt=float(r["sun_alt_deg"][0]))
    sites = {}
    for n, sla, slo in EGYPT_SITES:
        r = C.local_circumstances(B, np.array([sla]), np.array([slo]))
        sites[n] = dict(obsc=float(r["obscuration"][0]), mag=float(r["magnitude"][0]), tmax=float(r["tmax"][0]),
                        alt=float(r["sun_alt_deg"][0]), dur=float(r["duration_s"][0]))
    out["egypt"] = sites
    return out


def besselian(r):
    from eclipse2027.besselian import Besselian
    b = r["B"]
    B = Besselian(x=np.array(b["x"]), y=np.array(b["y"]), d=np.array(b["d"]), mu=np.array(b["mu"]),
                  l1=np.array(b["l1"]), l2=np.array(b["l2"]), tan_f1=b["tan_f1"], tan_f2=b["tan_f2"])
    B.t0_hours = r["t0"]
    return B


def central_track(B):
    t = np.linspace(-3.4, 3.4, 700)
    la, lo = C.central_line(B, t)
    ok = np.isfinite(la)
    if ok.sum() < 3:
        return None
    t = t[ok]
    lac, loc, ln, on, ls, os_ = C.path_limits(B, t[:: max(1, len(t) // 220)])
    return lac, loc, ln, on, ls, os_


def crosses_region(track):
    if track is None:
        return False
    lac, loc = track[0], track[1]
    lon0, lon1, lat0, lat1 = REGION
    return bool(np.any((loc > lon0) & (loc < lon1) & (lac > lat0) & (lac < lat1)))


def unwrap_nan(lo):
    lo = np.array(lo, float)
    lo[np.where(np.abs(np.diff(lo)) > 180)[0]] = np.nan
    return lo


# ------------------------------------------------------------------ global small multiples
_LAND = None


def world_panel(ax, r, B, track):
    lon = np.arange(-180, 180.1, 2.0)
    lat = np.arange(-80, 80.1, 2.0)
    LON, LAT = np.meshgrid(lon, lat)
    res = C.local_circumstances(B, LAT.ravel(), LON.ravel(), iterations=5)
    mag = np.where(res["sun_up"], res["magnitude"], 0).reshape(LON.shape)
    MK.base(ax, -180, 180, -80, 80, highlight=("EGY",), admin1=None)
    ax.contourf(LON, LAT, mag, levels=[0.001, 0.25, 0.5, 0.75, 2], colors=["#fbe1c4", "#f4ba78", "#e88a2c", "#b55a12"],
                alpha=0.55, zorder=2)
    cs = ax.contour(LON, LAT, mag, levels=[0.25, 0.5, 0.75], colors=ORANGE[-1], linewidths=0.5, zorder=3)
    ax.clabel(cs, fmt=lambda v: A(f"{v * 100:.0f}") + "٪", fontsize=5.5)
    if track is not None:
        lac, loc, ln, on, ls, os_ = track
        col = KIND_COL[r["kind"]]
        ax.plot(unwrap_nan(on), ln, color=col, lw=0.9, zorder=5)
        ax.plot(unwrap_nan(os_), ls, color=col, lw=0.9, zorder=5)
        ax.plot(unwrap_nan(loc), lac, color=col, lw=1.8, zorder=5)
    if "ge_lat" in r:
        ax.plot(r["ge_lon"], r["ge_lat"], marker="*", ms=7, color=INK, zorder=6)
    lon0, lon1, lat0, lat1 = REGION
    if crosses_region(track):
        ax.add_patch(plt.Rectangle((lon0, lat0), lon1 - lon0, lat1 - lat0, fc="none", ec=RED, lw=1.0, ls="--", zorder=6))
    ax.set_xticks([])
    ax.set_yticks([])


def panel_title(ax, r):
    y, m, d = r["date"]
    col = KIND_COL[r["kind"]]
    sar = f" | ساروس {A(r['saros'])}" if r.get("saros") else ""
    ax.set_title(f"{KIND_AR[r['kind']]} — {date_ar(y, m, d)}", fontsize=10, fontweight="bold", color=col, pad=19)
    ax.text(0.5, 1.02, f"{I.fmt_time(r['hour'], seconds=False)} ت.ع{sar} | غاما {A(f'{r['gamma']:.3f}')}",
            transform=ax.transAxes, ha="center", va="bottom", fontsize=7.6, color=INK2)
    if r["kind"] in ("total", "annular", "hybrid") and "ge_dur" in r:
        bottom = f"المدة عند الذروة {I.fmt_dur(r['ge_dur'])} | ارتفاع الشمس {A(f'{r['ge_alt']:.0f}')}°"
    elif r["kind"] in ("total", "annular"):
        bottom = "غير مركزي: يمسّ الظلُّ الأرضَ قرب القطب دون خط مركز"
    else:
        bottom = "كسوف جزئي فقط (لا يمر ظل القمر الكامل على الأرض)"
    cairo = r["egypt"]["القاهرة"]["obsc"]
    bottom += f" | القاهرة: {I.pct(cairo * 100, 0) if cairo > 0 else 'لا يُرى'}"
    ax.text(0.5, -0.03, bottom, transform=ax.transAxes, ha="center", va="top", fontsize=7.4, color=INK)


def fig_world_pages(rows, tracks):
    per = 6
    for p in range(0, len(rows), per):
        chunk = rows[p:p + per]
        fig = page(8.6, 10.2)
        a, b = chunk[0]["date"][0], chunk[-1]["date"][0]
        header(fig, f"كل كسوفات الشمس {A(Y0)}–{A(Y1)} ({A(p // per + 1)} من {A((len(rows) + per - 1) // per)})",
               f"من {date_ar(*chunk[0]['date'])} إلى {date_ar(*chunk[-1]['date'])} — البرتقالي: نسبة تغطية قطر الشمس، "
               "والخط الملوّن: مسار الكلية أو الحلقية")
        for k, r in enumerate(chunk):
            col, row = k % 2, k // 2
            ax = fig.add_axes([0.52 - col * 0.48, 0.615 - row * 0.275, 0.44, 0.2])
            world_panel(ax, r, besselian(r), tracks[id(r)])
            panel_title(ax, r)
        footer(fig, SRC + ". النجمة: موضع أعظم كسوف؛ المستطيل الأحمر المتقطع: مسار مركزي يعبر أفريقيا أو الشرق الأوسط.")
        save(fig, CH, f"world_eclipses_{a}_{b}", f"خرائط عالمية لكسوفات الشمس {A(a)}–{A(b)} (محسوبة).", "map")


# ------------------------------------------------------------------ statistics
def fig_stats(rows):
    counts = {k: sum(1 for r in rows if r["kind"] == k) for k in KIND_AR}
    n = len(rows)
    canon = {"total": 26.7, "annular": 33.2, "hybrid": 4.8, "partial": 35.3}   # 2000 BCE–3000 CE (Espenak & Meeus)
    fig = page(8.4, 5.4)
    header(fig, f"{A(n)} كسوفًا للشمس بين {A(Y0)} و{A(Y1)}",
           "توزيع الأنواع في هذه الفترة مقارنةً بخمسة آلاف عام (٢٠٠٠ ق.م – ٣٠٠٠م)")
    ax = fig.add_axes([0.08, 0.16, 0.84, 0.60])
    ks = list(KIND_AR)
    x = np.arange(len(ks))
    ours = [counts[k] / n * 100 for k in ks]
    ax.bar(x + 0.2, ours, width=0.38, color=[KIND_COL[k] for k in ks], label="٢٠٢٤–٢٠٤٥")
    ax.bar(x - 0.2, [canon[k] for k in ks], width=0.38, color=[KIND_COL[k] for k in ks], alpha=0.35, label="خمسة آلاف عام")
    for i, k in enumerate(ks):
        ax.text(i + 0.2, ours[i] + 1, f"{A(counts[k])}\n({A(f'{ours[i]:.0f}')}٪)", ha="center", fontsize=9)
        ax.text(i - 0.2, canon[k] + 1, A(f"{canon[k]:.0f}") + "٪", ha="center", fontsize=8.5, color=INK2)
    ax.set_xticks(x)
    ax.set_xticklabels([KIND_AR[k] for k in ks], fontsize=11)
    ax.set_yticks([])
    for s_ in ("top", "right", "left"):
        ax.spines[s_].set_visible(False)
    ax.set_ylim(0, 48)
    ax.text(0.99, 0.95, "الأعمدة الداكنة: ٢٠٢٤–٢٠٤٥ (حسابنا) | الفاتحة: ٢٠٠٠ ق.م–٣٠٠٠م (قانون الألفيات الخمسة لإسبيناك ومييس)",
            transform=ax.transAxes, ha="right", fontsize=8.6, color=INK2)
    footer(fig, SRC + ". تتفق أنواع الكسوفات وأعدادها مع الملحق أ في كتاب «Totality» لليتمان وإسبيناك (٢٠٢٤).")
    save(fig, CH, "eclipse_types_2024_2045", f"توزيع أنواع كسوفات الشمس {A(Y0)}–{A(Y1)} (محسوب).", "chart")


# ------------------------------------------------------------------ central paths over Africa & the Middle East
def fig_region_paths(rows, tracks):
    lon0, lon1, lat0, lat1 = REGION
    fig = plt.figure(figsize=(8.4, 8.6), facecolor=PAPER)
    ax = fig.add_axes([0.04, 0.07, 0.90, 0.78])
    MK.base(ax, lon0, lon1, lat0, lat1, highlight=("EGY",), admin1=None)
    k = 0
    for r in rows:
        tr = tracks[id(r)]
        if not crosses_region(tr):
            continue
        lac, loc, ln, on, ls, os_ = tr
        col = KIND_COL[r["kind"]]
        on_, os2 = unwrap_nan(on), unwrap_nan(os_)
        ok = np.isfinite(on_) & np.isfinite(os2)
        ax.fill(np.r_[on_[ok], os2[ok][::-1]], np.r_[ln[ok], ls[ok][::-1]], color=col, alpha=0.35, lw=0, zorder=3)
        ax.plot(unwrap_nan(loc), lac, color=col, lw=1.0, zorder=4)
        inside = np.where((loc > lon0 + 2) & (loc < lon1 - 2) & (lac > lat0 + 2) & (lac < lat1 - 2))[0]
        j = inside[len(inside) // 2 + (k % 3 - 1) * len(inside) // 5] if len(inside) else 0
        y, m, d = r["date"]
        ax.text(loc[j], lac[j], f"{A(d)} {MONTHS[m - 1]} {A(y)}", fontsize=8.2, color=col, fontweight="bold",
                ha="center", va="center", path_effects=halo(), zorder=6)
        k += 1
    for n, la, lo in REGION_CITIES:
        ax.plot(lo, la, "o", ms=3.5, color=INK, zorder=7)
        ax.text(lo, la - 1.3, n, fontsize=7.6, ha="center", va="top", color=INK2, path_effects=halo(), zorder=7)
    header(fig, f"مسارات الكسوفات المركزية فوق أفريقيا والشرق الأوسط {A(Y0)}–{A(Y1)}",
           "الأحمر كلي، والبرتقالي حلقي، والبنفسجي هجين — أشرطة بعرض مسار الظل الحقيقي")
    footer(fig, SRC + ".")
    save(fig, CH, "central_paths_africa_middle_east", f"مسارات الكسوفات الكلية والحلقية فوق أفريقيا والشرق الأوسط {A(Y0)}–{A(Y1)} (محسوبة).", "map")


def fig_region_detail(r, B, track):
    lon0, lon1, lat0, lat1 = REGION
    fig = plt.figure(figsize=(8.0, 8.2), facecolor=PAPER)
    ax = fig.add_axes([0.04, 0.115, 0.86, 0.71])
    MK.base(ax, lon0, lon1, lat0, lat1, highlight=("EGY",), admin1=None)
    MK.field(ax, B, lon0, lon1, lat0, lat1, n=260)
    MK.path(ax, B, color=NAVY)
    MK.cities(ax, B, REGION_CITIES, lon0, lon1, lat0, lat1, size=7.6)
    y, m, d = r["date"]
    header(fig, f"كسوف {KIND_AR[r['kind']]} — {date_ar(y, m, d)}",
           "فوق أفريقيا والشرق الأوسط: مدة الكلية أو الحلقية (أزرق) ونسبة تغطية الشمس (برتقالي)")
    sar = f" | ساروس {A(r['saros'])}" if r.get("saros") else ""
    info = f"أعظم كسوف {I.fmt_time(r['hour'], seconds=False)} ت.ع عند {I.fmt_lat(r['ge_lat'], 1)} {I.fmt_lon(r['ge_lon'], 1)}" \
           f" | المدة {I.fmt_dur(r['ge_dur'])}{sar}"
    fig.text(0.965, 0.84, info, ha="right", fontsize=8.8, color=INK2)
    eg = r["egypt"]
    fig.text(0.965, 0.042, "في مصر: " + " | ".join(
        f"{n} {pct(v['obsc']) if v['obsc'] > 0 and v['alt'] > 0 else 'لا يُرى'}" for n, v in eg.items()),
        ha="right", fontsize=8.8, color=INK)
    footer(fig, SRC + ".")
    save(fig, CH, f"region_{y}_{m:02d}_{d:02d}", f"كسوف {date_ar(y, m, d)} {KIND_AR[r['kind']]} فوق أفريقيا والشرق الأوسط (محسوب).", "map")


# ------------------------------------------------------------------ tables
def fig_table(rows, part, nparts):
    per = (len(rows) + nparts - 1) // nparts
    chunk = rows[(part - 1) * per: part * per]
    H = 1.9 + 0.36 * len(chunk)
    fig = page(9.4, H)
    ax = canvas(fig)
    header(fig, f"جدول كسوفات الشمس {A(Y0)}–{A(Y1)} ({A(part)} من {A(nparts)})",
           "حسابنا مقارنًا بقيم إسبيناك المنشورة؛ وآخر عمود نسبة احتجاب الشمس في القاهرة")
    cols = [(0.965, "التاريخ"), (0.80, "النوع"), (0.72, "ساروس"), (0.64, "الذروة ت.ع"), (0.54, "غاما"),
            (0.43, "المدة (حسابنا)"), (0.31, "المدة (إسبيناك)"), (0.21, "ارتفاع الشمس"), (0.10, "القاهرة")]
    top = 1 - 1.3 / H
    ax.add_patch(plt.Rectangle((0.02, top - 0.17 / H), 0.96, 0.34 / H, fc=NAVY, ec="none"))
    for x, c in cols:
        ax.text(x - 0.005, top, c, ha="right", va="center", fontsize=8.6, color="white", fontweight="bold")
    rh = 0.36 / H
    for i, r in enumerate(chunk):
        yc = top - 0.17 / H - rh * (i + 0.5)
        ax.add_patch(plt.Rectangle((0.02, yc - rh / 2), 0.96, rh, fc="#f1efea" if i % 2 == 0 else "white", ec="none"))
        y, m, d = r["date"]
        ref = r.get("ref") or {}
        central = r["kind"] != "partial" and "ge_dur" in r
        cairo = r["egypt"]["القاهرة"]
        noncentral = r["kind"] in ("total", "annular") and "ge_dur" not in r
        vals = [date_ar(y, m, d), KIND_AR[r["kind"]] + (" *" if noncentral else ""), A(r["saros"]) if r.get("saros") else "—",
                I.fmt_time(r["hour"], seconds=False), A(f"{r['gamma']:.4f}"),
                I.fmt_dur(r["ge_dur"]) if central else "—",
                (ref.get("duration") or "—").replace("m", " د ").replace("s", " ث") if central else "—",
                (A(f"{r['ge_alt']:.0f}") + "°") if central else "—",
                pct(cairo["obsc"]) if cairo["obsc"] > 0 and cairo["alt"] > 0 else "—"]
        vals[6] = A(vals[6]) if vals[6] != "—" else vals[6]
        for (x, _), v in zip(cols, vals):
            ax.text(x - 0.005, yc, v, ha="right", va="center", fontsize=8.4,
                    color=KIND_COL[r["kind"]] if x == 0.80 else (RED if x == 0.10 and v != "—" else INK),
                    fontweight="bold" if x in (0.965, 0.80) else "normal")
    footer(fig, SRC + ". قيم إسبيناك من الملحق أ في «Totality» (٢٠٢٤)؛ المدة عند نقطة أعظم كسوف، والثواني مقطوعة. "
           "* غير مركزي: يمسّ الظل الأرض قرب القطب دون خط مركز.")
    save(fig, CH, f"eclipses_table_{part}", f"جدول كسوفات الشمس {A(Y0)}–{A(Y1)} ({A(part)} من {A(nparts)}) مع المقارنة بقيم إسبيناك.")


def fig_egypt_table(rows):
    vis = [r for r in rows if any(v["obsc"] > 0 and v["alt"] > 0 for v in r["egypt"].values())]
    H = 1.9 + 0.4 * len(vis)
    fig = page(8.8, H)
    ax = canvas(fig)
    header(fig, f"كسوفات تُرى من مصر {A(Y0)}–{A(Y1)}", "نسبة احتجاب قرص الشمس ووقت الذروة بتوقيت مصر، في أربع مدن")
    names = [n for n, _, _ in EGYPT_SITES]
    cols = [(0.965, "التاريخ"), (0.78, "النوع")] + [(0.62 - k * 0.16, n) for k, n in enumerate(names)]
    top = 1 - 1.3 / H
    ax.add_patch(plt.Rectangle((0.02, top - 0.17 / H), 0.96, 0.34 / H, fc=NAVY, ec="none"))
    for x, c in cols:
        ax.text(x - 0.01, top, c, ha="right", va="center", fontsize=9.2, color="white", fontweight="bold")
    rh = 0.4 / H
    for i, r in enumerate(vis):
        yc = top - 0.17 / H - rh * (i + 0.5)
        ax.add_patch(plt.Rectangle((0.02, yc - rh / 2), 0.96, rh, fc="#f1efea" if i % 2 == 0 else "white", ec="none"))
        y, m, d = r["date"]
        hl = (y, m, d) == (2027, 8, 2)
        ax.text(0.955, yc, date_ar(y, m, d), ha="right", va="center", fontsize=9, fontweight="bold", color=RED if hl else INK)
        ax.text(0.77, yc, KIND_AR[r["kind"]], ha="right", va="center", fontsize=9, color=KIND_COL[r["kind"]])
        for k, n in enumerate(names):
            v = r["egypt"][n]
            if v["obsc"] > 0 and v["alt"] > 0:
                off = 3 if y >= 2023 else 2
                txt = (f"كلي {I.fmt_dur(v['dur'])}" if v["dur"] > 0 and r["kind"] != "annular" else pct(v["obsc"])) + \
                      " | " + I.fmt_time(v["tmax"] + egypt_offset(y, m, d), seconds=False)
            else:
                txt = "—"
            ax.text(0.61 - k * 0.16, yc, txt, ha="right", va="center", fontsize=8.6, color=RED if hl else INK)
    footer(fig, SRC + ". التوقيت المحلي: صيفي (ت.ع+٣) من آخر جمعة في أبريل إلى آخر خميس في أكتوبر، وشتوي (ت.ع+٢) فيما عداه.")
    save(fig, CH, "egypt_visibility_2024_2045", f"الكسوفات التي تُرى من مصر {A(Y0)}–{A(Y1)} ونسبها في أربع مدن (محسوب).")


def egypt_offset(y, m, d):
    """Egypt's legal time offset (h): EEST from the last Friday of April to the last Thursday of October (since 2023)."""
    def last(weekday, month):
        day = dt.date(y, month + 1, 1) - dt.timedelta(days=1)
        while day.weekday() != weekday:
            day -= dt.timedelta(days=1)
        return day
    return 3 if last(4, 4) <= dt.date(y, m, d) <= last(3, 10) else 2


# ------------------------------------------------------------------ main
def main():
    rows = compute()
    tracks = {id(r): (central_track(besselian(r)) if r["kind"] != "partial" else None) for r in rows}
    fig_stats(rows)
    fig_table(rows, 1, 2)
    fig_table(rows, 2, 2)
    fig_egypt_table(rows)
    fig_region_paths(rows, tracks)
    for r in rows:
        if crosses_region(tracks[id(r)]):
            fig_region_detail(r, besselian(r), tracks[id(r)])
    fig_world_pages(rows, tracks)
    write_catalogue("ch11")


if __name__ == "__main__":
    main()
