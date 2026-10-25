# -*- coding: utf-8 -*-
"""YouTube helpers shared by the page builders and build/onpage.py.

yt_meta.json (video id -> title, upload_date, duration, thumb) is filled by
    python3 build/yt.py --refresh
which asks yt-dlp for every video id found in the built pages and checks whether
a 1280x720 thumbnail (maxresdefault) exists on i.ytimg.com.

facade(id, title) renders the thumbnail as a real <img> with a play button; the
iframe is only created on click (see SCRIPT), which keeps YouTube's script off
the first paint and gives each page a crawlable image.
"""
import glob, html, json, os, re, subprocess, sys, urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
META_PATH = os.path.join(_HERE, "yt_meta.json")
META = json.load(open(META_PATH, encoding="utf-8")) if os.path.exists(META_PATH) else {}


def thumb(vid):
    """(url, width, height) of the best known thumbnail."""
    q = META.get(vid, {}).get("thumb", "hqdefault")
    return (f"https://i.ytimg.com/vi/{vid}/{q}.jpg",) + ((1280, 720) if q == "maxresdefault" else (480, 360))


def facade(vid, title):
    src, w, h = thumb(vid)
    t = html.escape(META.get(vid, {}).get("title") or title, quote=True)
    return (f'<div class="yt" data-id="{vid}"><a class="yt-link" href="https://www.youtube.com/watch?v={vid}">'
            f'<img src="{src}" alt="{t}" width="{w}" height="{h}" loading="lazy" decoding="async">'
            '<span class="yt-play" aria-hidden="true"></span></a></div>\n')


def facade_list(pid, title):
    """Playlist embed as a facade: the thumbnail of the playlist's first video (yt_meta.json "list:PID")."""
    m = META.get("list:" + pid) or {}
    if not m.get("first"):
        return None
    src, w, h = thumb(m["first"]) if m["first"] in META else (f"https://i.ytimg.com/vi/{m['first']}/{m.get('thumb', 'hqdefault')}.jpg",) + ((1280, 720) if m.get("thumb") == "maxresdefault" else (480, 360))
    t = html.escape(title, quote=True)
    return (f'<div class="yt" data-list="{pid}" data-id="{m["first"]}"><a class="yt-link" href="https://www.youtube.com/playlist?list={pid}">'
            f'<img src="{src}" alt="{t}" width="{w}" height="{h}" loading="lazy" decoding="async">'
            '<span class="yt-play" aria-hidden="true"></span></a></div>\n')


SCRIPT = ("<script>for(const d of document.querySelectorAll('.yt'))d.addEventListener('click',e=>{e.preventDefault();"
          "const f=document.createElement('iframe');f.src=d.dataset.list?'https://www.youtube-nocookie.com/embed/videoseries?list='+d.dataset.list+'&autoplay=1':'https://www.youtube-nocookie.com/embed/'+d.dataset.id+'?autoplay=1';"
          "f.title=d.querySelector('img').alt;f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';"
          "f.allowFullscreen=true;d.replaceChildren(f);});</script>")


def iso_duration(sec):
    sec = int(sec or 0)
    h, m, s = sec // 3600, sec % 3600 // 60, sec % 60
    return "PT" + (f"{h}H" if h else "") + (f"{m}M" if m else "") + f"{s}S"


def refresh(root):
    from concurrent.futures import ThreadPoolExecutor
    ids = set()
    for f in glob.glob(os.path.join(root, "**/*.html"), recursive=True):
        if "/build/" in f:
            continue
        s = open(f, encoding="utf-8").read()
        ids |= set(re.findall(r'(?:youtube(?:-nocookie)?\.com/embed/|youtu\.be/|youtube\.com/watch\?v=|class="yt" data-id=")([A-Za-z0-9_-]{11})', s))

    def has_maxres(vid):
        try:
            with urllib.request.urlopen(urllib.request.Request(f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg", method="HEAD"), timeout=15) as r:
                return r.status == 200
        except Exception:
            return False

    def one(vid):
        if META.get(vid, {}).get("ok"):
            return vid, META[vid]
        try:
            j = json.loads(subprocess.check_output(["yt-dlp", "--no-warnings", "--skip-download", "--no-playlist", "-J",
                                                    f"https://www.youtube.com/watch?v={vid}"], stderr=subprocess.DEVNULL, timeout=90))
            return vid, dict(ok=True, title=j.get("title"), upload_date=j.get("upload_date"), duration=j.get("duration"),
                             channel=j.get("channel"), thumb="maxresdefault" if has_maxres(vid) else "hqdefault")
        except Exception as e:
            return vid, dict(ok=False, err=type(e).__name__)

    with ThreadPoolExecutor(6) as ex:
        for vid, d in ex.map(one, sorted(ids)):
            META[vid] = d
    lists = set()
    for f in glob.glob(os.path.join(root, "**/*.html"), recursive=True):
        if "/build/" not in f:
            lists |= set(re.findall(r'(?:videoseries\?list=|data-list=")([A-Za-z0-9_-]+)', open(f, encoding="utf-8").read()))
    for pid in sorted(lists):
        if META.get("list:" + pid, {}).get("ok"):
            continue
        try:
            j = json.loads(subprocess.check_output(["yt-dlp", "--no-warnings", "--flat-playlist", "--playlist-items", "1", "-J",
                                                    f"https://www.youtube.com/playlist?list={pid}"], stderr=subprocess.DEVNULL, timeout=90))
            e = j["entries"][0]
            META["list:" + pid] = dict(ok=True, title=j.get("title"), first=e["id"], first_title=e.get("title"),
                                       thumb="maxresdefault" if has_maxres(e["id"]) else "hqdefault", count=j.get("playlist_count"))
        except Exception as e:
            META["list:" + pid] = dict(ok=False, err=type(e).__name__)
    json.dump(META, open(META_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
    print("yt_meta.json:", sum(1 for v in META.values() if v.get("ok")), "videos with metadata of", len(META))


if __name__ == "__main__":
    if "--refresh" in sys.argv:
        refresh(os.path.dirname(_HERE))
