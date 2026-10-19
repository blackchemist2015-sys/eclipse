"""Chapter 5 — camera settings explained, with Arabic terms and their English equivalents."""
import numpy as np

from common import (A, BLUE, GREEN, INK, INK2, LINE, MUTED, NAVY, PAPER, RED, SUN, SUN_DEEP, TITLE, Circ, arrow,
                    canvas, card, footer, header, page, plt, save, wrap)

CH = 5
LRI, PDI = "⁦", "⁩"


def en(t):
    return LRI + t + PDI


# ------------------------------------------------------------------ exposure triangle
def fig_exposure_triangle():
    fig = page(8.6, 8.6)
    ax = canvas(fig)
    header(fig, "مثلث التعريض (Exposure Triangle)", "ثلاثة إعدادات تتحكم في كمية الضوء الواصلة إلى المستشعر، ولكل منها أثر جانبي")
    A_, S_, I_ = (0.5, 0.74), (0.22, 0.40), (0.78, 0.40)
    ax.add_patch(plt.Polygon([A_, S_, I_], fc="#eef4fc", ec=BLUE[8], lw=2))
    ax.text(0.5, 0.52, "التعريض\n(Exposure)", ha="center", va="center", fontsize=13, fontweight="bold", color=NAVY,
            fontfamily=TITLE, linespacing=1.4)
    # aperture (apex)
    ax.text(0.5, 0.775, "فتحة العدسة (Aperture) — رقم f", ha="center", fontsize=11.5, fontweight="bold", color=NAVY)
    for k, (f, r) in enumerate([(2.8, 0.030), (5.6, 0.020), (11, 0.010)]):
        x = 0.40 + k * 0.10
        ax.add_patch(Circ(ax, (x, 0.83), 0.034, fc="#3b4250", ec="none"))
        ax.add_patch(Circ(ax, (x, 0.83), r, fc=SUN, ec="none"))
        ax.text(x, 0.873, en(f"f/{f:g}"), ha="center", fontsize=8.8)
    # shutter (left corner)
    ax.text(0.20, 0.345, "زمن الغالق (Shutter speed)", ha="center", fontsize=11.5, fontweight="bold", color=NAVY)
    for k, (lab, w) in enumerate([("1/1000 s", 0.02), ("1/60 s", 0.06), ("1 s", 0.13)]):
        y = 0.305 - k * 0.035
        ax.add_patch(plt.Rectangle((0.08, y - 0.011), w, 0.022, fc=SUN_DEEP, ec="none"))
        ax.text(0.23, y, en(lab), ha="left", va="center", fontsize=8.8)
    # ISO (right corner) — noise samples in small inset axes
    ax.text(0.80, 0.345, "الحساسية (ISO)", ha="center", fontsize=11.5, fontweight="bold", color=NAVY)
    rng = np.random.default_rng(2)
    for k, (iso, n) in enumerate([(100, 0.03), (800, 0.12), (6400, 0.35)]):
        x = 0.68 + k * 0.12
        ia = fig.add_axes([x - 0.045, 0.225, 0.09, 0.09 * 8.6 / 8.6 * 0.95])
        ia.imshow(np.clip(0.55 + rng.normal(0, n, (14, 14)), 0, 1), cmap="gray", vmin=0, vmax=1)
        ia.axis("off")
        ax.text(x, 0.205, en(f"ISO {iso}"), ha="center", fontsize=8.8)
    effects = ["الفتحة الأوسع (رقم f أصغر): ضوء أكثر وعمق ميدان (Depth of field) أقل؛ في الكسوف اختر فتحة أضيق بدرجة أو درجتين من أوسعها.",
               "الغالق الأبطأ: ضوء أكثر مع خطر الاهتزاز (Motion blur)؛ زمن قصير للحبات والألسنة، وطويل للهالة الخارجية.",
               "الحساسية الأعلى: إشارة مضخّمة مع ضوضاء (Noise) أكثر؛ ابقَ بين ١٠٠ و٤٠٠ ما دامت الكاميرا على حامل."]
    y = 0.165
    for t in effects:
        w = wrap(t, 135)
        ax.text(0.965, y, "• " + w, ha="right", va="top", fontsize=8.9, linespacing=1.3)
        y -= 0.042 * (w.count("\n") + 1)
    footer(fig, "الدرجة (Stop): مضاعفة الضوء أو تنصيفه — مثل الانتقال من ١/٢٥٠ إلى ١/١٢٥ ث، أو من ISO ٢٠٠ إلى ٤٠٠، أو من f/8 إلى f/5.6.")
    save(fig, CH, "exposure_triangle", "مثلث التعريض: فتحة العدسة وزمن الغالق والحساسية وأثر كل منها.")


