# -*- coding: utf-8 -*-
"""Artist images: gather one image per artist profile from the sources already listed on the page
(YouTube video thumbnails first, Deezer artist pictures second), write them as named, resized JPEG and
WebP files with embedded description, keywords and credit, then place them on the profile pages in
batches over time.

CLI:
  python3 build/images.py --gather [--only slug,...]   fetch and process images (writes build/images.json)
  python3 build/images.py --rollout N [--priority f]    mark N more gathered profiles for display (build/images_rollout.json)
  python3 build/images.py --apply                       place the figures on the pages marked for display
  python3 build/images.py --status                      counts

Both generators call apply_images() before the on-page pass, so figures survive rebuilds. Overrides in
build/images_overrides.json: {"slug": {"youtube": "VIDEO_ID"} | {"deezer_artist": 123} | {"skip": true}}.
"""
import datetime, glob, hashlib, html, io, json, os, re, sys, time, unicodedata, urllib.parse, urllib.request
from PIL import Image, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import islands_data

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE = "https://bouyonmusique.com"
IMG_DIR = os.path.join(ROOT, "img", "artistes")
DATA = os.path.join(HERE, "images.json")
ROLLOUT = os.path.join(HERE, "images_rollout.json")
OVERRIDES = os.path.join(HERE, "images_overrides.json")
LISTEN = os.path.join(HERE, "listen_sources.json")
YT_META = os.path.join(HERE, "yt_meta.json")
TODAY = datetime.date.today().isoformat()
UA = "Mozilla/5.0 (compatible; bouyonmusique-images/1.0; +https://bouyonmusique.com/)"
W, H = 1280, 720
SMALL = 640

ISL = {i[0]: i for i in islands_data.ISLANDS}


def _load(p, default):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else default


def norm(s):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())


def esc(s):
    return html.escape(s, quote=True)


def artists():
    """slug -> display name, from the A to Z list the islands step writes on artistes.html."""
    p = os.path.join(ROOT, "artistes.html")
    s = open(p, encoding="utf-8").read()
    m = re.search(r"<!-- islands:az:start -->(.*?)<!-- islands:az:end -->", s, re.S)
    blk = m.group(1) if m else s
    return {sl: html.unescape(n).strip() for sl, n in re.findall(r'<a href="/([a-z0-9-]+)\.html"[^>]*>([^<]{2,60})</a>', blk)}


def island(slug):
    links = islands_data.links_for(slug)
    if not links:
        return None
    code, _ = links[0]
    i = ISL[code]
    return {"code": code, "en": i[2], "fr": i[3], "anchor": i[4]}


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def deezer(path):
    try:
        return json.loads(fetch("https://api.deezer.com/" + path, 20))
    except Exception:
        return {}


# ---------------------------------------------------------------- source selection
def youtube_ids(rows):
    out = []
    for _, u in rows:
        m = re.search(r"youtube\.com/watch\?v=([\w-]{11})|youtu\.be/([\w-]{11})", u)
        if m:
            vid = m.group(1) or m.group(2)
            if vid not in out:
                out.append(vid)
    return out


def deezer_artist_ids(rows):
    ids = []
    for _, u in rows:
        m = re.search(r"deezer\.com/(?:[a-z]{2}/)?artist/(\d+)", u)
        if m and int(m.group(1)) not in ids:
            ids.append(int(m.group(1)))
    for _, u in rows:
        m = re.search(r"deezer\.com/(?:[a-z]{2}/)?(album|track)/(\d+)", u)
        if m:
            d = deezer(f"{m.group(1)}/{m.group(2)}")
            a = (d.get("artist") or {}).get("id")
            if a and a not in ids:
                ids.append(a)
            time.sleep(0.15)
    return ids


