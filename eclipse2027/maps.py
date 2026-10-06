"""Generate every map and table for the 2 August 2027 total solar eclipse.

Run:  python -m eclipse2027.maps
Outputs PNG maps to maps/ and CSV/TXT tables to results/.
"""
import csv
import os
import re
import unicodedata

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import BoundaryNorm, ListedColormap  # noqa: E402
from matplotlib.patches import Circle  # noqa: E402
from shapely.geometry import Polygon  # noqa: E402

from . import besselian, circumstances as circ  # noqa: E402
from .places import CITIES, COUNTRIES, EGYPT_CITIES  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA = os.path.join(ROOT, "data")
MAPS = os.path.join(ROOT, "maps")
RESULTS = os.path.join(ROOT, "results")

# --- palette: blue sequential for totality duration, orange sequential for obscuration
BLUE = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
        "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
ORANGE = ["#fdf1e4", "#fbe1c4", "#f8cf9f", "#f4ba78", "#efa351", "#e88a2c", "#d4711a", "#b55a12"]
INK, INK2, MUTED = "#1f1f1d", "#4a4a46", "#8a8984"
SEA, LAND, LAND_OTHER = "#e8eef3", "#fbfaf7", "#f1efea"
LIMIT = "#0d366b"
CENTRAL = "#b3261e"
SOURCE = ("Computed from JPL DE421 ephemeris (Skyfield) via Besselian elements; "
          "borders: Natural Earth. Sea-level observer, smooth lunar limb.")

B = besselian.compute()

DUR_LEVELS = np.arange(0, 6.5 * 60 + 1, 30)  # seconds
DUR_CMAP = ListedColormap(BLUE[: len(DUR_LEVELS) - 1])
DUR_NORM = BoundaryNorm(DUR_LEVELS, DUR_CMAP.N)
OBS_LEVELS = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99, 1.0])
OBS_CMAP = ListedColormap(ORANGE)
OBS_NORM = BoundaryNorm(OBS_LEVELS, OBS_CMAP.N)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": MUTED,
    "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.titleweight": "bold", "axes.titlesize": 12, "figure.dpi": 100,
})


def hm(v, suffix=""):
    m = int(round(v * 60)) % 1440
    return f"{m // 60:02d}:{m % 60:02d}{suffix}"


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


# ----------------------------------------------------------------- geodata
_geo = {}


def geo(name):
    if name not in _geo:
        _geo[name] = gpd.read_file(os.path.join(DATA, name + ".geojson"))
    return _geo[name]


# ----------------------------------------------------------------- path of totality
def _path():
    t = np.linspace(-1.75, 2.0, 2400)
    lat_c, lon_c, lat_n, lon_n, lat_s, lon_s = circ.path_limits(B, t)
    t_ok = t[np.isfinite(circ.central_line(B, t)[0])]
    return dict(t=t_ok + besselian.T0_UT_HOURS, lat_c=lat_c, lon_c=lon_c,
                lat_n=lat_n, lon_n=lon_n, lat_s=lat_s, lon_s=lon_s)


PATH = _path()
PATH_POLY = Polygon(list(zip(PATH["lon_n"], PATH["lat_n"])) +
                    list(zip(PATH["lon_s"][::-1], PATH["lat_s"][::-1])))


def grid(lon0, lon1, lat0, lat1, n=320):
    aspect = (lon1 - lon0) * np.cos(np.radians(0.5 * (lat0 + lat1))) / (lat1 - lat0)
    nx, ny = (n, int(n / aspect)) if aspect >= 1 else (int(n * aspect), n)
    nx, ny = max(nx, 60), max(ny, 60)
    lon = np.linspace(lon0, lon1, nx)
    lat = np.linspace(lat0, lat1, ny)
    LON, LAT = np.meshgrid(lon, lat)
    r = circ.local_circumstances(B, LAT.ravel(), LON.ravel())
    return LON, LAT, {k: (v.reshape(LON.shape) if np.ndim(v) else v) for k, v in r.items()}


def city_circumstances(lat, lon, utc):
    r = circ.local_circumstances(B, np.array([lat]), np.array([lon]))
    r = {k: float(np.ravel(v)[0]) for k, v in r.items()}
    alt, az = sun_altaz(lat, lon, r["tmax"])
    r.update(sun_alt=alt, sun_az=az, utc=utc)
    return r


def sun_altaz(lat, lon, ut_hours):
    from skyfield.api import wgs84
    ts, eph = besselian.ephemeris()
    t = ts.ut1(2027, 8, 2, 0, 0, ut_hours * 3600.0)
    obs = (eph["earth"] + wgs84.latlon(lat, lon)).at(t)
    alt, az, _ = obs.observe(eph["sun"]).apparent().altaz()
    return alt.degrees, az.degrees


