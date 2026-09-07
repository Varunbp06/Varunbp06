"""Resume stack -> self-hosted tech-orbit SVG (SMIL, loops, no services). Re-run manually if stack changes."""
import math

DST = 'tech-orbit.svg'
W, H, CX, CY, RX, RY, DUR = 640, 360, 320, 180, 232, 108, 28
BG, ACC, VAL, DIM = '#0d1117', '#00ffdc', '#e6edf3', '#7d8590'
STACK = ['Python', 'PyTorch', 'FastAPI', 'React', 'RAG', 'LLMs', 'Docker', 'PostgreSQL']

L = ['<?xml version="1.0" encoding="UTF-8"?>',
     f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="monospace">',
     f'<rect width="{W}" height="{H}" fill="{BG}" rx="10"/>',
     f'<ellipse cx="{CX}" cy="{CY}" rx="{RX}" ry="{RY}" fill="none" stroke="{DIM}" stroke-opacity="0.35" stroke-dasharray="4 5"/>',
     f'<ellipse cx="{CX}" cy="{CY}" rx="{RX - 62}" ry="{RY - 34}" fill="none" stroke="{DIM}" stroke-opacity="0.2"/>',
     f'<g><animateTransform attributeName="transform" type="rotate" from="0 {CX} {CY}" to="360 {CX} {CY}" dur="{DUR}s" repeatCount="indefinite"/>']
for i, s in enumerate(STACK):
    a = 2 * math.pi * i / len(STACK)
    x, y = CX + RX * math.cos(a), CY + RY * math.sin(a)
    L.append(f'<g><animateTransform attributeName="transform" type="rotate" from="0 {x:.0f} {y:.0f}" to="-360 {x:.0f} {y:.0f}" dur="{DUR}s" repeatCount="indefinite"/>'
             f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="{ACC}"/>'
             f'<text x="{x:.0f}" y="{y - 12:.0f}" text-anchor="middle" font-size="13" fill="{VAL}">{s}</text></g>')
L += ['</g>',
      f'<rect x="{CX - 118}" y="{CY - 24}" width="236" height="48" rx="10" fill="#0d3b42" stroke="{ACC}" stroke-opacity="0.6"/>',
      f'<text x="{CX}" y="{CY + 6}" text-anchor="middle" font-size="16" font-weight="bold" fill="{VAL}">AI/ML · RAG Systems</text>',
      f'<rect width="{W}" height="{H}" fill="none" stroke="#21262d" stroke-width="2" rx="10"/>', '</svg>']
open(DST, 'w', encoding='utf-8').write('\n'.join(L))
print(f'wrote {DST} ({len(STACK)} nodes)')
