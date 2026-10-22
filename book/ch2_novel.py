"""Chapter 2 — real solar and lunar eclipses named in the novel «أرصاد وأطوار», checked by computation.

The novel separates its historical events from its fiction (author's appendix); only the events it marks as
historical are used here, and each one is recomputed (ERFA Moon98/EPV00 + Espenak–Meeus ΔT before 1900).
"""
import numpy as np

import mapkit as MK
from common import (A, BLUE, GREEN, INK, INK2, LINE, MUTED, NAVY, PAPER, RED, SUN, SUN_DEEP, TITLE, Circ, canvas,
                    footer, halo, header, page, plt, save, wrap)
from eclipse2027 import circumstances as C, engine as E, i18n as I, lunar as L
from history_calc import GREG_MONTHS, HIJRI_MONTHS, hijri_from_jd

CH = 2
SRC = "المصدر: حسابات المؤلف"
NOVEL = "رواية «أرصاد وأطوار»"
CAIRO = (30.03, 31.23)        # Fustat / Fatimid Cairo
DENDERA = (26.1418, 32.6702)
AMARNA = (27.645, 30.896)     # Akhetaten
KIND_AR = {"total": "كلي", "annular": "حلقي", "hybrid": "هجين (حلقي-كلي)", "partial": "جزئي"}


def year_ar(y):
    """Astronomical year -> Arabic year label (1 BC = year 0)."""
    return f"{A(1 - y)} ق.م" if y <= 0 else f"{A(y)}م"


def date_ar(y, m, d):
    return f"{A(d)} {GREG_MONTHS[m - 1]} {year_ar(y)}"


def hijri_ar(jd):
    y, m, d = hijri_from_jd(jd)
    return f"{A(d)} {HIJRI_MONTHS[m - 1]} {A(y)}هـ"


def lmt(jd, lon):
    """Local mean time (decimal hours) at longitude lon for a JD (UT)."""
    return (E.date_from_jd(jd)[3] + lon / 15.0) % 24


def site(ec, la, lo):
    r = C.local_circumstances(ec.B, np.array([la]), np.array([lo]))
    return {k: float(np.ravel(v)[0]) for k, v in r.items()}


def sun_alt_at(ec, t_hours, la, lo):
    return float(C.instant(ec.B, t_hours - ec.B.t0_hours, [la], [lo])["sun_alt_deg"][0])


# ------------------------------------------------------------------ data
def compute():
    out = {}
    out["akh"] = E.eclipse_near(E.jd_from_date(-1337, 5, 14, 11), "erfa")
    out["s51"] = E.eclipse_near(E.jd_from_date(-50, 3, 7, 12), "erfa")
    out["s993"] = E.eclipse_near(E.jd_from_date(993, 8, 20, 8), "erfa")
    out["s1000"] = E.eclipse_near(E.jd_from_date(1000, 4, 7, 9), "erfa")
    out["s1004"] = E.eclipse_near(E.jd_from_date(1004, 1, 24, 13), "erfa")
    out["l52"] = L.lunar_eclipse_near(E.jd_from_date(-51, 9, 25, 23))
    out["l979"] = L.lunar_eclipse_near(E.jd_from_date(979, 11, 6, 21))
    out["l981"] = L.lunar_eclipse_near(E.jd_from_date(981, 4, 22, 2))
    out["l1002"] = L.lunar_eclipse_near(E.jd_from_date(1002, 3, 1, 23))
    return out


# ------------------------------------------------------------------ 1 Akhenaten
def dt_sigma(year):
    """Rough 1-sigma uncertainty of ΔT (s), after Morrison & Stephenson: ≈ 0.8 t², t in centuries from 1820."""
    return 0.8 * ((year - 1820) / 100.0) ** 2


