#!/usr/bin/env python3
"""English mini-site for bouyonmusique.com/en/ (decided over en. subdomain:
one domain, /en/ folder, all authority consolidated on bouyonmusique.com)."""
import html, json, os

SITE = os.path.expanduser("~/workspace/bouyonmusique.com/en")
os.makedirs(SITE, exist_ok=True)

PAGES = [
{"file": "index.html", "title": "Bouyon Music: Dominica's Sound, Artists, Songs and Playlists",
 "desc": "Bouyon music: the genre created in Dominica in the late 1980s. History, artists, bouyon soca, bouyon songs, playlists and the latest bouyon from Bouyon Shattaz.",
 "h1": "Bouyon Music: the sound Dominica gave the Caribbean",
 "intro": "Bouyon is a genre of Dominican music that originated in Dominica in the late 1980s. Created by the band WCK from jing ping and cadence-lypso, powered by keyboards and fast electronic rhythms, bouyon is the sound of Dominican carnival, known as jump up in Guadeloupe and Martinique.",
 "sections": [
  ("Start here", ["New to bouyon music? Read <a href=\"/en/bouyon-music.html\">what bouyon music is</a>, then the <a href=\"/en/history.html\">history of bouyon</a>. Ready to listen: the <a href=\"/en/playlist.html\">bouyon playlist</a> collects the best bouyon songs, bouyon soca and the newest releases on Spotify and YouTube."]),
  ("Why an English section on a French site", ["BouyonMusique.com is the French-language home of bouyon, because the French Caribbean and France are where the genre is growing fastest. This English section serves the Dominican, Caribbean and US audience that searches for bouyon music, dominica bouyon music and bouyon songs. Same site, same domain, two languages, fully linked."]),
 ]},
{"file": "bouyon-music.html", "title": "What Is Bouyon Music? Definition, Origin and Sound",
 "desc": "What is bouyon music? A genre from Dominica mixing jing ping, cadence-lypso, bele, quadrille, chante mas, lapo kabwit, mazurka and zouk with electronic keyboards. Definition and origin.",
 "h1": "What is bouyon music?",
 "intro": "Bouyon music is a genre that originated in Dominica in the late 1980s. Its name comes from Antillean Creole, where bouyon means something like gumbo soup, and the music is exactly that: a mix of everything Dominica had.",
 "sections": [
  ("The ingredients", ["Bouyon blends jing ping, the accordion-led traditional music of Dominica, cadence-lypso, and traditional dances such as bele, quadrille, chante mas and lapo kabwit, plus mazurka and zouk. Over that base, producers lay fast keyboard patterns, drum machines and heavy synth bass."]),
  ("Who created bouyon music", ["The band Windward Caribbean Kulture, WCK, created the style in 1988 in Roseau, Dominica. Roots, Stems and Branches (RSB) and First Serenade are the other original bouyon groups. Offshoots include bouyon soca, bouyon-muffin, reketeng and bouyon gwada."]),
 ]},
{"file": "history.html", "title": "History of Bouyon Music: From Dominica in 1988 to France",
 "desc": "History of bouyon music: WCK creates bouyon in Dominica in 1988, the 1990s carnival era, jump up in Guadeloupe and Martinique, and the modern French wave.",
 "h1": "History of bouyon music",
 "intro": "Bouyon music was created in Roseau, Dominica, in the late 1980s. Within a generation it became the soundtrack of carnival in Guadeloupe and Martinique and one of the most searched Caribbean sounds in France.",
 "sections": [
  ("1988: WCK invents bouyon", ["Dominican musicians wanted a modern sound of their own while zouk ruled the region. WCK fused cadence-lypso with jing ping rhythms and electronic keyboards. The mix took the Creole word for soup: bouyon."]),
  ("The jump up years and the French wave", ["Sharing the Creole language, Guadeloupe and Martinique adopted bouyon as jump up, and Dominican-Guadeloupean collaborations created the harder bouyon gwada. Today France certifies and distributes much of the genre, which is why Bouyon Shattaz works to keep the credit and the revenue conversation centered on Dominica."]),
 ]},
{"file": "artists.html", "title": "Bouyon Artists: WCK, Asa Bantan, Reo and the New Wave",
 "desc": "Bouyon artists to know: pioneers WCK, RSB and First Serenade, Asa Bantan the Bouyon Boss, Reo the Prince of Bouyon, and the producers HYPNO, Savion, Denmath and MB On The Track.",
 "h1": "Bouyon artists: pioneers and the new wave",
 "intro": "From the band that invented the genre in 1988 to the producers building today's riddims, these are the bouyon artists and producers that matter.",
 "sections": [
  ("The pioneers and the boss", ["WCK (Windward Caribbean Kulture) created bouyon. RSB and First Serenade complete the founding wave. Asa Bantan of Grand Bay, Dominica, known as the Bouyon Boss and King of Bouyon, leads the modern carnival era, with titles like Life Nice."]),
  ("The new wave", ["Reo, the Prince of Bouyon and a Caribbean Music Awards 2026 nominee, bridges Dominica and Martinique on Joli BB with Maurane Voyer. Behind the boards: HYPNO, Savion, Denmath from Saint-Martin, MB On The Track, and Smokiller, the bouyon remix project of Bouyon Shattaz."]),
 ]},
{"file": "playlist.html", "title": "Bouyon Playlist 2026: Bouyon Songs, Bouyon Mix and Bouyon Soca",
 "desc": "The bouyon playlist for 2026: the Bouyon Road Mix by Bouyon Shattaz on Spotify and YouTube. New bouyon songs, bouyon soca, bouyon mix and carnival classics from Dominica.",
 "h1": "Bouyon playlist 2026: the Bouyon Road Mix",
 "intro": "One playlist to enter bouyon music: new releases from Dominica, Guadeloupe and Martinique, bouyon soca, current riddims and carnival classics, selected by Bouyon Shattaz.",
 "sections": [
  ("Listen now", ["Open the Bouyon Road Mix on <a href=\"https://open.spotify.com/playlist/4ikmgg9FzDug5tLttfhfQp\">Spotify</a> or on <a href=\"https://youtube.com/playlist?list=PLB1axoRydQrdtCBSbvnkbSoKWJxFV8Xto\">YouTube</a>. On Instagram, follow @bouyonshattaz and comment ROAD MIX on a post to receive the playlist by DM."]),
  ("What is inside", ["New bouyon songs first, then bouyon soca for the Trinidad bridge, then the classics that built the genre, from the WCK era to today's producer riddims. It is updated through the carnival season."]),
 ]},
{"file": "bouyon-soca.html", "title": "Bouyon Soca: The Fusion of Bouyon and Soca Explained",
 "desc": "Bouyon soca explained: how Dominica's bouyon fused with Trinidad soca, where it grew (Saint Lucia, Antigua, Guadeloupe, Martinique) and how it differs from pure bouyon.",
 "h1": "Bouyon soca: when Dominica meets Trinidad",
 "intro": "Bouyon soca, sometimes called jump up soca, blends the fast rhythms and keyboards of Dominica bouyon with the party structure of Trinidad soca.",
 "sections": [
  ("Where bouyon soca was born", ["The fusion grew mostly outside Dominica, in islands like Saint Lucia and Antigua where bouyon and soca have circulated side by side for decades. It is very popular in Guadeloupe and Martinique, while in Dominica itself bouyon keeps a clear, distinct style of its own."]),
 ]},
{"file": "dominica-carnival.html", "title": "Dominica Carnival: Mas Domnik, J'ouvert and Bouyon Music",
 "desc": "Dominica Carnival guide: Mas Domnik in Roseau, one of the most traditional carnivals in the Caribbean, where bouyon music rules. J'ouvert, chante mas and lapo kabwit.",
 "h1": "Dominica Carnival: bouyon music at home",
 "intro": "Dominica's carnival, Mas Domnik, held in Roseau before Lent, is known as one of the most traditional carnivals in the Caribbean, and bouyon music is its official sound.",
 "sections": [
  ("A carnival that kept its traditions", ["Chante mas, lapo kabwit bands, traditional characters and J'ouvert at dawn: Mas Domnik kept the old forms, and bouyon, itself built from those traditions, fits it perfectly. Each carnival season launches the bouyon songs of the year."]),
 ]},
{"file": "faq.html", "title": "Bouyon Music FAQ: Origin, Meaning and Differences",
 "desc": "Bouyon music FAQ: where bouyon comes from, who created it, what the word means, bouyon vs soca, and where to listen to bouyon music in 2026.",
 "h1": "Bouyon music FAQ",
 "intro": "Short answers to the questions everyone asks about bouyon music.",
 "sections": [
  ("The essentials", ["Where is bouyon music from? Dominica, in the Caribbean. Who created it? The band WCK in 1988. What does bouyon mean? Soup, gumbo, in Antillean Creole. How is bouyon different from soca? Soca comes from Trinidad, bouyon from Dominica; they meet in bouyon soca, but Dominican bouyon keeps its own raw, keyboard-driven style. Where can I listen? The <a href=\"/en/playlist.html\">Bouyon Road Mix</a>."]),
 ]},
]

