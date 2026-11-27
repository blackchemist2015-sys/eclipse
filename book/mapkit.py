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
# road-map style (in the manner of web road maps, from open Natural Earth data); STYLE = "plain" keeps the old look
STYLE = "plain"      # set to "road" once the samples are approved
RM_WATER, RM_LAND, RM_LAND_OTHER, RM_URBAN = "#aadaff", "#f4f1ea", "#ece8de", "#e3ded2"
RM_MAJOR, RM_MAJOR_EDGE, RM_ROAD, RM_ROAD_EDGE = "#fdd17a", "#e3a33a", "#ffffff", "#cfc3ad"


def road_layers(ax, lon0, lon1, lat0, lat1, towns=12):
    """Urban areas, lakes, rivers, roads and (optionally) town names; towns are soft labels that give way to others."""
    sl = (slice(lon0 - 2, lon1 + 2), slice(lat0 - 2, lat1 + 2))
    geo("urban_region").cx[sl[0], sl[1]].plot(ax=ax, color=RM_URBAN, edgecolor="none", zorder=1.5)
    geo("lakes10_region").cx[sl[0], sl[1]].plot(ax=ax, color=RM_WATER, edgecolor="none", zorder=1.6)
    geo("rivers_region").cx[sl[0], sl[1]].plot(ax=ax, color="#7fb8e8", linewidth=1.3, zorder=4.3)
    roads = geo("roads_region").cx[sl[0], sl[1]]
    span = max(lon1 - lon0, lat1 - lat0)
    kinds = (("Secondary Highway", "Road"), ("Major Highway",)) if span < 14 else ((), ("Major Highway",))
    for types, edge, fill, w in ((kinds[0], RM_ROAD_EDGE, RM_ROAD, 0.9), (kinds[1], RM_MAJOR_EDGE, RM_MAJOR, 1.5)):
        g = roads[roads["type"].isin(types)]
        if len(g):
            g.plot(ax=ax, color=edge, linewidth=w + 0.8, zorder=4.4, alpha=0.9)
            g.plot(ax=ax, color=fill, linewidth=w, zorder=4.45, alpha=0.95)
    if towns:
        pl = geo("places_region").cx[lon0:lon1, lat0:lat1].sort_values("POP_MAX", ascending=False).head(towns)
        for _, q in pl.iterrows():
            if isinstance(q["NAME_AR"], str):
                ax.plot(q.geometry.x, q.geometry.y, "o", ms=2.4, color="#6b6a65", zorder=4.6)
                ax.annotate(q["NAME_AR"], (q.geometry.x, q.geometry.y), xytext=(3, 2), textcoords="offset points",
                            fontsize=6.4, color="#5b5a55", zorder=4.7, gid="admin", path_effects=halo(2))
OBS_LEVELS = np.array([1e-4, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99, 1.0])
OBS_CMAP = ListedColormap(ORANGE)
OBS_NORM = BoundaryNorm(OBS_LEVELS, OBS_CMAP.N)