def fig_akhenaten(ec):
    lon0, lon1, lat0, lat1 = 26.0, 36.0, 23.0, 32.0
    sig = dt_sigma(-1337)
    shift = 0.004178 * sig            # degrees of longitude per second of ΔT
    fig = plt.figure(figsize=(8.0, 7.8), facecolor=PAPER)
    ax = fig.add_axes([0.04, 0.215, 0.86, 0.585])
    MK.base(ax, lon0, lon1, lat0, lat1, labels=False)
    MK.field(ax, ec.B, lon0, lon1, lat0, lat1, n=280)
    la, lo = MK.path(ax, ec.B)
    for s, lab_ in [(+shift, "ΔT + " + A(f"{sig:.0f}") + " ث"), (-shift, "ΔT − " + A(f"{sig:.0f}") + " ث")]:
        ax.plot(lo + s, la, color=INK2, lw=1.0, ls=(0, (2, 3)), zorder=6)
        k = np.nanargmin(np.abs(lo + s - (34.6 if s > 0 else 27.0)))
        ax.text(lo[k] + s, la[k] + (0.15 if s > 0 else -0.15), lab_, fontsize=8, color=INK2, ha="center",
                va="bottom" if s > 0 else "top", path_effects=halo(), zorder=9)
    pts = [("تل العمارنة (أخت-آتون)", *AMARNA), ("القاهرة", *CAIRO), ("الأقصر", 25.6872, 32.6396)]
    MK.cities(ax, ec.B, pts, lon0, lon1, lat0, lat1, size=8.5)
    r = site(ec, *AMARNA)
    d_minus = site_shift(ec, AMARNA, -shift)
    d_plus = site_shift(ec, AMARNA, +shift)
    header(fig, "كسوف ١٤ مايو ١٣٣٨ ق.م فوق تل العمارنة",
           "«كسوف إخناتون» في " + NOVEL + ": كلي فوق عاصمته أخت-آتون بعد الظهر — بالحساب الحديث")
    fig.text(0.965, 0.835, f"النوع: {KIND_AR[ec.kind]} | الكلية في العمارنة {I.fmt_dur(r['duration_s'], long=True)} "
             f"والشمس على ارتفاع {A(f'{r['sun_alt_deg']:.0f}')}° | ΔT ≈ {A(f'{ec.delta_t:,.0f}')} ث",
             ha="right", fontsize=8.8, color=INK2)
    fig.text(0.965, 0.035, wrap("الخطان المنقّطان: موضع خط المركز لو اختلف فرق التوقيت ΔT بمقدار ± "
                                + A(f"{sig:.0f}") + " ثانية (انحراف معياري تقريبي). وتبقى العمارنة داخل الكلية في الحالتين "
                                + f"({I.fmt_dur(d_minus, long=True) if d_minus > 0 else 'خارجها'} و"
                                + f"{I.fmt_dur(d_plus, long=True) if d_plus > 0 else 'خارجها'}). "
                                + "أما نسبة الكسوف إلى السنة السادسة عشرة من حكم إخناتون فاجتهاد من الرواية لا يثبته نص مصري مؤرّخ.",
                                130), ha="right", va="bottom", fontsize=8.6, color=INK, linespacing=1.35)
    footer(fig, SRC + " بنظرية ERFA ومعادلات ΔT لإسبيناك ومييس؛ التاريخ بالتقويم اليولياني.")
    save(fig, CH, "novel_akhenaten_1338bc", "كسوف ١٤ مايو ١٣٣٨ ق.م الكلي فوق تل العمارنة مع نطاق عدم اليقين في ΔT (محسوب).", "map")


def site_shift(ec, pt, shift):
    """Totality at pt if the whole track moved east by `shift` degrees (a different ΔT)."""
    return site(ec, pt[0], pt[1] - shift)["duration_s"]


# ------------------------------------------------------------------ 2 Dendera ceiling: 51 BC solar + 52 BC lunar
def lunar_panel(ax, le, lon, title, note_lines):
    t = np.linspace(-3.2, 3.2, 161) / 24 + le.jd_ut
    x, y, umb, pen, sm = L.shadow_track(t)
    u, p, s = float(np.mean(umb)), float(np.mean(pen)), float(np.mean(sm))
    ax.set_facecolor(NAVY)
    ax.add_patch(plt.Circle((0, 0), p, fc="#3a4a66", ec="#6c7d99", lw=0.8))
    ax.add_patch(plt.Circle((0, 0), u, fc="#1c2638", ec="#9aa6b8", lw=0.8))
    ax.plot(-x, y, color="#9aa6b8", lw=0.8, ls="--")
    marks = [(le.u1, "بداية الظل"), (le.jd_ut, "الذروة"), (le.u4, "نهاية الظل")]
    if np.isnan(le.u1):
        marks = [(le.p1, "P1"), (le.jd_ut, "الذروة"), (le.p4, "P4")]
    for j, lab_ in marks:
        xx, yy, _, _, _ = L.shadow_track([j])
        inside = np.hypot(xx[0], yy[0]) < u + s
        col = "#b5533c" if (j == le.jd_ut and le.umbral_mag >= 1) else ("#d8c7a8" if not inside or j != le.jd_ut else "#c98b5e")
        ax.add_patch(plt.Circle((-xx[0], yy[0]), s, fc=col, ec="white", lw=0.6, zorder=4))
        ax.text(-xx[0], yy[0] - s - 0.07, I.fmt_time(lmt(j, lon), seconds=False), ha="center", va="top", fontsize=8,
                color="white")
    lim = p + 0.35
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=10.5, fontweight="bold", color=INK)
    ax.text(0.5, -0.04, "\n".join(note_lines), transform=ax.transAxes, ha="center", va="top", fontsize=8.8,
            linespacing=1.4)


