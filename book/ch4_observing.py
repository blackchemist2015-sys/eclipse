"""Chapter 4 — observing the eclipse safely (Arabic infographics)."""
import numpy as np

import mapkit as MK
from common import (A, BLUE, BODY, CARD, Circ, GREEN, INK, INK2, LINE, MUTED, NAVY, ORANGE, PAPER, RED, SUN, SUN_DEEP,
                    TITLE, arabic_ticks, arrow, canvas, card, check_icon, corona, footer, halo, header, mirror_y,
                    moon_disk, number_badge, page, para, plt, save, style_axes, sun_disk, wrap, write_catalogue)
from eclipse2027 import besselian, circumstances as C, i18n as I

CH = 4
UTC = 3
B = besselian.compute()


def city(la, lo):
    r = C.local_circumstances(B, np.array([la]), np.array([lo]))
    return {k: float(np.ravel(v)[0]) for k, v in r.items()}


# ------------------------------------------------------------------ generic layouts
def list_card(title, sub, items, slug, caption, flags=None, dark=False, cols=1, h=None, width=None, note=None):
    """Numbered (or ✓/✗) cards laid out in columns; row heights follow the wrapped text."""
    width = width or int(66 / cols)
    wrapped = [wrap(t, width) for t in items]
    nl = [w.count("\n") + 1 for w in wrapped]
    rows = int(np.ceil(len(items) / cols))
    row_lines = [max(nl[r + c * rows] for c in range(cols) if r + c * rows < len(items)) for r in range(rows)]
    row_h = [0.30 + 0.24 * k for k in row_lines]   # inches
    H = 1.55 + sum(row_h) + 0.15 * rows + 0.45
    fig = page(7.6, H, NAVY if dark else PAPER)
    ax = canvas(fig)
    header(fig, title, sub, color="white" if dark else INK, sub_color="#c9d3e3" if dark else INK2)
    colw = 0.92 / cols
    y_top = 1 - 1.45 / H
    for r in range(rows):
        hgt = row_h[r] / H
        yc = y_top - hgt / 2
        for c in range(cols):
            i = r + c * rows
            if i >= len(items):
                continue
            x1 = 0.96 - c * colw
            card(ax, x1 - colw + 0.01, yc - hgt / 2, colw - 0.02, hgt, fc="#18294a" if dark else CARD,
                 ec="#2a3d5c" if dark else LINE)
            if flags is not None:
                check_icon(ax, x1 - 0.04, yc, s=0.022, ok=flags[i])
            else:
                number_badge(ax, x1 - 0.04, yc, i + 1, r=0.02)
            ax.text(x1 - 0.08, yc, wrapped[i], ha="right", va="center", fontsize=10.2,
                    color="white" if dark else INK, linespacing=1.45)
        y_top -= hgt + 0.15 / H
    if note:
        footer(fig, note, color="#8a96a8" if dark else MUTED)
    save(fig, CH, slug, caption)


# ------------------------------------------------------------------ figures
def fig_golden_rule():
    fig = page(7.6, 5.4, "#2a0d0b")
    ax = canvas(fig)
    sun_disk(ax, 0.5, 0.62, 0.11)
    ax.text(0.5, 0.62, "!", ha="center", va="center", fontsize=60, color="#2a0d0b", fontweight="bold",
            fontfamily=["DejaVu Sans"], zorder=6)
    ax.text(0.5, 0.34, "القاعدة الذهبية", ha="center", color=SUN, fontsize=22, fontweight="bold", fontfamily=TITLE)
    ax.text(0.5, 0.25, "لا تنظر إلى الشمس أبدًا بالعين المجردة أو عبر عدسة أو منظار\nإلا من خلال مرشّح شمسي معتمد",
            ha="center", va="top", color="white", fontsize=13, linespacing=1.6)
    ax.text(0.5, 0.05, "الاستثناء الوحيد: دقائق الكلية التامة داخل مسار الكسوف الكلي", ha="center", color="#ffb4a8",
            fontsize=10.5)
    save(fig, CH, "golden_rule", "القاعدة الذهبية لرصد الشمس بأمان.")


