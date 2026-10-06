"""English / Arabic text for maps and book graphics.

Matplotlib >= 3.11 shapes Arabic and applies the Unicode bidi algorithm
itself, so Arabic strings are passed through unchanged (no reshaping).
Numbers in Arabic output use Eastern Arabic digits (٠١٢٣٤٥٦٧٨٩), the
convention of Egyptian publishing.
"""
import os

import numpy as np

LANG = os.environ.get("ECLIPSE_LANG", "en")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FONT_DIR = os.path.join(ROOT, "book", "fonts")

AR_FONT = ["Noto Sans Arabic", "DejaVu Sans"]
AR_TITLE_FONT = ["Noto Kufi Arabic", "DejaVu Sans"]
AR_BODY_FONT = ["Noto Naskh Arabic", "DejaVu Sans"]

_fonts_loaded = False


def _enable_rtl_text():
    """Force right-to-left paragraph direction for Arabic strings in matplotlib.

    A string such as "≈ ٥٫١°" has no strong letter, so the bidi algorithm would lay it out
    left-to-right; a leading RIGHT-TO-LEFT MARK on each line makes Arabic labels read correctly.
    Pure numeric labels (tick values) are left untouched.
    """
    import re
    from matplotlib.text import Text
    if getattr(Text, "_rtl_patched", False):
        return
    ar_letter = re.compile("[\u0621-\u064a]")
    ar_digit = re.compile("[\u0660-\u0669]")
    orig = Text.set_text

    def set_text(self, s):
        if isinstance(s, str) and s and not s.startswith("\u200f"):
            if ar_letter.search(s) or (ar_digit.search(s) and s.lstrip()[:1] in "≈~<>(+×"):
                s = "\n".join("\u200f" + line for line in s.split("\n"))
        return orig(self, s)

    Text.set_text = set_text
    Text._rtl_patched = True


def load_fonts():
    global _fonts_loaded
    if _fonts_loaded:
        return
    _enable_rtl_text()
    from matplotlib import font_manager as fm
    for f in sorted(os.listdir(FONT_DIR)):
        if f.endswith(".ttf"):
            fm.fontManager.addfont(os.path.join(FONT_DIR, f))
    _fonts_loaded = True


def set_lang(lang):
    global LANG
    LANG = lang
    if lang == "ar":
        load_fonts()


def is_ar():
    return LANG == "ar"


_DIG = str.maketrans("0123456789.%,", "٠١٢٣٤٥٦٧٨٩٫٪٬")


def num(s):
    """Convert ASCII digits (and . % ,) in a string to Arabic forms when LANG == 'ar'."""
    s = str(s)
    return s.translate(_DIG) if is_ar() else s


def ar_digits(s):
    return str(s).translate(_DIG)


def fmt_time(hours, offset=0.0, seconds=True):
    if hours is None or not np.isfinite(hours):
        return "—"
    s = (hours + offset) * 3600.0
    s = round(s) if seconds else round(s / 60) * 60
    s %= 86400
    h, rem = divmod(int(s), 3600)
    m, sec = divmod(rem, 60)
    out = f"{h:02d}:{m:02d}:{sec:02d}" if seconds else f"{h:02d}:{m:02d}"
    return num(out)


def ar_count(n, one, two, few, many):
    """Arabic noun agreement with a number: 1, 2, 3–10, 11+ (and 0)."""
    n = int(n)
    if n == 1:
        return one
    if n == 2:
        return two
    if 3 <= n % 100 <= 10:
        return ar_digits(n) + " " + few
    return ar_digits(n) + " " + many


def fmt_dur(sec, long=False):
    if sec is None or not np.isfinite(sec) or sec <= 0:
        return "—"
    m, s = divmod(int(round(sec)), 60)
    if is_ar():
        if long:
            mm = ar_count(m, "دقيقة واحدة", "دقيقتان", "دقائق", "دقيقة")
            ss = ar_count(s, "ثانية واحدة", "ثانيتان", "ثوانٍ", "ثانية")
            return mm if s == 0 else (ss if m == 0 else mm + " و" + ss)
        return ar_digits(f"{m}") + " د " + ar_digits(f"{s:02d}") + " ث"
    return f"{m}m {s:02d}s"