def fig_dendera(s51, l52):
    fig = page(9.0, 7.0)
    header(fig, "قرصا سقف دندرة: كسوف وخسوف",
           "يقرأ باحثون في دائرة البروج بسقف دندرة كسوفًا للشمس وخسوفًا للقمر رآهما المصريون قبيل نقش السقف (نحو ٥٠ ق.م)")
    ax1 = fig.add_axes([0.50, 0.36, 0.46, 0.48])
    lon0, lon1, lat0, lat1 = -20.0, 60.0, 0.0, 50.0
    MK.base(ax1, lon0, lon1, lat0, lat1, labels=False)
    MK.field(ax1, s51.B, lon0, lon1, lat0, lat1, n=260)
    MK.path(ax1, s51.B)
    MK.cities(ax1, s51.B, [("دندرة", *DENDERA)], lon0, lon1, lat0, lat1, size=8.5)
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_title(f"كسوف الشمس — {date_ar(-50, 3, 7)}", fontsize=10.5, fontweight="bold")
    r = site(s51, *DENDERA)
    ax1.text(0.5, -0.04, f"{KIND_AR[s51.kind]} مرّ مساره شمال أفريقيا وغربها؛ ورآه أهل دندرة جزئيًا:\n"
             f"احتجاب {I.pct(r['obscuration'] * 100, 0)} عند {I.fmt_time(r['tmax'] + DENDERA[1] / 15, seconds=False)} "
             "بالتوقيت الشمسي المحلي", transform=ax1.transAxes, ha="center", va="top", fontsize=8.8, linespacing=1.4)
    ax2 = fig.add_axes([0.08, 0.36, 0.34, 0.48])
    alt = L.moon_altitude(l52.jd_ut, *DENDERA)
    lunar_panel(ax2, l52, DENDERA[1], f"خسوف القمر — {date_ar(-51, 9, 25)}",
                [f"خسوف كلي، قدره الظلّي {A(f'{l52.umbral_mag:.2f}')}، والقمر على ارتفاع {A(f'{alt:.0f}')}° فوق دندرة",
                 f"الكلية من {I.fmt_time(lmt(l52.u2, DENDERA[1]), seconds=False)} إلى {I.fmt_time(lmt(l52.u3, DENDERA[1]), seconds=False)} بالتوقيت المحلي"])
    fig.text(0.965, 0.045, wrap("في السقف قرصان: داخل أحدهما إيزيس تمسك قردًا من ذيله (يُقرأ كسوفًا للشمس)، وفي الآخر عين حورس "
                                "(يُقرأ خسوفًا للقمر). والحساب يؤكد وقوع الحدثين ورؤيتهما من صعيد مصر؛ أما ربط القرصين بهما فقراءة "
                                "علمية حديثة لا نصّ قديم. والأصل في متحف اللوفر منذ ١٨٢١ وفي موضعه نسخة مصبوبة.", 130),
             ha="right", va="bottom", fontsize=8.6, linespacing=1.35)
    footer(fig, SRC + " بنظرية ERFA ومعادلات ΔT؛ الأوقات بالتوقيت الشمسي المحلي لدندرة. الرسم الأيسر: القمر يعبر ظل الأرض (الشمال إلى أعلى).")
    save(fig, CH, "novel_dendera_eclipses", "كسوف ٥١ ق.م وخسوف ٥٢ ق.م المقروءان في سقف دندرة (محسوبان).", "map")


# ------------------------------------------------------------------ 3 Ibn Yunus era: solar eclipses over Cairo
def fig_993(ec):
    from ch2_history import eclipse_map
    sc = site(ec, *CAIRO)
    eclipse_map(ec, "كسوف ٢٠ أغسطس ٩٩٣م فوق شمال مصر",
                f"مرّ الظل الكلي قبالة الساحل الشمالي؛ وغطّى القمر {I.pct(sc['obscuration'] * 100, 0)} من الشمس في القاهرة",
                "novel_eclipse_993", "كسوف ٢٠ أغسطس ٩٩٣م الكلي قبالة ساحل مصر الشمالي كما رُصد من القاهرة (محسوب).",
                bounds=(18.0, 42.0, 22.0, 38.0),
                pts=[("القاهرة", *CAIRO), ("الإسكندرية", 31.2001, 29.9187), ("الأقصر", 25.6872, 32.6396)])


