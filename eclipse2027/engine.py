"""General solar-eclipse engine: Besselian elements for any eclipse.

Two ephemeris back-ends:
  * "de421": JPL DE421 through Skyfield (1900–2050, high accuracy);
  * "erfa":  ERFA's Moon98 lunar theory + EPV00 Earth ephemeris, with the
             Espenak–Meeus ΔT polynomials — used for historical eclipses
             before 1900 (accuracy limited mainly by ΔT).
The Besselian elements produced here plug into ``circumstances`` exactly
like the 2027 elements in ``besselian``.
"""
from dataclasses import dataclass

import numpy as np

from .besselian import Besselian, EARTH_RADIUS_KM, K_PENUMBRA, K_UMBRA, SUN_RADIUS_KM

AU_KM = 149597870.7
C_AU_PER_DAY = 173.1446326846693


# ----------------------------------------------------------------- ΔT (Espenak & Meeus, NASA)
def delta_t(year):
    y = float(year)
    if y < -500:
        u = (y - 1820) / 100
        return -20 + 32 * u * u
    if y < 500:
        u = y / 100
        return (10583.6 - 1014.41 * u + 33.78311 * u**2 - 5.952053 * u**3 - 0.1798452 * u**4
                + 0.022174192 * u**5 + 0.0090316521 * u**6)
    if y < 1600:
        u = (y - 1000) / 100
        return (1574.2 - 556.01 * u + 71.23472 * u**2 + 0.319781 * u**3 - 0.8503463 * u**4
                - 0.005050998 * u**5 + 0.0083572073 * u**6)
    if y < 1700:
        t = y - 1600
        return 120 - 0.9808 * t - 0.01532 * t**2 + t**3 / 7129
    if y < 1800:
        t = y - 1700
        return 8.83 + 0.1603 * t - 0.0059285 * t**2 + 0.00013336 * t**3 - t**4 / 1174000
    if y < 1860:
        t = y - 1800
        return (13.72 - 0.332447 * t + 0.0068612 * t**2 + 0.0041116 * t**3 - 0.00037436 * t**4
                + 0.0000121272 * t**5 - 0.0000001699 * t**6 + 0.000000000875 * t**7)
    if y < 1900:
        t = y - 1860
        return 7.62 + 0.5737 * t - 0.251754 * t**2 + 0.01680668 * t**3 - 0.0004473624 * t**4 + t**5 / 233174
    if y < 1920:
        t = y - 1900
        return -2.79 + 1.494119 * t - 0.0598939 * t**2 + 0.0061966 * t**3 - 0.000197 * t**4
    if y < 1941:
        t = y - 1920
        return 21.20 + 0.84493 * t - 0.076100 * t**2 + 0.0020936 * t**3
    if y < 1961:
        t = y - 1950
        return 29.07 + 0.407 * t - t**2 / 233 + t**3 / 2547
    if y < 1986:
        t = y - 1975
        return 45.45 + 1.067 * t - t**2 / 260 - t**3 / 718
    if y < 2005:
        t = y - 2000
        return 63.86 + 0.3345 * t - 0.060374 * t**2 + 0.0017275 * t**3 + 0.000651814 * t**4 + 0.00002373599 * t**5
    if y < 2050:
        t = y - 2000
        return 62.92 + 0.32217 * t + 0.005589 * t**2
    u = (y - 1820) / 100
    return -20 + 32 * u * u - 0.5628 * (2150 - y)


# ----------------------------------------------------------------- calendar helpers
def jd_from_date(y, m, d, hours=0.0):
    """Julian Day (UT) for a proleptic Julian/Gregorian civil date (Julian before 1582-10-15)."""
    if m <= 2:
        y -= 1
        m += 12
    gregorian = (y, m, d) >= (1582, 10, 15)
    a = y // 100
    b = 2 - a + a // 4 if gregorian else 0
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + b - 1524.5 + hours / 24.0