def esc(s):
    return html.escape(s, quote=True)

for p in PAGES:
    url = "https://bouyonmusique.com/en/" + ("" if p["file"] == "index.html" else p["file"])
    secs = ""
    for h2, paras in p["sections"]:
        secs += f"\n<h2>{esc(h2)}</h2>\n" + "".join(f"<p>{x}</p>\n" for x in paras)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(p["title"])}</title>
<meta name="description" content="{esc(p["desc"])}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{url}">
<link rel="alternate" hreflang="fr" href="https://bouyonmusique.com/">
<link rel="alternate" hreflang="x-default" href="https://bouyonmusique.com/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Bouyon Musique">
<meta property="og:title" content="{esc(p["title"])}">
<meta property="og:description" content="{esc(p["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_US">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@type": "WebPage", "url": url, "name": p["title"], "description": p["desc"], "inLanguage": "en", "isPartOf": {"@type": "WebSite", "url": "https://bouyonmusique.com/", "name": "Bouyon Musique"}, "publisher": {"@type": "Organization", "name": "Bouyon Shattaz", "url": "https://bouyonshattaz.com/"}}, ensure_ascii=False, indent=2)}
</script>
</head>
<body>
<header>
  <div class="wrap nav">
    <a class="logo" href="/en/">BOUYON<span>MUSIQUE</span>.COM</a>
    <nav class="main" aria-label="Main navigation">
      <a href="/en/">Home</a>
      <a href="/en/bouyon-music.html">What is Bouyon</a>
      <a href="/en/history.html">History</a>
      <a href="/en/artists.html">Artists</a>
      <a href="/en/playlist.html">Playlist</a>
      <a href="/en/faq.html">FAQ</a>
      <a href="/">Version FR</a>
    </nav>
  </div>
