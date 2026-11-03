---
name: retro-profile-readme
description: Builds a retro, paper-and-pixel GitHub profile README (username/username repo) with a figlet ASCII name, optional ASCII/braille side art, a Mac-style window holding the bio, numbered pixel-label headings, pixel-art icon tiles for the tech stack and social links, and a terminal "exit" footer. Use when someone wants to create, redesign or restyle their GitHub profile README, asks for an ASCII-art or retro/pixel/terminal-style profile, or wants stack and social badges that look hand-made instead of shields.io.
license: MIT
compatibility: Needs Python 3.8+ and pyfiglet. Previews need Playwright with Chromium or a local Chrome. Network only for the first preview (fetches GitHub's markdown CSS).
metadata:
  author: Celio Junior
  version: "1.0.0"
---

# Retro profile README

The result is one `README.md` plus small SVGs in `imgs/`. Everything comes from a single
JSON config, so build it with the scripts instead of hand-writing the markup.

## 1. Gather the details

Ask for anything you can't find in the conversation or the user's repo. Don't invent it.

- Name for the big header (short works best: a first name or the handle) and the GitHub username.
- Bio: 2 to 4 short lines, plus an optional tagline and signature such as `-@handle`.
- Stack: languages and tools, in the order they want them shown.
- Social links: full URLs for the site, Instagram, TikTok, YouTube, X, LinkedIn, GitHub, etc.
- Email, if they want one. It only ever becomes a `mailto:` link behind the envelope icon,
  never visible text, so it's less exposed to scrapers. Don't put it in the bio.
- Colors, if they don't like the defaults (paper, ink, blue accent, yellow highlighter).
- Side art (optional, see below).

## 2. Side art (optional)

Ask whether they want a picture next to their name. Point them to
https://emojicombos.com/anime-ascii-art and https://emojicombos.com/pokemon-ascii-art
(or any similar collection, or their own drawing) and ask them to pick one and paste it to you.
Save it as a plain text file next to the config (e.g. `side-art.txt`) and set `side_art`.

- Never bundle or commit art you picked yourself from those sites. The user chooses it,
  and art there is made by other people, so mention they should credit or check the
  artist's terms if the piece names any.
- Keep it about as tall as the name (7 to 12 lines) and under ~30 columns wide.
- Braille art (⣿) renders a little wider than ASCII in GitHub's font. The script pads
  every name line to the same column before the art, so braille can only shift as a block,
  never break the name. Don't "fix" alignment by adding spaces inside the art.

## 3. Write the config and build

Copy `examples/profile.json`, edit it (every key is listed in
[references/config.md](references/config.md)), then run:

```bash
pip install pyfiglet
python3 scripts/build.py profile.json --out path/to/username-repo
```

It writes `README.md`, `imgs/headings/*.svg` and `imgs/icons/*.svg`. Errors are explicit:
a window line that's too long, a name too wide for the chosen figlet font, a glyph too big.

What the build already takes care of, so leave it alone when editing by hand:

- Icons share one 60×60 canvas (a 48px tile with a transparent margin), so spacing comes
  from the image, not from `&nbsp;` or margins.
- Icon tags are chained with the line break inside the tag (`...></a\n  ><a ...>`), so
  there's no whitespace between them and every gap is identical.
- A stack or social id without a bundled glyph gets a 2-letter pixel tile. For a real icon,
  add a `glyph` to that item (see references/config.md).
- Every image has alt text and a title. Headings are numbered `01`, `02`.

## 4. Check it in light and dark

```bash
pip install playwright && playwright install chromium   # or pass --chrome /path/to/chrome
python3 scripts/preview.py path/to/username-repo
```

Open `preview-light.png` and `preview-dark.png` and look at them. The script also reports
code blocks that scroll sideways (lower `width`, shorten bio lines or slim the art),
uneven icon spacing and images that didn't load. The tiles are paper-colored on purpose
so they hold up on GitHub's dark theme too.

## 5. Hand it over

Delete the preview PNGs, then commit only `README.md` and `imgs/` to the profile repo
(the repo named exactly like the username). Don't push, create the repo or change GitHub
settings unless the user asks you to.