def base(ax, lon0, lon1, lat0, lat1, highlight=("EGY",), admin1=("EGY",), labels=False, towns=12):
    road = STYLE == "road"
    ax.set_facecolor(RM_WATER if road else SEA)
    ax.set_xlim(lon0, lon1)
    ax.set_ylim(lat0, lat1)
    ax.set_aspect(1 / np.cos(np.radians(0.5 * (lat0 + lat1))))
    big = (lon1 - lon0) > 40
    countries = geo("countries_world" if big else "countries_region")
    view = countries.cx[lon0 - 2:lon1 + 2, lat0 - 2:lat1 + 2]
    land, other = (RM_LAND, RM_LAND_OTHER) if road else (LAND, LAND_OTHER)
    view.plot(ax=ax, color=[land if (highlight and a in highlight) else other for a in view.ADM0_A3],
              edgecolor="none", zorder=1)
    if road and not big:
        road_layers(ax, lon0, lon1, lat0, lat1, towns=towns)
    if admin1 and not big:
        a1 = geo("admin1_region")
        a1 = a1[a1.adm0_a3.isin(admin1)].cx[lon0:lon1, lat0:lat1]
        a1.boundary.plot(ax=ax, color=MUTED, lw=0.4, linestyle="--", zorder=5)
        if labels:
            for _, row in a1.iterrows():
                p = row.geometry.representative_point()
                if lon0 < p.x < lon1 and lat0 < p.y < lat1:
                    t_ = ax.text(p.x, p.y, I.admin_label(row.name_en, row.name_ar), fontsize=7, color=MUTED,
                                 ha="center", va="center", zorder=6, gid="admin")
                    ax._admin_texts = getattr(ax, "_admin_texts", []) + [t_]
            declutter(ax)
    if road:
        view.boundary.plot(ax=ax, color="#9c8fb0", lw=1.0, linestyle=(0, (4, 2)), zorder=5)
    else:
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
    road = STYLE == "road"
    if fill and not road:              # road-map style: obscuration shown by labelled lines only
        ax.contourf(LON, LAT, np.where(inside, np.nan, r["obscuration"]), levels=OBS_LEVELS, cmap=OBS_CMAP,
                    norm=OBS_NORM, alpha=0.55, zorder=2)
    if obs_lines:
        cs = ax.contour(LON, LAT, r["obscuration"], levels=[0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99],
                        colors=ORANGE[-1], linewidths=0.6, zorder=3)
        tag_clabels(ax.clabel(cs, fmt=lambda v: I.pct(v * 100, 0), fontsize=7))
    if dur and np.any(r["duration_s"] > 0):
        d = np.where(r["duration_s"] > 0, r["duration_s"], np.nan)
        lv = np.arange(0, np.nanmax(d) + 31, 30)
        from matplotlib.colors import LinearSegmentedColormap
        cm = LinearSegmentedColormap.from_list("dur", [BLUE[1], BLUE[5], BLUE[9]])
        if road:                       # a light grey band, like printed path maps
            ax.contourf(LON, LAT, d, levels=[0, 1e5], colors=["#4a5a78"], alpha=0.17, zorder=3.5)
            cs = ax.contour(LON, LAT, d, levels=lv[1::2], colors="#1f1f1d", linewidths=0.5, alpha=0.8, zorder=4.5)
        else:
            ax.contourf(LON, LAT, d, levels=lv, cmap=cm, alpha=0.75, zorder=3.5)
            cs = ax.contour(LON, LAT, d, levels=lv[1::2], colors=BLUE[11], linewidths=0.4, alpha=0.6, zorder=3.6)
        tag_clabels(ax.clabel(cs, fmt=lambda v: I.fmt_dur(v), fontsize=6.5))
    elif np.any(inside):
        ax.contourf(LON, LAT, inside.astype(float), levels=[0.5, 1.5], colors=["#f2b8a0"], alpha=0.7, zorder=3.5)
    declutter(ax)
    return LON, LAT, r


def tag_clabels(texts):
    """Mark contour labels so declutter() lets every other text win over them."""
    for t in texts:
        t.set_gid("clabel")
        t.set_clip_on(True)
    return texts


def declutter(ax, limit=0.15, first=()):
    """Remove map texts that overlap one kept before them: `first` wins, then point labels, other texts, region names, contour labels."""
    ax.apply_aspect()
    r = ax.figure.canvas.get_renderer()
    kept = []
    rest = [t for t in ax.texts if t not in first]
    rank = {"label": 0, None: 1, "admin": 2, "clabel": 3}
    for t in list(first) + sorted(rest, key=lambda t: rank.get(t.get_gid(), 1)):
        if t.axes is None or not t.get_visible() or not t.get_text().strip():
            continue
        bb = t.get_window_extent(r)
        if any(_overlap(bb, o)[1] > limit for o in kept):
            t.remove()
            if t in getattr(ax, "_admin_texts", []):
                ax._admin_texts.remove(t)
        else:
            kept.append(bb)


def path(ax, B, t0=-3.4, t1=3.4, color="#0d366b", central=RED):
    t = np.linspace(t0, t1, 1600)
    la, lo, ln, on, ls, os_ = C.path_limits(B, t)
    for x, y, c, lw, st in [(on, ln, color, 1.3, "-"), (os_, ls, color, 1.3, "-"), (lo, la, central, 1.1, (0, (6, 3)))]:
        x = np.array(x, float)
        x[np.where(np.abs(np.diff(x)) > 180)[0]] = np.nan
        ax.plot(x, y, color=c, lw=lw, ls=st, zorder=6)
    return la, lo


OFFSETS = [(-5, 3, "right", "bottom"), (5, 3, "left", "bottom"), (-5, -4, "right", "top"), (5, -4, "left", "top"),
           (0, 7, "center", "bottom"), (0, -8, "center", "top"), (-6, 16, "right", "bottom"), (6, -16, "left", "top"),
           (6, 16, "left", "bottom"), (-6, -16, "right", "top")]


def _overlap(a, b):
    """Overlap area of two boxes, and that area as a fraction of the smaller box (a small label hidden under a big one counts)."""
    h = max(0, min(a.x1, b.x1) - max(a.x0, b.x0)) * max(0, min(a.y1, b.y1) - max(a.y0, b.y0))
    return h, h / max(min(a.width * a.height, b.width * b.height), 1)