def fig_safe_unsafe():
    items = [("نظارة كسوف مطابقة للمعيار ISO 12312-2", True), ("زجاج لحام رقم ١٤ (أو ١٢ فأعلى)", True),
             ("الإسقاط بثقب صغير (كاميرا الثقب)", True), ("مرشّح شمسي معتمد مثبت على مقدمة المنظار", True),
             ("مشاهدة البث المباشر أو شاشة الكاميرا", True), ("النظارات الشمسية العادية مهما كانت داكنة", False),
             ("الزجاج المدخّن أو أفلام الأشعة السينية", False), ("الأقراص المدمجة وأفلام التصوير القديمة", False),
             ("المنظار أو التلسكوب دون مرشح أمامي", False), ("النظر عبر عدسة الكاميرا أو الهاتف المكبّرة", False)]
    list_card("آمن أم خطِر؟", "طرق رؤية الشمس الصحيحة والخاطئة", [t for t, _ in items], "safe_vs_unsafe",
              "مقارنة بين الوسائل الآمنة وغير الآمنة لمشاهدة الكسوف.", flags=[f for _, f in items], cols=2, h=6.2,
              note="ملاحظة: مرشحات العينية (التي تُركّب خلف العدسة عند العين) قد تتشقق من الحرارة — لا تستعملها.")


def fig_glasses_check():
    fig = page(7.6, 6.4)
    ax = canvas(fig)
    header(fig, "كيف تتأكد أن نظارتك آمنة؟", "افحص نظارة الكسوف قبل الحدث بأيام")
    # drawing of glasses
    for cx in (0.33, 0.62):
        ax.add_patch(plt.Rectangle((cx - 0.12, 0.62), 0.24, 0.13, fc="#151515", ec=INK, lw=2, transform=ax.transAxes))
    ax.plot([0.45, 0.50], [0.70, 0.70], color=INK, lw=3)
    ax.plot([0.21, 0.13], [0.72, 0.76], color=INK, lw=3)
    ax.plot([0.74, 0.82], [0.72, 0.76], color=INK, lw=3)
    ax.text(0.475, 0.58, "ISO 12312-2", ha="center", fontsize=11, fontweight="bold", color=INK2,
            fontfamily=["DejaVu Sans"])
    checks = ["علامة المعيار الدولي ISO 12312-2 مطبوعة على النظارة",
              "اسم الشركة المصنّعة وعنوانها واضحان",
              "لا خدوش ولا ثقوب ولا انفصال في الغشاء العاكس",
              "لا ترى من خلالها شيئًا داخل المنزل سوى مصباح ساطع جدًا يبدو خافتًا",
              "ترى الشمس من خلالها قرصًا مريحًا برتقاليًا أو أبيض دون إبهار",
              "تغطي العينين جيدًا ويمكن ارتداؤها فوق النظارة الطبية"]
    for i, c in enumerate(checks):
        y = 0.48 - i * 0.075
        check_icon(ax, 0.92, y, s=0.02, ok=True)
        ax.text(0.88, y, c, ha="right", va="center", fontsize=10.2)
    footer(fig, "إذا كانت النظارة مخدوشة أو قديمة أو مجهولة المصدر فاستبدلها. لا تشترِ إلا من مورد موثوق.")
    save(fig, CH, "glasses_checklist", "قائمة فحص نظارة الكسوف قبل الاستخدام.")


