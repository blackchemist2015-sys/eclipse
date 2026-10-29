const plain = (c) => Array.isArray(c) ? c.map((x) => (typeof x === "string" ? x : (x.text || (Array.isArray(x) ? x[0] : "")))).join("") : String(c);
// Build the Arabic (RTL) Word edition of the eclipse book from book/word/manuscript_img.json.
// Usage: node book/make_docx.js <manuscript_img.json> <output.docx>
const fs = require("fs");
const path = require("path");
const {
  AlignmentType, BorderStyle, Document, Footer, Header, HeadingLevel, ImageRun, LevelFormat, NumberFormat,
  PageBreak, PageNumber, PageOrientation, Packer, Paragraph, ShadingType, Table, TableCell, TableOfContents,
  TableRow, TextRun, WidthType,
} = require("docx");

const [, , specPath, outPath] = process.argv;
const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));
const ROOT = path.resolve(path.dirname(specPath), "..", "..");

const BODY = "Simplified Arabic";
const HEAD = "Arial";
const NAVY = "0D366B";
const MUTED = "6B6A65";
const PAGE_W = 11906, PAGE_H = 16838, MARGIN = 1247;          // A4, 2.2 cm margins
const TEXT_W = PAGE_W - 2 * MARGIN;                            // 9412 DXA ≈ 16.6 cm
const PX_PER_DXA = 96 / 1440;

const font = (name) => ({ ascii: name, hAnsi: name, cs: name, eastAsia: name });

function run(text, o = {}) {
  return new TextRun({
    text, rightToLeft: true, font: font(o.font || BODY), size: o.size || 26, sizeComplexScript: o.size || 26,
    bold: !!o.bold, boldComplexScript: !!o.bold, italics: !!o.italic, italicsComplexScript: !!o.italic,
    color: o.color,
  });
}

function enRun(text, o = {}) {
  return new TextRun({ text, rightToLeft: false, font: font("Arial"), size: Math.round((o.size || 26) * 0.82),
    sizeComplexScript: Math.round((o.size || 26) * 0.82), italics: true, color: o.enColor || "355C8C" });
}

// Arabic text or [[text, isEnglish], ...] segments → runs
function runs(t, o = {}) {
  if (typeof t === "string") return [run(t, o)];
  return t.map(([txt, en]) => (en ? enRun(txt, o) : run(txt, o)));
}

function para(text, o = {}) {
  return new Paragraph({
    bidirectional: true,
    alignment: o.align || AlignmentType.JUSTIFIED,
    spacing: { before: o.before ?? 0, after: o.after ?? 160, line: o.line || 340 },
    keepNext: !!o.keepNext,
    heading: o.heading,
    pageBreakBefore: !!o.pageBreakBefore,
    border: o.border,
    shading: o.shading,
    indent: o.indent,
    children: Array.isArray(text) && text.length && text[0] instanceof TextRun ? text : runs(text, o),
  });
}

function figure(it, brk = false) {
  const maxW = TEXT_W * PX_PER_DXA;              // px at 96 dpi
  const maxH = 21.5 / 2.54 * 96;                  // 21.5 cm
  let w = maxW, h = maxW * it.h / it.w;
  if (h > maxH) { h = maxH; w = maxH * it.w / it.h; }
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER, keepNext: true, pageBreakBefore: brk, spacing: { before: 200, after: 80 },
      children: [new ImageRun({ type: "jpg", data: fs.readFileSync(it.jpg), transformation: { width: Math.round(w), height: Math.round(h) },
        altText: { title: "شكل " + it.number, description: plain(it.caption).replace(/&/g, "و").replace(/[<>"]/g, ""), name: "fig" + it.number } })],
    }),
    para([run("شكل " + it.number + ": ", { bold: true, size: 20, color: NAVY, font: HEAD }), ...runs(it.caption, { size: 20, color: MUTED })],
      { align: AlignmentType.CENTER, after: 280 }),
  ];
}

function cell(text, width, o = {}) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: o.fill ? { fill: o.fill, type: ShadingType.CLEAR, color: "auto" } : undefined,
    margins: { top: 40, bottom: 40, left: 60, right: 60 },
    children: [/[A-Za-z]/.test(text) && !/[\u0600-\u06FF]/.test(text)
      ? new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 0, line: 260 },
          children: [new TextRun({ text, font: font("Arial"), size: o.size || 17, sizeComplexScript: o.size || 17, bold: !!o.bold, color: o.color })] })
      : para(text, { align: AlignmentType.CENTER, after: 0, line: 260, size: o.size || 17, bold: o.bold,
          color: o.color, font: o.bold ? HEAD : BODY })],
  });
}

function table(header, rows, widths, size) {
  const border = { style: BorderStyle.SINGLE, size: 4, color: "D9D6CE" };
  const total = widths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: total, type: WidthType.DXA }, columnWidths: widths, visuallyRightToLeft: true,
    borders: { top: border, bottom: border, left: border, right: border, insideHorizontal: border, insideVertical: border },
    rows: [
      new TableRow({ tableHeader: true, children: header.map((h, i) => cell(h, widths[i], { fill: "DCE8F7", bold: true, size, color: NAVY })) }),
      ...rows.map((r, k) => new TableRow({ cantSplit: true,
        children: r.map((v, i) => cell(v, widths[i], { fill: k % 2 ? "F6F4EF" : undefined, size, bold: i === 0 })) })),
    ],
  });
}

