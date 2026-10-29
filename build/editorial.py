"""Mixtape and chronique pages (BOU-3200), French only, called from generate.py.

Mixtapes: /mixtapes/<slug>.html plus the /mixtapes/ index, from data_mixtapes.py.
Chroniques: /chroniques/<slug>.html plus the /chroniques/ index, from data_chroniques.py
(no page and no index while the list is empty).
Each page has a byline with dates, the official embed, a facts box, sources,
the artists it mentions (linked to their profiles) and related pages.
"""
import json

BASE = "https://bouyonmusique.com/"
SMOKILLER = {"@id": BASE + "#smokiller"}
KINDS = {
    "mixtape": {"cat": "Mixtapes", "dir": "mixtapes/", "index_nav": "Mixtapes bouyon"},
    "chronique": {"cat": "Chroniques", "dir": "chroniques/", "index_nav": "Chroniques bouyon"},
}


def clock(s):
    return f"{s // 60}:{s % 60:02d}" if s < 3600 else f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def duration_fr(s):
    return f"{s // 60} min {s % 60:02d} s"


def duration_iso(s):
    return f"PT{s // 60}M{s % 60}S"


def items(mixtapes, chroniques):
    """Pseudo pages for hubs, footers and the sitemap."""
    out = []
    for kind, rows in (("mixtape", mixtapes), ("chronique", chroniques)):
        for r in rows:
            arts = []
            for slugs in [t[2] for t in r.get("tracks", [])] + [r.get("artists", [])]:
                arts += [a for a in slugs if a not in arts]
            out.append(dict(r, kind=kind, cat=KINDS[kind]["cat"], artists=arts))
    return out


def youtube_embed(video_id, title, esc):
    return ('<div class="embed">'
            f'<iframe src="https://www.youtube-nocookie.com/embed/{video_id}" title="{esc(title)}" loading="lazy" '
            ''
            'allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>\n')


def shell(ctx, url, title, desc, image, graph, crumbs, body, footer_html):
    esc = ctx["esc"]
    crumb_html = " / ".join(f'<a href="{u}">{esc(n)}</a>' if u else esc(n) for n, u in crumbs)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="fr" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Bouyon Musique">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="fr_FR">
