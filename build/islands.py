# -*- coding: utf-8 -*-
"""Island structure for bouyonmusique.com, from islands_data.py. Run from the repository root
after both generators (they call it at the end):

  python3 build/islands.py

It writes, in French and English:
  - the island page: /bouyon-par-ile.html and /en/bouyon-by-island.html (every island, every artist)
  - a full roster on each island hub (artistes-dominique / artists-dominica, Guadeloupe, Martinique)
  - an island line under the lead of every artist profile, linking to its island
  - the A to Z list of every profile, with flags, on artistes.html and en/artists.html
Generated blocks sit between <!-- islands:NAME:start --> and <!-- islands:NAME:end --> markers,
so a rerun replaces them. It adds the two island pages to the sitemaps once.
"""
import glob, html, json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from islands_data import ISLANDS, links_for

ROOT = os.environ.get('BOUYONMUSIQUE_SITE', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = 'https://bouyonmusique.com'
ISL = {i[0]: dict(code=i[0], flag=i[1], en=i[2], fr=i[3], anchor=i[4], hub_en=i[5], hub_fr=i[6], place_en=i[7], place_fr=i[8]) for i in ISLANDS}

T = {
 'en': dict(
   page='en/bouyon-by-island.html', artists='en/artists.html', prefix='/en/', glob='en/*.html',
   home='/en/', home_name='Home', artists_name='Bouyon artists', artists_url='/en/artists.html',
   title='Bouyon Artists by Island: Dominica, Guadeloupe, Martinique and More',
   desc='Every bouyon artist on Bouyon Musique, island by island: Dominica, Guadeloupe, Martinique, Saint Martin, Saint Lucia, Antigua, Barbados, Saint Vincent and beyond.',
   h1='Bouyon artists by island',
   lead='Bouyon was born in Dominica in 1988 and now runs through the whole Lesser Antilles. This page files every artist profile on the site under its island, using only what each profile states.',
   rule='Two kinds of link: <strong>from</strong> means the profile states where the artist comes from; <strong>scene</strong> means the profile places the artist in that island\'s circuit or on releases billed for it, without stating a birthplace. Artists whose profile states neither are listed at the end, not guessed.',
   from_='From {name}', scene='{name} scene and releases', none_title='Origin not stated',
   none_text='These profiles do not state an island, so none is assigned. Each profile explains what the sources say.',
   hub='All {name} artists', place='Bouyon in {name}', count='{n} artists',
   beyond_title='Beyond the Caribbean', island_word='Island', scene_word='Scene', notstated='Island: not stated in the sources',
   all_islands='All islands', tag_from='from', tag_scene='scene',
   roster_title='Every {name} artist on Bouyon Musique',
   roster_intro='{n} profiles, from the island page. Scene means the profile places the artist in the {name} circuit without stating a birthplace.',
   az_title='All artists A to Z', az_intro='{n} artist profiles in alphabetical order, with the island their profile states.',
   hubs_title='By island', colon=': ', faq='<h2>Frequently asked questions</h2>', lang='en', locale='en_US'),
 'fr': dict(
   page='bouyon-par-ile.html', artists='artistes.html', prefix='/', glob='*.html',
   home='/', home_name='Accueil', artists_name='Artistes bouyon', artists_url='/artistes.html',
   title='Artistes bouyon par île : Dominique, Guadeloupe, Martinique et plus',
   desc='Tous les artistes bouyon de Bouyon Musique, île par île : Dominique, Guadeloupe, Martinique, Saint-Martin, Sainte-Lucie, Antigua, Barbade, Saint-Vincent et au-delà.',
   h1='Les artistes bouyon par île',
   lead='Le bouyon est né en Dominique en 1988 et traverse aujourd\'hui toutes les Petites Antilles. Cette page range chaque fiche artiste du site sous son île, en s\'appuyant uniquement sur ce que dit chaque fiche.',
   rule='Deux types de lien : <strong>origine</strong> signifie que la fiche indique d\'où vient l\'artiste ; <strong>scène</strong> signifie que la fiche le place dans le circuit de l\'île ou sur des sorties annoncées pour elle, sans lieu de naissance. Les artistes dont la fiche n\'indique ni l\'un ni l\'autre sont listés à la fin, sans supposition.',
   from_='Origine : {name}', scene='Scène et sorties : {name}', none_title='Origine non indiquée',
   none_text='Ces fiches n\'indiquent pas d\'île, donc aucune ne leur est attribuée. Chaque fiche explique ce que disent les sources.',
   hub='Tous les artistes : {name}', place='Le bouyon : {name}', count='{n} artistes',
   beyond_title='Au-delà de la Caraïbe', island_word='Île', scene_word='Scène', notstated='Île : non indiquée par les sources',
   all_islands='Toutes les îles', tag_from='origine', tag_scene='scène',
   roster_title='Le roster complet : {name}',
   roster_intro='{n} fiches, reprises de la page par île. Scène signifie que la fiche place l\'artiste dans le circuit de l\'île sans indiquer de lieu de naissance.',
   az_title='Tous les artistes de A à Z', az_intro='{n} fiches artistes par ordre alphabétique, avec l\'île indiquée par leur fiche.',
   hubs_title='Par île', colon=' : ', faq='<h2>Questions fréquentes</h2>', lang='fr', locale='fr_FR'),
}
BEYOND = ('fr', 'us', 'ca')

def key(name):
    return unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode().lower()

def profiles(t):
    """{slug: display name} for every profile page in this language."""
    out = {}
    for f in glob.glob(os.path.join(ROOT, t['glob'])):
        s = open(f, encoding='utf-8').read()
        if '"MusicGroup"' not in s or '<p class="lead">' not in s:
            continue
        name = None
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                d = json.loads(m.group(1))
            except ValueError:
                continue
            for it in (d.get('@graph', [d]) if isinstance(d, dict) else d):
                if isinstance(it, dict) and it.get('@type') == 'BreadcrumbList' and it.get('itemListElement'):
                    name = it['itemListElement'][-1].get('name')
        if name:
            out[os.path.basename(f)[:-5]] = name.strip()
    return out

def iname(code, t):
    return ISL[code][t['lang']]

def island_href(code, t):
    return f"{t['prefix']}{os.path.basename(t['page'])}#{ISL[code]['anchor']}"

def alink(slug, names, t):
    return f'<a href="{t["prefix"]}{slug}.html">{html.escape(names[slug])}</a>'

def replace_block(s, name, new, anchor_before=None, anchor_after_lead=False):
    a, b = f'<!-- islands:{name}:start -->', f'<!-- islands:{name}:end -->'
    block = f'{a}\n{new}\n{b}\n'
    if a in s:
        return re.sub(re.escape(a) + r'.*?' + re.escape(b) + r'\n?', lambda m: block, s, flags=re.S)
    if anchor_after_lead:
        i = s.index('<p class="lead">'); j = s.index('</p>', i) + len('</p>')
        return s[:j] + '\n' + block + s[j:].lstrip('\n')
    if anchor_before and anchor_before in s:
        return s.replace(anchor_before, block + '\n' + anchor_before, 1)
    return s

def members(code, kind, names):
    return sorted([sl for sl in names if (code, kind) in links_for(sl)], key=lambda sl: key(names[sl]))

def island_section(code, names, t, heading='h2'):
    i = ISL[code]; nm = iname(code, t)
    fr_, sc = members(code, 'from', names), members(code, 'scene', names)
    extra = []
    hub = i['hub_' + t['lang']]; place = i['place_' + t['lang']]
    if hub: extra.append(f'<a href="{hub}">{t["hub"].format(name=nm)}</a>')
    if place: extra.append(f'<a href="{place}">{t["place"].format(name=nm)}</a>')
    out = [f'<{heading} id="{i["anchor"]}">{i["flag"]} {nm}</{heading}>',
           f'<p class="small">{t["count"].format(n=len(fr_) + len(sc))}' + (' · ' + ' · '.join(extra) if extra else '') + '</p>']
    if fr_:
        out.append(f'<h3 class="az-head">{t["from_"].format(name=nm)}</h3>\n<p class="az-list">' + ' · '.join(alink(x, names, t) for x in fr_) + '</p>')
    if sc:
        out.append(f'<h3 class="az-head">{t["scene"].format(name=nm)}</h3>\n<p class="az-list">' + ' · '.join(alink(x, names, t) for x in sc) + '</p>')
    return '\n'.join(out)

def flags_of(slug):
    return ''.join(ISL[c]['flag'] for c, _ in links_for(slug))

def island_page(names, t):
    tpl = open(os.path.join(ROOT, t['artists']), encoding='utf-8').read()
    url = BASE + '/' + t['page']
    other = T['fr' if t['lang'] == 'en' else 'en']
    jump = ' '.join(f'<a href="#{ISL[c]["anchor"]}">{ISL[c]["flag"]} {iname(c, t)}</a>' for c in ISL) + f' <a href="#not-stated">{t["none_title"]}</a>'
    sections = [island_section(c, names, t) for c in ISL if c not in BEYOND]
    sections.append(f'<h2>{t["beyond_title"]}</h2>')
    sections += [island_section(c, names, t, 'h2') for c in BEYOND]
    none = sorted([sl for sl in names if not links_for(sl)], key=lambda sl: key(names[sl]))
    sections.append(f'<h2 id="not-stated">{t["none_title"]}</h2>\n<p>{t["none_text"]} ({len(none)})</p>\n<p class="az-list">' + ' · '.join(alink(x, names, t) for x in none) + '</p>')
    main = f'''<main>
<div class="wrap">
<p class="breadcrumb"><a href="{t["home"]}">{t["home_name"]}</a> / <a href="{t["artists_url"]}">{t["artists_name"]}</a> / {t["h1"]}</p>
<h1>{t["h1"]}</h1>
<p class="lead">{t["lead"]}</p>
<p>{t["rule"]}</p>
<p class="az-letters">{jump}</p>
{chr(10).join(sections)}
</div>
</main>'''
    s = tpl[:tpl.index('<main>')] + main + tpl[tpl.index('</main>') + len('</main>'):]
    s = re.sub(r'<title>.*?</title>', f'<title>{t["title"]}</title>', s, count=1)
    for prop in ('name="description"', 'property="og:description"'):
        s = re.sub(r'(<meta ' + re.escape(prop) + r' content=")[^"]*', lambda m: m.group(1) + html.escape(t['desc'], quote=True), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + t['title'], s, count=1)
    s = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    s = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, s, count=1)
    hre = {t['lang']: url, other['lang']: BASE + '/' + other['page']}
    for lg in ('en', 'fr'):
        s = re.sub(r'(<link rel="alternate" hreflang="' + lg + r'" href=")[^"]*', lambda m, lg=lg: m.group(1) + hre[lg], s, count=1)
    s = re.sub(r'(<link rel="alternate" hreflang="x-default" href=")[^"]*', lambda m: m.group(1) + hre['fr'], s, count=1)
    items = [{'@type': 'ListItem', 'position': n + 1, 'name': names[sl], 'url': BASE + t['prefix'] + sl + '.html'}
             for n, sl in enumerate(sorted([x for x in names if links_for(x)], key=lambda x: key(names[x])))]
    ld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'CollectionPage', '@id': url + '#page', 'url': url, 'name': t['title'], 'description': t['desc'], 'inLanguage': t['lang'],
         'isPartOf': {'@id': BASE + '/#site'}, 'publisher': {'@id': BASE + '/#org'}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': t['home_name'], 'item': BASE + t['home']},
            {'@type': 'ListItem', 'position': 2, 'name': t['artists_name'], 'item': BASE + t['artists_url']},
            {'@type': 'ListItem', 'position': 3, 'name': t['h1'], 'item': url}]},
        {'@type': 'ItemList', 'name': t['h1'], 'numberOfItems': len(items), 'itemListElement': items}]}
    s = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + '\n</script>', s, count=1, flags=re.S)
    open(os.path.join(ROOT, t['page']), 'w', encoding='utf-8').write(s)