def place_label(ax, txt, xy, size=8, color=INK, prefer=0, zorder=9, **kw):
    """Annotate xy with txt, trying several offsets so the label neither hits earlier labels nor leaves the axes.

    When every spot still overlaps an earlier label, a multi-line label falls back to its first line (the name),
    and if even that collides the point is left unlabelled rather than printing text over text."""
    fig = ax.figure
    ax.apply_aspect()          # the box an equal-aspect map gets at draw time; measure against that
    r = fig.canvas.get_renderer()
    placed = getattr(ax, "_placed_labels", [])
    # every text already on the map is an obstacle; region names are soft (avoided if possible, else declutter()
    # drops them) and contour labels are ignored (declutter() removes those under a label)
    live = [t for t in ax.texts if t.get_visible() and t.get_text().strip()]
    hard = placed + [t.get_window_extent(r) for t in live if t.get_gid() not in ("clabel", "admin", "label")]
    soft = [t.get_window_extent(r) for t in live if t.get_gid() == "admin"]
    axbb = ax.get_window_extent(r)
    order = OFFSETS[prefer:] + OFFSETS[:prefer]

    def attempt(text):
        best, best_score, best_frac = None, None, 1.0
        for dx, dy, ha, va in order:
            a = ax.annotate(text, xy, xytext=(dx, dy), textcoords="offset points", ha=ha, va=va, fontsize=size,
                            color=color, zorder=zorder, path_effects=halo(), linespacing=1.05, gid="label", **kw)
            bb = a.get_window_extent(r)
            hits = [_overlap(bb, o) for o in hard]
            out = max(0, axbb.x0 - bb.x0) + max(0, bb.x1 - axbb.x1) + max(0, axbb.y0 - bb.y0) + max(0, bb.y1 - axbb.y1)
            score = sum(h for h, _ in hits) + 0.3 * sum(_overlap(bb, o)[0] for o in soft) + out * 50
            if best_score is None or score < best_score:
                if best is not None:
                    best.remove()
                best, best_score, best_frac = a, score, max([f for _, f in hits], default=0.0)
            else:
                a.remove()
            if score == 0:
                break
        return best, best_frac

    best, frac = attempt(txt)
    if frac > 0.12 and "\n" in txt:
        best.remove()
        best, frac = attempt(txt.split("\n")[0])
    if frac > 0.12:
        best.remove()
        return None
    placed.append(best.get_window_extent(r))
    ax._placed_labels = placed
    return best


def label_along(ax, xs, ys, txt, fracs=(0.33, 0.5, 0.67, 0.2, 0.8, 0.42, 0.58), dy=0.0, **kw):
    """Put txt on a line at the first of several positions along it (fractions of its visible part) that clears
    every text already on the axes; falls back to the first position."""
    ax.apply_aspect()
    r = ax.figure.canvas.get_renderer()
    others = [t.get_window_extent(r) for t in ax.texts
              if t.get_visible() and t.get_text().strip() and t.get_gid() != "clabel"]
    idx = np.where(np.isfinite(xs) & np.isfinite(ys))[0]
    if not len(idx):
        return None
    first = None
    for f in fracs:
        j = idx[min(len(idx) - 1, int(f * len(idx)))]
        t = ax.text(xs[j], ys[j] + dy, txt, **kw)
        bb = t.get_window_extent(r)
        if not any(_overlap(bb, o)[1] > 0.05 for o in others):
            if first is not None:
                first.remove()
            return t
        if first is None:
            first = t
        else:
            t.remove()
    return first


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
        place_label(ax, txt, (lo, la), size=size)
    declutter(ax)


EGYPT_PTS = [("القاهرة", 30.0444, 31.2357), ("الإسكندرية", 31.2001, 29.9187), ("الأقصر", 25.6872, 32.6396),
             ("أسوان", 24.0889, 32.8998), ("سوهاج", 26.5591, 31.6957), ("أسيوط", 27.1783, 31.1859),
             ("السلوم", 31.55, 25.16), ("مرسى مطروح", 31.3543, 27.2373), ("الغردقة", 27.2579, 33.8116),
             ("شرم الشيخ", 27.9158, 34.33), ("سيوة", 29.2032, 25.5195), ("الخارجة", 25.439, 30.5586),
             ("بورسعيد", 31.2653, 32.3019), ("المنيا", 28.1099, 30.7503), ("أبو سمبل", 22.3372, 31.6258),
             ("العريش", 31.1316, 33.7984), ("مرسى علم", 25.0676, 34.879)]
