# -*- coding: utf-8 -*-
"""Tracklist table and ItemList structured data for riddim pages (page key "tracklist")."""
import html, os
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

L = {"fr": {"h2": "Titres sur ce riddim", "artist": "Artiste", "title": "Titre", "date": "Date", "src": "Source", "yt": "YouTube", "dz": "Deezer", "other": "Page"},
     "en": {"h2": "Songs on this riddim", "artist": "Artist", "title": "Title", "date": "Date", "src": "Source", "yt": "YouTube", "dz": "Deezer", "other": "Page"}}


def _e(s):
    return html.escape(s or "", quote=True)


def _kind(u, t):
    return t["yt"] if "youtu" in u else (t["dz"] if "deezer" in u else t["other"])


def tracklist_html(page, lang, prefix):
    rows = page.get("tracklist") or []
    if not rows:
        return ""
    t = L[lang]
    out = f'\n<h2>{t["h2"]}</h2>\n<div class="table-wrap"><table class="tracklist">\n<thead><tr><th>{t["artist"]}</th><th>{t["title"]}</th><th>{t["date"]}</th><th>{t["src"]}</th></tr></thead>\n<tbody>\n'
    for r in rows:
        a = _e(r["artist"])
        if r.get("artist_slug") and os.path.exists(os.path.join(_ROOT, prefix.strip("/"), r["artist_slug"])):
            a = f'<a href="{prefix}{r["artist_slug"]}">{a}</a>'
        out += f'<tr><td>{a}</td><td>{_e(r["title"])}</td><td>{_e(r.get("date", ""))}</td><td><a href="{_e(r["source"])}" rel="nofollow noopener" target="_blank">{_kind(r["source"], t)}</a></td></tr>\n'
    return out + "</tbody></table></div>\n"


def tracklist_ld(page, url):
    rows = page.get("tracklist") or []
    if not rows:
        return None
    return {"@type": "ItemList", "@id": url + "#tracklist", "name": page.get("nav", ""), "numberOfItems": len(rows),
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@type": "MusicRecording", "name": r["title"],
                                 "byArtist": {"@type": "MusicGroup", "name": r["artist"]}, "url": r["source"]}} for i, r in enumerate(rows)]}


IDX = {"fr": {"h2": "Les riddims bouyon de cette liste", "r": "Riddim", "p": "Producteur ou label", "d": "Sortie", "n": "Titres vérifiés"},
       "en": {"h2": "The bouyon riddims on this list", "r": "Riddim", "p": "Producer or label", "d": "Release", "n": "Verified songs"}}


def riddim_index_html(page, lang, prefix):
    rows = page.get("riddim_index") or []
    if not rows:
        return ""
    t = IDX[lang]
    out = f'\n<h2>{t["h2"]}</h2>\n<div class="table-wrap"><table class="tracklist">\n<thead><tr><th>{t["r"]}</th><th>{t["p"]}</th><th>{t["d"]}</th><th>{t["n"]}</th></tr></thead>\n<tbody>\n'
    for r in rows:
        out += f'<tr><td><a href="{prefix}{r["slug"]}">{_e(r["name"])}</a></td><td>{_e(r["producer"])}</td><td>{_e(r["date"])}</td><td>{r["count"]}</td></tr>\n'
    return out + "</tbody></table></div>\n"
