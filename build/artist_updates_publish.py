#!/usr/bin/env python3
"""Publish artist updates marked Ready in Airtable onto bouyonmusique.com (runs in GitHub Actions).

For each Update with Status=Ready: append a marked block to the artist's build/parity_parts file (a new dated section at
the top of the FR and EN page, optional FAQ replacements, date_modified). The workflow then regenerates the site, runs
verify_site.py, commits and pushes. Phases:
  apply                 write the blocks; prints JSON of what was applied to state/artist_updates_applied.json
  check-built           confirm the generated pages show each update heading
  mark-published URL    after deploy: confirm live pages, mark Updates Published, Findings Published, Artist date
Env: AIRTABLE_TOKEN, AIRTABLE_BASE_ID. Stdlib only.
"""
import datetime, glob, html, json, os, re, sys, time, urllib.parse, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / 'build' / '.artist_updates_applied.json'
SITE = 'https://bouyonmusique.com'
TODAY = datetime.date.today()
MONTHS_FR = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']


def api(method, path, body=None, params=None):
    url = f"https://api.airtable.com/v0/{os.environ['AIRTABLE_BASE_ID']}/{path}"
    if params:
        url += '?' + urllib.parse.urlencode(params, doseq=True)
    for attempt in range(5):
        req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None,
                                     headers={'Authorization': f"Bearer {os.environ['AIRTABLE_TOKEN']}", 'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                time.sleep(0.25)
                return json.loads(r.read() or b'{}')
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                time.sleep(15 * (attempt + 1)); continue
            sys.exit(f'Airtable {method} {path} -> {e.code}: {e.read().decode()[:400]}')
        except (TimeoutError, urllib.error.URLError):
            time.sleep(15 * (attempt + 1))
    sys.exit(f'Airtable {method} {path} failed')


def update(table, rows):
    for i in range(0, len(rows), 10):
        api('PATCH', urllib.parse.quote(table), {'records': rows[i:i + 10], 'typecast': True})


def no_dashes(s):
    return s.replace(' — ', ', ').replace('—', ', ').replace(' – ', ', ').replace('–', '-')


def paragraphs(text):
    ps = [p.strip() for p in re.split(r'\n\s*\n', (text or '').strip()) if p.strip()]
    if ps and re.fullmatch(r'(Update|Mise à jour)[^.\n]{0,40}', ps[0]):
        ps = ps[1:]
    out = []
    for p in ps:
        p = html.escape(no_dashes(' '.join(p.split())), quote=False)
        out.append(re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)',
                          lambda m: f'<a href="{html.escape(m.group(2))}" rel="noopener">{m.group(1)}</a>', p))
    return out


def faq(text):
    items = []
    for b in re.split(r'\n\s*\n', (text or '').strip()):
        m = re.match(r'Q:\s*(.+?)\nA:\s*(.+)', b.strip(), re.S)
        if m:
            items.append((no_dashes(m.group(1).strip()), html.escape(no_dashes(' '.join(m.group(2).split())), quote=False)))
    return items


def headings(f, day):
    return (no_dashes(f.get('Heading EN') or f'Update, {day:%B} {day.day}, {day.year}'),
            no_dashes(f.get('Heading FR') or f'Mise à jour du {day.day} {MONTHS_FR[day.month - 1]} {day.year}'))


