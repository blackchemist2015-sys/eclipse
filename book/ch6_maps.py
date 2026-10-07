"""Chapter 6 — additional Arabic maps: governorates, regions and the shadow over Egypt."""
import numpy as np

import mapkit as MK
from common import (A, BLUE, INK, INK2, NAVY, ORANGE, PAPER, RED, footer, halo, header, plt, save, write_catalogue)
from common import SUN as SUN_C
from eclipse2027 import besselian, circumstances as C, i18n as I
from eclipse2027.places import EGYPT_CITIES

CH = 6
UTC = 3
B = besselian.compute()
SRC = "المصدر: حسابات المؤلف من تقويم JPL DE421؛ الحدود: Natural Earth."
PTS = [(I.place(n), la, lo) for n, g, la, lo, own in EGYPT_CITIES]

GOVS = ["Luxor", "Qena", "Sohag", "Asyut", "Minya", "Aswan", "Red Sea", "New Valley", "Matrouh", "Giza", "Beni Suef",
        "Faiyum", "Cairo", "South Sinai"]


def gov_map(name_en):
    a1 = MK.geo("admin1_region")
    g = a1[(a1.adm0_a3 == "EGY") & (a1.name_en == name_en)]
    x0, y0, x1, y1 = g.total_bounds
    cx_, cy_ = (x0 + x1) / 2, (y0 + y1) / 2
    lo_a, lo_b = min(x0, cx_ - 0.9), max(x1, cx_ + 0.9)
    la_a, la_b = min(y0, cy_ - 0.8), max(y1, cy_ + 0.8)
    x0, x1, y0, y1 = lo_a, lo_b, la_a, la_b
    gx0, gy0, gx1, gy1 = g.total_bounds
    padx, pady = (x1 - x0) * 0.12 + 0.15, (y1 - y0) * 0.12 + 0.15
    lon0, lon1, lat0, lat1 = x0 - padx, x1 + padx, y0 - pady, y1 + pady
    # keep a pleasant aspect
    w = (lon1 - lon0) * np.cos(np.radians((lat0 + lat1) / 2))
    h = lat1 - lat0
    if w / h < 0.75:
        c = (lon0 + lon1) / 2
        half = 0.75 * h / np.cos(np.radians((lat0 + lat1) / 2)) / 2
        lon0, lon1 = c - half, c + half
    elif w / h > 1.5:
        c = (lat0 + lat1) / 2
        half = w / 1.5 / 2
        lat0, lat1 = c - half, c + half
    fig = plt.figure(figsize=(7.6, 8.0), facecolor=PAPER)
    ax = fig.add_axes([0.04, 0.07, 0.86, 0.77])
    MK.base(ax, lon0, lon1, lat0, lat1, labels=True)
    g.boundary.plot(ax=ax, color=RED, lw=1.8, zorder=7)
    ax.set_xlabel("")
    ax.set_ylabel("")
    MK.field(ax, B, lon0, lon1, lat0, lat1, n=280)
    MK.path(ax, B, -1.7, 1.95)
    shown = []
    span = max(lon1 - lon0, lat1 - lat0)
    pts = sorted(PTS, key=lambda p: 0 if g.geometry.iloc[0].contains(__import__("shapely").geometry.Point(p[2], p[1])) else 1)
    for n, la, lo in pts:
        if lon0 < lo < lon1 and lat0 < la < lat1 and all(np.hypot(la - a, lo - b) > span * 0.06 for a, b in shown):
            shown.append((la, lo))
            MK.cities(ax, B, [(n, la, lo)], lon0, lon1, lat0, lat1, size=8.5)
    # governorate statistics
    LON, LAT = np.meshgrid(np.linspace(gx0, gx1, 160), np.linspace(gy0, gy1, 160))
    import geopandas as gpd
    pts_g = gpd.points_from_xy(LON.ravel(), LAT.ravel())
    inside = np.array(g.geometry.iloc[0].contains(pts_g)) if hasattr(g.geometry.iloc[0], "contains") else None
    inside = np.array([g.geometry.iloc[0].contains(p) for p in pts_g])
    r = C.local_circumstances(B, LAT.ravel()[inside], LON.ravel()[inside])
    dmax = float(np.max(r["duration_s"]))
    frac = float(np.mean(r["duration_s"] > 0)) * 100
    omin = float(np.min(r["obscuration"])) * 100
    nm = I.governorate(name_en)
    if dmax > 0:
        sub = f"أطول كلية داخل المحافظة {I.fmt_dur(dmax, long=True)} | {A(f'{frac:.0f}')}٪ من مساحتها داخل المسار"
    else:
        sub = f"كسوف جزئي فقط: الاحتجاب بين {I.pct(omin)} و{I.pct(float(np.max(r['obscuration'])) * 100)}"
    header(fig, f"محافظة {nm} وكسوف ٢ أغسطس ٢٠٢٧", sub)
    footer(fig, SRC + " الأزرق: مدة الكلية؛ البرتقالي: نسبة الاحتجاب؛ الحد الأحمر: المحافظة.")
    from eclipse2027.maps import slug
    save(fig, CH, f"governorate_{slug(name_en)}", f"خريطة محافظة {nm} ومدة الكلية ونسبة الاحتجاب فيها (محسوبة).", "map")