def fmt_lat(v, decimals=1):
    if is_ar():
        return ar_digits(f"{abs(v):.{decimals}f}") + "°" + (" ش" if v >= 0 else " ج")
    return f"{abs(v):.{decimals}f}°{'N' if v >= 0 else 'S'}"


def fmt_lon(v, decimals=1):
    if is_ar():
        return ar_digits(f"{abs(v):.{decimals}f}") + "°" + (" ق" if v >= 0 else " غ")
    return f"{abs(v):.{decimals}f}°{'E' if v >= 0 else 'W'}"


def pct(v, decimals=1):
    return num(f"{v:.{decimals}f}%")


# ------------------------------------------------------------------ names
AR_PLACES = {
    # Spain / Gibraltar
    "Cádiz": "قادس", "Seville": "إشبيلية", "Málaga": "مالقة", "Tarifa": "طريفة",
    "Algeciras": "الجزيرة الخضراء", "Jerez de la Frontera": "شريش", "Granada": "غرناطة",
    "Almería": "ألمرية", "Córdoba": "قرطبة", "Huelva": "ولبة", "Ceuta": "سبتة", "Melilla": "مليلية",
    "Marbella": "ماربيا", "Gibraltar": "جبل طارق", "La Línea": "لا لينيا", "Estepona": "إستيبونا",
    "Barbate": "برباط",
    # Morocco
    "Tangier": "طنجة", "Tetouan": "تطوان", "Chefchaouen": "شفشاون", "Al Hoceima": "الحسيمة",
    "Nador": "الناظور", "Rabat": "الرباط", "Fez": "فاس", "Larache": "العرائش", "Oujda": "وجدة",
    "Casablanca": "الدار البيضاء", "Meknes": "مكناس", "Marrakesh": "مراكش",
    # Algeria
    "Oran": "وهران", "Algiers": "الجزائر العاصمة", "Tlemcen": "تلمسان", "Constantine": "قسنطينة",
    "Annaba": "عنابة", "Sétif": "سطيف", "Batna": "باتنة", "Biskra": "بسكرة", "Mostaganem": "مستغانم",
    "Chlef": "الشلف", "Tébessa": "تبسة", "El Oued": "الوادي", "Ghardaïa": "غرداية", "Djelfa": "الجلفة",
    "Laghouat": "الأغواط",
    # Tunisia
    "Tunis": "تونس", "Sfax": "صفاقس", "Sousse": "سوسة", "Kairouan": "القيروان", "Gabès": "قابس",
    "Djerba (Houmt Souk)": "جربة (حومة السوق)", "Gafsa": "قفصة", "Tozeur": "توزر", "Monastir": "المنستير",
    "Bizerte": "بنزرت", "Kasserine": "القصرين", "Medenine": "مدنين", "Tataouine": "تطاوين",
    # Libya
    "Tripoli": "طرابلس", "Benghazi": "بنغازي", "Misrata": "مصراتة", "Sirte": "سرت", "Tobruk": "طبرق",
    "Derna": "درنة", "Ajdabiya": "أجدابيا", "Al Bayda": "البيضاء", "Jalu": "جالو", "Kufra": "الكفرة",
    "Sabha": "سبها", "Ghadames": "غدامس", "Brega": "البريقة", "Al Jaghbub": "الجغبوب",
    # Sudan
    "Wadi Halfa": "وادي حلفا", "Port Sudan": "بورتسودان", "Halaib": "حلايب", "Dongola": "دنقلا",
    "Abu Hamad": "أبو حمد", "Atbara": "عطبرة", "Karima": "كريمة", "Khartoum": "الخرطوم",
    # Saudi Arabia
    "Jeddah": "جدة", "Mecca": "مكة المكرمة", "Medina": "المدينة المنورة", "Taif": "الطائف",
    "Riyadh": "الرياض", "Abha": "أبها", "Al Bahah": "الباحة", "Yanbu": "ينبع", "Najran": "نجران",
    "Jizan": "جازان", "Bisha": "بيشة", "Al Lith": "الليث", "Al Qunfudhah": "القنفذة",
    "Wadi ad-Dawasir": "وادي الدواسر", "As Sulayyil": "السليل", "Rabigh": "رابغ",
    "Khamis Mushait": "خميس مشيط",
    # Yemen
    "Sana'a": "صنعاء", "Aden": "عدن", "Taiz": "تعز", "Al Hudaydah": "الحديدة", "Marib": "مأرب",
    "Mukalla": "المكلا", "Sayun": "سيئون", "Ataq": "عتق", "Ibb": "إب", "Al Ghaydah": "الغيضة",
    "Sa'dah": "صعدة", "Shibam": "شبام", "Hadibu (Socotra)": "حديبو (سقطرى)",
    # Somalia
    "Bosaso": "بوصاصو", "Garowe": "جروي", "Qardho": "قرضو", "Hafun": "حافون", "Berbera": "بربرة",
    "Hargeisa": "هرجيسا", "Erigavo": "عيرجابو", "Caluula": "علولا", "Iskushuban": "إسكوشوبان",
    "Burao": "برعو", "Las Anod": "لاسعانود", "Mogadishu": "مقديشو",
    # Egypt
    "Luxor": "الأقصر", "Aswan": "أسوان", "Qena": "قنا", "Sohag": "سوهاج", "Asyut": "أسيوط",
    "Minya": "المنيا", "Beni Suef": "بني سويف", "Faiyum": "الفيوم", "Cairo": "القاهرة", "Giza": "الجيزة",
    "Alexandria": "الإسكندرية", "Hurghada": "الغردقة", "Safaga": "سفاجا", "El Quseir": "القصير",
    "Marsa Alam": "مرسى علم", "Kharga": "الخارجة", "Mut (Dakhla Oasis)": "موط (واحة الداخلة)",
    "Edfu": "إدفو", "Kom Ombo": "كوم أمبو", "Esna": "إسنا", "Abu Simbel": "أبو سمبل",
    "Sharm El Sheikh": "شرم الشيخ", "Dendera": "دندرة", "Nag Hammadi": "نجع حمادي",
    "Abydos (El Balyana)": "أبيدوس (البلينا)", "Farafra": "الفرافرة", "Baris": "باريس",
    "Siwa": "سيوة", "Marsa Matruh": "مرسى مطروح", "Port Said": "بورسعيد", "Suez": "السويس",
    "Ismailia": "الإسماعيلية", "El Tor": "الطور", "Dahab": "دهب", "Arish": "العريش",
    "Berenice": "برنيس", "Shalateen": "الشلاتين", "Mansoura": "المنصورة", "Tanta": "طنطا",
    "Zagazig": "الزقازيق", "Damietta": "دمياط", "Mallawi": "ملوي", "Tahta": "طهطا", "Qus": "قوص",
    "Armant": "أرمنت", "Daraw": "دراو", "Ras Gharib": "رأس غارب", "El Gouna": "الجونة",
    # regional overview
    "Madrid": "مدريد", "Rome": "روما", "Athens": "أثينا", "Istanbul": "إسطنبول",
    "Addis Ababa": "أديس أبابا", "Lisbon": "لشبونة", "Paris": "باريس (فرنسا)", "Tehran": "طهران",
    "Dubai": "دبي",
}