def date_from_jd(jd):
    jd = jd + 0.5
    z = int(jd)
    f = jd - z
    if z < 2299161:
        a = z
    else:
        alpha = int((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - alpha // 4
    b = a + 1524
    c = int((b - 122.1) / 365.25)
    d = int(365.25 * c)
    e = int((b - d) / 30.6001)
    day = b - d - int(30.6001 * e)
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715
    return year, month, day, f * 24.0


# ----------------------------------------------------------------- back-ends
def _vectors_de421(jd_ut):
    from skyfield.framelib import true_equator_and_equinox_of_date as frame
    from .besselian import ephemeris
    ts, eph = ephemeris()
    t = ts.ut1_jd(jd_ut)
    obs = eph["earth"].at(t)
    S = obs.observe(eph["sun"]).apparent().frame_xyz(frame).km
    M = obs.observe(eph["moon"]).apparent().frame_xyz(frame).km
    return S, M, np.radians(t.gast * 15.0)


def _vectors_erfa(jd_ut):
    import erfa
    jd_ut = np.atleast_1d(jd_ut)
    year = 2000 + (jd_ut[0] - 2451545.0) / 365.25
    dt = delta_t(year) / 86400.0
    jd_tt = jd_ut + dt
    S_out, M_out, gast = [], [], []
    for ju, jt in zip(jd_ut, jd_tt):
        pvh, pvb = erfa.epv00(2451545.0, jt - 2451545.0)
        # Sun: geocentric, light-time corrected (~8.3 min)
        tau = np.linalg.norm(pvh[0]) / C_AU_PER_DAY
        pvh2, _ = erfa.epv00(2451545.0, jt - tau - 2451545.0)
        sun = -pvh2[0]
        moon = erfa.moon98(2451545.0, jt - 2451545.0)[0]
        # annual aberration (classical) with Earth's barycentric velocity
        v = pvb[1] / C_AU_PER_DAY

        def aberr(p):
            r = np.linalg.norm(p)
            u = p / r
            u2 = u + v - np.dot(u, v) * u
            return u2 / np.linalg.norm(u2) * r
        rnpb = erfa.pnm06a(2451545.0, jt - 2451545.0)  # GCRS -> true equator & equinox of date
        S_out.append(rnpb @ aberr(sun) * AU_KM)
        M_out.append(rnpb @ aberr(moon) * AU_KM)
        gast.append(erfa.gst06a(2451545.0, ju - 2451545.0, 2451545.0, jt - 2451545.0))
    return np.array(S_out).T, np.array(M_out).T, np.unwrap(np.array(gast))


def raw_elements(jd_ut, backend):
    S, M, gast = (_vectors_de421 if backend == "de421" else _vectors_erfa)(jd_ut)
    S = S / EARTH_RADIUS_KM
    M = M / EARTH_RADIUS_KM
    G = S - M
    g = G / np.linalg.norm(G, axis=0)
    d = np.arcsin(g[2])
    a = np.arctan2(g[1], g[0])
    mu = np.unwrap(gast - a)
    ca, sa, cd, sd = np.cos(a), np.sin(a), np.cos(d), np.sin(d)
    x = -sa * M[0] + ca * M[1]
    y = -sd * ca * M[0] - sd * sa * M[1] + cd * M[2]
    z = cd * ca * M[0] + cd * sa * M[1] + sd * M[2]
    gd = np.linalg.norm(G, axis=0)
    rs = SUN_RADIUS_KM / EARTH_RADIUS_KM
    f1 = np.arcsin((rs + K_PENUMBRA) / gd)
    f2 = np.arcsin((rs - K_UMBRA) / gd)
    l1 = z * np.tan(f1) + K_PENUMBRA / np.cos(f1)
    l2 = z * np.tan(f2) - K_UMBRA / np.cos(f2)
    return dict(x=x, y=y, z=z, d=d, mu=mu, l1=l1, l2=l2, tan_f1=np.tan(f1), tan_f2=np.tan(f2))


@dataclass
class Eclipse:
    jd_ut: float          # instant of greatest eclipse (min distance of shadow axis), UT
    date: tuple           # (year, month, day) civil date of greatest eclipse (UT)
    hour_ut: float
    gamma: float
    l2: float
    kind: str             # "total", "annular", "hybrid", "partial", "none"
    B: Besselian
    backend: str
    delta_t: float


def backend_for(jd):
    return "de421" if 2415100.0 < jd < 2469700.0 else "erfa"


def eclipse_near(jd_guess_ut, backend=None):
    """Find the solar eclipse whose conjunction is near jd_guess_ut and fit its Besselian elements."""
    backend = backend or backend_for(jd_guess_ut)
    # 1) coarse scan ±1.5 days for minimum |(x, y)|
    hrs = np.arange(-36, 36.01, 0.5)
    r = raw_elements(jd_guess_ut + hrs / 24, backend)
    i = int(np.argmin(np.hypot(r["x"], r["y"])))
    jd0 = jd_guess_ut + hrs[i] / 24
    hrs = np.linspace(-1, 1, 81)
    r = raw_elements(jd0 + hrs / 24, backend)
    i = int(np.argmin(np.hypot(r["x"], r["y"])))
    jd_ge = jd0 + hrs[i] / 24
    # 2) fit around the hour nearest greatest eclipse
    y, m, d, h = date_from_jd(jd_ge)
    t0h = float(np.round(h))
    jd_t0 = jd_ge - (h - t0h) / 24
    span = np.linspace(-3.5, 3.5, 71)
    r = raw_elements(jd_t0 + span / 24, backend)
    fit = lambda k: np.polynomial.polynomial.polyfit(span, r[k], 3)
    B = Besselian(x=fit("x"), y=fit("y"), d=fit("d"), mu=fit("mu"), l1=fit("l1"), l2=fit("l2"),
                  tan_f1=float(np.mean(r["tan_f1"])), tan_f2=float(np.mean(r["tan_f2"])))
    B.t0_hours = t0h
    B.date = (y, m, d)
    tg = (jd_ge - jd_t0) * 24
    e = B.at(tg)
    gamma = float(np.hypot(e["x"], e["y"]) * np.sign(e["y"]))
    l2 = float(e["l2"])
    kind = classify(gamma, l2, float(e["l1"]))
    return Eclipse(jd_ut=jd_ge, date=(y, m, d), hour_ut=h, gamma=gamma, l2=l2, kind=kind, B=B,
                   backend=backend, delta_t=delta_t(y + (m - 0.5) / 12))


def classify(gamma, l2, l1):
    g = abs(gamma)
    if g > 1.0 + l1:
        return "none"
    if g > 0.9972:
        return "partial" if g < 1.0 + l1 else "none"
    # central: compare umbral radius on the Earth's surface
    zeta = np.sqrt(max(1 - g * g, 0))
    l2_surface = l2 - zeta * 0.0046
    if l2 < 0 and l2_surface < 0:
        return "total"
    if l2 > 0 and l2_surface > 0:
        return "annular"
    return "hybrid"


def new_moons(year0, year1):
    """New moons (JD UT) between two years, from DE421 via Skyfield."""
    from skyfield import almanac
    from .besselian import ephemeris
    ts, eph = ephemeris()
    t, ph = almanac.find_discrete(ts.utc(year0, 1, 1), ts.utc(year1, 1, 1), almanac.moon_phases(eph))
    return [ti.ut1 for ti, p in zip(t, ph) if p == 0]


def solar_eclipses(year0, year1):
    """All solar eclipses between year0 and year1 (DE421 range), as Eclipse objects."""
    from skyfield.api import load  # noqa: F401
    from .besselian import ephemeris
    ts, eph = ephemeris()
    out = []
    for jd in new_moons(year0, year1):
        t = ts.ut1_jd(jd)
        e = eph["earth"].at(t)
        s = e.observe(eph["sun"]).apparent()
        m = e.observe(eph["moon"]).apparent()
        if s.separation_from(m).degrees > 1.8:   # far from a node — no eclipse possible
            continue
        ec = eclipse_near(jd, "de421")
        if ec.kind != "none":
            out.append(ec)
    return out
