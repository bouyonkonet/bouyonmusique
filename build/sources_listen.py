# -*- coding: utf-8 -*-
"""Listen + sources blocks for artist profiles.

Page builds read listen_sources.json (slug -> [[title, url], ...]): only
the title and URL of recordings a researcher opened and checked.

The raw research logs live in the notes repo
(bouyonkonet/bouyonmusique-notes, checked out beside this repo). After
editing them, refresh the JSON with:  python3 build/sources_listen.py --export

Log format: "## Name (slug.html)" headings, then lines
"- Title (album/year) - source: URL".
"""
import glob, html, json, os, re, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_JSON = os.path.join(_HERE, "listen_sources.json")
_RESEARCH = os.path.join(_HERE, "..", "..", "bouyonmusique-notes", "build", "research")
_LOGS = [os.path.join(_RESEARCH, "recordings-sources.md")] + sorted(
    glob.glob(os.path.join(_RESEARCH, "sources-w*.md")))

MAX_EMBEDS = 3
MAX_SOURCES = 15

PLATFORMS = [
    ("youtube.com", "YouTube"), ("youtu.be", "YouTube"), ("deezer.com", "Deezer"),
    ("music.apple.com", "Apple Music"), ("itunes.apple.com", "Apple Music"),
    ("open.spotify.com", "Spotify"), ("discogs.com", "Discogs"), ("qobuz.com", "Qobuz"),
    ("shazam.com", "Shazam"), ("soundcloud.com", "SoundCloud"), ("bandcamp.com", "Bandcamp"),
    ("audiomack.com", "Audiomack"),
]


def _platform(url):
    for dom, name in PLATFORMS:
        if dom in url:
            return name
    m = re.match(r"https?://(?:www\.)?([^/]+)", url)
    return m.group(1) if m else url


def _slugify(text):
    import unicodedata
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def _heading_slug(line):
    """Accepts '## Name (slug.html)', '## Name (slug)', '## Name (slug.py)', '### slug' and '## Name'."""
    text = line.lstrip("#").strip()
    m = re.search(r"\(([a-z0-9-]+)(?:\.html|\.py)?\)\s*(?:,.*)?$", text) or re.search(r"\(([a-z0-9-]+\.html)\)", text)
    if m:
        return m.group(1).replace(".html", "") + ".html"
    if re.fullmatch(r"[a-z0-9-]+", text):
        return text + ".html"
    name = text.split(" (")[0].strip()
    return _slugify(name) + ".html" if name else None


ALIASES = {"ken-zii-bwa.html": "kenzii-bwa.html", "v-ghn.html": "vghn.html", "lk.html": "louse-king.html", "d-yonte.html": "dyonte.html"}


def _load():
    data = {}
    for path in _LOGS:
        if not os.path.exists(path):
            continue
        wave_file = os.path.basename(path).startswith("sources-w")
        slug = None
        for line in open(path, encoding="utf-8"):
            if line.startswith("#"):
                slug = _heading_slug(line) if line.startswith("##") else None
                slug = ALIASES.get(slug, slug)
                if slug:
                    data.setdefault(slug, [])
                continue
            m = re.match(r"^-\s+(.*?)\s+-\s+source:\s+(https?://\S+)", line.strip())
            if slug and m:
                raw = m.group(1)
                if wave_file:
                    title = raw.split(" (")[0].strip() or raw
                else:
                    title = re.sub(r"\s*\((?:album|year|credit)[^)]*\)", "", raw).strip()
                data[slug].append((title, m.group(2).rstrip(".,;")))
    return data


def _read_json():
    with open(_JSON, encoding="utf-8") as fh:
        return {k: [tuple(e) for e in v] for k, v in json.load(fh).items()}


if __name__ == "__main__" and "--export" in sys.argv:
    _data = _load()
    if not _data:
        sys.exit("No research logs found in " + os.path.abspath(_RESEARCH))
    with open(_JSON, "w", encoding="utf-8") as fh:
        json.dump(_data, fh, ensure_ascii=False, indent=0, sort_keys=True)
    print(f"exported {len(_data)} profiles, {sum(len(v) for v in _data.values())} entries -> {_JSON}")
    sys.exit(0)

