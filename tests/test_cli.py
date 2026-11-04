"""Tests through the public seam: the build and art CLIs."""
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
BLANK, FULL = '⠀', '⣿'


def run(script, *args):
    return subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / 'scripts' / script), *map(str, args)],
                          capture_output=True, text=True, encoding='utf-8')


class Case(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = pathlib.Path(tmp.name)

    def build(self, **cfg):
        path = self.dir / 'profile.json'
        path.write_text(json.dumps({'name': 'Lo', 'figlet_font': 'small', **cfg}), encoding='utf-8')
        out = self.dir / 'out'
        self.result = run('build.py', path, '--out', out)
        self.assertEqual(self.result.returncode, 0, self.result.stderr)
        self.out = out
        return (out / 'README.md').read_text(encoding='utf-8')


class Projects(Case):
    item = {'name': 'Demo', 'url': 'https://example.com/?a=1&b=2', 'stack': 'Python', 'lines': ['One', 'Two <b>']}

    def test_section_sits_between_stack_and_social(self):
        md = self.build(stack=[{'id': 'python', 'label': 'Python'}], projects=[self.item],
                        socials=[{'id': 'github', 'label': 'GitHub', 'url': 'https://github.com/x'}])
        self.assertLess(md.index('headings/stack.svg'), md.index('headings/projects.svg'))
        self.assertLess(md.index('headings/projects.svg'), md.index('headings/social.svg'))
        self.assertTrue((self.out / 'imgs/headings/projects.svg').exists())
        self.assertIn('alt="02 Projects"', md)

    def test_item_links_and_escapes(self):
        md = self.build(projects=[self.item])
        self.assertIn('<a href="https://example.com/?a=1&amp;b=2">Demo</a>', md)
        self.assertIn('One<br>Two &lt;b&gt;', md)
        self.assertNotIn('Two <b>', md)

    def test_heading_word_comes_from_sections(self):
        md = self.build(projects=[self.item], sections={'projects': 'Projetos'})
        self.assertIn('alt="01 Projetos"', md)

    def test_no_projects_no_section(self):
        md = self.build(stack=[{'id': 'python', 'label': 'Python'}])
        self.assertNotIn('projects.svg', md)
        self.assertNotIn('<ul>', md)


class ClosingArt(Case):
    def art(self):
        (self.dir / 'end.txt').write_text(FULL * 10 + '\n', encoding='utf-8')
        return 'end.txt'

    def test_sits_before_footer_and_after_socials(self):
        md = self.build(closing_art=self.art(), footer={'prompt': 'x %', 'command': 'exit'},
                        socials=[{'id': 'github', 'label': 'GitHub', 'url': 'https://github.com/x'}])
        self.assertLess(md.index('headings/social.svg'), md.index(FULL))
        self.assertLess(md.index(FULL), md.index('x % exit'))

    def test_is_centered_over_the_window(self):
        md = self.build(closing_art=self.art())
        self.assertIn(' ' * 35 + FULL * 10, md)

    def test_works_without_footer(self):
        self.assertTrue(self.build(closing_art=self.art()).rstrip().endswith('```'))


class Stack(Case):
    def test_rows_render_one_paragraph_each(self):
        md = self.build(stack=[[{'id': 'python', 'label': 'Python'}, {'id': 'c', 'label': 'C'}],
                               [{'id': 'react', 'label': 'React'}]])
        rows = re.findall(r'<p>\n(.*?)\n</p>', md, flags=re.S)
        self.assertEqual([r.count('<img') for r in rows], [2, 1])

    def test_flat_list_is_one_row(self):
        md = self.build(stack=[{'id': 'python', 'label': 'Python'}, {'id': 'c', 'label': 'C'}])
        self.assertEqual([r.count('<img') for r in re.findall(r'<p>\n(.*?)\n</p>', md, flags=re.S)], [2])

    def test_every_bundled_icon_fits_the_tile(self):
        icons = json.loads((ROOT / 'scripts/glyphs.json').read_text(encoding='utf-8'))['icons']
        for name, rows in icons.items():
            self.assertEqual(len({len(r) for r in rows}), 1, f'{name} is not rectangular')
            self.assertLessEqual(max(len(rows), len(rows[0])), 14, name)

    def test_icons_leave_paper_visible(self):
        """A glyph that covers the tile hides the card and vanishes on GitHub's dark theme."""
        icons = json.loads((ROOT / 'scripts/glyphs.json').read_text(encoding='utf-8'))['icons']
        for name, rows in icons.items():
            ink = sum(c != '.' for r in rows for c in r)
            self.assertLessEqual(ink / 196, 0.55, name)

    def test_common_stack_needs_no_letter_fallback(self):
        ids = ('csharp dotnet javascript java nodejs nestjs fastapi django nextjs vite tailwind expo astro '
               'shadcn postgresql mysql sqlserver firebase prisma drizzle docker nginx aws cloudflare vercel '
               'git githubactions bitbucket stripe render').split()
        self.build(stack=[{'id': i, 'label': i} for i in ids])
        self.assertNotIn('no bundled glyph', self.result.stderr)


class ArtEditor(Case):
    def edit(self, rows, *args):
        src, dst = self.dir / 'in.txt', self.dir / 'edited.txt'
        src.write_text('\n'.join(rows) + '\n', encoding='utf-8')
        r = run('art.py', src, '--out', dst, *args)
        self.assertEqual(r.returncode, 0, r.stderr)
        return dst.read_text(encoding='utf-8').rstrip('\n').split('\n')

    def test_cut_removes_rows_and_ranges(self):
        rows = [chr(0x2801 + i) * 2 for i in range(6)]
        self.assertEqual(self.edit(rows, '--cut', '1-2,4'), [rows[0], rows[3], rows[5]])

    def test_invert_flips_every_dot(self):
        self.assertEqual(self.edit(['⠁⣾'], '--invert'), ['⣾⠁'])

    def test_outline_hollows_below_the_row_only(self):
        rows = [FULL * 6] * 6
        out = self.edit(rows, '--outline-from', 2)
        self.assertEqual(out[:2], rows[:2])
        self.assertEqual(out[3][2], BLANK)

    def test_output_is_trimmed_and_rectangular(self):
        out = self.edit([BLANK * 4, BLANK + FULL + BLANK * 2, BLANK + FULL * 2, BLANK * 3])
        self.assertEqual(out, [FULL + BLANK, FULL * 2])


if __name__ == '__main__':
    unittest.main()
