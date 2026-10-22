"""Lunar eclipses for historical dates (ERFA Moon98/EPV00 + Espenak–Meeus ΔT, or DE421 after 1900).

Shadow radii follow the classical (Chauvenet/Danjon-style) rule with a 2 % atmospheric enlargement:
    umbra    = 1.02 (0.998340 π_moon − s_sun + π_sun)
    penumbra = 1.02 (0.998340 π_moon + s_sun + π_sun)
Magnitudes are in units of the Moon's apparent diameter; times in UT.
"""
from dataclasses import dataclass

import numpy as np

from . import engine as E
from .besselian import EARTH_RADIUS_KM, SUN_RADIUS_KM

MOON_RADIUS_KM = 1737.4


@dataclass
class LunarEclipse:
    jd_ut: float
    date: tuple
    hour_ut: float
    kind: str              # "total", "partial", "penumbral", "none"
    umbral_mag: float
    penumbral_mag: float
    p1: float              # contacts (JD UT); NaN when absent
    u1: float
    u2: float
    u3: float
    u4: float
    p4: float
    delta_t: float


def _geometry(jd):
    backend = E.backend_for(float(np.atleast_1d(jd)[0]))
    S, M, gast = (E._vectors_de421 if backend == "de421" else E._vectors_erfa)(np.atleast_1d(jd))
    rs, rm = np.linalg.norm(S, axis=0), np.linalg.norm(M, axis=0)
    anti = -S / rs
    sep = np.arccos(np.clip(np.sum(anti * (M / rm), axis=0), -1, 1))
    pi_m, pi_s = np.arcsin(EARTH_RADIUS_KM / rm), np.arcsin(EARTH_RADIUS_KM / rs)
    s_s, s_m = np.arcsin(SUN_RADIUS_KM / rs), np.arcsin(MOON_RADIUS_KM / rm)
    umb = 1.02 * (0.998340 * pi_m - s_s + pi_s)
    pen = 1.02 * (0.998340 * pi_m + s_s + pi_s)
    return sep, umb, pen, s_m, M, gast


def lunar_eclipse_near(jd_guess_ut):
    """The lunar eclipse (if any) at the full moon nearest jd_guess_ut."""
    hrs = np.arange(-60, 60.01, 1.0)
    sep = _geometry(jd_guess_ut + hrs / 24)[0]
    jd0 = jd_guess_ut + hrs[int(np.argmin(sep))] / 24
    hrs = np.linspace(-1.5, 1.5, 181)
    jds = jd0 + hrs / 24
    sep, umb, pen, sm, _, _ = _geometry(jds)
    i = int(np.argmin(sep))
    jmax = jds[i]
    umag = (umb[i] + sm[i] - sep[i]) / (2 * sm[i])
    pmag = (pen[i] + sm[i] - sep[i]) / (2 * sm[i])
    kind = "total" if umag >= 1 else "partial" if umag > 0 else "penumbral" if pmag > 0 else "none"
    # contacts on a fine grid ±4 h
    jj = jmax + np.linspace(-4, 4, 961) / 24
    s2, u2_, p2_, sm2, _, _ = _geometry(jj)

    def cross(f):
        idx = np.where(np.diff(np.sign(f)) != 0)[0]
        out = []
        for k in idx:
            a, b = f[k], f[k + 1]
            out.append(jj[k] + (jj[k + 1] - jj[k]) * a / (a - b))
        return out
    pc = cross(p2_ + sm2 - s2)
    uc = cross(u2_ + sm2 - s2)
    tc = cross(u2_ - sm2 - s2)
    nan = float("nan")
    p1, p4 = (pc + [nan, nan])[:2] if len(pc) >= 2 else (nan, nan)
    u1, u4 = (uc[0], uc[-1]) if len(uc) >= 2 else (nan, nan)
    u2, u3 = (tc[0], tc[-1]) if len(tc) >= 2 else (nan, nan)
    y, m, d, h = E.date_from_jd(jmax)
    return LunarEclipse(jmax, (y, m, d), h, kind, float(umag), float(pmag), p1, u1, u2, u3, u4, p4,
                        E.delta_t(y + (m - 0.5) / 12))


def moon_altitude(jd_ut, lat, lon):
    """Approximate geocentric altitude (deg) of the Moon for an observer (refraction and parallax ignored)."""
    _, _, _, _, M, gast = _geometry(jd_ut)
    M = M[:, 0]
    ra, dec = np.arctan2(M[1], M[0]), np.arcsin(M[2] / np.linalg.norm(M))
    H = gast[0] + np.radians(lon) - ra
    phi = np.radians(lat)
    return float(np.degrees(np.arcsin(np.sin(phi) * np.sin(dec) + np.cos(phi) * np.cos(dec) * np.cos(H))))


def shadow_track(jds):
    """Moon's offset from the centre of Earth's shadow (deg; x towards east, y north) and radii (deg)."""
    jds = np.atleast_1d(jds)
    backend = E.backend_for(float(jds[0]))
    S, M, _ = (E._vectors_de421 if backend == "de421" else E._vectors_erfa)(jds)
    A = -S

    def radec(v):
        return np.arctan2(v[1], v[0]), np.arcsin(v[2] / np.linalg.norm(v, axis=0))
    ra_m, de_m = radec(M)
    ra_a, de_a = radec(A)
    x = np.degrees(np.unwrap(ra_m - ra_a) * np.cos(de_a))
    y = np.degrees(de_m - de_a)
    sep, umb, pen, s_m, _, _ = _geometry(jds)
    return x, y, np.degrees(umb), np.degrees(pen), np.degrees(s_m)
