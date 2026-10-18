"""Besselian elements of the 2027-08-02 total solar eclipse.

The elements are derived directly from the JPL DE421 ephemeris (through
Skyfield) and fitted with cubic polynomials in Universal Time, so every
later computation (local circumstances, path of totality, contact times)
is driven by real planetary positions rather than tabulated values.
"""
from dataclasses import dataclass

import numpy as np
from skyfield.api import load
from skyfield_data import get_skyfield_data_path

EARTH_RADIUS_KM = 6378.137
SUN_RADIUS_KM = 696000.0
K_PENUMBRA = 0.272488  # Moon radius / Earth radius (IAU, used for penumbra)
K_UMBRA = 0.272281     # NASA convention for umbral (total/annular) contacts
E2 = 0.00669438        # Earth's eccentricity squared (WGS-84)

T0_UT_HOURS = 10.0     # reference epoch: 2027-08-02 10:00 UT
FIT_SPAN_HOURS = 3.5


@dataclass
class Besselian:
    """Polynomial Besselian elements; t is hours from T0 (UT)."""
    x: np.ndarray
    y: np.ndarray
    d: np.ndarray       # radians
    mu: np.ndarray      # radians (wrapped continuously)
    l1: np.ndarray
    l2: np.ndarray
    tan_f1: float
    tan_f2: float

    def at(self, t):
        ev = np.polynomial.polynomial.polyval
        return dict(
            x=ev(t, self.x), y=ev(t, self.y), d=ev(t, self.d), mu=ev(t, self.mu),
            l1=ev(t, self.l1), l2=ev(t, self.l2),
            dx=ev(t, np.polynomial.polynomial.polyder(self.x)),
            dy=ev(t, np.polynomial.polynomial.polyder(self.y)),
            dd=ev(t, np.polynomial.polynomial.polyder(self.d)),
            dmu=ev(t, np.polynomial.polynomial.polyder(self.mu)),
        )


_TS = None
_EPH = None


def ephemeris():
    global _TS, _EPH
    if _EPH is None:
        _TS = load.timescale(builtin=True)
        _EPH = load(get_skyfield_data_path() + "/de421.bsp")
    return _TS, _EPH


def ut(hours_from_t0):
    """Skyfield Time for hours relative to T0 (UT)."""
    ts, _ = ephemeris()
    return ts.ut1(2027, 8, 2, 0, 0, T0_UT_HOURS * 3600.0 + np.asarray(hours_from_t0) * 3600.0)


def raw_elements(hours):
    ts, eph = ephemeris()
    t = ut(hours)
    earth = eph["earth"]
    obs = earth.at(t)
    s = obs.observe(eph["sun"]).apparent()
    m = obs.observe(eph["moon"]).apparent()
    # Equatorial rectangular coordinates (true equator and equinox of date), Earth radii.
    S = s.frame_xyz(_true_equator(t)).km / EARTH_RADIUS_KM
    M = m.frame_xyz(_true_equator(t)).km / EARTH_RADIUS_KM
    G = S - M
    g = G / np.linalg.norm(G, axis=0)
    d = np.arcsin(g[2])
    a = np.arctan2(g[1], g[0])
    mu = np.radians(t.gast * 15.0) - a
    # Rotate Moon into the fundamental plane frame.
    ca, sa, cd, sd = np.cos(a), np.sin(a), np.cos(d), np.sin(d)
    xm = -sa * M[0] + ca * M[1]
    ym = -sd * ca * M[0] - sd * sa * M[1] + cd * M[2]
    zm = cd * ca * M[0] + cd * sa * M[1] + sd * M[2]
    gdist = np.linalg.norm(G, axis=0)
    rs = SUN_RADIUS_KM / EARTH_RADIUS_KM
    sin_f1 = (rs + K_PENUMBRA) / gdist
    sin_f2 = (rs - K_UMBRA) / gdist
    f1, f2 = np.arcsin(sin_f1), np.arcsin(sin_f2)
    l1 = zm * np.tan(f1) + K_PENUMBRA / np.cos(f1)
    l2 = zm * np.tan(f2) - K_UMBRA / np.cos(f2)
    return dict(x=xm, y=ym, d=d, mu=np.unwrap(mu), l1=l1, l2=l2,
                tan_f1=np.tan(f1), tan_f2=np.tan(f2))


def _true_equator(t):
    from skyfield.framelib import true_equator_and_equinox_of_date
    return true_equator_and_equinox_of_date


def compute(degree=3):
    hours = np.linspace(-FIT_SPAN_HOURS, FIT_SPAN_HOURS, 141)
    r = raw_elements(hours)
    fit = lambda k: np.polynomial.polynomial.polyfit(hours, r[k], degree)
    return Besselian(x=fit("x"), y=fit("y"), d=fit("d"), mu=fit("mu"),
                     l1=fit("l1"), l2=fit("l2"),
                     tan_f1=float(np.mean(r["tan_f1"])),
                     tan_f2=float(np.mean(r["tan_f2"])))


# Published NASA elements (F. Espenak, NASA GSFC: VSOP87/ELP2000-82, Delta-T = 76.0 s,
# t in TD hours from 10:00 TD).  These are the elements behind NASA's own maps
# and tables, so durations and positions match NASA to a fraction of a second.
NASA_DELTA_T = 76.0
NASA_ELEMENTS = dict(
    x=[-0.0197720, 0.5447123, -0.0000446, -0.0000092],
    y=[0.1600610, -0.2111582, -0.0001217, 0.0000038],
    d=[17.7624702, -0.0101810, -0.0000040],          # degrees
    mu=[328.422546, 15.002100, 0.0],                 # degrees
    l1=[0.5305960, 0.0000138, -0.0000128],
    l2=[-0.0154640, 0.0000137, -0.0000128],
    tan_f1=0.0046064, tan_f2=0.0045834,
)
# NASA reference points (EclipseWise / NASA eclipse web site)
NASA_GREATEST_DURATION = dict(lat=26 + 48.8 / 60, lon=31 + 8.0 / 60, ut="10:00:21", seconds=383.24)
NASA_GREATEST_ECLIPSE = dict(lat=25 + 30.4 / 60, lon=33 + 10.8 / 60, ut="10:06:34", seconds=382.7)


def _shift(c, s):
    """Coefficients of p(t + s) for polynomial coefficients c (lowest first)."""
    out = np.zeros(len(c))
    for k, ck in enumerate(c):
        tk = np.polynomial.polynomial.polypow([s, 1.0], k)
        out[:len(tk)] += ck * tk
    return out


def nasa(delta_t=NASA_DELTA_T):
    """NASA's Besselian elements re-expressed in UT hours from 10:00 UT.

    t_TD = t_UT + delta_t; following Meeus (Elements of Solar Eclipses) the
    hour angle is corrected by 0.00417807 deg per second of Delta-T.
    """
    s = delta_t / 3600.0
    E = NASA_ELEMENTS
    rad = np.pi / 180
    mu = _shift(E["mu"], s)
    mu[0] -= 0.00417807 * delta_t
    return Besselian(x=_shift(E["x"], s), y=_shift(E["y"], s), d=_shift(E["d"], s) * rad, mu=mu * rad,
                     l1=_shift(E["l1"], s), l2=_shift(E["l2"], s), tan_f1=E["tan_f1"], tan_f2=E["tan_f2"])


def elements():
    """Elements used throughout the project: NASA's published set."""
    return nasa()