# ----------------------------------------------------------------- drawing helpers
def setup_axes(ax, lon0, lon1, lat0, lat1, highlight=None, admin1_for=None, admin1_labels=False):
    ax.set_facecolor(SEA)
    ax.set_xlim(lon0, lon1)
    ax.set_ylim(lat0, lat1)
    ax.set_aspect(1 / np.cos(np.radians(0.5 * (lat0 + lat1))))
    countries = geo("countries_region")
    view = countries.cx[lon0 - 1:lon1 + 1, lat0 - 1:lat1 + 1]
    for _, row in view.iterrows():
        hl = highlight is None or row.ADM0_A3 in highlight
        gpd.GeoSeries([row.geometry]).plot(ax=ax, color=LAND if hl else LAND_OTHER,
                                            edgecolor="none", zorder=1)
    lakes = geo("lakes_region").cx[lon0:lon1, lat0:lat1]
    if len(lakes):
        lakes.plot(ax=ax, color=SEA, edgecolor="none", zorder=1.1)
    if admin1_for:
        a1 = geo("admin1_region")
        a1 = a1[a1.adm0_a3.isin(admin1_for)].cx[lon0:lon1, lat0:lat1]
        a1.boundary.plot(ax=ax, color=MUTED, linewidth=0.45, zorder=5, linestyle=(0, (3, 2)))
        if admin1_labels:
            for _, row in a1.iterrows():
                p = row.geometry.representative_point()
                if lon0 < p.x < lon1 and lat0 < p.y < lat1:
                    ax.text(p.x, p.y, row.name_en or row["name"], fontsize=6.5, color=MUTED,
                            ha="center", va="center", style="italic", zorder=6)
    view.boundary.plot(ax=ax, color=INK2, linewidth=0.8, zorder=5)
    ax.tick_params(labelsize=7.5)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{abs(v):.1f}°{'E' if v >= 0 else 'W'}"))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{abs(v):.1f}°{'N' if v >= 0 else 'S'}"))
    for s in ax.spines.values():
        s.set_color(MUTED)


def draw_field(ax, LON, LAT, r, dur_lines=True, obs_lines=True, obs_fill=True, label_size=7):
    if obs_fill:
        ax.contourf(LON, LAT, np.where(r["duration_s"] > 0, np.nan, r["obscuration"]), levels=OBS_LEVELS, cmap=OBS_CMAP, norm=OBS_NORM,
                    alpha=0.55, zorder=2, extend="neither")
    if obs_lines:
        lv = [0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.97, 0.99]
        cs = ax.contour(LON, LAT, r["obscuration"], levels=lv, colors=ORANGE[-1], linewidths=0.6, zorder=3)
        ax.clabel(cs, fmt=lambda v: f"{v * 100:.0f}%", fontsize=label_size - 0.5, inline=True)
    d = np.where(r["duration_s"] > 0, r["duration_s"], np.nan)
    if np.isfinite(d).any():
        ax.contourf(LON, LAT, d, levels=DUR_LEVELS, cmap=DUR_CMAP, norm=DUR_NORM, alpha=0.6, zorder=3.5)
        if dur_lines:
            lv = [v for v in DUR_LEVELS[1:] if v < np.nanmax(d)]
            if lv:
                cs = ax.contour(LON, LAT, d, levels=lv, colors=LIMIT, linewidths=0.45, zorder=4, alpha=0.8)
                ax.clabel(cs, fmt=lambda v: f"{int(v // 60)}m{int(v % 60):02d}s", fontsize=label_size - 0.5)


def land_veil(ax):
    """Light veil over land drawn above the colour fields so coasts stay readable."""
    lon0, lon1 = ax.get_xlim()
    lat0, lat1 = ax.get_ylim()
    view = geo("countries_region").cx[lon0 - 1:lon1 + 1, lat0 - 1:lat1 + 1]
    view.plot(ax=ax, color="white", alpha=0.28, edgecolor="none", zorder=4.5)
    ax.set_xlabel("")
    ax.set_ylabel("")


def draw_path(ax, label=True):
    land_veil(ax)
    ax.plot(PATH["lon_n"], PATH["lat_n"], color=LIMIT, lw=1.4, zorder=6)
    ax.plot(PATH["lon_s"], PATH["lat_s"], color=LIMIT, lw=1.4, zorder=6)
    ax.plot(PATH["lon_c"], PATH["lat_c"], color=CENTRAL, lw=1.2, ls=(0, (6, 3)), zorder=6,
            label="Central line" if label else None)


def draw_cities(ax, cities, lon0, lon1, lat0, lat1, utc, fontsize=7.5, show_values=True, highlight=None):
    from matplotlib import patheffects as pe
    halo = [pe.withStroke(linewidth=2.6, foreground="white")]
    hl = [(la, lo) for n, la, lo in cities if n == highlight]
    for name, la, lo in cities:
        if not (lon0 < lo < lon1 and lat0 < la < lat1):
            continue
        if hl and name != highlight and np.hypot(la - hl[0][0], lo - hl[0][1]) < 0.12:
            continue
        c = city_circumstances(la, lo, utc)
        big = highlight is not None and name == highlight
        ax.plot(lo, la, "o", ms=8 if big else 4.5, mfc=CENTRAL if big else INK, mec="white", mew=1.0, zorder=8)
        if show_values:
            if c["duration_s"] > 0:
                val = f"total {circ.fmt_dur(c['duration_s'])}"
            else:
                val = f"{c['obscuration'] * 100:.1f}% covered"
            txt = f"{name}\n{val}"
        else:
            txt = name
        ax.annotate(txt, (lo, la), xytext=(5, 3), textcoords="offset points", fontsize=fontsize + (1.5 if big else 0),
                    color=INK, zorder=9, path_effects=halo, fontweight="bold" if big else "normal",
                    linespacing=1.05)


