"""Chapter 9 (book order: 6) — introductory science experiments for the eclipse."""
import numpy as np

from common import (A, BLUE, BODY, CARD, Circ, GREEN, INK, INK2, LINE, MUTED, NAVY, ORANGE, PAPER, RED, SUN, SUN_DEEP,
                    TITLE, arabic_ticks, canvas, card, footer, header, mirror_y, number_badge, page, plt, save,
                    style_axes, sun_disk, moon_disk, wrap, write_catalogue)
from eclipse2027 import besselian, circumstances as C, i18n as I

CH = 9
UTC = 3
B = besselian.compute()

EXPERIMENTS = [
    dict(slug="pinhole_crescents", title="أهلّة تحت الشجرة", level="ابتدائي", time="١٥ دقيقة",
         tools=["ورق مقوّى ودبوس", "مصفاة مطبخ", "ورقة بيضاء كبيرة"],
         steps=["اصنع ثقوبًا صغيرة بأشكال مختلفة (دائرة، مثلث، مربع)", "أسقط ضوء الشمس عبرها على الورقة البيضاء قبل الكسوف",
                "كرر ذلك كل عشر دقائق أثناء الكسوف الجزئي", "ارسم شكل البقع المضيئة في كل مرة"],
         observe="مهما كان شكل الثقب تظهر صورة الشمس دائرية، ثم هلالية أثناء الكسوف.",
         why="الثقب الصغير يعمل عمل العدسة: كل نقطة من قرص الشمس ترسم بقعة، فتتكوّن صورة الشمس نفسها لا صورة الثقب."),
    dict(slug="temperature_drop", title="هل تبرد الأرض أثناء الكسوف؟", level="إعدادي", time="ثلاث ساعات",
         tools=["مقياس حرارة رقمي في الظل", "ساعة", "ورقة الرصد (الفصل الخامس)"],
         steps=["ثبّت المقياس في الظل على ارتفاع متر عن الأرض", "سجّل القراءة كل خمس دقائق من قبل البداية بنصف ساعة",
                "زِد التسجيل إلى كل دقيقة حول الكلية", "ارسم منحنى الحرارة مع الزمن"],
         observe="تنخفض الحرارة تدريجيًا وتبلغ أدناها بعد ذروة الكسوف بدقائق.",
         why="يقل الإشعاع الشمسي الواصل فتفقد الأرض والهواء الحرارة؛ والتأخر يرجع إلى السعة الحرارية للأرض."),
    dict(slug="light_meter", title="منحنى الضوء بالهاتف", level="إعدادي", time="ثلاث ساعات",
         tools=["هاتف بتطبيق مقياس الإضاءة (Lux meter)", "حامل ثابت يوجّه الهاتف نحو السماء"],
         steps=["ثبّت الهاتف بحيث يواجه حساسه السماء دون أن تقع عليه ظلال", "سجّل شدة الإضاءة كل دقيقتين",
                "قارن قراءاتك بالمنحنى المحسوب لمدينتك", "احسب نسبة الإضاءة إلى قراءة ما قبل الكسوف"],
         observe="تنخفض الإضاءة ببطء أولًا ثم بسرعة شديدة في الدقائق الأخيرة قبل الكلية.",
         why="الضوء يتناسب تقريبًا مع مساحة القرص الظاهرة، والهلال الرفيع يختفي بسرعة."),
    dict(slug="sharp_shadows", title="الظلال تزداد حدة", level="ابتدائي", time="١٠ دقائق",
         tools=["قلم أو مسطرة", "ورقة بيضاء"],
         steps=["أمسك القلم فوق الورقة وانظر إلى ظله قبل الكسوف", "كرر ذلك حين يصبح الهلال رفيعًا",
                "قارن حواف الظل في الاتجاهين المتعامدين"],
         observe="يصبح الظل حادًا جدًا في اتجاه، ومشوّشًا في الاتجاه الآخر.",
         why="مصدر الضوء صار هلالًا رفيعًا بدل قرص كامل، فالظل حاد عبر عرض الهلال ومشوّش على طوله."),
    dict(slug="shadow_bands", title="اصطياد الأحزمة الظلية", level="ثانوي", time="٥ دقائق حول الكلية",
         tools=["ملاءة بيضاء كبيرة على الأرض", "هاتف للتصوير بالفيديو", "عصا متر لقياس المسافات"],
         steps=["افرش الملاءة على أرض مستوية قبل الكلية", "صوّر الملاءة بالفيديو قبل التماس الثاني بدقيقتين",
                "قدّر اتجاه حركة الخطوط والمسافة بينها", "كرر بعد التماس الثالث"],
         observe="خطوط باهتة متموجة تتحرك على الملاءة، تفصلها بضعة سنتيمترات.",
         why="اضطراب الهواء في الغلاف الجوي يركّز ويشتّت ضوء الهلال الرفيع، كما يحدث لوميض النجوم."),
    dict(slug="animal_behavior", title="الطيور والحيوانات", level="ابتدائي", time="ساعة",
         tools=["دفتر ملاحظات", "منظار عادي (للطيور فقط، لا للشمس)"],
         steps=["اختر مكانًا فيه طيور أو حيوانات أليفة", "سجّل سلوكها قبل الكسوف بنصف ساعة",
                "سجّل أي تغير حين تخفت الإضاءة", "قارن ملاحظاتك بملاحظات زملائك"],
         observe="قد تصمت الطيور وتعود إلى أعشاشها، وتتصرف بعض الحيوانات كأن المساء حلّ.",
         why="كثير من الكائنات تضبط سلوكها على شدة الضوء لا على الساعة."),
    dict(slug="timing_contacts", title="هل صدق الحساب؟", level="ثانوي", time="ثلاث ساعات",
         tools=["ساعة مضبوطة على التوقيت الدقيق", "نظارة كسوف", "بطاقة مدينتك (الفصل الرابع)"],
         steps=["اكتب الأوقات المحسوبة للتماسات في مدينتك", "راقب بالنظارة لحظة أول «عضة» في قرص الشمس",
                "سجّل الوقت بالثانية، وكذلك نهاية الكسوف", "احسب الفرق بين الرصد والحساب"],
         observe="يتطابق الرصد والحساب في حدود ثوانٍ قليلة.",
         why="حركة الشمس والقمر معروفة بدقة عالية؛ والفروق الصغيرة سببها تضاريس حافة القمر ورد فعل الراصد."),
    dict(slug="sun_size", title="قِس قطر الشمس بكاميرا الثقب", level="ثانوي", time="٢٠ دقيقة",
         tools=["صندوق طويل أو أنبوب", "ورق ألومنيوم ودبوس", "مسطرة بالمليمتر"],
         steps=["اصنع ثقبًا في طرف الأنبوب وثبّت ورقة بيضاء في الطرف الآخر", "قِس طول الأنبوب L وقطر صورة الشمس d",
                "احسب القطر الزاوي = d ÷ L", "اضربه في بعد الشمس (١٤٩٫٦ مليون كم) لتحصل على قطرها"],
         observe="تحصل على نسبة قريبة من ١ إلى ١٠٩.",
         why="المثلثان المتشابهان: قطر الشمس إلى بعدها يساوي قطر الصورة إلى طول الأنبوب."),
]


