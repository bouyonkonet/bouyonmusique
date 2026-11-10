# -*- coding: utf-8 -*-
"""On-page SEO pass over the built site. Both generators call apply_onpage() last;
it can also be run alone from the repository root:  python3 build/onpage.py

What it does on every page, in French and English, rerun-safe:
  - <title> and og:title follow the pipe format "Keyword | Benefit | Bouyon
    Musique". short_title() shortens ONLY the benefit segment when the total
    runs past 60 characters; the keyword and the brand are never cut. Titles
    that are not in the pipe format pass through unchanged. Meta description
    cut to 190 at a sentence or clause end (160 to 190 reads best).
  - H1s stay exactly as authored (frozen since the 2026-11-10 title rewrite).
  - Per-page image: the first YouTube thumbnail on the page becomes og:image,
    the WebPage primaryImageOfPage and the MusicGroup image.
  - VideoObject structured data for every YouTube facade (up to 3), from yt_meta.json,
    and the same videos in the sitemaps as <video:video> entries.
  - A table of contents (jump links) before the first h2 when the page has 3 or more sections.
  - Skip link to #content, preconnect to i.ytimg.com, the facade click script.
  - Publisher logo (ImageObject) on the Organization node.
  - twitter:title and twitter:description (the page title and description) when the page has none.
  - Outbound listen and follow links carry data-cta (instagram_follow, youtube_link, spotify_link),
    so a cookieless analytics script can count them per page without changing the links.
    The attribute is left out of the content hash: tagging a link does not move a page's dates.
  - Sitemap lastmod, WebPage dateModified and the visible "Updated" date follow the
    content: content_hashes.json remembers a hash of each page's visible text with links and
    contextual link sentences removed (content_digest), and a page whose text changed since the
    last build gets today's date. Link-only and anchor-only edits keep the page's dates.
"""
import datetime, glob, hashlib, html, json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yt
import images
import release