def fig_1004(ec):
    from ch2_history import eclipse_map
    sc = site(ec, *CAIRO)
    alt_end = sun_alt_at(ec, sc["c4"], *CAIRO)
    assert alt_end < 0, "the Sun should set before the end of the eclipse in Cairo"
    eclipse_map(ec, "كسوف ٢٤ يناير ١٠٠٤م: الشمس تغرب مكسوفة",
                f"كسوف هجين؛ بلغ الاحتجاب في القاهرة {I.pct(sc['obscuration'] * 100, 0)} والشمس على ارتفاع "
                f"{A(f'{sc['sun_alt_deg']:.0f}')}° فغربت قبل انتهائه",
                "novel_eclipse_1004", "كسوف ٢٤ يناير ١٠٠٤م الهجين: غروب الشمس مكسوفة في القاهرة (محسوب).",
                bounds=(14.0, 46.0, 18.0, 40.0),
                pts=[("القاهرة", *CAIRO), ("أسوان", 24.0889, 32.8998)])
    return alt_end


# ------------------------------------------------------------------ 4 lunar eclipses observed from Cairo
def fig_lunar_cairo(l979, l981, l1002):
    fig = page(9.4, 6.0)
    header(fig, "ثلاثة خسوفات للقمر فوق القاهرة الفاطمية",
           "خسوفا ٣٦٩ و٣٧٠هـ في أرصاد ابن يونس، وخسوف ٣٩٢هـ الكلي — كما يُرى القمر يعبر ظل الأرض")
    for k, (le, ttl) in enumerate([(l979, "ربيع الآخر ٣٦٩هـ"), (l981, "شوال ٣٧٠هـ"), (l1002, "ربيع الآخر ٣٩٢هـ")]):
        ax = fig.add_axes([0.68 - k * 0.32, 0.30, 0.28, 0.48])
        alt = L.moon_altitude(le.jd_ut, *CAIRO)
        kind = "كلي" if le.kind == "total" else "جزئي"
        y, m, d = le.date
        lunar_panel(ax, le, CAIRO[1], f"{ttl}\n{date_ar(y, m, d)}",
                    [f"خسوف {kind}، القدر الظلّي {A(f'{le.umbral_mag:.2f}')}",
                     f"الذروة {I.fmt_time(lmt(le.jd_ut, CAIRO[1]), seconds=False)} والقمر على ارتفاع {A(f'{max(alt, 0):.0f}')}°",
                     f"الحساب: ليلة {hijri_ar(le.jd_ut)}"])
    footer(fig, SRC + " بنظرية ERFA ومعادلات ΔT؛ الأوقات بالتوقيت الشمسي المحلي للقاهرة، والتاريخ الهجري حسابي (قد يختلف يومًا أو يومين عن الرؤية).")
    save(fig, CH, "novel_lunar_cairo", "خسوفات القمر في ٩٧٩ و٩٨١ و١٠٠٢م كما رُئيت من القاهرة (محسوبة).")