def profile_line(slug, t):
    lk = links_for(slug)
    page = t['prefix'] + os.path.basename(t['page'])
    if not lk:
        return f'<p class="island-tag">{t["notstated"]} · <a href="{page}#not-stated">{t["all_islands"]}</a></p>'
    parts = []
    for c, kind in lk:
        i = ISL[c]; target = i['hub_' + t['lang']] or island_href(c, t)
        mixed = any(k == 'from' for _, k in lk) and any(k == 'scene' for _, k in lk)
        parts.append(f'{i["flag"]} <a href="{target}">{iname(c, t)}</a>' + (f' ({t["tag_" + kind]})' if mixed else ''))
    word = t['island_word'] if any(k == 'from' for _, k in lk) else t['scene_word']
    return f'<p class="island-tag">{word}{t["colon"]}' + ' · '.join(parts) + f' · <a href="{page}">{t["all_islands"]}</a></p>'

def az_block(names, t):
    groups = {}
    for sl in sorted(names, key=lambda x: key(names[x])):
        c = key(names[sl])[:1].upper()
        groups.setdefault(c if c.isalpha() else '#', []).append(sl)
    order = sorted(groups, key=lambda k: (k != '#', k))
    anc = lambda k: 'az-num' if k == '#' else 'az-' + k.lower()
    out = [f'<h2 id="a-z">{t["az_title"]}</h2>', f'<p>{t["az_intro"].format(n=len(names))}</p>',
           '<p class="az-letters">' + ' '.join(f'<a href="#{anc(k)}">{k}</a>' for k in order) + '</p>']
    for k in order:
        out.append(f'<h3 id="{anc(k)}" class="az-head">{k}</h3>\n<p class="az-list">' +
                   ' · '.join(alink(sl, names, t) + (f' {flags_of(sl)}' if flags_of(sl) else '') for sl in groups[k]) + '</p>')
    return '\n'.join(out)