def experiment_card(e, k):
    fig = page(7.6, 8.4)
    ax = canvas(fig)
    header(fig, f"تجربة {A(k)}: {e['title']}", f"المستوى: {e['level']} | المدة: {e['time']}")
    y = 0.85
    tb = 0.075 + 0.04 * len(e["tools"])
    card(ax, 0.04, y - tb, 0.92, tb - 0.005, fc="#eef4fc", ec="none")
    ax.text(0.94, y - 0.025, "الأدوات", ha="right", fontsize=12, fontweight="bold", color=NAVY, fontfamily=TITLE)
    for i, t in enumerate(e["tools"]):
        ax.text(0.92, y - 0.07 - i * 0.04, "• " + t, ha="right", fontsize=10.5)
    y -= tb + 0.045
    ax.text(0.94, y, "الخطوات", ha="right", fontsize=12, fontweight="bold", color=NAVY, fontfamily=TITLE)
    for i, t in enumerate(e["steps"]):
        yy = y - 0.05 - i * 0.052
        number_badge(ax, 0.93, yy, i + 1, r=0.018)
        ax.text(0.89, yy, wrap(t, 84), ha="right", va="center", fontsize=10.4, linespacing=1.35)
    y = y - 0.075 - len(e["steps"]) * 0.052
    for lab, txt, col, fc in [("ماذا تلاحظ؟", e["observe"], GREEN, "#e9f5ee"), ("التفسير العلمي", e["why"], BLUE[10], "#f1efea")]:
        lines = wrap(txt, 86).count("\n") + 1
        h = 0.075 + 0.036 * lines
        card(ax, 0.04, y - h, 0.92, h, fc=fc, ec="none")
        ax.text(0.94, y - 0.025, lab, ha="right", fontsize=11.5, fontweight="bold", color=col, fontfamily=TITLE)
        ax.text(0.94, y - 0.055, wrap(txt, 86), ha="right", va="top", fontsize=10.2, linespacing=1.45)
        y -= h + 0.025
    ax.text(0.5, 0.012, "تذكير: لا تنظر إلى الشمس مباشرة إلا بنظارة كسوف معتمدة.", ha="center", fontsize=9.5, color=RED,
            fontweight="bold")
    save(fig, CH, "exp_" + e["slug"], f"تجربة للمستوى التمهيدي: {e['title']}.")