ROOT = os.environ.get("BOUYONMUSIQUE_SITE", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = "https://bouyonmusique.com"
HASHES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content_hashes.json")
TODAY = datetime.date.today().isoformat()
TITLE_MAX, DESC_MAX, H1_MAX = 60, 190, 70
# Publisher logo for the Organization node (Bouyon Shattaz runs the site).
ORG_LOGO = {"@type": "ImageObject", "url": "https://bouyonshattaz.com/icons/icon-512.png", "width": 512, "height": 512}
MONTHS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
TOC_SKIP = {"à lire aussi", "read next", "plus d'artistes bouyon", "more bouyon artists", "explorer cette rubrique",
            "explore this section", "artistes cités dans cette page", "artists mentioned on this page"}
T = {
    "fr": dict(toc="Sommaire", skip="Aller au contenu", updated="Mis à jour le",
               video="{title}, vidéo YouTube ouverte pour la page {page} de Bouyon Musique."),
    "en": dict(toc="On this page", skip="Skip to content", updated="Updated",
               video="{title}, a YouTube video opened for the {page} page on Bouyon Musique."),
}


# Version 2 hashes the visible text only: no markup, no links (adding, moving or re-wording a
# link is not a content change), no contextual link sentences, no byline. A real change to the
# copy still moves the page's dates; so does a newer date_modified in the page data.
HASH_VERSION = 2


def content_digest(main_html):
    t = re.sub(r'<p\b[^>]*(class="pubdate|data-release-dates)[^>]*>.*?</p>', " ", main_html, flags=re.S)
    t = re.sub(r"<!--ctx:[A-Za-z0-9_-]+-->.*?<!--/ctx-->", " ", t, flags=re.S)
    t = re.sub(r"<(script|style)\b.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r"<a\b[^>]*>.*?</a>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", html.unescape(t)).strip()
    return hashlib.sha256(t.encode("utf-8")).hexdigest()[:16]


def set_dates_line(s, pub, mod, lang):
    """One visible dates line per page, equal to the JSON-LD and the sitemap: rewrite it, or add it after the H1."""
    lab = ("Publié le", "Mis à jour le") if lang == "fr" else ("Published", "Updated")
    times = (f'{lab[0]} <time datetime="{pub}">{fmt_date(pub, lang)}</time> · '
             f'{lab[1]} <time datetime="{mod}">{fmt_date(mod, lang)}</time>')
    m = re.search(r'(<p\b[^>]*data-release-dates[^>]*>)(.*?)(</p>)', s, re.S)
    if m:
        inner = m.group(2)
        i = inner.find("<time")
        lead = inner[:i] if i >= 0 else inner
        lead = re.sub(r'(Publié le|Published)\s*$', "", lead.rstrip()) .rstrip()
        lead = (lead + " ") if lead else ""
        return s[:m.start()] + m.group(1) + lead + times + m.group(3) + s[m.end():]
    if "</h1>" in s:
        i = s.index("</h1>") + 5
        return s[:i] + f'\n<p class="pubdate release-dates" data-release-dates>{times}</p>' + s[i:]
    return s


def esc(s):
    return html.escape(s, quote=True)


def fmt_date(iso, lang):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {MONTHS_FR[d.month - 1]} {d.year}" if lang == "fr" else f"{MONTHS_EN[d.month - 1]} {d.day}, {d.year}"


def slugify(text):
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:60] or "section"


STOP = {"de", "du", "des", "la", "le", "les", "l’", "et", "au", "aux", "en", "à", "a", "the", "of", "and", "to", "in", "on", "at", "for", "with", "from", "by", "or", "un", "une", "d’", "par", "pour", "sur", "dans", "avec", "its", "his", "her", "their", "that", "who", "entre", "between", "vers", "chez", "sans", "sous", "comme", "as", "like", "into", "onto", "through", "across", "after", "before", "since", "until", "under", "over", "aux", "nommé", "nominated"}


def _word_cut(text, room):
    """Longest word-boundary prefix of text that fits in room, without a dangling stopword. Never returns more than room characters."""
    if len(text) <= room:
        return text
    if room <= 0:
        return ""
    if text[room] == " ":
        cut = text[:room]
    elif " " in text[:room]:
        cut = text[:room].rsplit(" ", 1)[0]
    else:
        return ""
    words = cut.split(" ")
    while words and (words[-1].lower().rstrip(",:;") in STOP or len(words[-1]) < 2
                     or (len(words) > 1 and words[-2].lower().rstrip(",:;") in STOP)):
        words.pop()
    return " ".join(words).rstrip(" ,;:")


def island_of(slug, lang):
    try:
        import islands_data
        for code, kind in islands_data.links_for(slug):
            for i in islands_data.ISLANDS:
                if i[0] == code:
                    return i[2] if lang == "en" else i[3]
    except Exception:
        pass
    return None


def short_title(t, slug=None, lang="fr"):
    """Pipe-format titles only: Keyword | Benefit | Bouyon Musique.

    Shorten ONLY the benefit (middle) segment, by word-cutting until the
    total fits TITLE_MAX. The keyword and the brand are never touched, no
    island is appended, and no second brand is added. A title that is not
    in the three-segment pipe format (old data titles, hand-built pages)
    passes through unchanged: the rewrite moves every data title to the
    pipe format, so nothing here should re-cut them. If the keyword plus
    the brand alone already fills TITLE_MAX, or the benefit cannot be cut
    to a usable length, the title is left untouched for a human call.
    """
    segs = [s.strip() for s in t.split(" | ")]
    if len(segs) != 3 or segs[2] != "Bouyon Musique":
        return t
    keyword, benefit, brand = segs
    if len(t) <= TITLE_MAX:
        return t
    fixed = len(keyword) + len(" | ") + len(" | ") + len(brand)
    if fixed >= TITLE_MAX:
        return t
    room = TITLE_MAX - fixed
    # Never split the benefit's first comma phrase: either it fits whole
    # (e.g. an island name) or the title is left untouched and flagged,
    # rather than keeping a fragment like "Saint" of "Saint Vincent...".
    first = benefit.split(",", 1)[0]
    if len(first) > room:
        return t
    cut = _word_cut(benefit, room)
    if len(cut) < len(first):
        cut = first
    if len(cut) < 4:
        return t
    out = keyword + " | " + cut + " | " + brand
    if len(out) > TITLE_MAX:
        return t
    return out


def short_desc(d):
    if len(d) <= DESC_MAX:
        return d
    cut = d[:DESC_MAX]
    out = None
    for sep in [". ", " : ", ": ", " ; ", "; ", ", "]:
        i = cut.rfind(sep)
        if i >= 70:
            out = cut[:i]
            break
    if out is None:
        out = cut.rsplit(" ", 1)[0]
    out = out.rstrip(" ,;:")
    if out.endswith(" et") or out.endswith(" and"):
        out = out.rsplit(" ", 1)[0]
    return out if out.endswith((".", "!", "?")) else out + "."


def ld_blocks(s):
    """[(raw_json, data)] for every JSON-LD block."""
    out = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            out.append((m.group(1), json.loads(m.group(1))))
        except ValueError:
            pass
    return out


def nodes_of(data):
    if isinstance(data, dict):
        return data["@graph"] if isinstance(data.get("@graph"), list) else [data]
    return data if isinstance(data, list) else []


def dump_like(raw, data):
    indent = 2 if "\n" in raw.strip() else None
    return "\n" + json.dumps(data, ensure_ascii=False, indent=indent) + "\n" if indent else json.dumps(data, ensure_ascii=False)


def types(node):
    t = node.get("@type") if isinstance(node, dict) else None
    return set(t) if isinstance(t, list) else ({t} if t else set())


CTA_KINDS = [
    (re.compile(r'https?://(?:www\.)?instagram\.com/bouyonshattaz/?'), "instagram_follow"),
    (re.compile(r'https?://(?:www\.|m\.)?(?:youtube\.com|youtu\.be)/'), "youtube_link"),
    (re.compile(r'https?://open\.spotify\.com/'), "spotify_link"),
]


def tag_ctas(html_part):
    """data-cta on outbound <a> links to Instagram @bouyonshattaz, YouTube and Spotify (rerun-safe)."""
    def tag(m):
        a = m.group(0)
        if "data-cta=" in a:
            return a
        href = re.search(r'href="([^"]+)"', a)
        for pat, kind in CTA_KINDS:
            if href and pat.match(href.group(1)):
                return a[:-1] + f' data-cta="{kind}">'
        return a
    return re.sub(r'<a [^>]*href="https?://[^"]+"[^>]*>', tag, html_part)


def page_url(rel):
    if rel.endswith("index.html"):
        rel = rel[:-len("index.html")]
    return BASE + "/" + rel


def process(path, rel, hashes):
    # Photo pages own their titles, image schema and four-variant sitemap.
    if rel.startswith(("photos/", "en/photos/")):
        return None
    s = open(path, encoding="utf-8").read()
    lang = "en" if rel.startswith("en/") else "fr"
    t = T[lang]
    url = page_url(rel)
    main_start = s.find("<main")
    if main_start < 0 or "<title>" not in s:
        return None
    blocks = ld_blocks(s)
    page_name = None
    for _, data in blocks:
        for n in nodes_of(data):
            if "BreadcrumbList" in types(n) and n.get("itemListElement"):
                page_name = n["itemListElement"][-1].get("name")

    # 1. title, description, H1
    title = html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1).strip())
    slug = os.path.basename(rel)[:-5]
    new_title = short_title(title, slug, lang)
    desc_m = re.search(r'<meta name="description" content="([^"]*)">', s)
    desc = html.unescape(desc_m.group(1)) if desc_m else ""
    new_desc = short_desc(desc) if desc else desc
    if new_title != title:
        s = re.sub(r"<title>.*?</title>", lambda m: f"<title>{esc(new_title)}</title>", s, count=1, flags=re.S)
        s = re.sub(r'<meta property="og:title" content="[^"]*">', lambda m: f'<meta property="og:title" content="{esc(new_title)}">', s, count=1)
    if new_desc != desc:
        s = re.sub(r'<meta name="description" content="[^"]*">', lambda m: f'<meta name="description" content="{esc(new_desc)}">', s, count=1)
        s = re.sub(r'<meta property="og:description" content="[^"]*">', lambda m: f'<meta property="og:description" content="{esc(new_desc)}">', s, count=1)
    # H1s are frozen: they stay exactly as authored. (2026-11-10 title rewrite:
    # pipe-format titles must not flow into H1s, and the repo rule keeps H1s
    # stable. The old rule that replaced H1s with the short title is removed.)

    # 1b. social card tags
    if '<meta name="twitter:title"' not in s and '<meta name="twitter:card"' in s:
        s = re.sub(r'(<meta name="twitter:card" content="[^"]*">)', lambda m: m.group(1) + f'\n<meta name="twitter:title" content="{esc(new_title)}">'
                   + (f'\n<meta name="twitter:description" content="{esc(new_desc)}">' if new_desc else ""), s, count=1)

    # 2. skip link, main id, large image previews
    s = s.replace('<meta name="robots" content="index, follow">', '<meta name="robots" content="index, follow, max-image-preview:large">', 1)
    if 'class="skip"' not in s:
        s = s.replace("<body>", f'<body>\n<a class="skip" href="#content">{t["skip"]}</a>', 1)
    if "<main>" in s:
        s = s.replace("<main>", '<main id="content">', 1)

    # 3. images, videos, preconnect, script
    main_html = s.split("<main", 1)[1].split("</main>", 1)[0]
    vids, any_img = [], None
    for m in re.finditer(r'<div class="yt"( data-list="[^"]+")? data-id="([A-Za-z0-9_-]{11})">.*?<img src="([^"]+)" alt="([^"]*)" width="(\d+)" height="(\d+)"', main_html, re.S):
        if any_img is None:
            any_img = (m.group(3), int(m.group(5)), int(m.group(6)), html.unescape(m.group(4)))
        if not m.group(1) and m.group(2) not in vids:
            vids.append(m.group(2))
    hero = re.search(r'<figure class="artist-hero">.*?<img src="([^"]+)"[^>]*? alt="([^"]*)"[^>]*? width="(\d+)" height="(\d+)"', main_html, re.S)
    if hero:
        any_img = (hero.group(1), int(hero.group(3)), int(hero.group(4)), html.unescape(hero.group(2)))
    first_img = any_img
    if first_img:
        src, w, h, alt = first_img
        if 'content="https://bouyonmusique.com/og-image.png"' in s:
            s = s.replace('<meta property="og:image" content="https://bouyonmusique.com/og-image.png">', f'<meta property="og:image" content="{src}">', 1)
            s = re.sub(r'<meta property="og:image:width" content="\d+">', f'<meta property="og:image:width" content="{w}">', s, count=1)
            s = re.sub(r'<meta property="og:image:height" content="\d+">', f'<meta property="og:image:height" content="{h}">', s, count=1)
            s = re.sub(r'<meta property="og:image:alt" content="[^"]*">', lambda m: f'<meta property="og:image:alt" content="{esc(alt)}">', s, count=1)
        if 'rel="preconnect" href="https://i.ytimg.com"' not in s:
            s = s.replace('<link rel="stylesheet" href="/style.css">', '<link rel="preconnect" href="https://i.ytimg.com">\n<link rel="stylesheet" href="/style.css">', 1)
        if "querySelectorAll('.yt')" not in s:
            s = s.replace("</body>", yt.SCRIPT + "\n</body>", 1)

    # 3b. outbound listen/follow links
    ms = s.find("<main")
    s = s[:ms] + tag_ctas(s[ms:])

    # 4. table of contents
    if "<!-- onpage:toc -->" not in s:
        head, body = s[:main_start], s[main_start:]
        used, entries = set(), []

        def add_id(m):
            attrs, inner = m.group(1), m.group(2)
            text = html.unescape(re.sub(r"<[^>]+>", "", inner)).strip()
            if 'id="' in attrs:
                hid = re.search(r'id="([^"]+)"', attrs).group(1)
            else:
                hid = slugify(text)
                n, base = 2, hid
                while hid in used:
                    hid, n = f"{base}-{n}", n + 1
                attrs += f' id="{hid}"'
            used.add(hid)
            if text.lower().replace("’", "'") not in TOC_SKIP:
                entries.append((hid, text))
            return f"<h2{attrs}>{inner}</h2>"
        body = re.sub(r"<h2([^>]*)>(.*?)</h2>", add_id, body, flags=re.S)
        if len(entries) >= 3:
            toc = (f'<!-- onpage:toc -->\n<nav class="toc" aria-label="{t["toc"]}"><strong>{t["toc"]}</strong>\n<ol>\n'
                   + "".join(f'<li><a href="#{hid}">{esc(text)}</a></li>\n' for hid, text in entries) + "</ol>\n</nav>\n")
            i = body.find("<h2")
            body = body[:i] + toc + body[i:]
        s = head + body

    # 5. content hash, dates
    main_html = s.split("<main", 1)[1].split("</main>", 1)[0]
    digest = content_digest(main_html)
    prev = hashes.get(url) or {}
    rpath = release._key(url[len(BASE):] or "/")
    # A real change = the text hash moved since the last build (links and the dates line are not part of it).
    text_changed = prev.get("v") == HASH_VERSION and prev.get("hash") not in (None, digest)
    pub = release.true_published(rpath, prev.get("published"))
    if rpath in release.DATES:
        # Stored dates (build/release_dates.json): modified is kept while the text is unchanged; a real change after
        # the cutoff moves it to that day, and that day is carried from build to build.
        lastmod = release.true_modified(rpath, release.DATA_MOD.get(rpath), pub)
        if prev.get("v") == HASH_VERSION and prev.get("lastmod", "") > release.CUTOFF:
            lastmod = max(lastmod, prev["lastmod"])
        if text_changed:
            lastmod = max(lastmod, TODAY)
    else:
        if prev and prev.get("v") != HASH_VERSION:
            lastmod = prev.get("lastmod", TODAY)
        else:
            lastmod = prev.get("lastmod", TODAY) if not text_changed else TODAY
        data_mod = release.DATA_MOD.get(rpath)
        lastmod = max([lastmod, pub] + ([data_mod] if data_mod else []))
    hashes[url] = {"hash": digest, "lastmod": lastmod, "published": pub, "v": HASH_VERSION}
    s = set_dates_line(s, pub, lastmod, lang)

    # 6. structured data
    already_video = any("VideoObject" in types(n) for _, d in blocks for n in nodes_of(d))
    videos = []
    for vid in vids[:3]:
        m = yt.META.get(vid) or {}
        if not (m.get("ok") and m.get("upload_date")):
            continue
        src, w, h = yt.thumb(vid)
        up = m["upload_date"]
        videos.append({
            "@type": "VideoObject", "@id": f"{url}#video-{vid}", "name": m["title"],
            "description": t["video"].format(title=m["title"], page=page_name or new_title),
            "thumbnailUrl": [src], "uploadDate": f"{up[:4]}-{up[4:6]}-{up[6:8]}",
            "duration": yt.iso_duration(m.get("duration")),
            "embedUrl": f"https://www.youtube-nocookie.com/embed/{vid}", "url": f"https://www.youtube.com/watch?v={vid}",
        })
    _is_page = lambda n: "@id" in n and str(n["@id"]).endswith(("#page", "#webpage"))
    has_page_node = any(_is_page(n) for _, d in blocks for n in nodes_of(d))
    PAGE_TYPES = {"WebPage", "FAQPage", "CollectionPage", "AboutPage", "ItemPage", "Article", "NewsArticle", "BlogPosting"}
    for bi, (raw, data) in enumerate(blocks):
        ns = nodes_of(data)
        changed = False
        has_video = any("VideoObject" in types(n) for n in ns)
        if not has_page_node and bi == 0 and isinstance(data, dict):
            # Hand-built pages without a #page node: add one first, so the page's own dates lead its structured data.
            node = {"@type": "WebPage", "@id": url + "#page", "url": url, "datePublished": pub, "dateModified": lastmod}
            if isinstance(data.get("@graph"), list):
                data["@graph"].insert(0, node)
            else:
                ctx_ = data.pop("@context", "https://schema.org")
                inner = dict(data); data.clear(); data.update({"@context": ctx_, "@graph": [node, inner]})
            ns = nodes_of(data); changed = True
        for n in ns:
            ty = types(n)
            # Every page-type node without an id of its own (the page's Article, FAQPage...) carries the page's dates.
            if set(ty) & PAGE_TYPES and "@id" not in n and (n.get("datePublished") or n.get("dateModified")):
                if n.get("datePublished") != pub or n.get("dateModified") != lastmod:
                    n["datePublished"], n["dateModified"] = pub, lastmod; changed = True
            is_page = _is_page(n)
            if is_page:
                if n.get("name") == title and new_title != title:
                    n["name"] = new_title; changed = True
                if n.get("description") == desc and new_desc != desc:
                    n["description"] = new_desc; changed = True
                if n.get("datePublished") != pub:
                    n["datePublished"] = pub; changed = True
                if n.get("dateModified") != lastmod:
                    n["dateModified"] = lastmod; changed = True
                if first_img and not n.get("primaryImageOfPage"):
                    n["primaryImageOfPage"] = {"@type": "ImageObject", "url": first_img[0], "width": first_img[1], "height": first_img[2], "caption": first_img[3]}
                    n["image"] = first_img[0]; changed = True
                if videos and not has_video and not n.get("video"):
                    n["video"] = [{"@id": v["@id"]} for v in videos]; changed = True
            if str(n.get("@id", "")).endswith("/#org") and "logo" not in n:
                n["logo"] = dict(ORG_LOGO); changed = True
            if "MusicGroup" in ty and first_img and not n.get("image"):
                n["image"] = first_img[0]; changed = True
            if "ProfilePage" in ty and isinstance(n.get("mainEntity"), dict) and "MusicGroup" in types(n["mainEntity"]) and first_img and not n["mainEntity"].get("image"):
                n["mainEntity"]["image"] = first_img[0]; changed = True
        if videos and not has_video and isinstance(data, dict) and isinstance(data.get("@graph"), list):
            data["@graph"].extend(videos); changed = True
        if changed:
            s = s.replace(raw, dump_like(raw, data), 1)
    open(path, "w", encoding="utf-8").write(s)
    return dict(url=url, lastmod=lastmod, videos=videos, image=images.page_image(rel),
                title_len=len(new_title), desc_len=len(new_desc), shortened=new_title != title)