def deezer_by_name(name, rows):
    """Exact normalised name match AND one of the artist's Deezer release titles among the profile's
    listed titles, so a namesake never gets another artist's face."""
    d = deezer(f"search/artist?q={urllib.parse.quote(name)}&limit=5")
    titles = {norm(t) for t, _ in rows if t}
    for a in d.get("data", []):
        if norm(a.get("name", "")) != norm(name):
            continue
        albums = deezer(f"artist/{a['id']}/albums?limit=50").get("data", [])
        for al in albums:
            t = norm(al.get("title", ""))
            if t and any(t in x or x in t for x in titles if len(x) >= 5):
                return a["id"], al.get("title")
        time.sleep(0.15)
    return None, None


def yt_thumb(vid, meta):
    """(bytes, quality) for the best thumbnail that really exists."""
    order = ["maxresdefault", "sddefault", "hqdefault"]
    if meta.get(vid, {}).get("thumb") == "hqdefault":
        order = ["hqdefault"]
    for q in order:
        try:
            b = fetch(f"https://i.ytimg.com/vi/{vid}/{q}.jpg", 20)
        except Exception:
            continue
        try:
            im = Image.open(io.BytesIO(b))
        except Exception:
            continue
        if im.width >= 480:
            return b, q, im.width, im.height
    return None, None, 0, 0


