# -*- coding: utf-8 -*-
"""Text links to the Bouyon Music 2026 YouTube playlist, in French and English. Runs after
islands.py (both generators call it at the end):

  python3 build/playlist_links.py            # apply
  python3 build/playlist_links.py --refresh  # re-read the playlist with yt-dlp, rewrite playlist_members.json

Embedded players do not count as links for search engines, so every page that embeds the
playlist also gets a plain link under the player. Every artist profile gets a "Listen" line:
artists with a song in the playlist are named, the others get the general line. The home page,
the artists page and the island page get one line under the lead.
Blocks sit between <!-- playlist:NAME:start --> and <!-- playlist:NAME:end --> markers.
"""
import html, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import islands

ROOT = islands.ROOT
PL_ID = 'PLB1axoRydQreXaKD2wlZ5IHJmNmoTWEEd'
PL_URL = f'https://www.youtube.com/playlist?list={PL_ID}'
PL_NAME = 'Bouyon Music 2026'
MEMBERS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'playlist_members.json')

T = {
 'en': dict(
   member='Listen: hear {artist} in the <a href="{url}">{pl} playlist on YouTube</a>, the newest bouyon songs from Dominica and the islands, updated every month.',
   general='Listen: the <a href="{url}">{pl} playlist on YouTube</a> collects the newest bouyon songs from Dominica and the islands, updated every month.',
   under='<a href="{url}">Open the {pl} playlist on YouTube</a> to save it and get new bouyon songs as they drop.',
   page='Listen while you browse: the <a href="{url}">{pl} playlist on YouTube</a>, the newest bouyon songs, updated every month.'),
 'fr': dict(
   member='Écouter : retrouvez {artist} dans la <a href="{url}">playlist {pl} sur YouTube</a>, les derniers sons bouyon de la Dominique et des îles, mise à jour chaque mois.',
   general='Écouter : la <a href="{url}">playlist {pl} sur YouTube</a> réunit les derniers sons bouyon de la Dominique et des îles, mise à jour chaque mois.',
   under='<a href="{url}">Ouvrir la playlist {pl} sur YouTube</a> pour l\'enregistrer et recevoir les nouveaux sons bouyon dès leur sortie.',
   page='À écouter en naviguant : la <a href="{url}">playlist {pl} sur YouTube</a>, les derniers sons bouyon, mise à jour chaque mois.'),
}
PAGES = {'en': ['en/index.html', 'en/artists.html', 'en/bouyon-by-island.html'],
         'fr': ['index.html', 'artistes.html', 'bouyon-par-ile.html']}

def block(s, name, new, after=None, after_lead=False):
    a, b = f'<!-- playlist:{name}:start -->', f'<!-- playlist:{name}:end -->'
    blk = f'{a}\n{new}\n{b}\n'
    if a in s:
        return re.sub(re.escape(a) + r'.*?' + re.escape(b) + r'\n?', lambda m: blk, s, flags=re.S)
    if after and after in s:
        i = s.index(after) + len(after)
        return s[:i] + '\n' + blk + s[i:].lstrip('\n')
    if after_lead and '<p class="lead">' in s:
        i = s.index('<p class="lead">'); j = s.index('</p>', i) + len('</p>')
        return s[:j] + '\n' + blk + s[j:].lstrip('\n')
    return s

def refresh():
    out = subprocess.check_output(['yt-dlp', '--flat-playlist', '-J', PL_URL], timeout=300)
    titles = [e['title'] for e in json.loads(out)['entries'] if e.get('title')]
    names = islands.profiles(islands.T['en'])
    hits = {}
    for sl, n in names.items():
        k = islands.key(n)
        if len(k) < 3:
            continue
        pat = re.compile(r'(?<![a-z0-9])' + re.escape(k) + r'(?![a-z0-9])')
        if any(pat.search(islands.key(t)) for t in titles):
            hits[sl] = n
    json.dump({'playlist': PL_ID, 'videos': len(titles), 'members': dict(sorted(hits.items()))},
              open(MEMBERS, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('playlist members:', len(hits), 'of', len(names), 'profiles')

def write(p, s0, s):
    if s != s0:
        open(p, 'w', encoding='utf-8').write(s)
        return 1
    return 0

def apply_playlist_links():
    members = json.load(open(MEMBERS, encoding='utf-8'))['members'] if os.path.exists(MEMBERS) else {}
    for lg, t in T.items():
        it = islands.T[lg]
        names = islands.profiles(it)
        n = 0
        for sl, nm in names.items():
            p = os.path.join(ROOT, it['prefix'].lstrip('/'), sl + '.html')
            s = open(p, encoding='utf-8').read()
            txt = (t['member'].format(artist=html.escape(nm), url=PL_URL, pl=PL_NAME) if sl in members
                   else t['general'].format(url=PL_URL, pl=PL_NAME))
            line = f'<p class="listen-tag">{txt}</p>'
            n += write(p, s, block(s, 'listen', line, after='<!-- islands:tag:end -->', after_lead=True))
        emb = 0
        for p in sorted(set(__import__('glob').glob(os.path.join(ROOT, it['glob'])))):
            s = open(p, encoding='utf-8').read()
            if f'embed/videoseries?list={PL_ID}' not in s:
                continue
            i = s.index(f'embed/videoseries?list={PL_ID}'); j = s.index('</div>', i) + len('</div>')
            if '<!-- playlist:under:start -->' not in s:
                s2 = s[:j] + '\n<!-- playlist:under:start -->\n<!-- playlist:under:end -->' + s[j:]
            else:
                s2 = s
            s2 = block(s2, 'under', f'<p>{t["under"].format(url=PL_URL, pl=PL_NAME)}</p>')
            emb += write(p, s, s2)
        pg = 0
        for rel in PAGES[lg]:
            p = os.path.join(ROOT, rel)
            if not os.path.exists(p):
                continue
            s = open(p, encoding='utf-8').read()
            line = f'<p class="listen-tag">{t["page"].format(url=PL_URL, pl=PL_NAME)}</p>'
            pg += write(p, s, block(s, 'page', line, after='<!-- islands:hubs:end -->', after_lead=True))
        print(lg, 'playlist links: profiles', n, '(named', sum(1 for x in names if x in members), ') embeds', emb, 'pages', pg)

if __name__ == '__main__':
    if '--refresh' in sys.argv:
        refresh()
    apply_playlist_links()
