# Handoff prompt for Claude Code: MusicRecording backfill, batch 2 (given to Sean 2026-10-20)

You are working in the repo bouyonkonet/bouyonmusique (clone it, pull the latest main first: 12 parity waves and recordings batch 1 landed after your PR #1). Read build/README.md, build/TAKEOVER-PLAN-20261020.md and the recordings section of build/ONPAGE-AUDIT-20261020.md before starting.

MISSION: backfill verified MusicRecording data for artist profiles that are already live but have no or few recordings. Recordings are how Google understands a discography; the rival site carries 8,109 MusicRecording entities, we are at about 220. First milestone: 1,500 verified recordings sitewide.

YOUR BATCH 2 SCOPE (only these profiles): gz-up, hypno, prod-bysavion, denmath, mb-on-the-track, dcamp-lewismelo, bonna, ridge, ricky-bishop, david-campana, dj-blax, ras-b, tallyboy, kkrytical, litleboy-lsbeats767. Their entries live in build/data_wave1.py and build/data_wave1_en.py. Do not touch any other module's recordings, and do not edit profile prose.

VERIFICATION STANDARD (hard): a recording enters only if you opened the source yourself in this session: the artist's official YouTube, Spotify, Apple Music, Shazam, Discogs, SoundCloud, Bandcamp, Audiomack, Deezer/Qobuz distributor pages, or the artist's official site or label page. Record only what the source shows: track title and artist credit exactly as printed; album, year and URL only when the source states them. NEVER copy discography lists from tiitii-nba.com; that site is off-limits as a source and must never be linked. Append every recording you add to build/research/recordings-sources.md under the artist's section with its verification URL; entries without a source line get cut in review.

FORMAT: match exactly how recordings batch 1 stored them in the data modules and how the generators emit them as MusicRecording schema. FR and EN modules carry identical recording data. Targets: 8-15 verified recordings for established artists, 3-5 for emerging ones. If an artist's verified catalogue is genuinely smaller, add what verifies and say so in the PR; never pad.

WORKFLOW:
1. Branch: claude/recordings-batch-2
2. Edit the two data modules, regenerate the site with the repo generators, and verify: 0 duplicate titles, 0 broken internal links, sitemap covers every indexable file except 404.html, no em dashes or en dashes anywhere in what you touched.
3. Open a PR titled "Recordings batch 2: existing profiles backfill" listing per-artist counts and the new sitewide MusicRecording total. Then STOP. Amani reviews the PR (fact spot-checks against the source log, schema validity, counts) and reports to Sean; Sean merges. Never merge your own PR, never push to main. Pull main before each new batch; new profiles land daily.

SITE RULES (non-negotiable): no em dashes or en dashes; artist titles are subjective and must be attributed, never stated as fact; Wrecketeng is the official spelling (per DJ Cut, the founding pioneer), reketeng is a widespread internet misspelling and is written only as that; bouyon soca was coined by Dada in Dominica in 2003 (Sean's first-hand testimony); Smokiller is described as Dominican-born only; sameAs links only from verified URLs; if a fact cannot be verified, flag it in the PR instead of writing it.

After batch 2, the queue continues with recordings backfill for parity waves 1-12 artists in wave order, one PR per wave group, same process.