def hubs_line(t):
    page = t['prefix'] + os.path.basename(t['page'])
    links = ' · '.join(f'{ISL[c]["flag"]} <a href="{ISL[c]["hub_" + t["lang"]] or island_href(c, t)}">{iname(c, t)}</a>' for c in ISL if c not in BEYOND)
    return f'<p class="az-hubs"><strong>{t["hubs_title"]}</strong>{t["colon"]} {links} · <a href="{page}"><strong>{t["all_islands"]}</strong></a> · <a href="#a-z">A-Z</a></p>'

def add_sitemap(path, url, lastmod):
    p = os.path.join(ROOT, path); s = open(p, encoding='utf-8').read()
    if f'<loc>{url}</loc>' in s:
        return
    entry = f'  <url>\n    <loc>{url}</loc>\n    <lastmod>{lastmod}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
    open(p, 'w', encoding='utf-8').write(s.replace('</urlset>', entry + '</urlset>'))

def apply_islands(lastmod='2026-10-24'):
    for lg, t in T.items():
        names = profiles(t)
        island_page(names, t)
        for sl in names:
            p = os.path.join(ROOT, t['prefix'].lstrip('/'), sl + '.html')
            s = open(p, encoding='utf-8').read()
            s2 = replace_block(s, 'tag', profile_line(sl, t), anchor_after_lead=True)
            if s2 != s: open(p, 'w', encoding='utf-8').write(s2)
        for c in ISL:
            hub = ISL[c]['hub_' + lg]
            if not hub: continue
            p = os.path.join(ROOT, hub.lstrip('/')); s = open(p, encoding='utf-8').read()
            n = len(members(c, 'from', names)) + len(members(c, 'scene', names))
            roster = (f'<h2 id="roster">{t["roster_title"].format(name=iname(c, t))}</h2>\n<p>{t["roster_intro"].format(n=n, name=iname(c, t))} '
                      f'<a href="{island_href(c, t)}">{t["all_islands"]}</a></p>\n' + island_section(c, names, t, 'h3').split('\n', 2)[2])
            open(p, 'w', encoding='utf-8').write(replace_block(s, 'roster', roster, anchor_before=t['faq']))
        p = os.path.join(ROOT, t['artists']); s = open(p, encoding='utf-8').read()
        s = re.sub(r'<!-- artist-index:start -->.*?<!-- artist-index:end -->\n*', '', s, flags=re.S)
        s = re.sub(r'<!-- artist-hubs:start -->.*?<!-- artist-hubs:end -->\n', '', s, flags=re.S)
        s = replace_block(s, 'hubs', hubs_line(t), anchor_after_lead=True)
        s = replace_block(s, 'az', az_block(names, t), anchor_before=t['faq'])
        open(p, 'w', encoding='utf-8').write(s)
        add_sitemap('sitemap-en.xml' if lg == 'en' else 'sitemap-pages.xml', BASE + '/' + t['page'], lastmod)
        print(lg, len(names), 'profiles,', sum(1 for x in names if links_for(x)), 'placed on an island')

if __name__ == '__main__':
    apply_islands()
