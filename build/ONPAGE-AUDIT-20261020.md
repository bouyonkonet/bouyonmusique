# On-page SEO audit: bouyonmusique.com vs tiitii-nba.com

Date: 2026-10-20  
Mode: local files only. No live web checks.

## Method and definitions

- Rival corpus: `~/workspace/tiitii-clone/site/` (754 HTML files).
- Our corpus: `~/workspace/bouyonmusique.com/` (206 HTML files).
- “Indexable” in this audit means an HTML page that is not `404.html` and does not carry a `noindex` robots directive. That gives **746 pages for TIITII NBA** and **205 pages for Bouyon Musique**. The rival mirror has no sitemap file and contains parameterized mirror captures, so its local-corpus count should be read as an audit denominator, not as proof of what Google has indexed.
- Word count is visible text extracted from `<main>` where present, otherwise `<body>`, with scripts, styles, noscript and template content removed. This is a content-depth measure, not a raw HTML text dump.
- Internal links are deduplicated internal page targets per page, excluding the page itself, assets, anchors, mail links and external domains.
- Image alt coverage is the share of `<img>` elements with non-empty alt text. A page with no `<img>` elements is reported as 0 images; its alt coverage is not meaningful.
- Schema counts are JSON-LD `@type` occurrences, including nested `@graph` entities.
- FAQ count is the number of `Question` entities attached to `FAQPage` schema.
- Samples:
  - Artist profiles: 24 pages per site, 12 FR + 12 EN. His sample is evenly spaced through the 312 indexable artist profiles; ours is evenly spaced through the 62 pages carrying `ProfilePage` schema.
  - Chapter/knowledge: a stratified sample of 24 pages per site, 12 FR + 12 EN, across definitions, chapters, versus pages, how-tos, glossary, island pages and instruments/topics.
  - Homepages/hubs: 12 analogous pages per site: home, bouyon hub, artist index, Dominica hub, Guadeloupe hub and a best/playlist hub in FR and EN.

## Executive scoreboard

| Area | TIITII NBA | Bouyon Musique | Current edge |
|---|---:|---:|---|
| Indexable local pages | 746 | 205 | His, by 3.64x |
| Artist profiles with ProfilePage population | 312 | 62 | His, by 5.03x |
| Pages with FAQPage schema | 408 / 746 (54.7%) | 203 / 205 (99.0%) | Ours |
| FAQ questions in schema, total | 1,566 | 832 | His on volume; ours per page |
| Sitewide word count, mean / median | 1,285 / 1,347 | 1,130 / 691 | His |
| Pages under 800 words | 307 / 746 (41.1%) | 108 / 205 (52.7%) | His has more thin pages in absolute terms; ours has the worse rate |
| Unique titles | 659 / 746 (88.3%) | 205 / 205 (100%) | Ours |
| BreadcrumbList pages | 500 / 746 (67.0%) | 195 / 205 (95.1%) | Ours |
| MusicRecording entities | 8,109 | 96 | His, by 84.5x |
| Pages with MusicRecording | 231 | 46 | His |
| Sitewide unique internal links per page, mean / median | 23.5 / 23 | 21.9 / 20 | His, narrowly |
| `<img>` elements on indexable pages | 51,631 | 0 | His on visual presence; ours has no page images to optimize |
| Alt coverage across all `<img>` elements | 4.8% | n/a, because 0 `<img>` elements | Neither is in a good position |

The short version: **we already beat him on title uniqueness, FAQ coverage, breadcrumb coverage and most exact-keyword placement rates. He beats us decisively on scale, artist-profile count, discography schema, hub internal linking and visual content.** His artist pages are not uniformly enormous: the sampled median is close to ours. The dangerous gap is the long tail of structured discography and the sheer number of indexable entities.

---

## 1. Artist profile pages

Sample: 24 pages per site.

