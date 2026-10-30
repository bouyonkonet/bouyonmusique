"""Artist hubs (BOU-3200): every artist profile lists every page that mentions
the artist, and every page lists the artists it mentions.

A mention is either a hand-written link to the profile in the page copy, or the
artist's name in the copy. Name matches are guarded so that "Life Nice",
"Serbin Freddy" or "Trixx Migos" do not count as Nice, Freddy or Trixx: a name
directly next to another capitalised word is skipped. Names that are also
common words, places or another person's name only count through a
hand-written link (LINK_ONLY). The same guard keeps linkify_sections in both
generators from auto-linking those false matches.
"""
import html
import re
import unicodedata

# Stage names that collide with words, places or other people. Mentions of
# these artists only count through a hand-written link in the copy.
LINK_ONLY = {"Nice", "Alpha", "Chief", "Sticky", "Freddy", "Hussey", "Kenny G", "Le Det", "Vador", "C4", "Quan", "Candy", "Motto", "Go Fast", "Que", "Kilogram", "Zone Rouge", "Starrin", "Redz", "Zi", "Halibut", "Daly", "Wawa"}

# Capitalised words that may sit next to a name without being part of it.
FUNCTION_WORDS = {
    "le", "la", "les", "l", "un", "une", "des", "du", "de", "d", "et", "ou", "avec", "pour", "par", "chez", "sur", "dans",
    "selon", "comme", "mais", "puis", "quand", "où", "si", "après", "avant", "entre", "depuis", "en", "à", "au", "aux",
    "ce", "cet", "cette", "son", "sa", "ses", "leur", "notre", "nos", "voir", "lire", "écouter", "c", "ici", "côté",
    "of", "the", "with", "and", "by", "for", "from", "in", "on", "at", "to", "a", "an", "his", "her", "their", "our",
    "see", "read", "listen", "feat", "ft", "featuring", "x", "vs", "aka", "dit", "dite", "alias", "mr", "dj",
}

_WORD = r"[^\W\d_][\w’'\-]*"
_PREV = re.compile("(" + _WORD + r")[  ]+$")
_NEXT = re.compile(r"^[  ]+(" + _WORD + ")")


def fold(s):
    """Accent-fold one character at a time, so offsets match the original."""
    return "".join(unicodedata.normalize("NFD", ch)[0] for ch in s)


def _capitalised_neighbour(word):
    return word[0].isupper() and word.lower().strip("’'") not in FUNCTION_WORDS


def term_ok(text, start, end):
    """False when the match is glued to another capitalised word (Life Nice, Trixx Migos)."""
    prev = _PREV.search(text[max(0, start - 40):start])
    if prev and _capitalised_neighbour(prev.group(1)):
        return False
    nxt = _NEXT.search(text[end:end + 40])
    if nxt and _capitalised_neighbour(nxt.group(1)):
        return False
    return True


def term_pattern(term):
    return re.compile(r"(?<![\w\-])" + re.escape(term) + r"(?![\w\-])")


def first_match(pat, text):
    """First guarded match of a compiled term pattern in plain text, or None."""
    for m in pat.finditer(text):
        if term_ok(text, m.start(), m.end()):
            return m
    return None


def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", " ", s))


def page_copy(page):
    parts = [page["intro"]]
    for h2, paras in page["sections"]:
        parts.append(h2)
        parts.extend(paras)
    for qa in page.get("faq") or []:
        parts.extend(qa)
    return "\n".join(parts)


def artists(pages):
    """Artist profiles: pages whose extra_graph has a ProfilePage."""
    out = []
    for p in pages:
        for e in p.get("extra_graph", []):
            me = e.get("mainEntity") if isinstance(e, dict) else None
            if e.get("@type") == "ProfilePage" and isinstance(me, dict):
                names = {p["nav"], me["name"]}
                alt = me.get("alternateName")
                names |= {alt} if isinstance(alt, str) else set(alt or [])
                names = {n for n in names if n and len(n) >= 2 and "(" not in n}
                out.append({
                    "slug": p["slug"], "nav": p["nav"], "id": me.get("@id") or ("#" + p["slug"]),
                    "link_only": bool(names & LINK_ONLY), "names": sorted(names, key=len, reverse=True),
                })
                break
    return out


def mentions(pages, arts, prefix, extra=None):
    """{page slug: [artist slug, ...]} in order of first mention. extra maps a
    page slug to artist slugs known from structured data (mixtape tracklists)."""
    names = []
    for a in arts:
        if a["link_only"]:
            continue
        for n in a["names"]:
            for variant in {n, n.upper()}:
                names.append((fold(variant), a["slug"]))
    names.sort(key=lambda t: -len(t[0]))
    by_name = {}
    for n, s in names:
        by_name.setdefault(n, s)
    # One alternation, longest names first, so "Mr Ridge" wins over "Ridge" and a
    # page is scanned once instead of once per name.
    combined = re.compile(r"(?<![\w\-])(?:" + "|".join(re.escape(n) for n in by_name) + r")(?![\w\-])")
    slugs = {a["slug"] for a in arts}
    out = {}
    for p in pages:
        src = page_copy(p)
        found = {}
        for m in re.finditer(r'href="' + re.escape(prefix) + r'([^"#]+)"', src):
            if m.group(1) in slugs:
                found.setdefault(m.group(1), m.start() / max(len(src), 1))
        text = fold(plain(src))
        for m in combined.finditer(text):
            if term_ok(text, m.start(), m.end()):
                found.setdefault(by_name[m.group(0)], m.start() / max(len(text), 1))
        for slug in (extra or {}).get(p["slug"], []):
            found.setdefault(slug, 1.0)
        found.pop(p["slug"], None)
        out[p["slug"]] = sorted(found, key=found.get)
    return out


def invert(ment):
    back = {}
    for page_slug, art_slugs in ment.items():
        for a in art_slugs:
            back.setdefault(a, []).append(page_slug)
    return back


def as_music_group(entity):
    """schema.org MusicGroup covers solo musicians too. Keep Person for the
    person-only properties (birthPlace, homeLocation) and add MusicGroup."""
    if entity.get("@type") == "Person" and entity.get("genre"):
        entity = dict(entity)
        entity["@type"] = ["Person", "MusicGroup"]
    return entity
