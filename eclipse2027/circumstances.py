"""Vectorised local circumstances and path geometry from Besselian elements.

Algorithms follow the Explanatory Supplement to the Astronomical Almanac
(ch. 9) / Meeus "Elements of Solar Eclipses": Newton iteration on the
fundamental-plane coordinates of the observer for the instant of maximum and
for the four contacts.
"""
import numpy as np

from .besselian import E2, T0_UT_HOURS

SQ1E2 = np.sqrt(1.0 - E2)


def observer_geocentric(lat_deg, height_m=0.0):
    phi = np.radians(lat_deg)
    u = np.arctan(SQ1E2 * np.tan(phi))
    h = height_m / 6378137.0
    rho_sin = SQ1E2 * np.sin(u) + h * np.sin(phi)
    rho_cos = np.cos(u) + h * np.cos(phi)
    return rho_sin, rho_cos


def _state(B, t, rho_sin, rho_cos, lam):
    e = B.at(t)
    H = e["mu"] + lam
    sH, cH = np.sin(H), np.cos(H)
    sd, cd = np.sin(e["d"]), np.cos(e["d"])
    xi = rho_cos * sH
    eta = rho_sin * cd - rho_cos * cH * sd
    zeta = rho_sin * sd + rho_cos * cH * cd
    dxi = e["dmu"] * rho_cos * cH
    deta = e["dmu"] * xi * sd - zeta * e["dd"]
    u, v = e["x"] - xi, e["y"] - eta
    a, b = e["dx"] - dxi, e["dy"] - deta
    L1 = e["l1"] - zeta * B.tan_f1
    L2 = e["l2"] - zeta * B.tan_f2
    return u, v, a, b, L1, L2, zeta


def local_circumstances(B, lat, lon, height_m=0.0, iterations=6):
    """Return a dict of arrays: times in UT hours of day (NaN when absent)."""
    lat = np.asarray(lat, float)
    lon = np.asarray(lon, float)
    rho_sin, rho_cos = observer_geocentric(lat, height_m)
    lam = np.radians(lon)

    t = np.zeros(np.broadcast(lat, lon).shape)
    for _ in range(iterations):
        u, v, a, b, L1, L2, zeta = _state(B, t, rho_sin, rho_cos, lam)
        t = t - (u * a + v * b) / (a * a + b * b)
    u, v, a, b, L1, L2, zeta = _state(B, t, rho_sin, rho_cos, lam)
    m = np.hypot(u, v)
    mag = (L1 - m) / (L1 + L2)
    ratio = (L1 - L2) / (L1 + L2)  # apparent Moon / Sun diameter
    tmax = t

    def contact(L_kind, sign):
        tc = tmax.copy()
        for _ in range(iterations):
            u, v, a, b, L1, L2, _z = _state(B, tc, rho_sin, rho_cos, lam)
            L = np.abs(L1 if L_kind == 1 else L2)
            n = np.hypot(a, b)
            S = (a * v - b * u) / (n * L)
            with np.errstate(invalid="ignore"):
                tau = -(u * a + v * b) / (n * n) + sign * L / n * np.sqrt(1 - S * S)
            tc = tc + tau
        return tc

    partial = m < L1
    total = m < np.abs(L2)
    with np.errstate(invalid="ignore"):
        c1 = np.where(partial, contact(1, -1), np.nan)
        c4 = np.where(partial, contact(1, +1), np.nan)
        c2 = np.where(total, contact(2, -1), np.nan)
        c3 = np.where(total, contact(2, +1), np.nan)
    sun_up = zeta > 0
    mag = np.where(partial & sun_up, mag, 0.0)
    obsc = obscuration(mag, ratio)
    dur = np.where(total & sun_up, (c3 - c2) * 3600.0, 0.0)
    off = getattr(B, "t0_hours", T0_UT_HOURS)
    return dict(tmax=tmax + off, c1=c1 + off, c2=c2 + off, c3=c3 + off, c4=c4 + off,
                magnitude=mag, obscuration=obsc, ratio=ratio, duration_s=dur,
                sun_alt_deg=np.degrees(np.arcsin(np.clip(zeta, -1, 1))),
                umbral_margin=np.abs(L2) - m, sun_up=sun_up)


def obscuration(mag, ratio):
    """Fraction of the solar disk area covered, for magnitude and Moon/Sun ratio."""
    mag = np.asarray(mag, float)
    r = np.asarray(ratio, float) * np.ones_like(mag)
    c = 1.0 + r - 2.0 * mag  # centre separation in solar radii
    out = np.zeros_like(mag)
    full = (mag > 0) & (c <= r - 1)
    out[full] = 1.0
    part = (mag > 0) & (c > np.abs(r - 1)) & (c < 1 + r)
    cc, rr = c[part], r[part]
    a1 = np.arccos(np.clip((cc**2 + 1 - rr**2) / (2 * cc), -1, 1))
    a2 = np.arccos(np.clip((cc**2 + rr**2 - 1) / (2 * cc * rr), -1, 1))
    area = a1 + rr**2 * a2 - 0.5 * np.sqrt(np.clip((-cc + 1 + rr) * (cc + 1 - rr) * (cc - 1 + rr) * (cc + 1 + rr), 0, None))
    out[part] = area / np.pi
    return out


