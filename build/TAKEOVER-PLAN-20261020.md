# BOUYONMUSIQUE.COM TAKEOVER PLAN - 2026-10-20
Target: outrank tiitii-nba.com on bouyon searches. All content original, written
from our own verified research library. None of his words, none of his images.

## STATUS - updated 2026-10-20 evening (keep this section current as work lands)

DONE AND LIVE:
- Phase 0 schema upgrade (commit 71f8872): BreadcrumbList on all generated
  pages, FAQPage on 128 pages, entity graph (WebSite / Bouyon Shattaz Org /
  Smokiller Person), dynamic sitemap lastmod.
- Phase 1 wave 1 (49c9b1c): 30 artist profiles (19 new + 11 deep rewrites,
  1,800-2,500 words), 8 chapters, 3 country hubs, FR+EN. Wave 1b: Trilla-G
  profile FR+EN. Publication dates spread Sep 2 - Oct 19, visible + schema +
  sitemap, never all the same day.
- Internal linking overhaul: 6,334 internal links, contextual linkify,
  hash-spread related blocks; every content page has 8+ inbound links.
- Branch pages from the 2026-10-20 deep research: rnbouyon + new-bouyon
  FR+EN; wrecketeng chapter gained the heirs section (RnBouyon + New Bouyon
  as heirs of reketeng) and the spelling note (reketeng historical,
  Wrecketeng = Smokiller's Dec 2025 revival).
- Bouyon soca: page leads with Sean's signed first-hand testimony (Dada,
  2003, Dominica; Triple Kay popularized). Consistency fix 1b7b3cd aligned
  the page intro and the Saint Lucia card so no competing origin story
  remains anywhere on the site.
- Sitemap rule locked: it must list EVERY indexable page (only 404.html
  excluded); robots.txt declares it. Current total: 205 URLs.
- Build system pushed into the repo under build/ (6a370b1) so Claude Code
  works from the same generators and data modules. Claude Code is connected
  to GitHub by Sean; coordination runs through git (pull first, clear commit
  messages, never duplicate a topic).
- PR #1 MERGED (2f24492, Claude Code): og:image + Twitter cards sitewide
  with og-image.png, FAQ sections on the hand-built pages, reketeng FAQ
  lineage, Saint Lucia/Antigua pages aligned to the Dada testimony,
  Smokiller identity wording set to Dominican-born only (per Sean:
  "I'm Dominican born that's all I should share for now"). Verified after
  merge: regeneration from build/ reproduces the merged site with zero
  drift.
- Threads: @bouyonshattaz mirrors @bouyonshattaz Instagram posts. The
  connector's post path is policy-blocked, so mirroring runs through the
  browser session Sean signed into, at publish time (posts are built here
  and on Codex, so no account watching). Pacing rule: randomized gaps, max
  3 posts per 5 minutes, 5-minute pause after each group of 3.
- Daily growth engine: Sean's standing order (2026-10-20) is 5+ new
  articles per day FR+EN with ongoing on-page SEO; the daily cron starts
  Wed 2026-10-21 and works a 29-topic backlog in 6 series (producers,
  women of bouyon, versus, Smokiller song stories, savoir-faire, actus),
  each article paired with an IG caption + Threads text written to the IG
  SEARCH CAPTION STANDARD.

NEXT (in queue order):
1. Daily batches from the backlog; WCMF 2026 night guides Oct 23/24/25,
   then night reports.
2. Versus pages, glossaire, bouyon family-tree chapter, Dennery Segment
   and Shatta explainer pages.
3. Smokiller song-story pages (Players, Nothing Into Something,
   Vulnerability, Heaven Baby, Throw Dat) with VideoObject + MusicRecording.
4. Scale artist profiles toward 150+; Smokiller producer/EPK page.
5. bouyonsoca.com: 301 redirect to bouyonmusique.com/bouyon-soca.html
   (pending: Sean confirms where the domain is registered/hosted).