| Metric | TIITII NBA | Bouyon Musique | Reading |
|---|---:|---:|---|
| Population available | 312 profiles | 62 profiles | His profile library is 5.03x larger. |
| Title pattern | `{Name}: {fact or signature hook}, bouyon, {Dominica / Guadeloupe / Martinique}` | `{Name}: {editorial epithet or hook}, {song / place / event}` | His is more standardized and entity-led. |
| Title length, mean / median / range | 50.0 / 50 / 41-57 chars | 59.8 / 59.5 / 50-65 chars | His is tighter; ours is still inside a usable range but less consistent. |
| Titles containing “bouyon” | 100% | 83.3% | His wins. |
| Titles containing a place | 91.7% | 37.5% | His wins clearly. |
| Titles containing a year | 0% | 8.3% | Neither uses years systematically on artist pages. |
| Meta description presence | 100% | 100% | Tie. |
| Meta description length, mean / median / range | 121.8 / 119.5 / 75-157 chars | 145.8 / 146 / 133-154 chars | Ours is fuller and more consistent. |
| Meta descriptions containing “bouyon” | 41.7% | 66.7% | Ours wins. |
| H1 form | Exact artist name only: median 8 chars, 1.7 words; equals the title prefix on 100% | Name plus descriptive subtitle: median 56 chars, 9.4 words; never merely the title prefix | His is cleaner for entity matching; ours is more keyword-rich. Do not copy his bare H1 blindly. |
| Word count, mean / median / range | 2,026 / 1,849 / 1,104-3,938 | 1,789 / 1,817 / 1,161-2,613 | Median is nearly tied. His mean is higher because his top profiles run much longer. |
| H2 count, mean / median / range | 26.2 / 26.5 / 21-31 | 7.3 / 7.5 / 5-9 | His wins; most of the surplus is release/discography structure, not 26 prose chapters. |
| H3 count, mean / median | 16.8 / 15 | 7.0 / 7 | His wins. |
| ProfilePage pages | 100% | 100% | Tie. |
| FAQPage pages | 100% | 100% | Tie. |
| BreadcrumbList pages | 100% | 100% | Tie. |
| MusicRecording pages | 66.7% | 75.0% | Ours has wider page coverage. |
| MusicRecording entities per sampled page, average | 20.4 | 1.6 | His wins by 12.8x per page. This is the largest artist-page gap. |
| Person schema pages | 91.7% | 100% | Ours. |
| MusicGroup schema pages | 66.7% | 16.7% | His, although the correct type depends on whether the act is a band or a solo artist. |
| FAQ questions per page | Exactly 4 on all sampled pages | Exactly 3 on all sampled pages | His wins by one question. |
| Unique internal links, mean / median / range | 30.5 / 28 / 23-51 | 24.4 / 24 / 21-30 | His wins. |
| Internal link instances, mean / median | 59.1 / 47 | 34.3 / 34 | His wins; his pages repeat links in discography and cards. |
| Images per page, mean / median / range | 158.3 / 150 / 131-207 | 0 / 0 / 0 | His has visual/media furniture; the count is inflated by repeated platform icons and release thumbnails. |
| Image alt coverage | 3.2% | n/a, 0 images | His alt implementation is very poor. We can beat him with a few real, described images rather than 150 repetitive ones. |

### Artist-page conclusion

Our median profile is already competitive. The work is not “make every profile 4,000 words.” The work is:

1. Raise the floor and the priority-page ceiling.
2. Add structured discography depth.
3. Standardize title place/genre signals.
4. Add real images and internal links.
5. Scale from 62 profiles toward his 312-profile footprint.

---

## 2. Chapter and knowledge pages

Stratified sample: 24 pages per site.

