"""Release schedule and page dates, shared by generate.py, generate_en_full.py, onpage.py and image_discovery.py.

  - release_dates.json: the published and modified day of every page that existed by the cutoff (2026-11-07).
    Published beats every other source and never changes. Modified is kept while the page's text is unchanged.
  - date_floors.json: the earliest day each date may show, from the dates the page itself states (event days, release
    days, cited sources). Published is never before its floor; modified never before its floor or published.
  - A real content change after the cutoff (onpage.py: visible text with links removed changed, or a page-data
    date_modified after the cutoff) moves modified to that day. Record it in release_dates.json after the deploy.
  - Pages released after the cutoff follow the release schedule ($SITE_RELEASE_FILE, else a local
    build/release_schedule.json kept out of git): held or not-yet-due pages are left out of the build, and a page that
    goes live takes its real release day.
"""
import datetime, json, os
from zoneinfo import ZoneInfo

BUILD = os.path.dirname(os.path.abspath(__file__))
DATES_FILE = os.path.join(BUILD, "release_dates.json")
FLOORS_FILE = os.path.join(BUILD, "date_floors.json")
HASHES_FILE = os.path.join(BUILD, "content_hashes.json")
BASE = "https://bouyonmusique.com"

REL_FILE = os.environ.get("SITE_RELEASE_FILE") or os.path.join(BUILD, "release_schedule.json")
TODAY = os.environ.get("SITE_RELEASE_TODAY") or datetime.datetime.now(ZoneInfo("America/New_York")).date().isoformat()


def _key(p):
    p = "/" + p.split("://", 1)[-1].split("/", 1)[-1] if "://" in p else "/" + p.lstrip("/")
    p = p.split("?")[0].split("#")[0]
    if p.endswith("/index.html"):
        p = p[:-10]
    return p if (p.endswith("/") or "." in p.rsplit("/", 1)[-1]) else p + "/"


SCHED = {_key(e.get("path") or e["url"]): e for e in json.load(open(REL_FILE))["pages"]} if os.path.exists(REL_FILE) else {}


def is_live(p):
    e = SCHED.get(_key(p))
    if not e:
        return True
    if e.get("status") == "held":
        return False
    d = e.get("released_at") or e.get("publish_at")
    return bool(d) and d <= TODAY


def published(p):
    """Scheduled pages only: released_at, else today when the page goes live with this build."""
    e = SCHED.get(_key(p))
    return (e.get("released_at") or TODAY) if e and is_live(p) else None


_D = json.load(open(DATES_FILE, encoding="utf-8")) if os.path.exists(DATES_FILE) else {}
DATES = _D.get("pages", {})
CUTOFF = _D.get("cutoff", "2026-11-07")
FLOORS = json.load(open(FLOORS_FILE, encoding="utf-8"))["pages"] if os.path.exists(FLOORS_FILE) else {}
_HASHES = json.load(open(HASHES_FILE, encoding="utf-8")) if os.path.exists(HASHES_FILE) else {}


def _floor(path, kind):
    return (FLOORS.get(_key(path)) or {}).get(kind)


def true_published(path, data_date=None):
    path = _key(path)
    d = published(path) or (DATES.get(path) or {}).get("published") or (_HASHES.get(BASE + path) or {}).get("published")
    if not d:
        d = data_date if data_date and data_date >= TODAY else TODAY
    f = _floor(path, "published")
    return max(d, f) if f else d


def true_modified(path, data_mod=None, pub=None):
    """Stored modified; a data date after the cutoff is a real change; never before published or the floor."""
    path = _key(path)
    pub = pub or true_published(path)
    stored = (DATES.get(path) or {}).get("modified")
    if stored:
        m = max(stored, data_mod) if data_mod and data_mod > CUTOFF else stored
    else:
        m = data_mod or pub
    return max([m, pub] + [x for x in [_floor(path, "modified")] if x])


# Data dates of the pages this process generated (path -> date_modified). onpage.py, called at the end of the same
# generator run, takes a page's date from here and never from previously built HTML.
DATA_MOD = {}


def stamp(page, path):
    """Set the page's date_published and date_modified from the stored dates and floors."""
    path = _key(path)
    pub = true_published(path, page.get("date_published"))
    data_pub, mod = page.get("date_published"), page.get("date_modified")
    if path not in DATES and data_pub and data_pub > pub and (not mod or mod < data_pub):
        mod = data_pub
    page["date_published"] = pub
    page["date_modified"] = true_modified(path, mod, pub)
    DATA_MOD[path] = page["date_modified"]
    return page


def drop_held_output(site_root, rel_paths):
    for rp in rel_paths:
        f = os.path.join(site_root, rp.lstrip("/"))
        if os.path.isfile(f):
            os.remove(f)
