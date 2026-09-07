"""data/contributions.json -> animated contrib-heatmap.svg (plays once, freezes)."""
import json
from datetime import date

IN, OUT = 'data/contributions.json', 'contrib-heatmap.svg'
PALETTE = ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353', '#69f0a0']
CELL, GAP, TOP, LEFT = 11, 3, 34, 30

d = json.load(open(IN))
days = sorted(d['days'], key=lambda x: x['date'])
# chunk into Sunday-start week columns (GitHub layout)
weeks, col = [], []
for x in days:
    wd = date.fromisoformat(x['date']).weekday()  # Mon=0
    sun = (wd + 1) % 7
    if sun == 0 and col:
        weeks.append(col)
        col = []
    col.append((sun, x))
if col:
    weeks.append(col)
weeks = weeks[-53:]
W = LEFT + len(weeks) * (CELL + GAP) + 8
H = TOP + 7 * (CELL + GAP) + 52

L = ['<?xml version="1.0" encoding="UTF-8"?>',
     f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="monospace">',
     '<style>rect.day{animation:drop .5s both}@keyframes drop{from{opacity:0;transform:translateY(-9px)}to{opacity:1;transform:translateY(0)}}</style>',
     f'<rect width="{W}" height="{H}" fill="#0d1117" rx="10"/>',
     f'<text x="{LEFT}" y="20" font-size="13" fill="#7d8590">{d["total"]:,} contributions in the last year</text>']
for ci, wk in enumerate(weeks):
    for sun, x in wk:
        px, py = LEFT + ci * (CELL + GAP), TOP + sun * (CELL + GAP)
        delay = (ci + sun) * 0.035
        L.append(f'<rect class="day" x="{px}" y="{py}" width="{CELL}" height="{CELL}" rx="2.5" '
                 f'fill="{PALETTE[min(x["level"], 5)]}" style="animation-delay:{delay:.2f}s"><title>{x["date"]}: {x["count"]}</title></rect>')

fy = TOP + 7 * (CELL + GAP) + 22
L.append(f'<text x="{LEFT}" y="{fy}" font-size="11" fill="#7d8590">Less</text>')
for i, c in enumerate(PALETTE[:6]):
    L.append(f'<rect x="{LEFT + 38 + i * 15}" y="{fy - 9}" width="11" height="11" rx="2.5" fill="{c}"/>')
L.append(f'<text x="{LEFT + 38 + 6 * 15 + 6}" y="{fy}" font-size="11" fill="#7d8590">More</text>')
L.append(f'<text x="{W - LEFT}" y="{fy}" font-size="11" fill="#7d8590" text-anchor="end">streak {d["current_streak"]}d · longest {d["longest_streak"]}d · best {d["best_day"]["count"]} on {d["best_day"]["date"]}</text>')
L.append(f'<rect width="{W}" height="{H}" fill="none" stroke="#21262d" stroke-width="2" rx="10"/>')
L.append('</svg>')
open(OUT, 'w', encoding='utf-8').write('\n'.join(L))
print(f'wrote {OUT} ({len(weeks)} weeks)')
