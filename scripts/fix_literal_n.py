# -*- coding: utf-8 -*-
"""Fix the two literal backslash-n sequences introduced by batch 2.

In scripts/apply_r3_edit_section3.py two replacement strings were written as raw
strings containing '\n\n'; Python therefore emitted a literal backslash + 'n'
instead of newlines, which LaTeX read as an undefined control sequence.
This replaces those literal sequences with real newlines.
"""
import io
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'manuscript.tex')

with io.open(PATH, encoding='utf-8') as f:
    text = f.read()

n = text.count('\\n\\n')
print(f'literal backslash-n pairs found: {n}')
text = text.replace('\\n\\n', '\n\n')

with io.open(PATH, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)
print('fixed' if n else 'nothing to fix')
