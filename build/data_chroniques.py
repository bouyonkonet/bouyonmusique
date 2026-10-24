"""Chroniques (BOU-3200): reviews of one record, rendered by editorial.py under /chroniques/.

Empty until a chronique is written and passes both fact checks. A chronique is
an opinion, so it needs a named author who listened to the record; the facts
around it (release date, credits, label) still come only from sources listed
in "sources". No rating: the template does not publish one.

Shape of one entry:
{
    "slug": "chroniques/<artiste>-<titre>.html",
    "nav": "<Titre> de <Artiste>",
    "title": "<= 65 caractères", "h1": "...", "desc": "...",
    "date_published": "AAAA-MM-JJ", "date_modified": "AAAA-MM-JJ" (optionnel),
    "item_type": "MusicRecording" ou "MusicAlbum",
    "item_name": "<titre exact>",
    "artists": ["<profil>.html", ...],          # profils de ce site, même artiste que le crédit
    "release_date": "AAAA-MM-JJ" ou None,        # seulement si une source le donne
    "video_id": "<id YouTube>" ou None,          # upload officiel de l'artiste ou du label, ou chaîne Smokiller
    "intro": "...", "sections": [(h2, [paragraphes])],
    "sources": [(libellé, url), ...],
    "related": ["<page>.html", ...],
}
"""

CHRONIQUES = []
