# -*- coding: utf-8 -*-
"""Island of every artist profile. Single source for the island pages, the roster on each
island hub, the island line on every profile and the flags in the A to Z list.

Two kinds of link, never mixed:
  FROM:  the profile itself states the artist's origin (born, from, raised, a band from).
  SCENE: the profile only places the artist in that island's circuit, base or release
         billing ("Barbados Bouyon 2026", "Vincy Bouyon", "anchored in the Guadeloupe scene").
A profile with neither stays out of both and is listed as "origin not stated". Never guess:
add a slug here only after reading the sentence in the profile that supports it.
Checked against every profile lead and meta description on 2026-10-24.
"""

ISLANDS = [
 # code, flag, EN name, FR name, anchor, EN hub, FR hub, EN place page, FR place page
 ('dm', '🇩🇲', 'Dominica', 'Dominique', 'dominica', '/en/artists-dominica.html', '/artistes-dominique.html', '/en/bouyon-dominica.html', '/bouyon-dominique.html'),
 ('gp', '🇬🇵', 'Guadeloupe', 'Guadeloupe', 'guadeloupe', '/en/artists-guadeloupe.html', '/artistes-guadeloupe.html', '/en/bouyon-guadeloupe.html', '/bouyon-guadeloupe.html'),
 ('mq', '🇲🇶', 'Martinique', 'Martinique', 'martinique', '/en/artists-martinique.html', '/artistes-martinique.html', '/en/bouyon-martinique.html', '/bouyon-martinique.html'),
 ('mf', '🇲🇫🇸🇽', 'Saint Martin / Sint Maarten', 'Saint-Martin / Sint Maarten', 'saint-martin', None, None, '/en/bouyon-saint-martin.html', '/bouyon-saint-martin.html'),
 ('lc', '🇱🇨', 'Saint Lucia', 'Sainte-Lucie', 'saint-lucia', None, None, '/en/bouyon-saint-lucia.html', '/bouyon-sainte-lucie.html'),
 ('ag', '🇦🇬', 'Antigua', 'Antigua', 'antigua', None, None, '/en/bouyon-antigua.html', '/bouyon-antigua.html'),
 ('bb', '🇧🇧', 'Barbados', 'Barbade', 'barbados', None, None, None, None),
 ('kn', '🇰🇳', 'Saint Kitts and Nevis', 'Saint-Christophe-et-Niévès', 'saint-kitts', None, None, None, None),
 ('vc', '🇻🇨', 'Saint Vincent and the Grenadines', 'Saint-Vincent-et-les-Grenadines', 'saint-vincent', None, None, None, None),
 ('gd', '🇬🇩', 'Grenada', 'Grenade', 'grenada', None, None, None, None),
 ('tt', '🇹🇹', 'Trinidad and Tobago', 'Trinité-et-Tobago', 'trinidad', None, None, None, None),
 ('jm', '🇯🇲', 'Jamaica', 'Jamaïque', 'jamaica', None, None, None, None),
 ('fr', '🇫🇷', 'France', 'France', 'france', None, None, '/en/bouyon-france.html', '/bouyon-france.html'),
 ('us', '🇺🇸', 'United States', 'États-Unis', 'united-states', None, None, None, None),
 ('ca', '🇨🇦', 'Canada', 'Canada', 'canada', None, None, None, None),
]