def cmd_apply():
    ready = api('GET', 'Updates', params={'filterByFormula': "{Status}='Ready'", 'pageSize': 50})['records']
    applied = []
    for u in ready:
        f = u['fields']
        try:
            if not f.get('Artist'):
                raise ValueError('no Artist linked')
            artist = api('GET', f"Artists/{f['Artist'][0]}")['fields']
            slug = artist['Slug']
            parts = glob.glob(str(ROOT / 'build' / 'parity_parts' / f'*_{slug[:-5]}.py'))
            if len(parts) != 1:
                raise ValueError(f'expected one parity part for {slug}, found {len(parts)}')
            en, fr = paragraphs(f.get('Draft EN')), paragraphs(f.get('Draft FR'))
            if not en or not fr:
                raise ValueError('Draft EN and Draft FR are both required')
            h_en, h_fr = headings(f, TODAY)
            part = Path(parts[0]); src = part.read_text(encoding='utf-8')
            marker = f'artist-update {u["id"]}'
            if marker not in src:
                fn = f'_apply_update_{u["id"]}'
                block = '\n'.join([
                    f'\n\n# --- {marker} ({TODAY.isoformat()}), published from the Airtable artist-updates base ---',
                    f'def {fn}(page, section, faq, day):',
                    '    page["sections"] = [section] + [s for s in page["sections"] if s[0] != section[0]]',
                    '    for q, a in faq:',
                    '        rows = [i for i, x in enumerate(page["faq"]) if x[0] == q]',
                    '        if rows: page["faq"][rows[0]] = (q, a)',
                    '        else: page["faq"].append((q, a))',
                    '    page["date_modified"] = day',
                    f'{fn}(FR, {(h_fr, fr)!r}, {faq(f.get("FAQ FR"))!r}, {TODAY.isoformat()!r})',
                    f'{fn}(EN, {(h_en, en)!r}, {faq(f.get("FAQ EN"))!r}, {TODAY.isoformat()!r})', ''])
                part.write_text(src.rstrip('\n') + block, encoding='utf-8')
                import runpy
                m = runpy.run_path(str(part))  # must still load, with the update first
                assert m['FR']['sections'][0][0] == h_fr and m['EN']['sections'][0][0] == h_en
            applied.append({'id': u['id'], 'artist_id': f['Artist'][0], 'name': artist['Stage Name'], 'slug': slug,
                            'h_en': h_en, 'h_fr': h_fr, 'findings': f.get('Findings', [])})
            print('applied', artist['Stage Name'], slug)
        except Exception as e:
            print('SKIP', u['id'], e)
            update('Updates', [{'id': u['id'], 'fields': {'Publish Log': f'{TODAY} not published: {e}'}}])
    STATE.write_text(json.dumps(applied, indent=1, ensure_ascii=False))
    gh_out = os.environ.get('GITHUB_OUTPUT')
    if gh_out:
        with open(gh_out, 'a') as o:
            o.write(f"count={len(applied)}\nnames={', '.join(a['name'] for a in applied)}\n")
    print(len(applied), 'update(s) applied')


def shows(text, h):
    return html.escape(h, quote=False) in text


def cmd_check_built():
    for a in json.loads(STATE.read_text()):
        fr = (ROOT / a['slug']).read_text(encoding='utf-8'); en = (ROOT / 'en' / a['slug']).read_text(encoding='utf-8')
        if not (shows(fr, a['h_fr']) and shows(en, a['h_en'])):
            sys.exit(f"built pages for {a['slug']} do not show the update heading")
    print('built pages ok')


def fetch(url):
    req = urllib.request.Request(f'{url}?v={int(time.time())}', headers={'User-Agent': 'bouyon-artist-updates', 'Cache-Control': 'no-cache'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8', 'replace')


def cmd_mark_published(commit, run_url):
    applied = json.loads(STATE.read_text())
    deadline = time.time() + 900
    pending = list(applied)
    while pending and time.time() < deadline:
        time.sleep(30)
        for a in list(pending):
            try:
                if shows(fetch(f"{SITE}/{a['slug']}"), a['h_fr']) and shows(fetch(f"{SITE}/en/{a['slug']}"), a['h_en']):
                    pending.remove(a)
                    update('Updates', [{'id': a['id'], 'fields': {'Status': 'Published', 'Published URL': f"{SITE}/{a['slug']}",
                                       'Published On': TODAY.isoformat(), 'Commit': commit[:12], 'Publish Log': f'Published by GitHub Actions: {run_url}'}}])
                    update('Artists', [{'id': a['artist_id'], 'fields': {'Last Published Update': TODAY.isoformat()}}])
                    if a['findings']:
                        update('Findings', [{'id': i, 'fields': {'Review': 'Published'}} for i in a['findings']])
                    print('live:', a['slug'])
            except Exception as e:
                print('live check:', a['slug'], e)
    for a in pending:
        update('Updates', [{'id': a['id'], 'fields': {'Commit': commit[:12], 'Publish Log': f'Pushed but not confirmed live after 15 min: {run_url}'}}])
    if pending:
        sys.exit(f'{len(pending)} update(s) not confirmed live')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'apply': cmd_apply()
    elif cmd == 'check-built': cmd_check_built()
    elif cmd == 'mark-published': cmd_mark_published(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else '')
    else: sys.exit(__doc__)