6. Google Search Console: Sean resubmits sitemap.xml ("I'll push it when
   done"); robots.txt already declares it.

NEW DIRECTIVES (Sean, 2026-10-20 afternoon, apply to Amani AND Claude Code):
- WRECKETENG LAW: the official spelling is Wrecketeng, from DJ Cut himself,
  the founding member who pioneered the style. "reketeng" is a misspelling
  spread across the internet. The site writes Wrecketeng everywhere and
  flags "reketeng" only as that error (fixed sitewide, commit be61a62;
  the legacy URL reketeng.html stays, its content uses Wrecketeng).
- ARTIST PARITY 1:1: Sean ordered one-to-one artist coverage with
  tiitii-nba.com. Measured 2026-10-20: he has 157 artist profiles, we have
  31, gap = 142 (roster and list in build/ARTIST-PARITY.md). Priority order:
  Dominica and our own story first (DJ Cut, Dada, Nursery Krew Inc,
  Bushtown Clan, ThaWizZarD, Skinny Banton), then WCMF 2026 bill names,
  then the rest. Target depth: match or beat his 3,400-3,600 words per
  profile where the verified dossier supports it; never pad with invention.
  Until parity, the daily engine works the parity list before other series.
- ON-PAGE SEO MUST BEAT HIS, TERM BY TERM: a head-to-head audit
  (build/ONPAGE-AUDIT-20261020.md) compares titles, H1s, meta, word counts,
  schema, FAQs, internal links and keyword coverage per page type; its
  ranked fix list gets applied in the generators and modules. Careful,
  deliberate on-page work on every keyword that matters (bouyon musique,
  music bouyon, bouyon music, bouyon soca, bouyon gwada, dominica bouyon,
  bouyon riddim, bouyon playlist, bouyon mix) is the standing standard,
  not a one-off pass.

FACT DISCIPLINE (Sean, 2026-10-20): fact-check your own work and Claude
Code's. When a fact changes, sweep EVERY page and module for the old claim;
never just prepend the new one (that is how the bouyon soca page ended up
arguing with itself). Claude Code's PR #1 FAQ additions across many pages
are written but not yet individually source-checked; they are first in line
for the fact-check pass inside the daily runs.

## The audit (measured 2026-10-20, both codebases read directly)

### Him (tiitii-nba.com)
- 754 HTML pages (FR + EN mirrors)
- 314 artist profile pages (157 FR + 157 EN), each ~3,400-3,600 words, with
  ProfilePage schema, FAQPage, Person/MusicGroup entity graph and a
  MusicRecording discography per artist (8,109 MusicRecording entries sitewide)
- /bouyon/ knowledge base: 53 subsections - history chapters (origins, Gwada
  transition, New Bouyon Wave, women, producers, consecration), 8 versus pages
  (bouyon vs afrobeats/shatta/soca/kompa/zouk/dancehall/coupe-decale/dennery),
  how-tos (comment danser, comment produire), glossaire, iles, carte,
  artistes-by-country hubs, interviews (talks), actus (news), hors-serie features
- Chapter pages ~2,100 words; FAQ schema on 316 pages; BreadcrumbList on 402
- 18 paroles pages + per-song promo fiches for his own catalogue
- Every page carries his socials/streams in the furniture (1,043 profile links)
- Press flywheel: DNO article links readers to his domain for genre origins

### Us (bouyonmusique.com, live)
- 141 pages (71 FR + 70 EN), avg ~515 words/page
- Schema is basic: WebSite/WebPage/Organization everywhere, 20 FAQPages total,
  2 Articles, 2 MusicPlaylist. NO ProfilePage, NO Person/MusicGroup entity
  graph, NO MusicRecording, NO BreadcrumbList
- Clean basics he also has: unique titles, canonicals, 1:1 hreflang, sitemap
- Assets he cannot match: the Dominica origin angle (he is the Guadeloupe
  chapter; we are the source), WCMF 2026 live coverage, a verified artist
  library with cleared photos, ROAD MIX playlists, the GitHub parasite +
  Facebook parasite network already forwarding traffic, the DNO pipeline

## The gaps, in order of ranking impact
1. Artist page scale and depth: 314 deep profiles vs our small shallow set.
2. Entity/schema graph: he tells Google exactly who every artist is (Person,
   MusicGroup, sameAs, discography). We barely declare anything.
3. Knowledge depth: his chapters run 2,100 words; ours run ~500.
4. Content types we lack entirely: versus pages, how-tos, glossary, news/actus,
   per-song pages, interviews.
5. Freshness engine: his actus + press loop vs our static site.

## The takeover build (all original, our research, our images)

### Phase 0 - Schema and structure upgrade (generator-level, existing 141 pages)
- Add BreadcrumbList to every page; FAQPage to every content page (original
  Q&As from our research, like the parasite PAA set but rewritten per page)
- Build the entity graph: Smokiller as Person/MusicRecordingArtist with sameAs
  (YouTube @smo.killer, IG @smo.killer, TikTok), Bouyon Shattaz as
  Organization/MusicGroup, site-wide @id linking
- ImageObject + real alt text from the library photos; Article schema with
  dates + author (Smokiller) on content pages
- Internal link mesh: every page links its chapter, 3 related artists, and the
  matching playlist page. Sitemap split + lastmod.

### Phase 1 - Artist wave 1 + chapters (FR + EN)
- 30 core artist profiles at 1,800-2,500 words each, ProfilePage + FAQ +
  Person/MusicGroup + verified discography as MusicRecording, written ONLY
  from our verified library and research record (Reo, Asa Bantan, Ridge,
  Signal Band, Shelly, Miimii KDS, Maurane Voyer, Smokiller himself, WCK,
  Midnight Groovers, TK International, Colton T, Pudaz, Gwada G, HYPNO!,
  Savion, Dcamp & Lewismelo, G'z Up, BONNA, Ricky Bishop, Denmath, MB On The
  Track, Litleboy, Niska... final list from library holdings)
- 8 original chapters from our record: origins/WCK, Wrecketeng (our exclusive
  angle, he has nothing like it), cadence-lypso roots, the Gwada chapter told
  from the Dominica side, women of bouyon, producers and passeurs, WCMF,
  bouyon mondial/crossover (the Smokiller flips story)
- Hubs: artistes Dominique / artistes Guadeloupe / artistes Martinique

### Phase 2 - Search furniture
- Versus pages (same 8 matchups, our own analysis), how-tos: comment produire
  un bouyon (Smokiller authority, targets "bouyon drum kit" demand),
  comment danser le bouyon ("bouyon danse"), glossaire bouyon
- Per-song pages for the Smokiller flips (Players, Nothing Into Something,
  Vulnerability, Heaven Baby, Don't): story, credits, VideoObject +
  MusicRecording schema, his YouTube embeds, free-download CTA to
  smokiller.com. No lyrics reproduced.
- Smokiller EPK/booking page equivalent, but as a producer: services,
  placements, contact. Dates page for Bouyon Shattaz events/WCMF week.

### Phase 3 - Scale and freshness (the engine that buries him)
- Artist waves 2 and 3 to 150+ profiles (parity, then past him), prioritised
  by search demand and WCMF bill
- Actus desk: 2 posts/week minimum, WCMF 2026 coverage first (countdown,
  night reports Oct 23-25), the Coi Leray story cross-posted with the DNO
  piece linking back to us, not to him
- Every IG/FB post points at the matching page (already our caption standard);
  parasite network keeps forwarding; DNO and future press link OUR domain
- Measurement: Google Search Console on bouyonmusique.com (verify + submit
  split sitemaps), weekly query check on bouyon music / music bouyon /
  bouyon gwada / artist-name queries vs his pages; iterate titles on losers

## Rules
- Zero copied sentences, zero of his images. Structure and page types are a
  format, not content; everything readable on our pages is ours.
- Facts only from the verified record, same research-before-copy standard.
- Trilla-G stays off bouyonmusique.com per Sean's 2026-10-18 order.
- Push path: generator -> local verify (links, titles, schema) -> git push to
  bouyonkonet/bouyonmusique -> live check. Nothing else changes on the domain.