| Metric | TIITII NBA | Bouyon Musique | Reading |
|---|---:|---:|---|
| Title pattern | Topic-first, usually `{Topic}: {angle}` or `{Topic} · TIITII NBA` on hub-like pages | `{Topic}: {Dominica / origin / year angle}` on almost every page | Ours is more consistently explanatory; his is tighter. |
| Title length, mean / median / range | 49.1 / 50 / 37-58 chars | 55.6 / 56 / 47-65 chars | His is tighter; ours is acceptable. |
| Titles containing “bouyon” | 100% | 91.7% | His wins narrowly. |
| Titles containing a place | 16.7% | 41.7% | Ours wins; the Dominica angle is visible. |
| Titles containing a year | 16.7% | 33.3% | Ours wins. |
| Meta description presence | 100% | 100% | Tie. |
| Meta description length, mean / median / range | 138.5 / 150 / 77-160 chars | 150.0 / 150 / 141-157 chars | Ours is more consistent. |
| Meta descriptions containing “bouyon” | 62.5% | 95.8% | Ours wins. |
| H1 length, median chars / words | 24.5 chars / 4.9 words | 50.5 chars / 8.5 words | His H1s are shorter and closer to the search phrase; ours are explanatory headlines. |
| H1 equals title prefix | 45.8% | 0% | His aligns title and H1 more often. |
| Word count, mean / median / range | 2,352 / 1,969 / 100-4,486 | 1,617 / 2,171 / 589-2,373 | Ours wins the median by 202 words. His wins the mean because several chapters exceed 3,000 words, while our low tail pulls the mean down. |
| H2 count, mean / median / range | 8.2 / 9 / 2-12 | 7.9 / 10 / 4-10 | Ours wins the median; essentially tied. |
| H3 count, mean / median | 2.4 / 2 | 6.4 / 7 | Ours has deeper substructure. |
| ProfilePage pages | 0% | 0% | Correctly absent. |
| FAQPage pages | 83.3% | 100% | Ours wins. |
| BreadcrumbList pages | 100% | 91.7% | His wins in this sample; the misses are hand-built pages. |
| Article pages | 8.3% | 25.0% | Ours wins, but 25% is still far too low for chapter pages. |
| Person schema pages | 91.7% | 91.7% | Tie. |
| MusicGroup schema pages | 41.7% | 0% | His has more entity references in chapter schema. |
| FAQ questions, mean / median / range | 2.3 / 1.5 / 0-5 | 3.6 / 3 / 3-5 | Ours wins. |
| Unique internal links, mean / median / range | 30.7 / 28.5 / 14-53 | 21.9 / 23.5 / 11-31 | His wins. |
| Images per page, mean / median / range | 10.6 / 9.5 / 1-26 | 0 / 0 / 0 | His wins on visual presence. |
| Image alt coverage | 34.6% | n/a, 0 images | His is still weak; a small number of properly described images would beat it. |

### Knowledge-page conclusion

Our generated wave-1 chapters are already strong: many sit around 2,200-2,500 words. The problem is a two-speed site. The thin sampled pages are concentrated in older or hand-built topics:

- `bouyon-gwada.html` and `en/bouyon-gwada.html`: roughly 600-680 words.
- `bouyon-drum-kit.html` and `en/bouyon-drum-kit.html`: roughly 590-626 words.
- `comment-faire-un-beat-bouyon.html` and `en/how-to-make-a-bouyon-beat.html`: roughly 646-696 words.
- `bouyon-soca.html` and `en/bouyon-soca.html`: roughly 801-895 words.
- `histoire.html` and `en/history.html`: roughly 849-968 words.

Those are not obscure pages. Bouyon gwada, bouyon soca, drum kit and how-to are money topics, so the low tail is exactly where expansion should start.

---

## 3. Homepages and hub pages

Sample: 12 analogous pages per site.

| Metric | TIITII NBA | Bouyon Musique | Reading |
|---|---:|---:|---|
| Title pattern | Mixed: artist-brand homepage, topic hub plus `TIITII NBA`, or `{Hub} ({year})` | Uniform topic-led pattern: `{Hub topic}: {Dominica / artists / playlist angle}` | Ours is more search-led; his homepage is artist-brand-led. |
| Title length, mean / median / range | 48.6 / 51.5 / 27-60 chars | 59.4 / 59 / 56-65 chars | His is tighter; ours is consistent. |
| Titles containing “bouyon” | 91.7% | 100% | Ours wins. |
| Titles containing a place | 58.3% | 66.7% | Ours wins narrowly. |
| Titles containing a year | 50.0% | 16.7% | His uses year-led hub titles more often. |
| Meta description presence | 100% | 100% | Tie. |
| Meta description length, mean / median / range | 137.9 / 147 / 81-157 chars | 147.6 / 147 / 137-160 chars | Tie on median; ours is more consistent. |
| H1 length, median chars / words | 33 chars / 5.7 words | 53 chars / 8.9 words | His is shorter; ours says more. |
| Word count, mean / median / range | 1,338 / 1,652 / 321-1,917 | 1,277 / 1,366 / 570-2,019 | His wins the median by 286 words. |
| H2 count, mean / median | 6.4 / 6.5 | 7.5 / 7.5 | Ours wins. |
| H3 count, mean / median | 20.8 / 5 | 6.8 / 7 | Mean is distorted by his artist-index cards; median is close. |
| FAQPage pages | 66.7% | 100% | Ours wins. |
| BreadcrumbList pages | 83.3% | 66.7% | His wins; our hand-built home/hub pages are the gap. |
| ItemList pages | 50.0% | 0% | His wins. Artist and playlist hubs need ItemList. |
| Person schema pages | 66.7% | 50.0% | His wins narrowly. |
| FAQ questions, mean / median / range | 5.2 / 4.5 / 0-17 | 4.0 / 4 / 3-5 | His wins on the largest hubs. |
| Unique internal links, mean / median / range | 69.5 / 50.5 / 36-165 | 26.5 / 26.5 / 10-47 | His wins decisively. This is the clearest hub-page gap. |
| Internal link instances, mean / median | 81.7 / 63.5 | 37.6 / 34 | His wins. |
| Images per page, mean / median / range | 32.8 / 10.5 / 9-108 | 0 / 0 / 0 | His wins on visual presence. |
| Image alt coverage | 11.2% | n/a, 0 images | His alt quality remains poor. |