const header = new Header({ children: [para(spec.title + " — ٢ أغسطس ٢٠٢٧", { align: AlignmentType.CENTER, size: 16, color: MUTED, after: 0,
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "E88A2C", space: 4 } } })] });
const footer = new Footer({
  children: [new Paragraph({ alignment: AlignmentType.CENTER, bidirectional: true,
    children: [new TextRun({ children: [PageNumber.CURRENT], font: font(BODY), size: 18, sizeComplexScript: 18, color: MUTED })] })],
});
const pageProps = (landscape) => ({
  page: { size: { width: PAGE_W, height: PAGE_H, orientation: landscape ? PageOrientation.LANDSCAPE : PageOrientation.PORTRAIT },
    margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN, header: 600, footer: 600 },
    pageNumbers: { formatType: NumberFormat.HINDI_NUMBERS } },
});

// ---------------------------------------------------------------- cover (full-page designed image)
const coverImg = path.join(ROOT, "book", "word", "cover_full.jpg");
const cover = [
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 0 }, children: [new ImageRun({ type: "jpg",
    data: fs.readFileSync(coverImg), transformation: { width: 776, height: 1094 },
    altText: { title: "الغلاف", description: "هالة الشمس أثناء الكسوف الكلي وعنوان الكتاب", name: "cover" } })] }),
];
const coverProps = { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: 0, bottom: 0, left: 0, right: 0, header: 0, footer: 0 } } };

// ---------------------------------------------------------------- front matter
const front = [
  para("ملاحظات حول هذا الكتاب", { size: 30, bold: true, font: HEAD, color: NAVY, after: 240 }),
  ...spec.notes.map((t) => para(t, { size: 22, after: 120 })),
  new Paragraph({ children: [new PageBreak()] }),
  para("المحتويات", { size: 36, bold: true, font: HEAD, color: NAVY, align: AlignmentType.CENTER, after: 300 }),
  new TableOfContents("المحتويات", { hyperlink: true, headingStyleRange: "1-2" }),
  new Paragraph({ children: [new PageBreak()] }),
];
for (const [kind, text] of spec.front) {
  if (kind === "h1") front.push(para(text, { heading: HeadingLevel.HEADING_1, size: 40, bold: true, font: HEAD, color: NAVY, after: 300 }));
  else if (kind === "h2") front.push(para(text, { heading: HeadingLevel.HEADING_2, size: 30, bold: true, font: HEAD, color: NAVY, before: 240 }));
  else if (kind === "warn") front.push(para(text, { bold: true, color: "B3261E", size: 26, before: 200,
    border: { right: { style: BorderStyle.SINGLE, size: 24, color: "B3261E", space: 8 } }, shading: { fill: "FDECEA", type: ShadingType.CLEAR, color: "auto" } }));
  else front.push(para(text));
}

// ---------------------------------------------------------------- chapters
const chapterChildren = [];
const GOLD = "E88A2C";
const toAr = (n) => String(n).replace(/\d/g, (d) => "٠١٢٣٤٥٦٧٨٩"[d]);
spec.chapters.forEach((ch, idx) => {
  // ---- opener page: banner image, big number, title, intro box, "in this chapter"
  const bw = TEXT_W * PX_PER_DXA;
  chapterChildren.push(new Paragraph({ alignment: AlignmentType.CENTER, pageBreakBefore: true, spacing: { before: 0, after: 240 },
    children: [new ImageRun({ type: "jpg", data: fs.readFileSync(ch.hero), transformation: { width: Math.round(bw), height: Math.round(bw / 2) },
      altText: { title: ch.name, description: "صورة افتتاحية للفصل", name: "hero" + idx } })] }));
  chapterChildren.push(para(ch.src === 11 ? "ملحق" : toAr(ch.num), { size: ch.src === 11 ? 56 : 96, bold: true, font: HEAD, color: GOLD,
    align: AlignmentType.CENTER, before: 480, after: 0, line: 360 }));
  chapterChildren.push(para(ch.label, { size: 24, color: MUTED, align: AlignmentType.CENTER, before: 200, after: 60, font: HEAD }));
  chapterChildren.push(para(ch.name, { heading: HeadingLevel.HEADING_1, size: 48, bold: true, font: HEAD, color: NAVY,
    align: AlignmentType.CENTER, after: 240,
    border: { bottom: { style: BorderStyle.SINGLE, size: 18, color: GOLD, space: 10 } } }));
  ch.intro.forEach((t) => chapterChildren.push(para(t, { size: 24, line: 330, after: 100,
    shading: { fill: "EEF4FC", type: ShadingType.CLEAR, color: "auto" },
    border: { right: { style: BorderStyle.SINGLE, size: 30, color: NAVY, space: 10 } }, indent: { left: 200 } })));
  if (ch.sections.length) {
    chapterChildren.push(para("في هذا الفصل", { size: 26, bold: true, font: HEAD, color: GOLD, before: 240, after: 80 }));
    ch.sections.forEach((h) => chapterChildren.push(para([run("◆  ", { size: 20, color: GOLD }), run(h, { size: 22, color: NAVY })],
      { after: 30, align: AlignmentType.RIGHT })));
  }
  // ---- content
  let first = true;
  for (const it of ch.items) {
    if (it.type === "h2") chapterChildren.push(para(it.text, { heading: HeadingLevel.HEADING_2, size: 32, bold: true, font: HEAD, color: NAVY,
      before: 360, after: 160, keepNext: true, pageBreakBefore: first,
      border: { right: { style: BorderStyle.SINGLE, size: 36, color: GOLD, space: 8 } },
      shading: { fill: "F4F1EA", type: ShadingType.CLEAR, color: "auto" } }));
    else if (it.type === "p") chapterChildren.push(para(it.text, { keepNext: false, pageBreakBefore: first }));
    else {
      chapterChildren.push(...figure(it, first));
    }
    first = false;
  }
});