def fig_shade_numbers():
    shades = np.arange(5, 15)
    T = 10 ** (-(shades - 1) * 3 / 7)
    fig = page(8.4, 5.0)
    header(fig, "زجاج اللحام: أي رقم يكفي؟", "نفاذية الضوء المرئي حسب رقم ظل المرشح (مقياس لوغاريتمي)")
    ax = fig.add_axes([0.08, 0.13, 0.80, 0.64])
    cols = [GREEN if s >= 14 else (SUN_DEEP if s >= 12 else RED) for s in shades]
    ax.bar([A(s) for s in shades], T * 100, color=cols, width=0.65)
    ax.set_yscale("log")
    ax.set_ylabel("النسبة النافذة من الضوء (٪)")
    ax.set_xlabel("رقم ظل زجاج اللحام")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: A(f"{v:g}")))
    style_axes(ax)
    mirror_y(ax)
    ax.text(0.97, 0.92, "رقم ١٤: آمن ومريح\nرقم ١٢–١٣: آمن لكن الشمس ساطعة\nأقل من ١٢: غير آمن", transform=ax.transAxes,
            va="top", ha="right", fontsize=9.5, linespacing=1.6, bbox=dict(fc="white", ec=LINE))
    footer(fig, "النفاذية محسوبة من العلاقة المعيارية: رقم الظل = ١ + (٧/٣) لو(١/النفاذية).")
    save(fig, CH, "welding_shade_numbers", "نفاذية زجاج اللحام حسب رقم الظل وحد الأمان للرصد الشمسي (محسوبة).", "chart")


def fig_pinhole_steps():
    fig = page(8.6, 5.0)
    ax = canvas(fig)
    header(fig, "اصنع كاميرا ثقب في خمس دقائق", "أبسط طريقة آمنة لرؤية الكسوف: لا تنظر إلى الشمس بل إلى صورتها")
    steps = ["اثقب ورقة مقوّاة بدبوس ثقبًا صغيرًا نظيفًا", "قف وظهرك إلى الشمس", "أمسك الورقة فوق كتفك ليمر الضوء من الثقب",
             "ضع ورقة بيضاء على بعد متر تقريبًا", "شاهد صورة الشمس الهلالية على الورقة البيضاء"]
    for i, s in enumerate(steps):
        x = 0.88 - i * 0.19
        card(ax, x - 0.085, 0.20, 0.17, 0.52)
        number_badge(ax, x, 0.66, i + 1, r=0.025)
        ax.text(x, 0.50, wrap(s, 16), ha="center", va="center", fontsize=9.6, linespacing=1.5)
    sun = sun_disk(ax, 0.12, 0.33, 0.03, glow=False)
    moon_disk(ax, 0.135, 0.34, 0.03, color=CARD, clip=sun)
    footer(fig, "كلما ابتعدت الورقة البيضاء عن الثقب كبرت الصورة وخفت إضاءتها.")
    save(fig, CH, "pinhole_steps", "خطوات صنع كاميرا الثقب لمشاهدة الكسوف بأمان.")


def fig_pinhole_size():
    ts, eph = besselian.ephemeris()
    d = eph["earth"].at(ts.utc(2027, 8, 2, 10)).observe(eph["sun"]).distance().km
    ang = 2 * np.arcsin(696000 / d)
    D = np.linspace(0.2, 5, 100)
    fig = page(8.4, 5.0)
    header(fig, "حجم صورة الشمس في كاميرا الثقب", "قطر الصورة يساوي المسافة بين الثقب والشاشة مقسومة على نحو ١٠٩")
    ax = fig.add_axes([0.08, 0.17, 0.80, 0.59])
    ax.plot(D, D * ang * 1000, color=BLUE[9], lw=2.4)
    for dd in (1, 2, 3, 5):
        ax.plot(dd, dd * ang * 1000, "o", color=RED)
        ax.text(dd, dd * ang * 1000 + 2, A(f"{dd * ang * 1000:.0f}") + " مم", ha="center", fontsize=9.5)
    ax.set_xlabel("المسافة بين الثقب والشاشة (متر)")
    ax.set_ylabel("قطر صورة الشمس (مم)")
    style_axes(ax)
    arabic_ticks(ax)
    mirror_y(ax)
    footer(fig, f"القطر الظاهري للشمس يوم الكسوف = {A(f'{np.degrees(ang) * 60:.1f}')} دقيقة قوسية (محسوب).")
    save(fig, CH, "pinhole_image_size", "قطر صورة الشمس في كاميرا الثقب حسب المسافة (محسوب).", "chart")


