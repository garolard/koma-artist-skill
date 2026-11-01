import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('prepare', Path(__file__).parents[1] / 'skills' / 'koma-artist-prepare' / 'scripts' / 'prepare.py')
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PrepareTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'original.jpg').write_bytes(b'original bytes')
        self.plan = self.root / 'plan.json'
        self.output = self.root / 'panels'

    def write_plan(self, panels):
        self.plan.write_text(json.dumps({'panels': panels}), encoding='utf-8')

    def test_copies_without_altering_original(self):
        self.write_plan([{'slot': 1, 'source': 'original.jpg', 'title': 'Lantern Alley'}])
        module.prepare(self.plan, self.output)
        self.assertEqual((self.output / '01 - Lantern Alley.jpg').read_bytes(), b'original bytes')
        self.assertEqual((self.root / 'original.jpg').read_bytes(), b'original bytes')

    def test_invalid_plan_never_creates_output(self):
        for panel in [
            {'slot': 2, 'source': 'original.jpg', 'title': 'Alley'},
            {'slot': 1, 'source': 'missing.jpg', 'title': 'Alley'},
            {'slot': 1, 'source': 'original.jpg', 'title': '../Alley'},
            {'slot': 1, 'source': 'original.jpg', 'title': '01 Alley'},
        ]:
            self.write_plan([panel])
            with self.assertRaises((ValueError, OSError)):
                module.prepare(self.plan, self.output)
            self.assertFalse(self.output.exists())

    def write_numbered_plan(self, count, template=None):
        for n in range(1, count + 1):
            (self.root / f'art{n}.jpg').write_bytes(f'art {n}'.encode())
        panels = [{'slot': n, 'source': f'art{n}.jpg', 'title': f'Panel {n}'} for n in range(1, count + 1)]
        plan = {'panels': panels} if template is None else {'template': template, 'panels': panels}
        self.plan.write_text(json.dumps(plan), encoding='utf-8')

    def test_template_sizes_are_enforced(self):
        for template, size in [('standard-v1', 49), ('small-v1', 25), ('mini-v1', 16)]:
            with self.subTest(template=template):
                self.write_numbered_plan(size + 1, template)
                with self.assertRaises(ValueError):
                    module.prepare(self.plan, self.output)
                self.assertFalse(self.output.exists())
                self.write_numbered_plan(size, template)
                module.prepare(self.plan, self.output)
                self.assertEqual(len(list(self.output.iterdir())), size)
                for path in self.output.iterdir():
                    path.unlink()
                self.output.rmdir()

    def test_default_template_is_standard(self):
        self.write_numbered_plan(26)
        module.prepare(self.plan, self.output)
        self.assertEqual(len(list(self.output.iterdir())), 26)

    def test_unknown_template_is_rejected(self):
        self.write_numbered_plan(1, 'large-v1')
        with self.assertRaises(ValueError):
            module.prepare(self.plan, self.output)
        self.assertFalse(self.output.exists())

    def test_existing_output_is_not_modified(self):
        self.output.mkdir()
        (self.output / 'keep').write_text('keep')
        self.write_plan([{'slot': 1, 'source': 'original.jpg', 'title': 'Alley'}])
        with self.assertRaises(ValueError):
            module.prepare(self.plan, self.output)
        self.assertEqual((self.output / 'keep').read_text(), 'keep')


if __name__ == '__main__':
    unittest.main()