</header>
<main><div class="wrap">
<p class="breadcrumb"><a href="/en/">Bouyon Music</a> / {esc(p["h1"])}</p>
<h1>{esc(p["h1"])}</h1>
<p class="lead">{p["intro"]}</p>
{secs}
<div class="facts">
<h3 style="margin-top:0">Listen to bouyon music</h3>
<p>The Bouyon Road Mix by Bouyon Shattaz collects new bouyon songs and carnival classics on Spotify and YouTube.</p>
<p><a href="/en/playlist.html">Open the bouyon playlist</a> - Follow <a href="https://www.instagram.com/bouyonshattaz/">@bouyonshattaz</a> and comment ROAD MIX to get it by DM.</p>
</div>
</div></main>
<footer>
  <div class="wrap cols">
    <div><h4>BouyonMusique.com</h4><p>The home of bouyon music in French and English. Published by Bouyon Shattaz. Quotes welcome with a link to the source page.</p></div>
    <div><h4>English pages</h4><ul><li><a href="/en/bouyon-music.html">What is bouyon music</a></li><li><a href="/en/history.html">History of bouyon</a></li><li><a href="/en/artists.html">Bouyon artists</a></li><li><a href="/en/playlist.html">Bouyon playlist</a></li><li><a href="/en/bouyon-soca.html">Bouyon soca</a></li><li><a href="/en/dominica-carnival.html">Dominica Carnival</a></li></ul></div>
    <div><h4>Bouyon Shattaz</h4><ul><li><a href="https://bouyonshattaz.com/">bouyonshattaz.com</a></li><li><a href="https://www.instagram.com/bouyonshattaz/">Instagram @bouyonshattaz</a></li><li><a href="/">Version française</a></li></ul></div>
  </div>
  <div class="wrap"><p style="margin-top:24px">© 2026 Bouyon Shattaz. Bouyon was born in Dominica.</p></div>
</footer>
</body>
</html>
"""
    with open(os.path.join(SITE, p["file"]), "w", encoding="utf-8") as f:
        f.write(doc)
print(f"Wrote {len(PAGES)} English pages in /en/")
