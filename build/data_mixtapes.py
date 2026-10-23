"""Mixtapes (BOU-3200): Smokiller's published mixes, one page each, rendered by editorial.py.

Sources, read on 2026-10-23:
- The YouTube watch pages (title, upload date, duration, chapters, channel), fetched with yt-dlp.
- Playlist membership: /home/nxusdev/smokiller-live-site/content/youtube-channel-2026-10-23.json.
- Credits of Smokiller's own uploads: smokiller.com release pages (content/releases.json, BOU-3199).

upload_date is the YouTube upload timestamp (yt-dlp "timestamp", UTC).
Track tuples: (start in seconds, chapter title exactly as on YouTube, [artist profile slugs on this site],
smokiller.com page or None). Only link a profile when the profile is the same artist the chapter names.
Do not add years, countries or credits that the chapter titles and the sources above do not give.
"""

SMOKILLER_CHANNEL = "https://www.youtube.com/@smo.killer"

PL_MIX_2026 = ("Bouyon Mix 2026 - Best Bouyon DJ Mixes (Nonstop Bouyon Music)", "PLB1axoRydQre_2MEDDGaRUNYTbZkAOt7j")
PL_MUSIC_2026 = ("Bouyon Music 2026 - Best New Bouyon Songs (Dominica Bouyon Hits)", "PLB1axoRydQreXaKD2wlZ5IHJmNmoTWEEd")
PL_OLD_SCHOOL = ("Old School Bouyon Classics - WCK, Asa Bantan & Dominica Bouyon Hits", "PLB1axoRydQreAzi_rTjxy5yOYfoe32myP")

