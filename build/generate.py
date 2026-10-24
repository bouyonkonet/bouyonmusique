#!/usr/bin/env python3
"""Generator for bouyonmusique.com expansion pages.
Reads PAGES from data modules, writes SEO HTML pages into the site folder,
regenerates sitemap.xml and plan-du-site.html.
"""
import datetime, hashlib, html, importlib, json, os, re, sys

BUILD_DATE = datetime.date.today().isoformat()

MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]

def fmt_date_fr(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {MONTHS_FR[d.month - 1]} {d.year}"

def spread_date(key):
    """Deterministic pseudo publication date in 2026-09-01..2026-10-16, by slug hash."""
    h = int(hashlib.md5(key.encode("utf-8")).hexdigest()[:8], 16)
    return (datetime.date(2026, 9, 1) + datetime.timedelta(days=h % 46)).isoformat()

SITE_ENTITIES = [
    {"@type": "WebSite", "@id": "https://bouyonmusique.com/#site", "url": "https://bouyonmusique.com/", "name": "Bouyon Musique", "inLanguage": ["fr", "en"], "publisher": {"@id": "https://bouyonmusique.com/#org"}},
    {"@type": "Organization", "@id": "https://bouyonmusique.com/#org", "name": "Bouyon Shattaz", "url": "https://bouyonshattaz.com/", "sameAs": ["https://www.instagram.com/bouyonshattaz/", "https://www.youtube.com/@smo.killer"]},
    {"@type": "Person", "@id": "https://bouyonmusique.com/#smokiller", "name": "Smokiller", "jobTitle": "Producteur et artiste bouyon", "birthPlace": "Dominique", "url": "https://smokiller.com/", "sameAs": ["https://www.youtube.com/@smo.killer", "https://www.instagram.com/smo.killer/", "https://www.tiktok.com/@smo.killer", "https://smokiller.com/"]},
]

CAT_FAQ = {
 "Styles de bouyon": [
  [
   "Qu'est-ce que le bouyon ?",
   "Le bouyon est un genre musical né en Dominique à la fin des années 1980. Son nom vient du mot kwéyòl pour la soupe : c'est un mélange de jing ping, de cadence-lypso, de calypso et de production électronique, lancé par le groupe WCK."
  ],
  [
   "Quels sont les ingrédients du bouyon ?",
   "Le bouyon mélange le jing ping, la cadence-lypso, le calypso et le chanté mas aux claviers et à la production électronique. C'est ce mélange, né en Dominique, qui lui donne son énergie de carnaval."
  ],
  [
   "Quelle est la différence entre le bouyon et le bouyon soca ?",
   "Le bouyon soca fusionne le bouyon dominicain avec les codes festifs de la soca. Selon le témoignage de première main de Smokiller, présent dans les studios à l'époque, le bouyon soca a été lancé en Dominique par Dada en 2003, avant d'être popularisé par Triple Kay et d'autres groupes."
  ],
  [
   "Qu'est-ce que le Wrecketeng ?",
   "Le Wrecketeng est la pratique dominicaine qui reconstruit des enregistrements existants sur des instrumentaux bouyon, dans la lignée du bouyon-muffin. Son orthographe officielle vient de DJ Cut, le pionnier du style ; la forme « reketeng » répandue sur internet est une erreur."
  ],
  [
   "Où écouter les styles de bouyon ?",
   "La page playlists du site rassemble la Bouyon Road Mix de Bouyon Shattaz sur Spotify et YouTube, avec les nouveautés bouyon et les classiques du carnaval."
  ]
 ],
 "Guides bouyon": [
  [
   "Par où commencer avec le bouyon ?",
   "Commencez par l'histoire du genre, puis par la playlist Bouyon Road Mix de Bouyon Shattaz, qui mélange classiques du carnaval de Dominique et nouveautés bouyon."
  ],
  [
   "Le bouyon vient de quel pays ?",
   "Le bouyon est né en Dominique, dans les Caraïbes, à la fin des années 1980, avec le groupe WCK comme pionnier."
  ],
  [
   "Comment danser le bouyon ?",
   "Le bouyon se danse en fête et au carnaval, sur des rythmes rapides pensés pour la route et les bands. Ce site consacre une page à la danse bouyon et à ses repères de base."
  ],
  [
   "Quelle playlist bouyon écouter en 2026 ?",
   "La Bouyon Road Mix de Bouyon Shattaz, sur Spotify et YouTube, rassemble les nouveautés bouyon et les classiques du carnaval de Dominique."
  ],
  [
   "Le bouyon et le shatta, est-ce la même chose ?",
   "Non. Le shatta est un sous-genre du dancehall né en Martinique, plus lent, tandis que le bouyon est né en Dominique avec des rythmes rapides de carnaval. Les deux scènes se croisent souvent, et des productions récentes les fusionnent."
  ]
 ],
 "Le bouyon par pays": [
  [
   "Dans quels pays le bouyon est-il populaire ?",
   "Né en Dominique, le bouyon est aujourd'hui central en Guadeloupe et en Martinique, présent en France, à Sainte-Lucie, à Saint-Martin et dans la diaspora caribéenne."
  ],
  [
   "Quel pays a créé le bouyon ?",
   "La Dominique. Le genre y est né à la fin des années 1980 et reste le son du carnaval de Roseau."
  ],
  [
   "Pourquoi le bouyon est-il si fort en Guadeloupe ?",
   "Le bouyon gwada s'est développé en Guadeloupe au contact des tournées des groupes dominicains comme WCK et Triple Kay : paroles en créole et beats électroniques, avec une branche plus dure, le bouyon hardcore."
  ],
  [
   "Quel rôle joue la Martinique dans le bouyon ?",
   "La Martinique est la terre du shatta et une place forte du bouyon dans les Antilles françaises : ses artistes et ses producteurs font circuler les deux sons entre Fort-de-France, la Guadeloupe et la Dominique."
  ],
  [
   "Où le bouyon se joue-t-il en France ?",
   "En France, le bouyon vit dans la diaspora antillaise, notamment à Paris, et sur les scènes et les plateformes qui programment les artistes de Guadeloupe, de Martinique et de Dominique."
  ]
 ],
 "Événements bouyon": [
  [
   "Quel est le grand festival du bouyon ?",
   "Le World Creole Music Festival se tient chaque année à Roseau, en Dominique. L'édition 2026 a lieu du 23 au 25 octobre au Windsor Park."
  ],
  [
   "Quand a lieu le carnaval de Dominique ?",
   "Le carnaval de Dominique, Mas Domnik, se tient avant le carême, avec le J'ouvert comme moment fort des musiques bouyon et soca."
  ],
  [
   "Qu'est-ce que le J'ouvert ?",
   "Le J'ouvert ouvre le carnaval de Dominique aux premières heures du matin : bands, peinture et musique bouyon et soca dans les rues de Roseau, avant les parades des jours gras."
  ],
  [
   "Où se tient le World Creole Music Festival ?",
   "Le World Creole Music Festival se tient au Windsor Park, à Roseau, la capitale de la Dominique. L'édition 2026 a lieu du 23 au 25 octobre."
  ],
  [
   "Quels artistes bouyon jouent au WCMF 2026 ?",
   "Les guides publiés du festival annoncent notamment Asa Bantan, Reo, Trilla-G, Signal Band et TK International parmi les noms bouyon de l'édition 2026, répartis sur trois nuits."
  ]
 ],
 "Artistes bouyon": [
  [
   "Qui sont les artistes bouyon de référence ?",
   "WCK a créé le genre, Asa Bantan est largement surnommé le King of Bouyon, et la nouvelle génération compte Reo, Ridge, Signal Band et Shelly, pendant que des producteurs comme Smokiller exportent le son."
  ],
  [
   "Qui publie ces pages artistes ?",
   "BouyonMusique.com est publié par Bouyon Shattaz, la plateforme de Smokiller, producteur né en Dominique, avec des faits vérifiés artiste par artiste."
  ],
  [
   "Quel groupe a créé le bouyon ?",
   "WCK, groupe de la Dominique, a lancé le bouyon à la fin des années 1980 en fusionnant la cadence-lypso et les musiques traditionnelles de l'île."
  ],
  [
   "Qui sont les producteurs derrière le bouyon d'aujourd'hui ?",
   "Des producteurs comme Smokiller, Denmath ou HYPNO! travaillent le son actuel, pendant que la mémoire du genre passe par des pionniers du sampling comme DJ Cut et les crews de Roseau."
  ],
  [
   "Comment les profils de ce site sont-ils écrits ?",
   "Chaque profil est écrit à partir de recherches vérifiées, artiste par artiste, avec des titres et des crédits sourcés. Les surnoms comme King of Bouyon sont toujours attribués, jamais présentés comme des faits."
  ]
 ],
 "Production bouyon": [
  [
   "Qui produit du bouyon aujourd'hui ?",
   "Des producteurs comme Smokiller (Bouyon Shattaz), Denmath, HYPNO! ou Savion travaillent le son bouyon, entre riddims, remixes et productions originales."
  ],
  [
   "Qu'est-ce qu'un riddim bouyon ?",
   "Un riddim est l'instrumental sur lequel plusieurs artistes posent leurs voix. Les riddims sont au cœur de la production bouyon et dancehall."
  ],
  [
   "Quels instruments font le son bouyon ?",
   "Les claviers en boucle, les percussions programmées et les basses électroniques portent le bouyon moderne, sur un socle hérité du jing ping et du lapo kabwit, les percussions traditionnelles de la Dominique."
  ],
  [
   "Comment un riddim devient-il un titre ?",
   "Le producteur construit l'instrumental, puis un ou plusieurs artistes posent leurs voix dessus. Un même riddim peut porter plusieurs titres, comme dans la culture dancehall dont le bouyon est proche."
  ],
  [
   "Où trouver des productions bouyon récentes ?",
   "Les pages production de ce site et la playlist Bouyon Road Mix suivent les sorties récentes, des riddims des producteurs de l'île aux remixes bouyon de Smokiller."
  ]
 ],
 "Écouter le bouyon": [
  [
   "Où écouter du bouyon en ligne ?",
   "Sur la Bouyon Road Mix de Bouyon Shattaz, disponible sur Spotify et YouTube via la page playlists de ce site."
  ],
  [
   "Comment recevoir la playlist bouyon ?",
   "Suivez @bouyonshattaz sur Instagram et commentez ROAD MIX sous une publication : la playlist vous est envoyée en message privé."
  ],
  [
   "Quelles chansons bouyon écouter en premier ?",
   "Les classiques de WCK, les titres de Triple Kay et les succès actuels d'Asa Bantan ou de Reo forment le socle d'une première écoute, complété par la Bouyon Road Mix."
  ],
  [
   "Le bouyon s'écoute-t-il toute l'année ?",
   "Oui. Né pour le carnaval, le bouyon vit toute l'année dans les fêtes de la Dominique, au World Creole Music Festival en octobre et dans les playlists des Antilles françaises et de la diaspora."
  ],
  [
   "Où voir le bouyon en vidéo ?",
   "Les clips des artistes sont liés depuis leurs profils sur ce site, et la chaîne YouTube de Smokiller publie des mixes et des remixes bouyon."
  ]
 ],
 "Culture bouyon": [
  [
   "Pourquoi le bouyon s'appelle-t-il ainsi ?",
   "Bouyon veut dire soupe en kwéyòl : le genre mélange les ingrédients des musiques traditionnelles dominiquaises avec la production électronique."
  ],
  [
   "Le bouyon fait-il partie de la culture créole ?",
   "Oui. Le bouyon est né dans les villages et le carnaval de la Dominique et il accompagne les fêtes créoles dans toute la Caraïbe francophone."
  ],
  [
   "Qu'est-ce que le chanté mas ?",
   "Le chanté mas est le chant traditionnel du carnaval dominiquais, porté par les groupes de mascarade. Le bouyon en garde l'énergie d'appel et de réponse dans ses voix de fête."
  ],
  [
   "Qu'est-ce que le Mas Domnik ?",
   "Mas Domnik est le nom du carnaval de la Dominique, réputé pour ses costumes traditionnels, son chanté mas et, depuis la fin des années 1980, le bouyon comme bande-son."
  ],
  [
   "Dans quelles langues chante le bouyon ?",
   "Le bouyon se chante en anglais, en kwéyòl, le créole dominiquais, et en français selon les artistes, de Roseau à Pointe-à-Pitre."
  ]
 ]
}


SITE = os.environ.get("BOUYONMUSIQUE_SITE") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PAGES = []
for mod in ["data_styles", "data_guides", "data_places", "data_events_artists", "data_production_ecoute", "data_culture", "data_wave1", "data_wave1b", "data_branches", "data_parity_w1", "data_parity_w2", "data_parity_w3", "data_parity_w4", "data_parity_w5", "data_parity_w6", "data_parity_w7", "data_parity_w8", "data_parity_w9", "data_parity_w10", "data_parity_w11", "data_parity_w12", "data_parity_w13", "data_parity_w14", "data_parity_w15", "data_parity_w16", "data_parity_w17", "data_parity_w18", "data_parity_w19", "data_parity_w20", "data_parity_w21", "data_parity_w22", "data_parity_w23", "data_parity_w24", "data_parity_w25", "data_parity_w26", "data_parity_w27", "data_parity_w28", "data_parity_w29", "data_parity_w30", "data_parity_w31", "data_parity_w32", "data_parity_w33", "data_parity_w34", "data_parity_w35", "data_parity_w36", "data_daily_20261021", "data_playlist_pages"]:
    m = importlib.import_module(mod)
    PAGES.extend(m.PAGES)

for _p in PAGES:
    _p.setdefault("date_published", spread_date(_p["slug"]))

FR2EN = {}
ENDATES = {}
for _mod in ["data_styles_en", "data_guides_en", "data_places_en", "data_events_artists_en", "data_production_ecoute_en", "data_culture_en", "data_wave1_en", "data_wave1b_en", "data_branches_en", "data_parity_w1_en", "data_parity_w2_en", "data_parity_w3_en", "data_parity_w4_en", "data_parity_w5_en", "data_parity_w6_en", "data_parity_w7_en", "data_parity_w8_en", "data_parity_w9_en", "data_parity_w10_en", "data_parity_w11_en", "data_parity_w12_en", "data_parity_w13_en", "data_parity_w14_en", "data_parity_w15_en", "data_parity_w16_en", "data_parity_w17_en", "data_parity_w18_en", "data_parity_w19_en", "data_parity_w20_en", "data_parity_w21_en", "data_parity_w22_en", "data_parity_w23_en", "data_parity_w24_en", "data_parity_w25_en", "data_parity_w26_en", "data_parity_w27_en", "data_parity_w28_en", "data_parity_w29_en", "data_parity_w30_en", "data_parity_w31_en", "data_parity_w32_en", "data_parity_w33_en", "data_parity_w34_en", "data_parity_w35_en", "data_parity_w36_en", "data_daily_20261021_en", "data_playlist_pages_en"]:
    try:
        _m = importlib.import_module(_mod)
        for _p in _m.PAGES:
            FR2EN[_p["fr_slug"]] = _p["slug"]
            ENDATES[_p["slug"]] = _p.get("date_modified") or _p.get("date_published") or spread_date(_p["fr_slug"])
    except Exception:
        pass
# Two EN pages can share a slug (the later module wins on disk): only keep the FR page the published EN page points to.
_en_owner = {}
for _fr, _en in FR2EN.items():
    _en_owner[_en] = _fr
FR2EN = {_fr: _en for _fr, _en in FR2EN.items() if _en_owner[_en] == _fr}

# Artist hubs, mixtapes and chroniques (BOU-3200): see hubs.py and editorial.py.
import editorial, hubs
from data_chroniques import CHRONIQUES
from data_mixtapes import MIXTAPES, SMOKILLER_CHANNEL
EDITORIAL = editorial.items(MIXTAPES, CHRONIQUES)
PAGE_BY_SLUG = {p["slug"]: p for p in PAGES + EDITORIAL}
ARTISTS = hubs.artists(PAGES)
ARTIST_BY_SLUG = {a["slug"]: a for a in ARTISTS}
MENTIONS = hubs.mentions(PAGES, ARTISTS, "/")
MENTIONS.update({e["slug"]: e["artists"] for e in EDITORIAL})
MENTIONED_IN = hubs.invert(MENTIONS)

CORE = [
    ("/", "Bouyon Musique (accueil)"),
    ("/histoire.html", "Histoire du bouyon"),
    ("/artistes.html", "Artistes bouyon"),
    ("/playlist-bouyon.html", "Playlist bouyon"),
    ("/bouyon-danse.html", "Bouyon danse"),
    ("/faq.html", "FAQ bouyon"),
    ("/en/", "Bouyon Music (EN)"),
]

def faq_text(a):
    """FAQ answers may hold links for the visible copy; schema gets plain text."""
    return html.unescape(re.sub(r"<[^>]+>", "", a))

def esc(s):
    return html.escape(s, quote=True)

def header(active_cat):
    return """<header>
  <div class="wrap nav">
    <a class="logo" href="/">BOUYON<span>MUSIQUE</span>.COM</a>
    <nav class="main" aria-label="Navigation principale">
      <a href="/">Accueil</a>
      <a href="/histoire.html">Histoire</a>
      <a href="/artistes.html">Artistes</a>
      <a href="/playlist-bouyon.html">Playlists</a>
      <a href="/mixtapes/">Mixtapes</a>
      <a href="/bouyon-danse.html">Bouyon danse</a>
      <a href="/plan-du-site.html">Tous les sujets</a>
      <a href="/faq.html">FAQ</a>
      <a href="/en/">EN</a>
    </nav>
  </div>
</header>"""

def footer(page, same_cat):
    links = "\n".join(f'        <li><a href="/{p["slug"]}">{esc(p["nav"])}</a></li>' for p in spread_pick(same_cat, page["slug"] + "|footer", 8))
    return f"""<footer>
  <div class="wrap cols">
    <div>
      <h4>BouyonMusique.com</h4>
      <p>Le guide francophone de la musique bouyon : histoire, artistes, danses, riddims et playlists. Publié par Bouyon Shattaz. Citations bienvenues avec un lien vers la page source.</p>
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
        <li><a href="https://bouyonshattaz.com/">bouyonshattaz.com</a></li><li><a href="https://bouyonsoca.com/">BouyonSoca : catalogues des artistes caribéens</a></li><li><a href="https://smokiller.com/">Smokiller : riddims et remixes bouyon</a></li>
        <li><a href="https://www.instagram.com/bouyonshattaz/">Instagram @bouyonshattaz</a></li>
        <li><a href="/plan-du-site.html">Plan du site : tous les sujets bouyon</a></li>
        <li><a href="/en/">English version: Bouyon Music</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap"><p style="margin-top:24px">© 2026 Bouyon Shattaz. Le bouyon est né en Dominique.</p></div>
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
            if t and t not in GENERIC_TERMS and t not in hubs.LINK_ONLY and len(t) >= 3:
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
                        m = None if seg.startswith("<a ") else hubs.first_match(pat, seg)
                        if m:
                            segs[j] = seg[:m.start()] + '<a href="' + target + '">' + term + '</a>' + seg[m.end():]
                            used.add(target)
                            count += 1
                            break
                    part = "".join(segs)
                parts[i] = part
            new_paras.append("".join(parts))
        out.append((h2, new_paras))
    return out

EXTRA_TERMS_FR = {
    "cadence-lypso": "racines-cadence-lypso.html",
    "World Creole Music Festival": "wcmf-festival-creole.html",
    "Mas Domnik": "mas-domnik.html",
}

# Playlist embeds (2026-10-21): matched by keyword between page topic and
# playlist title, description and track themes. See playlist-embeds/match-table.md
# (round 1 + round 2, supplied playlist links). Max one YouTube embed per
# page. Providers stack YouTube first.
_YT_BEST2026 = ("youtube", "PLB1axoRydQreXaKD2wlZ5IHJmNmoTWEEd", "Bouyon Music 2026 - Best New Bouyon Songs (Dominica Bouyon Hits)")
_YT_CARNIVAL2026 = ("youtube", "PLB1axoRydQrc3nyVJe_7Jh1ts4rzydf96", "Dominica Carnival 2026 - Mas Domnik Bouyon Road Anthems")
_YT_GWADA_PLAYLIST = ("youtube", "PLStLo0THKPaA", "Bouyon Gwada 2026 - Playlist Bouyon Guadeloupe & Martinique")
_YT_INSTRUMENTALS = ("youtube", "PLaTpX9xYuQ3Q", "Bouyon Instrumentals - Bouyon Riddim Beats & Type Beats (Free + 2026)")
_YT_KULTURAL = ("youtube", "PLGSMHEqIn1ws", "dominica kultural music | Smokiller Selection")
_YT_CREOLEDAY = ("youtube", "PLeRfSYxTrhsM", "Creole Day Songs | Jounen Kweyol, St Lucia & Dominica | Smokiller")
PLAYLIST_EMBEDS = {
    "bouyon-mix.html": [
        ("youtube", "PLB1axoRydQrdtCBSbvnkbSoKWJxFV8Xto", "Shatta Bouyon Mix 2026 | Dancehall & Afrobeats"),
        ("spotify", "4ikmgg9FzDug5tLttfhfQp", "Bouyon Music 2026 | Road Mix"),
    ],
    "dancehall-bouyon.html": [
        ("youtube", "PLB1axoRydQrdtCBSbvnkbSoKWJxFV8Xto", "Shatta Bouyon Mix 2026 | Dancehall & Afrobeats"),
        ("spotify", "4ikmgg9FzDug5tLttfhfQp", "Bouyon Music 2026 | Road Mix"),
    ],
    "playlist-shatta.html": [
        ("youtube", "PLRObCvDH1pO4", "Shatta Bouyon Playlist - Clips, Mixes et Dancehall Antillais"),
    ],
    "shatta-bouyon.html": [
        ("youtube", "PLB1axoRydQrdtCBSbvnkbSoKWJxFV8Xto", "Shatta Bouyon Mix 2026 | Dancehall & Afrobeats"),
    ],
    "bouyon-music-2026.html": [
        _YT_BEST2026,
        ("spotify", "4ikmgg9FzDug5tLttfhfQp", "Bouyon Music 2026 | Road Mix"),
    ],
    "nouveautes-bouyon-2026.html": [
        _YT_BEST2026,
        ("spotify", "4ikmgg9FzDug5tLttfhfQp", "Bouyon Music 2026 | Road Mix"),
    ],
    "chansons-bouyon.html": [
        ("youtube", "PLNzqsHgDlE0A", "Bouyon Songs 2026 - New Bouyon Music & Dominica Hits"),
        ("spotify", "4ikmgg9FzDug5tLttfhfQp", "Bouyon Music 2026 | Road Mix"),
    ],
    "meilleur-bouyon.html": [_YT_BEST2026],
    "old-school-bouyon.html": [
        ("youtube", "PLNlp6SK-JfuM", "WCK | Smokiller Selection 04"),
    ],
    "jing-ping.html": [_YT_KULTURAL],
    "bele-dominique.html": [_YT_KULTURAL],
    "bouyon-dominique.html": [
        ("youtube", "PLNqev8eauH84", "Dominica | Smokiller Selection"),
    ],
    "jump-up.html": [
        ("youtube", "PLFF6EdvjYi3k", "Jump up retro | Smokiller Selection"),
    ],
    "bouyon-sainte-lucie.html": [
        ("youtube", "PLFgskLhMaWWs", "st lucia zouks | Smokiller Selection"),
    ],
    "wck.html": [
        ("youtube", "PLcjMlMWDC5Jk", "Wck Bouyon | Smokiller Selection"),
    ],
    "bouyon-et-kweyol.html": [_YT_CREOLEDAY],
    "jounen-kweyol.html": [_YT_CREOLEDAY],
    "dj-mj.html": [
        ("youtube", "PLSfJDEQ1jpP4", "Bouyon Mix Clean - DJ Mixes and Radio Edits"),
    ],
    "miimii-kds.html": [
        ("youtube", "PLLXnxmIwXHyc", "Miimii KDS Bouyon - Clips, Portrait, Âge et Origine"),
    ],
    "qu-est-ce-que-le-bouyon.html": [
        ("youtube", "PLcjYRwKbRx68", "What Is Bouyon Music? Dominica History, Origins & Classics"),
    ],
    "bouyon-instrumental.html": [_YT_INSTRUMENTALS],
    "bouyon-type-beat.html": [_YT_INSTRUMENTALS],
    "bouyon-riddim.html": [
        ("youtube", "PLB1axoRydQre6mPaGbs_R3p-3JAp06EMo", "Bouyon Riddims 2026 - New Bouyon Riddim Songs & Warm Ups"),
    ],
    "bouyon-gwada.html": [_YT_GWADA_PLAYLIST],
    "bouyon-guadeloupe.html": [_YT_GWADA_PLAYLIST],
    "bouyon-martinique.html": [
        ("youtube", "PLCQdGQzS_iaI", "Bouyon Gwada 2026 - Best Guadeloupe & Martinique Bouyon (Clip Officiel)"),
    ],
    "gospel-bouyon.html": [
        ("youtube", "PLKtZbNpmSpWI", "Gospel Bouyon - Best Christian Bouyon Songs & Gospel Bouyon Remixes"),
    ],
    "dominica-carnival-2026.html": [_YT_CARNIVAL2026],
    "mas-domnik.html": [_YT_CARNIVAL2026],
}

from sources_listen import listen_sources_html

def playlist_embeds_html(slug):
    out = ""
    for kind, pid, title in PLAYLIST_EMBEDS.get(slug, []):
        if kind == "youtube":
            out += ('\n<h2>À regarder aussi</h2>\n'
                    f'<h3>{esc(title)}</h3>\n'
                    '<div style="position:relative;padding-top:56.25%;margin:1em 0">'
                    f'<iframe src="https://www.youtube-nocookie.com/embed/videoseries?list={pid}" title="{esc(title)}" loading="lazy" '
                    'style="position:absolute;inset:0;width:100%;height:100%;border:0;border-radius:12px" '
                    'allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>\n')
        else:
            out += ('\n<h2>À écouter aussi</h2>\n'
                    f'<h3>{esc(title)}</h3>\n'
                    f'<iframe src="https://open.spotify.com/embed/playlist/{pid}?utm_source=generator" title="{esc(title)}" width="100%" height="352" '
                    'style="border:0;border-radius:12px" loading="lazy" allow="clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>\n')
    return out

def byline(page):
    pub, mod = page.get("date_published"), page.get("date_modified")
    out = f'<p class="pubdate">Par <a href="/smokiller.html" rel="author">Smokiller</a> · Publié le <time datetime="{pub}">{fmt_date_fr(pub)}</time>'
    if mod and mod > pub:
        out += f' · Mis à jour le <time datetime="{mod}">{fmt_date_fr(mod)}</time>'
    return out + "</p>"

def cited_html(slugs):
    """Every page: the artists it mentions, linked to their profiles."""
    if not slugs:
        return ""
    links = " \u00b7 ".join(f'<a href="/{s}">{esc(ARTIST_BY_SLUG[s]["nav"])}</a>' for s in slugs)
    return f'\n<h2>Artistes cités dans cette page</h2>\n<p class="strip">{links}</p>\n'

def hub_html(page):
    """Artist profiles: every page of the site that mentions the artist, grouped by section."""
    refs = [PAGE_BY_SLUG[s] for s in MENTIONED_IN.get(page["slug"], [])]
    if page["slug"] not in ARTIST_BY_SLUG or not refs:
        return "", None
    groups = {}
    for r in refs:
        groups.setdefault(r["cat"], []).append(r)
    name = page["nav"]
    lead = f"Une page du site cite {esc(name)}." if len(refs) == 1 else f"{len(refs)} pages du site citent {esc(name)}."
    out = f'\n<h2>{esc(name)} sur Bouyon Musique</h2>\n<p>{lead}</p>\n'
    for cat in sorted(groups, key=lambda c: (c not in ("Mixtapes", "Chroniques"), c == "Artistes bouyon")):
        links = " \u00b7 ".join(f'<a href="/{r["slug"]}">{esc(r["nav"])}</a>' for r in groups[cat])
        out += f'<h3>{esc(cat)}</h3>\n<p class="strip">{links}</p>\n'
    ld = {"@type": "ItemList", "name": f"Pages qui citent {name}", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": r["nav"], "url": "https://bouyonmusique.com/" + r["slug"]} for i, r in enumerate(refs)]}
    return out, ld

def render(page, all_pages):
    same_cat = [p for p in all_pages if p["cat"] == page["cat"] and p["slug"] != page["slug"]]
    rel = spread_pick(same_cat, page["slug"], 9)
    url = f'https://bouyonmusique.com/{page["slug"]}'
    sections = ""
    for h2, paras in linkify_sections(page, all_pages, EXTRA_TERMS_FR, "/"):
        sections += f'\n<h2>{esc(h2)}</h2>\n'
        for para in paras:
            sections += f"<p>{para}</p>\n"
    faq_list = page.get("faq") or CAT_FAQ.get(page["cat"], [])
    faq_html = ""
    ld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "@id": url + "#page",
        "url": url,
        "name": page["title"],
        "description": page["desc"],
        "inLanguage": page.get("lang", "fr"),
        "dateModified": page.get("date_modified") or page.get("date_published") or BUILD_DATE,
        "isPartOf": {"@id": "https://bouyonmusique.com/#site"},
        "publisher": {"@id": "https://bouyonmusique.com/#org"},
        "author": {"@id": "https://bouyonmusique.com/#smokiller"},
    }
    if page.get("date_published"):
        ld["datePublished"] = page["date_published"]
    cited = MENTIONS.get(page["slug"], [])
    if cited:
        ld["mentions"] = [{"@id": ARTIST_BY_SLUG[s]["id"]} for s in cited]
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
        faq_html = '\n<h2>Questions fréquentes</h2>\n'
        for q, a in faq_list:
            faq_html += f"<details><summary>{esc(q)}</summary><p>{a}</p></details>\n"
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": faq_text(a)}}
                for q, a in faq_list
            ],
        })
    for _e in page.get("extra_graph", []):
        _e = dict(_e)
        if _e.get("@type") in ("ProfilePage", "Article") and page.get("date_published"):
            _e.setdefault("datePublished", page["date_published"])
        if _e.get("@type") == "ProfilePage" and isinstance(_e.get("mainEntity"), dict):
            _e["mainEntity"] = hubs.as_music_group(_e["mainEntity"])
        graph.append(_e)
    hub, hub_ld = hub_html(page)
    if hub_ld:
        graph.append(hub_ld)
    date_html = ""
    if page.get("date_published"):
        date_html = "\n" + byline(page)
    rel_html = ""
    if rel:
        rel_html = '\n<h2>À lire aussi</h2>\n<div class="grid">\n'
        for p in rel:
            rel_html += f'  <div class="card"><h3>{esc(p["nav"])}</h3><p>{esc(p["desc"][:150])}...</p><p><a href="/{p["slug"]}">Lire la page</a></p></div>\n'
        rel_html += "</div>\n"
    strip_html = ""
    _is_hub = page["slug"].startswith("artistes-")
    _n = 60 if _is_hub else 24
    _pool = [p for p in same_cat if p not in rel]
    if len(_pool) < _n:
        _have = {p["slug"] for p in _pool} | {p["slug"] for p in rel} | {page["slug"]}
        _pool += [p for p in all_pages if p["slug"] not in _have]
    _strip = spread_pick(_pool, page["slug"] + "|strip", _n)
    if _is_hub and _strip:
        graph.append({"@type": "ItemList", "name": page["nav"], "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": p["nav"], "url": "https://bouyonmusique.com/" + p["slug"]} for i, p in enumerate(_strip)]})
    if _strip:
        _t = "Plus d'artistes bouyon" if page["cat"] == "Artistes bouyon" else "Explorer cette rubrique"
        _links = " \u00b7 ".join(f'<a href="/{p["slug"]}">{esc(p["nav"])}</a>' for p in _strip)
        strip_html = f'\n<h2>{_t}</h2>\n<p class="strip">{_links}</p>\n'
    cta = """
<div class="facts">
<h3 style="margin-top:0">Écouter le bouyon maintenant</h3>
<p>La Bouyon Road Mix de Bouyon Shattaz rassemble les nouveautés bouyon et les classiques du carnaval sur Spotify et YouTube.</p>
<p><a href="/playlist-bouyon.html">Ouvrir la playlist bouyon</a> - Suivre <a href="https://www.instagram.com/bouyonshattaz/">@bouyonshattaz</a> et commenter ROAD MIX pour la recevoir en DM.</p>
</div>
"""
    embed_html = playlist_embeds_html(page["slug"])
    embed_html += listen_sources_html(page["slug"], "fr")
    hreflang_en = ""
    if page["slug"] in FR2EN:
        hreflang_en = f'<link rel="alternate" hreflang="en" href="https://bouyonmusique.com/en/{FR2EN[page["slug"]]}">\n'
    return f"""<!DOCTYPE html>
<html lang="{page.get('lang','fr')}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(page["title"])}</title>
<meta name="description" content="{esc(page["desc"])}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="fr" href="{url}">
{hreflang_en}<link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Bouyon Musique">
<meta property="og:title" content="{esc(page["title"])}">
<meta property="og:description" content="{esc(page["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="fr_FR">
<meta property="og:image" content="https://bouyonmusique.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Bouyon Musique, le guide de la musique bouyon">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)}
</script>
</head>
<body>
{header(page["cat"])}
<main>
<div class="wrap">
<p class="breadcrumb"><a href="/">Accueil</a> / {esc(page["cat"])} / {esc(page["nav"])}</p>
<h1>{esc(page["h1"])}</h1>{date_html}
<p class="lead">{page["intro"]}</p>
{sections}{hub}
{cta}
{embed_html}{faq_html}{cited_html(cited)}
{rel_html}
{strip_html}
</div>
</main>
{footer(page, same_cat)}
</body>
</html>
"""

def previous_lastmods():
    """loc -> lastmod from the sitemaps currently on disk (single file or index)."""
    out = {}
    for name in sorted(os.listdir(SITE)):
        if name.startswith("sitemap") and name.endswith(".xml"):
            text = open(os.path.join(SITE, name), encoding="utf-8").read()
            for loc, mod in re.findall(r"<url>\s*<loc>https://bouyonmusique\.com([^<]*)</loc>\s*<lastmod>([^<]+)</lastmod>", text):
                out[loc] = mod
    return out

def video_xml(e):
    x = lambda t: html.escape(t, quote=False)
    return f"""    <video:video>
      <video:thumbnail_loc>https://bouyonmusique.com/mixtapes/img/{e["video_id"]}.jpg</video:thumbnail_loc>
      <video:title>{x(e["youtube_title"])}</video:title>
      <video:description>{x(faq_text(e["intro"]))}</video:description>
      <video:player_loc>https://www.youtube.com/embed/{e["video_id"]}</video:player_loc>
      <video:duration>{e["duration"]}</video:duration>
      <video:publication_date>{e["upload_date"]}</video:publication_date>
    </video:video>
