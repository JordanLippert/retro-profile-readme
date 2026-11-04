# Spec: projects, closing art, stack icons, art editor and a One Piece profile

Status: ready-for-agent

## Problem Statement

The generator covers a bio, a flat stack row and socials. A working developer has more to
show: side projects, a stack of around thirty tools, and a page that feels like theirs. Most
tools fall back to two-letter tiles, there is no place for projects, art can only sit at the
top, and art that is too tall or too filled has to be fixed by hand.

## Solution

Extend the generator with a projects section, a closing art block, a bundled icon set for
common stacks, grouped stack rows and a small braille art editor. Then use them to build
Jordan Lippert's bilingual One Piece profile.

## User Stories

1. As a profile owner, I want a projects section, so that visitors see what I built.
2. As a profile owner, I want each project to link to its site or repo, so that visitors can open it.
3. As a profile owner, I want a stack line per project, so that the tools are clear at a glance.
4. As a profile owner, I want several description lines per project, so that I can write in two languages.
5. As a profile owner, I want the projects heading numbered like the others, so that the page stays consistent.
6. As a profile owner with no projects, I want the section omitted, so that existing configs keep working.
7. As a profile owner, I want special characters in project text escaped, so that the page cannot break.
8. As a profile owner, I want art before the terminal footer, so that the page has a closing beat.
9. As a profile owner, I want that art centered, so that it lines up with the window above.
10. As a profile owner, I want bundled icons for common languages, frameworks, databases and infra, so that I do not get two-letter tiles.
11. As a profile owner, I want to split my stack into rows, so that thirty icons stay readable.
12. As a profile owner, I want a flat stack list to keep working, so that old configs do not break.
13. As an art user, I want to remove rows from a piece, so that a tall drawing gets shorter.
14. As an art user, I want to turn solid areas into outlines, so that heavy drawings get lighter.
15. As an art user, I want outlining to start at a chosen row, so that a detailed face stays intact.
16. As an art user, I want to invert a filled piece, so that it reads in both themes.
17. As an art user, I want empty edges trimmed, so that the piece centers correctly.
18. As Jordan, I want my profile config and art kept in this fork, so that I can rebuild the page later.
19. As a maintainer, I want the generic features separate from personal data, so that they could go upstream.
20. As a profile owner on a dark theme, I want every icon to keep its paper tile visible, so that no icon disappears into the page.
21. As a visitor, I want the stack grouped by back end, front end and mobile, data and infra, so that I can scan it quickly.
22. As a bilingual reader, I want the bio and project text in Portuguese and English, so that recruiters in both languages can read it.
23. As Jordan, I want no phone number or internal employer metrics on the page, so that nothing private or company-owned goes public.

## Implementation Decisions

- The build gains a `projects` config list. Items hold name, url, stack and lines. It renders as
  HTML, not markdown, so the local preview and GitHub show the same thing. Heading word comes from
  `sections.projects`.
- Section order is stack, projects, social, closing art, footer.
- `closing_art` is a path relative to the config. It renders as its own text block, centered like stacked art.
- `stack` accepts a flat list or a list of lists. Each inner list is one row of icons.
- Icons are 14x14 at most, in the existing glyph format. Sources are Simple Icons (CC0) and Devicon
  (MIT), reduced to pixels, with hand-drawn glyphs where the reduction is illegible. Logos stay trademarks of their owners.
- The art editor is a separate script that works on the braille dot grid: trim, cut rows, invert, outline from a row.
- A glyph covers at most 55% of the tile. A glyph that fills the tile hides the paper card and vanishes on the dark theme, so filled logos are reduced to about 11x11.
- Jordan's page uses the small Luffy unedited beside the name, in the `standard` font. Outlining it weakened the hat and face, so it was rejected.
- Jordan's closing art is Sanji with a shortened torso and an outlined body, which keeps the face intact and suits the "rebaixado" joke. The original stays next to it, so the edit can be rerun.
- Personal data lives in its own profile folder. Gallery art goes in the existing anime examples only if it is not personal.

## Testing Decisions

- One seam: run the build CLI with a config and assert on the README and SVGs. The art editor is tested the same way, through its CLI.
- Tests cover external output only, using the standard library test runner, so no new dependency.
- Icon data is checked as a whole: every glyph must be rectangular, fit the tile and leave paper visible.
- No prior tests exist in this repo. The preview script stays a manual check.

## Out of Scope

- Opening a pull request upstream.
- Publishing to the JordanLippert/JordanLippert repo, which needs separate approval.
- Middle-of-page art beyond the closing block.
- Changing the interview in SKILL.md beyond mentioning the new keys.

## Further Notes

Art comes from emojicombos, with no artist named. Characters belong to their owners.
