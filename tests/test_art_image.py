"""`art_as_image` draws braille dots into SVGs, so GitHub's line height cannot pull them apart."""
from test_cli import Case

DOT = '⣿'


class ArtAsImage(Case):
    def art(self, name='art.txt'):
        (self.dir / name).write_text(DOT * 4 + '\n' + DOT * 4 + '\n', encoding='utf-8')
        return name

    def page(self, **cfg):
        return self.build(art_as_image=True, side_art=self.art(),
                          window={'paragraphs': [['Hello there']]}, **cfg)

    def svg(self, name):
        return (self.out / 'imgs/art' / name).read_text(encoding='utf-8')

    def test_header_becomes_an_image_and_the_bio_stays_text(self):
        md = self.page()
        self.assertIn('imgs/art/header.svg', md)
        self.assertLess(md.index('header.svg'), md.index('Hello there'))
        self.assertNotIn(DOT, md)

    def test_dots_are_drawn_in_the_svg(self):
        self.page()
        self.assertIn('<path', self.svg('header.svg'))

    def test_every_dot_of_the_art_is_drawn(self):
        self.build(art_as_image=True, closing_art=self.art())
        self.assertEqual(self.svg('closing.svg').count('z'), 4 * 2 * 8)

    def test_closing_art_sits_before_the_footer(self):
        md = self.page(closing_art=self.art('end.txt'), footer={'prompt': 'x %', 'command': 'exit'})
        self.assertLess(md.index('imgs/art/closing.svg'), md.index('x % exit'))
        self.assertNotIn(DOT, md)

    def test_alt_text_is_configurable_and_escaped(self):
        md = self.page(header_alt='Lo & art', closing_art=self.art('end.txt'), closing_art_alt='End <art>')
        self.assertIn('alt="Lo &amp; art"', md)
        self.assertIn('alt="End &lt;art&gt;"', md)

    def test_images_scale_down_on_narrow_screens(self):
        md = self.page()
        tag = md[md.index('<img src="./imgs/art/header.svg"'):].split('>')[0]
        self.assertIn('width=', tag)
        self.assertNotIn('height=', tag)

    def test_works_without_side_art(self):
        md = self.build(art_as_image=True)
        self.assertIn('imgs/art/header.svg', md)

    def test_text_mode_is_unchanged_by_default(self):
        md = self.build(side_art=self.art())
        self.assertIn(DOT, md)
        self.assertNotIn('imgs/art', md)
