#!/usr/bin/env python3
"""Phase 0 patch (takeover plan 2026-10-20): upgrade both generators with
BreadcrumbList schema, a site entity graph (WebSite / Organization / Smokiller
Person with sameAs), per-category fallback FAQs, and dynamic sitemap lastmod."""
import re

# ---------- FR: generate.py ----------
p = "generate.py"
s = open(p, encoding="utf-8").read()

s = s.replace(
    "import html, importlib, json, os, sys",
    "import datetime, html, importlib, json, os, sys\n\nBUILD_DATE = datetime.date.today().isoformat()\n\nSITE_ENTITIES = [\n"
    "    {\"@type\": \"WebSite\", \"@id\": \"https://bouyonmusique.com/#site\", \"url\": \"https://bouyonmusique.com/\", \"name\": \"Bouyon Musique\", \"inLanguage\": [\"fr\", \"en\"], \"publisher\": {\"@id\": \"https://bouyonmusique.com/#org\"}},\n"
    "    {\"@type\": \"Organization\", \"@id\": \"https://bouyonmusique.com/#org\", \"name\": \"Bouyon Shattaz\", \"url\": \"https://bouyonshattaz.com/\", \"sameAs\": [\"https://www.instagram.com/bouyonshattaz/\", \"https://www.youtube.com/@smo.killer\"]},\n"
    "    {\"@type\": \"Person\", \"@id\": \"https://bouyonmusique.com/#smokiller\", \"name\": \"Smokiller\", \"alternateName\": \"Sean Smokiller Francis\", \"jobTitle\": \"Producteur et artiste bouyon\", \"birthPlace\": \"Dominique\", \"url\": \"https://smokiller.com/\", \"sameAs\": [\"https://www.youtube.com/@smo.killer\", \"https://www.instagram.com/smo.killer/\", \"https://www.tiktok.com/@smo.killer\", \"https://smokiller.com/\"]},\n"
    "]\n\n"
    "CAT_FAQ = {\n"
    "    \"Styles de bouyon\": [(\"Qu'est-ce que le bouyon ?\", \"Le bouyon est un genre musical né en Dominique à la fin des années 1980. Son nom vient du mot kwéyòl pour la soupe : c'est un mélange de jing ping, de cadence-lypso, de calypso et de production électronique, lancé par le groupe WCK.\"), (\"Où écouter les styles de bouyon ?\", \"La page playlists du site rassemble la Bouyon Road Mix de Bouyon Shattaz sur Spotify et YouTube, avec les nouveautés bouyon et les classiques du carnaval.\")],\n"
    "    \"Guides bouyon\": [(\"Par où commencer avec le bouyon ?\", \"Commencez par l'histoire du genre, puis par la playlist Bouyon Road Mix de Bouyon Shattaz, qui mélange classiques du carnaval de Dominique et nouveautés bouyon.\"), (\"Le bouyon vient de quel pays ?\", \"Le bouyon est né en Dominique, dans les Caraïbes, à la fin des années 1980, avec le groupe WCK comme pionnier.\")],\n"
    "    \"Le bouyon par pays\": [(\"Dans quels pays le bouyon est-il populaire ?\", \"Né en Dominique, le bouyon est aujourd'hui central en Guadeloupe et en Martinique, présent en France, à Sainte-Lucie, à Saint-Martin et dans la diaspora caribéenne.\"), (\"Quel pays a créé le bouyon ?\", \"La Dominique. Le genre y est né à la fin des années 1980 et reste le son du carnaval de Roseau.\")],\n"
    "    \"Événements bouyon\": [(\"Quel est le grand festival du bouyon ?\", \"Le World Creole Music Festival se tient chaque année à Roseau, en Dominique. L'édition 2026 a lieu du 23 au 25 octobre au Windsor Park.\"), (\"Quand a lieu le carnaval de Dominique ?\", \"Le carnaval de Dominique, Mas Domnik, se tient avant le carême, avec le J'ouvert comme moment fort des musiques bouyon et soca.\")],\n"
    "    \"Artistes bouyon\": [(\"Qui sont les artistes bouyon de référence ?\", \"WCK a créé le genre, Asa Bantan est largement surnommé le King of Bouyon, et la nouvelle génération compte Reo, Ridge, Signal Band et Shelly, pendant que des producteurs comme Smokiller exportent le son.\"), (\"Qui publie ces pages artistes ?\", \"BouyonMusique.com est publié par Bouyon Shattaz, la plateforme du producteur dominicain Smokiller, avec des faits vérifiés artiste par artiste.\")],\n"
    "    \"Production bouyon\": [(\"Qui produit du bouyon aujourd'hui ?\", \"Des producteurs comme Smokiller (Bouyon Shattaz), Denmath, HYPNO! ou Savion travaillent le son bouyon, entre riddims, remixes et productions originales.\"), (\"Qu'est-ce qu'un riddim bouyon ?\", \"Un riddim est l'instrumental sur lequel plusieurs artistes posent leurs voix. Les riddims sont au cœur de la production bouyon et dancehall.\")],\n"
    "    \"Écouter le bouyon\": [(\"Où écouter du bouyon en ligne ?\", \"Sur la Bouyon Road Mix de Bouyon Shattaz, disponible sur Spotify et YouTube via la page playlists de ce site.\"), (\"Comment recevoir la playlist bouyon ?\", \"Suivez @bouyonshattaz sur Instagram et commentez ROAD MIX sous une publication : la playlist vous est envoyée en message privé.\")],\n"
    "    \"Culture bouyon\": [(\"Pourquoi le bouyon s'appelle-t-il ainsi ?\", \"Bouyon veut dire soupe en kwéyòl : le genre mélange les ingrédients des musiques traditionnelles dominiquaises avec la production électronique.\"), (\"Le bouyon fait-il partie de la culture créole ?\", \"Oui. Le bouyon est né dans les villages et le carnaval de la Dominique et il accompagne les fêtes créoles dans toute la Caraïbe francophone.\")],\n"
    "}\n",
    1,
)

