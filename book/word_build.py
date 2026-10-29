"""Build the Word edition: manuscript JSON → compressed images → .docx (via make_docx.js)."""
import json
import os
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(ROOT, ".cache", "docx_images")
OUT = os.path.join(HERE, "word", "كتاب_الكسوف_الكلي_2027.docx")


# lead image for each chapter opener (source chapter id -> image, crop centre as fractions)
HERO = {1: ("data/nasa_images/corona.jpg", 0.5, 0.5), 8: ("data/open_images/eso_lasilla_sequence.jpg", 0.5, 0.45),
        2: ("data/nasa_images/partial_sequence.jpg", 0.62, 0.3), 3: ("data/nasa_images/iss_shadow.jpg", 0.5, 0.5),
        4: ("data/nasa_images/viewing.jpg", 0.5, 0.45), 9: ("data/nasa_images/citizen_science.jpg", 0.5, 0.4),
        5: ("data/nasa_images/diamond_ring.jpg", 0.5, 0.55), 10: ("data/nasa_images/iss_transit.jpg", 0.5, 0.45),
        6: ("data/open_images/eso_lasilla_totality.jpg", 0.5, 0.35), 7: ("maps_ar/02_regional_overview_totality_and_obscuration.png", 0.5, 0.58),
        11: ("data/nasa_images/dscovr_shadow.jpg", 0.5, 0.42)}


def hero(src):
    """Crop the chapter's lead image to a 2:1 banner and cache it as JPEG."""
    path, cx, cy = HERO[src]
    dst = os.path.join(CACHE, f"hero_{src}.jpg")
    full = os.path.join(ROOT, path)
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(full):
        im = Image.open(full).convert("RGB")
        w, h = im.size
        bw, bh = (w, w // 2) if w / h < 2 else (h * 2, h)
        x0 = int(min(max(cx * w - bw / 2, 0), w - bw))
        y0 = int(min(max(cy * h - bh / 2, 0), h - bh))
        im = im.crop((x0, y0, x0 + bw, y0 + bh))
        im.thumbnail((1600, 800))
        im.save(dst, "JPEG", quality=86, optimize=True)
    return dst


def main():
    subprocess.run([sys.executable, os.path.join(HERE, "cover.py")], check=True)
    subprocess.run([sys.executable, os.path.join(HERE, "manuscript.py")], check=True)
    spec = json.load(open(os.path.join(HERE, "word", "manuscript.json"), encoding="utf-8"))
    os.makedirs(CACHE, exist_ok=True)
    for ch in spec["chapters"]:
        ch["hero"] = hero(ch["src"])
        for it in ch["items"]:
            if it["type"] != "figure":
                continue
            src = os.path.join(HERE, it["file"])
            dst = os.path.join(CACHE, os.path.basename(os.path.dirname(src)) + "_" + os.path.basename(src)[:-4] + ".jpg")
            if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
                im = Image.open(src).convert("RGB")
                im.thumbnail((1600, 2200))
                im.save(dst, "JPEG", quality=84, optimize=True)
            w, h = Image.open(dst).size
            it.update(jpg=dst, w=w, h=h)
    tmp = os.path.join(HERE, "word", "manuscript_img.json")
    json.dump(spec, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    subprocess.run(["node", os.path.join(HERE, "make_docx.js"), tmp, OUT], check=True)


if __name__ == "__main__":
    main()