def add_colorbars(fig, ax, show_obs=True, show_dur=True):
    from matplotlib.patches import Rectangle
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes
    if show_dur:
        ax.add_patch(Rectangle((0.0, 0.0), 0.44, 0.085, transform=ax.transAxes, facecolor="white",
                               edgecolor="none", alpha=0.85, zorder=9.5))
    if show_obs:
        ax.add_patch(Rectangle((0.56, 0.0), 0.44, 0.085, transform=ax.transAxes, facecolor="white",
                               edgecolor="none", alpha=0.85, zorder=9.5))
    if show_dur:
        cax = inset_axes(ax, width="38%", height="2.2%", loc="lower left", borderpad=1.6)
        sm = plt.cm.ScalarMappable(cmap=DUR_CMAP, norm=DUR_NORM)
        cb = fig.colorbar(sm, cax=cax, orientation="horizontal", ticks=DUR_LEVELS[::2])
        cb.ax.set_xticklabels([f"{int(v // 60)}:{int(v % 60):02d}" for v in DUR_LEVELS[::2]], fontsize=6.5)
        cb.ax.set_title("Duration of totality (min:s)", fontsize=7, color=INK2, pad=2)
        cax.patch.set_alpha(0.9)
    if show_obs:
        cax2 = inset_axes(ax, width="38%", height="2.2%", loc="lower right", borderpad=1.6)
        sm = plt.cm.ScalarMappable(cmap=OBS_CMAP, norm=OBS_NORM)
        cb = fig.colorbar(sm, cax=cax2, orientation="horizontal", ticks=OBS_LEVELS)
        cb.ax.set_xticklabels([f"{v * 100:.0f}" for v in OBS_LEVELS], fontsize=6.5)
        cb.ax.set_title("Sun's disk covered at maximum (%)", fontsize=7, color=INK2, pad=2)


def footer(fig, extra=""):
    fig.text(0.01, 0.006, SOURCE + (" " + extra if extra else ""), fontsize=6.5, color=MUTED, ha="left", va="bottom")


def save(fig, name):
    os.makedirs(MAPS, exist_ok=True)
    path = os.path.join(MAPS, name + ".png")
    fig.savefig(path, dpi=150, facecolor="white")
    plt.close(fig)
    print("wrote", os.path.relpath(path, ROOT))
    return path


# ----------------------------------------------------------------- world overview maps
def world_overview(idx):
    import cartopy.crs as ccrs
    proj = ccrs.Orthographic(central_longitude=20, central_latitude=20)
    fig = plt.figure(figsize=(11, 11))
    ax = fig.add_axes([0.03, 0.06, 0.94, 0.86], projection=proj)
    ax.set_global()
    ax.set_facecolor(SEA)
    world = geo("countries_world")
    ax.add_geometries(world.geometry, crs=ccrs.PlateCarree(), facecolor=LAND, edgecolor=INK2, linewidth=0.35, zorder=1)
    lon = np.linspace(-180, 180, 721)
    lat = np.linspace(-89.5, 89.5, 359)
    LON, LAT = np.meshgrid(lon, lat)
    r = circ.local_circumstances(B, LAT.ravel(), LON.ravel())
    obs = r["obscuration"].reshape(LON.shape)
    tmax = np.where(obs > 0, r["tmax"].reshape(LON.shape), np.nan)
    ax.contourf(LON, LAT, obs, levels=np.r_[1e-4, OBS_LEVELS[1:]], cmap=OBS_CMAP, norm=OBS_NORM, alpha=0.6,
                transform=ccrs.PlateCarree(), zorder=2)
    cs = ax.contour(LON, LAT, obs, levels=[0.0001, 0.2, 0.4, 0.6, 0.8, 0.9], colors=ORANGE[-1], linewidths=0.7,
                    transform=ccrs.PlateCarree(), zorder=3)
    ax.clabel(cs, fmt=lambda v: f"{v * 100:.0f}%", fontsize=7)
    ct = ax.contour(LON, LAT, tmax, levels=np.arange(7.0, 13.01, 0.5), colors=INK2, linewidths=0.5,
                    linestyles="dashed", transform=ccrs.PlateCarree(), zorder=3)
    ax.clabel(ct, fmt=lambda v: hm(v, " UT"), fontsize=6.5)
    ax.fill(np.r_[PATH["lon_n"], PATH["lon_s"][::-1]], np.r_[PATH["lat_n"], PATH["lat_s"][::-1]],
            color=BLUE[-2], alpha=0.85, transform=ccrs.PlateCarree(), zorder=4)
    ax.plot(PATH["lon_c"], PATH["lat_c"], color=CENTRAL, lw=1.0, transform=ccrs.PlateCarree(), zorder=5)
    # greatest duration point
    gd = greatest_duration()
    ax.plot(gd["lon"], gd["lat"], marker="*", ms=14, mfc=CENTRAL, mec="white", transform=ccrs.PlateCarree(), zorder=6)
    ax.gridlines(color=MUTED, linewidth=0.3, alpha=0.6)
    fig.suptitle("Total Solar Eclipse — 2 August 2027", fontsize=17, fontweight="bold", color=INK, y=0.975)
    fig.text(0.5, 0.935, "Path of totality (blue), obscuration of the Sun (orange %) and time of maximum eclipse (dashed, UT)."
             f"  ★ greatest duration {circ.fmt_dur(gd['dur'])} at {gd['lat']:.2f}°N {gd['lon']:.2f}°E",
             ha="center", fontsize=9.5, color=INK2)
    footer(fig)
    return save(fig, f"{idx:02d}_world_overview_orthographic")