# ------------------------------------------------------------------ glossary of settings
TERMS = [
    ("فتحة العدسة", "Aperture (f-number)", "قطر الفتحة التي يدخل منها الضوء؛ الرقم الأصغر يعني فتحة أوسع.", "f/8–f/11 للعدسات المقرّبة"),
    ("زمن الغالق", "Shutter speed", "المدة التي يبقى فيها المستشعر معرَّضًا للضوء.", "من ١/٤٠٠٠ ث (الحبات) إلى ٢ ث (الهالة)"),
    ("الحساسية", "ISO", "تضخيم إشارة المستشعر؛ كلما ارتفعت زادت الضوضاء.", "١٠٠–٤٠٠"),
    ("الوضع اليدوي", "Manual mode (M)", "أنت تضبط الفتحة والغالق والحساسية بنفسك.", "إلزامي: الوضع الآلي يخطئ مع الهالة"),
    ("البعد البؤري", "Focal length", "يحدد التكبير ومجال الرؤية؛ قطر صورة الشمس ≈ البعد ÷ ١٠٩.", "٤٠٠–٨٠٠ مم للهالة"),
    ("التركيز اليدوي", "Manual focus (MF)", "ضبط الوضوح يدويًا بدل الآلة.", "على حافة الشمس عبر المرشح، ثم ثبّته"),
    ("الصيغة الخام", "RAW", "ملف يحفظ كل بيانات المستشعر دون ضغط أو معالجة.", "دائمًا، مع JPEG إن شئت"),
    ("التعريضات المتدرجة", "Bracketing / AEB", "سلسلة لقطات آلية بأزمنة مختلفة لتغطية مدى السطوع.", "٥–٩ لقطات بفارق درجة إلى درجتين"),
    ("توازن الأبيض", "White balance", "ضبط درجة لون الصورة.", "ضوء النهار (Daylight) ثابت، لا تلقائي"),
    ("مثبت الصورة", "Image stabilization (IS/VR)", "نظام يعوّض اهتزاز اليد.", "أوقفه على الحامل"),
    ("العرض الحي", "Live View", "رؤية الصورة على الشاشة الخلفية بدل محدد الرؤية.", "للتركيز والتأطير عبر المرشح"),
    ("المدرّج التكراري", "Histogram", "رسم يوضح توزيع درجات السطوع في الصورة.", "تجنّب التكدس عند الحافة اليمنى"),
    ("المرشح الشمسي", "Solar filter (ND 5.0)", "يقلل ضوء الشمس ١٠٠ ألف مرة.", "في المراحل الجزئية فقط"),
    ("مؤقّت الفواصل", "Intervalometer", "يلتقط صورًا آلية بفواصل زمنية محددة.", "للتتابع الزمني كل ٣–٥ دقائق"),
]