# ---------------------------------------------------------------- image processing
def to_hero(im):
    """1280x720 frame: 16:9 sources are resized; other ratios sit on a blurred, darkened fill."""
    im = im.convert("RGB")
    w, h = im.size
    if abs(w / h - 16 / 9) < 0.02:
        return im.resize((W, H), Image.LANCZOS)
    if w / h > 1.25 and w / h < 1.4 and h >= 360:
        # 4:3 YouTube hqdefault with letterbox bars: crop the 16:9 centre
        bh = int(w * 9 / 16)
        top = (h - bh) // 2
        return im.crop((0, top, w, top + bh)).resize((W, H), Image.LANCZOS)
    scale = max(W / w, H / h)
    bg = im.resize((int(w * scale) + 1, int(h * scale) + 1), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = bg.filter(ImageFilter.GaussianBlur(28)).point(lambda v: int(v * 0.55))
    fscale = min(W / w, H / h)
    fg = im.resize((int(w * fscale), int(h * fscale)), Image.LANCZOS)
    bg.paste(fg, ((W - fg.width) // 2, (H - fg.height) // 2))
    return bg


def xmp_packet(d):
    kw = "".join(f"<rdf:li>{esc(k)}</rdf:li>" for k in d["keywords"])
    return f"""<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/" xmlns:xmpRights="http://ns.adobe.com/xap/1.0/rights/" xmlns:xmp="http://ns.adobe.com/xap/1.0/" xmlns:Iptc4xmpCore="http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/">
<dc:title><rdf:Alt><rdf:li xml:lang="x-default">{esc(d["title"])}</rdf:li></rdf:Alt></dc:title>
<dc:description><rdf:Alt><rdf:li xml:lang="x-default">{esc(d["description"])}</rdf:li></rdf:Alt></dc:description>
<dc:subject><rdf:Bag>{kw}</rdf:Bag></dc:subject>
<dc:creator><rdf:Seq><rdf:li>{esc(d["creator"])}</rdf:li></rdf:Seq></dc:creator>
<dc:rights><rdf:Alt><rdf:li xml:lang="x-default">{esc(d["rights"])}</rdf:li></rdf:Alt></dc:rights>
<photoshop:Credit>{esc(d["credit"])}</photoshop:Credit>
<photoshop:Source>{esc(d["source"])}</photoshop:Source>
<photoshop:Headline>{esc(d["title"])}</photoshop:Headline>
<xmpRights:Marked>True</xmpRights:Marked>
<xmpRights:WebStatement>{esc(d["page"])}</xmpRights:WebStatement>
<xmp:CreatorTool>bouyonmusique.com</xmp:CreatorTool>
</rdf:Description></rdf:RDF></x:xmpmeta>
<?xpacket end="w"?>""".encode("utf-8")


def exif_bytes(d):
    ex = Image.Exif()
    ascii_ = lambda t: unicodedata.normalize("NFKD", t.replace("\u201c", '"').replace("\u201d", '"').replace("\u00ab", '"').replace("\u00bb", '"')).encode("ascii", "ignore").decode()
    ex[0x010E] = ascii_(d["description"])[:250]
    ex[0x013B] = ascii_(d["creator"])[:120]
    ex[0x8298] = ascii_(d["rights"])[:250]
    ex[0x0131] = "bouyonmusique.com"
    for tag, val in ((0x9C9B, d["title"]), (0x9C9E, "; ".join(d["keywords"])), (0x9C9C, d["credit"])):
        ex[tag] = val.encode("utf-16-le") + b"\x00\x00"
    return ex.tobytes()


def write_variants(im, base, meta):
    """base is the path without size and extension. Returns [(path, w, h)]."""
    out = []
    xmp, exif = xmp_packet(meta), exif_bytes(meta)
    for width in (W, SMALL):
        v = im if width == W else im.resize((SMALL, int(SMALL * H / W)), Image.LANCZOS)
        for ext, kw in (("jpg", {"format": "JPEG", "quality": 82, "optimize": True, "progressive": True}),
                        ("webp", {"format": "WEBP", "quality": 78, "method": 6})):
            p = f"{base}-{width}.{ext}"
            v.save(p, exif=exif, xmp=xmp, **kw)
            out.append((p, v.width, v.height))
    return out


# ---------------------------------------------------------------- gather
def gather(only=None):
    os.makedirs(IMG_DIR, exist_ok=True)
    data = _load(DATA, {})
    over = _load(OVERRIDES, {})
    listen = _load(LISTEN, {})
    ymeta = _load(YT_META, {})
    names = artists()
    done = skipped = 0
    for slug, name in sorted(names.items()):
        if only and slug not in only:
            continue
        if slug in data and not (only and slug in only):
            continue
        ov = over.get(slug, {})
        if ov.get("skip"):
            skipped += 1
            continue
        rows = list(listen.get(slug + ".html", []))
        # song titles quoted in the profile text count as listed titles for the Deezer name confirmation
        fp = os.path.join(ROOT, slug + ".html")
        if os.path.exists(fp):
            body = open(fp, encoding="utf-8").read().split("<main", 1)[-1]
            quoted = re.findall(r"[«\u201c]\s*([^»\u201d<]{3,80}?)\s*[»\u201d]", html.unescape(re.sub(r"<[^>]+>", "", body)))
            rows += [(q, "") for q in quoted]
        isl = island(slug)
        src = None
        # 1. YouTube thumbnail of a video the profile already lists
        vids = ([ov["youtube"]] if ov.get("youtube") else []) + youtube_ids(rows)
        # videos already embedded elsewhere on the site whose channel is the artist, or whose title names the artist
        nn = norm(name)
        if len(nn) >= 4:
            own = [v for v, m in ymeta.items() if not v.startswith("list:") and m.get("ok") and norm(m.get("channel", "")) == nn]
            titled = [v for v, m in ymeta.items() if not v.startswith("list:") and m.get("ok") and re.match(r"^\W*" + re.escape(name.lower()) + r"\b", (m.get("title") or "").lower())]
            vids += [v for v in own + titled if v not in vids]
        for vid in vids:
            b, q, w, h = yt_thumb(vid, ymeta)
            if b:
                m = ymeta.get(vid, {})
                src = {"kind": "youtube", "id": vid, "url": f"https://www.youtube.com/watch?v={vid}", "quality": q,
                       "title": m.get("title") or next((t for t, u in rows if vid in u), ""), "channel": m.get("channel", "")}
                break
        # 2. Deezer artist picture, from the profile's own Deezer links
        if not src:
            ids = ([ov["deezer_artist"]] if ov.get("deezer_artist") else []) + deezer_artist_ids(rows)
            if not ids and rows:
                aid, _ = deezer_by_name(name, rows)
                if aid:
                    ids = [aid]
            for aid in ids:
                a = deezer(f"artist/{aid}")
                pic = a.get("picture_xl") or ""
                if pic and "/artist//" not in pic and norm(a.get("name", "")) == norm(name):
                    try:
                        b = fetch(pic, 20)
                    except Exception:
                        continue
                    src = {"kind": "deezer", "id": aid, "url": a.get("link", f"https://www.deezer.com/artist/{aid}"),
                           "title": a.get("name", name), "channel": "Deezer"}
                    break
        if not src:
            skipped += 1
            continue
        try:
            im = to_hero(Image.open(io.BytesIO(b)))
        except Exception:
            skipped += 1
            continue
        fr_isl = f" de {isl['fr']}" if isl and isl["code"] in ("dm", "gp", "mq", "lc", "ag", "bb", "gd", "vc", "tt", "jm") else (f" ({isl['fr']})" if isl else "")
        en_isl = f" from {isl['en']}" if isl and isl["code"] in ("dm", "gp", "mq", "lc", "ag", "bb", "gd", "vc", "tt", "jm") else (f" ({isl['en']})" if isl else "")
        if src["kind"] == "youtube":
            alt_fr = f"{name}, artiste bouyon{fr_isl} : image du clip « {src['title']} »" if src["title"] else f"{name}, artiste bouyon{fr_isl} : image de clip"
            alt_en = f"{name}, bouyon artist{en_isl}: still from the video “{src['title']}”" if src["title"] else f"{name}, bouyon artist{en_isl}: video still"
            cap_fr = f"Image : miniature YouTube de « {src['title']} »" + (f", chaîne {src['channel']}" if src["channel"] else "") + "."
            cap_en = f"Image: YouTube thumbnail of “{src['title']}”" + (f", {src['channel']} channel" if src["channel"] else "") + "."
            credit = src["channel"] or "YouTube uploader"
            rights = f"Thumbnail of the YouTube video {src['url']}; rights remain with {credit}. Shown on bouyonmusique.com to present the artist."
        else:
            alt_fr = f"{name}, artiste bouyon{fr_isl} : photo de l'artiste (page Deezer)"
            alt_en = f"{name}, bouyon artist{en_isl}: artist photo (Deezer page)"
            cap_fr = f"Image : photo d'artiste de la page Deezer de {name}."
            cap_en = f"Image: artist photo from {name}'s Deezer page."
            credit = f"{name} / Deezer"
            rights = f"Artist picture from the Deezer artist page {src['url']}; rights remain with the artist and their label. Shown on bouyonmusique.com to present the artist."
        fname = f"{slug}-bouyon" + (f"-{isl['anchor']}" if isl else "")
        base = os.path.join(IMG_DIR, fname)
        kws = [name, "bouyon", "bouyon music", "musique bouyon"] + ([isl["en"], isl["fr"]] if isl else []) + (["Dominica", "Dominique"] if not isl or isl["code"] != "dm" else [])
        meta = {"title": f"{name} (bouyon)", "description": alt_en, "keywords": list(dict.fromkeys(kws)), "creator": credit,
                "rights": rights, "credit": credit + (" via YouTube" if src["kind"] == "youtube" else ""), "source": src["url"],
                "page": f"{BASE}/{slug}.html"}
        variants = write_variants(im, base, meta)
        data[slug] = {"name": name, "file": fname, "w": W, "h": H, "source": src, "alt_fr": alt_fr, "alt_en": alt_en,
                      "caption_fr": cap_fr, "caption_en": cap_en, "island": isl, "gathered": TODAY,
                      "sha": hashlib.sha1(open(variants[0][0], "rb").read()).hexdigest()[:12],
                      "bytes": {os.path.basename(p): os.path.getsize(p) for p, _, _ in variants}}
        done += 1
        time.sleep(0.2)
    json.dump(data, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    print(f"images: gathered {done}, skipped {skipped}, total {len(data)} of {len(names)} profiles")


# ---------------------------------------------------------------- rollout
def rollout(n, priority=None):
    data = _load(DATA, {})
    state = _load(ROLLOUT, {})
    prio = _load(priority, {}) if priority else {}
    def score(slug):
        imp = sum(v[1] for k, v in prio.items() if k.rstrip("/") in (f"{slug}.html", f"en/{slug}.html")) if prio else 0
        return (-imp, 0 if data[slug]["source"]["kind"] == "youtube" else 1, slug)
    todo = sorted((s for s in data if s not in state), key=score)[:n]
    for s in todo:
        state[s] = TODAY
    json.dump(state, open(ROLLOUT, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print(f"images: rollout +{len(todo)} ({', '.join(todo)}); {len(state)} of {len(data)} gathered are live")
    return todo


# ---------------------------------------------------------------- apply
def figure(d, lang, slug):
    f = d["file"]
    u = f"{BASE}/img/artistes/{f}"
    alt = d["alt_fr"] if lang == "fr" else d["alt_en"]
    cap = d["caption_fr"] if lang == "fr" else d["caption_en"]
    src = d["source"]
    link = f' <a href="{esc(src["url"])}" rel="nofollow noopener" target="_blank">{"Voir la source" if lang == "fr" else "View source"}</a>'
    sizes = "(max-width: 760px) 100vw, 760px"
    return (f'<figure class="artist-hero"><picture>'
            f'<source type="image/webp" srcset="{u}-{SMALL}.webp {SMALL}w, {u}-{W}.webp {W}w" sizes="{sizes}">'
            f'<img src="{u}-{W}.jpg" srcset="{u}-{SMALL}.jpg {SMALL}w, {u}-{W}.jpg {W}w" sizes="{sizes}" alt="{esc(alt)}" '
            f'title="{esc(d["name"])}" width="{W}" height="{H}" loading="eager" fetchpriority="high" decoding="async"></picture>'
            f'<figcaption>{esc(cap)}{link}</figcaption></figure>')


def page_image(rel):
    """Sitemap and structured-data facts for a page, or None. rel like 'reo.html' or 'en/reo.html'."""
    data = _load(DATA, {})
    state = _load(ROLLOUT, {})
    lang = "en" if rel.startswith("en/") else "fr"
    slug = os.path.basename(rel)[:-5]
    d = data.get(slug)
    if not d or slug not in state:
        return None
    return {"loc": f"{BASE}/img/artistes/{d['file']}-{W}.jpg", "title": d["name"] + (" (bouyon)" if lang == "en" else " (bouyon)"),
            "caption": d["alt_en"] if lang == "en" else d["alt_fr"], "w": W, "h": H}


def apply_images():
    data = _load(DATA, {})
    state = _load(ROLLOUT, {})
    placed = removed = 0
    for slug, d in data.items():
        for lang, rel in (("fr", f"{slug}.html"), ("en", f"en/{slug}.html")):
            p = os.path.join(ROOT, rel)
            if not os.path.exists(p):
                continue
            s = open(p, encoding="utf-8").read()
            s2 = re.sub(r"\n?<!-- images:hero:start -->.*?<!-- images:hero:end -->", "", s, flags=re.S)
            if slug in state:
                blk = "\n<!-- images:hero:start -->\n" + figure(d, lang, slug) + "\n<!-- images:hero:end -->"
                m = re.search(r'<p class="lead">.*?</p>', s2, re.S)
                if m:
                    s2 = s2[:m.end()] + blk + s2[m.end():]
                    placed += 1
            elif s2 != s:
                removed += 1
            if s2 != s:
                open(p, "w", encoding="utf-8").write(s2)
    print(f"images: {placed} figures placed, {removed} removed; {len(state)} profiles live of {len(data)} gathered")


def status():
    data = _load(DATA, {}); state = _load(ROLLOUT, {}); names = artists()
    kinds = {}
    for d in data.values():
        kinds[d["source"]["kind"]] = kinds.get(d["source"]["kind"], 0) + 1
    print(f"profiles {len(names)} | gathered {len(data)} {kinds} | live {len(state)} | waiting {len(data) - len(state)} | without image {len(names) - len(data)}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--gather" in a:
        only = set(a[a.index("--only") + 1].split(",")) if "--only" in a else None
        gather(only)
    if "--rollout" in a:
        rollout(int(a[a.index("--rollout") + 1]), a[a.index("--priority") + 1] if "--priority" in a else None)
    if "--apply" in a:
        apply_images()
    if "--status" in a or not a:
        status()