_GD = None


def greatest_duration():
    global _GD
    if _GD is None:
        t = np.linspace(-1.0, 1.0, 4001)
        la, lo = circ.central_line(B, t)
        r = circ.local_circumstances(B, la, lo)
        i = int(np.nanargmax(r["duration_s"]))
        _GD = dict(lat=la[i], lon=lo[i], dur=r["duration_s"][i], t=r["tmax"][i], alt=r["sun_alt_deg"][i])
    return _GD


def regional_overview(idx):
    lon0, lon1, lat0, lat1 = -20, 62, -2, 50
    fig, ax = plt.subplots(figsize=(15, 9.6))
    setup_axes(ax, lon0, lon1, lat0, lat1)
    LON, LAT, r = grid(lon0, lon1, lat0, lat1, n=420)
    draw_field(ax, LON, LAT, r, dur_lines=False)
    tmax = np.where(r["obscuration"] > 0, r["tmax"], np.nan)
    ct = ax.contour(LON, LAT, tmax, levels=np.arange(8.0, 12.01, 0.25), colors=INK2, linewidths=0.45,
                    linestyles="dashed", zorder=4)
    ax.clabel(ct, fmt=lambda v: hm(v, " UT"), fontsize=6.5)
    draw_path(ax)
    # time ticks on the central line every 10 minutes
    for tt in np.arange(8.5, 11.85, 1 / 6):
        la, lo = circ.central_line(B, tt - besselian.T0_UT_HOURS)
        if np.isfinite(la) and lon0 < lo < lon1 and lat0 < la < lat1:
            ax.plot(lo, la, "o", ms=3.5, color=CENTRAL, zorder=7)
            ax.annotate(hm(tt), (lo, la), xytext=(3, -9),
                        textcoords="offset points", fontsize=6.5, color=CENTRAL, zorder=7)
    big = [("Seville", 37.3891, -5.9845), ("Tangier", 35.7595, -5.8340), ("Algiers", 36.7538, 3.0588),
           ("Tunis", 36.8065, 10.1815), ("Tripoli", 32.8872, 13.1913), ("Benghazi", 32.1167, 20.0667),
           ("Cairo", 30.0444, 31.2357), ("Luxor", 25.6872, 32.6396), ("Jeddah", 21.4858, 39.1925),
           ("Mecca", 21.3891, 39.8579), ("Sana'a", 15.3694, 44.1910), ("Aden", 12.7855, 45.0187),
           ("Bosaso", 11.2842, 49.1816), ("Madrid", 40.4168, -3.7038), ("Rome", 41.9028, 12.4964),
           ("Athens", 37.9838, 23.7275), ("Istanbul", 41.0082, 28.9784), ("Riyadh", 24.7136, 46.6753),
           ("Khartoum", 15.5007, 32.5599), ("Addis Ababa", 9.0300, 38.7400), ("Lisbon", 38.7223, -9.1393),
           ("Paris", 48.8566, 2.3522), ("Tehran", 35.6892, 51.3890), ("Dubai", 25.2048, 55.2708)]
    draw_cities(ax, big, lon0, lon1, lat0, lat1, 0, fontsize=7)
    gd = greatest_duration()
    ax.plot(gd["lon"], gd["lat"], marker="*", ms=15, mfc=CENTRAL, mec="white", zorder=8)
    ax.set_title("Total solar eclipse of 2 August 2027 — Europe, North Africa & Middle East", loc="left")
    add_colorbars(fig, ax)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    footer(fig, "Red dots: central-line time of totality (UT).")
    return save(fig, f"{idx:02d}_regional_overview_totality_and_obscuration")