### Hub-page conclusion

Our hubs read like articles with lists. His hubs behave like directories. To beat him, ours need both: keep the 1,400-2,000 words of editorial, then add complete linked cards for every relevant artist/topic and mark the list up as `ItemList`.

---

## 4. Sitewide results

| Metric | TIITII NBA | Bouyon Musique |
|---|---:|---:|
| HTML files in local corpus | 754 | 206 |
| Indexable by this audit's rule | 746 | 205 |
| Pages with FAQPage | 408 (54.7%) | 203 (99.0%) |
| Total FAQ questions in schema | 1,566 | 832 |
| Word count mean | 1,285 | 1,130 |
| Word count median | 1,347 | 691 |
| Word count 10th percentile | 279 | 570 |
| Word count 90th percentile | 2,392 | 2,177 |
| Pages under 500 words | 272 (36.5%) | 1 (0.5%) |
| Pages under 800 words | 307 (41.1%) | 108 (52.7%) |
| Pages under 1,000 words | 315 (42.2%) | 114 (55.6%) |
| Pages under 1,500 words | 417 (55.9%) | 144 (70.2%) |
| Pages under 2,000 words | 585 (78.4%) | 170 (82.9%) |
| Unique titles | 659 / 746 (88.3%) | 205 / 205 (100%) |
| Extra duplicate-title instances | 87 | 0 |
| Missing titles | 0 | 0 |
| Missing meta descriptions | 0 | 0 |
| Title length, median | 50 chars | 56 chars |
| Meta description length, median | 142 chars | 150 chars |
| ProfilePage pages | 312 | 62 |
| FAQPage pages | 408 | 203 |
| BreadcrumbList pages | 500 | 195 |
| MusicRecording pages | 231 | 46 |
| MusicRecording entities | 8,109 | 96 |
| Article pages | 22 | 10 |
| Person entities/pages represented in schema scan | 601 pages with Person | 191 pages with Person |
| MusicGroup pages | 326 | 12 |
| ItemList pages | 13 | 0 |
| Unique internal links per page, mean / median / range | 23.5 / 23 / 0-165 | 21.9 / 20 / 10-103 |
| Total `<img>` elements | 51,631 | 0 |
| Non-empty image alt coverage | 4.8% | n/a |

Important interpretation: his sitewide median word count is protected by the 312 artist profiles and the long knowledge chapters. Ours is dragged down by the older 500-900-word topic layer. Our problem is therefore **not the newest wave-1 writing**; it is the long tail of thin pages that still make up more than half the site.

## 5. Money-keyword coverage

Counts are pages carrying the exact normalized phrase. Percentages use 746 pages for TIITII NBA and 205 for Bouyon Musique.

| Exact term | Site | In title | In H1 | In first 100 words |
|---|---|---:|---:|---:|
| bouyon musique | TIITII NBA | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| bouyon musique | Bouyon Musique | 2 (1.0%) | 1 (0.5%) | 2 (1.0%) |
| music bouyon | TIITII NBA | 0 (0.0%) | 0 (0.0%) | 2 (0.3%) |
| music bouyon | Bouyon Musique | 0 (0.0%) | 0 (0.0%) | 1 (0.5%) |
| bouyon music | TIITII NBA | 0 (0.0%) | 0 (0.0%) | 3 (0.4%) |
| bouyon music | Bouyon Musique | 9 (4.4%) | 4 (2.0%) | 10 (4.9%) |
| bouyon soca | TIITII NBA | 3 (0.4%) | 4 (0.5%) | 17 (2.3%) |
| bouyon soca | Bouyon Musique | 6 (2.9%) | 4 (2.0%) | 20 (9.8%) |
| bouyon gwada | TIITII NBA | 3 (0.4%) | 1 (0.1%) | 69 (9.2%) |
| bouyon gwada | Bouyon Musique | 8 (3.9%) | 2 (1.0%) | 17 (8.3%) |
| dominica bouyon | TIITII NBA | 3 (0.4%) | 3 (0.4%) | 5 (0.7%) |
| dominica bouyon | Bouyon Musique | 1 (0.5%) | 2 (1.0%) | 9 (4.4%) |
| bouyon riddim | TIITII NBA | 0 (0.0%) | 0 (0.0%) | 3 (0.4%) |
| bouyon riddim | Bouyon Musique | 2 (1.0%) | 2 (1.0%) | 3 (1.5%) |
| bouyon playlist | TIITII NBA | 1 (0.1%) | 1 (0.1%) | 16 (2.1%) |
| bouyon playlist | Bouyon Musique | 1 (0.5%) | 1 (0.5%) | 7 (3.4%) |