def fig_natural_pinholes():
    fig = page(8.0, 5.0, "#2f3a24")
    ax = canvas(fig)
    header(fig, "كاميرات الثقب الطبيعية", "الفراغات بين أوراق الأشجار وثقوب المصفاة ترسم مئات الأهلّة على الأرض",
           color="white", sub_color="#d7e0c8")
    rng = np.random.default_rng(2)
    for _ in range(60):
        x, y = rng.uniform(0.05, 0.95), rng.uniform(0.06, 0.70)
        r = rng.uniform(0.012, 0.022)
        s = sun_disk(ax, x, y, r, glow=False, color="#f3dc8a")
        moon_disk(ax, x + r * 0.55, y + r * 0.2 * ax._asp, r, color="#2f3a24", clip=s)
    save(fig, CH, "natural_pinholes", "أهلّة الشمس المكسوفة تحت الأشجار: كاميرات ثقب طبيعية.")


def glasses_timeline(name, la, lo, slug):
    c = city(la, lo)
    tot = c["duration_s"] > 0
    fig = page(8.6, 4.4)
    ax = canvas(fig)
    header(fig, f"متى ترتدي النظارة في {name}؟", "الخط الزمني بتوقيت مصر الصيفي (محسوب)")
    t0, t1 = c["c1"] + UTC - 0.1, c["c4"] + UTC + 0.1

    def X(t):
        return 0.94 - (t - t0) / (t1 - t0) * 0.88

    y = 0.50
    ax.add_patch(plt.Rectangle((X(c["c4"] + UTC), y - 0.06), X(c["c1"] + UTC) - X(c["c4"] + UTC), 0.12, fc=ORANGE[3],
                               transform=ax.transAxes))
    if tot:
        w = max(X(c["c2"] + UTC) - X(c["c3"] + UTC), 0.035)
        xm = X((c["c2"] + c["c3"]) / 2 + UTC)
        ax.add_patch(plt.Rectangle((xm - w / 2, y - 0.10), w, 0.20, fc=NAVY, transform=ax.transAxes))
        ax.text(xm, y + 0.16, "انزع النظارة\n" + I.fmt_dur(c["duration_s"], long=True), ha="center", color=NAVY,
                fontsize=10, fontweight="bold")
        for tt, lab, ha in [(c["c2"], "التماس الثاني", "left"), (c["c3"], "التماس الثالث", "right")]:
            ax.text(X(tt + UTC) + (0.012 if ha == "left" else -0.012), y - 0.16, lab + "\n" + I.fmt_time(tt + UTC),
                    ha=ha, va="top", fontsize=8.5)
    ax.text(X((c["c1"] + c["c2"]) / 2 + UTC if tot else (c["c1"] + c["tmax"]) / 2 + UTC), y, "ارتدِ النظارة", ha="center",
            va="center", fontsize=11, fontweight="bold")
    ax.text(X((c["c3"] + c["c4"]) / 2 + UTC if tot else (c["tmax"] + c["c4"]) / 2 + UTC), y, "ارتدِ النظارة", ha="center",
            va="center", fontsize=11, fontweight="bold")
    for tt, lab in [(c["c1"], "بداية الكسوف"), (c["c4"], "نهاية الكسوف")]:
        ax.text(X(tt + UTC), y - 0.16, lab + "\n" + I.fmt_time(tt + UTC, seconds=False), ha="center", va="top", fontsize=8.5)
    if not tot:
        ax.text(0.5, 0.17, f"{name} خارج مسار الكلية (احتجاب {I.pct(c['obscuration'] * 100)}): لا تنزع النظارة في أي لحظة",
                ha="center", color=RED, fontsize=11, fontweight="bold")
    footer(fig, "المصدر: حسابات المؤلف من تقويم JPL DE421.")
    save(fig, CH, slug, f"الخط الزمني لارتداء نظارة الكسوف في {name} (محسوب).", "chart")


