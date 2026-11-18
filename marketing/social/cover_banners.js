// Profile cover banners for LinkedIn and X/Twitter, in the brand banner's design: a maroon field with a faint
// diamond pattern and gold hairlines, the gold "KALA KARI / CREATIONS" wordmark with its diamond divider, the
// tagline, "LUCKNOW · JAIPUR · KUTCH", the shipping/WhatsApp line, and the jharokha emblem on the right.
//
// Each size keeps its bottom-left corner clear, because the profile photo or page logo sits over it.
//
// Usage:  node cover_banners.js <out-dir> <fonts-dir>      (fonts-dir holds fontsource-cinzel, -cormorant-garamond)
// Uses brand/logo/defs.svgfrag for the emblem.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');

const OUT = process.argv[2], FONTS = process.argv[3];
const defs = fs.readFileSync(path.join(__dirname, '..', '..', 'brand', 'logo', 'defs.svgfrag'), 'utf8')
  // a deep-maroon niche inside the arch, as on the brand banner
  .replace(/(<symbol id="emblem"[^>]*>)/, '$1<path d="M -56 152 V 62 C -56 22 -26 8 -9 -4 C -3 -9 0 -18 0 -30 C 0 -18 3 -9 9 -4 C 26 8 56 22 56 62 V 152 Z" fill="#5C1E2E"/>');
const f = (fam, file) => 'data:font/woff2;base64,' +
  fs.readFileSync(path.join(FONTS, `fontsource-${fam}`, 'package', 'files', file)).toString('base64');
const fontCss = `
@font-face{font-family:Cinzel;font-weight:600;src:url(${f('cinzel', 'cinzel-latin-600-normal.woff2')})}
@font-face{font-family:Corm;font-weight:600;src:url(${f('cormorant-garamond', 'cormorant-garamond-latin-600-normal.woff2')})}
@font-face{font-family:Corm;font-weight:500;src:url(${f('cormorant-garamond', 'cormorant-garamond-latin-500-normal.woff2')})}
@font-face{font-family:Corm;font-weight:500;font-style:italic;src:url(${f('cormorant-garamond', 'cormorant-garamond-latin-500-italic.woff2')})}`;

// k = type scale; cx = centre of the text block; em = emblem box [x, y, height]; lines = y of the gold hairlines;
// rows = which text rows to show and their baselines
const SIZES = {
  'linkedin-profile-cover-1584x396': {
    w: 1584, h: 396, k: 0.68, cx: 900, top: 114, em: [1285, 62, 272], lines: [34, 362],
    rows: ['word', 'div', 'sub', 'tag', 'cities', 'ship'],
  },
  'x-twitter-header-1500x500': {
    w: 1500, h: 500, k: 0.80, cx: 790, top: 152, em: [1175, 100, 312], lines: [62, 438],
    rows: ['word', 'div', 'sub', 'tag', 'cities', 'ship'],
  },
  'linkedin-company-cover-1128x191': {
    w: 1128, h: 191, k: 0.50, cx: 585, top: 66, em: [905, 24, 144], lines: [12, 179],
    rows: ['word', 'div', 'sub', 'tagcities'],
  },
};

