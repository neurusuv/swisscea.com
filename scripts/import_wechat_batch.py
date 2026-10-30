#!/usr/bin/env python3
"""Import only new IDs; failed articles never leak partial files into the site."""
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit


def article_ids(value):
    result = []
    for token in re.split(r'[\s,]+', value.strip()):
        if not token:
            continue
        if token.startswith('https://'):
            url = urlsplit(token)
            if url.netloc != 'mp.weixin.qq.com' or not url.path.startswith('/s/'):
                raise ValueError('Use a WeChat short ID or https://mp.weixin.qq.com/s/<ID> URL.')
            token = url.path[3:]
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,128}', token):
            raise ValueError(f'Invalid WeChat short ID: {token!r}')
        if token not in result:
            result.append(token)
    if not result:
        raise ValueError('At least one article ID is required.')
    return result


def pending_ids(root, ids):
    return [value for value in ids if not (root / 'docs/news' / f'wechat-{value}.md').exists()]


def import_batch(root, ids, run=subprocess.run):
    imported = 0
    failed = []
    for value in pending_ids(root, ids):
        # The importer writes images before verifying the date. Isolate each
        # article and only promote its files after the importer succeeds.
        with tempfile.TemporaryDirectory(prefix='scea-news-') as temporary:
            staging = Path(temporary)
            news = staging / 'docs/news'
            news.mkdir(parents=True)
            shutil.copy2(root / 'docs/news/index.md', news / 'index.md')
            result = run([sys.executable, str(root / 'scripts/import_wechat_scea.py'), value], cwd=staging)
            article = news / f'wechat-{value}.md'
            if result.returncode or not article.is_file():
                failed.append(value)
                print(f'FAILED {value}; no files from this article were published.', flush=True)
                continue
            shutil.copy2(article, root / 'docs/news' / article.name)
            images = staging / 'docs/public/images/news' / f'wechat-{value}'
            if images.is_dir():
                shutil.copytree(images, root / 'docs/public/images/news' / images.name, dirs_exist_ok=True)
            # Build-time generation maintains both lists. Never overwrite the
            # latest news index with the isolated importer's temporary copy.
            imported += 1
    if failed:
        raise RuntimeError('Import failed for ' + ', '.join(failed) + '; batch will not be committed.')
    return imported


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--plan', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    ids = article_ids(os.environ.get('ARTICLE_IDS', ''))
    pending = pending_ids(root, ids)
    print(f'Requested {len(ids)}, already present {len(ids) - len(pending)}, new {len(pending)}.', flush=True)
    if args.plan:
        output = os.environ.get('GITHUB_OUTPUT')
        if output:
            with open(output, 'a', encoding='utf-8') as handle:
                handle.write(f'pending={len(pending)}\n')
        return
    print(f'Imported {import_batch(root, pending)} new articles.', flush=True)


if __name__ == '__main__':
    main()