def region_map(title, sub, bounds, slug, caption):
    lon0, lon1, lat0, lat1 = bounds
    fig = plt.figure(figsize=(7.6, 7.6), facecolor=PAPER)
    ax = fig.add_axes([0.04, 0.07, 0.86, 0.77])
    MK.base(ax, lon0, lon1, lat0, lat1, labels=True)
    MK.field(ax, B, lon0, lon1, lat0, lat1, n=300)
    MK.path(ax, B, -1.7, 1.95)
    shown = []
    span = max(lon1 - lon0, lat1 - lat0)
    for n, la, lo in PTS:
        if lon0 < lo < lon1 and lat0 < la < lat1 and all(np.hypot(la - a, lo - b) > span * 0.06 for a, b in shown):
            shown.append((la, lo))
            MK.cities(ax, B, [(n, la, lo)], lon0, lon1, lat0, lat1, size=8.5)
    header(fig, title, sub)
    footer(fig, SRC)
    save(fig, CH, slug, caption, "map")


def bahariya_map():
    """Bahariya Oasis: inside the path, central line ~24 km south of Bawiti."""
    lon0, lon1, lat0, lat1 = 27.9, 29.8, 27.4, 28.9
    fig = plt.figure(figsize=(7.6, 7.2), facecolor=PAPER)
    ax = fig.add_axes([0.04, 0.09, 0.86, 0.73])
    MK.base(ax, lon0, lon1, lat0, lat1, labels=False)
    MK.field(ax, B, lon0, lon1, lat0, lat1, n=320)
    MK.path(ax, B, -1.7, 1.95)
    for n, g, la0, lo0, own in EGYPT_CITIES:
        if "Bahariya" not in n:
            continue
        rr = C.local_circumstances(B, np.array([la0]), np.array([lo0]))
        short = I.place(n).split(" (")[0]
        right = "Mandisha" in n
        ax.plot(lo0, la0, "o", ms=6, mfc=INK, mec="white", mew=1.2, zorder=9)
        ax.annotate(short + "\nكلي " + I.fmt_dur(rr["duration_s"][0]), (lo0, la0), xytext=(8 if right else -8, 4),
                    textcoords="offset points", ha="left" if right else "right", fontsize=9.5, path_effects=halo(),
                    zorder=10)
    # longest totality inside the oasis: on the central line south of Bawiti
    t = np.linspace(-0.6, 0.2, 40001)
    la, lo = C.central_line(B, t)
    j = int(np.nanargmin(np.abs(lo - 28.865)))
    r = C.local_circumstances(B, la[j:j + 1], lo[j:j + 1])
    ax.plot(lo[j], la[j], marker="*", ms=18, color=SUN_C, mec=INK, zorder=10)
    ax.annotate("أطول كلية في الواحة\n" + I.fmt_dur(r["duration_s"][0], long=True) + "\n" + I.fmt_lat(la[j], 2) + "  " +
                I.fmt_lon(lo[j], 2), (lo[j], la[j]), xytext=(12, -10), textcoords="offset points", ha="left", va="top",
                fontsize=9.5, fontweight="bold", path_effects=halo(), zorder=11)
    header(fig, "الواحات البحرية تحت الظل",
           "الواحة كلها داخل مسار الكلية؛ وخط المركز يعبرها جنوب الباويطي بنحو " + A(f"{(28.349 - la[j]) * 111:.0f}") + " كم")
    footer(fig, SRC + " النجمة: نقطة خط المركز داخل نطاق الواحة.")
    save(fig, CH, "bahariya_oasis", "الواحات البحرية: مدة الكلية في الباويطي والحيز ومنديشة، وأطول مدة على خط المركز (محسوبة).", "map")


