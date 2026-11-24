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
            "ch6_maps.py", "ch8_world_history.py", "ch9_experiments.py", "ch10_apps.py", "ch11_appendix.py", "ch12_arab.py"]
# order of chapters in the book (source chapter ids); figures are numbered by book position
BOOK_ORDER = [1, 8, 2, 3, 4, 9, 5, 10, 12, 6, 7, 11]
ORD_AR = ["الأول", "الثاني", "الثالث", "الرابع", "الخامس", "السادس", "السابع", "الثامن", "التاسع", "العاشر", "الحادي عشر", "الثاني عشر"]
NAMES = {1: "الأساس العلمي للكسوف", 8: "توثيق الكسوف عبر التاريخ", 2: "الكسوف في تاريخ مصر",
         3: "كسوف ٢ أغسطس ٢٠٢٧", 4: "الرصد الآمن", 9: "تجارب علمية تمهيدية", 5: "تصوير الكسوف",
         10: "تطبيقات وأدوات التخطيط", 6: "خرائط إضافية", 7: "الأطلس: خرائط المسار ومصر",
         11: "ملحق: كل كسوفات الشمس ٢٠٢٤–٢٠٤٥", 12: "الكسوف في المدن العربية: مواعيد وخرائط ومواقع"}
TITLES = {src: (NAMES[src] if src == 11 else f"الفصل {ORD_AR[i]}: {NAMES[src]}") for i, src in enumerate(BOOK_ORDER)}

# Figures left out of the book to keep it under 250 pages (they are still drawn; the text that introduced them moves to
# the next figure kept in the same chapter). Keys are file names without extension.
EXCLUDE = set("""
fig_1_28_central_paths_1951_2000 fig_1_41_nasa_iss_transit fig_1_42_nasa_citizen_science fig_1_43_nasa_orion
fig_1_44_nasa_viewing fig_1_47_open_sdo_flare_earth_scale
fig_8_03_eclipse_763bc_assyria fig_8_06_eclipse_1851_first_photo
fig_8_11_eclipse_1973_concorde fig_8_12_eclipse_431bc_athens fig_8_14_delta_t_curve
fig_2_09_eclipse_978 fig_2_11_history_eclipse_1004 fig_2_12_history_lunar_cairo fig_2_15_eclipse_1882_comet_tewfik
fig_2_18_eclipse_2006_story fig_2_20_central_eclipses_egypt_table fig_2_21_cairo_luxor_all_eclipses
fig_2_22_central_eclipses_four_cities_1000_2050 fig_2_25_monuments_map
fig_3_05_shadow_0850 fig_3_08_shadow_0975 fig_3_11_shadow_1025 fig_3_12_shadow_1050 fig_3_14_shadow_1150
fig_3_30_city_card_minya fig_3_31_city_card_beni_suef fig_3_32_city_card_faiyum fig_3_34_city_card_giza
fig_3_36_city_card_hurghada fig_3_37_city_card_safaga fig_3_38_city_card_el_quseir fig_3_40_city_card_kharga
fig_3_41_city_card_mut_dakhla_oasis fig_3_42_city_card_edfu fig_3_43_city_card_kom_ombo fig_3_44_city_card_esna
fig_3_45_city_card_abu_simbel fig_3_46_city_card_sharm_el_sheikh fig_3_47_city_card_siwa fig_3_49_city_card_berenice
fig_4_10_glasses_timeline_sohag fig_4_12_glasses_timeline_aswan fig_4_13_glasses_timeline_asyut
fig_4_14_glasses_timeline_hurghada fig_4_18_heat_safety fig_4_19_where_to_watch_egypt
fig_5_08_exposure_table_f80 fig_5_09_exposure_table_f110 fig_5_13_tripod_drift_limit fig_5_15_totality_plan_sohag
fig_5_17_sequence_plan_cairo fig_5_18_sequence_plan_aswan fig_5_19_sequence_plan_hurghada fig_5_20_wide_angle_needed
fig_5_24_processing_workflow fig_5_27_vibration_free fig_5_29_camera_types
fig_6_05_governorate_minya fig_6_06_governorate_aswan fig_6_09_governorate_matrouh fig_6_11_governorate_beni_suef
fig_6_12_governorate_faiyum fig_6_13_governorate_cairo fig_6_14_governorate_south_sinai fig_6_18_delta_cairo
fig_6_19_sinai fig_6_20_egypt_shadow_1275 fig_6_21_egypt_shadow_1285 fig_6_22_egypt_shadow_1295
fig_6_23_egypt_shadow_1305 fig_6_24_egypt_shadow_1315 fig_6_25_egypt_shadow_1325
fig_11_06_region_2026_08_12 fig_11_08_region_2027_08_02
fig_11_11_region_2030_11_25 fig_11_12_region_2031_05_21
fig_11_14_region_2038_01_05 fig_11_15_region_2038_07_02
""".split())
ATLAS_KEEP = ("01_", "02_", "03_", "04_", "10_", "15_", "16_",          # general maps; Arab countries are in chapter 9
              "17_", "20_", "25_", "28_", "34_", "39_", "41_")             # a selection of Egyptian city maps with phases


def renumber(cat):
    """Assign book-order figure numbers (chapter position in the book, then index)."""
    from eclipse2027.i18n import ar_digits
    pos = {src: i + 1 for i, src in enumerate(BOOK_ORDER)}
    count = {}
    out = []
    for src in BOOK_ORDER:
        for c in [c for c in cat if c["chapter"] == src]:
            count[src] = count.get(src, 0) + 1
            p, n = pos[src], count[src]
            out.append(dict(c, book_chapter=p, src_number=c["number"], number=f"{p}-{n}", number_ar=ar_digits(n) + "-" + ar_digits(p)))
    return out

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
    files = sorted(f for f in os.listdir(os.path.join(ROOT, "maps_ar")) if f.endswith(".png") and f.startswith(ATLAS_KEEP))
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
    for n in [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]:
        p = os.path.join(FIG, f"catalogue_ch{n}.json")
        cat += json.load(open(p, encoding="utf-8"))
    cat += arabic_maps_catalogue()
    cat = [c for c in cat if os.path.splitext(os.path.basename(c["file"]))[0] not in EXCLUDE]
    cat = renumber(cat)
    json.dump(cat, open(os.path.join(HERE, "catalogue.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    kinds = {"map": "خريطة", "chart": "رسم بياني", "infographic": "إنفوجرافيك", "photo": "صورة"}
    parts = []
    for ch in BOOK_ORDER:
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
