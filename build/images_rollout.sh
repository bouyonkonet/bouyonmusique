#!/usr/bin/env bash
# Daily artist-image batch: gather images for any new profiles, show N more profiles' images, rebuild, verify, publish.
# Cron runs this on the build machine. Nothing is pushed when the verifier reports an error.
set -euo pipefail
N="${1:-12}"
REPO="https://github.com/bouyonkonet/bouyonmusique.git"
WORK="$HOME/bouyonmusique-rollout"
LOG="$HOME/bouyon-indexing/logs/images-rollout.log"
mkdir -p "$(dirname "$LOG")"
exec >>"$LOG" 2>&1
echo "== $(date -Is) batch of $N"
if [ ! -d "$WORK/.git" ]; then git clone -q "$REPO" "$WORK"; fi
cd "$WORK"
git fetch -q origin && git checkout -q -B main origin/main
# page priority: Search Console impressions of the last 28 days (optional; the rollout works without it)
PRIO="$WORK/build/.images_priority.json"
python3 - "$PRIO" <<'PY' || true
import sys, json, datetime
sys.path.insert(0, "/home/nxusdev/bouyon-indexing")
try:
    import gsc_index as g
    today = datetime.date.today(); s = [x for x in g.SITES if x["domain"] == "bouyonmusique.com"][0]
    url = f"https://www.googleapis.com/webmasters/v3/sites/{g.q(s['property'])}/searchAnalytics/query"
    code, r = g.api("POST", url, {"startDate": str(today - datetime.timedelta(days=28)), "endDate": str(today), "dimensions": ["page"], "rowLimit": 2000})
    out = {x["keys"][0].replace("https://bouyonmusique.com/", ""): (x["clicks"], x["impressions"], round(x["position"], 1)) for x in r.get("rows", [])}
    json.dump(out, open(sys.argv[1], "w"))
except Exception as e:
    print("priority skipped:", e)
PY
python3 build/images.py --gather
python3 build/images.py --rollout "$N" --priority "$PRIO"
rm -f "$PRIO"
python3 build/generate.py >/dev/null && python3 build/generate_en_full.py >/dev/null
python3 build/verify_site.py | tail -1 | grep -q "^0 errors" || { echo "verify failed, not publishing"; git checkout -q -- . ; exit 1; }
if [ -z "$(git status --short)" ]; then echo "nothing to publish"; exit 0; fi
git add -A
git -c user.name="Bouyon Konet" -c user.email="bouyonkonet@users.noreply.github.com" commit -qm "Artist images: batch of $(date +%Y-%m-%d)"
GH_TOKEN="$(gh auth token -u bouyonkonet)"
git -c credential.helper= -c credential.helper='!f(){ echo username=bouyonkonet; echo password='"$GH_TOKEN"'; };f' push -q origin main
python3 "$HOME/bouyon-indexing/gsc_index.py" --site bouyonmusique.com submit >/dev/null 2>&1 || true
python3 build/images.py --status