def central_line_profile(idx):
    t = np.linspace(-1.70, 1.95, 1200)
    la, lo = circ.central_line(B, t)
    ok = np.isfinite(la)
    t, la, lo = t[ok], la[ok], lo[ok]
    r = circ.local_circumstances(B, la, lo)
    w = path_width(t)
    fig, axs = plt.subplots(3, 1, figsize=(12, 9.5), sharex=True)
    x = lo
    axs[0].plot(x, r["duration_s"] / 60, color=BLUE[-3], lw=2)
    axs[0].set_ylabel("Totality on central line (min)")
    axs[1].plot(x, w, color=BLUE[-3], lw=2)
    axs[1].set_ylabel("Path width (km)")
    axs[2].plot(x, r["sun_alt_deg"], color=ORANGE[-2], lw=2)
    axs[2].set_ylabel("Sun altitude (°)")
    axs[2].set_xlabel("Longitude of central line (°E)")
    marks = [("Atlantic", -30), ("Strait of\nGibraltar", -5.6), ("Algeria", 3.5), ("Tunisia", 9.3),
             ("Libya", 18), ("Egypt", 31), ("Saudi\nArabia", 41), ("Yemen", 48.5), ("Somalia/\nIndian Ocean", 56)]
    for ax in axs:
        ax.grid(color="#e4e2dc", lw=0.6)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for _, mx in marks:
            ax.axvline(mx, color="#e4e2dc", lw=0.8, zorder=0)
    for name, mx in marks:
        axs[0].text(mx, 6.55, name, ha="center", va="bottom", fontsize=7.5, color=INK2)
    axs[0].set_ylim(0, 7.2)
    gd = greatest_duration()
    axs[0].plot(gd["lon"], gd["dur"] / 60, "*", ms=13, color=CENTRAL)
    axs[0].annotate(f"Greatest duration {circ.fmt_dur(gd['dur'])}\n{gd['lat']:.2f}°N {gd['lon']:.2f}°E (Egypt)",
                    (gd["lon"], gd["dur"] / 60), xytext=(12, -32), textcoords="offset points", fontsize=8, color=INK)
    fig.suptitle("Along the central line: duration, path width and Sun altitude", fontsize=13, fontweight="bold", x=0.02, ha="left")
    fig.tight_layout(rect=(0, 0.02, 1, 0.97))
    footer(fig)
    with open(os.path.join(RESULTS, "central_line.csv"), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["time_UT", "latitude_deg", "longitude_deg", "totality_duration_s", "path_width_km", "sun_altitude_deg"])
        for i in range(0, len(t), 5):
            wr.writerow([circ.fmt_hms(t[i] + besselian.T0_UT_HOURS), f"{la[i]:.4f}", f"{lo[i]:.4f}",
                         f"{r['duration_s'][i]:.1f}", f"{w[i]:.1f}", f"{r['sun_alt_deg'][i]:.1f}"])
    return save(fig, f"{idx:02d}_central_line_duration_width_profile")


def path_width(t):
    _, _, ln, on, ls, os_ = circ.path_limits(B, t)
    la = np.radians(0.5 * (ln + ls))
    return 6371 * np.radians(1) * np.hypot(ln - ls, (on - os_) * np.cos(la))


# ----------------------------------------------------------------- country maps
def country_map(idx, key):
    name, codes, utc, tzl, lon0, lon1, lat0, lat1 = COUNTRIES[key]
    span = max(lon1 - lon0, lat1 - lat0)
    w = 13 if (lon1 - lon0) * np.cos(np.radians((lat0 + lat1) / 2)) >= (lat1 - lat0) else 10
    fig, ax = plt.subplots(figsize=(w, 10))
    setup_axes(ax, lon0, lon1, lat0, lat1, highlight=codes, admin1_for=codes, admin1_labels=span < 8)
    LON, LAT, r = grid(lon0, lon1, lat0, lat1, n=360)
    draw_field(ax, LON, LAT, r)
    draw_path(ax)
    cities = CITIES[key]
    if key == "egypt":
        skip = {"Giza", "Esna", "Kom Ombo", "Edfu", "Qena"}
        cities = [(n, la, lo) for n, _g, la, lo, own in EGYPT_CITIES if own and n not in skip] + \
                 [(n, la, lo) for n, _g, la, lo, own in EGYPT_CITIES if n in ("Siwa", "Port Said", "Berenice", "Farafra")]
    draw_cities(ax, cities, lon0, lon1, lat0, lat1, utc, fontsize=7 if span > 6 else 8)
    ax.set_title(f"{name} — total solar eclipse, 2 August 2027\n", loc="left")
    ax.text(0.0, 1.008, f"Totality duration (blue) and % of the Sun covered (orange) at each city · local time {tzl} = UT{utc:+d}",
            transform=ax.transAxes, fontsize=8.5, color=INK2, va="bottom")
    add_colorbars(fig, ax)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    footer(fig, "Blue lines: limits of totality; red dashed: central line.")
    return save(fig, f"{idx:02d}_country_{key}")


