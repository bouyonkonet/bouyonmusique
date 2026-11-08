"""Contextual links between the listening and event pages and the pages that support them.

Each entry in context_links.json adds one sentence at the end of a content paragraph of a generated page
(paragraph 0 is the lead, the first paragraph after the byline). The sentence sits between
<!--ctx:ID--> and <!--/ctx--> markers, so a rerun replaces it instead of adding it twice.
Both generators call apply_context_links() at the end; `python3 build/context_links.py` reapplies it alone.
"""
from pathlib import Path
import json
import re

DATA = Path(__file__).with_name('context_links.json')
MARK = re.compile(r'<!--ctx:[A-Za-z0-9_-]+-->.*?<!--/ctx-->', re.S)
PARA = re.compile(r'<p\b[^>]*>(.*?)</p>', re.S)


def _content_paragraphs(text):
    """(start, end) of each prose paragraph inside <main>.

    Skipped: the breadcrumb, the byline, image-only paragraphs, the island and listen lines of the
    profiles, and any paragraph of fewer than 12 words.
    """
    m0 = text.find('<main')
    m1 = text.find('</main>', m0)
    if m0 < 0 or m1 < 0:
        return []
    out = []
    for m in PARA.finditer(text, m0, m1):
        if re.search(r'class="[^"]*(breadcrumb|pubdate)', m.group(0)[:120]):
            continue
        inner = m.group(1)
        plain = re.sub(r'<[^>]+>', ' ', inner)
        if ('rel="author"' in inner or re.match(r'\s*<(source|img|picture)\b', inner)
                or re.match(r'\s*(Island|Île|Scene|Scène|Listen|Écouter)\s?:', plain)
                or len(plain.split()) < 12):
            continue
        out.append((m.start(1), m.end(1)))
    return out


def apply_context_links(site_root=None):
    root = Path(site_root) if site_root else Path(__file__).resolve().parents[1]
    entries = json.loads(DATA.read_text())['pages']
    for name, adds in entries.items():
        page = root / name
        if not page.is_file():
            continue
        text = MARK.sub('', page.read_text())
        # Insert from the last paragraph backwards so earlier offsets stay valid.
        for add in sorted(adds, key=lambda a: a['para'], reverse=True):
            paras = _content_paragraphs(text)
            if add['para'] >= len(paras):
                raise SystemExit(f'context_links: {name} has no content paragraph {add["para"]}')
            end = paras[add['para']][1]
            block = f'<!--ctx:{add["id"]}--> {add["html"]}<!--/ctx-->'
            text = text[:end] + block + text[end:]
        page.write_text(text)


if __name__ == '__main__':
    import sys
    apply_context_links(sys.argv[1] if len(sys.argv) > 1 else None)
