#!/usr/bin/env python3
"""Checks the built site and prints page metrics (BOU-3200).

python3 build/verify_site.py [site root] [--metrics-only]

Checks: internal links resolve, JSON-LD parses, every indexable page is in the
sitemaps and every sitemap URL exists, no duplicate titles, no em or en dashes
in mixtape and chronique pages, no auto-link of a name glued to another
capitalised word (Life Nice, Serbin Freddy, Trixx Migos).
"""
import collections, json, os, re, statistics, sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else Path(__file__).resolve().parents[1])
METRICS_ONLY = "--metrics-only" in sys.argv
BASE = "https://bouyonmusique.com"
SKIP_DIRS = {"build", ".git", "node_modules"}


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        if not SKIP_DIRS & set(p.relative_to(ROOT).parts):
            yield p


def url_of(p):
    rel = p.relative_to(ROOT).as_posix()
    return "/" + (rel[:-len("index.html")] if rel.endswith("index.html") else rel)


def target(href):
    path = href.split("#")[0].split("?")[0]
    if not path:
        return None
    f = ROOT / path.lstrip("/")
    return f / "index.html" if path.endswith("/") else f


def main():
    errors, titles = [], collections.defaultdict(list)
    m = collections.Counter()
    links_per_page = []
    indexable = set()
    for p in pages():
        text = p.read_text(encoding="utf-8")
        u = url_of(p)
        main_html = text.split("<main", 1)[-1].split("</main>", 1)[0]
        hrefs = re.findall(r'href="(/[^"]*)"', text)
        links_per_page.append(len(hrefs))
        for h in set(hrefs):
            t = target(h)
            if t and not t.exists():
                errors.append(f"{u}: broken link {h}")
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
            try:
                data = json.loads(block)
            except ValueError as e:
                errors.append(f"{u}: JSON-LD does not parse ({e})")
                continue
            s = json.dumps(data, ensure_ascii=False)
            m["pages_datePublished"] += '"datePublished"' in s
            m["pages_dateModified"] += '"dateModified"' in s
            m["pages_MusicGroup"] += '"MusicGroup"' in s
            m["pages_mentions_schema"] += '"mentions"' in s
            m["pages_VideoObject"] += '"VideoObject"' in s
        noindex = 'name="robots" content="noindex' in text
        if p.name != "404.html" and not noindex:
            indexable.add(u)
            t = re.search(r"<title>(.*?)</title>", text, re.S)
            if t:
                titles[t.group(1).strip()].append(u)
        m["pages"] += 1
        m["pages_byline"] += 'rel="author"' in main_html
        m["pages_breadcrumb"] += 'class="breadcrumb"' in main_html
        m["pages_related"] += bool(re.search(r"<h2>(À lire aussi|Read next)</h2>", main_html))
        m["pages_artist_hub_module"] += bool(re.search(r"<h2>[^<]+ (sur Bouyon Musique|on Bouyon Music)</h2>", main_html))
        m["pages_cited_artists_module"] += bool(re.search(r"<h2>(Artistes cités dans cette page|Artists mentioned on this page)</h2>", main_html))
        m["pages_youtube_embed"] += "youtube-nocookie.com/embed/" in main_html or 'class="yt"' in main_html
        m["mixtape_pages"] += u.startswith("/mixtapes/") and u != "/mixtapes/"
        m["chronique_pages"] += u.startswith("/chroniques/") and u != "/chroniques/"
        if u.startswith(("/mixtapes/", "/chroniques/")) and re.search("[–—]", main_html):
            errors.append(f"{u}: em or en dash in copy")
        for bad in re.findall(r"[A-Z][\w’']+ <a href=\"[^\"]+\">[^<]+</a>|<a href=\"[^\"]+\">[^<]+</a> [A-Z][a-z]+", main_html):
            word = re.sub(r"<[^>]+>", "", bad)
            if re.search(r"\b(Life Nice|Feeling Nice|Serbin Freddy|Miguel Hussey|Trixx Migos)\b", word):
                errors.append(f"{u}: auto-link glued to another name: {word}")
    for t, us in titles.items():
        if len(us) > 1:
            errors.append(f"duplicate title {t!r}: {us}")

    sm = ROOT / "sitemap.xml"
    locs = []
    root_xml = sm.read_text(encoding="utf-8")
    children = re.findall(r"<sitemap>\s*<loc>([^<]+)</loc>", root_xml)
    files = [ROOT / c.replace(BASE + "/", "") for c in children] if children else [sm]
    for f in files:
        if not f.exists():
            errors.append(f"missing sitemap {f.name}")
            continue
        x = f.read_text(encoding="utf-8")
        locs += [l.replace(BASE, "") for l in re.findall(r"<url>\s*<loc>([^<]+)</loc>", x)]
        m["video_sitemap_entries"] += x.count("<video:video>")
        m["image_sitemap_entries"] = m.get("image_sitemap_entries", 0) + x.count("<image:image>")
    m["sitemaps"] = len(files)
    m["sitemap_urls"] = len(locs)
    dup = [l for l, c in collections.Counter(locs).items() if c > 1]
    if dup:
        errors.append(f"sitemap duplicates: {dup[:5]}")
    for l in set(locs) - indexable:
        errors.append(f"sitemap URL with no indexable page: {l}")
    for u in sorted(indexable - set(locs)):
        errors.append(f"indexable page missing from sitemaps: {u}")

    m["internal_links_median"] = statistics.median(links_per_page)
    m["internal_links_total"] = sum(links_per_page)
    print(json.dumps(dict(m), indent=1))
    if not METRICS_ONLY:
        for e in errors:
            print("ERROR", e)
        print(f"{len(errors)} errors")
        sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
