"""Real photo -> 3D-embossed duotone portrait SVG (static, SMIL-safe). Overwrites varun-ascii.svg."""
from PIL import Image, ImageDraw

SRC, DST = 'data/source-prepped.png', 'varun-ascii.svg'
COLS, CELL_W, CELL_H, FS = 132, 7, 12, 10
RAMP = " .`:-=+*cs#%@"
TONES = ['#1a120b', '#4a2f1d', '#7a4a24', '#b87333', '#e09a4e', '#ffd479', '#a8f0e4', '#e6fffa']
BG, ACCENT = '#0d1117', '#00ffdc'

img = Image.open(SRC).convert('L')
rows = max(20, round(COLS * (img.height / img.width) * (CELL_W / CELL_H)))
g = img.resize((COLS, rows), Image.LANCZOS)
px = g.load()
# radial vignette: melt photo edges into card bg so the subject glows center
cx, cy, maxd = (COLS - 1) / 2, (rows - 1) / 2, ((COLS / 2) ** 2 + (rows / 2) ** 2) ** 0.5
lum = [[min(255, px[x, y] + 200 * (((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 / maxd) ** 2) for x in range(COLS)] for y in range(rows)]
W, H = COLS * CELL_W, rows * CELL_H


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def runs(y):
    out, start, tone = [], 0, int(lum[y][0] / 256 * 8)
    for x in range(1, COLS):
        t = int(lum[y][x] / 256 * 8)
        if t != tone:
            out.append((start, x, tone))
            start, tone = x, t
    out.append((start, COLS, tone))
    return out


L = ['<?xml version="1.0" encoding="UTF-8"?>',
     f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="monospace" font-size="{FS}">',
     '<defs>' + ''.join(f'<style>.t{i}{{fill:{c}}}</style>' for i, c in enumerate(TONES)) +
     '<filter id="ds" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000" flood-opacity="0.6"/></filter>'
     f'<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0.10"/>'
     f'<stop offset="0.5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="{ACCENT}" stop-opacity="0.08"/></linearGradient></defs>',
     f'<rect width="{W}" height="{H}" fill="{BG}" rx="12"/>',
     f'<g filter="url(#ds)" opacity="0.85" transform="translate(3,4)">']
for y in range(rows):
    L.append(f'<text x="4" y="{y * CELL_H + CELL_H - 2}" fill="#000">' +
             ''.join(esc(RAMP[7] * (e - s)) for s, e, _ in runs(y)) + '</text>')
L.append('</g>')
for y in range(rows):
    yv = y * CELL_H + CELL_H - 2
    L.append('<text x="4" y="%d">%s</text>' % (yv, ''.join(
        '<tspan class="t%d">%s</tspan>' % (t, esc(''.join(RAMP[min(int(lum[y][x] / 256 * len(RAMP)), len(RAMP) - 1)] for x in range(s, e))))
        for s, e, t in runs(y))))
L += [f'<rect width="{W}" height="{H}" fill="url(#sheen)" rx="12" opacity="0.6"/>',
      f'<rect width="{W}" height="{H}" fill="none" stroke="#21262d" stroke-width="3" rx="12"/>',
      f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" fill="none" stroke="{ACCENT}" stroke-opacity="0.35" rx="8"/>',
      '</svg>']
open(DST, 'w', encoding='utf-8').write('\n'.join(L))
print(f'wrote {DST} ({COLS}x{rows})')
