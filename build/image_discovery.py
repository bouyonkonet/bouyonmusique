"""Build bilingual artist photo pages from the existing, released image catalogue.

No fetching or rollout advancement. Generated pages, file aliases and the image
sitemap are reconciled with the release state on every run.
"""
import html
import hashlib
import json
import re
import struct
from pathlib import Path
from urllib.parse import urlsplit

import images

ROOT = Path(images.ROOT)
BASE = images.BASE
MARKER = '<!-- image-discovery:generated -->'
MANIFEST = Path(images.HERE) / 'image_discovery_manifest.json'
CACHE = Path(images.HERE) / 'image_variants_cache.json'


def esc(value):
    return html.escape(str(value), quote=True)


def dump(value):
    return json.dumps(value, ensure_ascii=False).replace('<', '\\u003c')


def keywords(d):
    name = d['name']
    values = [name, 'bouyon', 'bouyon music', 'musique bouyon',
              f'{name} bouyon', f'{name} music', f'{name} musique',
              f'{name} photo', f'{name} photos', f'{name} picture',
              f'{name} images', f'{name} artiste', f'{name} artist']
    if d.get('island'):
        for lang in ('fr', 'en'):
            label = d['island'][lang]
            values.extend([label, f'{name} {label}', f'bouyon {label}'])
    if d['source']['kind'] == 'youtube':
        values.extend([d['source']['title'], f'{name} video', f'{name} clip'])
    subjects = [name, name+' bouyon', name+' bouyon music', name+' musique bouyon']
    terms = ['photo','photos','picture','pictures','image','images','portrait',
             'artiste','artist','musique','music','gallery','galerie','wallpaper',
             'fond d’écran','clip','video','artwork','cover','visuel']
    values.extend(f'{subject} {term}' for subject in subjects for term in terms)
    return list(dict.fromkeys(v for v in values if v))


def iptc_record(dataset, value):
    raw = value.encode('utf-8')
    return b'\x1c\x02' + bytes([dataset]) + struct.pack('>H', len(raw)) + raw


def jpeg_metadata(raw, d):
    """Add one IPTC APP13 segment without decoding or changing image pixels.

    Called against the immutable source JPEG, so repeated builds do not stack
    metadata segments or recompress the photograph.
    """
    if not raw.startswith(b'\xff\xd8'):
        raise ValueError('Expected JPEG source')
    # UTF-8 coded character set, repeated keyword records, source and credit.
    iptc = b'\x1c\x01\x5a\x00\x03\x1b%G'
    for word in keywords(d):
        # IIM keyword datasets are limited to 64 octets.
        word = word.encode('utf-8')[:64].decode('utf-8', errors='ignore')
        iptc += iptc_record(25, word)
    iptc += iptc_record(120, d['alt_en'])
    iptc += iptc_record(110, d['source']['channel'] or d['name'])
    iptc += iptc_record(115, d['source']['url'])
    resource = b'8BIM\x04\x04\x00\x00' + struct.pack('>I', len(iptc)) + iptc
    if len(iptc) % 2:
        resource += b'\x00'
    payload = b'Photoshop 3.0\x00' + resource
    return raw[:2] + b'\xff\xed' + struct.pack('>H', len(payload) + 2) + payload + raw[2:]


def released():
    data = images._load(images.DATA, {})
    state = images._load(images.ROLLOUT, {})
    overrides = images._load(images.OVERRIDES, {})
    rows = {}
    for slug in sorted(state):
        if overrides.get(slug, {}).get('skip') or slug not in data:
            continue
        d = data[slug]
        if not (ROOT / f'{slug}.html').exists() or not (ROOT / f'en/{slug}.html').exists():
            raise ValueError(f'Missing bilingual artist profile: {slug}')
        for width in (640, 1280):
            for fmt in ('jpg', 'webp'):
                if not (ROOT / f'img/artistes/{d["file"]}-{width}.{fmt}').exists():
                    raise ValueError(f'Missing image variant: {slug}/{width}/{fmt}')
        rows[slug] = d
    return rows, state


def photo_path(slug, lang):
    return ('/en' if lang == 'en' else '') + '/photos/' + (f'{slug}.html' if slug else '')