SOURCES = _read_json() if os.path.exists(_JSON) else {}


# YouTube videos whose owner turned off embedding (oEmbed 401, playableInEmbed false):
# an iframe would show "Video unavailable", so these stay as plain source links.
NO_EMBED = {"Ji5Q52BoLEw"}


def _embed(url):
    """Return (kind, iframe src, height) for platforms with a public embed, else None."""
    m = re.search(r"youtube\.com/watch\?v=([\w-]{11})|youtu\.be/([\w-]{11})", url)
    if m and (m.group(1) or m.group(2)) not in NO_EMBED:
        return ("youtube", f"https://www.youtube-nocookie.com/embed/{m.group(1) or m.group(2)}", None)
    m = re.search(r"deezer\.com/(?:[a-z]{2}/)?(track|album)/(\d+)", url)
    if m:
        kind, did = m.groups()
        return ("deezer", f"https://widget.deezer.com/widget/auto/{kind}/{did}?tracklist={'true' if kind == 'album' else 'false'}",
                300 if kind == "album" else 152)
    m = re.search(r"music\.apple\.com/([a-z]{2})/(album|song)/([^?\s]+)(\?i=\d+)?", url)
    if m:
        cc, kind, path, song = m.groups()
        return ("apple", f"https://embed.music.apple.com/{cc}/{kind}/{path}{song or ''}", 175 if (song or kind == "song") else 450)
    return None


def _iframe(kind, src, height, title):
    t = html.escape(title, quote=True)
    if kind == "youtube":
        return ('<div style="position:relative;padding-top:56.25%;margin:1em 0">'
                f'<iframe src="{src}" title="{t}" loading="lazy" '
                'style="position:absolute;inset:0;width:100%;height:100%;border:0;border-radius:12px" '
                'allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>\n')
    allow = "autoplay *; encrypted-media *; fullscreen *; clipboard-write" if kind == "apple" else "encrypted-media; clipboard-write"
    return (f'<iframe src="{src}" title="{t}" width="100%" height="{height}" loading="lazy" '
            f'style="border:0;border-radius:12px;margin:.5em 0" allow="{allow}"></iframe>\n')


def listen_sources_html(slug, lang="fr"):
    entries = SOURCES.get(slug) or []
    if not entries:
        return ""
    # Embeds: prefer YouTube videos, then Deezer, then Apple Music; one per distinct URL.
    picked, seen = [], set()
    for want in ("youtube", "deezer", "apple"):
        for title, url in entries:
            e = _embed(url)
            if e and e[0] == want and e[1] not in seen and len(picked) < MAX_EMBEDS:
                if want == "youtube" and sum(p[0][0] == "youtube" for p in picked) >= 2:
                    continue
                seen.add(e[1])
                picked.append((e, title))
    # Sources: unique URLs, first title seen for each.
    srcs, useen = [], set()
    for title, url in entries:
        if url not in useen:
            useen.add(url)
            srcs.append((title, url))
    if lang == "en":
        h_listen, h_src = "Listen", "Verified sources"
        note = "Every link below was opened and checked when this profile was written or updated."
    else:
        h_listen, h_src = "Écouter", "Sources vérifiées"
        note = "Chaque lien ci-dessous a été ouvert et vérifié lors de la rédaction ou de la mise à jour de ce profil."
    out = ""
    if picked:
        out += f'\n<h2>{h_listen}</h2>\n' + "".join(_iframe(e[0], e[1], e[2], t) for e, t in picked)
    items = "".join(
        f'<li><a href="{html.escape(u, quote=True)}" rel="noopener" target="_blank">{html.escape(t)}</a> <span class="src-platform">({_platform(u)})</span></li>\n'
        for t, u in srcs[:MAX_SOURCES])
    more = len(srcs) - MAX_SOURCES
    if more > 0:
        items += f'<li>{"+ " + str(more) + (" more verified sources" if lang == "en" else " autres sources vérifiées")}</li>\n'
    out += f'\n<h2>{h_src}</h2>\n<p>{note}</p>\n<ul class="sources">\n{items}</ul>\n'
    return out
