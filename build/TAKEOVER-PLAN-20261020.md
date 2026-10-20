# BOUYONMUSIQUE.COM TAKEOVER PLAN - 2026-10-20
Target: outrank tiitii-nba.com on bouyon searches. All content original, written
from our own verified research library. None of his words, none of his images.

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
