# -*- coding: utf-8 -*-
"""A to Z term list and DefinedTermSet for the bouyon glossary pages (FR glossaire-du-bouyon.html, EN bouyon-glossary.html)."""
import html, re, unicodedata
import glossary_terms

SLUGS = {"glossaire-du-bouyon.html": "fr", "bouyon-glossary.html": "en"}
L = {"fr": {"h2": "Le glossaire du bouyon de A à Z", "more": "En savoir plus", "nav": "Aller à la lettre"},
     "en": {"h2": "The bouyon glossary from A to Z", "more": "Read more", "nav": "Jump to letter"}}


def _e(s):
    return html.escape(s or "", quote=True)


def _letter(t):
    c = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()[:1].upper()
    return c if c.isalpha() else "#"


def _terms(lang):
    k = "en" if lang == "en" else "fr"
    return sorted(glossary_terms.TERMS, key=lambda t: unicodedata.normalize("NFKD", t[k]).encode("ascii", "ignore").decode().lower())


def glossary_html(page, lang):
    if SLUGS.get(page.get("slug")) != lang:
        return ""
    t = L[lang]; k = "en" if lang == "en" else "fr"; d = "def_en" if lang == "en" else "def_fr"; ln = "link_en" if lang == "en" else "link_fr"
    terms = _terms(lang)
    letters = []
    for x in terms:
        if _letter(x[k]) not in letters:
            letters.append(_letter(x[k]))
    out = f'\n<h2 id="a-z">{t["h2"]}</h2>\n<p class="az-hubs"><strong>{t["nav"]}</strong>{" :" if lang == "fr" else ":"} ' + " · ".join(f'<a href="#g-{c.lower()}">{c}</a>' for c in letters) + "</p>\n<dl class=\"glossary\">\n"
    cur = None
    for x in terms:
        c = _letter(x[k])
        anchor = f' id="g-{c.lower()}"' if c != cur else ""
        cur = c
        out += f'<dt id="{_e(x["key"])}"><span{anchor}></span>{_e(x[k])}</dt>\n<dd>{_e(x[d])} <a href="{_e(x[ln])}">{t["more"]}</a></dd>\n'
    return out + "</dl>\n"


def glossary_ld(page, url, lang):
    if SLUGS.get(page.get("slug")) != lang:
        return None
    k = "en" if lang == "en" else "fr"; d = "def_en" if lang == "en" else "def_fr"
    return {"@type": "DefinedTermSet", "@id": url + "#glossary", "name": page.get("nav", ""), "inLanguage": lang,
            "hasDefinedTerm": [{"@type": "DefinedTerm", "@id": url + "#" + x["key"], "name": x[k], "description": x[d],
                                "inDefinedTermSet": url + "#glossary", "url": url + "#" + x["key"]} for x in _terms(lang)]}
