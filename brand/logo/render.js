const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const OUT = process.argv[2], FONTS = process.argv[3];
const defs = fs.readFileSync(path.join(OUT, 'defs.svgfrag'), 'utf8');
const f = (p) => 'data:font/woff2;base64,' + fs.readFileSync(path.join(FONTS, p)).toString('base64');
const fontCss = `
@font-face{font-family:Cinzel;font-weight:600;src:url(${f('cinzel/package/files/cinzel-latin-600-normal.woff2')})}
@font-face{font-family:Cinzel;font-weight:700;src:url(${f('cinzel/package/files/cinzel-latin-700-normal.woff2')})}
@font-face{font-family:Cormorant;font-weight:600;src:url(${f('cormorant-garamond/package/files/cormorant-garamond-latin-600-normal.woff2')})}`;

const MAROON = '#752C39', GOLDTXT = '#8A6630', CREAM = '#F7F2E9', LIGHTGOLD = '#D9BC79';

// Each variant: svg body + a layout fn run in-page to size the viewBox
const variants = {
  'kalakari-logo-horizontal': { word: MAROON, sub: GOLDTXT, mono: MAROON, layout: 'h' },
  'kalakari-logo-horizontal-inverse': { word: CREAM, sub: LIGHTGOLD, mono: CREAM, layout: 'h' },
  'kalakari-logo-stacked': { word: MAROON, sub: GOLDTXT, mono: MAROON, layout: 's' },
  'kalakari-favicon': { mono: CREAM, layout: 'f' },
};

function body(v) {
  if (v.layout === 'h') return `
    <use href="#emblem" x="4" y="4" width="88" height="136"/>
    <text id="w" x="116" y="74" font-family="Cinzel" font-weight="600" font-size="56" letter-spacing="5" fill="${v.word}">KALA KARI</text>
    <g id="d" fill="url(#gold)"></g>
    <text id="s" y="124" font-family="Cormorant" font-weight="600" font-size="23" letter-spacing="11" fill="${v.sub}" text-anchor="middle">CREATIONS</text>`;
  if (v.layout === 's') return `
    <use href="#emblem" x="190" y="10" width="140" height="216"/>
    <text id="w" x="260" y="300" text-anchor="middle" font-family="Cinzel" font-weight="600" font-size="62" letter-spacing="6" fill="${v.word}">KALA KARI</text>
    <g id="d" fill="url(#gold)"></g>
    <text id="s" x="260" y="356" font-family="Cormorant" font-weight="600" font-size="26" letter-spacing="13" fill="${v.sub}" text-anchor="middle">CREATIONS</text>`;
  return `
    <rect x="0" y="0" width="512" height="512" rx="96" fill="${MAROON}"/>
    <rect x="18" y="18" width="476" height="476" rx="80" fill="none" stroke="url(#gold)" stroke-width="5"/>
    <g transform="translate(256 0)" font-family="Cinzel" font-weight="700" font-size="300" fill="url(#gold)">
      <text x="-41" y="362">K</text>
      <text x="-41" y="362" transform="scale(-1,1)">K</text>
    </g>
    <path d="M 256 398 L 270 412 L 256 426 L 242 412 Z" fill="url(#gold)"/>
    <rect x="150" y="410" width="80" height="4" fill="url(#gold)"/>
    <rect x="282" y="410" width="80" height="4" fill="url(#gold)"/>`;
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 1 });
  for (const [name, v] of Object.entries(variants)) {
    const html = `<!doctype html><html><head><style>${fontCss} html,body{margin:0;background:transparent} svg{display:block}</style></head>
      <body><svg id="logo" xmlns="http://www.w3.org/2000/svg" style="--mono:${v.mono}" viewBox="0 0 520 380">${defs}${body(v)}</svg></body></html>`;
    await page.setContent(html);
    await page.evaluate(() => document.fonts.ready);
    const vb = await page.evaluate((layout) => {
      const svg = document.getElementById('logo');
      const ns = 'http://www.w3.org/2000/svg';
      const w = document.getElementById('w'), s = document.getElementById('s'), d = document.getElementById('d');
      if (layout === 'f') return [0, 0, 512, 512];
      // letter-spacing adds trailing space after last glyph; trim it from centre maths
      const ls = parseFloat(w.getAttribute('letter-spacing'));
      const wb = w.getBBox();
      const cx = wb.x + (wb.width - ls) / 2;
      const left = wb.x, right = wb.x + wb.width - ls;
      const sls = parseFloat(s.getAttribute('letter-spacing'));
      s.setAttribute('x', cx + sls / 2);
      const dy = layout === 'h' ? 94 : 322;
      const mk = (tag, attrs) => { const e = document.createElementNS(ns, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); d.appendChild(e); };
      mk('rect', { x: left + 2, y: dy - 0.8, width: cx - left - 14, height: 1.6 });
      mk('rect', { x: cx + 12, y: dy - 0.8, width: right - cx - 14, height: 1.6 });
      mk('path', { d: `M ${cx} ${dy - 6} L ${cx + 6} ${dy} L ${cx} ${dy + 6} L ${cx - 6} ${dy} Z` });
      mk('circle', { cx: left + 2, cy: dy, r: 2.2 });
      mk('circle', { cx: right - 2, cy: dy, r: 2.2 });
      const bb = svg.getBBox();
      const pad = 6;
      return [Math.floor(bb.x - pad), Math.floor(bb.y - pad), Math.ceil(bb.width + 2 * pad), Math.ceil(bb.height + 2 * pad)];
    }, v.layout);
    await page.evaluate((vb) => {
      const svg = document.getElementById('logo');
      svg.setAttribute('viewBox', vb.join(' '));
      svg.setAttribute('width', vb[2]); svg.setAttribute('height', vb[3]);
    }, vb);
    // standalone SVG with embedded fonts
    const svgText = await page.evaluate((css) => {
      const svg = document.getElementById('logo').cloneNode(true);
      const st = document.createElementNS('http://www.w3.org/2000/svg', 'style');
      st.textContent = css; svg.insertBefore(st, svg.firstChild);
      return new XMLSerializer().serializeToString(svg);
    }, fontCss);
    fs.writeFileSync(path.join(OUT, name + '.svg'), svgText);
    // PNG at high resolution
    const target = v.layout === 'f' ? 512 : (v.layout === 'h' ? 300 : 1200);
    const scale = v.layout === 's' ? target / vb[2] : target / vb[3];
    await page.setViewportSize({ width: Math.ceil(vb[2] * scale) + 4, height: Math.ceil(vb[3] * scale) + 4 });
    await page.evaluate(([vb, sc]) => {
      const svg = document.getElementById('logo');
      svg.setAttribute('width', vb[2] * sc); svg.setAttribute('height', vb[3] * sc);
    }, [vb, scale]);
    await page.locator('#logo').screenshot({ path: path.join(OUT, name + '.png'), omitBackground: true });
    console.log(name, 'viewBox', vb.join(' '));
  }
  await browser.close();
})();