def variant_path(slug, d, width, fmt, treatment='original'):
    island = '-' + d['island']['anchor'] if d.get('island') else ''
    suffix = '' if treatment=='original' else '-'+treatment
    return f'/img/photos/{slug}-bouyon-music-artiste-photo{island}{suffix}-{width}.{fmt}'


def variants():
    return [(t,w,ext) for t in ('original','banner','square','mirror')
            for w in ((1080,540) if t=='square' else (1280,640)) for ext in ('jpg','webp')]


def image_objects(slug, d, lang):
    return [{
        '@type': 'ImageObject', '@id': BASE + variant_path(slug, d, w, ext, treatment),
        'contentUrl': BASE + variant_path(slug, d, w, ext, treatment),
        'url': BASE + photo_path(slug, lang),
        'name': d['name'] + (' : photo bouyon' if lang == 'fr' else ': bouyon photo') + ' · '+treatment,
        'description': d['alt_' + lang], 'caption': d['caption_' + lang],
        'keywords': keywords(d), 'width': w, 'height': w if treatment=='square' else w * 9 // 16,
        'encodingFormat': 'image/jpeg' if ext == 'jpg' else 'image/webp',
        'creditText': d['source']['channel'] or d['name'],
        'isBasedOn': d['source']['url'],
        'mainEntityOfPage': BASE + photo_path(slug, lang),
    } for treatment,w,ext in variants()]


def picture(slug, d, lang, hero=False):
    alt = d['alt_' + lang] + ' · ' + ' · '.join(keywords(d)[:18])
    title = ' · '.join(keywords(d)[:24])
    src = variant_path(slug, d, 1280 if hero else 640, 'jpg')
    return (f'<picture><source type="image/webp" srcset="{variant_path(slug,d,640,"webp")} 640w, '
            f'{variant_path(slug,d,1280,"webp")} 1280w" sizes="(max-width:640px) 100vw, {1080 if hero else 340}px">'
            f'<img src="{src}" srcset="{variant_path(slug,d,640,"jpg")} 640w, {variant_path(slug,d,1280,"jpg")} 1280w" '
            f'sizes="(max-width:640px) 100vw, {1080 if hero else 340}px" alt="{esc(alt)}" title="{esc(title)}" '
            f'width="1280" height="720" loading="{"eager" if hero else "lazy"}" '
            f'{"fetchpriority=high " if hero else ""}decoding="async"></picture>')


def shell(slug, lang, title, description, body, graph, image_url=None):
    path = photo_path(slug, lang)
    en = lang == 'en'
    prefix = '/en' if en else ''
    other = photo_path(slug, 'fr' if en else 'en')
    return f'''<!DOCTYPE html>
<html lang="{lang}"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
{MARKER}
<title>{esc(title)}</title><meta name="description" content="{esc(description)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{BASE}{path}">
<link rel="alternate" hreflang="fr" href="{BASE}{photo_path(slug,'fr')}">
<link rel="alternate" hreflang="en" href="{BASE}{photo_path(slug,'en')}">
<link rel="alternate" hreflang="x-default" href="{BASE}{photo_path(slug,'fr')}">
<meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{BASE}{path}">
<meta property="og:image" content="{image_url or BASE+'/og-image.png'}"><meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{image_url or BASE+'/og-image.png'}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/style.css">
<link rel="stylesheet" href="/photos/gallery.css">
<script type="application/ld+json">{dump({'@context':'https://schema.org','@graph':graph})}</script>
</head><body><a class="skip" href="#content">{'Skip to content' if en else 'Aller au contenu'}</a>
<header><div class="wrap nav"><a class="logo" href="{prefix}/">BOUYON <span>MUSIQUE</span></a>
<nav class="main"><a href="{prefix}/{'artists' if en else 'artistes'}.html">{'Artists' if en else 'Artistes'}</a>
<a href="{photo_path('',lang)}">Photos</a><a href="{other}" lang="{'fr' if en else 'en'}">{'Français' if en else 'English'}</a></nav></div></header>
<main id="content" class="wrap photo-main">{body}</main>
<footer><div class="wrap"><p>Bouyon Musique · <a href="{prefix}/">{'Home' if en else 'Accueil'}</a> · <a href="{photo_path('',lang)}">{'Artist photos' if en else 'Photos des artistes'}</a></p></div></footer></body></html>
'''


