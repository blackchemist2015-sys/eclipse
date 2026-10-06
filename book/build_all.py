"""Rebuild every book figure and the Arabic gallery index.

Usage:  python book/build_all.py            (from the repository root)
"""
import json
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG = os.path.join(HERE, "figures")
CHAPTERS = ["ch1_science.py", "ch2_history.py", "ch3_event2027.py", "ch4_observing.py", "ch5_photography.py",
            "ch6_maps.py"]
TITLES = {1: "الفصل الأول: الأساس العلمي للكسوف", 2: "الفصل الثاني: الكسوف في تاريخ مصر",
          3: "الفصل الثالث: كسوف ٢ أغسطس ٢٠٢٧", 4: "الفصل الرابع: الرصد الآمن", 5: "الفصل الخامس: تصوير الكسوف",
          6: "الفصل السادس: خرائط إضافية", 7: "الفصل السابع: الأطلس — ٤٠ خريطة بالعربية"}

MAP_CAPTIONS_AR = {
    "world_overview_orthographic": "نظرة عالمية: مسار الكلية ونسب الاحتجاب ووقت الذروة",
    "regional_overview_totality_and_obscuration": "أوروبا وشمال أفريقيا والشرق الأوسط: الكلية والاحتجاب",
    "central_line_duration_width_profile": "على امتداد خط المركز: المدة وعرض المسار وارتفاع الشمس",
    "egypt_governorates_totality": "مصر حسب المحافظات: أين يطول الكسوف الكلي؟",
    "egypt_contact_times": "مصر: توقيت بداية الكسوف وذروته",
}


def run(script):
    r = subprocess.run([sys.executable, "-W", "ignore", script], cwd=HERE, capture_output=True, text=True)
    if r.returncode:
        print(r.stdout[-2000:], r.stderr[-4000:])
        raise SystemExit(f"{script} failed")
    return script


def build_figures():
    if os.path.isdir(FIG):
        shutil.rmtree(FIG)
    with ThreadPoolExecutor(3) as ex:
        for s in ex.map(run, CHAPTERS):
            print("done", s)


def arabic_maps_catalogue():
    from eclipse2027 import i18n as I
    from eclipse2027.places import COUNTRIES, EGYPT_CITIES
    from eclipse2027.maps import slug
    I.set_lang("ar")
    out = []
    files = sorted(f for f in os.listdir(os.path.join(ROOT, "maps_ar")) if f.endswith(".png"))
    city_by_slug = {slug(n): n for n, *_ in EGYPT_CITIES}
    for k, f in enumerate(files, 1):
        key = f[3:-4]
        if key in MAP_CAPTIONS_AR:
            cap = MAP_CAPTIONS_AR[key]
        elif key.startswith("country_"):
            cap = f"خريطة {I.AR_COUNTRIES[key[8:]]}: مسار الكلية ونسب الاحتجاب في المدن"
        elif key.startswith("egypt_city_"):
            n = city_by_slug[key[11:]]
            cap = f"خريطة مدينة {I.place(n)} مع مراحل الكسوف وجدول المواعيد"
        else:
            cap = key
        out.append(dict(chapter=7, number=f"7-{k}", number_ar=I.ar_digits(k) + "-" + I.ar_digits(7),
                        file=os.path.relpath(os.path.join(ROOT, "maps_ar", f), HERE), caption=cap, kind="map"))
    return out


def write_index():
    sys.path.insert(0, ROOT)
    cat = []
    for n in range(1, 7):
        p = os.path.join(FIG, f"catalogue_ch{n}.json")
        cat += json.load(open(p, encoding="utf-8"))
    cat += arabic_maps_catalogue()
    json.dump(cat, open(os.path.join(HERE, "catalogue.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    kinds = {"map": "خريطة", "chart": "رسم بياني", "infographic": "إنفوجرافيك"}
    parts = []
    for ch in range(1, 8):
        items = [c for c in cat if c["chapter"] == ch]
        cards = "\n".join(
            f'<figure><a href="{c["file"]}"><img loading="lazy" src="{c["file"]}" alt=""></a>'
            f'<figcaption><b>شكل {c["number_ar"]}</b> <span class="k">{kinds.get(c["kind"], "")}</span><br>{c["caption"]}</figcaption></figure>'
            for c in items)
        parts.append(f'<section><h2>{TITLES[ch]} <small>({len(items)} شكلًا)</small></h2><div class="grid">{cards}</div></section>')
    total = len(cat)
    html = f"""<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>رسوم كتاب كسوف ٢٠٢٧</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@600;700&family=Noto+Naskh+Arabic:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:#fbfaf7;--ink:#1f1f1d;--muted:#6b6a65;--card:#fff;--line:#e4e2dc;--accent:#0d366b}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{--bg:#12161d;--ink:#ecebe6;--muted:#a3a29c;--card:#1b212b;--line:#2a313d;--accent:#9ec5f4}}}}
:root[data-theme="dark"]{{--bg:#12161d;--ink:#ecebe6;--muted:#a3a29c;--card:#1b212b;--line:#2a313d;--accent:#9ec5f4}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:"Noto Naskh Arabic",serif;line-height:1.7}}
header{{padding:32px 16px 8px;max-width:1200px;margin:auto}}
h1,h2{{font-family:"Noto Kufi Arabic",sans-serif}} h1{{margin:0 0 6px;font-size:1.9rem}}
h2{{font-size:1.25rem;border-bottom:2px solid var(--line);padding-bottom:6px;color:var(--accent)}} h2 small{{color:var(--muted);font-weight:400}}
main{{max-width:1200px;margin:auto;padding:0 16px 48px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}}
figure{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}}
figure img{{width:100%;display:block;background:#fff}} figcaption{{padding:8px 12px 12px;font-size:.92rem}}
.k{{font-size:.75rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:0 8px;margin-inline-start:6px}}
p.lead{{color:var(--muted);margin:0}}
</style></head><body>
<header><h1>رسوم كتاب «الكسوف الكلي للشمس — ٢ أغسطس ٢٠٢٧»</h1>
<p class="lead">{total} شكلًا: إنفوجرافيك ورسوم بيانية وخرائط عربية، محسوبة من تقويم JPL DE421 ونظرية ERFA للتاريخ القديم. اضغط أي شكل لفتحه بدقة الطباعة.</p></header>
<main>{''.join(parts)}</main></body></html>"""
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(html)
    print("total figures:", total)


if __name__ == "__main__":
    if "--index-only" not in sys.argv:
        build_figures()
    write_index()
