# Config reference

JSON file. Paths inside it are relative to the config file. Only `name` is required.

| Key | Default | Notes |
| --- | --- | --- |
| `name` | (required) | Text for the big figlet header. |
| `figlet_font` | `roman` | Any pyfiglet font. `roman` looks editorial; `standard`, `small`, `slant` are narrower. Run `pyfiglet -l` to list them. |
| `side_art` | none | Text file with ASCII or braille art shown next to the name. User-supplied or from `examples/art/`. |
| `side_art_gap` | `4` | Spaces between the widest name line and the art. |
| `side_art_layout` | `side` | `side` puts the art to the right of the name; `stacked` centers it above the name, for wider pieces. |
| `width` | `79` | Width of the window box in characters. Keep the whole header under ~80 so it doesn't scroll. |
| `window.title` | `~/about.txt` | Centered in the title bar, next to `(x) (-) (+)`. |
| `window.paragraphs` | `[]` | List of paragraphs; each is a list of lines (max `width - 4` chars). A blank line goes between them. |
| `window.signature` | none | Line right under the last paragraph, e.g. `-@handle`. |
| `sections.stack` / `sections.projects` / `sections.social` | `Stack` / `Projects` / `Social media` | Heading words. Pixel font has A-Z, 0-9, space and `, . ! ' / - + #`. |
| `numbered_headings` | `true` | Prefix headings with `01`, `02`. |
| `stack` | `[]` | Items `{ "id", "label" }`. Shown without links. A list of lists makes one row of icons per inner list. |
| `projects` | `[]` | Items `{ "name", "url", "stack", "lines" }`, shown between stack and social. `lines` is a list, one line each. Leave out to skip the section. |
| `closing_art` | none | Text file with art shown centered right before the footer. |
| `art_as_image` | `false` | Draws `side_art` and `closing_art` as SVG images on a paper card, so the line height of code blocks cannot pull the dots apart. The name uses the pixel font; the bio stays text. |
| `header_alt` / `closing_art_alt` | name / `Closing art` | Alt text for those images. |
| `socials` | `[]` | Items `{ "id", "label", "url" }`, optional `alt` and `title`. |
| `email` | none | Adds an envelope icon linking to `mailto:`. Never shown as text. |
| `palette` | see below | Any subset of the colors below. |
| `footer` | none | `{ "prompt", "command", "lines", "cursor" }`. Leave out to skip the footer. |

Default palette:

```json
{ "paper": "#fbfaf6", "ink": "#1d1c1a", "accent": "#1846b8",
  "highlight": "#f2c230", "bevel_light": "#ffffff", "bevel_dark": "#b9b5aa" }
```

`accent` colors the heading numbers and some icon details; `highlight` is the marker band
behind heading words and the yellow in icons like Python.

## Icons

Bundled ids: `c`, `clojure`, `python`, `swift`, `typescript`, `react`, `website`, `instagram`,
`tiktok`, `youtube`, `x`, `linkedin`, `github`, `email`.

Stack ids: `csharp`, `dotnet`, `javascript`, `java`, `nodejs`, `nestjs`, `fastapi`, `django`, `nextjs`,
`vite`, `tailwind`, `expo`, `astro`, `shadcn`, `postgresql`, `mysql`, `sqlserver`, `firebase`, `prisma`,
`drizzle`, `docker`, `nginx`, `aws`, `cloudflare`, `vercel`, `render`, `git`, `githubactions`,
`bitbucket`, `stripe`. Reduced from Simple Icons (CC0) and Devicon (MIT) or drawn by hand; the logos
belong to their owners.

Any other id gets the first two letters of `label` (or of `short`, if set) in the pixel font.
To draw your own, add a `glyph` to the item: a list of equal-length strings, at most 14×14, where
`#` is ink, `*` is accent, `o` is highlight and `.` is empty.

```json
{ "id": "go", "label": "Go", "glyph": [
  ".######.",
  "#......#",
  "#.##.#.#",
  "#......#",
  ".######." ] }
```

New bundled glyphs go in `scripts/glyphs.json` under `icons`.

## Editing art

`scripts/art.py` edits braille art on its dot grid and trims the empty edges:

```bash
python3 scripts/art.py in.txt --out out.txt --cut 19-25,31 --outline-from 14
```

- `--cut`: remove rows, counted from 0, to shorten a tall piece.
- `--invert`: flip every dot, for mostly filled pieces.
- `--outline-from`: hollow solid areas from that row down, counted after the cut, so a detailed face stays intact.