# ----------------------------------------------------------------- Egypt maps
def egypt_governorates(idx):
    name, codes, utc, tzl, lon0, lon1, lat0, lat1 = COUNTRIES["egypt"]
    fig, ax = plt.subplots(figsize=(12.5, 11.5))
    setup_axes(ax, lon0, lon1, lat0, lat1, highlight=codes, admin1_for=codes, admin1_labels=True)
    LON, LAT, r = grid(lon0, lon1, lat0, lat1, n=520)
    draw_field(ax, LON, LAT, r, obs_fill=False)
    draw_path(ax)
    draw_cities(ax, CITIES["egypt"], lon0, lon1, lat0, lat1, utc, fontsize=6.4, show_values=False)
    ax.set_title("Egypt by governorate — where totality lasts longest (2 August 2027)", loc="left")
    add_colorbars(fig, ax, show_obs=False)
    # governorate summary table: max totality inside each governorate
    a1 = geo("admin1_region")
    a1 = a1[a1.adm0_a3 == "EGY"]
    rows = []
    pts = gpd.GeoDataFrame(geometry=gpd.points_from_xy(LON.ravel(), LAT.ravel()), crs=a1.crs)
    joined = gpd.sjoin(pts, a1[["name_en", "geometry"]], predicate="within")
    dur = r["duration_s"].ravel()
    obs = r["obscuration"].ravel()
    for gname, grp in joined.groupby("name_en"):
        d = dur[grp.index.values]
        o = obs[grp.index.values]
        rows.append((gname, d.max(), (d > 0).mean() * 100, o.min() * 100, o.max() * 100))
    rows.sort(key=lambda x: -x[1] - x[4] / 1e3)
    with open(os.path.join(RESULTS, "egypt_governorates.csv"), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["governorate", "max_totality_s", "max_totality", "area_in_totality_pct",
                     "min_obscuration_pct", "max_obscuration_pct"])
        for g, d, a, omin, omax in rows:
            wr.writerow([g, f"{d:.0f}", circ.fmt_dur(d), f"{a:.0f}", f"{omin:.1f}", f"{omax:.1f}"])
    txt = "Governorate      max totality  area in path\n" + "\n".join(
        f"{g[:16]:<16} {circ.fmt_dur(d):>9}   {a:5.0f}%" for g, d, a, _o, _p in rows if d > 0)
    ax.text(0.99, 0.99, txt, transform=ax.transAxes, ha="right", va="top", fontsize=6.6, family="DejaVu Sans Mono",
            color=INK, bbox=dict(facecolor="white", edgecolor=MUTED, alpha=0.92, boxstyle="round,pad=0.5"), zorder=10)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    footer(fig)
    return save(fig, f"{idx:02d}_egypt_governorates_totality")


def egypt_contact_times(idx):
    name, codes, utc, tzl, lon0, lon1, lat0, lat1 = COUNTRIES["egypt"]
    fig, axs = plt.subplots(1, 2, figsize=(17, 8.8))
    LON, LAT, r = grid(lon0, lon1, lat0, lat1, n=360)
    for ax, key, title in [(axs[0], "c1", "Partial eclipse begins (first contact)"),
                           (axs[1], "tmax", "Maximum eclipse")]:
        setup_axes(ax, lon0, lon1, lat0, lat1, highlight=codes, admin1_for=codes)
        draw_field(ax, LON, LAT, r, dur_lines=False, obs_lines=False, obs_fill=True)
        tt = r[key] + utc
        lv = np.arange(np.floor(np.nanmin(tt) * 12) / 12, np.nanmax(tt) + 0.01, 1 / 12)
        cs = ax.contour(LON, LAT, tt, levels=lv, colors=INK, linewidths=0.7, zorder=6)
        ax.clabel(cs, fmt=hm, fontsize=7)
        draw_path(ax)
        draw_cities(ax, [c for c in CITIES["egypt"] if c[0] in {"Cairo", "Alexandria", "Luxor", "Aswan", "Hurghada",
                     "Asyut", "Sohag", "Kharga", "Marsa Alam", "Sharm El Sheikh", "Siwa", "Abu Simbel", "Port Said"}],
                    lon0, lon1, lat0, lat1, utc, fontsize=6.6, show_values=False)
        ax.set_title(f"{title} — {tzl} (UT+3)", loc="left", fontsize=11)
    fig.suptitle("Egypt — eclipse timing, 2 August 2027 (contours every 5 minutes, local time)", fontsize=13,
                 fontweight="bold", x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0.02, 1, 0.96))
    footer(fig)
    return save(fig, f"{idx:02d}_egypt_contact_times")


# ----------------------------------------------------------------- per-city detail
def disk_sequence(lat, lon, c):
    """Topocentric Sun/Moon offsets (arcmin, horizon frame) at several instants."""
    from skyfield.api import wgs84
    ts, eph = besselian.ephemeris()
    t1, tm, t4 = c["c1"], c["tmax"], c["c4"]
    times = [t1, t1 + (tm - t1) / 3, t1 + 2 * (tm - t1) / 3, tm, tm + (t4 - tm) / 3, tm + 2 * (t4 - tm) / 3, t4]
    out = []
    for th in times:
        t = ts.ut1(2027, 8, 2, 0, 0, th * 3600.0)
        obs = (eph["earth"] + wgs84.latlon(lat, lon)).at(t)
        s = obs.observe(eph["sun"]).apparent()
        m = obs.observe(eph["moon"]).apparent()
        sa, sz, sd = s.altaz()
        ma, mz, md = m.altaz()
        dx = ((mz.degrees - sz.degrees + 180) % 360 - 180) * np.cos(np.radians(sa.degrees)) * 60
        dy = (ma.degrees - sa.degrees) * 60
        rs = np.degrees(np.arcsin(696000 / sd.km)) * 60
        rm = np.degrees(np.arcsin(1737.4 / md.km)) * 60
        out.append((th, dx, dy, rs, rm))
    return out