<meta property="og:image" content="{image[0]}">
<meta property="og:image:width" content="{image[1]}">
<meta property="og:image:height" content="{image[2]}">
<meta property="og:image:alt" content="{esc(image[3])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)}
</script>
</head>
<body>
{ctx["header"]}
<main>
<div class="wrap">
<p class="breadcrumb">{crumb_html}</p>
{body}
</div>
</main>
{footer_html}
</body>
</html>
"""


def breadcrumb_ld(crumbs, url):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": (BASE + u.lstrip("/")) if u else url}
        for i, (n, u) in enumerate(crumbs)]}


def related_html(slugs, ctx):
    esc, pages = ctx["esc"], ctx["pages"]
    cards = ""
    for s in slugs:
        p = pages[s]
        cards += f'  <div class="card"><h3>{esc(p["nav"])}</h3><p>{esc(p["desc"][:150])}...</p><p><a href="/{p["slug"]}">Lire la page</a></p></div>\n'
    return f'\n<h2>À lire aussi</h2>\n<div class="grid">\n{cards}</div>\n' if cards else ""


def render(item, siblings, ctx):
    esc, kind = ctx["esc"], item["kind"]
    k = KINDS[kind]
    url = BASE + item["slug"]
    crumbs = [("Musique bouyon", "/"), (k["cat"], "/" + k["dir"]), (item["nav"], None)]
    artists = [ctx["artists"][a] for a in item["artists"]]
    mentions = [{"@id": a["id"]} for a in artists]
    page_ld = {
        "@type": "WebPage", "@id": url + "#page", "url": url, "name": item["title"], "description": item["desc"],
        "inLanguage": "fr", "datePublished": item["date_published"],
        "dateModified": item.get("date_modified") or item["date_published"],
        "isPartOf": {"@id": BASE + "#site"}, "publisher": {"@id": BASE + "#org"}, "author": SMOKILLER,
        "mainEntity": {"@id": url + "#" + kind},
    }
    if mentions:
        page_ld["mentions"] = mentions
    graph = [page_ld, breadcrumb_ld(crumbs, url)]
    vid = item.get("video_id")
    image = (BASE + "og-image.png", 1200, 630, "Bouyon Musique, le guide de la musique bouyon")
    if vid and kind == "mixtape":
        thumb = f"{BASE}mixtapes/img/{vid}.jpg"
        image = (thumb, 960, 540, f"Visuel de {item['nav']}, publié par Smokiller")
        page_ld["primaryImageOfPage"] = {"@type": "ImageObject", "url": thumb, "width": 960, "height": 540}
    if vid:
        graph.append({
            "@type": "VideoObject", "@id": url + "#video", "name": item.get("youtube_title") or item["nav"],
            "description": ctx["plain"](item["intro"]),
            "thumbnailUrl": [image[0], f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"] if kind == "mixtape" else [f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"],
            "embedUrl": f"https://www.youtube.com/embed/{vid}", "url": f"https://www.youtube.com/watch?v={vid}",
            **({"uploadDate": item["upload_date"], "duration": duration_iso(item["duration"])} if kind == "mixtape" else {}),
        })

    facts, tracklist = [], ""
    if kind == "mixtape":
        graph.append({
            "@type": "MusicPlaylist", "@id": url + "#mixtape", "name": item["nav"], "creator": SMOKILLER,
            "datePublished": item["upload_date"][:10], "numTracks": len(item["tracks"]), "video": {"@id": url + "#video"},
            "track": [dict({"@type": "MusicRecording", "position": i + 1, "name": t[1]},
                           **({"byArtist": [{"@id": ctx["artists"][a]["id"]} for a in t[2]]} if t[2] else {}))
                      for i, t in enumerate(item["tracks"])],
        })
        pl = " et ".join(f'<a href="https://www.youtube.com/playlist?list={pid}">{esc(n.split(" - ")[0])}</a>' for n, pid in item["playlists"])
        facts = [
            'Mixée par : <a href="/smokiller.html">Smokiller</a>',
            f'Mise en ligne : {ctx["fmt_date"](item["upload_date"][:10])}, sur la <a href="{ctx["channel"]}">chaîne YouTube de Smokiller</a>',
            f'Durée : {duration_fr(item["duration"])}',
            f'Chapitres : {len(item["tracks"])} titres',
            f'Playlists : {pl}',
        ]
        rows = ""
        for start, name, profiles, ext in item["tracks"]:
            extra = [f'<a href="/{a}">{esc(ctx["artists"][a]["nav"])}</a>' for a in profiles]
            if ext:
                extra.append(f'<a href="{ext}">fiche sur smokiller.com</a>')
            tail = f' <span class="muted">({" · ".join(extra)})</span>' if extra else ""
            rows += f'<li><a href="https://www.youtube.com/watch?v={vid}&amp;t={start}s">{clock(start)}</a> {esc(name)}{tail}</li>\n'
        tracklist = f'\n<h2>Tracklist</h2>\n<p>Les {len(item["tracks"])} chapitres de la vidéo, avec leur minutage. Un clic sur le minutage ouvre la vidéo à ce moment.</p>\n<ol class="tracklist">\n{rows}</ol>\n'
        sources = [(f'Vidéo YouTube « {item["youtube_title"]} », titre, date, durée et chapitres', f"https://www.youtube.com/watch?v={vid}")]
        sources += [(f"Playlist YouTube « {n} »", f"https://www.youtube.com/playlist?list={pid}") for n, pid in item["playlists"]]
        sources += [(f"Fiche smokiller.com : {u.rsplit('/', 1)[1]}", u) for u in dict.fromkeys(t[3] for t in item["tracks"] if t[3])]
    else:
        reviewed = {"@type": item["item_type"], "name": item["item_name"],
                    "byArtist": [{"@id": a["id"]} for a in artists]}
        if item.get("release_date"):
            reviewed["datePublished"] = item["release_date"]
        graph.append({"@type": "Review", "@id": url + "#chronique", "name": item["title"], "author": SMOKILLER,
                      "publisher": {"@id": BASE + "#org"}, "datePublished": item["date_published"],
                      "inLanguage": "fr", "itemReviewed": reviewed})
        facts = [f'Titre : {esc(item["item_name"])}',
                 "Artiste : " + ", ".join(f'<a href="/{a["slug"]}">{esc(a["nav"])}</a>' for a in artists)]
        if item.get("release_date"):
            facts.append(f'Sortie : {ctx["fmt_date"](item["release_date"])}')
        sources = item["sources"]
    graph += ctx["site_entities"]

    sections = "".join(f'\n<h2>{esc(h2)}</h2>\n' + "".join(f"<p>{p}</p>\n" for p in paras) for h2, paras in item["sections"])
    embed = youtube_embed(vid, item.get("youtube_title") or item["nav"], esc) if vid else ""
    facts_html = '<div class="facts">\n<ul>\n' + "".join(f"<li>{f}</li>\n" for f in facts) + "</ul>\n</div>\n"
    sources_html = '\n<h2>Sources</h2>\n<ul>\n' + "".join(f'<li><a href="{u}">{esc(n)}</a></li>\n' for n, u in sources) + "</ul>\n"
    others = [s for s in siblings if s["slug"] != item["slug"]]
    others_html = ""
    if others:
        others_html = f'\n<h2>Autres {k["cat"].lower()}</h2>\n<p class="strip">' + " · ".join(
            f'<a href="/{s["slug"]}">{esc(s["nav"])}</a>' for s in others) + "</p>\n"
    body = (f'<h1>{esc(item["h1"])}</h1>\n{ctx["byline"](item)}\n<p class="lead">{item["intro"]}</p>\n'
            f'{embed}{facts_html}{sections}{tracklist}{sources_html}{ctx["cited"](item["artists"])}'
            f'{related_html(item.get("related", []), ctx)}{others_html}')
    return shell(ctx, url, item["title"], item["desc"], image, graph, crumbs, body, ctx["footer"](item, others))


def render_index(kind, rows, ctx):
    esc, k = ctx["esc"], KINDS[kind]
    url = BASE + k["dir"]
    crumbs = [("Musique bouyon", "/"), (k["cat"], None)]
    if kind == "mixtape":
        title = "Mixtapes bouyon de Smokiller : tracklists et vidéos"
        desc = "Les mixtapes bouyon publiées par Smokiller sur YouTube, avec la tracklist minutée de chaque mix et les profils des artistes qu’elles font tourner."
        lead = "Smokiller publie des mixtapes bouyon sur sa chaîne YouTube. Chaque page reprend la vidéo, la tracklist minutée telle qu’elle apparaît dans les chapitres, et renvoie vers les profils des artistes cités sur ce site."
    else:
        title = "Chroniques bouyon : titres et albums écoutés"
        desc = "Les chroniques de Bouyon Musique : un titre ou un album bouyon écouté, avec ses crédits sourcés."
        lead = "Chaque chronique écoute un titre ou un album bouyon. Les crédits et les dates viennent des sources citées en bas de page."
    cards = ""
    for r in rows:
        meta = f'Publiée le {ctx["fmt_date"](r["date_published"])}'
        if kind == "mixtape":
            meta = f'Mise en ligne le {ctx["fmt_date"](r["upload_date"][:10])} · {duration_fr(r["duration"])} · {len(r["tracks"])} titres'
        cards += f'  <div class="card"><h3><a href="/{r["slug"]}">{esc(r["nav"])}</a></h3><p>{meta}</p><p>{esc(r["desc"])}</p></div>\n'
    graph = [
        {"@type": "CollectionPage", "@id": url + "#page", "url": url, "name": title, "description": desc, "inLanguage": "fr",
         "isPartOf": {"@id": BASE + "#site"}, "publisher": {"@id": BASE + "#org"},
         "dateModified": max(r.get("date_modified") or r["date_published"] for r in rows),
         "mainEntity": {"@type": "ItemList", "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": r["nav"], "url": BASE + r["slug"]} for i, r in enumerate(rows)]}},
        breadcrumb_ld(crumbs, url),
    ] + ctx["site_entities"]
    body = f'<h1>{esc(k["index_nav"])}</h1>\n<p class="lead">{lead}</p>\n<div class="grid">\n{cards}</div>\n'
    if kind == "mixtape":
        arts = []
        for r in rows:
            arts += [a for a in r["artists"] if a not in arts]
        names = sorted(((ctx["artists"].get(a) or {}).get("name") or (ctx["pages"].get(a) or {}).get("nav", a), a) for a in arts)
        total = sum(len(r["tracks"]) for r in rows)
        body += (
            '<h2>Ce que contient une page mixtape</h2>\n'
            f'<p>Le site compte {len(rows)} mixtapes et {total} chapitres. Chaque page reprend la vidéo YouTube de Smokiller, la date de mise en ligne et la durée telles '
            'que la chaîne les publie, puis la tracklist chapitre par chapitre avec le minutage exact. Les intitulés des chapitres sont recopiés tels quels : '
            'le site n’ajoute ni année, ni pays, ni crédit que la vidéo et les sources citées ne donnent pas. Quand un chapitre nomme un artiste qui a sa fiche '
            'sur Bouyon Musique, le titre renvoie vers cette fiche.</p>\n'
            '<h2>Où écouter les mixtapes</h2>\n'
            f'<p>Les mixtapes sont publiées sur la <a href="{ctx["channel"]}">chaîne YouTube de Smokiller</a> et rangées dans ses playlists, dont '
            '<a href="https://www.youtube.com/playlist?list=PLB1axoRydQre_2MEDDGaRUNYTbZkAOt7j">Bouyon Mix 2026</a> pour les mixes et '
            '<a href="https://www.youtube.com/playlist?list=PLB1axoRydQreXaKD2wlZ5IHJmNmoTWEEd">Bouyon Music 2026</a> pour les titres. '
            'Pour comprendre comment un mix bouyon est construit, lire <a href="/bouyon-mix.html">le guide du mix bouyon</a> ; pour les titres un par un, '
            '<a href="/playlist-bouyon.html">la playlist bouyon</a> et <a href="/nouveautes-bouyon-2026.html">les nouveautés bouyon 2026</a>. '
            'Le profil du producteur : <a href="/smokiller.html">Smokiller</a>.</p>\n'
            '<h2>Les artistes que les mixtapes font tourner</h2>\n'
            '<p>' + " · ".join(f'<a href="/{a if a.endswith(".html") else a + ".html"}">{esc(n)}</a>' for n, a in names) + '</p>\n'
        )
    page = {"slug": k["dir"], "cat": k["cat"], "nav": k["index_nav"]}
    return shell(ctx, url, title, desc, (BASE + "og-image.png", 1200, 630, "Bouyon Musique, le guide de la musique bouyon"),
                 graph, crumbs, body, ctx["footer"](page, rows))
