# Build system for bouyonmusique.com

The repo root is the deployed GitHub Pages site (HTML output). This build/ folder is the source of truth for generated pages.

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
- Read TAKEOVER-PLAN-20261020.md in this folder for the strategy. Content and style rules are in the handoff prompt; they are strict (verified facts only, no copied text, no em dashes anywhere).