def seconds(iso):
    m = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else 0


def video_xml(v):
    x = lambda t: html.escape(t, quote=False)
    dur = seconds(v.get("duration"))
    return (f"    <video:video>\n      <video:thumbnail_loc>{v['thumbnailUrl'][0]}</video:thumbnail_loc>\n"
            f"      <video:title>{x(v['name'])}</video:title>\n      <video:description>{x(v['description'])}</video:description>\n"
            f"      <video:player_loc>{v['embedUrl']}</video:player_loc>\n"
            + (f"      <video:duration>{dur}</video:duration>\n" if dur else "")
            + f"      <video:publication_date>{v['uploadDate']}</video:publication_date>\n    </video:video>\n")


def update_sitemaps(info):
    by_url = {i["url"]: i for i in info}
    index_mods = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "sitemap-*.xml"))):
        x = open(f, encoding="utf-8").read()

        def fix(m):
            block = m.group(0)
            loc = re.search(r"<loc>([^<]+)</loc>", block).group(1)
            i = by_url.get(loc)
            if not i:
                return block
            block = re.sub(r"<lastmod>[^<]+</lastmod>", f"<lastmod>{i['lastmod']}</lastmod>", block, count=1)
            if i["videos"] and "<video:video>" not in block:
                block = block.replace("  </url>", "".join(video_xml(v) for v in i["videos"]) + "  </url>")
            block = re.sub(r"\s*<image:image>.*?</image:image>", "", block, flags=re.S)
            if i.get("image"):
                im = i["image"]
                block = block.replace("  </url>", f"    <image:image>\n      <image:loc>{im['loc']}</image:loc>\n      <image:title>{esc(im['title'])}</image:title>\n      <image:caption>{esc(im['caption'])}</image:caption>\n    </image:image>\n  </url>")
            return block
        x2 = re.sub(r"<url>.*?</url>", fix, x, flags=re.S)
        if "<image:image>" in x2 and "xmlns:image" not in x2:
            x2 = x2.replace('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"', 1)
        if "<video:video>" in x2 and "xmlns:video" not in x2:
            x2 = x2.replace('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"', 1)
        if x2 != x:
            open(f, "w", encoding="utf-8").write(x2)
        mods = re.findall(r"<lastmod>([^<]+)</lastmod>", x2)
        index_mods[BASE + "/" + os.path.basename(f)] = max(mods) if mods else TODAY
    idx = os.path.join(ROOT, "sitemap.xml")
    if os.path.exists(idx):
        x = open(idx, encoding="utf-8").read()
        x2 = re.sub(r"<sitemap>\s*<loc>([^<]+)</loc>\s*<lastmod>[^<]+</lastmod>",
                    lambda m: f"<sitemap>\n    <loc>{m.group(1)}</loc>\n    <lastmod>{index_mods.get(m.group(1), TODAY)}</lastmod>", x)
        if x2 != x:
            open(idx, "w", encoding="utf-8").write(x2)


def apply_onpage():
    hashes = json.load(open(HASHES, encoding="utf-8")) if os.path.exists(HASHES) else {}
    info = []
    for f in sorted(glob.glob(os.path.join(ROOT, "**/*.html"), recursive=True)):
        rel = os.path.relpath(f, ROOT)
        if rel.startswith(("build/", ".git/")) or rel == "404.html":
            continue
        r = process(f, rel, hashes)
        if r:
            info.append(r)
    update_sitemaps(info)
    json.dump(hashes, open(HASHES, "w", encoding="utf-8"), indent=0, sort_keys=True)
    print("onpage:", len(info), "pages;", sum(r["shortened"] for r in info), "titles shortened;",
          sum(1 for r in info if r["videos"]), "pages with VideoObject;",
          sum(1 for r in info if r["lastmod"] == TODAY), "lastmod set to today")


if __name__ == "__main__":
    apply_onpage()