"""

def write_editorial():
    ctx = {
        "esc": esc, "plain": faq_text, "fmt_date": fmt_date_fr, "header": header(""), "byline": byline,
        "cited": cited_html, "pages": PAGE_BY_SLUG, "artists": ARTIST_BY_SLUG, "site_entities": SITE_ENTITIES,
        "channel": SMOKILLER_CHANNEL, "footer": lambda page, same: footer(page, same),
    }
    for kind, k in editorial.KINDS.items():
        rows = [e for e in EDITORIAL if e["kind"] == kind]
        if not rows:
            continue
        os.makedirs(os.path.join(SITE, k["dir"]), exist_ok=True)
        for e in rows:
            with open(os.path.join(SITE, e["slug"]), "w", encoding="utf-8") as f:
                f.write(editorial.render(e, rows, ctx))
        with open(os.path.join(SITE, k["dir"], "index.html"), "w", encoding="utf-8") as f:
            f.write(editorial.render_index(kind, rows, ctx))

def main():
    for page in PAGES:
        out = os.path.join(SITE, page["slug"])
        with open(out, "w", encoding="utf-8") as f:
            f.write(render(page, PAGES))
    # plan du site
    cats = {}
    for p in PAGES:
        cats.setdefault(p["cat"], []).append(p)
    body = ""
    for cat, ps in cats.items():
        body += f'\n<h2>{esc(cat)}</h2>\n<ul>\n'
        for p in ps:
            body += f'<li><a href="/{p["slug"]}">{esc(p["nav"])}</a> : {esc(p["desc"])}</li>\n'
        body += "</ul>\n"
    core_links = "\n".join(f'<li><a href="{u}">{esc(n)}</a></li>' for u, n in CORE)
    plan = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Plan du site Bouyon Musique : tous les sujets bouyon</title>
<meta name="description" content="Toutes les pages de BouyonMusique.com : histoire du bouyon, styles, artistes, producteurs, playlists, carnaval de la Dominique et scènes bouyon par pays.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://bouyonmusique.com/plan-du-site.html">
<link rel="alternate" hreflang="fr" href="https://bouyonmusique.com/plan-du-site.html">
<link rel="alternate" hreflang="en" href="https://bouyonmusique.com/en/site-map.html">
<link rel="alternate" hreflang="x-default" href="https://bouyonmusique.com/plan-du-site.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Bouyon Musique">
<meta property="og:title" content="Plan du site Bouyon Musique : tous les sujets bouyon">
<meta property="og:description" content="Toutes les pages de BouyonMusique.com : histoire du bouyon, styles, artistes, producteurs, playlists, carnaval de la Dominique et scènes bouyon par pays.">
<meta property="og:url" content="https://bouyonmusique.com/plan-du-site.html">
<meta property="og:locale" content="fr_FR">
<meta property="og:image" content="https://bouyonmusique.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Bouyon Musique, le guide de la musique bouyon">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://bouyonmusique.com/"}}, {{"@type": "ListItem", "position": 2, "name": "Plan du site", "item": "https://bouyonmusique.com/plan-du-site.html"}}]}}
</script>
</head>
<body>
{header("")}
<main><div class="wrap">
<p class="breadcrumb"><a href="/">Accueil</a> / Plan du site</p>
<h1>Tous les sujets bouyon du site</h1>
<p class="lead">BouyonMusique.com couvre la musique bouyon sous tous ses angles : ses styles, ses lieux, ses artistes, ses producteurs et ses événements.</p>
<h2>Pages principales</h2>
<ul>
{core_links}
</ul>
{body}
</div></main>
<footer><div class="wrap"><p>© 2026 Bouyon Shattaz. Le bouyon est né en Dominique. Citations bienvenues avec un lien vers la page source. <a href="/">Retour à l’accueil</a></p></div></footer>
</body>
</html>
"""
    with open(os.path.join(SITE, "plan-du-site.html"), "w", encoding="utf-8") as f:
        f.write(plan)
    write_editorial()
    # Sitemaps (BOU-3200): sitemap.xml is an index of one sitemap per page type.
    urls = [u for u, _ in CORE] + [f'/{p["slug"]}' for p in PAGES] + ["/plan-du-site.html"] + ["/en/history.html", "/en/artists.html", "/en/playlist-bouyon.html", "/en/bouyon-dance.html", "/en/faq.html", "/en/site-map.html"] + [f'/en/{s}' for s in FR2EN.values()]
    for kind in editorial.KINDS:
        rows = [e for e in EDITORIAL if e["kind"] == kind]
        if rows:
            urls += ["/" + editorial.KINDS[kind]["dir"]] + [f'/{e["slug"]}' for e in rows]
    seen, ordered = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u); ordered.append(u)
    # Hand-built pages have no date in the data: keep the lastmod already published.
    lastmod = previous_lastmods()
    for p in PAGES + EDITORIAL:
        lastmod[f'/{p["slug"]}'] = p.get("date_modified") or p.get("date_published", BUILD_DATE)
    for _slug_en, _d in ENDATES.items():
        lastmod[f"/en/{_slug_en}"] = _d
    for kind, k in editorial.KINDS.items():
        rows = [e for e in EDITORIAL if e["kind"] == kind]
        if rows:
            lastmod["/" + k["dir"]] = max(e.get("date_modified") or e["date_published"] for e in rows)
    artist_urls = {"/artistes.html"} | {f'/{p["slug"]}' for p in PAGES if p["cat"] == "Artistes bouyon"}
    videos = {f'/{e["slug"]}': e for e in EDITORIAL if e.get("video_id") and e["kind"] == "mixtape"}
    def kind_of(u):
        if u.startswith("/en/"):
            return "en"
        if u in artist_urls:
            return "artistes"
        for kind, k in editorial.KINDS.items():
            if u.startswith("/" + k["dir"]):
                return k["dir"].strip("/")
        return "pages"
    groups = {}
    for u in ordered:
        groups.setdefault(kind_of(u), []).append(u)
    index = ""
    for name, us in groups.items():
        items = ""
        for u in us:
            pr = "1.0" if u == "/" else ("0.9" if u in [c for c, _ in CORE] else "0.8")
            items += f"""  <url>
    <loc>https://bouyonmusique.com{u}</loc>
    <lastmod>{lastmod.get(u, BUILD_DATE)}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{pr}</priority>
{video_xml(videos[u]) if u in videos else ""}  </url>
"""
        ns = ' xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"' if any(u in videos for u in us) else ""
        with open(os.path.join(SITE, f"sitemap-{name}.xml"), "w", encoding="utf-8") as f:
            f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"{ns}>
{items}</urlset>
""")
        index += f"""  <sitemap>
    <loc>https://bouyonmusique.com/sitemap-{name}.xml</loc>
    <lastmod>{max(lastmod.get(u, BUILD_DATE) for u in us)}</lastmod>
  </sitemap>
"""
    with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{index}</sitemapindex>
""")
    print("Sitemaps: " + ", ".join(f"{n} {len(us)}" for n, us in groups.items()))
    print(f"Wrote {len(PAGES)} generated pages, {len(EDITORIAL)} mixtapes and chroniques, plan-du-site, sitemap index with {len(ordered)} URLs")

if __name__ == "__main__":
    main()
    from music_discovery import apply_music_discovery
    apply_music_discovery(SITE)
