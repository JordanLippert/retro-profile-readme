#!/usr/bin/env python3
"""Build a retro GitHub profile README from a profile config.

    python3 scripts/build.py path/to/profile.json --out path/to/profile-repo

Writes README.md, imgs/icons/*.svg and imgs/headings/*.svg into --out.
Needs Python 3.8+ and pyfiglet (pip install pyfiglet) for the big name.
See references/config.md for every config key.
"""
import argparse, html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
GLY = json.load(open(os.path.join(HERE, 'glyphs.json')))
ICONS, FONT = GLY['icons'], GLY['font_5x7']

DEFAULT_PALETTE = {  # light "paper" look that also reads on GitHub dark mode
    'paper': '#fbfaf6', 'ink': '#1d1c1a', 'accent': '#1846b8',
    'highlight': '#f2c230', 'bevel_light': '#ffffff', 'bevel_dark': '#b9b5aa'}
CANVAS, MARGIN, TILE, SCALE = 20, 2, 16, 3   # 60x60 px icon, 48 px tile, 12 px gap


def die(msg):
    sys.exit(f'build.py: {msg}')


# ---------------------------------------------------------------- svg helpers
def svg(w, h, rects, title):
    body = ''.join(f'<rect x="{x}" y="{y}" width="{rw}" height="{rh}" fill="{c}"/>'
                   for x, y, rw, rh, c in rects)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w*SCALE}" height="{h*SCALE}" '
            f'viewBox="0 0 {w} {h}" shape-rendering="crispEdges"><title>{html.escape(title)}</title>'
            f'{body}</svg>\n')


def card(P, x0, y0, w, h):
    """Paper card with a 1-unit ink outline (notched corners) and a soft bevel."""
    return [(x0+1, y0, w-2, 1, P['ink']), (x0+1, y0+h-1, w-2, 1, P['ink']),
            (x0, y0+1, 1, h-2, P['ink']), (x0+w-1, y0+1, 1, h-2, P['ink']),
            (x0+1, y0+1, w-2, h-2, P['paper']),
            (x0+1, y0+1, w-2, 1, P['bevel_light']), (x0+1, y0+1, 1, h-2, P['bevel_light']),
            (x0+1, y0+h-2, w-2, 1, P['bevel_dark']), (x0+w-2, y0+1, 1, h-2, P['bevel_dark'])]


def pixels(P, rows, ox, oy):
    col = {'#': P['ink'], '*': P['accent'], 'o': P['highlight']}
    return [(ox+x, oy+y, 1, 1, col[ch]) for y, r in enumerate(rows) for x, ch in enumerate(r) if ch in col]


def text_w(s):
    return sum(len(FONT[c][0]) + 1 for c in s) - 1 if s else 0


def text_px(s, x, y, color):
    out = []
    for c in s:
        out += [(x+xx, y+yy, 1, 1, color) for yy, r in enumerate(FONT[c]) for xx, ch in enumerate(r) if ch == '#']
        x += len(FONT[c][0]) + 1
    return out


def glyph_for(item):
    """Custom glyph from the config, a bundled one, or 1-2 letters as a fallback."""
    if item.get('glyph'):
        return item['glyph']
    if item['id'] in ICONS:
        return ICONS[item['id']]
    letters = ''.join(c for c in item.get('short', item['label']).upper() if c in FONT and c != ' ')[:2] or '?'
    print(f'  note: no bundled glyph for "{item["id"]}", using letters "{letters}"', file=sys.stderr)
    w = text_w(letters)
    grid = [['.'] * w for _ in range(7)]
    for x, y, *_ in text_px(letters, 0, 0, ''):
        grid[y][x] = '#'
    return [''.join(r) for r in grid]


def icon_svg(P, item):
    rows = glyph_for(item)
    gw, gh = max(map(len, rows)), len(rows)
    if gw > TILE - 2 or gh > TILE - 2:
        die(f'glyph for "{item["id"]}" is {gw}x{gh}; max is {TILE-2}x{TILE-2}')
    ox, oy = MARGIN + (TILE - gw) // 2, MARGIN + (TILE - gh) // 2
    return svg(CANVAS, CANVAS, card(P, MARGIN, MARGIN, TILE, TILE) + pixels(P, rows, ox, oy), item['label'])


