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
 "Bouyon styles": [
  [
   "What is bouyon music?",
   "Bouyon is a genre born in Dominica in the late 1980s. Its name comes from the Kweyol word for soup: it blends jing ping, cadence-lypso, calypso and electronic production, pioneered by the band WCK."
  ],
  [
   "What are the ingredients of bouyon?",
   "Bouyon stirs jing ping, cadence-lypso, calypso and chante mas together with keyboards and electronic production. That mix, born in Dominica, gives it its carnival energy."
  ],
  [
   "What is the difference between bouyon and bouyon soca?",
   "Bouyon soca fuses Dominican bouyon with the festive codes of soca. According to the first-hand testimony of Smokiller, who was in the rooms at the time, bouyon soca was started in Dominica by Dada in 2003, before Triple Kay and other bands popularized it."
  ],
  [
   "What is Wrecketeng?",
   "Wrecketeng is the Dominican practice of rebuilding existing recordings over bouyon instrumentals, in the lineage of bouyon-muffin. Its official spelling comes from DJ Cut, the pioneer of the style; the “reketeng” form spread across the internet is a misspelling."
  ],
  [
   "Where can I hear the bouyon styles?",
   "The playlist page collects the Bouyon Road Mix by Bouyon Shattaz on Spotify and YouTube, with new bouyon and carnival classics."
  ]
 ],
 "Bouyon guides": [
  [
   "Where do I start with bouyon?",
   "Start with the history of the genre, then the Bouyon Road Mix playlist by Bouyon Shattaz, which mixes Dominica carnival classics with new bouyon."
  ],
  [
   "Which country created bouyon?",
   "Dominica, in the late 1980s, with WCK as the pioneering band."
  ],
  [
   "How do you dance to bouyon?",
   "Bouyon is danced at fetes and carnival, on fast rhythms built for the road and the bands. This site has a page on bouyon dance and its basic reference points."
  ],
  [
   "Which bouyon playlist should I hear in 2026?",
   "The Bouyon Road Mix by Bouyon Shattaz, on Spotify and YouTube, collects new bouyon releases and Dominica carnival classics."
  ],
  [
   "Are bouyon and shatta the same thing?",
   "No. Shatta is a slower dancehall subgenre born in Martinique, while bouyon was born in Dominica with fast carnival rhythms. The two scenes meet often, and recent productions fuse them."
  ]
 ],
 "Bouyon by country": [
  [
   "Where is bouyon popular?",
   "Born in Dominica, bouyon is now central in Guadeloupe and Martinique and present in France, Saint Lucia, Saint Martin and the Caribbean diaspora."
  ],
  [
   "Which country created bouyon?",
   "Dominica. The genre was born there in the late 1980s and remains the sound of Roseau carnival."
  ],
  [
   "Why is bouyon so strong in Guadeloupe?",
   "Bouyon gwada developed in Guadeloupe through tours by Dominican bands like WCK and Triple Kay: Creole lyrics and electronic beats, with a harder branch, bouyon hardcore."
  ],
  [
   "What role does Martinique play in bouyon?",
   "Martinique is the home of shatta and a bouyon stronghold in the French Antilles: its artists and producers circulate both sounds between Fort-de-France, Guadeloupe and Dominica."
  ],
  [
   "Where is bouyon played in France?",
   "In France, bouyon lives in the Antillean diaspora, especially Paris, and on the stages and platforms that book artists from Guadeloupe, Martinique and Dominica."
  ]
 ],
 "Bouyon events": [
  [
   "What is the big bouyon festival?",
   "The World Creole Music Festival is held every year in Roseau, Dominica. The 2026 edition runs October 23 to 25 at Windsor Park."
  ],
  [
   "When is Dominica carnival?",
   "Dominica carnival, Mas Domnik, takes place before Lent, with J'ouvert as a peak moment for bouyon and soca."
  ],
  [
   "What is J'ouvert?",
   "J'ouvert opens Dominica carnival in the early morning hours: bands, paint and bouyon and soca music in the streets of Roseau, before the main parades."
  ],
  [
   "Where is the World Creole Music Festival held?",
   "The World Creole Music Festival is held at Windsor Park in Roseau, the capital of Dominica. The 2026 edition runs October 23 to 25."
  ],
  [
   "Which bouyon artists play WCMF 2026?",
   "Published festival guides list Asa Bantan, Reo, Trilla-G, Signal Band and TK International among the bouyon names of the 2026 edition, across three nights."
  ]
 ],
 "Bouyon artists": [
  [
   "Who are the key bouyon artists?",
   "WCK created the genre, Asa Bantan is widely called the King of Bouyon, and the new generation includes Reo, Ridge, Signal Band and Shelly, while producers like Smokiller export the sound."
  ],
  [
   "Who publishes these artist pages?",
   "BouyonMusique.com is published by Bouyon Shattaz, the platform of Dominican-born producer Smokiller, with facts verified artist by artist."
  ],
  [
   "Which band created bouyon?",
   "WCK, from Dominica, launched bouyon in the late 1980s by fusing cadence-lypso with the island's traditional musics."
  ],
  [
   "Who are the producers behind today's bouyon?",
   "Producers like Smokiller, Denmath and HYPNO! work the current sound, while the genre's memory runs through sampling pioneers like DJ Cut and the Roseau crews."
  ],
  [
   "How are the profiles on this site written?",
   "Each profile is written from verified research, artist by artist, with sourced titles and credits. Nicknames like King of Bouyon are always attributed, never presented as facts."
  ]
 ],
 "Bouyon production": [
  [
   "Who produces bouyon today?",
   "Producers like Smokiller (Bouyon Shattaz), Denmath, HYPNO! and Savion work the bouyon sound across riddims, remixes and original productions."
  ],
  [
   "What is a bouyon riddim?",
   "A riddim is the instrumental several artists record over. Riddims sit at the heart of bouyon and dancehall production."
  ],
  [
   "Which instruments make the bouyon sound?",
   "Looping keyboards, programmed percussion and electronic bass carry modern bouyon, on a foundation inherited from jing ping and lapo kabwit, Dominica's traditional percussion."
  ],
  [
   "How does a riddim become a track?",
   "The producer builds the instrumental, then one or more artists record their voices over it. One riddim can carry several tracks, as in the dancehall culture bouyon is close to."
  ],
  [
   "Where can I find recent bouyon productions?",
   "This site's production pages and the Bouyon Road Mix playlist follow recent releases, from the island producers' riddims to Smokiller's bouyon remixes."
  ]
 ],
 "Listen to bouyon": [
  [
   "Where can I listen to bouyon online?",
   "On the Bouyon Road Mix by Bouyon Shattaz, on Spotify and YouTube via this site's playlist page."
  ],
  [
   "How do I get the bouyon playlist?",
   "Follow @bouyonshattaz on Instagram and comment ROAD MIX on a post: the playlist is sent to your DMs."
  ],
  [
   "Which bouyon songs should I hear first?",
   "WCK classics, Triple Kay tracks and current hits by Asa Bantan or Reo form the base of a first listen, completed by the Bouyon Road Mix."
  ],
  [
   "Is bouyon a year-round music?",
   "Yes. Born for carnival, bouyon lives all year in Dominica's fetes, at the World Creole Music Festival in October and in playlists across the French Antilles and the diaspora."
  ],
  [
   "Where can I watch bouyon on video?",
   "Artists' clips are linked from their profiles on this site, and Smokiller's YouTube channel publishes bouyon mixes and remixes."
  ]
 ],
 "Bouyon culture": [
  [
   "Why is it called bouyon?",
   "Bouyon means soup in Kweyol: the genre stirs Dominica's traditional musics together with electronic production."
  ],
  [
   "Is bouyon part of Creole culture?",
   "Yes. Bouyon was born in Dominica's villages and carnival and soundtracks Creole celebrations across the French Caribbean."
  ],
  [
   "What is chante mas?",
   "Chante mas is the traditional singing of Dominica carnival, carried by masquerade groups. Bouyon keeps its call-and-response energy in its fete vocals."
  ],
  [
   "What is Mas Domnik?",
   "Mas Domnik is the name of Dominica carnival, known for its traditional costumes, its chante mas and, since the late 1980s, bouyon as its soundtrack."
  ],
  [
   "Which languages does bouyon sing in?",
   "Bouyon is sung in English, in Kweyol, the Dominican Creole, and in French depending on the artist, from Roseau to Pointe-a-Pitre."
  ]
 ]
}