AR_GOVERNORATES = {
    "Luxor": "الأقصر", "Aswan": "أسوان", "Qena": "قنا", "Sohag": "سوهاج", "Asyut": "أسيوط",
    "Minya": "المنيا", "Beni Suef": "بني سويف", "Faiyum": "الفيوم", "Cairo": "القاهرة", "Giza": "الجيزة",
    "Alexandria": "الإسكندرية", "Red Sea": "البحر الأحمر", "New Valley": "الوادي الجديد",
    "South Sinai": "جنوب سيناء", "North Sinai": "شمال سيناء", "Matrouh": "مطروح",
    "Port Said": "بورسعيد", "Suez": "السويس", "Ismailia": "الإسماعيلية", "Dakahlia": "الدقهلية",
    "Gharbia": "الغربية", "Al Sharqia": "الشرقية", "Damietta": "دمياط", "Kafr el-Sheikh": "كفر الشيخ",
    "Beheira": "البحيرة", "Monufia": "المنوفية", "Qalyubia": "القليوبية",
}

AR_COUNTRIES = {
    "spain": "إسبانيا", "gibraltar": "جبل طارق والمضيق", "morocco": "المغرب", "algeria": "الجزائر",
    "tunisia": "تونس", "libya": "ليبيا", "egypt": "مصر", "sudan": "السودان (الشمال الشرقي)",
    "saudi_arabia": "المملكة العربية السعودية", "yemen": "اليمن",
    "somalia": "الصومال (بونتلاند وأرض الصومال)",
}