def heading_svg(P, num, word):
    word = word.upper()
    bad = sorted({c for c in num + word if c not in FONT})
    if bad:
        die(f'heading "{word}" uses characters the pixel font lacks: {bad}')
    nw, ww = text_w(num), text_w(word)
    w, h = 6 + nw + (4 if num else 0) + ww + 6, 17
    r = card(P, 0, 0, w - 1, h - 1) + [(1, h-1, w-1, 1, P['ink']), (w-1, 1, 1, h-1, P['ink'])]
    x = 6
    if num:
        r += text_px(num, x, 4, P['accent']); x += nw + 4
    r += [(x-1, 8, ww+2, 4, P['highlight'])] + text_px(word, x, 4, P['ink'])
    return svg(w, h, r, word.title()), w * SCALE, h * SCALE


# --------------------------------------------------------------- ascii parts
def figlet(text, font):
    try:
        import pyfiglet
    except ImportError:
        die('pyfiglet is missing: pip install pyfiglet')
    lines = pyfiglet.figlet_format(text, font=font, width=300).rstrip('\n').split('\n')
    while lines and not lines[-1].strip():
        lines.pop()
    while lines and not lines[0].strip():
        lines.pop(0)
    return [l.rstrip() for l in lines]


def header_block(cfg, base):
    name = figlet(cfg['name'], cfg.get('figlet_font', 'roman'))
    W = cfg.get('width', 79)
    art = []
    if cfg.get('side_art'):
        art = open(os.path.join(base, cfg['side_art']), encoding='utf-8').read().rstrip('\n').split('\n')
    layout = cfg.get('side_art_layout', 'side')
    if layout not in ('side', 'stacked'):
        die(f'side_art_layout must be "side" or "stacked", not "{layout}"')
    gap = cfg.get('side_art_gap', 4)
    col = 1 + max(map(len, name)) + gap          # every side-art line starts at this column
    lines = []
    if layout == 'stacked' and art:              # art on top, centered over the window
        pad = ' ' * max(1, (W + 2 - max(map(len, art))) // 2)
        lines = [(pad + s).rstrip() for s in art] + [''] + [(' ' + a).rstrip() for a in name]
        col = len(pad)
    else:
        n = max(len(name), len(art))
        top_n, top_a = (n - len(name)) // 2, (n - len(art)) // 2
        for i in range(n):
            a = name[i - top_n] if 0 <= i - top_n < len(name) else ''
            s = art[i - top_a] if 0 <= i - top_a < len(art) else ''
            lines.append(((' ' + a).ljust(col) + s).rstrip() if s else (' ' + a).rstrip())
    ascii_w = max(len(' ' + l) for l in name)
    if ascii_w > W:
        die(f'figlet name is {ascii_w} columns wide (> width {W}); try a smaller figlet_font')
    if art and col + max(map(len, art)) > W + 5:
        print(f'  warning: name + side art is ~{col + max(map(len, art))} columns; '
              'it may scroll sideways on narrow screens', file=sys.stderr)

    return '\n'.join(lines + ['', window_block(cfg)])


def window_block(cfg):
    W = cfg.get('width', 79)
    win = cfg.get('window', {})
    inner = W - 4
    def row(s=''):
        if len(s) > inner:
            die(f'window line is {len(s)} chars, max {inner}: "{s}"')
        return ' | ' + s.ljust(inner) + ' |'
    lights = '(x) (-) (+)'
    bar = lights + win.get('title', '~/about.txt').center(inner - 2 * len(lights)) + ' ' * len(lights)
    box = [' .' + '-' * (W - 2) + '.', row(bar), ' |' + '-' * (W - 2) + '|', row()]
    for para in win.get('paragraphs', []):
        box += [row(l) for l in para] + [row()]
    if win.get('signature'):
        box[-1:] = [row(win['signature']), row()]
    box.append(" '" + '-' * (W - 2) + "'")
    return '\n'.join(box)


def read_art(base, path):
    return open(os.path.join(base, path), encoding='utf-8').read().rstrip('\n').split('\n')


def closing_art_block(cfg, base):
    if not cfg.get('closing_art'):
        return ''
    rows = read_art(base, cfg['closing_art'])
    pad = ' ' * max(1, (cfg.get('width', 79) + 2 - max(map(len, rows))) // 2)
    return '\n'.join(pad + r for r in rows)


# ------------------------------------------------------------------ art images
BRAILLE_DOTS = ((0, 0, 0x01), (0, 1, 0x02), (0, 2, 0x04), (1, 0, 0x08),
                (1, 1, 0x10), (1, 2, 0x20), (0, 3, 0x40), (1, 3, 0x80))
BORDER = 3


def dots_path(rows, ox, oy, pitch):
    """One path with a small square per braille dot."""
    size = pitch - 1
    d = []
    for cy, row in enumerate(rows):
        for cx, c in enumerate(row):
            bits = ord(c) - 0x2800
            for dx, dy, bit in BRAILLE_DOTS:
                if 0 <= bits <= 0xFF and bits & bit:
                    d.append(f'M{ox + (cx * 2 + dx) * pitch} {oy + (cy * 4 + dy) * pitch}h{size}v{size}h-{size}z')
    return ''.join(d)


def art_card(P, w, h, body, title):
    """Paper card with the same ink outline and bevel as the icon tiles."""
    t = BORDER
    rects = [(t, 0, w-2*t, t, P['ink']), (t, h-t, w-2*t, t, P['ink']),
             (0, t, t, h-2*t, P['ink']), (w-t, t, t, h-2*t, P['ink']),
             (t, t, w-2*t, h-2*t, P['paper']),
             (t, t, w-2*t, t, P['bevel_light']), (t, t, t, h-2*t, P['bevel_light']),
             (t, h-2*t, w-2*t, t, P['bevel_dark']), (w-2*t, t, t, h-2*t, P['bevel_dark'])]
    shapes = ''.join(f'<rect x="{x}" y="{y}" width="{rw}" height="{rh}" fill="{c}"/>' for x, y, rw, rh, c in rects)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'shape-rendering="crispEdges"><title>{html.escape(title)}</title>{shapes}{body}</svg>\n')


def closing_svg(P, rows, title):
    pitch, pad = 3, 24
    w = len(rows[0]) * 2 * pitch + 2 * pad
    h = len(rows) * 4 * pitch + 2 * pad
    return art_card(P, w, h, f'<path fill="{P["ink"]}" d="{dots_path(rows, pad, pad, pitch)}"/>', title), w


def banner_svg(P, name, rows, title):
    """The name in the pixel font of the headings, with the art beside it."""
    word = name.upper()
    bad = sorted({c for c in word if c not in FONT})
    if bad:
        die(f'name "{word}" uses characters the pixel font lacks: {bad}')
    scale, pitch, pad, gap = 10, 4, 32, 48
    text_width, text_height = text_w(word) * scale, 7 * scale
    art_w = len(rows[0]) * 2 * pitch if rows else 0
    art_h = len(rows) * 4 * pitch if rows else 0
    w = pad + text_width + (gap + art_w if rows else 0) + pad
    h = max(art_h, text_height + scale * 4) + 2 * pad
    x, y = pad, (h - text_height) // 2
    band = (f'<rect x="{x - scale}" y="{y + 4 * scale}" width="{text_width + 2 * scale}" '
            f'height="{4 * scale}" fill="{P["highlight"]}"/>')
    letters = ''.join(f'<rect x="{x + px * scale}" y="{y + py * scale}" width="{scale}" height="{scale}" fill="{c}"/>'
                      for px, py, _, _, c in text_px(word, 0, 0, P['ink']))
    art = ''
    if rows:
        art = f'<path fill="{P["ink"]}" d="{dots_path(rows, w - pad - art_w, (h - art_h) // 2, pitch)}"/>'
    return art_card(P, w, h, band + letters + art, title), w


def image_tag(path, alt, width, center=False):
    """No height attribute, so the image keeps its shape when a narrow screen scales it down."""
    tag = f'<img src="./{path}" alt="{html.escape(alt)}" width="{width}">'
    return f'<p align="center">{tag}</p>' if center else f'<p>{tag}</p>'


def footer_block(cfg):
    f = cfg.get('footer')
    if not f:
        return ''
    lines = [f' {f.get("prompt", "user@host ~ %")} {f.get("command", "exit")}']
    lines += [(' ' + l if l else '') for l in f.get('lines', ['logout', 'Saving session...completed.', '', '[Process completed]'])]
    lines[-1] += f.get('cursor', '\u258c')
    return '\n'.join(lines)


# -------------------------------------------------------------------- readme
def chain(tags):
    """Back-to-back tags; line breaks fall inside the tag so no whitespace gap appears."""
    return '<p>\n  ' + '\n  >'.join(t[:-1] for t in tags) + '>\n</p>'


def project_item(p):
    """One list item: linked name, stack, then the description lines."""
    head = f'<b><a href="{html.escape(p["url"])}">{html.escape(p["name"])}</a></b>'
    if p.get('stack'):
        head += f' · {html.escape(p["stack"])}'
    return '  <li>' + '<br>'.join([head] + [html.escape(l) for l in p.get('lines', [])]) + '</li>'


def build(cfg_path, out):
    base = os.path.dirname(os.path.abspath(cfg_path))
    cfg = json.load(open(cfg_path, encoding='utf-8'))
    for k in ('name',):
        if k not in cfg:
            die(f'config is missing "{k}"')
    P = {**DEFAULT_PALETTE, **cfg.get('palette', {})}
    os.makedirs(f'{out}/imgs/icons', exist_ok=True)
    os.makedirs(f'{out}/imgs/headings', exist_ok=True)

    as_image = cfg.get('art_as_image', False)
    if as_image:
        os.makedirs(f'{out}/imgs/art', exist_ok=True)
        alt = cfg.get('header_alt', cfg['name'])
        rows = read_art(base, cfg['side_art']) if cfg.get('side_art') else []
        banner, width = banner_svg(P, cfg['name'], rows, alt)
        open(f'{out}/imgs/art/header.svg', 'w', encoding='utf-8').write(banner)
        parts = [image_tag('imgs/art/header.svg', alt, width), '```text\n' + window_block(cfg) + '\n```']
    else:
        parts = ['```text\n' + header_block(cfg, base) + '\n```']
    sections = cfg.get('sections', {})
    num = 0
    def heading(key, default):
        nonlocal num
        num += 1
        n = f'{num:02d}' if cfg.get('numbered_headings', True) else ''
        word = sections.get(key, default)
        s, w, h = heading_svg(P, n, word)
        open(f'{out}/imgs/headings/{key}.svg', 'w').write(s)
        alt = (n + ' ' if n else '') + word.capitalize()
        parts.append(f'<p><img src="./imgs/headings/{key}.svg" alt="{html.escape(alt)}" width="{w}" height="{h}"></p>')

    def section(key, default, items, linked):
        if not items:
            return
        heading(key, default)
        for row in items if isinstance(items[0], list) else [items]:  # a list of lists is one row each
            tags = []
            for it in row:
                it.setdefault('label', it['id'].title())
                fname = f'{"lang-" if not linked else ""}{it["id"]}.svg'
                open(f'{out}/imgs/icons/{fname}', 'w').write(icon_svg(P, it))
                alt, title = html.escape(it.get('alt', it['label'])), html.escape(it.get('title', it['label']))
                img = f'<img src="./imgs/icons/{fname}" alt="{alt}" title="{title}" width="60" height="60">'
                tags.append(f'<a href="{html.escape(it["url"])}">{img}</a>' if linked else img)
            parts.append(chain(tags))

    section('stack', 'Stack', cfg.get('stack', []), False)
    projects = cfg.get('projects', [])
    if projects:  # HTML, not markdown, so the preview renders it the way GitHub does
        heading('projects', 'Projects')
        parts.append('<ul>\n' + '\n'.join(project_item(p) for p in projects) + '\n</ul>')
    socials = list(cfg.get('socials', []))
    if cfg.get('email'):  # link only, the address never shows as text
        socials.append({'id': 'email', 'url': 'mailto:' + cfg['email'], 'label': 'Email', 'alt': 'Send me an email'})
    section('social', 'Social media', socials, True)
    if as_image and cfg.get('closing_art'):
        alt = cfg.get('closing_art_alt', 'Closing art')
        closing, width = closing_svg(P, read_art(base, cfg['closing_art']), alt)
        open(f'{out}/imgs/art/closing.svg', 'w', encoding='utf-8').write(closing)
        parts.append(image_tag('imgs/art/closing.svg', alt, width, center=True))
    elif cfg.get('closing_art'):
        parts.append('```text\n' + closing_art_block(cfg, base) + '\n```')
    foot = footer_block(cfg)
    if foot:
        parts.append('```text\n' + foot + '\n```')
    open(f'{out}/README.md', 'w', encoding='utf-8').write('\n\n'.join(parts) + '\n')
    print(f'wrote {out}/README.md')


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('config')
    ap.add_argument('--out', default='.')
    a = ap.parse_args()
    build(a.config, a.out)