### Keyword reading

- We already lead on exact-phrase placement rate for **bouyon musique, bouyon music, bouyon soca, dominica bouyon, bouyon riddim and bouyon playlist**.
- His only clear first-100-words win is **bouyon gwada**: 69 pages (9.2%) against our 17 pages (8.3%). His artist bios repeat the phrase at scale.
- Neither site has **music bouyon** in a title or H1. That exact word order should be handled deliberately on the French search landing layer, not stuffed into every page.
- The requested phrase list mixes natural and reversed forms. The correct response is one primary exact term per URL, placed in title, H1 or subtitle, first 100 words, one H2, meta description and one FAQ answer. Do not force all eight phrases onto one page.

---

# Ranked fix list

Owner key:

- **[Generators]** means the change belongs in `build/generate.py`, `build/generate_en_full.py`, shared templates, schema builders or validation.
- **[Content]** means the change belongs in `data_*.py` / `data_*_en.py` modules and research dossiers.
- **[Both]** means generator support plus new or expanded content data is required.

## 1. Expand the thin-page layer before adding more thin pages — [Content]

- Current state: **108 of our 205 pages are under 800 words** and **170 are under 2,000 words**.
- Target: no money, chapter, artist or hub page under **1,200 words**; core knowledge pages at **2,200-2,600 words**; sitewide median from **691 to at least 1,500 words** in the next expansion wave.
- First pages to expand, FR and EN:
  - `bouyon-gwada.html`: about 679 words to **2,400+**.
  - `bouyon-drum-kit.html`: about 626 words to **2,200+**.
  - `comment-faire-un-beat-bouyon.html`: about 696 words to **2,400+**.
  - `bouyon-soca.html`: about 895 words to **2,400+**.
  - `histoire.html`: about 968 words to **2,600+**.
  - Their EN mirrors to the same targets.
- Every expansion must add unique sections, examples, entities and internal links. Do not pad with repeated genre boilerplate.

## 2. Raise artist-profile depth with a fixed section formula — [Content]

- Current sampled state: ours **1,789 mean / 1,817 median words**, his **2,026 mean / 1,849 median**.
- Targets:
  - Emerging or thin-dossier artist minimum: **1,500 words**, honestly labelled by the available record.
  - Standard profile: **2,200-2,800 words**.
  - Priority profile: **3,200-3,800 words**.
  - Sampled median target: **2,400+ words**.
- Required structure for a standard profile:
  1. Identity and origin.
  2. Sound and role in bouyon.
  3. Career timeline.
  4. Key recordings, one H3 per verified major track or release.
  5. Collaborations and network.
  6. Live, carnival and WCMF relevance where verified.
  7. Why the artist matters now.
  8. Sources and related listening.
  9. Five FAQs.
  10. Related artists and chapters.
- His H2 advantage comes from discography structure. Match the structure, not his wording.

## 3. Build a verified MusicRecording layer at scale — [Both]

- Current state: **96 MusicRecording entities on 46 pages** for us; **8,109 entities on 231 pages** for him. Sampled artist average: **1.6 per page for us, 20.4 for him**.
- Targets:
  - Established artist: **8-15 verified `MusicRecording` entries**.
  - Emerging artist: **3-5 verified entries**, or none if the recording record is not verified.
  - Priority artists with a documented catalogue: **15-25 entries**.
  - First sitewide milestone: **1,500 verified recordings**.
  - Parity milestone: **8,200+ verified recordings**, only as real discography dossiers are built.
