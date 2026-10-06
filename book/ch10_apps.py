"""Chapter 10 (book order: after photography) — apps and tools for planning, observing and photographing."""
from common import (A, BLUE, BODY, CARD, GREEN, INK, INK2, LINE, MUTED, NAVY, PAPER, RED, SUN_DEEP, TITLE, canvas,
                    card, footer, header, number_badge, page, plt, save, wrap, write_catalogue)

CH = 10
LRI, PDI = "⁦", "⁩"

APPS = [
    ("الخرائط والتخطيط", BLUE[9], [
        ("X. Jubier eclipse maps", "خرائط تفاعلية تعطي مواعيد الكسوف لأي نقطة تضغط عليها", "متصفح"),
        ("NASA Eclipse Website", "خرائط وجداول رسمية لكل كسوف", "متصفح"),
        ("timeanddate.com", "مواعيد مبسطة لكل مدينة ورسوم متحركة للمسار", "متصفح وتطبيق"),
        ("Google Earth", "استكشاف موقع الرصد والأفق قبل السفر", "متصفح وتطبيق")]),
    ("السماء والفلك", "#7a4fc2", [
        ("Stellarium", "قبة سماوية مجانية تعرض الكسوف وموقع الكواكب", "حاسوب وهاتف"),
        ("SkySafari", "خريطة سماء متقدمة ومحاكاة للكسوف", "iOS / Android"),
        ("Sky Guide", "خريطة سماء سهلة الاستعمال", "iOS"),
        ("Star Walk 2", "تعرّف على النجوم والكواكب بتوجيه الهاتف", "iOS / Android")]),
    ("تخطيط التصوير", SUN_DEEP, [
        ("PhotoPills", "مخطِّط للتصوير يعرض موقع الشمس ومسار الكسوف", "iOS / Android"),
        ("The Photographer's Ephemeris", "اتجاه الشمس وظلالها فوق الخريطة", "متصفح وتطبيق"),
        ("Sun Surveyor", "الواقع المعزز لموقع الشمس في السماء", "iOS / Android")]),
    ("التوقيت والأتمتة", GREEN, [
        ("Solar Eclipse Timer", "عدّ تنازلي صوتي للتماسات حسب موقعك", "iOS / Android"),
        ("Eclipse Orchestrator", "تحكم آلي في الكاميرا أثناء الكسوف", "Windows"),
        ("Solar Eclipse Maestro", "تحكم آلي في الكاميرا أثناء الكسوف", "macOS")]),
    ("الطقس", "#6d6d68", [
        ("Windy", "خرائط السحب والرياح والتوقعات", "متصفح وتطبيق"),
        ("Clear Outside", "توقعات صفاء السماء للرصد الفلكي", "متصفح وتطبيق"),
        ("الهيئة العامة للأرصاد الجوية المصرية", "النشرات الرسمية لمصر", "متصفح")]),
]


def fig_apps():
    rows = sum(len(a[2]) + 1 for a in APPS)
    H = 1.6 + rows * 0.34
    fig = page(8.6, H)
    ax = canvas(fig)
    header(fig, "تطبيقات ومواقع مفيدة", "لتخطيط الرصد والتصوير يوم ٢ أغسطس ٢٠٢٧")
    y = 1 - 1.45 / H
    step = 0.34 / H
    for cat, col, items in APPS:
        ax.add_patch(plt.Rectangle((0.04, y - step * 0.42), 0.92, step * 0.84, fc=col, ec="none", transform=ax.transAxes))
        ax.text(0.94, y, cat, ha="right", va="center", color="white", fontsize=11.5, fontweight="bold", fontfamily=TITLE)
        y -= step
        for name, what, plat in items:
            ax.plot([0.04, 0.96], [y - step / 2, y - step / 2], color=LINE, lw=0.8)
            ax.text(0.94, y, what, ha="right", va="center", fontsize=9.8)
            ax.text(0.06, y, LRI + name + PDI, ha="left", va="center", fontsize=10, fontweight="bold",
                    fontfamily=["DejaVu Sans", "Noto Sans Arabic"], color=col)
            ax.text(0.47, y, plat, ha="center", va="center", fontsize=8.8, color=MUTED)
            y -= step
    footer(fig, "الأسماء للإرشاد فقط ولا تمثل ترويجًا؛ تتغير التطبيقات وأسعارها وتوافرها، فتحقق منها قبل الاعتماد عليها.")
    save(fig, CH, "useful_apps", "تطبيقات ومواقع مفيدة لتخطيط رصد الكسوف وتصويره.")


def fig_planning():
    steps = [("قبل ١٢ شهرًا", "اختر موقعك داخل المسار واحجز الإقامة والمواصلات"),
             ("قبل ٦ أشهر", "اشترِ نظارات الكسوف والمرشحات من مورد موثوق"),
             ("قبل ٣ أشهر", "جرّب المعدات والتطبيقات، واصنع كاميرا الثقب"),
             ("قبل شهر", "تدرّب على خطة التصوير في التوقيت نفسه من اليوم"),
             ("قبل أسبوع", "راقب توقعات الطقس واستعد بموقع بديل"),
             ("قبل يوم", "اشحن البطاريات وجهّز الماء والقبعات وزامن الساعات"),
             ("يوم الكسوف", "صل مبكرًا، ارتدِ النظارة، واستمتع بالكلية بعينيك"),
             ("بعد الكسوف", "شارك صورك وقياساتك، واحتفظ بالنظارات لكسوفات قادمة")]
    fig = page(7.6, 8.8)
    ax = canvas(fig)
    header(fig, "الطريق إلى يوم الكسوف", "جدول تخطيط مقترح للأفراد والمدارس والمجموعات")
    top, bot = 0.84, 0.07
    st = (top - bot) / (len(steps) - 1)
    ax.plot([0.70, 0.70], [bot, top], color=LINE, lw=3)
    for i, (w, t) in enumerate(steps):
        y = top - i * st
        number_badge(ax, 0.70, y, i + 1, color=RED if "يوم الكسوف" == w else BLUE[8], r=0.022)
        ax.text(0.95, y, w, ha="right", va="center", fontsize=11, fontweight="bold", color=NAVY, fontfamily=TITLE)
        ax.text(0.66, y, wrap(t, 46), ha="right", va="center", fontsize=10.4, linespacing=1.4)
    save(fig, CH, "planning_timeline", "جدول زمني مقترح للاستعداد لكسوف ٢٠٢٧.")


def main():
    fig_apps()
    fig_planning()
    write_catalogue("ch10")


if __name__ == "__main__":
    main()
