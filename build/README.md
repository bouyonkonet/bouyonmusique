# Build system for bouyonmusique.com

The repo root holds the site output (HTML). This build/ folder is the source of truth for generated pages. GitHub Pages deploys through .github/workflows/pages.yml, which publishes only site files (HTML, CSS, images, sitemaps, robots.txt, CNAME). build/, AGENTS.md and README.md are never served.

Internal notes (research logs, plans, audits, discovery queues, playlist inventories) live in the bouyonmusique-notes repo, under the same build/ paths. Check it out beside this repo (~/bouyonmusique-notes). Artist pages read build/listen_sources.json (title + URL only); after editing the research logs in the notes repo, run `python3 build/sources_listen.py --export`.

Current direction, October 21, 2026: improve existing French coverage and music discovery; measure clicks before expanding the 675-URL sitemap. See ../AGENTS.md. The 2027 review pages are outside this deployment and must not be added by regeneration.

The five reviewed listening additions live in music_discovery_blocks.json. Both generators apply music_discovery.py after generation so these additions survive rebuilds without replacing existing titles, H1s, canonical URLs, playlists or article bodies. To reapply only these additions, run `python3 build/music_discovery.py` from the repository root. This does not change the sitemap.

- generate.py builds the French pages into the repo root. generate_en_full.py builds the full English mirror into /en/.
- Both generators write into the repository that contains this build/ folder (set BOUYONMUSIQUE_SITE to write somewhere else). A full run takes about 90 seconds.
- Content lives in data_*.py modules: French module + matching *_en.py module. New content goes in a new module pair, registered in the import lists of generate.py and generate_en_full.py.
- After editing: run `python3 generate.py && python3 generate_en_full.py`, then `python3 verify_site.py` (broken internal links, JSON-LD, duplicate titles, sitemap coverage, dashes in mixtape copy, wrong-artist auto-links; it also prints the page metrics). Commit, push, then check the live pages (GitHub Pages takes about 2 minutes).

## Artist hubs, mixtapes, chroniques (BOU-3200)

- Artist profiles stay at /<slug>.html and are the artist hubs: no /artistes/<slug> copies (they would duplicate ranking pages and grow the sitemap). hubs.py finds every page that mentions an artist, by a hand-written link to the profile or by the artist's name in the copy. A name glued to another capitalised word ("Life Nice", "Serbin Freddy", "Trixx Migos") does not count, and names in hubs.LINK_ONLY (Nice, Freddy, Kenny G and other names shared with words or people) count only through a hand-written link. The same guard stops linkify_sections from auto-linking those false matches.
- Each profile gets a "<Nom> sur Bouyon Musique" module listing those pages by section, plus an ItemList. Every page gets "Artistes cités dans cette page" and schema.org mentions. Profiles of musicians are typed ["Person", "MusicGroup"] (schema.org: MusicGroup can be a solo musician).
- Bylines: "Par Smokiller · Publié le · Mis à jour le" from date_published and date_modified. dateModified in the schema is the page's date_modified, not the build date.
- Mixtapes: data_mixtapes.py, rendered by editorial.py to /mixtapes/<slug>.html and /mixtapes/. Only Smokiller's published mixes; tracklists copied from the live YouTube chapters; thumbnails in mixtapes/img/ are Smokiller's own artwork from YouTube. Read the sources note at the top of data_mixtapes.py before adding one.
- Chroniques: data_chroniques.py (empty) uses the same renderer under /chroniques/. The shape of an entry is documented there. Nothing is published while the list is empty.
- sitemap.xml is a sitemap index: sitemap-pages.xml, sitemap-artistes.xml, sitemap-mixtapes.xml (with video entries), sitemap-en.xml, and sitemap-chroniques.xml once a chronique exists. Hand-built pages keep the lastmod already in the sitemaps.
- The root pages index.html, histoire/histories and artistes are hand-built, not generator-driven. Everything else comes from the modules.
- Read build/TAKEOVER-PLAN-20261020.md in the notes repo for the strategy. Content and style rules are in the handoff prompt; they are strict (verified facts only, no copied text, no em dashes anywhere).

## Islands (artist to island, island to artist)

