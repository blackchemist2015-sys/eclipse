"""Arabic eclipse maps for any eclipse (used by the book chapters)."""
import geopandas as gpd
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap

from common import (A, BLUE, INK, INK2, MUTED, ORANGE, RED, ROOT, halo, plt)
from eclipse2027 import circumstances as C, i18n as I

_geo = {}


def geo(name):
    if name not in _geo:
        _geo[name] = gpd.read_file(f"{ROOT}/data/{name}.geojson")
    return _geo[name]


SEA, LAND, LAND_OTHER = "#e8eef3", "#fbfaf7", "#f1efea"
OBS_LEVELS = np.array([1e-4, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99, 1.0])
OBS_CMAP = ListedColormap(ORANGE)
OBS_NORM = BoundaryNorm(OBS_LEVELS, OBS_CMAP.N)


def base(ax, lon0, lon1, lat0, lat1, highlight=("EGY",), admin1=("EGY",), labels=False):
    ax.set_facecolor(SEA)
    ax.set_xlim(lon0, lon1)
    ax.set_ylim(lat0, lat1)
    ax.set_aspect(1 / np.cos(np.radians(0.5 * (lat0 + lat1))))
    big = (lon1 - lon0) > 40
    countries = geo("countries_world" if big else "countries_region")
    view = countries.cx[lon0 - 2:lon1 + 2, lat0 - 2:lat1 + 2]
    view.plot(ax=ax, color=[LAND if (highlight and a in highlight) else LAND_OTHER for a in view.ADM0_A3],
              edgecolor="none", zorder=1)
    if admin1 and not big:
        a1 = geo("admin1_region")
        a1 = a1[a1.adm0_a3.isin(admin1)].cx[lon0:lon1, lat0:lat1]
        a1.boundary.plot(ax=ax, color=MUTED, lw=0.4, linestyle="--", zorder=5)
        if labels:
            for _, row in a1.iterrows():
                p = row.geometry.representative_point()
                if lon0 < p.x < lon1 and lat0 < p.y < lat1:
                    ax.text(p.x, p.y, I.admin_label(row.name_en, row.name_ar), fontsize=7, color=MUTED,
                            ha="center", va="center", zorder=6)
    view.boundary.plot(ax=ax, color=INK2, lw=0.7, zorder=5)
    ax.set_xlabel("")
    ax.set_ylabel("")
    dec = 1 if max(lon1 - lon0, lat1 - lat0) < 5 else 0
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: I.fmt_lon(v, dec)))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: I.fmt_lat(v, dec)))
    ax.yaxis.tick_right()
    ax.tick_params(labelsize=8)


def field(ax, B, lon0, lon1, lat0, lat1, n=260, obs_lines=True, fill=True, dur=True):
    aspect = (lon1 - lon0) * np.cos(np.radians(0.5 * (lat0 + lat1))) / (lat1 - lat0)
    nx, ny = (n, max(60, int(n / aspect))) if aspect >= 1 else (max(60, int(n * aspect)), n)
    LON, LAT = np.meshgrid(np.linspace(lon0, lon1, nx), np.linspace(lat0, lat1, ny))
    r = C.local_circumstances(B, LAT.ravel(), LON.ravel())
    r = {k: (v.reshape(LON.shape) if np.ndim(v) else v) for k, v in r.items()}
    inside = (r["umbral_margin"] > 0) & r["sun_up"]
    if fill:
        ax.contourf(LON, LAT, np.where(inside, np.nan, r["obscuration"]), levels=OBS_LEVELS, cmap=OBS_CMAP,
                    norm=OBS_NORM, alpha=0.55, zorder=2)
    if obs_lines:
        cs = ax.contour(LON, LAT, r["obscuration"], levels=[0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99],
                        colors=ORANGE[-1], linewidths=0.6, zorder=3)
        ax.clabel(cs, fmt=lambda v: I.pct(v * 100, 0), fontsize=7)
    if dur and np.any(r["duration_s"] > 0):
        d = np.where(r["duration_s"] > 0, r["duration_s"], np.nan)
        lv = np.arange(0, np.nanmax(d) + 31, 30)
        from matplotlib.colors import LinearSegmentedColormap
        cm = LinearSegmentedColormap.from_list("dur", [BLUE[1], BLUE[5], BLUE[9]])
        ax.contourf(LON, LAT, d, levels=lv, cmap=cm, alpha=0.75, zorder=3.5)
        cs = ax.contour(LON, LAT, d, levels=lv[1::2], colors=BLUE[11], linewidths=0.4, alpha=0.6, zorder=3.6)
        ax.clabel(cs, fmt=lambda v: I.fmt_dur(v), fontsize=6.5)
    elif np.any(inside):
        ax.contourf(LON, LAT, inside.astype(float), levels=[0.5, 1.5], colors=["#f2b8a0"], alpha=0.7, zorder=3.5)
    return LON, LAT, r


def path(ax, B, t0=-3.4, t1=3.4, color="#0d366b", central=RED):
    t = np.linspace(t0, t1, 1600)
    la, lo, ln, on, ls, os_ = C.path_limits(B, t)
    for x, y, c, lw, st in [(on, ln, color, 1.3, "-"), (os_, ls, color, 1.3, "-"), (lo, la, central, 1.1, (0, (6, 3)))]:
        x = np.array(x, float)
        x[np.where(np.abs(np.diff(x)) > 180)[0]] = np.nan
        ax.plot(x, y, color=c, lw=lw, ls=st, zorder=6)
    return la, lo


def cities(ax, B, pts, lon0, lon1, lat0, lat1, size=8, values=True, utc=None):
    for name, la, lo in pts:
        if not (lon0 < lo < lon1 and lat0 < la < lat1):
            continue
        r = C.local_circumstances(B, np.array([la]), np.array([lo]))
        ax.plot(lo, la, "o", ms=4.5, mfc=INK, mec="white", mew=1, zorder=8)
        txt = name
        if values:
            if r["duration_s"][0] > 0:
                txt += "\n" + "كلي " + I.fmt_dur(r["duration_s"][0])
            elif r["umbral_margin"][0] > 0:
                txt += "\nحلقي"
            elif r["obscuration"][0] > 0:
                txt += "\n" + I.pct(r["obscuration"][0] * 100) + " مُغطّى"
        ax.annotate(txt, (lo, la), xytext=(-5, 3), textcoords="offset points", ha="right", fontsize=size,
                    color=INK, zorder=9, path_effects=halo(), linespacing=1.05)


EGYPT_PTS = [("القاهرة", 30.0444, 31.2357), ("الإسكندرية", 31.2001, 29.9187), ("الأقصر", 25.6872, 32.6396),
             ("أسوان", 24.0889, 32.8998), ("سوهاج", 26.5591, 31.6957), ("أسيوط", 27.1783, 31.1859),
             ("السلوم", 31.55, 25.16), ("مرسى مطروح", 31.3543, 27.2373), ("الغردقة", 27.2579, 33.8116),
             ("شرم الشيخ", 27.9158, 34.33), ("سيوة", 29.2032, 25.5195), ("الخارجة", 25.439, 30.5586),
             ("بورسعيد", 31.2653, 32.3019), ("المنيا", 28.1099, 30.7503), ("أبو سمبل", 22.3372, 31.6258),
             ("العريش", 31.1316, 33.7984), ("مرسى علم", 25.0676, 34.879)]
