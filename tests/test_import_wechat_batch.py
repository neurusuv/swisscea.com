import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('batch', Path(__file__).resolve().parents[1] / 'scripts/import_wechat_batch.py')
batch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batch)


class ImportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / 'docs/news').mkdir(parents=True)
        (self.root / 'docs/news/index.md').write_text('<ul>original</ul>', encoding='utf-8')

    def test_urls_duplicates_and_rejected_inputs(self):
        self.assertEqual(batch.article_ids('abc, https://mp.weixin.qq.com/s/def?x=1\nabc'), ['abc', 'def'])
        for value in ['', '../escape', '$(whoami)', 'https://example.com/s/abc', 'https://mp.weixin.qq.com.evil/s/abc']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                batch.article_ids(value)

    def test_existing_article_does_not_fetch(self):
        (self.root / 'docs/news/wechat-abc.md').write_text('existing', encoding='utf-8')
        def unexpected(*args, **kwargs):
            self.fail('Existing articles must not trigger a network importer')
        self.assertEqual(batch.import_batch(self.root, ['abc'], unexpected), 0)

    def test_success_promotes_article_and_images_without_overwriting_index(self):
        def succeed(command, cwd):
            article = cwd / 'docs/news/wechat-abc.md'
            article.write_text('complete article', encoding='utf-8')
            (cwd / 'docs/news/index.md').write_text('stale index', encoding='utf-8')
            image = cwd / 'docs/public/images/news/wechat-abc/01.jpg'
            image.parent.mkdir(parents=True)
            image.write_bytes(b'photo')
            return subprocess.CompletedProcess(command, 0)
        self.assertEqual(batch.import_batch(self.root, ['abc'], succeed), 1)
        self.assertEqual((self.root / 'docs/news/wechat-abc.md').read_text(), 'complete article')
        self.assertEqual((self.root / 'docs/public/images/news/wechat-abc/01.jpg').read_bytes(), b'photo')
        self.assertEqual((self.root / 'docs/news/index.md').read_text(), '<ul>original</ul>')

    def test_partial_images_and_article_do_not_escape_failed_import(self):
        def fail(command, cwd):
            image = cwd / 'docs/public/images/news/wechat-abc/01.jpg'
            image.parent.mkdir(parents=True)
            image.write_bytes(b'partial')
            (cwd / 'docs/news/wechat-abc.md').write_text('partial', encoding='utf-8')
            return subprocess.CompletedProcess(command, 1)
        with self.assertRaisesRegex(RuntimeError, 'batch will not be committed'):
            batch.import_batch(self.root, ['abc'], fail)
        self.assertFalse((self.root / 'docs/news/wechat-abc.md').exists())
        self.assertFalse((self.root / 'docs/public').exists())

    def test_success_exit_without_article_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, 'abc'):
            batch.import_batch(self.root, ['abc'], lambda command, cwd: subprocess.CompletedProcess(command, 0))


if __name__ == '__main__':
    unittest.main()