def fig_eye():
    fig = page(8.6, 5.0)
    ax = canvas(fig)
    header(fig, "لماذا يؤذي ضوء الشمس العين؟", "عدسة العين تركز ضوء الشمس على بقعة صغيرة من الشبكية")
    ax.add_patch(Circ(ax, (0.40, 0.50), 0.13, fc="white", ec=INK2, lw=2))
    ax.add_patch(plt.matplotlib.patches.Ellipse((0.53, 0.50), 0.025, 0.14, fc=BLUE[3], ec=INK2, transform=ax.transAxes))
    ax.plot([0.92, 0.535], [0.62, 0.55], color=SUN_DEEP, lw=1.5)
    ax.plot([0.92, 0.535], [0.38, 0.45], color=SUN_DEEP, lw=1.5)
    ax.plot([0.53, 0.272], [0.55, 0.50], color=SUN_DEEP, lw=1.5)
    ax.plot([0.53, 0.272], [0.45, 0.50], color=SUN_DEEP, lw=1.5)
    ax.add_patch(Circ(ax, (0.272, 0.50), 0.012, fc=RED, ec="none"))
    sun_disk(ax, 0.94, 0.50, 0.03)
    ax.text(0.53, 0.70, "العدسة", ha="center", fontsize=10)
    ax.text(0.20, 0.50, "الشبكية\n(بقعة الإبصار\nالمركزي)", ha="center", va="center", fontsize=9.5, color=RED)
    para(ax, 0.95, 0.23, "لا تحوي الشبكية مستقبلات للألم، فقد يحدث الضرر (اعتلال الشبكية الشمسي) دون أن تشعر به، "
         "وتظهر الأعراض بعد ساعات: بقعة عمياء أو تشوّش في وسط الرؤية، وقد يكون دائمًا.", width=78, size=9.8)
    save(fig, CH, "eye_damage", "كيف يسبب النظر إلى الشمس اعتلال الشبكية الشمسي.")


def fig_where_to_watch():
    lon0, lon1, lat0, lat1 = 24.5, 37.0, 21.7, 31.8
    fig = plt.figure(figsize=(7.6, 7.6), facecolor=PAPER)
    ax = fig.add_axes([0.04, 0.07, 0.86, 0.78])
    MK.base(ax, lon0, lon1, lat0, lat1, labels=False)
    MK.field(ax, B, lon0, lon1, lat0, lat1, n=320, obs_lines=False)
    MK.path(ax, B, -1.7, 1.95)
    picks = [("الأقصر", 25.6872, 32.6396, "معابد وفنادق ومطار"), ("سوهاج", 26.5591, 31.6957, "قرب خط المركز"),
             ("مرسى علم", 25.0676, 34.879, "ساحل البحر الأحمر"), ("برنيس", 23.9466, 35.474, "على خط المركز تقريبًا"),
             ("سيوة", 29.2032, 25.5195, "واحة في الصحراء الغربية")]
    for n, la, lo, why in picks:
        c = city(la, lo)
        ax.plot(lo, la, marker="*", ms=15, color=SUN, mec=INK, zorder=9)
        left = n in ("سوهاج", "برنيس")
        ax.annotate(f"{n}: {I.fmt_dur(c['duration_s'])}\n{why}", (lo, la), xytext=(-10 if left else 10, 2),
                    textcoords="offset points", ha="right" if left else "left", fontsize=9, path_effects=halo(), zorder=10)
    header(fig, "أين تشاهد الكلية في مصر؟", "مواقع مقترحة داخل المسار: مدة طويلة وخدمات وأفق مفتوح")
    footer(fig, "اختر موقعًا قريبًا من خط المركز (الخط الأحمر المتقطع) لتحصل على أطول مدة. الأرقام محسوبة.")
    save(fig, CH, "where_to_watch_egypt", "مواقع مقترحة لمشاهدة الكسوف الكلي في مصر ومدة الكلية فيها (محسوبة).", "map")