def fig_settings_glossary(part):
    rows = TERMS[:7] if part == 1 else TERMS[7:]
    H = 1.7 + 0.82 * len(rows)
    fig = page(8.8, H)
    ax = canvas(fig)
    header(fig, f"قاموس إعدادات الكاميرا ({A(part)} من ٢)", "المصطلح بالعربية والإنجليزية، ومعناه، والقيمة المقترحة يوم الكسوف")
    cols = [(0.965, "المصطلح (Term)"), (0.72, "المعنى"), (0.24, "يوم الكسوف")]
    top = 1 - 1.30 / H
    ax.add_patch(plt.Rectangle((0.03, top - 0.22 / H), 0.94, 0.44 / H, fc=NAVY, ec="none"))
    for x, c in cols:
        ax.text(x - 0.01, top, c, ha="right", va="center", fontsize=10, color="white", fontweight="bold")
    rh = 0.82 / H
    for i, (ar, eng, mean, ecl) in enumerate(rows):
        yc = top - 0.22 / H - rh * (i + 0.5)
        ax.add_patch(plt.Rectangle((0.03, yc - rh / 2), 0.94, rh, fc="#f1efea" if i % 2 == 0 else "white", ec=LINE))
        ax.text(0.955, yc + 0.13 / H, ar, ha="right", va="center", fontsize=10.5, fontweight="bold", color=NAVY)
        ax.text(0.955, yc - 0.17 / H, en(eng), ha="right", va="center", fontsize=9, color=BLUE[10],
                fontfamily=["DejaVu Sans"])
        ax.text(0.71, yc, wrap(mean, 42), ha="right", va="center", fontsize=9.2, linespacing=1.3)
        ax.text(0.23, yc, wrap(ecl, 26), ha="right", va="center", fontsize=9.2, color=GREEN, linespacing=1.3)
    footer(fig, "المصطلحات الإنجليزية كما تظهر في قوائم معظم الكاميرات؛ قد تختلف التسمية قليلًا بين الشركات (مثل IS لدى كانون وVR لدى نيكون).")
    save(fig, CH, f"settings_glossary_{part}", f"قاموس إعدادات الكاميرا بالعربية والإنجليزية مع القيم المقترحة للكسوف ({A(part)} من ٢).")


# ------------------------------------------------------------------ settings per phase
def fig_phase_settings():
    def shutter(q, fnum=8, iso=100):
        t = fnum ** 2 / (iso * 2 ** q)
        ladder = [1 / 8000, 1 / 4000, 1 / 2000, 1 / 1000, 1 / 500, 1 / 250, 1 / 125, 1 / 60, 1 / 30, 1 / 15, 1 / 8,
                  1 / 4, 1 / 2, 1, 2, 4, 8]
        s = min(ladder, key=lambda x: abs(np.log(x / t)))
        return ("١/" + A(int(round(1 / s)))) if s < 1 else (A(int(s)) + " ث")

    phases = [("الكسوف الجزئي", "Partial phases", "مركّب (ND 5.0)", 8, "كل ٥–١٠ دقائق"),
              ("حبات بيلي والخاتم الماسي", "Baily's beads & Diamond ring", "منزوع", 12, "تصوير متتابع سريع (Burst)"),
              ("الكروموسفير والألسنة", "Chromosphere & Prominences", "منزوع", 9, "أول الكلية وآخرها"),
              ("الهالة الداخلية", "Inner corona", "منزوع", 5, "ضمن سلسلة متدرجة"),
              ("الهالة الوسطى", "Mid corona", "منزوع", 1, "ضمن سلسلة متدرجة"),
              ("الهالة الخارجية", "Outer corona", "منزوع", -1, "على حامل ثابت تمامًا"),
              ("ضوء الأرض على القمر", "Earthshine", "منزوع", -8, "حامل متتبع؛ اختياري")]
    H = 1.9 + 0.62 * len(phases)
    fig = page(8.8, H, NAVY)
    ax = canvas(fig)
    header(fig, "إعدادات مقترحة لكل مرحلة", "الوضع اليدوي (M) | فتحة " + en("f/8") + " | حساسية " + en("ISO 100") +
           " | تركيز يدوي | صيغة " + en("RAW"), color="white", sub_color="#c9d3e3")
    cols = [(0.965, "المرحلة (Phase)"), (0.61, "المرشح (Filter)"), (0.43, "زمن الغالق"), (0.25, "ملاحظة")]
    top = 1 - 1.35 / H
    for x, c in cols:
        ax.text(x, top, c, ha="right", va="center", fontsize=10, color=SUN, fontweight="bold")
    rh = 0.62 / H
    for i, (ar, eng, filt, q, note) in enumerate(phases):
        yc = top - 0.30 / H - rh * (i + 0.5)
        card(ax, 0.03, yc - rh / 2 + 0.01, 0.94, rh - 0.02, fc="#18294a", ec="#2a3d5c", r=0.01)
        ax.text(0.955, yc + 0.10 / H, ar, ha="right", va="center", fontsize=10.2, color="white", fontweight="bold")
        ax.text(0.955, yc - 0.14 / H, en(eng), ha="right", va="center", fontsize=8.4, color="#9ec5f4",
                fontfamily=["DejaVu Sans"])
        ax.text(0.61, yc, filt, ha="right", va="center", fontsize=9.6, color=SUN_DEEP if "ND" in filt else "#c9d3e3")
        ax.text(0.43, yc, shutter(q), ha="right", va="center", fontsize=11, color="white", fontweight="bold")
        ax.text(0.25, yc, wrap(note, 22), ha="right", va="center", fontsize=9, color="#c9d3e3", linespacing=1.3)
    footer(fig, "الأزمنة محسوبة: الزمن = (رقم الفتحة)² ÷ (ISO × ٢^Q) بقيم Q لإسبيناك (ناسا). عند ISO ٢٠٠ نصّف كل زمن، وعند f/5.6 نصّفه أيضًا.",
           color="#8a96a8")
    save(fig, CH, "phase_settings", "إعدادات الكاميرا المقترحة لكل مرحلة من مراحل الكسوف (محسوبة).")