MIXTAPES = [
    {
        "slug": "mixtapes/bouyon-music-2026-mix-vol-1.html",
        "nav": "Bouyon Music 2026 Mix Vol. 1",
        "title": "Bouyon Music 2026 Mix Vol. 1 : tracklist de la mixtape de Smokiller",
        "h1": "Bouyon Music 2026 Mix Vol. 1, la mixtape de Smokiller",
        "desc": "Bouyon Music 2026 Mix Vol. 1 : 20 titres en 41 minutes, mixés par Smokiller. Tracklist minutée, Trilla-G, J Lion, Khallion, DOVA, Reo et Téhilah.",
        "date_published": "2026-10-23",
        "video_id": "82ubbjfYbak",
        "youtube_title": "Bouyon Music 2026 Mix 🇩🇲 Best New Bouyon Songs Vol. 1 | Trilla-G, J Lion, Tipsy, Khallion, DOVA",
        "upload_date": "2026-10-17T07:33:45+00:00",
        "duration": 2518,
        "related": ["bouyon-mix.html", "bouyon-music-2026.html", "nouveautes-bouyon-2026.html", "trilla-g.html"],
        "playlists": [PL_MIX_2026, PL_MUSIC_2026],
        "intro": "Bouyon Music 2026 Mix Vol. 1 est une mixtape de 41 minutes que Smokiller a publiée sur sa chaîne YouTube le 17 octobre 2026. Ses 20 chapitres enchaînent les titres sans coupure, et la description de la vidéo la présente comme mixée par Smokiller pour Bouyon Shattaz.",
        "sections": [
            ("Les artistes de la mixtape", [
                "Trilla-G est le nom qui revient le plus : quatre chapitres sur vingt, avec « Action », « Hennessy and Malibu », « Take Me As I Am » et « De Other Man », ce dernier crédité à Shelly, Trilla-G et Unstoppable Shax. La mixtape passe aussi par J Lion avec « Take Another Man », par Khallion avec « Bend Down », où Green Apple est invité, par DOVA avec « EARTHQUAKE » et par Slyme Hoyss avec « Back & Forth ».",
                "Le dernier chapitre, à 37 minutes 02, est « La Vie Doux », crédité à Reo et Téhilah. Plus tôt, à 12 minutes 10, « Pull D Pin » réunit Machel Montano, Skinny Fabulous, Lil Natty et Thunda, et « CAPITAL » de Mical Teja et Patrice Roberts arrive à 23 minutes 11.",
            ]),
            ("Les titres de la chaîne de Smokiller", [
                "Quatre chapitres correspondent à des titres publiés sur la chaîne de Smokiller. Le Time Skip Riddim arrive en deuxième position, juste après « Unstick », puis vient le Bouyon Shattaz anthem, publié par Smokiller le 15 septembre 2026. « Tipsy - [MadameZelle] » est le Tipsy Riddim de MadameZelle, que la page Bandcamp du titre crédite à Smokiller à la production. Le RnBouyon Instrumental, dont Smokiller signe aussi la production selon la description d’une de ses vidéos, arrive à 25 minutes 23.",
                "Les pages de smokiller.com liées dans la tracklist donnent pour chacun de ces titres la date de mise en ligne et la source de chaque crédit. Quand une mise en ligne ne nomme pas de producteur, comme le Time Skip Riddim, cette page n’en ajoute pas.",
            ]),
            ("Où écouter la mixtape", [
                "La vidéo est publique sur la chaîne YouTube de Smokiller. Elle figure dans deux playlists de la chaîne : Bouyon Mix 2026, qui rassemble les mixes, et Bouyon Music 2026, qui suit les nouveaux titres bouyon. Les titres sont repris ici tels qu’ils apparaissent dans les chapitres de la vidéo, sans correction d’orthographe.",
            ]),
        ],
        "tracks": [
            (0, "Unstick ft Fifin X Wotlis", [], None),
            (115, "Time Skip Riddim", [], "https://smokiller.com/riddims/time-skip-riddim"),
            (165, "Bouyon Shattaz anthem", [], "https://smokiller.com/releases/bouyon-shattaz-anthem"),
            (280, "KTB- Come Ova", [], None),
            (393, "J Lion - Take Another Man", ["j-lion.html"], None),
            (526, "IDFWU Riddim", [], None),
            (658, "Tipsy - [MadameZelle]", [], "https://smokiller.com/riddims/tipsy-riddim"),
            (730, "Machel Montano, Skinny Fabulous, Lil Natty & Thunda - Pull D Pin", ["machel-montano.html", "skinny-fabulous.html"], None),
            (861, "Trilla-G - Action", ["trilla-g.html"], None),
            (993, "Trilla-G - Hennessy and Malibu", ["trilla-g.html"], None),
            (1125, "Shelly x Trilla-G x Unstoppable Shax - De Other Man", ["shelly.html", "trilla-g.html", "unstoppable-shax.html"], None),
            (1258, "Trilla-G - Take Me As I Am", ["trilla-g.html"], None),
            (1391, "Mical Teja x Patrice Roberts - CAPITAL", [], None),
            (1523, "RnBouyon Instrumental", [], "https://smokiller.com/riddims/rnbouyon"),
            (1584, "Khallion - Bend Down ft Green Apple", ["khallion.html"], None),
            (1716, "OG Park & Rum Lawd - Whale Fu See (Whale Oil Riddim)", [], None),
            (1848, "DOVA - EARTHQUAKE", ["dova.html"], None),
            (1980, "Slyme Hoyss-Back & Forth", ["slyme-hoyss.html"], None),
            (2112, "DPENG FT SOCA INFERNO-SECRET BAY", [], None),
            (2222, "Reo x Téhilah - La Vie Doux", ["reo.html", "tehilah.html"], None),
        ],
    },
    {
        "slug": "mixtapes/old-school-bouyon-mix.html",
        "nav": "Old School Bouyon Mix",
        "title": "Old School Bouyon Mix : tracklist de la mixtape de Smokiller",
        "h1": "Old School Bouyon Mix, la mixtape des classiques de Smokiller",
        "desc": "Old School Bouyon Mix : 21 titres en 46 minutes, mixés par Smokiller. Tracklist minutée, d’Esclav, WCK, Triple Kay et XS Groove à Efex et Energy Band.",
        "date_published": "2026-10-23",
        "video_id": "fVMslUhYIYU",
        "youtube_title": "Old School Bouyon Mix 🇩🇲 Best Dominica Bouyon Classics Nonstop | WCK, Esclav, Triple Kay, Efex",
        "upload_date": "2026-10-17T06:23:59+00:00",
        "duration": 2762,
        "related": ["old-school-bouyon.html", "bouyon-mix.html", "wck.html", "tk-international.html"],
        "playlists": [PL_OLD_SCHOOL, PL_MIX_2026],
        "intro": "Old School Bouyon Mix est une mixtape de 46 minutes que Smokiller a publiée sur sa chaîne YouTube le 17 octobre 2026, le même jour que Bouyon Music 2026 Mix Vol. 1. Ses 21 chapitres partent de deux mises en ligne de Smokiller, puis enchaînent sans coupure 19 titres que les chapitres classent en bouyon, d’Esclav à WCK.",
        "sections": [
            ("Les artistes de la mixtape", [
                "Esclav est le groupe le plus présent, avec quatre chapitres : « No Ugly Ting », « Appreciation », « Splashington » et « Sortir Descande ». Triple Kay y joue « Please », XS Groove « Lights in the Moon » et WCK « 2Way Switch ». Les autres chapitres sont signés Machine Creole, S.O.S Band, Royalty Band, Virtual Band, Connection Band, Jawbreakerz, Impromptu Band, Era Squad, Look Us Band, Efex, Nursery Krew et Energy Band.",
                "Chaque chapitre porte une année entre parenthèses. Selon ces années, le titre le plus ancien est « Hurricane » d’Efex, en 1998, et le plus récent « Totally » de Royalty Band, en 2023. Ces années sont celles des chapitres de la vidéo : cette page ne les a pas vérifiées titre par titre.",
            ]),
            ("Les titres de la chaîne de Smokiller", [
                "La mixtape s’ouvre sur le Bouyon Shattaz anthem, publié par Smokiller le 15 septembre 2026, puis passe au Time Skip Riddim, mis en ligne sur sa chaîne le 31 janvier 2026 sous le titre « Time Skip Riddim [BOUYON2026] ». Leurs pages sur smokiller.com sont liées dans la tracklist.",
            ]),
            ("Où écouter la mixtape", [
                "La vidéo est publique sur la chaîne YouTube de Smokiller. Elle figure dans deux playlists de la chaîne : Old School Bouyon Classics et Bouyon Mix 2026. Les titres sont repris ici tels qu’ils apparaissent dans les chapitres de la vidéo, sans correction d’orthographe.",
            ]),
        ],
        "tracks": [
            (0, "Bouyon Shattaz anthem", [], "https://smokiller.com/releases/bouyon-shattaz-anthem"),
            (115, "Time Skip Riddim [BOUYON2026]", [], "https://smokiller.com/riddims/time-skip-riddim"),
            (152, "Machine Creole - No Rhythm Box (Bouyon 2010)", [], None),
            (266, "Esclav - No Ugly Ting (Bouyon 2007)", [], None),
            (390, "S.O.S Band - Up to the Time (Bouyon 2010)", [], None),
            (511, "Esclav - Appreciation (Bouyon 2007)", [], None),
            (633, "Royalty Band - Totally (Bouyon 2023)", [], None),
            (694, "Virtual Band - On and On (Bouyon 2016)", [], None),
            (815, "Esclav - Splashington (Bouyon 2007)", [], None),
            (937, "Connection Band - Mad Sick (Bouyon 2005)", [], None),
            (1061, "Jawbreakerz - Move It Like A Snake (Bouyon 2006)", [], None),
            (1186, "Triple Kay - Please (Bouyon 2008)", ["tk-international.html"], None),
            (1310, "Impromptu Band - Point Dem Out (Bouyon 2008)", [], None),
            (1433, "XS Groove - Lights in the Moon (Bouyon 2008)", ["xs-groove.html"], None),
            (1555, "Esclav - Sortir Descande (Bouyon 2008)", [], None),
            (1677, "Era Squad - Medley (Bouyon 2006)", [], None),
            (1800, "WCK - 2Way Switch (Bouyon 2008)", ["wck.html"], None),
            (1926, "Look Us Band - We Ready (Bouyon 2001)", [], None),
            (2050, "Efex - Hurricane (Bouyon 1998)", [], None),
            (2175, "Nursery Krew - Blue Blue (Bouyon 2008)", [], None),
            (2298, "Energy Band - Medley (Bouyon 2006)", [], None),
        ],
    },
]
