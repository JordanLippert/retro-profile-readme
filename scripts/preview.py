#!/usr/bin/env python3
"""Render a built README roughly the way GitHub shows it, in light and dark.

    python3 scripts/preview.py path/to/profile-repo [--chrome /usr/bin/google-chrome]

Writes preview-light.png and preview-dark.png next to README.md and prints
checks: code blocks that scroll sideways, and uneven gaps between icons.
Needs `pip install playwright` plus either `playwright install chromium`
or a local Chrome passed with --chrome. GitHub's markdown CSS is fetched
from jsDelivr once and cached in ~/.cache/retro-profile-readme/.
"""
import argparse, html, os, pathlib, re, sys, urllib.request

CSS_URL = 'https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown-{}.css'
CACHE = pathlib.Path.home() / '.cache' / 'retro-profile-readme'


def css(theme):
    f = CACHE / f'gh-{theme}.css'
    if not f.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        f.write_bytes(urllib.request.urlopen(CSS_URL.format(theme), timeout=30).read())
    return f.read_text()


def page(md, theme):
    body = re.sub(r'```text\n(.*?)\n```',
                  lambda m: '<div class="highlight"><pre>' + html.escape(m.group(1)) + '</pre></div>', md, flags=re.S)
    bg, border = ('#ffffff', '#d0d7de') if theme == 'light' else ('#0d1117', '#30363d')
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{css(theme)}'
            f'body{{background:{bg};margin:0;padding:32px}}'
            f'.markdown-body{{max-width:830px;margin:0 auto;border:1px solid {border};border-radius:6px;padding:32px}}'
            f'</style></head><body><article class="markdown-body">{body}</article></body></html>')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('repo')
    ap.add_argument('--chrome', help='path to a Chrome/Chromium binary (optional)')
    a = ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit('preview.py: pip install playwright (then `playwright install chromium` or pass --chrome)')
    root = pathlib.Path(a.repo).resolve()
    md = (root / 'README.md').read_text(encoding='utf-8')
    ok = True
    with sync_playwright() as p:
        b = p.chromium.launch(**({'executable_path': a.chrome} if a.chrome else {}))
        for theme in ('light', 'dark'):
            f = root / f'.preview-{theme}.html'
            f.write_text(page(md, theme), encoding='utf-8')
            pg = b.new_page(viewport={'width': 960, 'height': 600}, device_scale_factor=1.5)
            pg.goto(f.as_uri()); pg.wait_for_load_state('networkidle')
            out = root / f'preview-{theme}.png'
            pg.screenshot(path=str(out), full_page=True)
            f.unlink()
            print(out)
            if theme == 'light':
                pres = pg.evaluate("() => [...document.querySelectorAll('pre')].map(e => [e.scrollWidth, e.clientWidth])")
                for i, (sw, cw) in enumerate(pres):
                    if sw > cw:
                        ok = False
                        print(f'  check: code block {i+1} scrolls sideways ({sw}px content in {cw}px box)')
                rows = pg.evaluate("""() => [...document.querySelectorAll('p')]
                    .filter(p => p.querySelectorAll('img').length > 1)
                    .map(p => [...p.querySelectorAll('img')].map(i => Math.round(i.getBoundingClientRect().left)))""")
                for r in rows:
                    gaps = {r[i+1] - r[i] for i in range(len(r) - 1)}
                    if len(gaps) > 1:
                        ok = False
                        print(f'  check: uneven icon spacing {sorted(gaps)}')
                broken = pg.evaluate("() => [...document.images].filter(i => !i.naturalWidth).map(i => i.src)")
                for s in broken:
                    ok = False
                    print(f'  check: image did not load: {s}')
        b.close()
    print('checks passed' if ok else 'some checks failed, see above')


if __name__ == '__main__':
    main()