- **[Generators]** Add a reusable recording-schema builder that emits `MusicRecording` with verified `name`, `byArtist`, `datePublished`, `genre`, `duration`, `inAlbum` and `url` only when each field is sourced.
- **[Content]** Populate from the Bouyon Shattaz artist library and primary discography sources. Never invent a track, date, duration or album to raise the count.

## 4. Scale the artist-profile library — [Content]

- Current state: **62 ProfilePage pages** against his **312**.
- Targets:
  - Near term: **160 profiles total** (about 80 FR + 80 EN).
  - Parity-plus target: **320 profiles total** (about 160 FR + 160 EN).
- Priority order:
  1. Dominica originators, bands and WCMF acts.
  2. Guadeloupe and Martinique carriers.
  3. Producers, keyboard players, engineers and DJs.
  4. Women of bouyon.
  5. Saint Lucia, Antigua and diaspora connectors with a verified bouyon link.
- Do not publish a profile until it can meet the 1,500-word honest minimum or is explicitly a short verified directory entry inside a hub, not a standalone thin page.

## 5. Turn hubs into real directories with ItemList — [Both]

- Current sampled state: his hubs average **69.5 unique internal links**, ours **26.5**. His `ItemList` coverage is 50% in the hub sample; ours is **0%**.
- Targets per major hub:
  - **55-75 unique internal links** minimum.
  - Artist country hubs: **80-120 unique internal links** once the profile library supports them.
  - **1,800-2,200 words** of editorial plus cards.
  - One H3 per featured artist/topic card.
  - `ItemList` with `itemListElement` for every card.
  - `BreadcrumbList` on 100% of hubs, including hand-built pages.
- **[Generators]** Add a hub-card renderer that outputs the visible card, the internal link and the matching `ItemList` entry from one data list, so visible content and schema cannot drift.

## 6. Raise internal-link floors on artist and knowledge pages — [Generators]

- Current sampled medians:
  - Artist: his **28 unique targets**, ours **24**.
  - Knowledge: his **28.5**, ours **23.5**.
  - Hub: his **50.5**, ours **26.5**.
- Targets:
  - Artist pages: **35-45 unique internal targets**.
  - Knowledge pages: **35-50 unique internal targets**.
  - Hubs: **55-75**, country hubs **80+**.
- Required link pattern per artist page:
  - 1 country hub.
  - 1 artist index.
  - 2 knowledge chapters.
  - 3-6 related artists.
  - 2 style/branch pages.
  - 1 place page.
  - 1 playlist page.
  - Contextual first-mention links inside the prose, plus related blocks.
- Required pattern per knowledge page: link every named artist with a profile, every branch with a page, the relevant country hub, one how-to or chapter, and one playlist or listening page.
- Add a generator warning when a generated page falls below its page-type floor.

## 7. Standardize artist title and H1 signals — [Generators]

- Current state: his artist titles put a place on **91.7%** and “bouyon” on **100%**. Ours put a place on **37.5%** and “bouyon” on **83.3%**.
- Artist title formula, 50-60 characters where the name allows:
  - FR: `{Name}: {signature hook}, bouyon, {Dominique / Guadeloupe / Martinique}`
  - EN: `{Name}: {signature hook}, bouyon, {Dominica / Guadeloupe / Martinique}`
- Targets:
  - “bouyon” in **100%** of artist titles.
  - Place in **90%+** of artist titles.
  - Unique title on **100%**.
  - No site-brand suffix needed on artist pages.
- Keep our keyword-rich H1 form, but make it consistent:
  - `{Name}: {role or signature phrase} of {place} bouyon` or the closest natural equivalent.
  - The exact artist name must remain the opening entity in both title and H1.
- **[Generators]** Validate title length, uniqueness, opening entity, place field and genre field from the artist data record.

## 8. Fix the money-topic title/H1/first-100 alignment — [Both]

- Current state: our sampled knowledge titles average 55.6 chars and our descriptions are strong, but only **91.7%** of sampled knowledge titles contain “bouyon”, and title/H1 rarely match exactly.
- Targets for every core topic page:
  - Primary exact keyword in the **title**.
  - Primary exact keyword in the **H1 or its opening subtitle**.
  - Primary exact keyword in the **first 100 words**.
  - Primary exact keyword in **one H2**.
  - Primary exact keyword in the **meta description**.
  - Primary exact keyword in **one FAQ answer**.