def city_map(idx, name, gov, lat, lon):
    utc, tzl = 3, "EEST"
    c = city_circumstances(lat, lon, utc)
    half = 1.35
    lat0, lat1 = lat - half, lat + half
    hl = half / np.cos(np.radians(lat)) * 1.15
    lon0, lon1 = lon - hl, lon + hl
    fig = plt.figure(figsize=(16, 9))
    ax = fig.add_axes([0.04, 0.07, 0.56, 0.84])
    setup_axes(ax, lon0, lon1, lat0, lat1, highlight=["EGY"], admin1_for=["EGY"], admin1_labels=True)
    LON, LAT, r = grid(lon0, lon1, lat0, lat1, n=260)
    draw_field(ax, LON, LAT, r, obs_fill=c["duration_s"] <= 0)
    draw_path(ax)
    near = [x for x in CITIES["egypt"]]
    draw_cities(ax, near, lon0, lon1, lat0, lat1, utc, fontsize=7.2, highlight=name)
    ax.set_title(f"{name} ({gov} Governorate) — total solar eclipse, 2 August 2027\n", loc="left", fontsize=12.5)
    ax.text(0.0, 1.008, f"{lat:.4f}°N  {lon:.4f}°E · local time EEST = UT+3 · labels: totality or % of Sun covered",
            transform=ax.transAxes, fontsize=8.5, color=INK2, va="bottom")
    add_colorbars(fig, ax, show_obs=c["duration_s"] <= 0)

    # --- right: phases of the eclipse as seen from the city
    seq = disk_sequence(lat, lon, c)
    axd = fig.add_axes([0.63, 0.52, 0.35, 0.34])
    axd.set_facecolor("#0f1b2d")
    axd.set_aspect("equal")
    spacing = 2.6 * seq[0][3]
    for k, (th, dx, dy, rs, rm) in enumerate(seq):
        cx = (k - 3) * spacing
        cy = 0.0
        is_total = c["duration_s"] > 0 and k == 3
        if is_total:
            for gr, al in [(2.2, 0.08), (1.7, 0.14), (1.35, 0.25)]:
                axd.add_patch(Circle((cx, cy), rs * gr, color="#e9f1ff", alpha=al, lw=0))
        sun = Circle((cx, cy), rs, color="#f7b733", lw=0)
        axd.add_patch(sun)
        moon = Circle((cx + dx, cy + dy), rm, color="#0f1b2d", lw=0)
        axd.add_patch(moon)
        moon.set_clip_path(sun)
        lab = ["C1", "", "", "Max", "", "", "C4"][k]
        axd.text(cx, -1.25 * rs, f"{lab}\n{circ.fmt_hms(th, utc, seconds=False)}" if lab else circ.fmt_hms(th, utc, seconds=False),
                 color="white", ha="center", va="top", fontsize=7.5)
    axd.set_xlim(-3.5 * spacing, 3.5 * spacing)
    axd.set_ylim(-2.6 * seq[0][3], 1.6 * seq[0][3])
    axd.set_xticks([])
    axd.set_yticks([])
    axd.set_title(f"Eclipse phases seen from {name} ({tzl}; up = towards zenith)", fontsize=10, loc="left")

    # --- table
    axt = fig.add_axes([0.63, 0.07, 0.35, 0.38])
    axt.axis("off")
    total = c["duration_s"] > 0
    rows = [
        ("Eclipse type here", "TOTAL" if total else "Partial"),
        ("Partial begins (C1)", f"{circ.fmt_hms(c['c1'], utc)} {tzl}   ({circ.fmt_hms(c['c1'])} UT)"),
        ("Totality begins (C2)", f"{circ.fmt_hms(c['c2'], utc)} {tzl}" if total else "—"),
        ("Maximum eclipse", f"{circ.fmt_hms(c['tmax'], utc)} {tzl}   ({circ.fmt_hms(c['tmax'])} UT)"),
        ("Totality ends (C3)", f"{circ.fmt_hms(c['c3'], utc)} {tzl}" if total else "—"),
        ("Partial ends (C4)", f"{circ.fmt_hms(c['c4'], utc)} {tzl}   ({circ.fmt_hms(c['c4'])} UT)"),
        ("Duration of totality", circ.fmt_dur(c["duration_s"]) if total else "none (outside the path)"),
        ("Duration of whole eclipse", circ.fmt_dur((c["c4"] - c["c1"]) * 3600).replace("m ", " min ").replace("s", " s")),
        ("Magnitude", f"{c['magnitude']:.4f}"),
        ("Obscuration of the Sun", f"{c['obscuration'] * 100:.2f} %"),
        ("Sun altitude / azimuth", f"{c['sun_alt']:.1f}° / {c['sun_az']:.1f}°"),
    ]
    tb = axt.table(cellText=[[a, b] for a, b in rows], colWidths=[0.42, 0.58], loc="upper left", cellLoc="left")
    tb.auto_set_font_size(False)
    tb.set_fontsize(9)
    tb.scale(1, 1.55)
    for (ri, ci), cell in tb.get_celld().items():
        cell.set_edgecolor("#e4e2dc")
        if ci == 0:
            cell.set_text_props(color=INK2)
        else:
            cell.set_text_props(color=INK, fontweight="bold" if ri in (0, 6) else "normal")
        if ri == 0:
            cell.set_facecolor(BLUE[2] if total else ORANGE[1])
    footer(fig)
    return save(fig, f"{idx:02d}_egypt_city_{slug(name)}")


