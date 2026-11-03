---
name: retro-profile-readme
description: Builds a retro, paper-and-pixel GitHub profile README (username/username repo) by interviewing the user. It asks short questions with concrete options (name and figlet font, ASCII/braille art from a bundled gallery or their own, bio, stack, social links, terminal footer), then writes the config, builds a figlet header, a Mac-style bio window, pixel headings and icon tiles, shows light/dark previews and iterates before publishing. Use when someone wants to create, redesign or restyle their GitHub profile README, asks for an ASCII-art, retro, pixel or terminal-style profile, or wants hand-made looking stack and social badges instead of shields.io.
license: MIT
compatibility: Needs Python 3.8+ and pyfiglet. Previews need Playwright with Chromium or a local Chrome. Network only for the first preview (fetches GitHub's markdown CSS).
metadata:
  author: Celio Junior
  version: "1.1.0"
---

# Retro profile README

You make the decisions together with the user: ask, offer concrete options, let them pick,
then build. They should never have to edit JSON. The result is one `README.md` plus small
SVGs in `imgs/`, generated from a `profile.json` that you write.

## How to ask

- One short question at a time, or a compact batch when the answers are quick.
- Always give options to pick from (numbered is easiest), with your suggestion first.
- "You pick" is a valid answer to anything. Use the default listed below and move on.
- Fill in what you already know (from the conversation, their GitHub profile, an existing
  README) and just confirm it instead of asking from scratch. Never invent facts about them.

## 1. Interview

Ask in this order. Defaults in brackets.

1. **GitHub username.** Needed for the repo name (`<username>/<username>`). [from context]
2. **Name for the big title.** First name, nickname or handle; shorter looks better.
   [first name] Then render it in 2 or 3 figlet fonts that fit and show them in a code block:

   ```bash
   python3 -c "import pyfiglet,sys; print(pyfiglet.figlet_format(sys.argv[1], font=sys.argv[2], width=300))" "Name" roman
   ```

   Good candidates: `roman` (editorial, wide), `standard`, `small`, `slant`. Drop any that
   go over ~75 columns. [`roman` if it fits, else `standard`]
3. **Art.** Ask if they want a picture by the name. [none, or the bundled computer]
   - Show a shortlist from [examples/art/README.md](examples/art/README.md) that matches their
     taste (Pokémon or anime), with name and size, e.g. "Gengar, 30×16, side".
   - Or let them paste their own from https://emojicombos.com/anime-ascii-art or
     https://emojicombos.com/pokemon-ascii-art (or any drawing). Save it as `side-art.txt`.
   - Pick the layout from the width: name width + 5 + art width up to ~80 can go **side** by
     side; anything wider goes **stacked** (above the name, up to ~62 columns). If side
     doesn't fit, offer a narrower font or stacked and let them choose.
   - If a pasted piece is mostly filled (lots of ⣿), offer the inverted version: XOR each
     braille cell's offset from U+2800 with 0xFF. Light strokes read better in both themes.
   - Mention that the art is someone else's and the characters belong to their owners, so
     they should credit the artist if one is named.
4. **Bio** for the `~/about.txt` window: 2 to 4 short lines, plus an optional second
   paragraph and a signature like `-@handle`. Offer to draft it from what they tell you and
   show the draft. Lines must be at most 75 characters. [signature `-@<username>`]
5. **Stack.** Languages and tools to show, in order. Bundled icons: C, Clojure, Python,
   Swift, TypeScript, React, GitHub. Anything else gets a 2-letter pixel tile, or you can
   draw a glyph (see [references/config.md](references/config.md)). [their top repo languages]
6. **Social links.** Which networks and the handle or URL for each. Bundled icons: website,
   Instagram, TikTok, YouTube, X, LinkedIn, GitHub, email. For email, say it only becomes a
   `mailto:` link behind an icon, never visible text, but the address is still in the page
   source, so scrapers can find it. Suggest a public or alias address. [no email]
7. **Footer.** The closing terminal block. [prompt `<username>@github ~ %`, command `exit`,
   the default logout lines] They can also skip it.
8. **Colors**, only if they bring it up. Defaults: paper, ink, blue accent, yellow highlight.

## 2. Build

Write `profile.json` yourself, following [examples/profile.json](examples/profile.json)
(every key is in [references/config.md](references/config.md)). Paths inside it are
relative to the config. Then:

```bash
pip install pyfiglet
python3 scripts/build.py profile.json --out path/to/<username>
```

Errors are explicit (a window line too long, a name too wide for the font, a glyph too big).
Fix them yourself and tell the user only if it changes something they chose, e.g. a bio
line you had to rewrap.

The build already handles icon spacing, alt text and heading numbers, so don't hand-edit
the output. Braille art renders a little wider than ASCII in GitHub's font; the script
aligns it as a block, so never add spaces inside the art to "fix" it.

## 3. Preview and iterate

```bash
pip install playwright && playwright install chromium   # or pass --chrome /path/to/chrome
python3 scripts/preview.py path/to/<username>
```

Show the user `preview-light.png` and `preview-dark.png` (or describe them if you can't
show images). Fix anything the checks report: a header that scrolls sideways (narrower
font, stacked art or smaller art), uneven icons, images that didn't load. Then ask what
they'd change, update the config, rebuild and show it again until they're happy.

## 4. Publish only when they say so

Ask before doing anything outside your workspace. When they approve:

- Delete the preview PNGs.
- Commit only `README.md` and `imgs/` to the repo named exactly like the username.
- Push, create the repo or change GitHub settings only if they explicitly ask for it.
  If you can't, hand them the folder and the two commands to run.