FROM = {
 'dm': """all-star-band asa-bantan avatar-omish benji bonna bushtown-clan carlyn-xp colton-t cornell-phillip cross-vibes-band
  dada daddy-chess derek-rah-peters dj-cut dj-flip-tha-boss dj-mj dj-taffy dj-wizz767 don-lash earlson-matthew ebony-empress
  edday explosive-band faithii first-serenade-band foxy-jael fr3eze gwada-g ignition-band keks-mafia kenny-g-dominica khallion
  killa-laurent klockerz-krew kwib-la-beats midnight-groovers mr-delly mr-gwada mystrie ncore nice nursery-krew-inc pa-pel
  pryhmex pudaz ras-b reo riddim-knockaz ridge rohie rsb rudy-rush shelly signal-band slyme-hoyss smokiller starsha sukie
  sweet-ticky tazzo-thaboss tehilah tk-international trilla-g trixzmigos unstoppable-shax wck""",
 'gp': """1t1 aknose arendi d0-production dj-leguste gaza-girls-crew holly-g jixels kevni lestef-kjf-boyz lms magistral-beats
  miimii-kds miky-ding-la pinpin-osp riddla shanika shashabim shazdown-mmw team-bwe-tou-sa tiitii-nba totally-spices yellow-gaza""",
 'mq': "blicassty maurane-voyer",
 'mf': "brg-hollywood d4a-nillio denmath tolly-boys youry-fleming",
 'lc': "lu-city motto",
 'vc': "magikal problem-child skinny-fabulous wetty-beatz",
 'gd': "jab-king vghn",
 'tt': "bunji-garlin lyrikal machel-montano nessa-preppy",
 'jm': "chronic-law kkrytical shawn-storm stalk-ashley",
 'fr': "alkpote denden kai-du-m niska teyma theodora",
 'ag': "ac-tafari claudette-peters",
 'us': "boston-chery major-lazer",
 'ca': "david-campana malko mopao-mumu",
}

SCENE = {
 'dm': """dernel-green dova dpeng effects-band fetty-mark freddy hussey poyzin r-b-m real-reel skinny-banton tha-wizzard triszy trixx zwady candy daddy-keyz dj-sleem dj-snow mv-on-de-keys noface-beatz go-fast""",
 'gp': """bilix binksdrick bismok corane-vincent dcamp dinho dj-demafidem dj-softee dj-tkrys doc-fix-dem doc-fix-it doc-j edday flw
  laka larose le-bluff le-rebelle hb-war lejuh letin-severine letin-sylia leyou lgc lunik ma6mo malcolm mr-boka riko suppa ted-la
  theomaa ti-locksee vj-ben weelow yu-mei""",
 'mf': "bernard-gumbs-wizito ebony-empress redpunchdrip general-pye sully-jacob",
 'lc': "imran-nerdy jayanti shemmy-j tallyboy",
 'ag': "king-low-rider louse-king ricardo-drue",
 'gd': "big-red-hd",
 'bb': "bajan-balotelli fiddy-ii jordan-english kas-matik quan-de-artist sharkie stella-billy",
 'kn': "daddy2sec",
 'vc': "dyonte jauwan-hadaway ktb og-park spyout stratvincybwoy superk",
 'fr': "dalibido-6dl tenslay",
 'us': "klassik-frescobar madamezelle",
}

# Wave 40 (2026-10-29)
FROM['dm'] += " king-dice"
FROM['lc'] += " freezy kisha-kay"
FROM['bb'] = FROM.get('bb', "") + " fadda-fox"
FROM['jm'] += " shanna-raymond"
FROM['kn'] = FROM.get('kn', "") + " shanna-raymond"
SCENE['gd'] += " blaka-dan"
SCENE['bb'] += " ian-stylez"
SCENE['vc'] += " shattah-ayow"
# Wave 41 (2026-10-29)
FROM['gp'] += " fowko mikty"
FROM['dm'] += " major-mystic supalyne"
FROM['tt'] += " college-boy-jesse"
FROM['vc'] += " caspa-g"
SCENE['vc'] += " kilogram"
SCENE['mq'] = SCENE.get('mq', "") + " mad-general"
SCENE['dm'] += " zone-rouge"
# Wave 42 (2026-10-29)
FROM['dm'] += " frank-white jcro"
FROM['ag'] += " kaution-band"
SCENE['vc'] += " redz"
# Wave 43 (2026-10-29)
FROM['jm'] += " mr-vegas"
FROM['dm'] += " deluxe-f"
FROM['mf'] += " sick-tonez"
SCENE['ag'] += " fucha-kid"
FROM = {k: v.split() for k, v in FROM.items()}
SCENE = {k: v.split() for k, v in SCENE.items()}

def links_for(slug):
    """[(code, 'from'|'scene')] for one profile slug (without .html)."""
    out = [(c, 'from') for c, l in FROM.items() if slug in l]
    out += [(c, 'scene') for c, l in SCENE.items() if slug in l and (c, 'from') not in out]
    order = [i[0] for i in ISLANDS]
    return sorted(out, key=lambda x: (x[1] != 'from', order.index(x[0])))