function svgFor(s) {
  const [ex, ey, eh] = s.em;
  const ew = eh * 160 / 248;
  return `<svg id="b" xmlns="http://www.w3.org/2000/svg" width="${s.w}" height="${s.h}" viewBox="0 0 ${s.w} ${s.h}">
  ${defs}
  <defs>
    <radialGradient id="bg" cx="0.5" cy="0.5" r="0.75">
      <stop offset="0" stop-color="#7A2D3D"/><stop offset="0.7" stop-color="#6E2837"/><stop offset="1" stop-color="#5A202D"/>
    </radialGradient>
    <linearGradient id="goldtext" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#E2C88A"/><stop offset="0.55" stop-color="#C9A45E"/><stop offset="1" stop-color="#9C7838"/>
    </linearGradient>
    <pattern id="dia" width="64" height="64" patternUnits="userSpaceOnUse">
      <path d="M 32 26 L 35 32 L 32 38 L 29 32 Z" fill="#ffffff" fill-opacity="0.045"/>
      <path d="M 0 -6 L 3 0 L 0 6 L -3 0 Z M 64 58 L 67 64 L 64 70 L 61 64 Z M 0 58 L 3 64 L 0 70 L -3 64 Z M 64 -6 L 67 0 L 64 6 L 61 0 Z" fill="#ffffff" fill-opacity="0.045"/>
    </pattern>
  </defs>
  <rect width="${s.w}" height="${s.h}" fill="url(#bg)"/>
  <rect width="${s.w}" height="${s.h}" fill="url(#dia)"/>
  ${s.lines.map(y => `<rect x="0" y="${y}" width="${s.w}" height="${Math.max(1, s.h / 400)}" fill="#B08A4C" fill-opacity="0.8"/>`).join('')}
  <use href="#emblem" x="${ex}" y="${ey}" width="${ew}" height="${eh}" style="--mono:#F7F2E9"/>
  <g id="t"></g>
</svg>`;
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  for (const scale of [1, 2]) {
    const page = await browser.newPage({ deviceScaleFactor: scale });
    for (const [name, s] of Object.entries(SIZES)) {
      await page.setViewportSize({ width: s.w, height: s.h });
      await page.setContent(`<!doctype html><html><head><style>${fontCss} html,body{margin:0} svg{display:block}</style></head><body>${svgFor(s)}</body></html>`);
      await page.evaluate(() => document.fonts.ready);
      await page.evaluate((s) => {
        const ns = 'http://www.w3.org/2000/svg', g = document.getElementById('t'), k = s.k;
        const el = (tag, a, txt) => { const e = document.createElementNS(ns, tag); for (const n in a) e.setAttribute(n, a[n]); if (txt) e.textContent = txt; g.appendChild(e); return e; };
        // centred text; letter-spacing leaves trailing space after the last glyph, so shift by half of it
        const ctext = (txt, y, a) => {
          const e = el('text', Object.assign({ x: s.cx, y, 'text-anchor': 'middle' }, a), txt);
          const ls = parseFloat(a['letter-spacing'] || 0);
          e.setAttribute('x', s.cx + ls / 2);
          return e;
        };
        let y = s.top;
        const rows = s.rows;
        // wordmark
        const word = ctext('KALA KARI', y, { 'font-family': 'Cinzel', 'font-weight': 600, 'font-size': 118 * k, 'letter-spacing': 10 * k, fill: 'url(#goldtext)' });
        const wb = word.getBBox(), wls = 10 * k;
        const left = wb.x, right = wb.x + wb.width - wls, mid = (left + right) / 2;
        // divider: two gold rules and a diamond, under the wordmark
        const dy = y + 44 * k;
        el('rect', { x: left + 0.12 * (right - left), y: dy - 1.2 * k, width: (mid - left) * 0.88 - 26 * k, height: 2.4 * k, fill: '#C9A45E' });
        el('rect', { x: mid + 26 * k, y: dy - 1.2 * k, width: (right - mid) * 0.88 - 26 * k, height: 2.4 * k, fill: '#C9A45E' });
        el('path', { d: `M ${mid} ${dy - 12 * k} L ${mid + 12 * k} ${dy} L ${mid} ${dy + 12 * k} L ${mid - 12 * k} ${dy} Z`, fill: '#D3B06A' });
        y = dy + 62 * k;
        ctext('CREATIONS', y, { 'font-family': 'Corm', 'font-weight': 600, 'font-size': 46 * k, 'letter-spacing': 38 * k, fill: '#D1AE68' });
        if (rows.includes('tag')) {
          y += 80 * k;
          ctext('Handcrafted ethnic wear from three craft homes', y, { 'font-family': 'Corm', 'font-style': 'italic', 'font-weight': 500, 'font-size': 46 * k, fill: '#F7F2E9' });
          y += 70 * k;
          ctext('LUCKNOW · JAIPUR · KUTCH', y, { 'font-family': 'Corm', 'font-weight': 600, 'font-size': 42 * k, 'letter-spacing': 8 * k, fill: '#D1AE68' });
          y += 72 * k;
          ctext('Pan-India shipping · WhatsApp +91 94081 14592', y, { 'font-family': 'Corm', 'font-weight': 500, 'font-size': 36 * k, fill: '#F2E9DA' });
        } else {
          y += 76 * k;
          ctext('Handcrafted ethnic wear from three craft homes · Lucknow · Jaipur · Kutch', y,
                { 'font-family': 'Corm', 'font-style': 'italic', 'font-weight': 500, 'font-size': 44 * k, fill: '#F7F2E9' });
        }
      }, s);
      const file = path.join(OUT, name + (scale === 2 ? '@2x' : '') + '.png');
      await page.locator('#b').screenshot({ path: file });
      console.log(file);
    }
    await page.close();
  }
  await browser.close();
})();