def fig_activity_sheet():
    fig = page(7.6, 9.4)
    ax = canvas(fig)
    header(fig, "ورقة رصد ميداني للطلاب", "سجّل الحرارة والإضاءة وسلوك الكائنات قبل الكلية وبعدها")
    cols = ["الوقت", "الحرارة (°م)", "الإضاءة / السماء", "ملاحظات (طيور، رياح، ظلال)"]
    xs = [0.95, 0.77, 0.60, 0.40]
    ax.text(0.95, 0.86, "المكان: ........................   التاريخ: ٢ أغسطس ٢٠٢٧   اسم الراصد: ........................",
            ha="right", fontsize=9.5)
    y0 = 0.80
    for x, c in zip(xs, cols):
        ax.text(x, y0, c, ha="right", fontsize=10, fontweight="bold", color=BLUE[10])
    times = ["قبل البداية بـ ١٥ د", "بداية الكسوف", "+٣٠ دقيقة", "+٦٠ دقيقة", "قبل الكلية بـ ١٠ د", "قبل الكلية بدقيقة",
             "منتصف الكلية", "بعد الكلية بدقيقة", "بعد الكلية بـ ١٠ د", "+٣٠ دقيقة", "نهاية الكسوف"]
    for i, tm in enumerate(times):
        y = y0 - 0.055 * (i + 1)
        ax.plot([0.04, 0.96], [y - 0.02, y - 0.02], color=LINE, lw=1)
        ax.text(0.95, y, tm, ha="right", va="center", fontsize=9.3, color=NAVY if "الكلية" in tm and "منتصف" in tm else INK)
    for x in [0.785, 0.615, 0.415]:
        ax.plot([x, x], [0.15, y0 + 0.02], color=LINE, lw=1)
    footer(fig, "تجربة مقترحة: ضع مقياس الحرارة في الظل، وسجّل القراءة في الأوقات المذكورة ثم ارسم منحنى التغير.")
    save(fig, CH, "student_observation_sheet", "نموذج ورقة رصد ميداني للطلاب أثناء الكسوف.")