def egypt_frames():
    lon0, lon1, lat0, lat1 = 24.5, 37.0, 21.7, 31.8
    for hh in [12.75, 12.85, 12.95, 13.05, 13.15, 13.25]:
        tt = hh - UTC
        fig = plt.figure(figsize=(7.6, 7.0), facecolor=PAPER)
        ax = fig.add_axes([0.04, 0.07, 0.86, 0.76])
        MK.base(ax, lon0, lon1, lat0, lat1, labels=False)
        LON, LAT = np.meshgrid(np.linspace(lon0, lon1, 300), np.linspace(lat0, lat1, 260))
        r = C.instant(B, tt - besselian.T0_UT_HOURS, LAT.ravel(), LON.ravel())
        ob = r["obscuration"].reshape(LON.shape)
        ax.contourf(LON, LAT, ob, levels=MK.OBS_LEVELS, cmap=MK.OBS_CMAP, norm=MK.OBS_NORM, alpha=0.6, zorder=2)
        cs = ax.contour(LON, LAT, ob, levels=[0.8, 0.9, 0.95, 0.99], colors=ORANGE[-1], linewidths=0.6, zorder=3)
        ax.clabel(cs, fmt=lambda v: I.pct(v * 100, 0), fontsize=7)
        um = r["umbra"].reshape(LON.shape).astype(float)
        if um.any():
            ax.contourf(LON, LAT, um, levels=[0.5, 1.5], colors=[NAVY], zorder=4)
        MK.path(ax, B, -1.7, 1.95)
        MK.cities(ax, B, [p for p in PTS if p[0] in ("القاهرة", "الإسكندرية", "الأقصر", "أسوان", "سوهاج", "أسيوط",
                                                       "الغردقة", "مرسى علم", "سيوة", "الخارجة", "شرم الشيخ")],
                  lon0, lon1, lat0, lat1, size=8, values=False)
        hhs = I.fmt_time(hh, seconds=False)
        header(fig, f"ظل القمر فوق مصر الساعة {hhs}", "البقعة الداكنة: الظل الكامل (كلية الآن)؛ البرتقالي: نسبة الاحتجاب في اللحظة نفسها")
        footer(fig, SRC + " التوقيت: توقيت مصر الصيفي.")
        save(fig, CH, f"egypt_shadow_{int(round(hh * 100)):04d}", f"موقع ظل القمر فوق مصر الساعة {hhs} بتوقيت مصر (محسوب).", "map")


def main():
    for g in GOVS:
        gov_map(g)
    region_map("ساحل البحر الأحمر", "من الغردقة إلى الشلاتين: منتجعات داخل مسار الكلية وخارجه", (32.6, 36.6, 22.6, 28.2),
               "red_sea_coast", "خريطة ساحل البحر الأحمر ومدة الكلية في مدنه (محسوبة).")
    bahariya_map()
    region_map("واحات الصحراء الغربية", "سيوة والبحرية والفرافرة والداخلة والخارجة", (24.6, 31.2, 24.2, 30.2),
               "western_oases", "خريطة الواحات المصرية وكسوف ٢٠٢٧ (محسوبة).")
    region_map("الدلتا والقاهرة الكبرى", "كسوف جزئي عميق في أكثر مناطق مصر سكانًا", (29.2, 32.8, 29.3, 31.7),
               "delta_cairo", "نسبة الاحتجاب في الدلتا والقاهرة الكبرى (محسوبة).")
    region_map("سيناء وخليج السويس", "كسوف جزئي بنسب تتجاوز ٩٠٪", (32.2, 35.0, 27.5, 31.4),
               "sinai", "نسبة الاحتجاب في سيناء ومدن القناة (محسوبة).")
    egypt_frames()
    write_catalogue("ch6")


if __name__ == "__main__":
    main()
