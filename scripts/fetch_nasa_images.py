"""Download open NASA photographs of eclipse phenomena for the book (NASA Image and Video Library).

NASA still images are generally not copyrighted (https://www.nasa.gov/nasa-brand-center/images-and-media/);
each one is credited in the book as "NASA/<photographer>" with its NASA ID.

Usage (from the repository root; needs access to images-api.nasa.gov and images-assets.nasa.gov):
    python scripts/fetch_nasa_images.py            # fetch every phenomenon not yet downloaded
    python scripts/fetch_nasa_images.py --force    # re-fetch all
Pin a specific image by putting its NASA ID in PINNED.
"""
import json
import os
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "nasa_images")
API = "https://images-api.nasa.gov"

# key: (search query, words that must appear in title/description, words that must not)
PHENOMENA = {
    "diamond_ring": ("diamond ring total solar eclipse", ["diamond ring"], ["composite"]),
    "baily_beads": ("Baily's beads eclipse", ["baily"], []),
    "corona": ("total solar eclipse corona totality", ["total"], ["partial", "composite", "transit"]),
    "prominences": ("total solar eclipse prominences chromosphere", ["eclipse"], ["transit"]),
    "partial_sequence": ("solar eclipse composite sequence phases", ["composite"], []),
    "iss_shadow": ("moon shadow earth International Space Station eclipse", ["shadow"], []),
    "dscovr_shadow": ("DSCOVR EPIC moon shadow eclipse", ["shadow"], []),
    "iss_transit": ("International Space Station transit sun solar eclipse", ["transit"], []),
    "citizen_science": ("Civil Air Patrol solar eclipse mission weather data", ["weather"], []),
    "viewing": ("eclipse glasses viewing total solar eclipse", ["glasses"], []),
    "orion": ("Artemis II solar eclipse Orion", ["eclipse"], []),
}
# Images chosen by hand after reviewing the library (the search above is only a fallback)
PINNED = {
    "diamond_ring": "NHQ201708210102",      # Madras, Oregon, 2017 — Aubrey Gemignani
    "baily_beads": "NHQ201708210101",       # Madras, Oregon, 2017 — Aubrey Gemignani
    "corona": "NHQ201708210100",            # Madras, Oregon, 2017 — Aubrey Gemignani
    "prominences": "NHQ202404080107",       # Dallas, Texas, 2024 — Keegan Barber
    "partial_sequence": "NHQ201708210106",  # Madras composite, 2017 — Aubrey Gemignani
    "iss_shadow": "iss071e002694",          # 2024 umbra from the ISS
    "dscovr_shadow": "GSFC_20171208_Archive_e000005",  # DSCOVR/EPIC, 2017
    "iss_transit": "NHQ201708210202",       # ISS transit composite, 2017 — Joel Kowsky
    "citizen_science": "MAF_20240408_NOLAeclipse04",  # students record weather data, 2024 — Michael DeMocker
    "viewing": "NHQ201708210108",           # eclipse glasses, Madras 2017
    "orion": "art002e010782",               # Artemis II crew, eclipse from Orion, 2026
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "eclipse2027-book"}), timeout=60) as r:
        return r.read()


def search(q, page=1):
    url = f"{API}/search?" + urllib.parse.urlencode(dict(q=q, media_type="image", page=page))
    return json.loads(get(url))["collection"]["items"]


def pick(key):
    q, need, avoid = PHENOMENA[key]
    if key in PINNED:
        items = search(PINNED[key])
    else:
        items = search(q)
    for it in items:
        d = it["data"][0]
        text = (d.get("title", "") + " " + d.get("description", "")).lower()
        if key in PINNED:
            if d["nasa_id"] == PINNED[key]:
                return d
            continue
        if all(w in text for w in need) and not any(w in text for w in avoid):
            return d
    return None


def asset_url(nasa_id):
    hrefs = [i["href"] for i in json.loads(get(f"{API}/asset/{urllib.parse.quote(nasa_id)}"))["collection"]["items"]]
    for suffix in ("~large.jpg", "~medium.jpg", "~orig.jpg"):
        for h in hrefs:
            if h.endswith(suffix):
                return h.replace("http://", "https://")
    return None


def main():
    os.makedirs(OUT, exist_ok=True)
    cpath = os.path.join(OUT, "credits.json")
    credits = json.load(open(cpath, encoding="utf-8")) if os.path.exists(cpath) else {}
    force = "--force" in sys.argv
    for key in PHENOMENA:
        if key in credits and not force and os.path.exists(os.path.join(OUT, f"{key}.jpg")):
            continue
        try:
            d = pick(key)
        except OSError as e:
            sys.exit(f"cannot reach {API} ({e}); allow images-api.nasa.gov and images-assets.nasa.gov")
        if d is None:
            print(f"{key}: no matching image")
            continue
        url = asset_url(d["nasa_id"])
        if url is None:
            print(f"{key}: no JPEG for {d['nasa_id']}")
            continue
        open(os.path.join(OUT, f"{key}.jpg"), "wb").write(get(url))
        credits[key] = dict(nasa_id=d["nasa_id"], title=d.get("title", ""), photographer=d.get("photographer", ""),
                            center=d.get("center", ""), date=d.get("date_created", "")[:10], url=url,
                            page=f"https://images.nasa.gov/details/{d['nasa_id']}")
        print(f"{key}: {d['nasa_id']} — {d.get('title', '')}")
        json.dump(credits, open(cpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
