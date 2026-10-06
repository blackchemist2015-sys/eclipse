"""Historical eclipse computations for chapter 2 (cached to results/)."""
import json
import os

import numpy as np

from common import ROOT
from eclipse2027 import circumstances as C, engine as E

CACHE = os.path.join(ROOT, "results")

SITES = {"القاهرة": (30.0444, 31.2357), "الإسكندرية": (31.2001, 29.9187), "الأقصر": (25.6872, 32.6396),
         "أسوان": (24.0889, 32.8998)}

SYNODIC = 29.530588853
NM_2000 = 2451550.26   # new moon 2000-01-06 18:14 UT


def hijri_from_jd(jd):
    """Tabular (arithmetical) Islamic calendar date for a JD — may differ by a day from sighting."""
    jd = int(np.floor(jd + 0.5))
    l = jd - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    j = ((10985 - l) // 5316) * ((50 * l) // 17719) + (l // 5670) * ((43 * l) // 15238)
    l = l - ((30 - j) // 15) * ((17719 * j) // 50) - (j // 16) * ((15238 * j) // 43) + 29
    m = (24 * l) // 709
    d = l - (709 * m) // 24
    y = 30 * n + j - 30
    return y, m, d


HIJRI_MONTHS = ["محرم", "صفر", "ربيع الأول", "ربيع الآخر", "جمادى الأولى", "جمادى الآخرة", "رجب", "شعبان",
                "رمضان", "شوال", "ذو القعدة", "ذو الحجة"]
GREG_MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر",
               "نوفمبر", "ديسمبر"]


def summarize(ec, sites=SITES):
    out = {}
    for name, (la, lo) in sites.items():
        r = C.local_circumstances(ec.B, np.array([la]), np.array([lo]))
        out[name] = dict(obsc=float(r["obscuration"][0]), mag=float(r["magnitude"][0]),
                         dur=float(r["duration_s"][0]), tmax=float(r["tmax"][0]), alt=float(r["sun_alt_deg"][0]))
    return out


def scan_historic(y0=1000, y1=1900, name="historic_egypt_1000_1900.json"):
    """Find central eclipses (total/annular/hybrid) whose path covers any of SITES, y0..y1 (ERFA back-end)."""
    path = os.path.join(CACHE, name)
    if os.path.exists(path):
        return json.load(open(path))
    import erfa
    jd0 = E.jd_from_date(y0, 1, 1)
    jd1 = E.jd_from_date(y1, 1, 1)
    k0 = int(np.floor((jd0 - NM_2000) / SYNODIC))
    k1 = int(np.ceil((jd1 - NM_2000) / SYNODIC))
    rows = []
    for k in range(k0, k1):
        jd = NM_2000 + k * SYNODIC
        # quick node test with Moon98 + EPV00 at the mean new moon
        pv = erfa.moon98(2451545.0, jd - 2451545.0)[0]
        pvh, _ = erfa.epv00(2451545.0, jd - 2451545.0)
        sun = -pvh[0]
        ang = np.degrees(np.arccos(np.dot(pv, sun) / np.linalg.norm(pv) / np.linalg.norm(sun)))
        if ang > 12:   # Moon far from the Sun's direction → mean new moon too far from a node
            pass
        # ecliptic latitude of the Moon
        lat = np.degrees(np.arcsin(np.dot(pv / np.linalg.norm(pv), [0, -0.3977771559, 0.9174820621])))
        if abs(lat) > 2.2:
            continue
        try:
            ec = E.eclipse_near(jd, "erfa")
        except Exception:
            continue
        if ec.kind in ("none", "partial"):
            continue
        s = summarize(ec)
        hit = {n: v for n, v in s.items() if v["dur"] > 0 or (ec.kind == "annular" and v["mag"] > 0 and
                                                              v["obsc"] > 0.80 and _annular_at(ec, n))}
        if not any(v["dur"] > 0 for v in s.values()) and not any(_annular_at(ec, n) for n in s):
            continue
        rows.append(dict(date=list(ec.date), hour=ec.hour_ut, kind=ec.kind, jd=ec.jd_ut, gamma=ec.gamma,
                         dt=ec.delta_t, sites=s, annular_sites=[n for n in s if _annular_at(ec, n)]))
        print(ec.date, ec.kind, [n for n, v in s.items() if v["dur"] > 0], rows[-1]["annular_sites"])
    json.dump(rows, open(path, "w"), ensure_ascii=False)
    return rows


def _annular_at(ec, site):
    la, lo = SITES[site]
    r = C.local_circumstances(ec.B, np.array([la]), np.array([lo]))
    # inside the antumbra: distance from axis below |L2|
    return bool(r["umbral_margin"][0] > 0 and r["sun_up"][0] and ec.kind in ("annular", "hybrid"))


if __name__ == "__main__":
    scan_historic()
