"""Photo -> monochrome self-typing ASCII SVG (SMIL, plays once, freezes)."""
from PIL import Image

SRC, DST = 'data/source-prepped.png', 'varun-ascii.svg'
COLS, CELL_W, CELL_H, FS = 110, 7, 12, 10
RAMP = " .`:-=+*cs#%@"
FILL, BG, ACCENT = '#d7dee6', '#0d1117', '#00ffdc'

img = Image.open(SRC).convert('L')
rows = max(20, round(COLS * (img.height / img.width) * (CELL_W / CELL_H)))
g = img.resize((COLS, rows), Image.LANCZOS)
px = g.load()
W, H = COLS * CELL_W, rows * CELL_H
STEP = 0.11  # stagger per row


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="monospace" font-size="{FS}">',
         f'<rect width="{W}" height="{H}" fill="{BG}" rx="10"/>', '<defs>']
for i in range(rows):
    lines.append(f'<clipPath id="r{i}"><rect x="0" y="{i * CELL_H}" width="0" height="{CELL_H}">'
                 f'<animate attributeName="width" from="0" to="{W}" dur="0.9s" begin="{i * STEP:.2f}s" fill="freeze"/></rect></clipPath>')
lines.append('</defs>')

for i in range(rows):
    y = i * CELL_H + CELL_H - 2
    chars = ''.join(RAMP[min(int((255 - px[x, i]) / 255 * len(RAMP)), len(RAMP) - 1)] for x in range(COLS))
    lines.append(f'<text x="4" y="{y}" fill="{FILL}" clip-path="url(#r{i})">{esc(chars)}</text>')
    # block cursor riding the wipe edge
    lines.append(f'<rect x="0" y="{i * CELL_H + 1}" width="7" height="{CELL_H - 2}" fill="{ACCENT}">'
                 f'<animate attributeName="x" from="0" to="{W}" dur="0.9s" begin="{i * STEP:.2f}s" fill="freeze"/>'
                 f'<animate attributeName="opacity" values="1;1;0" keyTimes="0;0.92;1" dur="{(rows - i) * STEP + 0.9:.2f}s" fill="freeze"/></rect>')

total = rows * STEP + 1.2
lines.append(f'<rect width="{W}" height="{H}" fill="none" stroke="#21262d" stroke-width="2" rx="10"/>')
lines.append('</svg>')
open(DST, 'w', encoding='utf-8').write('\n'.join(lines))
print(f'wrote {DST} ({COLS}x{rows}, ~{total:.1f}s)')