AR_TZ = {
    "CEST": "توقيت وسط أوروبا الصيفي", "UTC+1": "التوقيت المحلي", "CET": "توقيت وسط أوروبا",
    "EET": "توقيت شرق أوروبا", "EEST": "توقيت مصر الصيفي", "CAT": "توقيت وسط أفريقيا",
    "AST": "توقيت السعودية واليمن", "EAT": "توقيت شرق أفريقيا",
}

_ADMIN_PREFIXES = ("محافظة ", "ولاية ", "مقاطعة ", "منطقة ", "جهة ", "إقليم ", "بلدية ")


def place(name):
    if is_ar():
        return AR_PLACES.get(name, name)
    return name


def governorate(name):
    if is_ar():
        return AR_GOVERNORATES.get(name, name)
    return name


def admin_label(name_en, name_ar):
    if is_ar() and isinstance(name_ar, str) and name_ar:
        for p in _ADMIN_PREFIXES:
            if name_ar.startswith(p):
                name_ar = name_ar[len(p):]
        return AR_GOVERNORATES.get(name_en, name_ar)
    return name_en


def utc_label(utc):
    if is_ar():
        sign = "+" if utc >= 0 else "−"
        return "التوقيت العالمي " + sign + ar_digits(abs(utc))
    return f"UT{utc:+d}"