def artist_page(slug, d, lang, state, neighbors):
    en = lang == 'en'
    profile = ('/en/' if en else '/') + slug + '.html'
    title = d['name'] + (': bouyon photos and music' if en else ' : photos et musique bouyon')
    desc = d['alt_' + lang]
    objects = image_objects(slug, d, lang)
    source = d['source']
    island = d.get('island')
    island_line = ''
    if island:
        hub = '/en/bouyon-by-island.html' if en else '/bouyon-par-ile.html'
        island_line = f'<p class="small">{"Scene" if en else "Scène"} : <a href="{hub}#{esc(island["anchor"])}">{esc(island[lang])}</a></p>'
    formats = ''.join(f'<a href="{variant_path(slug,d,w,fmt,t)}">{t.title()} {w} × {w if t=="square" else w*9//16} {fmt.upper()}</a>' for t,w,fmt in variants())
    treatments = ''.join(f'<figure><a href="{variant_path(slug,d,w,"jpg",t)}"><img src="{variant_path(slug,d,w,"jpg",t)}" width="{w}" height="{w if t=="square" else w*9//16}" loading="lazy" alt="{esc(d["name"]+" bouyon "+t)}"></a><figcaption>{t.title()}</figcaption></figure>' for t,w in [('banner',1280),('square',1080),('mirror',1280)])
    links = ''.join(f'<li><a href="{photo_path(s,lang)}">{esc(row["name"])}</a></li>' for s,row in neighbors)
    body = f'''<p class="breadcrumb"><a href="{photo_path('',lang)}">{'Artist photos' if en else 'Photos des artistes'}</a> / {esc(d['name'])}</p>
<p class="kicker">BOUYON EN IMAGES</p><h1>{esc(title)}</h1>{island_line}
<figure class="photo-hero">{picture(slug,d,lang,True)}<figcaption>{esc(d['caption_'+lang])} <a href="{esc(source['url'])}" rel="noopener">{'View source' if en else 'Voir la source'}</a></figcaption></figure>
<div class="photo-info"><section><h2>{'Listen to' if en else 'Écouter'} {esc(d['name'])}</h2>
<p>{'Find the artist biography, releases and listening links in the full profile.' if en else 'Retrouvez la biographie, les titres et les liens d’écoute sur la fiche de l’artiste.'}</p>
<a class="btn" href="{profile}">{'Artist profile and music' if en else 'Biographie et musique'}</a></section>
<section><h2>{'Image source' if en else 'Source de l’image'}</h2><p>{esc(source['title'] or d['name'])}</p>
<p><a href="{esc(source['url'])}">{esc(source['channel'] or source['kind'].title())}</a></p>
<p class="small">{'Image rights remain with the original rights holders. These file formats do not grant a reuse licence.' if en else 'Les droits de l’image restent ceux des ayants droit d’origine. Ces formats ne constituent pas une licence de réutilisation.'}</p></section></div>
<h2>{'Artwork variations' if en else 'Variantes visuelles'}</h2><div class="photo-grid">{treatments}</div>
<h2>{'Image formats' if en else 'Formats de l’image'}</h2><div class="photo-formats">{formats}</div>
<div aria-hidden="true" style="position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden">{esc(' · '.join(keywords(d)))}</div>
<details><summary>{'Photo topics' if en else 'Thèmes de la photo'}</summary><p>{esc(' · '.join(keywords(d)))}</p></details>
<h2>{'More artist photos' if en else 'Autres photos d’artistes'}</h2><ul class="photo-related">{links}</ul>'''
    url = BASE + photo_path(slug,lang)
    graph = [{'@type':'WebPage','@id':url+'#page','url':url,'name':title,'description':desc,'inLanguage':lang,
              'datePublished':state[slug], 'mainEntity':objects,
              'primaryImageOfPage':{'@id':objects[0]['@id']},'about':{'@id':BASE+profile+'#artist'}},
             {'@type':'BreadcrumbList','itemListElement':[
                 {'@type':'ListItem','position':1,'name':'Photos','item':BASE+photo_path('',lang)},
                 {'@type':'ListItem','position':2,'name':d['name'],'item':url}]}]
    return shell(slug,lang,title,desc,body,graph,BASE+variant_path(slug,d,1280,'jpg','banner'))


