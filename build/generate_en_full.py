#!/usr/bin/env python3
"""Build the full English mirror of bouyonmusique.com under /en/ from the *_en data modules.
Core EN pages (index, history, artists, playlist-bouyon, bouyon-dance, faq) are hand-built HTML, not handled here.
This script builds: 64 topic pages + en/site-map.html.
"""
import datetime, hashlib, html, importlib, json, os, re, sys

BUILD_DATE = datetime.date.today().isoformat()

MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def fmt_date_en(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{MONTHS_EN[d.month - 1]} {d.day}, {d.year}"

def spread_date(key):
    """Deterministic pseudo publication date in 2026-09-01..2026-10-16, by FR slug hash (matches generate.py)."""
    h = int(hashlib.md5(key.encode("utf-8")).hexdigest()[:8], 16)
    return (datetime.date(2026, 9, 1) + datetime.timedelta(days=h % 46)).isoformat()

SITE_ENTITIES = [
    {"@type": "WebSite", "@id": "https://bouyonmusique.com/#site", "url": "https://bouyonmusique.com/", "name": "Bouyon Musique", "inLanguage": ["fr", "en"], "publisher": {"@id": "https://bouyonmusique.com/#org"}},
    {"@type": "Organization", "@id": "https://bouyonmusique.com/#org", "name": "Bouyon Shattaz", "url": "https://bouyonshattaz.com/", "sameAs": ["https://www.instagram.com/bouyonshattaz/", "https://www.youtube.com/@smo.killer"]},
    {"@type": "Person", "@id": "https://bouyonmusique.com/#smokiller", "name": "Smokiller", "jobTitle": "Bouyon artist and producer", "birthPlace": "Dominica", "url": "https://smokiller.com/", "sameAs": ["https://www.youtube.com/@smo.killer", "https://www.instagram.com/smo.killer/", "https://www.tiktok.com/@smo.killer", "https://smokiller.com/"]},
]

CAT_FAQ = {
    "Bouyon styles": [("What is bouyon music?", "Bouyon is a genre born in Dominica in the late 1980s. Its name comes from the Kweyol word for soup: it blends jing ping, cadence-lypso, calypso and electronic production, pioneered by the band WCK."), ("Where can I hear the bouyon styles?", "The playlist page collects the Bouyon Road Mix by Bouyon Shattaz on Spotify and YouTube, with new bouyon and carnival classics.")],
    "Bouyon guides": [("Where do I start with bouyon?", "Start with the history of the genre, then the Bouyon Road Mix playlist by Bouyon Shattaz, which mixes Dominica carnival classics with new bouyon."), ("Which country created bouyon?", "Dominica, in the late 1980s, with WCK as the pioneering band.")],
    "Bouyon by country": [("Where is bouyon popular?", "Born in Dominica, bouyon is now central in Guadeloupe and Martinique and present in France, Saint Lucia, Saint Martin and the Caribbean diaspora."), ("Which country created bouyon?", "Dominica. The genre was born there in the late 1980s and remains the sound of Roseau carnival.")],
    "Bouyon events": [("What is the big bouyon festival?", "The World Creole Music Festival is held every year in Roseau, Dominica. The 2026 edition runs October 23 to 25 at Windsor Park."), ("When is Dominica carnival?", "Dominica carnival, Mas Domnik, takes place before Lent, with J'ouvert as a peak moment for bouyon and soca.")],
    "Bouyon artists": [("Who are the key bouyon artists?", "WCK created the genre, Asa Bantan is widely called the King of Bouyon, and the new generation includes Reo, Ridge, Signal Band and Shelly, while producers like Smokiller export the sound."), ("Who publishes these artist pages?", "BouyonMusique.com is published by Bouyon Shattaz, the platform of Dominican-born producer Smokiller, with facts verified artist by artist.")],
    "Bouyon production": [("Who produces bouyon today?", "Producers like Smokiller (Bouyon Shattaz), Denmath, HYPNO! and Savion work the bouyon sound across riddims, remixes and original productions."), ("What is a bouyon riddim?", "A riddim is the instrumental several artists record over. Riddims sit at the heart of bouyon and dancehall production.")],
    "Listen to bouyon": [("Where can I listen to bouyon online?", "On the Bouyon Road Mix by Bouyon Shattaz, on Spotify and YouTube via this site's playlist page."), ("How do I get the bouyon playlist?", "Follow @bouyonshattaz on Instagram and comment ROAD MIX on a post: the playlist is sent to your DMs.")],
    "Bouyon culture": [("Why is it called bouyon?", "Bouyon means soup in Kweyol: the genre stirs Dominica's traditional musics together with electronic production."), ("Is bouyon part of Creole culture?", "Yes. Bouyon was born in Dominica's villages and carnival and soundtracks Creole celebrations across the French Caribbean.")],
}


SITE = os.path.expanduser("~/workspace/bouyonmusique.com/en")
BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)