# ------------------------------------------------------------------ UI strings
S = {
    "source": ("Computed from JPL DE421 ephemeris (Skyfield) via Besselian elements; borders: Natural Earth. "
               "Sea-level observer, smooth lunar limb.",
               "حُسبت من تقويم مختبر الدفع النفاث JPL DE421 عبر عناصر بِسِل؛ الحدود: Natural Earth. "
               "الراصد عند مستوى سطح البحر، مع إهمال تضاريس حافة القمر."),
    "total": ("total", "كلي"),
    "covered": ("covered", "مُغطّى"),
    "dur_bar": ("Duration of totality (min:s)", "مدة الكسوف الكلي (دقيقة:ثانية)"),
    "obs_bar": ("Sun's disk covered at maximum (%)", "نسبة تغطية قرص الشمس عند الذروة (٪)"),
    "central_line": ("Central line", "خط المركز"),
    "world_title": ("Total Solar Eclipse — 2 August 2027", "الكسوف الكلي للشمس — ٢ أغسطس ٢٠٢٧"),
    "world_sub": ("Path of totality (blue), obscuration of the Sun (orange %) and time of maximum eclipse (dashed, UT).",
                  "مسار الكسوف الكلي (أزرق)، ونسبة تغطية الشمس (برتقالي)، ووقت ذروة الكسوف (خطوط متقطعة، بالتوقيت العالمي)."),
    "greatest_dur": ("★ greatest duration {d} at {lat} {lon}", "★ أطول مدة {d} عند {lat} {lon}"),
    "regional_title": ("Total solar eclipse of 2 August 2027 — Europe, North Africa & Middle East",
                       "الكسوف الكلي للشمس ٢ أغسطس ٢٠٢٧ — أوروبا وشمال أفريقيا والشرق الأوسط"),
    "regional_foot": ("Red dots: central-line time of totality (UT).",
                      "النقاط الحمراء: وقت الكسوف الكلي على خط المركز (بالتوقيت العالمي)."),
    "ut": (" UT", " ت.ع"),
    "prof_dur": ("Totality on central line (min)", "مدة الكلية على خط المركز (دقيقة)"),
    "prof_w": ("Path width (km)", "عرض المسار (كم)"),
    "prof_alt": ("Sun altitude (°)", "ارتفاع الشمس (°)"),
    "prof_x": ("Longitude of central line (°E)", "خط طول نقطة خط المركز (° شرقاً)"),
    "prof_title": ("Along the central line: duration, path width and Sun altitude",
                   "على امتداد خط المركز: مدة الكلية وعرض المسار وارتفاع الشمس"),
    "prof_gd": ("Greatest duration {d}\n{lat} {lon} (Egypt)", "أطول مدة {d}\n{lat} {lon} (مصر)"),
    "country_title": ("{name} — total solar eclipse, 2 August 2027", "{name} — الكسوف الكلي للشمس، ٢ أغسطس ٢٠٢٧"),
    "country_sub": ("Totality duration (blue) and % of the Sun covered (orange) at each city | local time {tz} = {utc}",
                    "مدة الكلية (أزرق) ونسبة تغطية الشمس (برتقالي) لكل مدينة | الوقت المحلي: {tz} = {utc}"),
    "country_foot": ("Blue lines: limits of totality; red dashed: central line.",
                     "الخطان الأزرقان: حدّا مسار الكلية؛ الخط الأحمر المتقطع: خط المركز."),
    "gov_title": ("Egypt by governorate — where totality lasts longest (2 August 2027)",
                  "مصر حسب المحافظات — أين يطول الكسوف الكلي؟ (٢ أغسطس ٢٠٢٧)"),
    "gov_head": ("Governorate", "المحافظة"),
    "gov_max": ("max totality", "أطول كلية"),
    "gov_area": ("area in path", "المساحة داخل المسار"),
    "c1_title": ("Partial eclipse begins (first contact)", "بداية الكسوف الجزئي (التماس الأول)"),
    "max_title": ("Maximum eclipse", "ذروة الكسوف"),
    "times_title": ("Egypt — eclipse timing, 2 August 2027 (contours every 5 minutes, local time)",
                    "مصر — توقيت الكسوف، ٢ أغسطس ٢٠٢٧ (خطوط كل ٥ دقائق، بالتوقيت المحلي)"),
    "egypt_tz": ("EEST (UT+3)", "توقيت مصر الصيفي (ت.ع +٣)"),
    "city_title": ("{name} ({gov} Governorate) — total solar eclipse, 2 August 2027",
                   "{name} (محافظة {gov}) — الكسوف الكلي للشمس، ٢ أغسطس ٢٠٢٧"),
    "city_sub": ("{lat}  {lon} | local time EEST = UT+3 | labels: totality or % of Sun covered",
                 "{lat}  {lon} | التوقيت المحلي: توقيت مصر الصيفي (ت.ع +٣) | البطاقات: مدة الكلية أو نسبة التغطية"),
    "phases_title": ("Eclipse phases seen from {name} (EEST; up = towards zenith)",
                     "مراحل الكسوف كما تُرى من {name} (الأعلى = نحو سمت الرأس)"),
    "C1": ("C1", "بداية"), "Max": ("Max", "الذروة"), "C4": ("C4", "النهاية"),
    "r_type": ("Eclipse type here", "نوع الكسوف هنا"),
    "r_c1": ("Partial begins (C1)", "بداية الكسوف الجزئي (التماس ١)"),
    "r_c2": ("Totality begins (C2)", "بداية الكلية (التماس ٢)"),
    "r_max": ("Maximum eclipse", "ذروة الكسوف"),
    "r_c3": ("Totality ends (C3)", "نهاية الكلية (التماس ٣)"),
    "r_c4": ("Partial ends (C4)", "نهاية الكسوف الجزئي (التماس ٤)"),
    "r_dur": ("Duration of totality", "مدة الكسوف الكلي"),
    "r_whole": ("Duration of whole eclipse", "مدة الكسوف كاملاً"),
    "r_mag": ("Magnitude", "قدر الكسوف"),
    "r_obs": ("Obscuration of the Sun", "نسبة احتجاب الشمس"),
    "r_alt": ("Sun altitude / azimuth", "ارتفاع الشمس / اتجاهها (السمت)"),
    "TOTAL": ("TOTAL", "كلي"), "Partial": ("Partial", "جزئي"),
    "outside": ("none (outside the path)", "لا يوجد (خارج المسار)"),
    "minutes": ("min", "دقيقة"),
    "Egypt": ("Egypt", "مصر"),
}

PROFILE_MARKS = [
    (("Atlantic", "المحيط الأطلسي"), -30), (("Strait of\nGibraltar", "مضيق\nجبل طارق"), -5.6),
    (("Algeria", "الجزائر"), 3.5), (("Tunisia", "تونس"), 9.3), (("Libya", "ليبيا"), 18),
    (("Egypt", "مصر"), 31), (("Saudi\nArabia", "السعودية"), 41), (("Yemen", "اليمن"), 48.5),
    (("Somalia/\nIndian Ocean", "الصومال/\nالمحيط الهندي"), 56),
]


def t(key, **kw):
    en, ar = S[key]
    s = ar if is_ar() else en
    return s.format(**kw) if kw else s