def main():
    fig_golden_rule()
    fig_safe_unsafe()
    fig_glasses_check()
    fig_shade_numbers()
    fig_pinhole_steps()
    fig_pinhole_size()
    fig_natural_pinholes()
    fig_eye()
    glasses_timeline("الأقصر", 25.6872, 32.6396, "glasses_timeline_luxor")
    glasses_timeline("سوهاج", 26.5591, 31.6957, "glasses_timeline_sohag")
    glasses_timeline("القاهرة", 30.0444, 31.2357, "glasses_timeline_cairo")
    glasses_timeline("أسوان", 24.0889, 32.8998, "glasses_timeline_aswan")
    glasses_timeline("أسيوط", 27.1783, 31.1859, "glasses_timeline_asyut")
    glasses_timeline("الغردقة", 27.2579, 33.8116, "glasses_timeline_hurghada")
    list_card("خرافات وحقائق", "تصحيح مفاهيم شائعة عن الكسوف",
              ["خرافة: أشعة الكسوف أخطر من أشعة الشمس العادية. الحقيقة: الضوء نفسه، لكن الناس يحدّقون في الشمس أثناء الكسوف.",
               "خرافة: يمكن النظر حين تُحجب الشمس بنسبة ٩٩٪. الحقيقة: ١٪ من قرص الشمس أسطع من البدر بآلاف المرات.",
               "خرافة: الطعام يتسمم أثناء الكسوف. الحقيقة: لا يوجد أي أساس علمي لذلك.",
               "خرافة: النظارة الشمسية الداكنة تكفي. الحقيقة: تسمح بمرور ضوء يفوق الحد الآمن بآلاف المرات.",
               "خرافة: الكسوف يؤذي الحوامل والأجنة. الحقيقة: لا دليل علميًا على ذلك؛ الخطر الوحيد هو على العين.",
               "خرافة: لا خطر من النظر عبر الهاتف. الحقيقة: الشاشة آمنة للعين، لكن عدسة الهاتف قد تتضرر عند التكبير دون مرشح."],
              "myths_facts", "خرافات شائعة عن الكسوف وتصحيحها.", width=72)
    list_card("قائمة تجهيزات يوم الكسوف", "ما الذي تحمله معك؟",
              ["نظارة كسوف معتمدة لكل فرد + نظارة احتياطية", "قبعة واسعة ومظلة وواقٍ من الشمس", "ماء وفير (الحرارة قد تتجاوز ٤٠°م)",
               "ورقة بيضاء أو مصفاة مطبخ لإسقاط الأهلّة", "ساعة أو تطبيق بتنبيهات التماسات", "مقياس حرارة ودفتر ملاحظات",
               "كرسي قابل للطي أو حصيرة", "خطة للوصول مبكرًا وبديل عند الزحام"],
              "checklist_day", "قائمة التجهيزات المقترحة ليوم الكسوف.", cols=2, h=5.4)
    list_card("سلامة الأطفال والمدارس", "إرشادات للمعلمين وأولياء الأمور",
              ["درّب الأطفال على ارتداء النظارة قبل الحدث بأيام", "إشراف مباشر من شخص بالغ لكل مجموعة صغيرة",
               "ممنوع النظر عبر المناظير أو الكاميرات دون مرشح", "استخدم كاميرا الثقب والأهلّة تحت الأشجار للصغار جدًا",
               "اشرح متى يُسمح بنزع النظارة (داخل المسار فقط، أثناء الكلية فقط)", "رتّب أماكن ظليلة وماءً للشرب"],
              "children_safety", "إرشادات سلامة الأطفال والمدارس أثناء الكسوف.", h=5.8)
    list_card("الحر في صعيد مصر: سلامتك أولًا", "يقع الكسوف ظهرًا في أغسطس والشمس شبه عمودية",
              ["اشرب الماء بانتظام قبل أن تشعر بالعطش", "ارتدِ ملابس فاتحة واسعة وغطاء للرأس",
               "اجلس في الظل حتى قبيل الكلية بدقائق", "انتبه لعلامات ضربة الشمس: صداع ودوار وغثيان",
               "تجنب الوقوف الطويل على الأسطح الساخنة", "لا تترك الأطفال أو الهواتف والكاميرات في الشمس المباشرة"],
              "heat_safety", "إرشادات الوقاية من الحر أثناء متابعة الكسوف.", dark=True, h=5.6)
    fig_where_to_watch()
    fig_activity_sheet()
    list_card("المناظير والتلسكوبات", "قواعد استعمال الأجهزة البصرية",
              ["ركّب مرشحًا شمسيًا معتمدًا على مقدمة الجهاز (العدسة الأمامية) لا عند العين",
               "غطِّ المنظار الباحث الصغير أو انزعه", "لا تنظر عبر المنظار وأنت ترتدي نظارة الكسوف؛ المرشح الأمامي هو الحماية",
               "انزع المرشح الأمامي أثناء الكلية فقط، وأعده قبل ظهور الخاتم الماسي الثاني",
               "الإسقاط على ورقة بيضاء خلف التلسكوب ممكن، لكنه يسخّن أجزاء الجهاز: لا تتركه دون رقابة"],
              "optics_rules", "قواعد استعمال المناظير والتلسكوبات لرصد الشمس.", h=5.4)
    write_catalogue("ch4")


if __name__ == "__main__":
    main()
