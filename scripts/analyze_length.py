# -*- coding: utf-8 -*-
"""Locate the longest paragraphs / sections in manuscript.tex to plan the
editorial trimming (R3 items 3 and 4: length and triple repetition)."""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

lines = io.open(PATH, encoding='utf-8').read().split('\n')

paras = []
sec = 'PREAMBLE'
for i, ln in enumerate(lines):
    if re.match(r'\\(section|subsection)\*?\{', ln):
        sec = ln.strip()
        continue
    s = ln.strip()
    if not s or s.startswith('%'):
        continue
    if s.startswith('\\begin{') or s.startswith('\\end{') or s.startswith('\\') and len(s) < 60:
        continue
    paras.append((len(s), i + 1, sec, s[:70]))

paras.sort(reverse=True)
print('=== 20 longest paragraphs ===')
for n, ln, sec, head in paras[:20]:
    print(f'{n:5d} chars  L{ln:<4d} {head}')

total = sum(len(l) for l in lines)
print(f'\ntotal tex chars: {total:,}   lines: {len(lines)}')

print('\n=== section/subsection sizes (chars) ===')
secs = {}
cur = 'PREAMBLE'
start = 0
for i, ln in enumerate(lines):
    if re.match(r'\\(section|subsection)\*?\{', ln):
        secs[cur] = secs.get(cur, 0) + sum(len(x) for x in lines[start:i])
        cur = ln.strip()[:70]
        start = i
secs[cur] = secs.get(cur, 0) + sum(len(x) for x in lines[start:])
for k, v in sorted(secs.items(), key=lambda kv: -kv[1]):
    print(f'{v:7,d}  {k}')
