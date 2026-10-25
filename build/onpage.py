# -*- coding: utf-8 -*-
"""On-page SEO pass over the built site. Both generators call apply_onpage() last;
it can also be run alone from the repository root:  python3 build/onpage.py

What it does on every page, in French and English, rerun-safe:
  - <title> and og:title cut to 60 characters, keeping the name first and the
    word bouyon in; meta description cut to 155 at a sentence or clause end.
    The data files keep the long editorial titles; the page shows the short one.
  - H1 replaced by the short title when it has no "bouyon" or runs past 70 characters.
  - Per-page image: the first YouTube thumbnail on the page becomes og:image,
    the WebPage primaryImageOfPage and the MusicGroup image.
  - VideoObject structured data for every YouTube facade (up to 3), from yt_meta.json,
    and the same videos in the sitemaps as <video:video> entries.
  - A table of contents (jump links) before the first h2 when the page has 3 or more sections.
  - Skip link to #content, preconnect to i.ytimg.com, the facade click script.
  - Sitemap lastmod, WebPage dateModified and the visible "Updated" date follow the
    content: content_hashes.json remembers each page's main text, and a page whose
    text changed since the last build gets today's date.
"""
import datetime, glob, hashlib, html, json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yt

ROOT = os.environ.get("BOUYONMUSIQUE_SITE", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = "https://bouyonmusique.com"
HASHES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content_hashes.json")
TODAY = datetime.date.today().isoformat()
TITLE_MAX, DESC_MAX, H1_MAX = 60, 155, 70
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
    """Longest word-boundary prefix of text that fits in room, without a dangling stopword."""
    if len(text) <= room:
        return text
    words = text[:room + 1].rsplit(" ", 1)[0].split(" ")
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
    """Name first, then as many clauses as fit in 60 characters, with "bouyon" kept when the title had it."""
    has_bouyon = "bouyon" in t.lower()
    if len(t) <= TITLE_MAX and has_bouyon:
        return t
    sep = " : " if " : " in t else ": "
    name, rest = (t.split(sep, 1) + [""])[:2] if sep in t else (t, "")
    clauses = [c.strip() for c in re.split(r",\s+", rest) if c.strip()]
    tail_at = next((i for i, c in enumerate(clauses) if re.fullmatch(r"bouyon.*", c, re.I)), None)
    body, tail = (clauses, []) if tail_at is None else (clauses[:tail_at], clauses[tail_at:])
    join = lambda kept: name + (sep + ", ".join(kept) if kept else "")
    kept = []
    for c in body:
        if len(join(kept + [c])) > TITLE_MAX:
            if not kept:
                cut = _word_cut(c, TITLE_MAX - len(name) - len(sep) - (0 if "bouyon" in c.lower() or not has_bouyon else 8))
                if len(cut) >= 8:
                    kept.append(cut)
            break
        kept.append(c)
    if has_bouyon and "bouyon" not in join(kept).lower():
        for c in tail or ["bouyon"]:
            if len(join(kept + [c])) <= TITLE_MAX:
                kept.append(c)
            else:
                break
        while "bouyon" not in join(kept).lower():
            if len(kept) > 1:
                kept.pop()
                if len(join(kept + ["bouyon"])) <= TITLE_MAX:
                    kept.append("bouyon")
            elif kept:
                kept = [_word_cut(kept[0], TITLE_MAX - len(name) - len(sep) - 8), "bouyon"]
            else:
                kept = ["bouyon"]
        isl = island_of(slug, lang) if slug else None
        if isl and isl.lower() not in join(kept).lower() and len(join(kept + [isl])) <= TITLE_MAX:
            kept.append(isl)
    elif has_bouyon:
        for c in tail:
            if len(join(kept + [c])) > TITLE_MAX:
                break
            kept.append(c)
    if len(join(kept)) < 45 and len(kept) < len(body):
        cut = _word_cut(body[len(kept)], TITLE_MAX - len(join(kept)) - 2)
        if len(cut) >= 10:
            kept.append(cut)
    out = join(kept)
    if len(out) > TITLE_MAX:
        out = _word_cut(out, TITLE_MAX - (8 if has_bouyon else 0))
        if has_bouyon and "bouyon" not in out.lower():
            out += ", bouyon"
    if (not has_bouyon or len(out) <= 40) and len(out) + len(" | Bouyon Musique") <= TITLE_MAX:
        out += " | Bouyon Musique"
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


def page_url(rel):
    if rel.endswith("index.html"):
        rel = rel[:-len("index.html")]
    return BASE + "/" + rel


def process(path, rel, hashes):
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
    h1m = re.search(r"<h1>(.*?)</h1>", s, re.S)
    if h1m:
        h1 = html.unescape(re.sub(r"<[^>]+>", "", h1m.group(1))).strip()
        if "bouyon" not in h1.lower() or len(h1) > H1_MAX:
            new_h1 = re.sub(r" \| Bouyon Musique$", "", new_title)
            if new_h1 != h1:
                s = s[:h1m.start()] + f"<h1>{esc(new_h1)}</h1>" + s[h1m.end():]

    # 2. skip link and main id
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
    hashed = re.sub(r'<p class="pubdate">.*?</p>', "", main_html, flags=re.S)
    digest = hashlib.sha256(hashed.encode("utf-8")).hexdigest()[:16]
    prev = hashes.get(url) or {}
    lastmod = prev.get("lastmod", TODAY) if prev.get("hash") == digest else TODAY
    data_dates = [d for _, data in blocks for n in nodes_of(data) if "@id" in n and str(n["@id"]).endswith("#page")
                  for d in [n.get("dateModified"), n.get("datePublished")] if d]
    if data_dates and max(data_dates) > lastmod:
        lastmod = max(data_dates)
    hashes[url] = {"hash": digest, "lastmod": lastmod}
    upd = re.search(r'(%s <time datetime=")[^"]+(">)[^<]*(</time>)' % re.escape(t["updated"]), s)
    if upd and upd.group(0).find(lastmod) < 0 and lastmod > re.search(r'datetime="([^"]+)"', upd.group(0)).group(1):
        s = s[:upd.start()] + upd.group(1) + lastmod + upd.group(2) + fmt_date(lastmod, lang) + upd.group(3) + s[upd.end():]

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
    for raw, data in blocks:
        ns = nodes_of(data)
        changed = False
        has_video = any("VideoObject" in types(n) for n in ns)
        for n in ns:
            ty = types(n)
            is_page = "@id" in n and str(n["@id"]).endswith("#page")
            if is_page:
                if n.get("name") == title and new_title != title:
                    n["name"] = new_title; changed = True
                if n.get("description") == desc and new_desc != desc:
                    n["description"] = new_desc; changed = True
                if n.get("dateModified") and n["dateModified"] < lastmod or (not n.get("dateModified") and n.get("datePublished")):
                    n["dateModified"] = lastmod; changed = True
                if first_img and not n.get("primaryImageOfPage"):
                    n["primaryImageOfPage"] = {"@type": "ImageObject", "url": first_img[0], "width": first_img[1], "height": first_img[2], "caption": first_img[3]}
                    n["image"] = first_img[0]; changed = True
                if videos and not has_video and not n.get("video"):
                    n["video"] = [{"@id": v["@id"]} for v in videos]; changed = True
            if "MusicGroup" in ty and first_img and not n.get("image"):
                n["image"] = first_img[0]; changed = True
            if "ProfilePage" in ty and isinstance(n.get("mainEntity"), dict) and "MusicGroup" in types(n["mainEntity"]) and first_img and not n["mainEntity"].get("image"):
                n["mainEntity"]["image"] = first_img[0]; changed = True
        if videos and not has_video and isinstance(data, dict) and isinstance(data.get("@graph"), list):
            data["@graph"].extend(videos); changed = True
        if changed:
            s = s.replace(raw, dump_like(raw, data), 1)
    open(path, "w", encoding="utf-8").write(s)
    return dict(url=url, lastmod=lastmod, videos=videos,
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
            return block
        x2 = re.sub(r"<url>.*?</url>", fix, x, flags=re.S)
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
