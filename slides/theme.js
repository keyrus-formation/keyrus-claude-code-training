// Shared look for the 4 half-day decks. Neutral navy/teal palette (official Keyrus template not available here).
// shortcut: no official Keyrus template/logo, swap THEME colors and add the logo in the layouts when available.
const pptxgen = require("pptxgenjs");

const THEME = {
  name: "Keyrus Claude Code Training",
  headFontFace: "Calibri",
  bodyFontFace: "Calibri",
  colors: { dk1: "1B1F3B", lt1: "FFFFFF", dk2: "0B1F4D", lt2: "EEF2F8", accent1: "0B1F4D", accent2: "00A3A1", accent3: "F59E0B", accent4: "6366F1", accent5: "10B981", accent6: "EF4444", hlink: "00A3A1", folHlink: "6366F1" },
};

function newDeck(title) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.33" x 7.5"
  pres.title = title;
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;
  pres.defineSlideMaster({
    title: "CONTENT", background: { color: "FFFFFF" },
    slideNumber: { x: 12.4, y: 7.0, w: 0.6, h: 0.3, fontSize: 10, color: "6B7280" },
    objects: [{ text: { text: "Claude Code for Data Consultants", options: { x: 0.6, y: 7.0, w: 6, h: 0.3, fontSize: 10, color: "6B7280", margin: 0, isTextBox: true } } }],
    // Pass { placeholder: "title" } to addText: position and style come from here.
    slideNumberOnly: false,
  });
  pres.defineSlideMaster({ title: "DARK", background: { color: THEME.colors.dk2 } });
  return { pres, C };
}

// Helpers: every slide gets a title (same position everywhere) and speaker notes.
const T = { x: 0.6, y: 0.4, w: 12.1, h: 0.9, fontSize: 32, bold: true, color: THEME.colors.dk2, margin: 0, isTextBox: true, fontFace: "Calibri" };

function contentSlide(pres, title, notes) {
  const s = pres.addSlide({ masterName: "CONTENT" });
  s.addText(title, { ...T });
  if (notes) s.addNotes(notes);
  return s;
}
function darkSlide(pres, title, subtitle, notes) {
  const s = pres.addSlide({ masterName: "DARK" });
  s.addText(title, { x: 0.8, y: 2.4, w: 11.7, h: 1.4, fontSize: 44, bold: true, color: "FFFFFF", margin: 0, isTextBox: true, fontFace: "Calibri" });
  if (subtitle) s.addText(subtitle, { x: 0.8, y: 3.9, w: 11.7, h: 1.0, fontSize: 22, color: "CBD5E1", margin: 0, isTextBox: true, fontFace: "Calibri" });
  if (notes) s.addNotes(notes);
  return s;
}
// n cards in a row: [{head, body}]
function cards(pres, s, items, y = 1.7, h = 4.6) {
  const gap = 0.3, w = (12.1 - gap * (items.length - 1)) / items.length;
  items.forEach((it, i) => {
    const x = 0.6 + i * (w + gap);
    s.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: THEME.colors.lt2 }, line: { color: THEME.colors.lt2 }, rectRadius: 0.1 });
    s.addText(String(i + 1), { x: x + 0.25, y: y + 0.25, w: 0.55, h: 0.55, shape: pres.ShapeType.ellipse, fill: { color: THEME.colors.accent2 }, color: "FFFFFF", bold: true, fontSize: 18, align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText(it.head, { x: x + 0.25, y: y + 0.95, w: w - 0.5, h: 0.8, fontSize: 20, bold: true, color: THEME.colors.dk2, margin: 0, valign: "top", isTextBox: true });
    s.addText(it.body, { x: x + 0.25, y: y + 1.8, w: w - 0.5, h: h - 2.0, fontSize: 16, color: THEME.colors.dk1, margin: 0, valign: "top", isTextBox: true });
  });
}
// Big stat callouts: [{value, label}]
function stats(pres, s, items, y = 2.2) {
  const w = 12.1 / items.length;
  items.forEach((it, i) => {
    s.addText(it.value, { x: 0.6 + i * w, y, w: w - 0.2, h: 1.4, fontSize: 60, bold: true, color: THEME.colors.accent2, margin: 0, isTextBox: true });
    s.addText(it.label, { x: 0.6 + i * w, y: y + 1.5, w: w - 0.2, h: 1.2, fontSize: 16, color: THEME.colors.dk1, margin: 0, valign: "top", isTextBox: true });
  });
}
// Left-aligned bullet list in a box
function bullets(s, items, opts = {}) {
  s.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1, paraSpaceAfter: 8 } })),
    { x: 0.6, y: 1.6, w: 12.1, h: 5.0, fontSize: 18, color: THEME.colors.dk1, valign: "top", margin: 0, isTextBox: true, ...opts });
}

module.exports = { THEME, newDeck, contentSlide, darkSlide, cards, stats, bullets };
