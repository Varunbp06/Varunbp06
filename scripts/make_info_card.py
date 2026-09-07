"""Neofetch-style info card SVG for Varun B P (SMIL stagger, freezes)."""
import os

DST = 'info-card.svg'
STATIC = os.environ.get('STATIC') == '1'
W, LH, X0, Y0 = 490, 30, 22, 78
KEY, VAL, DIM, ACC = '#00ffdc', '#e6edf3', '#7d8590', '#39d353'

rows = [
    ('varun@github', '─────────────', True),
    ('Name', 'Varun B P — AI/ML Engineer'),
    ('Based', 'Nelamangala, Karnataka, India'),
    ('Degree', 'B.E. AI & Data Science, VTU (CGPA 7.9)'),
    ('Stack', 'Python · PyTorch · FastAPI · React/Next.js'),
    ('Focus', 'Agentic RAG · LLMs · Explainable AI'),
    ('Shipped', 'Aurelia AI · NexaMind AI · Aurevia Health AI'),
    ('Certs', 'Hugging Face ×4 · MS Applied Skills · Databricks'),
    ('Contact', 'varunbpvarunbp@gmail.com'),
]
H = Y0 + len(rows) * LH + 26


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


L = ['<?xml version="1.0" encoding="UTF-8"?>',
     f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="monospace">',
     '<defs><linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">'
     '<stop offset="0" stop-color="#0d3b42"/><stop offset="1" stop-color="#0d1117"/></linearGradient>'
     '<filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000" flood-opacity="0.45"/></filter></defs>',
     f'<rect width="{W}" height="{H}" fill="#0d1117" rx="10" filter="url(#soft)"/>',
     f'<rect width="{W}" height="38" fill="url(#bar)" rx="10"/><rect y="28" width="{W}" height="10" fill="url(#bar)"/>',
     f'<circle cx="20" cy="19" r="6" fill="#ff5f57"/><circle cx="40" cy="19" r="6" fill="#febc2e"/><circle cx="60" cy="19" r="6" fill="#28c840"/>',
     f'<text x="{W / 2}" y="25" text-anchor="middle" font-size="13" fill="{DIM}">varun@github: ~</text>',
     f'<rect width="{W}" height="{H}" fill="none" stroke="#21262d" stroke-width="2" rx="10"/>']

for i, (k, v, *rest) in enumerate(rows):
    y = Y0 + i * LH
    title = bool(rest)
    anim = '' if STATIC else (
        f'<animate attributeName="opacity" values="0;1" keyTimes="0;1" dur="0.01s" begin="{0.3 + i * 0.28:.2f}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="0 8" to="0 0" dur="0.45s" begin="{0.3 + i * 0.28:.2f}s" fill="freeze"/>')
    key = f'<tspan fill="{ACC if title else KEY}" font-weight="bold">{esc(k)}</tspan>'
    sep = '' if title else '<tspan fill="#3fb950">: </tspan>'
    val = '' if title else f'<tspan fill="{VAL}">{esc(v)}</tspan>'
    L.append(f'<g opacity="{"1" if STATIC else "0"}">{anim}<text x="{X0}" y="{y}" font-size="{"15" if title else "13.5"}">{key}{sep}{val}</text></g>')

L.append('</svg>')
open(DST, 'w', encoding='utf-8').write('\n'.join(L))
print(f'wrote {DST} ({len(rows)} rows)')