- **[Generators]** Add a keyword-field check per page: `primary_keyword`, `secondary_keywords`, language and search intent must be present in the content record before generation.
- **[Content]** Assign one primary term per URL from this bank: bouyon musique, music bouyon, bouyon music, bouyon soca, bouyon gwada, dominica bouyon, bouyon riddim, bouyon playlist. Do not reuse the same primary on two competing pages.

## 9. Expand FAQs from generic coverage to entity-specific depth — [Both]

- Current state:
  - Artist pages: ours exactly **3 FAQs**, his exactly **4**.
  - Knowledge pages: ours mean **3.6**, his mean **2.3**.
  - Hubs: ours mean **4.0**, his mean **5.2**.
  - Sitewide FAQPage coverage: ours **99.0%**, his **54.7%**.
- Targets:
  - Artist: **5 FAQs**.
  - Knowledge: **5 FAQs** on core chapters, minimum 4 on supporting pages.
  - Hub: **6 FAQs**.
  - FAQPage coverage stays at **100%** for generated and hand-built pages.
- Artist FAQ set:
  1. Who is the artist and where are they from?
  2. What is their bouyon style or role?
  3. What are their key songs or releases?
  4. Who have they worked with?
  5. Where can the reader hear them or see them in the bouyon network?
- **[Generators]** Keep visible FAQ and FAQPage schema generated from the same array.
- **[Content]** Replace repeated fallback answers with artist-specific and page-specific facts.

## 10. Complete Article and Breadcrumb schema on knowledge and hub pages — [Generators]

- Current state:
  - Sampled knowledge `Article` coverage: ours **25.0%**, his **8.3%**.
  - Sitewide `Article` pages: ours **10**, his **22**.
  - Sampled hub `BreadcrumbList`: ours **66.7%**, his **83.3%**.
  - Sitewide `BreadcrumbList`: ours **95.1%**, his **67.0%**.
- Targets:
  - `Article` on **100%** of chapter, guide, versus, history and explainer pages.
  - `BreadcrumbList` on **100%** of all indexable pages, including home, hubs, FAQ and hand-built pages.
  - Every `Article` carries `headline`, `description`, `author`, `publisher`, `datePublished`, `dateModified`, `mainEntityOfPage` and `image` once page images exist.
- This is a generator/template fix first; content modules should only supply the dates and headline data.

## 11. Add real page images and beat his alt quality, not his icon count — [Both]

- Current state: our indexable pages contain **0 `<img>` elements**. His artist sample averages **158.3 images**, but only **3.2%** have non-empty alt; most are repeated streaming icons and release thumbnails.
- Targets:
  - Artist page: **1 primary portrait or cleared artist image + 1-3 supporting images** where rights and files exist.
  - Knowledge page: **2-4 relevant images** on core chapters.
  - Hub: a real image on each featured card, not on every directory row if that would slow the page.
  - Content-image alt coverage: **100%** with descriptive alt text naming the artist/topic and bouyon context.
  - Decorative icons: `alt=""` and kept out of the content-image count.
  - Add `ImageObject` in the page graph and a page-specific `og:image` where a cleared image exists.
- **[Generators]** Add responsive image markup, width/height, lazy loading below the first image and alt-text validation.
- **[Content]** Use only the cleared Bouyon Shattaz library or licensed/owned images. Do not copy his images.

## 12. Rebuild country and artist hubs as 2,000-word linked dossiers — [Content]

- Current sampled hub median: his **1,652 words**, ours **1,366 words**.
- Targets for `artistes-dominique`, `artistes-guadeloupe`, `artistes-martinique` and their EN mirrors:
  - **2,000-2,400 words**.
  - 8-10 H2 sections: origin, sound, key bands, solo artists, producers, women, carnival/WCMF, current wave, playlists, FAQ.
  - Every profiled artist linked once in a card and once in prose where natural.
  - Links to the relevant branch pages: bouyon gwada, bouyon soca, Wrecketeng/reketeng history, Dennery Segment where relevant, shatta where relevant.
  - 6 FAQs and an `ItemList` covering the full card set.

## 13. Cap and sharpen meta descriptions — [Generators]

- Current state: both sites have 100% meta description presence. Our sampled medians are already strong: artist **146 chars**, knowledge **150**, hub **147**. His artist median is only **119.5**.
- Problem: our sitewide maximum is **205 chars**, so a minority of descriptions are too long and will be truncated or rewritten.
- Target: **145-160 characters** on every page, hard validation range **140-165**.
- Formula:
  - Primary keyword or artist/topic in the first 90 characters.
  - One concrete differentiator: origin, date, signature track, festival, method or Dominica angle.
  - No keyword repetition beyond one exact primary phrase and one natural variant.