PAGES = []
for mod in ["data_styles_en", "data_guides_en", "data_places_en", "data_events_artists_en", "data_production_ecoute_en", "data_culture_en", "data_wave1_en", "data_wave1b_en", "data_branches_en"]:
    m = importlib.import_module(mod)
    PAGES.extend(m.PAGES)

for _p in PAGES:
    _p.setdefault("date_published", spread_date(_p["fr_slug"]))

CORE_EN = [
    ("/en/", "Bouyon Music (home)"),
    ("/en/history.html", "History of bouyon"),
    ("/en/artists.html", "Bouyon artists"),
    ("/en/playlist-bouyon.html", "Bouyon playlist"),
    ("/en/bouyon-dance.html", "Bouyon dance"),
    ("/en/faq.html", "Bouyon FAQ"),
]

def esc(s):
    return html.escape(s, quote=True)

HEADER = """<header>
  <div class="wrap nav">
    <a class="logo" href="/en/">BOUYON<span>MUSIQUE</span>.COM</a>
    <nav class="main" aria-label="Main navigation">
      <a href="/en/">Home</a>
      <a href="/en/what-is-bouyon.html">What is Bouyon</a>
      <a href="/en/history.html">History</a>
      <a href="/en/artists.html">Artists</a>
      <a href="/en/playlist-bouyon.html">Playlist</a>
      <a href="/en/bouyon-dance.html">Dance</a>
      <a href="/en/site-map.html">All topics</a>
      <a href="/en/faq.html">FAQ</a>
      <a href="/">FR</a>
    </nav>
  </div>
</header>"""

def footer(page, same_cat):
    links = "\n".join(f'        <li><a href="/en/{p["slug"]}">{esc(p["nav"])}</a></li>' for p in spread_pick(same_cat, page["slug"] + "|footer", 8))
    return f"""<footer>
  <div class="wrap cols">
    <div>
      <h4>BouyonMusique.com</h4>
      <p>The guide to bouyon music in French and English: history, artists, dance, riddims and playlists. Published by Bouyon Shattaz.</p>
    </div>
    <div>
      <h4>{esc(page["cat"])}</h4>
      <ul>
{links}
      </ul>
    </div>
    <div>
      <h4>Bouyon Shattaz</h4>
      <ul>
        <li><a href="https://bouyonshattaz.com/">bouyonshattaz.com</a></li>
        <li><a href="https://www.instagram.com/bouyonshattaz/">Instagram @bouyonshattaz</a></li>
        <li><a href="/en/site-map.html">Site map: every bouyon topic</a></li>
        <li><a href="/">Version française</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap"><p style="margin-top:24px">© 2026 Bouyon Shattaz. Bouyon was born in Dominica.</p></div>
</footer>"""

def spread_pick(items, seed, n):
    return sorted(items, key=lambda q: hashlib.md5((seed + "|" + q["slug"]).encode("utf-8")).hexdigest())[:n]

GENERIC_TERMS = {"Bouyon", "Dominica", "Dominique", "Soca", "Accueil", "FAQ", "Home"}