def hub_page(rows, lang):
    en = lang == 'en'
    title = 'Bouyon artist photos: the visual directory' if en else 'Photos des artistes bouyon : le répertoire en images'
    desc = 'Explore bouyon artist photos, video artwork and music profiles.' if en else 'Découvrez les photos des artistes bouyon, les visuels des clips et les fiches musicales.'
    cards = []
    items = []
    for slug,d in sorted(rows.items(), key=lambda pair: pair[1]['name'].casefold()):
        island = d['island'][lang] if d.get('island') else 'Bouyon'
        cards.append(f'<article class="photo-card"><a href="{photo_path(slug,lang)}">{picture(slug,d,lang)}<h2>{esc(d["name"])}</h2></a><p>{esc(island)} · {esc(d["source"]["kind"].title())}</p></article>')
        items.append({'@type':'ListItem','position':len(items)+1,'url':BASE+photo_path(slug,lang),'name':d['name']})
    body = f'<p class="kicker">BOUYON EN IMAGES · {len(rows)} {"ARTISTS" if en else "ARTISTES"}</p><h1>{title}</h1><p class="lead">{desc}</p><div class="photo-grid">'+''.join(cards)+'</div>'
    graph = [{'@type':'CollectionPage','@id':BASE+photo_path('',lang)+'#page','url':BASE+photo_path('',lang),'name':title,'inLanguage':lang,
              'mainEntity':{'@type':'ItemList','numberOfItems':len(items),'itemListElement':items}}]
    hero = BASE+variant_path(next(iter(rows)),next(iter(rows.values())),1280,'jpg') if rows else None
    return shell('',lang,title,desc,body,graph,hero)


CSS = '''.photo-main{padding-top:36px}.photo-main>h1{max-width:850px}.photo-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;margin-top:38px}.photo-card{border:1px solid var(--line);background:var(--panel);border-radius:12px;overflow:hidden}.photo-card>a{text-decoration:none;color:var(--text)}.photo-card img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}.photo-card h2{font-size:22px;margin:15px 18px 4px}.photo-card p{font-size:14px;margin:0 18px 18px;color:var(--muted)}.photo-hero{margin:28px 0}.photo-hero img{display:block;width:100%;height:auto;border-radius:12px}.photo-hero figcaption{font-size:14px;color:var(--muted);margin-top:10px}.photo-info{display:grid;grid-template-columns:1fr 1fr;gap:40px}.photo-formats{display:flex;flex-wrap:wrap;gap:14px}.photo-formats a{padding:12px 18px;border:1px solid var(--line);border-radius:8px}.photo-related{display:flex;gap:24px;flex-wrap:wrap;list-style:none}.photo-card a:hover h2{color:var(--turq)}@media(max-width:850px){.photo-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:540px){.photo-grid,.photo-info{grid-template-columns:1fr}.photo-main{padding-top:20px}}
'''


