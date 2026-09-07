"""Face-match audit: photo luminance vs rendered tone map (Pearson r + region check)."""
import re
import statistics
from PIL import Image

COLS = 132
img = Image.open('data/source-prepped.png').convert('L')
rows = max(20, round(COLS * (img.height / img.width) * (7 / 12)))
g = img.resize((COLS, rows), Image.LANCZOS)
src = list(g.getdata())

svg = open('varun-ascii.svg', encoding='utf-8').read()
spans = re.findall(r'<tspan class="t(\d)">(.*?)</tspan>', svg)
ren = []
for tone, cell in spans:
    ren.extend([int(tone)] * len(cell))
print('grid:', COLS, 'x', rows, '| rendered cells:', len(ren), '| expected:', COLS * rows)
assert len(ren) == COLS * rows, 'cell count mismatch'

ms, mr = statistics.mean(src), statistics.mean(ren)
cov = sum((a - ms) * (b - mr) for a, b in zip(src, ren))
r = cov / ((sum((a - ms) ** 2 for a in src) * sum((b - mr) ** 2 for b in ren)) ** 0.5)
print('Pearson r (photo vs render):', round(r, 4))


def region(x0, x1, y0, y1):
    return statistics.mean(ren[y * COLS + x]
                           for y in range(int(rows * y0), int(rows * y1))
                           for x in range(int(COLS * x0), int(COLS * x1)))


center = region(.33, .67, .25, .75)
corners = (region(0, .2, 0, .2) + region(.8, 1, 0, .2) + region(0, .2, .8, 1) + region(.8, 1, .8, 1)) / 4
print('center tone:', round(center, 2), '| corner tone:', round(corners, 2))
print('FACE MATCH:', 'PASS' if r > 0.9 and abs(center - corners) > 0.5 else 'FAIL')