# ------------------------------------------------------------------ 5 summary table
def fig_table(D):
    akh = site(D["akh"], *AMARNA)
    s51 = site(D["s51"], *DENDERA)
    s993 = site(D["s993"], *CAIRO)
    s1000 = site(D["s1000"], *CAIRO)
    s1004 = site(D["s1004"], *CAIRO)
    rows = [
        ("١٤ مايو ١٣٣٨ ق.م", "كسوف شمس كلي", "كلي فوق أخت-آتون نحو ٤٫٥ دقيقة",
         f"كلي؛ {I.fmt_dur(akh['duration_s'])} في العمارنة", "ممكن (تاريخه غير يقيني)"),
        ("٢٥ سبتمبر ٥٢ ق.م", "خسوف قمر", "عين حورس في سقف دندرة",
         f"كلي، قدر {A(f'{D['l52'].umbral_mag:.2f}')}، مرئي من دندرة", "صحيح"),
        ("٧ مارس ٥١ ق.م", "كسوف شمس", "إيزيس والقرد في سقف دندرة",
         f"{KIND_AR[D['s51'].kind]}؛ جزئي {I.pct(s51['obscuration'] * 100, 0)} في دندرة", "صحيح"),
        ("ربيع الآخر ٣٦٩هـ", "خسوف قمر", "رصده ابن يونس",
         f"٦ نوفمبر ٩٧٩م، جزئي {A(f'{D['l979'].umbral_mag:.2f}')}", "صحيح"),
        ("شوال ٣٧٠هـ", "خسوف قمر", "رصده ابن يونس (الرواية: ١٠ شوال)",
         f"٢٢ أبريل ٩٨١م ({hijri_ar(D['l981'].jd_ut)})، جزئي {A(f'{D['l981'].umbral_mag:.2f}')} قبيل غروب القمر", "صحيح، واليوم ١٤ لا ١٠"),
        ("٢٠ أغسطس ٩٩٣م", "كسوف شمس كلي", "قبالة الساحل الشمالي، ٩٦٪ في القاهرة",
         f"كلي؛ {I.pct(s993['obscuration'] * 100, 0)} في القاهرة", "صحيح"),
        ("٧ أبريل ١٠٠٠م", "كسوف شمس", "جزئي نحو نصف القرص ضحى",
         f"{I.pct(s1000['obscuration'] * 100, 0)} في القاهرة ذروته {I.fmt_time(s1000['tmax'] + CAIRO[1] / 15, seconds=False)}", "صحيح"),
        ("١ مارس ١٠٠٢م", "خسوف قمر كلي", "رصده ابن يونس مع سيف (روائي)",
         f"كلي، قدر {A(f'{D['l1002'].umbral_mag:.2f}')}، مرئي من القاهرة", "صحيح"),
        ("٢٤ يناير ١٠٠٤م", "كسوف شمس هجين", "الشمس تغرب مكسوفة على القاهرة",
         f"{I.pct(s1004['obscuration'] * 100, 0)} عند الغروب", "صحيح"),
        ("١٣٧٧م", "كسوف شمس كلي", "آخر كلية فوق طيبة (الأقصر) قبل ٢٠٢٧", "يوافق جدول هذا الفصل", "صحيح"),
        ("٢ أغسطس ٢٠٢٧", "كسوف شمس كلي", "الأقصر ٦ د ٢٢ ث (١٣:٠٢:١٤–١٣:٠٨:٣٦)",
         "الأقصر ٦ د ٢٠ ث (١٣:٠١:٥٨–١٣:٠٨:١٨)", "قريب (فرق ثانيتين)"),
    ]
    H = 1.9 + 0.58 * len(rows)
    fig = page(9.4, H)
    ax = canvas(fig)
    header(fig, "كسوفات وخسوفات " + NOVEL + " بميزان الحساب",
           "الأحداث التي يصفها ملحق الرواية بأنها حقيقية، مقارنةً بحسابات هذا الكتاب")
    cols = [(0.965, "التاريخ"), (0.815, "الحدث"), (0.665, "في الرواية"), (0.395, "حسابنا"), (0.13, "الحكم")]
    top = 1 - 1.35 / H
    ax.add_patch(plt.Rectangle((0.02, top - 0.22 / H), 0.96, 0.44 / H, fc=NAVY, ec="none"))
    for x, c in cols:
        ax.text(x - 0.005, top, c, ha="right", va="center", fontsize=9.6, color="white", fontweight="bold")
    rh = 0.58 / H
    for i, row in enumerate(rows):
        yc = top - 0.22 / H - rh * (i + 0.5)
        ax.add_patch(plt.Rectangle((0.02, yc - rh / 2), 0.96, rh, fc="#f1efea" if i % 2 == 0 else "white", ec=LINE))
        widths = [16, 14, 30, 30, 16]
        for (x, _), txt, w in zip(cols, row, widths):
            col = GREEN if txt.startswith("صحيح") else (SUN_DEEP if txt.startswith(("ممكن", "قريب")) else INK)
            ax.text(x - 0.005, yc, wrap(txt, w), ha="right", va="center", fontsize=8.4, color=col, linespacing=1.25,
                    fontweight="bold" if x in (0.965, 0.13) else "normal")
    footer(fig, SRC + ". ما قبل ١٥٨٢ بالتقويم اليولياني؛ والهجري حسابي. الأحداث الروائية المتخيَّلة (الشخصيات والمنامات والنبوءات) مستبعدة.")
    save(fig, CH, "novel_eclipses_table", "الكسوفات والخسوفات الحقيقية في رواية «أرصاد وأطوار» مقارنةً بالحساب.")


def ancient_figures(D):
    fig_akhenaten(D["akh"])
    fig_dendera(D["s51"], D["l52"])


def fatimid_figures(D):
    fig_993(D["s993"])
    fig_1004(D["s1004"])
    fig_lunar_cairo(D["l979"], D["l981"], D["l1002"])
    fig_table(D)