SITE = os.path.expanduser("~/workspace/bouyonmusique.com/en")
BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)

PAGES = []
for mod in ["data_styles_en", "data_guides_en", "data_places_en", "data_events_artists_en", "data_production_ecoute_en", "data_culture_en", "data_wave1_en", "data_wave1b_en", "data_branches_en", "data_parity_w1_en", "data_parity_w2_en", "data_parity_w3_en", "data_parity_w4_en", "data_parity_w5_en", "data_parity_w6_en", "data_parity_w7_en", "data_parity_w8_en", "data_parity_w9_en", "data_parity_w10_en", "data_parity_w11_en", "data_parity_w12_en", "data_parity_w13_en", "data_parity_w14_en", "data_parity_w15_en", "data_parity_w16_en", "data_parity_w17_en", "data_parity_w18_en", "data_parity_w19_en"]:
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

def faq_text(a):
    """FAQ answers may hold links for the visible copy; schema gets plain text."""
    return html.unescape(re.sub(r"<[^>]+>", "", a))

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
                    # only match plain text, never inside a link inserted earlier in this loop
                    segs = re.split(r'(<a [^>]*>.*?</a>)', part)
                    for j, seg in enumerate(segs):
                        if not seg.startswith("<a ") and pat.search(seg):
                            segs[j] = pat.sub('<a href="' + target + '">' + term + '</a>', seg, count=1)
                            used.add(target)
                            count += 1
                            break
                    part = "".join(segs)
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
    rel = spread_pick(same_cat, page["slug"], 9)
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
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": faq_text(a)}} for q, a in faq_list]})
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
    strip_html = ""
    _is_hub = page["slug"].startswith("artistes-")
    _n = 60 if _is_hub else 24
    _pool = [p for p in same_cat if p not in rel]
    if len(_pool) < _n:
        _have = {p["slug"] for p in _pool} | {p["slug"] for p in rel} | {page["slug"]}
        _pool += [p for p in PAGES if p["slug"] not in _have]
    _strip = spread_pick(_pool, page["slug"] + "|strip", _n)
    if _is_hub and _strip:
        graph.append({"@type": "ItemList", "name": page["nav"], "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": p["nav"], "url": "https://bouyonmusique.com/en/" + p["slug"]} for i, p in enumerate(_strip)]})
    if _strip:
        _t = "More bouyon artists" if page["cat"] == "Bouyon artists" else "Explore this section"
        _links = " \u00b7 ".join(f'<a href="/en/{p["slug"]}">{esc(p["nav"])}</a>' for p in _strip)
        strip_html = f'\n<h2>{_t}</h2>\n<p class="strip">{_links}</p>\n'
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
<meta property="og:image" content="https://bouyonmusique.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Bouyon Musique, the guide to bouyon music">
<meta name="twitter:card" content="summary_large_image">
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
{strip_html}
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
<link rel="alternate" hreflang="x-default" href="https://bouyonmusique.com/plan-du-site.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Bouyon Musique">
<meta property="og:title" content="Site Map - Bouyon Music: every bouyon topic in English">
<meta property="og:description" content="Every English page on BouyonMusique.com: bouyon history, styles, artists, producers, playlists, Dominica Carnival and bouyon scenes by country.">
<meta property="og:url" content="https://bouyonmusique.com/en/site-map.html">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="https://bouyonmusique.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Bouyon Musique, the guide to bouyon music">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bouyonmusique.com/en/"}}, {{"@type": "ListItem", "position": 2, "name": "Site map", "item": "https://bouyonmusique.com/en/site-map.html"}}]}}
</script>
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
