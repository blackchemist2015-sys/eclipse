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


def main():
    subprocess.run([sys.executable, os.path.join(HERE, "manuscript.py")], check=True)
    spec = json.load(open(os.path.join(HERE, "word", "manuscript.json"), encoding="utf-8"))
    os.makedirs(CACHE, exist_ok=True)
    for ch in spec["chapters"]:
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