def central_line(B, t_hours):
    """Geodetic lat/lon (deg) of the shadow axis on the ellipsoid, plus duration helpers."""
    e = B.at(np.asarray(t_hours, float))
    d, x, y = e["d"], e["x"], e["y"]
    rho1 = np.sqrt(1 - E2 * np.cos(d) ** 2)
    sd1 = np.sin(d) / rho1
    cd1 = SQ1E2 * np.cos(d) / rho1
    y1 = y / rho1
    Bq = 1 - x * x - y1 * y1
    ok = Bq > 0
    z1 = np.sqrt(np.where(ok, Bq, np.nan))
    sphi1 = y1 * cd1 + z1 * sd1
    cphi1_c = z1 * cd1 - y1 * sd1
    theta = np.arctan2(x, cphi1_c)
    phi1 = np.arcsin(np.clip(sphi1, -1, 1))
    lat = np.degrees(np.arctan(np.tan(phi1) / SQ1E2))
    lon = np.degrees(theta - e["mu"])
    lon = (lon + 180) % 360 - 180
    return lat, lon


def fmt_hms(hours, offset=0.0, seconds=True):
    if hours is None or not np.isfinite(hours):
        return "—"
    s = (hours + offset) * 3600.0
    s = round(s) if seconds else round(s / 60) * 60
    s %= 86400
    h, rem = divmod(int(s), 3600)
    m, sec = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{sec:02d}" if seconds else f"{h:02d}:{m:02d}"


def fmt_dur(sec):
    if not np.isfinite(sec) or sec <= 0:
        return "—"
    m, s = divmod(int(round(sec)), 60)
    return f"{m}m {s:02d}s"


def path_limits(B, t_hours, max_km=250.0, iterations=30):
    """Northern/southern limits of totality, found by bisection perpendicular to the track.

    Returns (lat_c, lon_c, lat_n, lon_n, lat_s, lon_s) arrays (deg).
    """
    t_hours = np.asarray(t_hours, float)
    lat_c, lon_c = central_line(B, t_hours)
    ok = np.isfinite(lat_c)
    t_hours, lat_c, lon_c = t_hours[ok], lat_c[ok], lon_c[ok]
    # local track direction (east, north in km)
    dlon = np.gradient(np.unwrap(np.radians(lon_c))) * np.cos(np.radians(lat_c))
    dlat = np.gradient(np.radians(lat_c))
    norm = np.hypot(dlon, dlat)
    te, tn = dlon / norm, dlat / norm
    out = []
    for side in (+1, -1):  # +1 = left of motion (north for an eastward track)
        pe, pn = -tn * side, te * side
        lo_s = np.zeros_like(lat_c)
        hi_s = np.full_like(lat_c, max_km)
        for _ in range(iterations):
            mid = 0.5 * (lo_s + hi_s)
            la = lat_c + np.degrees(mid * pn / 6371.0)
            lo = lon_c + np.degrees(mid * pe / (6371.0 * np.cos(np.radians(lat_c))))
            r = local_circumstances(B, la, lo, iterations=5)
            inside = r["umbral_margin"] > 0
            lo_s = np.where(inside, mid, lo_s)
            hi_s = np.where(inside, hi_s, mid)
        la = lat_c + np.degrees(lo_s * pn / 6371.0)
        lo = lon_c + np.degrees(lo_s * pe / (6371.0 * np.cos(np.radians(lat_c))))
        out += [la, lo]
    return (lat_c, lon_c, *out)


def instant(B, t_hours, lat, lon, height_m=0.0):
    """Eclipse state at one instant t (hours from B's T0) for arrays of observers."""
    lat = np.asarray(lat, float)
    lon = np.asarray(lon, float)
    rho_sin, rho_cos = observer_geocentric(lat, height_m)
    u, v, a, b, L1, L2, zeta = _state(B, np.full(np.broadcast(lat, lon).shape, float(t_hours)), rho_sin, rho_cos,
                                      np.radians(lon))
    m = np.hypot(u, v)
    up = zeta > 0
    mag = np.where((m < L1) & up, (L1 - m) / (L1 + L2), 0.0)
    ratio = (L1 - L2) / (L1 + L2)
    return dict(magnitude=mag, obscuration=obscuration(mag, ratio), umbra=(m < np.abs(L2)) & up, sun_up=up,
                sun_alt_deg=np.degrees(np.arcsin(np.clip(zeta, -1, 1))))