def page_terms(all_pages, page, extra):
    slugs = {q["slug"] for q in all_pages}
    terms = {}
    for q in all_pages:
        if q["slug"] == page["slug"]:
            continue
        cand = [q["nav"]]
        h1name = q["h1"].split(":")[0].strip()
        if 3 <= len(h1name) <= 40:
            cand.append(h1name)
        for t in cand:
            if t and t not in GENERIC_TERMS and len(t) >= 3:
                terms.setdefault(t, q["slug"])
    for t, s in extra.items():
        if s in slugs and s != page["slug"]:
            terms.setdefault(t, s)
    return sorted(terms.items(), key=lambda kv: -len(kv[0]))

def linkify_sections(page, all_pages, extra, prefix, cap=8):
    terms = page_terms(all_pages, page, extra)
    used = set()
    for _h2, paras in page["sections"]:
        for para in paras:
            for m in re.findall(r'href="([^"]+)"', para):
                used.add(m)
    out = []
    count = 0
    for h2, paras in page["sections"]:
        new_paras = []
        for para in paras:
            if count >= cap:
                new_paras.append(para)
                continue
            parts = re.split(r'(<a [^>]*>.*?</a>)', para)
            for i, part in enumerate(parts):
                if part.startswith("<a "):
                    continue
                for term, slug in terms:
                    if count >= cap:
                        break
                    target = prefix + slug
                    if target in used:
                        continue
                    pat = re.compile(r'(?<![\w\-])' + re.escape(term) + r'(?![\w\-])')
                    if pat.search(part):
                        part = pat.sub('<a href="' + target + '">' + term + '</a>', part, count=1)
                        used.add(target)
                        count += 1
                parts[i] = part
            new_paras.append("".join(parts))
        out.append((h2, new_paras))
    return out

EXTRA_TERMS_EN = {
    "cadence-lypso": "cadence-lypso-roots.html",
    "World Creole Music Festival": "wcmf-creole-festival.html",
    "Mas Domnik": "mas-domnik.html",
}

def render(page):
    same_cat = [p for p in PAGES if p["cat"] == page["cat"] and p["slug"] != page["slug"]]
    rel = spread_pick(same_cat, page["slug"], 6)
    url = f'https://bouyonmusique.com/en/{page["slug"]}'
    fr_url = f'https://bouyonmusique.com/{page["fr_slug"]}'
    sections = ""
    for h2, paras in linkify_sections(page, PAGES, EXTRA_TERMS_EN, "/en/"):
        sections += f'\n<h2>{esc(h2)}</h2>\n'
        for para in paras:
            sections += f"<p>{para}</p>\n"
    faq_list = page.get("faq") or CAT_FAQ.get(page["cat"], [])
    graph = [{
        "@context": "https://schema.org", "@type": "WebPage", "@id": url + "#page", "url": url,
        "name": page["title"], "description": page["desc"], "inLanguage": "en",
        "dateModified": BUILD_DATE,
        "isPartOf": {"@id": "https://bouyonmusique.com/#site"},
        "publisher": {"@id": "https://bouyonmusique.com/#org"},
        "author": {"@id": "https://bouyonmusique.com/#smokiller"},
    }, {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bouyonmusique.com/en/"},
            {"@type": "ListItem", "position": 2, "name": page["cat"], "item": "https://bouyonmusique.com/en/site-map.html"},
            {"@type": "ListItem", "position": 3, "name": page["nav"], "item": url},
        ],
    }] + SITE_ENTITIES
    if graph and graph[0].get("@type") == "WebPage" and page.get("date_published"):
        graph[0]["datePublished"] = page["date_published"]
    faq_html = ""
    if faq_list:
        faq_html = '\n<h2>Frequently asked questions</h2>\n'
        for q, a in faq_list:
            faq_html += f"<details><summary>{esc(q)}</summary><p>{a}</p></details>\n"
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_list]})
    for _e in page.get("extra_graph", []):
        _e = dict(_e)
        if _e.get("@type") in ("ProfilePage", "Article") and page.get("date_published"):
            _e.setdefault("datePublished", page["date_published"])
        graph.append(_e)
    date_html = ""
    if page.get("date_published"):
        date_html = f'\n<p class="pubdate">Published {fmt_date_en(page["date_published"])}</p>'
    rel_html = ""
    if rel:
        rel_html = '\n<h2>Read next</h2>\n<div class="grid">\n'
        for p in rel:
            rel_html += f'  <div class="card"><h3>{esc(p["nav"])}</h3><p>{esc(p["desc"][:150])}...</p><p><a href="/en/{p["slug"]}">Read the page</a></p></div>\n'
        rel_html += "</div>\n"
    cta = """
<div class="facts">
<h3 style="margin-top:0">Listen to bouyon now</h3>
<p>The Bouyon Road Mix by Bouyon Shattaz collects new bouyon releases and carnival classics on Spotify and YouTube.</p>
<p><a href="/en/playlist-bouyon.html">Open the bouyon playlist</a> - Follow <a href="https://www.instagram.com/bouyonshattaz/">@bouyonshattaz</a> and comment ROAD MIX to get it by DM.</p>
</div>
"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(page["title"])}</title>
<meta name="description" content="{esc(page["desc"])}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{url}">
<link rel="alternate" hreflang="fr" href="{fr_url}">
<link rel="alternate" hreflang="x-default" href="{fr_url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Bouyon Musique">
<meta property="og:title" content="{esc(page["title"])}">
<meta property="og:description" content="{esc(page["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_US">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)}
</script>
</head>
<body>
{HEADER}
<main>
<div class="wrap">
<p class="breadcrumb"><a href="/en/">Home</a> / {esc(page["cat"])} / {esc(page["nav"])}</p>
<h1>{esc(page["h1"])}</h1>{date_html}
<p class="lead">{page["intro"]}</p>
{sections}
{cta}
{faq_html}
{rel_html}
</div>
</main>
{footer(page, same_cat)}
</body>
</html>
"""