- build/islands_data.py is the single source: every artist profile slug is filed under an island as FROM (the profile states the origin) or SCENE (the profile only places the artist in that island's circuit, base or release billing). A profile with neither is listed as "origin not stated". Add a slug only after reading the sentence in its profile that supports it; never guess.
- build/islands.py (run automatically at the end of both generators, or by hand with `python3 build/islands.py`) writes the island page (/bouyon-par-ile.html, /en/bouyon-by-island.html), the full roster on each island hub, the island line under the lead of every profile, and the A to Z list with flags on artistes.html and en/artists.html. Its blocks sit between `<!-- islands:NAME:start/end -->` markers.
- New profile: add its slug to islands_data.py (or leave it out if the origin is not stated), then rerun.
- sources_listen.NO_EMBED lists YouTube videos whose owner disabled embedding; they stay as source links instead of a broken player.

## Playlist links (Bouyon Music 2026 on YouTube)

`build/playlist_links.py` runs after `islands.py` and adds plain text links to the Bouyon Music 2026 YouTube playlist: a Listen line on every artist profile (artists with a song in the playlist are named, from `playlist_members.json`), a link under every embed of that playlist, and one line on the home, artists and island pages. Run `python3 build/playlist_links.py --refresh` to re-read the playlist with yt-dlp and update the member list.

## On-page pass (titles, images, video data, dates)

`build/onpage.py` runs last in both generators (`apply_onpage()`), after the playlist links. Rerun-safe.

- Titles are cut to 60 characters (name first, "bouyon" kept, brand suffix only when the title never had the word), descriptions to 155 at a sentence or clause end. The data files keep the long editorial titles; `short_title()` decides what the page shows. H1s without "bouyon" or longer than 70 characters take the short title.
- YouTube embeds are facades (`build/yt.py`, `facade()`): a real `<img>` of the video thumbnail with a play button, the iframe is created on click. `yt_meta.json` holds title, upload date, duration and thumbnail size per video; refresh it with `python3 build/yt.py --refresh` (yt-dlp, slow, YouTube rate-limits bursts).
- The first thumbnail of a page becomes its og:image, the WebPage primaryImageOfPage and the MusicGroup image. Pages without a video keep og-image.png.
- Every facade with known metadata gets a VideoObject in the JSON-LD and a `<video:video>` entry in the sitemaps.
- A "Sommaire" / "On this page" jump list is inserted before the first h2 when the page has 3 or more sections (h2s get ids).
- `content_hashes.json` stores a hash of each page's main text. When the text changes between builds, the sitemap lastmod, the WebPage dateModified and the visible "Updated" date move to the build day. Keep the file in git so dates only move when content does.

## Artist images (2026-10-28)

Verified Instagram posts/profile images, release artwork, and publisher photos can also be pinned with `local_image`, `sha256`, `source`, `revision`, and `require_verified_source` in `images_overrides.json`. The checksum is checked before processing, and pinned sources never fall back to a name search. Captions distinguish profile images, release artwork, group photos, and individual photos. A source correction uses a new revision in its image URLs. Skipped artists are excluded from rollout state.

`build/images.py` gives each artist profile one image, taken from a source the profile already lists: the thumbnail of a YouTube video on the page (or a video of the artist embedded elsewhere on the site), otherwise the artist picture of the Deezer page the profile links to. A Deezer name search is used only when one of the artist's Deezer release titles also appears in the profile's listed titles. Images are written to `img/artistes/<slug>-bouyon-<island>-{1280,640}.{jpg,webp}` with EXIF and XMP fields (title, description, keywords, creator, credit, source URL, rights note). Provenance sits in `build/images.json`; `build/images_overrides.json` can force a video, a Deezer artist id or a skip.

Images are shown in batches: `python3 build/images.py --rollout N` marks N more profiles (highest Search Console impressions first) in `build/images_rollout.json`, and `apply_images()` (run by both generators before the on-page pass) places a `<figure class="artist-hero">` with srcset, WebP and a credit caption after the lead paragraph of the FR and EN pages. The on-page pass then uses that image for og:image, primaryImageOfPage, the MusicGroup image and an `<image:image>` entry in the sitemaps, and sets `max-image-preview:large`. `build/images_rollout.sh N` is the daily cron job (gather new, roll out N, build, verify, publish).

## Artist photo directory

`image_discovery.py` runs after the artist images in both generators. It creates
FR `/photos/` and EN `/en/photos/` directories, an individual photo page for each
released artist, and `sitemap-images.xml`. Only entries already released in
`images_rollout.json` are included. Files in `img/photos/` include the source composition, branded landscape, square crop
and mirrored colour variants, each at two sizes in JPEG/WebP. EXIF, XMP and IPTC
carry keyword, caption, source and credit fields. Each page includes all sixteen
file variants in structured data and its sitemap entry. Brand font licenses are
kept beside the fonts. `image_variants_cache.json` avoids recompressing unchanged
source images on later builds. The source files in `img/artistes/` stay intact.

`image_discovery_manifest.json` tracks generated outputs. Removing an artist
from the release list or setting its `images_overrides.json` entry to `skip: true`
removes its gallery pages, aliases, sitemap entries and directory links on rebuild.
Original profile URLs and image provenance remain in the source catalogue.

Verified social photos can be pinned in `images_overrides.json` with `local_image`,
`sha256`, `source`, `revision` and `require_verified_source: true`. The gather
replaces a cached namesake when the pinned source changes and fails if the
source bytes change. Quoted prose no longer confirms Deezer matches: it may
describe a different performer. A revision changes every generated image URL.