def fig_scale_model():
    fig = page(8.6, 5.0)
    ax = canvas(fig)
    header(fig, "نموذج الكسوف في الفصل", "بكرة وحبة حمص ومصباح: نموذج بمقياس رسم حقيقي")
    earth_cm = 2.0
    scale = earth_cm / 12742
    rows = [("الأرض", 12742, "كرة قطرها " + A("2") + " سم"),
            ("القمر", 3475, f"حبة قطرها {A(f'{3475 * scale * 10:.1f}')} مم"),
            ("المسافة إلى القمر", 384400, f"{A(f'{384400 * scale:.0f}')} سم"),
            ("الشمس", 1392700, f"كرة قطرها {A(f'{1392700 * scale / 100:.1f}')} م"),
            ("المسافة إلى الشمس", 149.6e6, f"{A(f'{149.6e6 * scale / 100:.0f}')} م")]
    for i, (n, km, v) in enumerate(rows):
        y = 0.72 - i * 0.11
        card(ax, 0.30, y - 0.04, 0.66, 0.08)
        ax.text(0.94, y, n, ha="right", va="center", fontsize=11, fontweight="bold")
        ax.text(0.62, y, v, ha="right", va="center", fontsize=11, color=NAVY)
    ax.add_patch(Circ(ax, (0.20, 0.55), 0.04, fc="#3987e5"))
    ax.add_patch(Circ(ax, (0.08, 0.55), 0.011, fc="#9aa6b8"))
    ax.text(0.20, 0.45, "الأرض", ha="center", fontsize=9)
    ax.text(0.08, 0.45, "القمر", ha="center", fontsize=9)
    footer(fig, "كل سنتيمتر في النموذج يمثل نحو " + A(f"{1 / scale:,.0f}") + " كم (محسوب). أسقط ظل الحبة على الكرة بمصباح بعيد لترى بقعة الظل الصغيرة.")
    save(fig, CH, "scale_model", "أبعاد نموذج الكسوف بمقياس رسم حقيقي للاستخدام في الفصل (محسوب).")


def fig_predicted_light(name="الأقصر", la=25.6872, lo=32.6396):
    t = np.linspace(8.5, 11.6, 400)
    ob = np.array([float(C.instant(B, tt - besselian.T0_UT_HOURS, [la], [lo])["obscuration"][0]) for tt in t])
    fig = page(8.4, 5.0)
    header(fig, f"المنحنى المتوقع لتجربة الضوء في {name}", "قارن قراءات هاتفك بهذا المنحنى المحسوب (نسبة الضوء إلى ما قبل الكسوف)")
    ax = fig.add_axes([0.08, 0.14, 0.80, 0.62])
    ax.plot(t + UTC, (1 - ob) * 100, color=NAVY, lw=2.2)
    ax.fill_between(t + UTC, 0, (1 - ob) * 100, color=BLUE[1], alpha=0.6)
    for tt, lab in [(11.75, "سجّل كل ٥ دقائق"), (12.85, "كل دقيقة"), (13.4, "كل ٥ دقائق")]:
        ax.text(tt, 104, lab, ha="center", fontsize=9, color=INK2)
    ax.set_ylim(0, 112)
    xt = np.arange(11.5, 14.76, 0.5)
    ax.set_xticks(xt)
    ax.set_xticklabels([I.fmt_time(x, seconds=False) for x in xt])
    ax.set_ylabel("الضوء المتبقي (٪)")
    style_axes(ax)
    arabic_ticks(ax, x=False)
    mirror_y(ax)
    footer(fig, "المصدر: حسابات المؤلف من تقويم JPL DE421؛ الإضاءة الحقيقية أثناء الكلية ليست صفرًا تمامًا بسبب ضوء الأفق.")
    save(fig, CH, "predicted_light_curve", f"منحنى الضوء المتوقع في {name} لمقارنته بقياسات الطلاب (محسوب).", "chart")


def main():
    for k, e in enumerate(EXPERIMENTS, 1):
        experiment_card(e, k)
    fig_scale_model()
    fig_predicted_light()
    write_catalogue("ch9")


if __name__ == "__main__":
    main()
