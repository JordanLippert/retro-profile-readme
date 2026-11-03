# Art gallery

Ready-made braille pieces you can drop into `side_art`. Most are light line art on a blank
background, which reads well on GitHub in both light and dark mode.

```json
"side_art": "examples/art/pokemon/gengar.txt"
```

- **side** pieces are up to ~33 columns and 21 rows, made to sit next to a short name.
- **stacked** pieces (in the `stacked/` folders) are wider, up to 62 columns. Use them with
  `"side_art_layout": "stacked"` so the art goes above the name instead of beside it.
- Side art only fits if the name leaves room: name width + 5 + art width should stay
  around 80. A five-letter name in the default `roman` font is already ~45 to 60 columns,
  so with the wider pieces switch to `"figlet_font": "standard"` (or `small`), or go stacked.
  `build.py` warns when it gets too wide and `preview.py` flags a header that scrolls.

Every file was cleaned up the same way: trailing whitespace removed, regular spaces swapped
for the blank braille character (U+2800), empty edges cropped and every row padded to the
same width. `clefairy.txt` is the inverted version of `clefairy-filled.txt` (each braille
cell XOR 0xFF), since the original is mostly filled background.

## Pokémon

Source: <https://emojicombos.com/pokemon-ascii-art>

| File | What | Size (cols × rows) | Layout |
| --- | --- | --- | --- |
| [`pokemon/gengar.txt`](pokemon/gengar.txt) | Gengar | 30 × 16 | side |
| [`pokemon/mew.txt`](pokemon/mew.txt) | Mew | 25 × 14 | side |
| [`pokemon/pikachu.txt`](pokemon/pikachu.txt) | Pikachu in Ash's cap | 25 × 14 | side |
| [`pokemon/psyduck.txt`](pokemon/psyduck.txt) | Psyduck | 23 × 17 | side |
| [`pokemon/jigglypuff.txt`](pokemon/jigglypuff.txt) | Jigglypuff | 22 × 12 | side |
| [`pokemon/mewtwo.txt`](pokemon/mewtwo.txt) | Mewtwo | 22 × 15 | side |
| [`pokemon/snorlax.txt`](pokemon/snorlax.txt) | Snorlax | 25 × 11 | side |
| [`pokemon/eevee.txt`](pokemon/eevee.txt) | Eevee | 30 × 16 | side |
| [`pokemon/bulbasaur.txt`](pokemon/bulbasaur.txt) | Bulbasaur | 20 × 10 | side |
| [`pokemon/squirtle.txt`](pokemon/squirtle.txt) | Squirtle | 27 × 14 | side |
| [`pokemon/charizard.txt`](pokemon/charizard.txt) | Charizard | 28 × 14 | side |
| [`pokemon/mimikyu.txt`](pokemon/mimikyu.txt) | Mimikyu | 21 × 14 | side |
| [`pokemon/clefairy.txt`](pokemon/clefairy.txt) | Clefairy (inverted) | 30 × 15 | side |
| [`pokemon/clefairy-filled.txt`](pokemon/clefairy-filled.txt) | Clefairy (original, filled) | 30 × 15 | side |
| [`pokemon/stacked/charizard-large.txt`](pokemon/stacked/charizard-large.txt) | Charizard | 56 × 28 | stacked |
| [`pokemon/stacked/pikachu-sitting.txt`](pokemon/stacked/pikachu-sitting.txt) | Pikachu, sitting | 46 × 25 | stacked |
| [`pokemon/stacked/bulbasaur-large.txt`](pokemon/stacked/bulbasaur-large.txt) | Bulbasaur | 42 × 20 | stacked |

## Anime

Source: <https://emojicombos.com/anime-ascii-art>

| File | What | Size (cols × rows) | Layout |
| --- | --- | --- | --- |
| [`anime/anya-forger.txt`](anime/anya-forger.txt) | Anya Forger (Spy x Family) | 33 × 21 | side |
| [`anime/frieren-chibi.txt`](anime/frieren-chibi.txt) | Frieren, tiny | 20 × 8 | side |
| [`anime/gojo.txt`](anime/gojo.txt) | Gojo Satoru (Jujutsu Kaisen) | 23 × 15 | side |
| [`anime/saitama-ok.txt`](anime/saitama-ok.txt) | Saitama "OK" (One Punch Man) | 28 × 14 | side |
| [`anime/death-note-l.txt`](anime/death-note-l.txt) | L logo (Death Note) | 28 × 17 | side |
| [`anime/mahoraga-wheel.txt`](anime/mahoraga-wheel.txt) | Mahoraga's wheel (Jujutsu Kaisen) | 24 × 13 | side |
| [`anime/brand-of-sacrifice.txt`](anime/brand-of-sacrifice.txt) | Brand of Sacrifice (Berserk) | 23 × 18 | side |
| [`anime/jiji.txt`](anime/jiji.txt) | Jiji (Kiki's Delivery Service) | 15 × 10 | side |
| [`anime/boo-tao.txt`](anime/boo-tao.txt) | Boo Tao ghost (Genshin Impact) | 22 × 11 | side |
| [`anime/lain.txt`](anime/lain.txt) | Lain (Serial Experiments Lain) | 21 × 13 | side |
| [`anime/punpun.txt`](anime/punpun.txt) | Punpun (Oyasumi Punpun) | 25 × 11 | side |
| [`anime/sharingan.txt`](anime/sharingan.txt) | Sharingan eye (Naruto) | 17 × 12 | side |
| [`anime/stacked/goku.txt`](anime/stacked/goku.txt) | Goku (Dragon Ball) | 60 × 32 | stacked |
| [`anime/stacked/kurama.txt`](anime/stacked/kurama.txt) | Kurama (Naruto) | 62 × 29 | stacked |
| [`anime/stacked/pochita.txt`](anime/stacked/pochita.txt) | Pochita (Chainsaw Man) | 50 × 25 | stacked |
| [`anime/stacked/amaterasu-eyes.txt`](anime/stacked/amaterasu-eyes.txt) | Amaterasu eyes (Naruto) | 50 × 12 | stacked |
| [`anime/stacked/straw-hat-jolly-roger.txt`](anime/stacked/straw-hat-jolly-roger.txt) | Straw Hat Jolly Roger (One Piece) | 60 × 31 | stacked |

## Where these come from

All pieces were picked from community submissions on emojicombos.com (the two pages linked
above). The characters belong to their respective owners (Pokémon is a trademark of
Nintendo, Creatures and Game Freak; the anime characters belong to their creators and
studios). They're here for use on a personal profile. Check the source page before using
one somewhere else, and credit the artist if a piece names one. The repo's MIT license
covers the code, not these pieces.

There are hundreds more on those pages. If none of these fit, pick one there, save it as a
`.txt` file and point `side_art` at it.
