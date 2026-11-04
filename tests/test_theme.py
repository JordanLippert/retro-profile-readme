"""`theme_aware` swaps paper cards for transparent images with a light and a dark version."""
import json

from test_cli import ROOT, Case

DOT = '⣿'
ICONS = json.loads((ROOT / 'scripts/icons24.json').read_text(encoding='utf-8'))


class ThemeAware(Case):
    def art(self, name='art.txt'):
        (self.dir / name).write_text(DOT * 4 + '\n', encoding='utf-8')
        return name

    def page(self, **cfg):
        return self.build(theme_aware=True, art_as_image=True, side_art=self.art(), closing_art=self.art('end.txt'),
                          stack=[{'id': 'docker', 'label': 'Docker'}], **cfg)

    def all_svgs(self):
        return [p.read_text(encoding='utf-8') for p in self.out.rglob('*.svg')]

    def test_every_image_has_both_versions(self):
        self.page()
        for base in ('imgs/icons/lang-docker', 'imgs/headings/stack', 'imgs/art/header', 'imgs/art/closing'):
            self.assertTrue((self.out / f'{base}-dark.svg').exists(), base)
            self.assertTrue((self.out / f'{base}-light.svg').exists(), base)

    def test_page_lets_github_pick_the_version(self):
        md = self.page()
        self.assertIn('<source media="(prefers-color-scheme: dark)" srcset="./imgs/icons/lang-docker-dark.svg">', md)
        self.assertIn('<img src="./imgs/icons/lang-docker-light.svg"', md)

    def test_no_paper_background_is_left(self):
        self.page()
        for svg in self.all_svgs():
            self.assertNotIn('#fbfaf6', svg)
            self.assertNotIn('#ffffff', svg)

    def test_icon_uses_the_color_of_each_theme(self):
        self.page()
        for theme in ('dark', 'light'):
            svg = (self.out / f'imgs/icons/lang-docker-{theme}.svg').read_text(encoding='utf-8')
            self.assertIn('#' + ICONS['docker'][theme], svg)

    def test_labels_survive(self):
        md = self.page()
        self.assertIn('alt="Docker"', md)
        self.assertIn('title="Docker"', md)
        self.assertIn('alt="01 Stack"', md)

    def test_links_wrap_the_picture(self):
        md = self.build(theme_aware=True, socials=[{'id': 'github', 'label': 'GitHub', 'url': 'https://github.com/x'}])
        self.assertIn('<a href="https://github.com/x"><picture>', md)

    def test_unknown_icon_falls_back_to_letters(self):
        self.build(theme_aware=True, stack=[{'id': 'zig', 'label': 'Zig'}])
        self.assertTrue((self.out / 'imgs/icons/lang-zig-dark.svg').exists())

    def test_cards_stay_when_the_option_is_off(self):
        self.build(art_as_image=True, stack=[{'id': 'python', 'label': 'Python'}])
        self.assertTrue((self.out / 'imgs/art/header.svg').exists())
        self.assertTrue((self.out / 'imgs/icons/lang-python.svg').exists())


class IconData(Case):
    def test_every_icon_fits_the_grid_and_has_both_colors(self):
        for name, icon in ICONS.items():
            self.assertEqual(len({len(r) for r in icon['rows']}), 1, name)
            self.assertLessEqual(max(len(icon['rows']), len(icon['rows'][0])), 24, name)
            self.assertRegex(icon['dark'], '^[0-9A-F]{6}$', name)
            self.assertRegex(icon['light'], '^[0-9A-F]{6}$', name)