def apply_discovery():
    import image_variants
    rows, state = released()
    outputs = {}
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    new_cache = {}
    renderer_hash = hashlib.sha256(Path(image_variants.__file__).read_bytes()).hexdigest()
    def emit(path, data):
        rel = path.lstrip('/')
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        payload = data.encode('utf-8') if isinstance(data,str) else data
        if not p.exists() or p.read_bytes() != payload:
            p.write_bytes(payload)
        outputs[rel] = True
    ordered = sorted(rows.items(), key=lambda pair: pair[1]['name'].casefold())
    for i,(slug,d) in enumerate(ordered):
        source = (ROOT / f'img/artistes/{d["file"]}-1280.jpg').read_bytes()
        signature = hashlib.sha256(source+dump(d).encode()+dump(keywords(d)).encode()+renderer_hash.encode()).hexdigest()
        paths = [variant_path(slug,d,w,fmt,t) for t,w,fmt in variants()]
        if cache.get(slug)==signature and all((ROOT/p.lstrip('/')).is_file() for p in paths):
            outputs.update({p.lstrip('/'):True for p in paths})
        else:
            credit = d['source']['channel'] or d['name']
            metadata = {'title':d['name']+' bouyon music photo','description':d['alt_en']+'; '+'; '.join(keywords(d)),
                        'keywords':keywords(d),'creator':credit,'credit':credit,'source':d['source']['url'],
                        'rights':'Source image rights remain with the original rights holders.', 'page':BASE+photo_path(slug,'en')}
            rendered = image_variants.treatments(source,d['name'],(d.get('island') or {}).get('en',''))
            # Re-encode the named original variants once to carry expanded EXIF/XMP.
            from PIL import Image
            import io
            rendered['original']=Image.open(io.BytesIO(source)).convert('RGB')
            for treatment,width,fmt in variants():
                raw=image_variants.encode(rendered[treatment],width,fmt,metadata)
                emit(variant_path(slug,d,width,fmt,treatment),jpeg_metadata(raw,d) if fmt=='jpg' else raw)
        new_cache[slug]=signature
        neighbors = (ordered[i+1:]+ordered[:i])[:4]
        for lang in ('fr','en'):
            emit(photo_path(slug,lang),artist_page(slug,d,lang,state,neighbors))
    for lang in ('fr','en'):
        emit(photo_path('',lang)+'index.html',hub_page(rows,lang))
    emit('/photos/gallery.css',CSS)
    entries = []
    for lang in ('fr','en'):
        entries.append(f'  <url><loc>{BASE}{photo_path("",lang)}</loc></url>')
        for slug,d in ordered:
            imgs = ''.join(f'<image:image><image:loc>{BASE}{variant_path(slug,d,w,fmt,t)}</image:loc></image:image>' for t,w,fmt in variants())
            entries.append(f'  <url><loc>{BASE}{photo_path(slug,lang)}</loc><lastmod>{state[slug]}</lastmod>{imgs}</url>')
    emit('/sitemap-images.xml','<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'+'\n'.join(entries)+'\n</urlset>\n')
    index = ROOT / 'sitemap.xml'
    xml = index.read_text()
    if BASE+'/sitemap-images.xml' not in xml:
        xml = xml.replace('</sitemapindex>',f'  <sitemap><loc>{BASE}/sitemap-images.xml</loc></sitemap>\n</sitemapindex>')
        index.write_text(xml)
    # Links are marker-owned and reapplied after both language generators.
    for lang in ('fr','en'):
        prefix = 'en/' if lang=='en' else ''
        for rel in [prefix+'index.html',prefix+('artists.html' if lang=='en' else 'artistes.html')]+[prefix+s+'.html' for s in images._load(images.DATA,{})]:
            p = ROOT / rel
            if not p.exists():
                continue
            text = p.read_text()
            clean = re.sub(r'\s*<!-- photos:link:start -->.*?<!-- photos:link:end -->','',text,flags=re.S)
            slug = p.stem if p.stem in rows else ''
            is_profile = p.stem in images._load(images.DATA,{})
            if not is_profile or slug:
                label = (rows[slug]['name']+' : photos') if slug else ('Artist photo gallery' if lang=='en' else 'Galerie photos des artistes')
                block = f'\n<!-- photos:link:start --><p class="photo-link"><a href="{photo_path(slug,lang)}">{esc(label)}</a></p><!-- photos:link:end -->'
                clean = re.sub(r'\s*</main>',lambda match:block+'\n</main>',clean,count=1)
            if clean != text:
                p.write_text(clean)
    old = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else []
    for rel in set(old)-set(outputs):
        # Only this module's tracked outputs can be deleted.
        if rel.startswith(('photos/','en/photos/','img/photos/')) and '..' not in Path(rel).parts:
            p=ROOT/rel
            if p.is_file():
                p.unlink()
    MANIFEST.write_text(json.dumps(sorted(outputs),indent=1)+'\n')
    CACHE.write_text(json.dumps(new_cache,sort_keys=True,indent=1)+'\n')
    print(f'image discovery: {len(rows)} artists, {len(rows)*2+2} pages, {len(rows)*len(variants())} image files')


if __name__ == '__main__':
    apply_discovery()