old_block = '''    faq_html = ""
    ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "url": url,
        "name": page["title"],
        "description": page["desc"],
        "inLanguage": page.get("lang", "fr"),
        "isPartOf": {"@type": "WebSite", "url": "https://bouyonmusique.com/", "name": "Bouyon Musique"},
        "publisher": {"@type": "Organization", "name": "Bouyon Shattaz", "url": "https://bouyonshattaz.com/"},
    }
    graph = [ld]
    if page.get("faq"):
        faq_html = '\\n<h2>Questions fréquentes</h2>\\n'
        for q, a in page["faq"]:
            faq_html += f"<details><summary>{esc(q)}</summary><p>{a}</p></details>\\n"
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a.replace("<a href=", "").split(">")[0] if "<" in a else a}}
                for q, a in page["faq"]
            ],
        })'''
new_block = '''    faq_list = page.get("faq") or CAT_FAQ.get(page["cat"], [])
    faq_html = ""
    ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "@id": url + "#page",
        "url": url,
        "name": page["title"],
        "description": page["desc"],
        "inLanguage": page.get("lang", "fr"),
        "dateModified": BUILD_DATE,
        "isPartOf": {"@id": "https://bouyonmusique.com/#site"},
        "publisher": {"@id": "https://bouyonmusique.com/#org"},
        "author": {"@id": "https://bouyonmusique.com/#smokiller"},
    }
    breadcrumb = {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://bouyonmusique.com/"},
            {"@type": "ListItem", "position": 2, "name": page["cat"], "item": "https://bouyonmusique.com/plan-du-site.html"},
            {"@type": "ListItem", "position": 3, "name": page["nav"], "item": url},
        ],
    }
    graph = [ld, breadcrumb] + SITE_ENTITIES
    if faq_list:
        faq_html = '\\n<h2>Questions fréquentes</h2>\\n'
        for q, a in faq_list:
            faq_html += f"<details><summary>{esc(q)}</summary><p>{a}</p></details>\\n"
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faq_list
            ],
        })'''
assert old_block in s, "FR render block not found"
s = s.replace(old_block, new_block, 1)
s = s.replace("<lastmod>2026-10-17</lastmod>", "<lastmod>{BUILD_DATE}</lastmod>", 1)
open(p, "w", encoding="utf-8").write(s)
print("generate.py patched")

# ---------- EN: generate_en_full.py ----------
p = "generate_en_full.py"
s = open(p, encoding="utf-8").read()

assert "import html, importlib, json, os, sys" in s, "EN import line not found"
s = s.replace(
    "import html, importlib, json, os, sys",
    "import datetime, html, importlib, json, os, sys\n\nBUILD_DATE = datetime.date.today().isoformat()\n\nSITE_ENTITIES = [\n", 1)