def main():
    for page in PAGES:
        with open(os.path.join(SITE, page["slug"]), "w", encoding="utf-8") as f:
            f.write(render(page))
    cats = {}
    for p in PAGES:
        cats.setdefault(p["cat"], []).append(p)
    body = ""
    for cat, ps in cats.items():
        body += f'\n<h2>{esc(cat)}</h2>\n<ul>\n'
        for p in ps:
            body += f'<li><a href="/en/{p["slug"]}">{esc(p["nav"])}</a> : {esc(p["desc"])}</li>\n'
        body += "</ul>\n"
    core_links = "\n".join(f'<li><a href="{u}">{esc(n)}</a></li>' for u, n in CORE_EN)
    plan = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Site Map - Bouyon Music: every bouyon topic in English</title>
<meta name="description" content="Every English page on BouyonMusique.com: bouyon history, styles, artists, producers, playlists, Dominica Carnival and bouyon scenes by country.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://bouyonmusique.com/en/site-map.html">
<link rel="alternate" hreflang="en" href="https://bouyonmusique.com/en/site-map.html">
<link rel="alternate" hreflang="fr" href="https://bouyonmusique.com/plan-du-site.html">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
</head>
<body>
{HEADER}
<main><div class="wrap">
<p class="breadcrumb"><a href="/en/">Home</a> / Site map</p>
<h1>Every bouyon topic on this site</h1>
<p class="lead">BouyonMusique.com covers bouyon music from every angle: its styles, its places, its artists, its producers and its events.</p>
<h2>Main pages</h2>
<ul>
{core_links}
</ul>
{body}
</div></main>
<footer><div class="wrap"><p>© 2026 Bouyon Shattaz. Bouyon was born in Dominica. <a href="/en/">Back to the English home</a> - <a href="/plan-du-site.html">Plan du site en français</a></p></div></footer>
</body>
</html>
"""
    with open(os.path.join(SITE, "site-map.html"), "w", encoding="utf-8") as f:
        f.write(plan)
    print(f"Wrote {len(PAGES)} EN topic pages + site-map")

if __name__ == "__main__":
    main()