- **[Generators]** Fail or warn on missing, duplicate or out-of-range descriptions.

## 14. Close the bouyon gwada first-100 gap — [Content]

- Current state: **bouyon gwada** appears in the first 100 words on **69 of his pages (9.2%)** and **17 of ours (8.3%)**, while we lead him in title and H1 placement.
- Targets:
  - First-100 coverage: **15%+ of indexable pages** as the library grows, driven by real Guadeloupe artist profiles and Gwada chapters, not repeated boilerplate.
  - Every Guadeloupe artist profile intro must name bouyon gwada naturally in the first 100 words when that is the artist's actual lane.
  - Every Gwada chapter and hub must use the phrase in title, intro and one H2.
  - Build the Gwada artist set before trying to raise the percentage; the percentage should follow real coverage.

## 15. Give music bouyon a deliberate landing pattern — [Both]

- Current state: neither site has **music bouyon** in a title or H1. Ours has it in the first 100 words on 1 page; his on 2 pages.
- Targets:
  - One FR landing page or homepage section with **music bouyon** in the H1 subtitle and first 100 words.
  - One FR explainer with **music bouyon** in the title if search intent is kept separate from the canonical **bouyon musique** homepage; otherwise keep the homepage canonical and put the exact phrase in its H1/intro/FAQ to avoid creating two competing pages.
  - EN pages should not be forced into the French word order; EN targets **bouyon music** instead.
- **[Generators]** Add language-intent mapping so FR and EN mirrors do not blindly swap word order.

## 16. Consolidate or expand glossary and definition pages — [Content]

- Current state: his knowledge sample includes a **100-word** glossary page, showing his own weak point. Our older topic layer has the same risk at 500-900 words.
- Rule:
  - A standalone term page must reach **600-900 words** with definition, origin, sound traits, 3-5 named examples, related terms and 8-12 internal links.
  - If the term cannot support 600 verified words, fold it into a master glossary page with anchors instead of publishing a thin standalone page.
- Priority terms: riddim, sewo, jing ping, lapo kabwit, chanté mas, bouyon-muffin, Wrecketeng, Dennery Segment, shatta, jump up.

## 17. Add song-story pages that feed recordings, artists and playlists — [Content]

- His profile strength is reinforced by release-level pages and discography entries. Our current `MusicRecording` count is too low partly because the song layer is thin.
- Targets:
  - Each priority song page: **1,200-1,800 words**.
  - Schema: `MusicRecording` plus `VideoObject` when an official or owned embed is used.
  - Links: artist profile, producer profile, playlist page, relevant branch/chapter and 2 related songs.
  - No lyrics beyond a short fragment; story, credits, release context and reception only from verified sources.
- Start with the Smokiller flips already in the queue: Players, Nothing Into Something, Vulnerability, Heaven Baby and Throw Dat.

## 18. Add generator validation so the wins do not regress — [Generators]

Add a build-time report that fails or warns when any generated page has:

- Duplicate title, H1 or meta description.
- Title outside **45-65 chars** without an explicit exception.
- Meta description outside **140-165 chars**.
- Word count below the page-type floor.
- Fewer internal links than the page-type floor.
- Missing `FAQPage`, `BreadcrumbList`, `ProfilePage` or `Article` where the page type requires it.
- A `MusicRecording` with an unverified or empty required field.
- A content image with empty alt, or a decorative image incorrectly marked as content.
- A primary keyword missing from title, first 100 words or meta description.

This validation belongs in the generator layer, not in manual review.

---

## Bottom line

We do not need to imitate TIITII NBA page for page. The audit shows a narrower and more winnable fight:

- **Protect our current wins:** 100% unique titles, 99% FAQPage coverage, 95.1% breadcrumb coverage, stronger meta descriptions and better exact-keyword rates on most money terms.
- **Attack his structural wins:** profile count, discography schema, hub directory depth, internal links and images.
- **Exploit his weaknesses:** 87 duplicate-title instances, only 54.7% FAQPage coverage, 4.8% image alt coverage, many short news/glossary pages and artist descriptions that often omit the word bouyon.

If the first six fixes are executed properly, our pages will not merely be longer. They will be deeper where Google can measure it: entities, recordings, linked directories, complete schema and money-keyword placement, while keeping the Dominica origin angle he cannot credibly copy.
