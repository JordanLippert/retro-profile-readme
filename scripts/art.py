#!/usr/bin/env python3
"""Edit braille art on its dot grid, then trim the empty edges.

    python3 scripts/art.py in.txt --out out.txt --cut 19-25,31 --outline-from 14

Steps run in this order: --cut, --invert, --outline-from, trim. Rows count from 0.
--cut uses the rows of the input; --outline-from counts rows after the cut.
"""
import argparse

BLANK = 0x2800
DOTS = ((0, 0, 0x01), (0, 1, 0x02), (0, 2, 0x04), (1, 0, 0x08),
        (1, 1, 0x10), (1, 2, 0x20), (0, 3, 0x40), (1, 3, 0x80))


def load(path):
    text = open(path, encoding='utf-8').read().rstrip('\n').replace(' ', chr(BLANK))
    return text.split('\n')


def pad(rows):
    width = max(map(len, rows))
    return [r.ljust(width, chr(BLANK)) for r in rows]


def parse_rows(spec):
    """'1-3,7' -> {1, 2, 3, 7}"""
    rows = set()
    for part in spec.split(','):
        start, _, end = part.partition('-')
        rows.update(range(int(start), int(end or start) + 1))
    return rows


def invert(rows):
    return [''.join(chr(BLANK + ((ord(c) - BLANK) ^ 0xFF)) for c in r) for r in rows]


def outline(rows, start):
    """Keep only the dots on an edge, from row `start` down."""
    height, width = len(rows) * 4, len(rows[0]) * 2
    grid = [[0] * width for _ in range(height)]
    for cy, row in enumerate(rows):
        for cx, c in enumerate(row):
            for dx, dy, bit in DOTS:
                grid[cy * 4 + dy][cx * 2 + dx] = 1 if (ord(c) - BLANK) & bit else 0

    def on(y, x):
        return 0 <= y < height and 0 <= x < width and grid[y][x]

    def keep(y, x):
        if not grid[y][x]:
            return False
        return y < start * 4 or not (on(y - 1, x) and on(y + 1, x) and on(y, x - 1) and on(y, x + 1))

    return [''.join(chr(BLANK + sum(bit for dx, dy, bit in DOTS if keep(cy * 4 + dy, cx * 2 + dx)))
                    for cx in range(len(rows[0])))
            for cy in range(len(rows))]


def trim(rows):
    def empty(row):
        return all(ord(c) == BLANK for c in row)

    while rows and empty(rows[0]):
        rows = rows[1:]
    while rows and empty(rows[-1]):
        rows = rows[:-1]
    if not rows:
        return rows
    left = min(len(r) - len(r.lstrip(chr(BLANK))) for r in rows)
    right = min(len(r) - len(r.rstrip(chr(BLANK))) for r in rows)
    return [r[left:len(r) - right] for r in rows]


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('art')
    ap.add_argument('--out', required=True)
    ap.add_argument('--cut', help='rows to remove, e.g. 19-25,31')
    ap.add_argument('--invert', action='store_true', help='flip every dot, for mostly filled pieces')
    ap.add_argument('--outline-from', type=int, help='hollow solid areas from this row down')
    a = ap.parse_args()
    art = load(a.art)
    if a.cut:
        drop = parse_rows(a.cut)
        art = [r for i, r in enumerate(art) if i not in drop]
    if a.invert:
        art = invert(art)
    art = pad(art)  # after invert, or the padding would flip into a solid edge
    if a.outline_from is not None:
        art = outline(art, a.outline_from)
    open(a.out, 'w', encoding='utf-8').write('\n'.join(trim(art)) + '\n')