// ---------------------------------------------------------------- appendices
const appendixPortrait = [
  para("الملاحق", { heading: HeadingLevel.HEADING_1, size: 52, bold: true, font: HEAD, color: NAVY, align: AlignmentType.CENTER,
    pageBreakBefore: true, before: 2400, after: 600 }),
  para("ملحق ب: مدن مختارة في الدول الأخرى", { heading: HeadingLevel.HEADING_2, size: 32, bold: true, font: HEAD, color: NAVY, after: 160 }),
  para("وقت الذروة بالتوقيت المحلي لكل دولة، ومدة الكلية أو نسبة الاحتجاب.", { size: 22 }),
  table(["الدولة", "المدينة", "الذروة (محلي)", "المنطقة الزمنية", "مدة الكلية", "الاحتجاب"], spec.other_table,
    [1700, 2000, 1500, 1500, 1400, 1300], 18),
  para("ملحق ج: مسرد المصطلحات", { heading: HeadingLevel.HEADING_2, size: 32, bold: true, font: HEAD, color: NAVY, before: 400, after: 160, pageBreakBefore: true }),
  table(["المصطلح", "Term", "المعنى"], spec.glossary3, [2200, 2400, 4800], 19),
  para("ملحق د: المصادر والمنهجية", { heading: HeadingLevel.HEADING_2, size: 32, bold: true, font: HEAD, color: NAVY, before: 400, after: 160, pageBreakBefore: true }),
  ...spec.method.map((t) => para(t, { size: 22 })),
  ...spec.sources.map((t, i) => para([run(String(i + 1).replace(/\d/g, (d) => "٠١٢٣٤٥٦٧٨٩"[d]) + ". ", { size: 22, bold: true }),
    run(t, { size: 22 })], { after: 100, align: AlignmentType.RIGHT })),
];
const appendixLandscape = [
  para("ملحق أ: جدول مواعيد الكسوف في المدن المصرية", { heading: HeadingLevel.HEADING_2, size: 32, bold: true, font: HEAD, color: NAVY, after: 120 }),
  para("بتوقيت مصر الصيفي (التوقيت العالمي +٣)، مرتبة حسب مدة الكلية ثم نسبة الاحتجاب. الشرطة (—) تعني أن المدينة خارج مسار الكلية.", { size: 22 }),
  table(["المدينة", "المحافظة", "بداية الكسوف", "بداية الكلية", "الذروة", "نهاية الكلية", "نهاية الكسوف", "مدة الكلية", "الاحتجاب", "ارتفاع الشمس"],
    spec.egypt_table, [1800, 1600, 1400, 1400, 1400, 1400, 1400, 1400, 1200, 1200], 17),
];

const doc = new Document({
  creator: "Eclipse 2027 book project", title: spec.title, description: spec.subtitle,
  features: { updateFields: true },
  styles: {
    default: { document: { run: { font: font(BODY), size: 26, sizeComplexScript: 26 }, paragraph: { bidirectional: true } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: font(HEAD), size: 52, bold: true, color: NAVY }, paragraph: { outlineLevel: 0, spacing: { after: 400 } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: font(HEAD), size: 32, bold: true, color: NAVY }, paragraph: { outlineLevel: 1, spacing: { before: 300, after: 160 } } },
    ],
  },
  numbering: { config: [{ reference: "src", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.START,
    style: { paragraph: { indent: { start: 500, hanging: 360 } } } }] }] },
  sections: [
    { properties: coverProps, children: cover },
    { properties: pageProps(false), headers: { default: header }, footers: { default: footer }, children: [...front, ...chapterChildren] },
    { properties: pageProps(true), headers: { default: header }, footers: { default: footer }, children: appendixLandscape },
    { properties: pageProps(false), headers: { default: header }, footers: { default: footer }, children: appendixPortrait },
  ],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(outPath, buf); console.log("wrote", outPath, (buf.length / 1e6).toFixed(1), "MB"); });