# ----------------------------------------------------------------- tables
def write_tables():
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "besselian_elements.txt"), "w") as f:
        f.write("Besselian elements, total solar eclipse 2027-08-02, fitted from JPL DE421 (Skyfield)\n")
        f.write(f"t = hours from T0 = {besselian.T0_UT_HOURS:.1f} h UT;  value = a0 + a1 t + a2 t^2 + a3 t^3\n\n")
        for k in ("x", "y", "l1", "l2"):
            f.write(f"{k:>3}: " + "  ".join(f"{v:+.8f}" for v in getattr(B, k)) + "\n")
        f.write("  d: " + "  ".join(f"{v:+.8f}" for v in np.degrees(B.d)) + "   (deg)\n")
        f.write(" mu: " + "  ".join(f"{v:+.8f}" for v in np.degrees(B.mu)) + "   (deg, continuous)\n")
        f.write(f"tan f1 = {B.tan_f1:.7f}   tan f2 = {B.tan_f2:.7f}\n")
        gd = greatest_duration()
        f.write(f"\nGreatest duration on the central line: {circ.fmt_dur(gd['dur'])} at "
                f"{gd['lat']:.3f}N {gd['lon']:.3f}E, {circ.fmt_hms(gd['t'])} UT, Sun altitude {gd['alt']:.1f} deg\n")
        f.write(f"Central line on Earth from {circ.fmt_hms(PATH['t'][0])} to {circ.fmt_hms(PATH['t'][-1])} UT\n")
        w = path_width(np.linspace(-1.5, 1.8, 300))
        f.write(f"Maximum path width: {np.nanmax(w):.0f} km\n")

    fields = ["country", "city", "governorate", "latitude", "longitude", "utc_offset", "eclipse_type",
              "C1_local", "C2_local", "max_local", "C3_local", "C4_local", "C1_UT", "max_UT", "C4_UT",
              "totality_s", "totality", "magnitude", "obscuration_pct", "sun_altitude_deg", "sun_azimuth_deg"]
    gov = {n: g for n, g, *_ in EGYPT_CITIES}
    rows = []
    for key, (cname, _codes, utc, *_rest) in COUNTRIES.items():
        for name, la, lo in CITIES[key]:
            if key == "gibraltar" and name != "Gibraltar":
                continue
            c = city_circumstances(la, lo, utc)
            total = c["duration_s"] > 0
            rows.append(dict(
                country=cname if key != "gibraltar" else "Gibraltar", city=name, governorate=gov.get(name, "") if key == "egypt" else "",
                latitude=f"{la:.4f}", longitude=f"{lo:.4f}", utc_offset=f"{utc:+d}",
                eclipse_type="total" if total else ("partial" if c["magnitude"] > 0 else "none"),
                C1_local=circ.fmt_hms(c["c1"], utc), C2_local=circ.fmt_hms(c["c2"], utc) if total else "",
                max_local=circ.fmt_hms(c["tmax"], utc), C3_local=circ.fmt_hms(c["c3"], utc) if total else "",
                C4_local=circ.fmt_hms(c["c4"], utc), C1_UT=circ.fmt_hms(c["c1"]), max_UT=circ.fmt_hms(c["tmax"]),
                C4_UT=circ.fmt_hms(c["c4"]), totality_s=f"{c['duration_s']:.0f}",
                totality=circ.fmt_dur(c["duration_s"]) if total else "", magnitude=f"{c['magnitude']:.4f}",
                obscuration_pct=f"{c['obscuration'] * 100:.2f}", sun_altitude_deg=f"{c['sun_alt']:.1f}",
                sun_azimuth_deg=f"{c['sun_az']:.1f}"))
    for fname, sel in [("local_circumstances_all_cities.csv", rows),
                       ("local_circumstances_egypt.csv", [r for r in rows if r["country"] == "Egypt"])]:
        if "egypt" in fname:
            sel = sorted(sel, key=lambda r: (-float(r["totality_s"]), -float(r["obscuration_pct"])))
        with open(os.path.join(RESULTS, fname), "w", newline="", encoding="utf-8") as f:
            wr = csv.DictWriter(f, fieldnames=fields)
            wr.writeheader()
            wr.writerows(sel)
    print("wrote results/*.csv")
    return rows


def main():
    os.makedirs(RESULTS, exist_ok=True)
    write_tables()
    i = 1
    world_overview(i); i += 1
    regional_overview(i); i += 1
    central_line_profile(i); i += 1
    for key in COUNTRIES:
        country_map(i, key)
        i += 1
    egypt_governorates(i); i += 1
    egypt_contact_times(i); i += 1
    for name, gov, la, lo, own in EGYPT_CITIES:
        if own:
            city_map(i, name, gov, la, lo)
            i += 1
    print(f"{i - 1} maps written")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:  # e.g. python -m eclipse2027.maps city:Luxor  /  country:egypt
        for arg in sys.argv[1:]:
            kind, _, what = arg.partition(":")
            if kind == "city":
                for n, g, la, lo, _o in EGYPT_CITIES:
                    if n == what:
                        city_map(99, n, g, la, lo)
            elif kind == "country":
                country_map(99, what)
            else:
                globals()[kind](99)
    else:
        main()
