# retro-profile-readme

An [Agent Skill](https://agentskills.io/specification) that builds a retro GitHub profile
README: a big ASCII name, optional side art, your bio in a little Mac window, pixel-art
headings and icons for your stack and socials, and a terminal that logs out at the end.

<table>
  <tr>
    <th>Light theme</th>
    <th>Dark theme</th>
  </tr>
  <tr>
    <td><img src="assets/preview-light.png" alt="Example profile README in GitHub's light theme"></td>
    <td><img src="assets/preview-dark.png" alt="The same README in GitHub's dark theme"></td>
  </tr>
</table>

## Install

Clone it into your agent's skills folder. The folder has to be called `retro-profile-readme`.

| Agent | Where |
| --- | --- |
| Claude Code | `~/.claude/skills/` (or `.claude/skills/` in a project) |
| Cursor | `~/.cursor/skills/` (or `.cursor/skills/` / `.agents/skills/` in a project) |
| Codex | `~/.agents/skills/` (or `.agents/skills/` in a repo), then call `$retro-profile-readme` |
| Claude.ai | Zip this folder, then Customize > Skills > + > Upload a skill (code execution on) |

```bash
git clone https://github.com/devcelio/retro-profile-readme ~/.claude/skills/retro-profile-readme
```

## Use

Ask your agent something like *"make me a retro GitHub profile README"* and it handles the
rest. To do it by hand:

1. `pip install pyfiglet`
2. Copy [`examples/profile.json`](examples/profile.json) and fill in your name, bio, stack
   and links. Every key is in [references/config.md](references/config.md).
3. `python3 scripts/build.py my-profile.json --out ../<username>`
4. Commit `README.md` and `imgs/` to the repo named after your username.

Want to check it first? `pip install playwright && playwright install chromium`, then
`python3 scripts/preview.py ../<username>` saves light and dark screenshots.

## Side art

The picture next to your name is optional. There's a small gallery of ready-to-use braille
pieces in [`examples/art/`](examples/art/) (Pokémon and anime), or grab one from:

- https://emojicombos.com/anime-ascii-art
- https://emojicombos.com/pokemon-ascii-art

Save it as a `.txt` file and point `side_art` at it. Around 7 to 20 lines and under ~33
columns fits beside the name; wider pieces work with `"side_art_layout": "stacked"`.
That art is made by other people and the characters belong to their owners, so credit the
artist when there is one.

## License

MIT, see [LICENSE](LICENSE). The art in `examples/art/` isn't covered by it, see
[its README](examples/art/README.md).
