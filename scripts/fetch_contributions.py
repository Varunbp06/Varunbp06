"""Scrape public contribution calendar (no token) -> data/contributions.json."""
import json
import re
from collections import defaultdict
import requests
from bs4 import BeautifulSoup

USER = 'Varunbp06'
URL = f'https://github.com/users/{USER}/contributions'
OUT = 'data/contributions.json'

soup = BeautifulSoup(requests.get(URL, timeout=30).text, 'html.parser')
counts = {}
for tip in soup.find_all('tool-tip'):
    m = re.match(r'(\d+|No)\s+contributions?\s+on\s+(.+)', tip.get_text(strip=True).replace('.', ''))
    if m and tip.get('for'):
        counts[tip['for']] = 0 if m.group(1) == 'No' else int(m.group(1))
cells = soup.find_all(attrs={'data-date': True})
days = sorted((c['data-date'], counts.get(c.get('id'), 0), int(c.get('data-level', 0) or 0)) for c in cells)
if not days:
    raise SystemExit('no contribution cells found')

total = sum(d[1] for d in days)
best = max(days, key=lambda d: d[1])
cur = long = run = 0
prev = None
for d, n, _ in days:
    run = run + 1 if n > 0 else 0
    cur = run
    long = max(long, run)
    prev = d
monthly = defaultdict(int)
for d, n, _ in days:
    monthly[d[:7]] += n

json.dump({'user': USER, 'total': total, 'best_day': {'date': best[0], 'count': best[1]},
           'current_streak': cur, 'longest_streak': long,
           'monthly': dict(sorted(monthly.items())), 'days': [{'date': d, 'count': n, 'level': lv} for d, n, lv in days]},
          open(OUT, 'w'), indent=1)
print(f'wrote {OUT}: {total} contributions, {len(days)} days')