# ------------------------------------------------------------------ histogram
def fig_histogram():
    fig = page(8.8, 6.0)
    header(fig, "اقرأ المدرّج التكراري (Histogram)", "أصدق من شاشة الكاميرا في ظلام الكلية: يكشف ضياع التفاصيل في الظلال أو الإضاءات")
    x = np.linspace(0, 1, 256)
    cases = [("تعريض ناقص (Underexposed)", 0.12, 0.06, RED, "تفاصيل الهالة الخافتة ضاعت في السواد"),
             ("تعريض مناسب", 0.42, 0.14, GREEN, "منحنى ممتد دون التصاق بالحافتين"),
             ("تعريض زائد (Overexposed)", 0.90, 0.07, RED, "الهالة الداخلية «محروقة» (Clipping)")]
    for k, (ttl, mu, sd, col, note) in enumerate(cases):
        a = fig.add_axes([0.70 - k * 0.315, 0.32, 0.26, 0.38])
        y = 0.75 * np.exp(-0.5 * ((x - 0.03) / 0.02) ** 2) + np.exp(-0.5 * ((x - mu) / sd) ** 2)
        if mu > 0.8:
            y[-6:] += 2.2
        if mu < 0.2:
            y[:6] += 2.2
        a.fill_between(x, 0, y, color=col, alpha=0.55)
        a.set_xlim(0, 1)
        a.set_ylim(0, 3.2)
        a.set_xticks([0, 1])
        a.set_xticklabels(["أسود", "أبيض"], fontsize=8.5)
        a.set_yticks([])
        for s_ in ("top", "right", "left"):
            a.spines[s_].set_visible(False)
        a.set_title(ttl, fontsize=10.5, fontweight="bold", color=col)
        a.text(0.5, -0.17, wrap(note, 30), transform=a.transAxes, ha="center", va="top", fontsize=9)
    fig.text(0.965, 0.80, "المحور الأفقي: السطوع من الأسود (يسار) إلى الأبيض (يمين)، والرأسي: عدد البكسلات. القمة اليسرى = السماء وقرص القمر المظلم.",
             ha="right", fontsize=9.2, color=INK2)
    footer(fig, "رسم توضيحي. أثناء الكلية لا توجد صورة «صحيحة» واحدة؛ لذلك تُصوَّر سلسلة متدرجة (Bracketing) وتُدمج لاحقًا (HDR).")
    save(fig, CH, "histogram_guide", "كيف تقرأ المدرّج التكراري لتقييم تعريض صور الكسوف (رسم توضيحي).", "chart")


def all_figures():
    fig_exposure_triangle()
    fig_settings_glossary(1)
    fig_settings_glossary(2)
    fig_phase_settings()
    fig_histogram()