s = s.replace(
    "SITE_ENTITIES = [\n",
    "SITE_ENTITIES = [\n"
    '    {"@type": "WebSite", "@id": "https://bouyonmusique.com/#site", "url": "https://bouyonmusique.com/", "name": "Bouyon Musique", "inLanguage": ["fr", "en"], "publisher": {"@id": "https://bouyonmusique.com/#org"}},\n'
    '    {"@type": "Organization", "@id": "https://bouyonmusique.com/#org", "name": "Bouyon Shattaz", "url": "https://bouyonshattaz.com/", "sameAs": ["https://www.instagram.com/bouyonshattaz/", "https://www.youtube.com/@smo.killer"]},\n'
    '    {"@type": "Person", "@id": "https://bouyonmusique.com/#smokiller", "name": "Smokiller", "alternateName": "Sean Smokiller Francis", "jobTitle": "Bouyon artist and producer", "birthPlace": "Dominica", "url": "https://smokiller.com/", "sameAs": ["https://www.youtube.com/@smo.killer", "https://www.instagram.com/smo.killer/", "https://www.tiktok.com/@smo.killer", "https://smokiller.com/"]},\n'
    ']\n\n'
    'CAT_FAQ = {\n'
    '    "Bouyon styles": [("What is bouyon music?", "Bouyon is a genre born in Dominica in the late 1980s. Its name comes from the Kweyol word for soup: it blends jing ping, cadence-lypso, calypso and electronic production, pioneered by the band WCK."), ("Where can I hear the bouyon styles?", "The playlist page collects the Bouyon Road Mix by Bouyon Shattaz on Spotify and YouTube, with new bouyon and carnival classics.")],\n'
    '    "Bouyon guides": [("Where do I start with bouyon?", "Start with the history of the genre, then the Bouyon Road Mix playlist by Bouyon Shattaz, which mixes Dominica carnival classics with new bouyon."), ("Which country created bouyon?", "Dominica, in the late 1980s, with WCK as the pioneering band.")],\n'
    '    "Bouyon by country": [("Where is bouyon popular?", "Born in Dominica, bouyon is now central in Guadeloupe and Martinique and present in France, Saint Lucia, Saint Martin and the Caribbean diaspora."), ("Which country created bouyon?", "Dominica. The genre was born there in the late 1980s and remains the sound of Roseau carnival.")],\n'
    '    "Bouyon events": [("What is the big bouyon festival?", "The World Creole Music Festival is held every year in Roseau, Dominica. The 2026 edition runs October 23 to 25 at Windsor Park."), ("When is Dominica carnival?", "Dominica carnival, Mas Domnik, takes place before Lent, with J\'ouvert as a peak moment for bouyon and soca.")],\n'
    '    "Bouyon artists": [("Who are the key bouyon artists?", "WCK created the genre, Asa Bantan is widely called the King of Bouyon, and the new generation includes Reo, Ridge, Signal Band and Shelly, while producers like Smokiller export the sound."), ("Who publishes these artist pages?", "BouyonMusique.com is published by Bouyon Shattaz, the platform of Dominican-born producer Smokiller, with facts verified artist by artist.")],\n'
    '    "Bouyon production": [("Who produces bouyon today?", "Producers like Smokiller (Bouyon Shattaz), Denmath, HYPNO! and Savion work the bouyon sound across riddims, remixes and original productions."), ("What is a bouyon riddim?", "A riddim is the instrumental several artists record over. Riddims sit at the heart of bouyon and dancehall production.")],\n'
    '    "Listen to bouyon": [("Where can I listen to bouyon online?", "On the Bouyon Road Mix by Bouyon Shattaz, on Spotify and YouTube via this site\'s playlist page."), ("How do I get the bouyon playlist?", "Follow @bouyonshattaz on Instagram and comment ROAD MIX on a post: the playlist is sent to your DMs.")],\n'
    '    "Bouyon culture": [("Why is it called bouyon?", "Bouyon means soup in Kweyol: the genre stirs Dominica\'s traditional musics together with electronic production."), ("Is bouyon part of Creole culture?", "Yes. Bouyon was born in Dominica\'s villages and carnival and soundtracks Creole celebrations across the French Caribbean.")],\n'
    '}\n',
    1,
)

old_en = '''    graph = [{
        "@context": "https://schema.org", "@type": "WebPage", "url": url,
        "name": page["title"], "description": page["desc"], "inLanguage": "en",
        "isPartOf": {"@type": "WebSite", "url": "https://bouyonmusique.com/", "name": "Bouyon Musique"},
        "publisher": {"@type": "Organization", "name": "Bouyon Shattaz", "url": "https://bouyonshattaz.com/"},
    }]
    faq_html = ""
    if page.get("faq"):
        faq_html = '\\n<h2>Frequently asked questions</h2>\\n'
        for q, a in page["faq"]:
            faq_html += f"<details><summary>{esc(q)}</summary><p>{a}</p></details>\\n"
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in page["faq"]]})'''
new_en = '''    faq_list = page.get("faq") or CAT_FAQ.get(page["cat"], [])
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
    faq_html = ""
    if faq_list:
        faq_html = '\\n<h2>Frequently asked questions</h2>\\n'
        for q, a in faq_list:
            faq_html += f"<details><summary>{esc(q)}</summary><p>{a}</p></details>\\n"
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_list]})'''
assert old_en in s, "EN render block not found"
s = s.replace(old_en, new_en, 1)
open(p, "w", encoding="utf-8").write(s)
print("generate_en_full.py patched")
