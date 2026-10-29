# -*- coding: utf-8 -*-
# Bouyon riddims list (bouyonmusique.com, 2026-10-28): hub of the riddim pages built from parity_parts/r01_*-riddim.py.
# Every fact below repeats a fact sourced on the riddim page it links to; see the header comment of each riddim file.
import glob, importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

_META = {
 "link-up-riddim.html": ("Wetty Beatz (Wetty-Beatz Productionz)", "2026-05-25"),
 "okra-slime-riddim.html": ("10Star Records", "2026-03-24"),
 "cut-eye-riddim.html": ("Drummixx Productions", "2025-10-10"),
 "kryptic-riddim.html": ("Krishna 'Dada' Lawrence (Dadamanufakture)", "2025-07-06"),
 "whale-oil-riddim.html": ("Suhrawh (Boss Raw Records)", "2025-04-13"),
 "pelau-riddim.html": ("Boogy Rankss", "2023-03-20"),
 "champion-riddim.html": ("R.B.M Productions (Nature Island Records)", "2019-02-14"),
}


def _rows():
    rows = []
    for p in sorted(glob.glob(os.path.join(_HERE, "r01_*-riddim.py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(p)[:-3], p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        slug = m.FR["slug"]
        hf, he = m.FR.get("hub_meta", {}), m.EN.get("hub_meta", {})
        prod, date = _META.get(slug) or (hf.get("producer", ""), hf.get("date", ""))
        prod_en = _META.get(slug, (he.get("producer") or prod,))[0]
        rows.append({"slug": slug, "name": m.FR["nav"], "producer": prod, "producer_en": prod_en, "date": date, "count": len(m.FR["tracklist"])})
    return sorted(rows, key=lambda r: r["date"], reverse=True)


_ROWS = _rows()

FR = {
 "slug": "liste-riddims-bouyon.html",
 "cat": "Riddims bouyon",
 "nav": "Liste des riddims bouyon",
 "title": "Liste des riddims bouyon : producteurs et titres 2019 à 2026",
 "desc": "Les riddims bouyon de 2019 à 2026, du Champion Riddim au Link Up Riddim : producteur, date de sortie et liste des titres vérifiés sur YouTube et Deezer.",
 "h1": "Liste des riddims bouyon",
 "intro": "Cette page rassemble les riddims bouyon que nous avons documentés titre par titre, du Champion Riddim de 2019 au Link Up Riddim de mai 2026. Pour chacun, la page dédiée donne le producteur, la date de sortie et la liste des chansons posées dessus, chaque chanson renvoyant à la page YouTube ou Deezer qui nomme le riddim.",
 "date_published": "2026-10-28",
 "sections": [
  ["Un riddim, plusieurs voix", [
   "En bouyon comme en soca et en dancehall, un riddim est une instrumentale que plusieurs chanteurs reprennent, chacun avec son texte. Le producteur la confie à une poignée de voix, puis publie souvent tout le lot le même jour : les six titres du Pelau Riddim de Boogy Rankss sont arrivés sur sa chaîne YouTube le 20 mars 2023, et ceux du Kryptic Riddim sur la chaîne dadamanufakture le 4 juillet 2025, deux jours avant l'album sur Deezer. Les plus anciens de la liste viennent de Dominique : le Champion Riddim de R.B.M et le DeBouyon Riddim de Cornell Phillip, tous deux sortis en février 2019.",
   "C'est pour cela qu'une chanson bouyon se cherche souvent par son riddim. Notre page <a href=\"/bouyon-riddim.html\">bouyon riddim</a> explique la notion, et <a href=\"/comment-un-riddim-devient-un-titre.html\">comment un riddim devient un titre</a> suit le chemin d'une instrumentale jusqu'à la chanson finie. Ici, la liste sert à retrouver qui a chanté quoi, et sur quelle base."]],
  ["Les riddims de 2025 et 2026", [
   "Le Kryptic Riddim, produit, mixé et masterisé en Dominique par Krishna « Dada » Lawrence, est le plus fourni de la liste avec dix titres vérifiés, dont « Shake Something » de Pudaz et Paris. Le Cut Eye Riddim de Drummixx Productions, sorti le 10 octobre 2025, a été promu en janvier 2026 sous l'étiquette Bouyon 2026, avec Khallion, Ebony Empress et Motto. Le Whale Oil Riddim de Boss Raw Records, produit par Suhrawh, se tient entre bouyon et soca vincentaise.",
   "En 2026, la Barbade et Saint-Vincent prennent le relais. Le Okra Slime Riddim de 10Star Records est billé Barbados Bouyon dès le visualiseur de Sharkie, le 24 mars 2026, et Quan De Artist, Stella Billy et Fiddy ii suivent dans les dix semaines. Le 25 mai 2026, Wetty Beatz publie le Link Up Riddim sur son label, avec Magikal, Problem Child et Nerdy. Entre les deux, le Bouyon Rave Riddim de ProducerDlo et Hossi (janvier 2026), le Backside Riddim de Khaos Entertainment (décembre 2025, billé Bouyon 2026) et le Tequila Riddim de Next Gen Records (avril 2025, billé Bouyon 2025) complètent le tableau."]],
  ["Comment cette liste est vérifiée", [
   "Une chanson n'entre dans la liste d'un riddim que si une page ouverte le dit elle-même : le titre ou la description de la vidéo YouTube, ou l'album Deezer du riddim. Producteur, label et date viennent des mêmes pages ; quand elles ne disent rien, la page du riddim le précise au lieu de deviner.",
   "Un riddim n'a sa page que s'il réunit au moins quatre titres vérifiés et qu'une source primaire le présente comme du bouyon. Plusieurs riddims cités sur nos fiches d'artistes attendent encore cette preuve, par exemple parce que leurs vidéos ne disent que soca ou Dennery Segment. La liste s'allonge à mesure que les sources le confirment."]],
 ],
 "faq": [
  ("Qu'est-ce qu'un riddim bouyon ?", "Une instrumentale bouyon reprise par plusieurs chanteurs, chacun avec sa chanson. Le producteur publie souvent tous les titres le même jour, sur YouTube puis en album sur les plateformes."),
  ("Quel est le riddim bouyon le plus fourni de la liste ?", "Le Kryptic Riddim de Krishna « Dada » Lawrence, avec dix titres vérifiés, dont Shake Something de Pudaz et Paris."),
  ("Quels sont les riddims bouyon de 2026 ?", "Le Okra Slime Riddim de 10Star Records (Barbados Bouyon 2026), le Link Up Riddim de Wetty Beatz (25 mai 2026), le Bouyon Rave Riddim de ProducerDlo (janvier 2026), ainsi que le Cut Eye Riddim de Drummixx Productions et le Backside Riddim de Khaos Entertainment, sortis fin 2025 et billés Bouyon 2026."),
  ("Comment savoir sur quel riddim est une chanson ?", "Cherchez le nom de la chanson dans les listes de titres de nos pages riddim : chaque ligne renvoie à la page YouTube ou Deezer qui nomme le riddim."),
  ("Pourquoi certains riddims connus manquent-ils ?", "Parce qu'une source primaire doit les présenter comme du bouyon et confirmer au moins quatre titres. Ceux qui ne sont billés que soca ou Dennery Segment attendent cette preuve."),
 ],
 "riddim_index": _ROWS,
 "extra_graph": [{"@type": "CollectionPage", "@id": "https://bouyonmusique.com/liste-riddims-bouyon.html#collection", "name": "Liste des riddims bouyon", "hasPart": [{"@type": "WebPage", "url": "https://bouyonmusique.com/" + r["slug"], "name": r["name"]} for r in _ROWS]}],
}

EN = {
 "slug": "bouyon-riddims-list.html",
 "fr_slug": "liste-riddims-bouyon.html",
 "cat": "Bouyon riddims",
 "nav": "Bouyon riddims list",
 "title": "Bouyon riddims list: producers and songs, 2019 to 2026",
 "desc": "Bouyon riddims from 2019 to 2026, from the Champion Riddim to the Link Up Riddim: producer, release date and the songs verified on YouTube and Deezer.",
 "h1": "Bouyon riddims list",
 "intro": "This page gathers the bouyon riddims we have documented song by song, from the 2019 Champion Riddim to the Link Up Riddim of May 2026. Each riddim page gives the producer, the release date and the songs voiced on it, and every song links to the YouTube or Deezer page that names the riddim.",
 "date_published": "2026-10-28",
 "sections": [
  ["One riddim, many voices", [
   "In bouyon, as in soca and dancehall, a riddim is an instrumental that several singers take on, each with their own lyrics. The producer hands it to a handful of voices and often releases the whole batch on one day: the six Pelau Riddim songs went up on Boogy Rankss's YouTube channel on March 20, 2023, and the Kryptic Riddim songs landed on the dadamanufakture channel on July 4, 2025, two days before the album reached Deezer. The oldest on the list come from Dominica: R.B.M's Champion Riddim and Cornell Phillip's DeBouyon Riddim, both released in February 2019.",
   "That is why a bouyon song is so often looked up by its riddim. Our <a href=\"/en/bouyon-riddim.html\">bouyon riddim</a> page explains the idea, and <a href=\"/en/how-a-riddim-becomes-a-song.html\">how a riddim becomes a song</a> follows an instrumental all the way to a finished track. This list is for finding who sang what, and on what evidence."]],
  ["The riddims of 2025 and 2026", [
   "The Kryptic Riddim, produced, mixed and mastered in Dominica by Krishna 'Dada' Lawrence, is the deepest on the list with ten verified songs, including Pudaz and Paris's \"Shake Something\". Drummixx Productions' Cut Eye Riddim came out on October 10, 2025 and was pushed in January 2026 under the Bouyon 2026 tag, with Khallion, Ebony Empress and Motto. Boss Raw Records' Whale Oil Riddim, produced by Suhrawh, sits between bouyon and Vincy soca.",
   "In 2026, Barbados and Saint Vincent took over. 10Star Records' Okra Slime Riddim was billed Barbados Bouyon from Sharkie's visualizer on March 24, 2026, with Quan De Artist, Stella Billy and Fiddy ii following within ten weeks. On May 25, 2026, Wetty Beatz released the Link Up Riddim on his own label, with Magikal, Problem Child and Nerdy. In between, ProducerDlo and Hossi's Bouyon Rave Riddim (January 2026), Khaos Entertainment's Backside Riddim (December 2025, billed Bouyon 2026) and Next Gen Records' Tequila Riddim (April 2025, billed Bouyon 2025) fill in the picture."]],
  ["How this list is checked", [
   "A song joins a riddim's list only when an opened page says so itself: the title or description of the YouTube video, or the riddim's Deezer album. Producer, label and date come from the same pages, and when they say nothing, the riddim page says so instead of guessing.",
   "A riddim gets its own page only with at least four verified songs and a primary source that presents it as bouyon. Several riddims named on our artist profiles are still waiting for that proof, for instance because their videos only say soca or Dennery Segment. The list grows as sources confirm them."]],
 ],
 "faq": [
  ("What is a bouyon riddim?", "A bouyon instrumental taken on by several singers, each with their own song. Producers often release every song on the same day, on YouTube first and then as an album on streaming platforms."),
  ("Which bouyon riddim on the list has the most songs?", "The Kryptic Riddim by Krishna 'Dada' Lawrence, with ten verified songs, including Shake Something by Pudaz and Paris."),
  ("What are the 2026 bouyon riddims?", "10Star Records' Okra Slime Riddim (Barbados Bouyon 2026), Wetty Beatz's Link Up Riddim (May 25, 2026), ProducerDlo's Bouyon Rave Riddim (January 2026), plus Drummixx Productions' Cut Eye Riddim and Khaos Entertainment's Backside Riddim, released late 2025 and billed Bouyon 2026."),
  ("How do I find which riddim a song is on?", "Look the song up in the tracklists on our riddim pages: every row links to the YouTube or Deezer page that names the riddim."),
  ("Why are some well-known riddims missing?", "Because a primary source has to present them as bouyon and confirm at least four songs. Riddims billed only as soca or Dennery Segment are waiting for that proof."),
 ],
 "riddim_index": [dict(r, producer=r["producer_en"]) for r in _ROWS],
 "extra_graph": [{"@type": "CollectionPage", "@id": "https://bouyonmusique.com/en/bouyon-riddims-list.html#collection", "name": "Bouyon riddims list", "hasPart": [{"@type": "WebPage", "url": "https://bouyonmusique.com/en/" + r["slug"], "name": r["name"]} for r in _ROWS]}],
}
