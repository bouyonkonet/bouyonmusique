# -*- coding: utf-8 -*-
def place(slug, nav, title, desc, h1, intro, s1h, s1, s2h=None, s2=None, faq=None, **extra):
    secs = [(s1h, [s1])]
    if s2h: secs.append((s2h, [s2]))
    p = {"slug": slug, "cat": "Le bouyon par pays", "nav": nav, "title": title, "desc": desc,
         "h1": h1, "intro": intro, "sections": secs}
    if faq: p["faq"] = faq
    p.update(extra)
    return p

PAGES = [
place("bouyon-dominique.html", "Bouyon en Dominique",
"Bouyon en Dominique : le pays qui a créé le bouyon",
"Le bouyon en Dominique : Roseau, le carnaval Mas Domnik, WCK et les groupes originels. Le pays créateur du bouyon et le coeur de la music bouyon mondiale.",
"Bouyon en Dominique : là où tout a commencé",
"La Dominique est le pays du bouyon. C’est à Roseau, sa capitale, que WCK a créé le genre en 1988, et c’est dans ses villages et son carnaval que le son continue de vivre à l’état brut.",
"Roseau et le carnaval", "Le carnaval de la Dominique, le Mas Domnik, est la maison du bouyon : les groupes live et les sound systems y jouent les titres qui deviendront les classiques de l’année. Grand Bay, le village d’Asa Bantan, le Bouyon Boss, est l’un des hauts lieux de cette culture.",
"Une petite île, une invention mondiale", "Avec moins de 70 000 habitants dans son histoire moderne, la Dominique a inventé deux genres qui ont voyagé dans le monde entier : la cadence-lypso puis le bouyon. Défendre cette origine est le coeur du travail de Bouyon Shattaz et de ce site.", date_modified="2026-10-20", faq=[
  (
    "Dans quels pays le bouyon est-il populaire ?",
    "Né en Dominique, le bouyon est aujourd'hui central en Guadeloupe et en Martinique, où on l'appelle aussi jump up, et présent en France, à Sainte-Lucie, à Antigua, à Saint-Martin et dans la diaspora caribéenne, de New York à Londres, Toronto et Montréal. Son centre de gravité reste la Dominique, où il est la musique du carnaval depuis les années 1990.",
  ),
  (
    "Quel pays a créé le bouyon ?",
    "La Dominique. Le genre y est né à la fin des années 1980 : c'est à Roseau, la capitale de l'île, que le groupe WCK l'a créé en 1988. Le bouyon reste aujourd'hui le son du carnaval de Roseau, le Mas Domnik, où les groupes live et les sound systems lancent chaque année les futurs classiques.",
  ),
  (
    "Qui a créé le bouyon en Dominique ?",
    "Le bouyon a été créé par <a href=\"/wck.html\">WCK</a> (Windward Caribbean Kulture), un groupe formé à Roseau, la capitale de la Dominique, en 1988. WCK a fusionné la cadence-lypso et le jing ping avec des claviers électroniques et des boîtes à rythmes, donnant naissance au son que l'on appelle bouyon.",
  ),
  (
    "Où écouter du bouyon en Dominique ?",
    "Le meilleur endroit est le carnaval de la Dominique, le Mas Domnik, à Roseau : les groupes live et les sound systems y jouent les titres qui deviennent les classiques de l'année. Grand Bay, le village d'Asa Bantan, identifié comme le Bouyon Boss par Dominica Festivals, est aussi l'un des hauts lieux de la culture bouyon sur l'île.",
  ),
  (
    "Quels genres musicaux la Dominique a-t-elle inventés ?",
    "La Dominique a inventé deux genres qui ont voyagé dans le monde entier : la cadence-lypso, puis le bouyon, créé par WCK en 1988. C'est remarquable pour une île qui a compté moins de 70 000 habitants dans son histoire moderne, et c'est pourquoi ce site défend l'origine dominicaine du bouyon.",
  ),
  (
    "Le bouyon vient-il de la Dominique ou de la Guadeloupe ?",
    "De la Dominique. Le bouyon a été créé à Roseau en 1988 par WCK, puis il a traversé la mer vers la Guadeloupe grâce à la langue créole partagée. La Guadeloupe l'a dansé en jump up et en a tiré sa propre branche, le bouyon gwada. TIITII NBA, artiste guadeloupéen, dit en substance que le bouyon appartient à la Dominique et que la Guadeloupe en est le <a href=\"/gwada-vue-de-dominique.html\">deuxième chapitre</a>.",
  ),
  (
    "Quand a lieu le carnaval de la Dominique ?",
    "Le carnaval de la Dominique, le <a href=\"/mas-domnik.html\">Mas Domnik</a>, se tient chaque année à Roseau avant le carême, avec ses temps forts le lundi et le mardi gras, précédés du J'ouvert à l'aube, moment fort du bouyon et de la soca. Les fêtes et les sound systems des semaines précédentes lancent les titres bouyon de l'année.",
  ),
  (
    "Qu'est-ce que le World Creole Music Festival ?",
    "C'est le grand rendez-vous musical de la Dominique : trois nuits de musique créole au stade Windsor Park, à Roseau, chaque année en octobre, le mois de l'indépendance dominicaine. L'édition 2026 a lieu du 23 au 25 octobre, avec notamment Asa Bantan et Reo le samedi 24, selon les guides publiés. Voir le <a href=\"/world-creole-music-festival.html\">World Creole Music Festival</a>.",
  ),
  (
    "Qui sont les artistes bouyon de la Dominique aujourd'hui ?",
    "Parmi les noms suivis par ce site : Asa Bantan, de Grand Bay, largement surnommé le King of Bouyon, Reo, présenté comme le Prince of Bouyon par 13th Street Promotions, Ridge, Shelly, Signal Band et Trilla-G. Le genre garde aussi ses groupes fondateurs : WCK, Roots, Stems and Branches (RSB) et First Serenade. Voir les <a href=\"/artistes-dominique.html\">artistes bouyon de la Dominique</a>.",
  ),
  (
    "Quels styles de bouyon sont nés en Dominique ?",
    "Plusieurs. Dans les années 1990, quand les voix du bouyon s'ouvrent au dancehall et au ragga jamaïcains, naissent le bouyon-muffin et le <a href=\"/wrecketeng.html\">Wrecketeng</a>, bâti sur des mélodies samplées et des voix rap. En 2003, Dada lance le bouyon soca en Dominique, selon le témoignage de Smokiller. Le bouyon gwada, lui, est né de collaborations avec la Guadeloupe.",
  ),
  (
    "Reketeng ou Wrecketeng : quelle est la bonne orthographe ?",
    "Wrecketeng. C'est l'orthographe officielle, transmise par <a href=\"/dj-cut.html\">DJ Cut</a>, le pionnier du style en Dominique. La forme « reketeng », très répandue sur internet, est une faute d'orthographe. Le Wrecketeng désigne la pratique dominicaine qui reconstruit des enregistrements existants sur des instrumentaux bouyon, dans la lignée du bouyon-muffin, et il est cité comme une racine du bouyon moderne.",
  ),
  (
    "En quelle langue chante-t-on le bouyon en Dominique ?",
    "En kwéyòl, la langue créole de la Dominique, mélangé à l'anglais. Cette langue porte les appels, les blagues, les commentaires sociaux et l'énergie du chanté mas, comme celle du carnaval, dont le nom même, Mas Domnik, est créole. Le kwéyòl dominicain est proche des créoles voisins, ce qui a aidé le bouyon à voyager. Voir <a href=\"/bouyon-et-kweyol.html\">bouyon et kwéyòl</a>.",
  )
]),
place("bouyon-guadeloupe.html", "Bouyon en Guadeloupe",
"Bouyon en Guadeloupe : le bouyon gwada et le jump up",
"Le bouyon en Guadeloupe : appelé jump up, devenu bouyon gwada dans sa branche hardcore. Carnaval de Pointe-à-Pitre, DJ, producteurs et public Gwada du bouyon.",
"Bouyon en Guadeloupe : la deuxième maison du genre",
"La Guadeloupe est la deuxième maison du bouyon. L’île partage le créole avec la Dominique, et son public a adopté le son au point de créer sa propre branche : le bouyon gwada.",
"Du jump up au bouyon gwada", "Au carnaval et dans les fêtes, le public guadeloupéen appelle le bouyon jump up. Puis les musiciens de Gwada, en collaboration avec les Dominicains, durcissent le son : c’est la naissance du <a href=\"/bouyon-gwada.html\">bouyon gwada</a>, plus électronique et plus cru.",
"Un public qui fait les hits", "Les DJ et les pages bouyon de Guadeloupe jouent un rôle décisif : ce sont souvent leurs choix et leurs réseaux qui transforment un riddim en titre de carnaval, relayé ensuite vers la Martinique et Paris. Voir aussi <a href=\"/bouyon-paris.html\">le bouyon à Paris</a>.", date_modified="2026-10-20", faq=[
  (
    "Dans quels pays le bouyon est-il populaire ?",
    "Né en Dominique, le bouyon est aujourd'hui central en Guadeloupe et en Martinique, où le public l'appelle aussi jump up. Il est présent en France, à Sainte-Lucie, à Antigua, à Saint-Martin et dans la diaspora caribéenne, de New York à Londres, Toronto et Montréal.",
  ),
  (
    "Quel pays a créé le bouyon ?",
    "La Dominique. Le genre est né à Roseau à la fin des années 1980, quand le groupe WCK, formé en 1988, a fusionné la cadence-lypso avec le jing ping et les tambours traditionnels comme le lapo kabwit. Il reste le son du carnaval de Roseau, le Mas Domnik.",
  ),
  (
    "Qu'est-ce que le bouyon gwada ?",
    "Le bouyon gwada, aussi appelé hardcore bouyon, est la branche du bouyon née de collaborations entre musiciens de la Dominique et de la Guadeloupe. Plus dur, plus électronique et plus cru que le bouyon des groupes live, il pousse les boîtes à rythmes, les basses et les voix en créole guadeloupéen. Voir le <a href=\"/bouyon-gwada.html\">bouyon gwada</a>.",
  ),
  (
    "Comment appelle-t-on le bouyon en Guadeloupe ?",
    "En Guadeloupe, le public appelle le bouyon jump up, au carnaval comme dans les fêtes. Le mot désigne aussi la façon de danser le bouyon en sautant, devenue la signature des soirées gwada. Le son arrive de la Dominique voisine, porté par la langue créole partagée et les allers-retours des carnavals.",
  ),
  (
    "Quels artistes bouyon viennent de Guadeloupe ?",
    "Parmi les profils suivis par ce site : Miimii KDS, créditée sur « Pow Pow / Allo Doudou », certifié or par le SNEP, TIITII NBA, de Morne-à-l'Eau, dont « Kitty Kitty » a dépassé 1,65 million d'écoutes, et Ricky Bishop, d'origine guadeloupéenne et malgache, créateur du concept New Bouyon. Voir les <a href=\"/artistes-guadeloupe.html\">artistes bouyon de Guadeloupe</a>.",
  ),
  (
    "Le bouyon vient-il de la Guadeloupe ?",
    "Non, le bouyon vient de la Dominique, où WCK l'a créé à Roseau en 1988. La Guadeloupe ne l'a pas inventé : elle l'a reçu de la Dominique voisine, l'a fait sauter en jump up, puis l'a transformé en une scène à part entière, le bouyon gwada. La Dominique garde le crédit de créatrice, la Guadeloupe celui d'avoir donné au bouyon l'une de ses plus grandes scènes. Voir <a href=\"/gwada-vue-de-dominique.html\">Gwada vue de Dominique</a>.",
  ),
  (
    "Comment le bouyon est-il arrivé en Guadeloupe ?",
    "Par la langue créole partagée, les carnavals et les tournées. Le créole dominicain et celui de la Guadeloupe se comprennent, et le bouyon n'a pas eu besoin de traduction. Il s'est développé en Guadeloupe au contact des tournées de groupes dominicains comme WCK et Triple Kay, puis les collaborations entre musiciens des deux îles ont donné le bouyon gwada. Voir l'<a href=\"/histoire.html\">histoire du bouyon</a>.",
  ),
  (
    "Quel titre bouyon guadeloupéen a été certifié or ?",
    "« Pow Pow / Allo Doudou », de Niska, Litleboy LSBeats767 et la Guadeloupéenne Miimii KDS, a été certifié Single Or par le SNEP à 15 millions d'équivalents streams. Le nom de Litleboy LSBeats767 renvoie à l'indicatif 767 de la Dominique, ce qui fait de ce titre un pont entre les deux îles. Voir <a href=\"/miimii-kds.html\">Miimii KDS</a>.",
  ),
  (
    "Qui est TIITII NBA ?",
    "TIITII NBA est un artiste bouyon de Morne-à-l'Eau, en Guadeloupe. Son nom porte un programme : NBA signifie New Bouyon Age, la nouvelle ère du bouyon. Son titre « Kitty Kitty » a dépassé 1,65 million d'écoutes selon Dominica News Online, et il anime bouyonews, le média bouyon en français qui couvre l'actualité du genre pour la Guadeloupe, la Martinique et la France.",
  ),
  (
    "Quel label guadeloupéen a signé un artiste dominicain ?",
    "More Sewo, label guadeloupéen créé en 2007 par Arturo Bellot, a signé BONNA, artiste bouyon dominicain de La Plaine. Ce fait montre que le trafic entre les deux scènes va désormais dans les deux sens : un label de Gwada investit dans un talent de l'île d'origine du bouyon, pendant que la Dominique apporte l'origine, les artistes et le répertoire fondateur.",
  ),
  (
    "Le bouyon gwada et le jump up, est-ce la même chose ?",
    "Pas tout à fait. Jump up est le nom que les Antilles françaises donnent au bouyon venu de la Dominique en général, et à la façon de le danser en sautant. Le bouyon gwada est plus précis : c'est la branche hardcore née de collaborations entre la Dominique et la Guadeloupe, avec boîtes à rythmes, basses lourdes et voix en créole guadeloupéen. Voir la page <a href=\"/jump-up.html\">jump up</a>.",
  ),
  (
    "Quel drapeau représente la scène bouyon gwada ?",
    "Le drapeau local que les Guadeloupéens appellent le leur : des bandes vertes en haut et en bas, une bande rouge au milieu et une étoile jaune. Bouyon Shattaz l'utilise dans ses designs consacrés à la scène gwada, parce que c'est le signe que cette scène reconnaît elle-même, et non un symbole improvisé ou administratif.",
  ),
  (
    "Qu'est-ce que le New Bouyon de Ricky Bishop ?",
    "Le New Bouyon est le concept créé par Ricky Bishop, rappeur et ingénieur du son d'origine guadeloupéenne et malgache basé à Bordeaux : un bouyon mélangé à la trap et à la musique électronique. Il lui a donné forme en 2024 avec les EP #newbouyon et #sexybouyon. À ne pas confondre avec le New Bouyon Age de TIITII NBA. Voir <a href=\"/ricky-bishop.html\">Ricky Bishop</a>.",
  )
]),
place("bouyon-martinique.html", "Bouyon en Martinique",
"Bouyon en Martinique : le jump up de Fort-de-France",
"Le bouyon en Martinique : jump up au carnaval de Fort-de-France, public martiniquais, liens créoles avec la Dominique et la Guadeloupe, artistes et fêtes.",
"Bouyon en Martinique : le jump up au pays du zouk",
"La Martinique, terre du zouk, est aussi une terre de bouyon. Le public martiniquais connaît le genre sous le nom de jump up et le vit au carnaval comme dans les fêtes toute l’année.",
"Une histoire créole partagée", "Dominique, Guadeloupe et Martinique partagent la langue kwéyòl et des traditions de carnaval proches : chanté mas, groupes de rue, danses créoles. Le bouyon circule entre les trois îles depuis les années 1990, porté par les échanges de musiciens et de publics.",
"Des artistes qui font le pont", "Des collaborations comme Joli BB de Reo, artiste dominicain, avec Maurane Voyer, chanteuse martiniquaise, montrent le bouyon de 2026 à l’oeuvre : une création dominicaine, un pont martiniquais, un public des deux côtés de la mer. Voir la page <a href=\"/maurane-voyer.html\">Maurane Voyer</a>.", date_modified="2026-10-20", faq=[
  (
    "Comment appelle-t-on le bouyon en Martinique ?",
    "En Martinique, le bouyon est surtout appelé jump up. Le public martiniquais le vit sous ce nom au carnaval comme dans les fêtes toute l'année. Pour beaucoup d'Antillais, bouyon et jump up désignent le même son : la musique rapide venue de la Dominique qui fait sauter tout le monde. Voir la page <a href=\"/jump-up.html\">jump up</a>.",
  ),
  (
    "Quels artistes martiniquais font du bouyon ?",
    "La chanteuse martiniquaise Maurane Voyer est la figure la plus visible en 2026 : elle chante Joli BB avec Reo, artiste dominicain, un titre sorti le 9 octobre 2026 sur le label Mauve. Elle est aussi annoncée pour la première nuit du World Creole Music Festival 2026 à Roseau, le vendredi 23 octobre. Voir la page <a href=\"/maurane-voyer.html\">Maurane Voyer</a>.",
  ),
  (
    "Dans quels pays le bouyon est-il populaire ?",
    "Né en Dominique à la fin des années 1980, le bouyon est aujourd'hui central en Guadeloupe et en Martinique, où on l'appelle aussi jump up. Il est présent en France, à Sainte-Lucie, à Saint-Martin et dans la diaspora caribéenne, et circule entre la Dominique, la Guadeloupe et la Martinique depuis les années 1990.",
  ),
  (
    "Quel pays a créé le bouyon ?",
    "La Dominique. Le genre y est né à la fin des années 1980, lancé par le groupe WCK, formé en 1988 à Roseau, et il reste le son du carnaval de Roseau. La Martinique, qui partage avec la Dominique la langue kwéyòl et des traditions de carnaval proches, l'a adopté sous le nom de jump up.",
  ),
  (
    "Le shatta et le bouyon viennent-ils de la Martinique ?",
    "Le shatta, oui : c'est un sous-genre du dancehall né en Martinique, que ce site décrit comme la cousine martiniquaise du bouyon. Le bouyon, non : il est né en Dominique, créé par WCK à Roseau en 1988, et la Martinique l'a adopté sous le nom de jump up. Les deux scènes se croisent souvent, et le shatta bouyon les fusionne. Voir <a href=\"/bouyon-ou-shatta.html\">bouyon ou shatta</a>.",
  ),
  (
    "Quelle est la différence entre le zouk et le bouyon ?",
    "Le zouk vient de la Guadeloupe et de la Martinique : popularisé au début des années 1980 par des groupes comme Kassav, il est propre, dansant, romantique dans sa version zouk love. Le bouyon vient de la Dominique : plus rapide, plus brut, plus carnaval que salon. Le zouk fait même partie des ingrédients du bouyon. Voir <a href=\"/bouyon-ou-zouk.html\">bouyon ou zouk</a>.",
  ),
  (
    "Qui a écrit Joli BB de Reo et Maurane Voyer ?",
    "Joli BB est écrit par Maurane Voyer, Dario Yankey et Nicolas Lanclume. Dario Yankey est le vrai nom de <a href=\"/reo.html\">Reo</a>, l'artiste dominicain présenté comme le Prince of Bouyon par 13th Street Promotions. Le titre est sorti le 9 octobre 2026 sur le label Mauve : une chanteuse martiniquaise, un artiste de l'île source et une équipe d'écriture nommée.",
  ),
  (
    "Quels autres artistes martiniquais sont liés au bouyon ?",
    "Ce site signale aussi Koko Bwa, artiste martiniquais dont le premier single, « Tarif », est sorti en avril 2025 avec le producteur Denmath en featuring et Boutcha Bwa. Bouyon Shattaz a accepté de publier ce titre en octobre 2026. Le hub martiniquais du site grandit ainsi, profil vérifié après profil vérifié. Voir les <a href=\"/artistes-martinique.html\">artistes bouyon de Martinique</a>.",
  ),
  (
    "Où danser le bouyon en Martinique ?",
    "Au carnaval de la Martinique, où le jump up est la bande-son des groupes à peaux, des déboulés et des fêtes de rue, et dans les fêtes toute l'année. Le bouyon s'y danse en sautant, une danse qui transforme le titre en épreuve d'endurance joyeuse, et les vidéos de ces danses font ensuite circuler les titres. Voir <a href=\"/bouyon-danse.html\">bouyon danse</a>.",
  ),
  (
    "Pourquoi les Martiniquais comprennent-ils le bouyon dominicain ?",
    "Parce que la Dominique et la Martinique partagent la langue kwéyòl : le créole dominicain est proche de celui de la Martinique. Un titre bouyon peut donc être compris et repris en Martinique sans traduction, et une voix martiniquaise sonne juste sur un riddim de Roseau. Ce passeport linguistique a permis au bouyon de devenir le jump up des Antilles françaises. Voir <a href=\"/bouyon-et-kweyol.html\">bouyon et kwéyòl</a>.",
  ),
  (
    "D'où vient le nom jump up ?",
    "Le terme jump up existait déjà dans les Antilles françaises pour désigner des musiques de carnaval très rythmées, notamment après le titre L'hivernage d'Exile One en 1987, surnommé The Yo. Quand le bouyon dominicain a traversé la mer, le public martiniquais l'a rangé naturellement dans cette famille : le nom résume son effet, un tempo rapide qui fait sauter tout le monde.",
  ),
  (
    "Où écouter le bouyon que danse la Martinique ?",
    "Sur la Bouyon Road Mix de Bouyon Shattaz, sur Spotify et YouTube : le public martiniquais est l'un des publics centraux de cette playlist, qui rassemble les nouveautés de la Dominique, de la Guadeloupe et de la Martinique, le bouyon soca et les classiques du carnaval. Pour la recevoir en DM, suivez @bouyonshattaz et commentez ROAD MIX. Voir la <a href=\"/playlist-bouyon.html\">playlist bouyon</a>.",
  )
]),
place("bouyon-france.html", "Bouyon en France",
"Bouyon en France : certifications, scènes et diaspora",
"Le bouyon en France : certifications, distribution et diaspora antillaise. Pourquoi la France est le grand marché du genre et l’enjeu du crédit dominicain.",
"Bouyon en France : le grand marché du genre",
"La France est devenue le grand marché économique du bouyon : c’est là que les titres se certifient, que la distribution se structure et que vivent une grande partie des fans antillais. Cette réalité donne à la France un pouvoir énorme sur un genre né en Dominique.",
"Certifications et industrie", "Des titres bouyon ont décroché des certifications de single d’or en France, preuve que le genre a dépassé le public antillais historique. Les structures françaises de distribution et de publishing jouent un rôle central, de Believe et TuneCore aux labels indépendants. C’est exactement le terrain où Bouyon Shattaz construit son réseau de distribution en gardant l’origine dominicaine au centre.",
"La diaspora comme public", "Paris et les grandes villes françaises concentrent une diaspora guadeloupéenne, martiniquaise, guyanaise et dominicaine qui fait vivre les soirées bouyon et les réseaux. Pour ce public, le bouyon est un lien direct avec le pays.", date_modified="2026-10-20", faq=[
  (
    "Dans quels pays le bouyon est-il populaire ?",
    "Né en Dominique, le bouyon est aujourd’hui central en Guadeloupe et en Martinique, présent en France, à Sainte-Lucie, à Saint-Martin et dans la diaspora caribéenne. En France, Paris et les grandes villes concentrent une diaspora guadeloupéenne, martiniquaise, guyanaise et dominicaine qui fait vivre les soirées bouyon et les réseaux.",
  ),
  (
    "Quel pays a créé le bouyon ?",
    "La Dominique. Le genre y est né en 1988 à Roseau, créé par le groupe WCK (Windward Caribbean Kulture), qui a branché la cadence-lypso et le jing ping sur des claviers électroniques et des boîtes à rythmes. Il reste le son du carnaval de Roseau, même si la France est devenue son grand marché économique.",
  ),
  (
    "Pourquoi la France est-elle le grand marché du bouyon ?",
    "Parce que c’est en France que les titres bouyon se certifient, que la distribution se structure et que vit une grande partie des fans antillais. Les structures françaises de distribution et de publishing, de Believe et TuneCore aux labels indépendants, y jouent un rôle central, ce qui donne à la France un pouvoir énorme sur un genre né en Dominique.",
  ),
  (
    "Quel titre bouyon a été certifié or en France ?",
    "« Pow Pow / Allo Doudou », de Niska, Litleboy LSBeats767 et <a href=\"/miimii-kds.html\">Miimii KDS</a>, a été certifié Single Or par la SNEP à 15 millions d’équivalents streams. C’est la preuve officielle que le bouyon a dépassé le public antillais historique et qu’il convertit sur le marché français, au-delà des plateformes sociales.",
  ),
  (
    "Le bouyon est-il né en France ?",
    "Non. Le bouyon est né en Dominique, à Roseau, en 1988, avec le groupe WCK. La France est son grand marché économique et lui offre une deuxième vie sur les réseaux, avec des certifications et des scènes, mais la chronologie est sans ambiguïté : la création est dominicaine, et les Antilles françaises puis la France l'ont adopté ensuite. Voir l'<a href=\"/origine-du-bouyon.html\">origine du bouyon</a>.",
  ),
  (
    "Pourquoi défendre l'origine dominicaine du bouyon en France ?",
    "Parce qu'une grande partie de l'argent du bouyon, certifications, distribution et grandes scènes, se fait en France et dans les Antilles françaises. Défendre l'origine dominicaine n'est pas de la nostalgie : c'est une question de crédits, de droits et de revenus pour les créateurs de l'île. C'est la mission éditoriale de <a href=\"/bouyon-shattaz.html\">Bouyon Shattaz</a>.",
  ),
  (
    "Où écouter du bouyon en France ?",
    "Dans les soirées bouyon de Paris et des grandes villes françaises, portées par la diaspora guadeloupéenne, martiniquaise, guyanaise et dominicaine, et sur la Bouyon Road Mix de Bouyon Shattaz, sur Spotify et YouTube. Paris concentre la plus grande diaspora antillaise d'Europe, avec des soirées dédiées et des DJ spécialisés. Voir <a href=\"/bouyon-paris.html\">le bouyon à Paris</a>.",
  ),
  (
    "Quels artistes et producteurs bouyon travaillent depuis la France ?",
    "Parmi les profils suivis par ce site : Ricky Bishop, rappeur d'origine guadeloupéenne et malgache basé à Bordeaux, créateur du concept New Bouyon, et Denmath, producteur originaire de Saint-Martin basé entre Nantes et Paris, connu pour Tropical Riddim et Harley Riddim. Leurs parcours dessinent la géographie actuelle du genre, entre les îles et la France. Voir <a href=\"/denmath.html\">Denmath</a>.",
  ),
  (
    "Quels distributeurs travaillent le bouyon en France ?",
    "Les structures françaises de distribution et de publishing jouent un rôle central, de Believe et TuneCore aux labels indépendants. Beaucoup d'artistes sortent aussi leurs titres sous des structures minuscules qui portent leur nom ou celui de leur producteur. C'est sur ce terrain que Bouyon Shattaz construit son réseau de distribution, en gardant l'origine dominicaine au centre.",
  ),
  (
    "Comment le bouyon est-il arrivé en France ?",
    "Par les Antilles françaises et la diaspora. Le bouyon a d'abord traversé la mer vers la Guadeloupe et la Martinique, où il a pris le nom de jump up, puis il s'est installé en France métropolitaine. Il y vit une deuxième vie sur les réseaux : des producteurs antillais en font des riddims taillés pour le club et la danse en vidéo, sous des noms comme shatta bouyon. Voir l'<a href=\"/histoire.html\">histoire du bouyon</a>.",
  ),
  (
    "Qui est Miimii KDS ?",
    "Miimii KDS est une artiste bouyon de Guadeloupe, révélation de la nouvelle vague. Son titre « Sé Miimii » porte son nom comme une signature, et elle est créditée sur « Pow Pow / Allo Doudou », certifié or par le SNEP. Cette certification en France, pour une artiste bouyon guadeloupéenne, mesure le chemin du genre, des soirées des îles aux certifications de l'industrie française. Voir les <a href=\"/artistes-guadeloupe.html\">artistes de Guadeloupe</a>.",
  )
]),
place("bouyon-paris.html", "Bouyon à Paris",
"Bouyon à Paris : soirées, DJ et scène bouyon parisienne",
"Le bouyon à Paris : la capitale française comme scène majeure du bouyon. Soirées, DJ antillais, diaspora et nouveaux producteurs du shatta bouyon.",
"Bouyon à Paris : la capitale du son antillais",
"Paris concentre la plus grande diaspora antillaise d’Europe, et le bouyon y a trouvé une scène : soirées dédiées, DJ spécialisés, producteurs qui fabriquent les riddims du moment et public qui réclame chaque nouveauté.",
"Le circuit parisien", "Un titre bouyon de 2026 suit souvent le même circuit : né en Dominique ou en Gwada, testé par les DJ de Paris, poussé sur les réseaux, puis certifié sur le marché français. Comprendre Paris, c’est comprendre l’économie actuelle du bouyon.",
"Le rôle des médias parisiens et antillais", "Les médias et pages spécialisées, de Paris aux Antilles, décident de la visibilité. Le réseau que Bouyon Shattaz fédère vise à ce que les artistes dominicains gardent la main sur ce circuit, de l’interview au meme.", date_modified="2026-10-20", faq=[
  (
    "Dans quels pays le bouyon est-il populaire ?",
    "Né en Dominique, le bouyon est aujourd’hui central en Guadeloupe et en Martinique, présent en France, à Sainte-Lucie, à Saint-Martin et dans la diaspora caribéenne. En France, Paris et les grandes villes concentrent une diaspora guadeloupéenne, martiniquaise, guyanaise et dominicaine qui fait vivre les soirées bouyon et les réseaux.",
  ),
  (
    "Quel pays a créé le bouyon ?",
    "La Dominique. Le genre y est né en 1988 à Roseau, créé par le groupe WCK (Windward Caribbean Kulture), qui a branché la cadence-lypso et le jing ping sur des claviers électroniques et des boîtes à rythmes. Il reste le son du carnaval de Roseau, même si la France est devenue son grand marché économique.",
  ),
  (
    "Pourquoi Paris compte-t-il autant pour le bouyon ?",
    "Paris concentre la plus grande diaspora antillaise d’Europe, et le bouyon y a trouvé une scène : soirées dédiées, DJ spécialisés, producteurs qui fabriquent les riddims du moment et public qui réclame chaque nouveauté. Un titre né en Dominique ou en Gwada y est souvent testé par les DJ, poussé sur les réseaux, puis certifié sur le marché français.",
  ),
  (
    "Quel artiste bouyon donne son premier concert solo à Paris en 2026 ?",
    "<a href=\"/ricky-bishop.html\">Ricky Bishop</a>, artiste du New Bouyon basé à Bordeaux, donne son premier concert solo à Paris le 20 octobre 2026. Une scène parisienne en nom propre qui montre que la géographie du genre s’écrit aussi en France métropolitaine, aux côtés de producteurs comme Denmath, entre Nantes et Paris.",
  ),
  (
    "Où écouter du bouyon à Paris ?",
    "Dans les soirées bouyon de la capitale, portées par la diaspora antillaise, où des DJ spécialisés testent chaque nouveau riddim. Pour suivre les titres qui passent dans ces soirées, la Bouyon Road Mix de Bouyon Shattaz, sur Spotify et YouTube, rassemble nouveautés bouyon et classiques du carnaval. Elle s'obtient aussi en DM en commentant ROAD MIX sur @bouyonshattaz. Voir la <a href=\"/playlist-bouyon.html\">playlist bouyon</a>.",
  ),
  (
    "Comment un titre bouyon devient-il un hit à Paris ?",
    "Il suit souvent le même circuit : né en Dominique ou en Gwada, testé par les DJ de Paris, poussé sur les réseaux, puis certifié sur le marché français. En amont, les DJ et les pages bouyon de Guadeloupe jouent un rôle décisif : leurs choix transforment un riddim en titre de carnaval, relayé ensuite vers la Martinique et Paris. Voir <a href=\"/bouyon-guadeloupe.html\">le bouyon en Guadeloupe</a>.",
  ),
  (
    "Quels producteurs bouyon sont basés à Paris ?",
    "<a href=\"/denmath.html\">Denmath</a>, de son vrai nom Mathurin DENMATH Denis, est un producteur, ingénieur du son et directeur artistique originaire de Saint-Martin, basé entre Nantes et Paris. Il est connu pour ses riddims bouyon Tropical Riddim et Harley Riddim, sortis en 2022, et il est crédité en featuring sur « Tarif » de Koko Bwa, sorti en avril 2025.",
  ),
  (
    "Qui est DJ Blax ?",
    "<a href=\"/dj-blax.html\">DJ Blax</a> est un DJ et producteur international basé à Paris, également directeur artistique. Sa biographie affiche INTERNATIONAL DJ FROM PVRIS, et sa rangée de drapeaux correspond aux lieux où il a joué, pas à ses origines. Son single Don't Care, avec la chanteuse Tamillia, est sorti le 16 octobre 2026, avec un clip tourné à St Maarten.",
  ),
  (
    "Quel rôle jouent les médias dans le bouyon à Paris ?",
    "Les médias et pages spécialisées, de Paris aux Antilles, décident de la visibilité d'un titre. Le réseau que fédère <a href=\"/bouyon-shattaz.html\">Bouyon Shattaz</a> vise à ce que les artistes dominicains gardent la main sur ce circuit, de l'interview au meme. TIITII NBA, avec bouyonews, couvre aussi l'actualité du genre en français pour la Guadeloupe, la Martinique et la France.",
  ),
  (
    "Quel style de bouyon Ricky Bishop défend-il à Paris ?",
    "Le New Bouyon, le concept qu'il a créé : un bouyon mélangé à la trap et à la musique électronique. Le magazine Modzik l'a profilé sous le titre La New Wave du bouyon et a couvert sa série d'événements #NewBouyonExperience. Son premier concert solo parisien, annoncé sous l'intitulé Ricky Bishop - 1st Paris Solo Show, a lieu le mardi 20 octobre 2026.",
  ),
  (
    "Quelle diaspora fait vivre le bouyon à Paris ?",
    "Paris concentre la plus grande diaspora antillaise d'Europe. Avec les grandes villes françaises, la capitale réunit une diaspora guadeloupéenne, martiniquaise, guyanaise et dominicaine qui fait vivre les soirées bouyon et les réseaux. Pour ce public, le bouyon est un lien direct avec le pays, et c'est aussi pour la diaspora que ce site existe en français et en anglais. Voir <a href=\"/bouyon-diaspora.html\">bouyon et diaspora</a>.",
  )
]),
place("bouyon-guyane.html", "Bouyon en Guyane",
"Bouyon en Guyane : le bouyon sur le continent sud-américain",
"Le bouyon en Guyane : le public guyanais du bouyon, entre Cayenne, les carnavals et les réseaux antillais. La branche continentale de la music bouyon.",
"Bouyon en Guyane : le son créole du continent",
"La Guyane, territoire français d’Amérique du Sud à forte culture créole, fait partie de l’audience naturelle du bouyon. Les titres de la Dominique, de la Guadeloupe et de la Martinique y circulent par les réseaux, les radios et les fêtes.",
"Un public connecté aux Antilles", "Le public guyanais suit la même actualité bouyon que celui de Gwada et de Martinique : mêmes riddims, mêmes artistes, mêmes danses. Pour les artistes dominicains, la Guyane complète le triangle francophone des Caraïbes et de la France.", date_modified="2026-10-20", faq=[
  (
    "Dans quels pays le bouyon est-il populaire ?",
    "Né en Dominique, le bouyon est aujourd'hui central en Guadeloupe et en Martinique, présent en France, à Sainte-Lucie, à Saint-Martin et dans la diaspora caribéenne, de New York à Londres, Toronto et Montréal. Sur le continent sud-américain, la Guyane fait aussi partie de son audience naturelle, portée par sa forte culture créole.",
  ),
  (
    "Quel pays a créé le bouyon ?",
    "La Dominique. Le genre y est né à la fin des années 1980 : c'est à Roseau, la capitale de l'île, que le groupe WCK l'a créé en 1988, en mélangeant jing ping, cadence-lypso et rythmes électroniques. Le bouyon reste aujourd'hui le son du carnaval de Roseau.",
  ),
  (
    "Le bouyon est-il écouté en Guyane ?",
    "Oui. La Guyane, territoire français d'Amérique du Sud à forte culture créole, fait partie de l'audience naturelle du bouyon. Les titres de la Dominique, de la Guadeloupe et de la Martinique y circulent par les réseaux, les radios et les fêtes, et le public guyanais suit les mêmes riddims, artistes et danses que celui des Antilles.",
  ),
  (
    "Qu'est-ce que le bouyon ?",
    "Le bouyon est un genre musical né en Dominique à la fin des années 1980, lancé par le groupe WCK. Son nom veut dire soupe en kwéyòl : il mélange jing ping, cadence-lypso, zouk et rythmes électroniques. Son tempo rapide en a fait la bande-son du carnaval, en Dominique comme en Guadeloupe et en Martinique. Voir l'<a href=\"/histoire.html\">histoire du bouyon</a>.",
  ),
  (
    "Quelle chanteuse bouyon s'est produite en Guyane ?",
    "<a href=\"/shanika.html\">Shanika</a>, chanteuse de Guadeloupe de la vague bouyon et shatta. Selon sa biographie publiée chez Music Story, son titre « Kay ve yo », sorti le 27 mai 2023 et produit par DJ Taffy selon les crédits du clip, a attiré une attention particulière et lui a permis de se produire dans plusieurs pays, dont la France, l'Allemagne et la Guyane.",
  ),
  (
    "Le bouyon gwada est-il joué en Guyane ?",
    "Oui, ce site en documente un exemple. <a href=\"/jixels.html\">Jixels</a>, claviériste et producteur bouyon ancré en Guadeloupe, légende sur TikTok un show au festival de la bouffe à Kourou, en Guyane, avec les hashtags bouyon, 973 pour la Guyane et 971 pour la Guadeloupe. Le circuit du bouyon gwada déborde donc jusqu'en Guyane française.",
  ),
  (
    "Que signifie 973 dans le bouyon ?",
    "973 est l'indicatif de la Guyane. Des artistes bouyon taguent leurs vidéos avec les indicatifs 971 pour la Guadeloupe, 767 pour la Dominique, 972 pour la Martinique et 973 pour la Guyane : une façon de s'adresser à tout l'arc du bouyon francophone et créolophone, de la Guadeloupe à la Guyane en passant par la Dominique et la Martinique.",
  ),
  (
    "Où écouter du bouyon quand on est en Guyane ?",
    "Sur la Bouyon Road Mix de Bouyon Shattaz, sur Spotify et YouTube, qui rassemble les nouveautés de la Dominique, de la Guadeloupe et de la Martinique, le bouyon soca et les classiques du carnaval. La logique de la playlist est simple : partir de l'origine, la Dominique, puis suivre le son là où il vit, en Gwada, en Martinique, en Guyane et à Paris. Voir la <a href=\"/playlist-bouyon.html\">playlist bouyon</a>.",
  ),
  (
    "Pourquoi la Guyane compte-t-elle pour les artistes dominicains ?",
    "Parce qu'elle complète le triangle francophone des Caraïbes et de la France. Territoire français d'Amérique du Sud à forte culture créole, la Guyane suit la même actualité bouyon que la Guadeloupe et la Martinique : mêmes riddims, mêmes artistes, mêmes danses. Les titres dominicains y circulent par les réseaux, les radios et les fêtes.",
  ),
  (
    "La diaspora guyanaise écoute-t-elle du bouyon en France ?",
    "Oui. Paris et les grandes villes françaises concentrent une diaspora guadeloupéenne, martiniquaise, guyanaise et dominicaine qui fait vivre les soirées bouyon et les réseaux. Pour ce public, le bouyon est un lien direct avec le pays. La présence de ces fans antillais est l'une des raisons pour lesquelles la France est devenue le grand marché du genre. Voir <a href=\"/bouyon-france.html\">le bouyon en France</a>.",
  )
]),
place("bouyon-saint-martin.html", "Bouyon à Saint-Martin",
"Bouyon à Saint-Martin : les producteurs de SXM et le bouyon",
"Le bouyon à Saint-Martin : l’île de Denmath, producteur bouyon de SXM basé entre Nantes et Paris. La place de Saint-Martin dans la nouvelle scène bouyon.",
"Bouyon à Saint-Martin : petite île, producteurs pointus",
"Saint-Martin compte dans la nouvelle géographie du bouyon grâce à ses producteurs, au premier rang desquels Denmath, beatmaker originaire de SXM, spécialiste du bouyon, du kompa et du shatta, connu pour ses riddims Tropical Riddim et Harley Riddim.",
"Un pont entre Caraïbes et France", "Basé entre Nantes et Paris, Denmath illustre le parcours des producteurs de la nouvelle génération : racines caribéennes, studio en France, collaborations dans toutes les Antilles. Voir sa page dédiée : <a href=\"/denmath.html\">Denmath</a>.", date_modified="2026-10-20", faq=[
  (
    "Dans quels pays le bouyon est-il populaire ?",
    "Né en Dominique, le bouyon est aujourd'hui central en Guadeloupe et en Martinique, présent en France, à Sainte-Lucie, à Saint-Martin et dans la diaspora caribéenne. À Saint-Martin, ce site documente des producteurs comme Denmath et des actes bouyon de Sint Maarten, la partie néerlandaise de l'île, comme BRG Hollywood et les Tolly Boys.",
  ),
  (
    "Quel pays a créé le bouyon ?",
    "La Dominique. Le genre y est né à la fin des années 1980 : c'est à Roseau, la capitale de l'île, que le groupe WCK l'a créé en 1988, en mélangeant jing ping, cadence-lypso et rythmes électroniques. Le bouyon reste aujourd'hui le son du carnaval de Roseau.",
  ),
  (
    "Quels producteurs bouyon viennent de Saint-Martin ?",
    "Le nom principal est Denmath, de son vrai nom Mathurin DENMATH Denis : producteur, ingénieur du son et directeur artistique originaire de Saint-Martin, d'héritage haïtien, basé entre Nantes et Paris. Spécialiste du bouyon, du kompa et du shatta, il est connu pour ses riddims Tropical Riddim et Harley Riddim. Voir sa page <a href=\"/denmath.html\">Denmath</a>.",
  ),
  (
    "Quelle chanteuse bouyon a grandi à Saint-Martin ?",
    "Tamillia, de son nom complet Tamillia Chance, a grandi à Saint-Martin, dans les cultures française et néerlandaise de l'île, et a participé à The Voice Kids France à 14 ans. Elle est la voix de Don't Care, le single de DJ Blax sorti le 16 octobre 2026, dont le clip a été tourné à St Maarten, la partie néerlandaise de l'île. Voir <a href=\"/dj-blax.html\">DJ Blax</a>.",
  ),
  (
    "Qui est BRG Hollywood ?",
    "<a href=\"/brg-hollywood.html\">BRG Hollywood</a>, de son vrai nom Jaheim Meyers, est un artiste bouyon de Sint Maarten. Son titre « We Not Going Home », avec C4, sorti le 31 octobre 2025 sur le label BankrollGang, a fait de lui le premier artiste du côté néerlandais de l'île à atteindre un million de vues sur YouTube, un jalon salué par le Premier ministre, le Dr Luc Mercelina.",
  ),
  (
    "Tolly Boys et Tallyboy, est-ce le même artiste ?",
    "Non. Les <a href=\"/tolly-boys.html\">Tolly Boys</a>, avec un o, sont un acte bouyon de Sint Maarten, autour de l'auteur Youry Fleming, connus pour « Get on Bad », « Oú Paté Vwey » et « GoDownGoDown », puis pour le label YMW Tolly Boys. Tallyboy, avec un a, est un artiste solo de Sainte-Lucie. Ni la même personne, ni la même île, ni le même catalogue.",
  ),
  (
    "Qui est Wizito ?",
    "Wizito est le nom de scène de <a href=\"/bernard-gumbs-wizito.html\">Bernard Gumbs</a>. Ses trois titres vérifiés, « Payé » avec Youry Ymw en 2023, « Love Me » en 2024 et « TunTun » en 2025, sortent sur le label YMW Tolly Boys. Un mix consacré aux sorties locales du carnaval de St Maarten 2024 a retenu « Love Me », ce qui le rattache au circuit bouyon de Saint-Martin, sans origine personnelle publiée.",
  ),
  (
    "Ebony Empress est-elle de Saint-Martin ?",
    "Elle y vit, mais elle est née en Dominique. <a href=\"/ebony-empress.html\">Ebony Empress</a>, de son vrai nom Everlyne Walters, est née dans le village de Lagoon, à Portsmouth, et elle est aujourd'hui basée à Saint-Martin. Percée en 2018 avec « Quality Bumper », elle a terminé deuxième dauphine du Senior Calypso de Saint-Martin en 2024 et a été nommée aux Caribbean Music Awards 2026.",
  ),
  (
    "Saint-Martin ou Sint Maarten : quelle différence pour le bouyon ?",
    "C'est la même île, partagée en deux : Sint Maarten, aussi écrit St Maarten, est sa partie néerlandaise, et Saint-Martin sa partie française. Pour le bouyon, BRG Hollywood et les Tolly Boys sont documentés côté Sint Maarten, Tamillia a grandi dans les cultures française et néerlandaise de l'île, et Denmath est présenté comme originaire de Saint-Martin, sans précision de côté.",
  ),
  (
    "Le bouyon est-il populaire à Saint-Martin ?",
    "Oui, et les sources le montrent jusque dans les écoles. Une étude universitaire menée dans une école primaire de Sint Maarten décrit les Tolly Boys comme des interprètes locaux de bouyon dont les écoliers chantaient le titre le plus célèbre en classe. En 2026, « We Not Going Home » de BRG Hollywood a dépassé le million de vues sur YouTube, une première pour le côté néerlandais de l'île.",
  )
]),
place("bouyon-sainte-lucie.html", "Bouyon à Sainte-Lucie",
"Bouyon à Sainte-Lucie : le bouyon soca vu de Castries",
"Le bouyon à Sainte-Lucie : l’île voisine de la Dominique où le bouyon soca a grandi et s’est répandu, après son lancement en Dominique en 2003. Liens entre Roseau et Castries, carnavals et publics créoles.",
"Bouyon à Sainte-Lucie : la voisine où le bouyon soca a grandi",
"Sainte-Lucie est l’île créolophone la plus proche de la Dominique. Le bouyon soca a été lancé en Dominique par Dada en 2003, selon le témoignage de Smokiller, présent dans les studios à l’époque. Sainte-Lucie est ensuite devenue l’une des îles où la fusion a le plus grandi, chez des producteurs et un public qui aiment autant la soca de Trinidad que le bouyon dominicain.",
"Deux carnavals qui se répondent", "Les publics de Roseau et de Castries partagent langue, histoire et goût de la fête. Les titres voyagent d’un carnaval à l’autre, et le <a href=\"/bouyon-soca.html\">bouyon soca</a> est devenu leur langue musicale commune.", date_modified="2026-10-20", faq=[
  (
    "Dans quels pays le bouyon est-il populaire ?",
    "Né en Dominique, le bouyon est aujourd'hui central en Guadeloupe et en Martinique, présent en France, à Sainte-Lucie, à Saint-Martin et dans la diaspora caribéenne. À Sainte-Lucie, l'île créolophone la plus proche de la Dominique, il circule surtout sous la forme du bouyon soca, d'un carnaval à l'autre.",
  ),
  (
    "Quel pays a créé le bouyon ?",
    "La Dominique. Le bouyon y est né à la fin des années 1980 : en 1988, le groupe <a href=\"/wck.html\">WCK</a>, formé à Roseau, fusionne la cadence-lypso et le jing ping avec les claviers électroniques et les boîtes à rythmes. Le genre reste aujourd'hui le son du carnaval de Roseau, le Mas Domnik.",
  ),
  (
    "Quels sont les liens entre la Dominique et Sainte-Lucie ?",
    "Sainte-Lucie est l'île créolophone la plus proche de la Dominique. Les publics de Roseau et de Castries partagent la langue, l'histoire et le goût de la fête, et les titres voyagent d'un carnaval à l'autre. Le bouyon soca est devenu la langue musicale commune des deux îles, que la Bouyon Road Mix relie aussi pendant la saison des carnavals.",
  ),
  (
    "Qu'est-ce que le bouyon soca ?",
    "Le bouyon soca est la fusion entre le bouyon de la Dominique et la soca de Trinidad : le tempo rapide, les claviers en boucle et la basse synthétique du bouyon rencontrent la structure festive de la soca. Lancé en Dominique par Dada en 2003, il s'est ensuite développé dans des îles voisines comme Sainte-Lucie et Antigua. Plus de détails sur la page <a href=\"/bouyon-soca.html\">bouyon soca</a>.",
  ),
  (
    "Le bouyon soca a-t-il été créé à Sainte-Lucie ?",
    "Non. Selon le témoignage de première main de Smokiller, présent dans les studios avec Dada et la Nursery Krew, le bouyon soca a été lancé par <a href=\"/dada.html\">Dada</a> en Dominique en 2003. Un texte de référence largement repris l'attribue à des producteurs surtout sainte-luciens, mais ce site retient le témoignage du participant direct. Sainte-Lucie est ensuite l'une des îles où la fusion a le plus grandi.",
  ),
  (
    "Qu'est-ce que le Dennery Segment ?",
    "Le Dennery Segment est le son soca de Sainte-Lucie, né dans la commune de Dennery, dans la vallée de la Mabouya. Il est bâti sur des rythmes venus du kuduro angolais, du zouk et des percussions luciennes, avec des paroles en créole. Son de fête rapide et local, il occupe à Sainte-Lucie une place comparable à celle du bouyon chez ses voisins.",
  ),
  (
    "Le Dennery Segment est-il du bouyon ?",
    "Non. Le Dennery Segment est un cousin sainte-lucien du bouyon, pas une branche du genre dominicain. Les deux se tiennent côte à côte dans la carte des musiques de fête des Caraïbes orientales, avec les mêmes usages de rue et de carnaval, et les DJ les mélangent : un mix du selector Klondé sur BBC Radio 1Xtra était présenté comme un mix de bouyon de la Dominique et de Dennery Segment.",
  ),
  (
    "Quels artistes de Sainte-Lucie suit ce site ?",
    "<a href=\"/tallyboy.html\">Tallyboy</a>, interprète et auteur-compositeur de Sainte-Lucie. Son adresse Instagram, @tallyboypondmic_758, porte le 758, l'indicatif de l'île, comme une signature. Un guide du World Creole Music Festival publié par writeups24 cite aussi un Tally Boy, en deux mots, parmi les artistes sainte-luciens associés au DYP Band pour le festival de Roseau.",
  ),
  (
    "Tallyboy et Tolly Boys, est-ce le même artiste ?",
    "Non. Tallyboy, avec un a, est un artiste solo de Sainte-Lucie, dont l'adresse Instagram porte l'indicatif 758. Les <a href=\"/tolly-boys.html\">Tolly Boys</a>, avec un o, sont un acte bouyon de Sint Maarten, la partie néerlandaise de Saint-Martin, autour de l'auteur Youry Fleming et du label YMW Tolly Boys. Les deux noms se ressemblent, mais ni l'île ni le catalogue ne sont les mêmes.",
  ),
  (
    "Quels sont les grands titres du bouyon soca ?",
    "Les références retiennent « Famalay » et « Conch Shell » comme emblèmes du genre, deux productions de Dada selon la presse et les crédits officiels. « Famalay », interprété par Machel Montano, Skinny Fabulous et Bunji Garlin, a été le titre de Road March 2019 de Trinidad et Tobago. « Conch Shell » réunit Machel Montano, Skinny Fabulous et Iwer George.",
  ),
  (
    "Où écouter du bouyon soca de Roseau à Castries ?",
    "Sur la Bouyon Road Mix de Bouyon Shattaz, sur Spotify et YouTube. Sa partie bouyon soca suit la fusion qui fait la jonction entre Roseau, Castries, Pointe-à-Pitre et Fort-de-France pendant la saison des carnavals, à côté des nouveautés bouyon et des classiques du carnaval. Pour la recevoir en DM, commentez ROAD MIX sur @bouyonshattaz. Voir la <a href=\"/playlist-bouyon.html\">playlist bouyon</a>.",
  ),
  (
    "Pourquoi le bouyon passe-t-il si bien à Sainte-Lucie ?",
    "Notamment grâce à la langue. Le kwéyòl dominicain est proche des créoles de Guadeloupe, de Martinique et de Sainte-Lucie, et ce passeport linguistique aide les titres à voyager d'une île à l'autre sans traduction. À Sainte-Lucie, un public qui aime autant la soca de Trinidad que le bouyon dominicain a fait grandir le bouyon soca. Voir <a href=\"/bouyon-et-kweyol.html\">bouyon et kwéyòl</a>.",
  )
]),
place("bouyon-antigua.html", "Bouyon à Antigua",
"Bouyon à Antigua : le bouyon soca dans les Leeward",
"Le bouyon à Antigua : la place de l’île dans la diffusion du bouyon et du bouyon soca dans les îles Leeward, entre carnaval d’Antigua et sons de la Dominique.",
"Bouyon à Antigua : la diffusion vers les Leeward",
"Antigua fait partie des îles où le bouyon et sa fusion avec la soca se sont installés durablement. Son carnaval et ses sound systems relaient les sons de la Dominique vers les îles Leeward.",
"Un public de connaisseurs", "Comme Sainte-Lucie, Antigua a contribué à façonner le bouyon soca en le confrontant aux codes de la soca et des fêtes locales. Cette histoire partagée rappelle que le bouyon est un genre caribéen, avec un centre de gravité clair : la Dominique.", date_modified="2026-10-20", faq=[
  (
    "Dans quels pays le bouyon est-il populaire ?",
    "Né en Dominique, le bouyon est aujourd'hui central en Guadeloupe et en Martinique, où le public l'appelle aussi jump up. Il est présent en France, à Sainte-Lucie, à Antigua, à Saint-Martin et dans la diaspora caribéenne, de New York à Londres, Toronto et Montréal. Dans les îles Leeward, Antigua est l'un des relais du son dominicain.",
  ),
  (
    "Quel pays a créé le bouyon ?",
    "La Dominique. Le genre est né à Roseau à la fin des années 1980, quand le groupe WCK, formé en 1988, a fusionné la cadence-lypso avec le jing ping et les tambours traditionnels comme le lapo kabwit. Il reste le son du carnaval de Roseau, le Mas Domnik.",
  ),
  (
    "Le bouyon est-il populaire à Antigua ?",
    "Oui. Antigua fait partie des îles où le bouyon et sa fusion avec la soca se sont installés durablement. Son carnaval et ses sound systems relaient les sons de la Dominique vers les îles Leeward, et bouyon et soca y circulent depuis les années 1980 et 1990, comme à Sainte-Lucie.",
  ),
  (
    "Quel rôle Antigua a-t-elle joué dans le bouyon soca ?",
    "Comme Sainte-Lucie, Antigua a contribué à façonner le bouyon soca en le confrontant aux codes de la soca et des fêtes locales. Le style lui-même a été lancé en Dominique par Dada en 2003, selon le témoignage de Smokiller, avant de se développer dans ces îles. Voir la page <a href=\"/bouyon-soca.html\">bouyon soca</a>.",
  ),
  (
    "Qu'est-ce que le bouyon soca ?",
    "Le bouyon soca est la fusion la plus populaire née autour du bouyon : les rythmes rapides et les claviers du bouyon dominicain rencontrent l'énergie et les codes de la soca de Trinidad. Pensé pour la route, les bands et les sound systems, il voyage d'île en île pendant la saison des carnavals, jusqu'à Antigua.",
  ),
  (
    "Quel titre bouyon a marché à Antigua ?",
    "« Whistle While You Work » de Triple Kay est le titre que ce site documente sur ce point. Présenté par le groupe comme un bouyon 2024, il est décrit par son site officiel comme un succès en tête de plusieurs classements régionaux, notamment à Antigua. Les crédits officiels nomment Kendel « Killa » Laurent comme producteur du riddim. Voir le profil de <a href=\"/killa-laurent.html\">Killa Laurent</a>.",
  ),
  (
    "Qui a produit « Forks Up » de Romel ?",
    "Kendel « Killa » Laurent, producteur de la Dominique, selon les crédits officiels. Ce titre soca de 2019 de Romel, artiste soca d'Antigua, a été produit et mixé par Killa Laurent au Music Box Studio, en Dominique, avec un mastering de Cornel « Fingers » Philip, d'Imperial Publishing. Le crédit montre un studio dominicain au service d'une voix d'Antigua, dans le circuit régional des carnavals.",
  ),
  (
    "Triple Kay joue-t-il au carnaval d'Antigua ?",
    "Oui, selon le site officiel du groupe. TK International, aussi appelé Triple Kay, groupe bouyon de la Dominique, cite les carnavals d'Antigua, de Saint-Thomas, de Sainte-Croix et de Saint-Martin parmi ses scènes habituelles, aux côtés de Caribana à Toronto et du carnaval de Notting Hill. C'est l'une des routes par lesquelles le bouyon dominicain arrive à Antigua. Voir <a href=\"/tk-international.html\">TK International</a>.",
  ),
  (
    "Quels autres artistes de la Dominique se sont produits à Antigua ?",
    "Daddy Chess, entre autres. Son profil publié sur ItzCaribbean le fait se produire dans toute la Caraïbe, des îles Vierges à Sainte-Lucie, Trinidad, la Barbade et Antigua. Chester Letang de son vrai nom, voix du Swinging Stars Orchestra, il est un artiste de calypso et de soca qui partage les scènes de carnaval du bouyon. Voir <a href=\"/daddy-chess.html\">Daddy Chess</a>.",
  ),
  (
    "Tizzy, la chanteuse d'Antigua, est-elle une artiste bouyon ?",
    "Non. Tizzy, de son vrai nom Tanzania Sebastian, est une chanteuse de soca d'Antigua, voix du groupe El A Kru, connue pour « Expose ». Son nom s'écrit avec un i et elle n'a pas de profil bouyon. Elle ne doit pas être confondue avec Tazzy, ni avec Tazzo Thaboss, artiste de la Dominique : ce sont trois noms distincts. Voir la page <a href=\"/tazzy.html\">Tazzy</a>.",
  ),
  (
    "Où écouter le bouyon soca qui circule jusqu'à Antigua ?",
    "Sur la Bouyon Road Mix de Bouyon Shattaz, disponible sur Spotify et YouTube. La playlist rassemble les nouveautés bouyon de la Dominique et des Antilles françaises, le bouyon soca, les riddims du moment et les classiques du carnaval. Pour la recevoir en message privé, suivez @bouyonshattaz sur Instagram et commentez ROAD MIX. Voir la <a href=\"/playlist-bouyon.html\">playlist bouyon</a>.",
  )
]),
place("bouyon-diaspora.html", "Bouyon et diaspora",
"Bouyon et diaspora : le bouyon à New York, Londres et Toronto",
"Le bouyon dans la diaspora : comment les Dominicains et Antillais de New York, Londres, Toronto et Montréal gardent le bouyon vivant loin des Caraïbes.",
"Bouyon et diaspora : le son du pays, loin du pays",
"Partout où vivent des Dominicains et des Antillais, le bouyon voyage dans les valises et les téléphones : New York et Brooklyn, Londres, Toronto, Montréal. Pour la diaspora, un titre bouyon est un morceau du pays.",
"Les fêtes de la diaspora", "Les soirées caribéennes des grandes villes mélangent bouyon, soca, dancehall et zouk, mais le moment bouyon garde sa charge particulière : c’est le son de Roseau, de Grand Bay et du Mas Domnik. Les réseaux sociaux ont remplacé les cassettes d’autrefois : un riddim né en Dominique fait le tour du monde en quelques heures.",
"Un public stratégique", "La diaspora consomme, partage et finance le bouyon moderne. C’est pour elle aussi que Bouyon Shattaz publie en anglais comme en français, et que ce site existe en deux langues.", date_modified="2026-10-20", faq=[
  (
    "Dans quels pays le bouyon est-il populaire ?",
    "Né en Dominique, le bouyon est aujourd'hui central en Guadeloupe et en Martinique, présent en France, à Sainte-Lucie, à Saint-Martin et dans la diaspora caribéenne. Partout où vivent des Dominicains et des Antillais, il voyage avec eux, de New York et Brooklyn à Londres, Toronto et Montréal.",
  ),
  (
    "Quel pays a créé le bouyon ?",
    "La Dominique. Le bouyon y est né à la fin des années 1980 : en 1988, le groupe <a href=\"/wck.html\">WCK</a>, formé à Roseau, la capitale, fusionne la cadence-lypso et le jing ping avec les claviers électroniques et les boîtes à rythmes. Le genre reste aujourd'hui le son du carnaval de Roseau, le Mas Domnik.",
  ),
  (
    "Dans quelles villes de la diaspora écoute-t-on du bouyon ?",
    "À New York et Brooklyn, à Londres, à Toronto et à Montréal, partout où vivent des Dominicains et des Antillais. Les soirées caribéennes de ces grandes villes mélangent bouyon, soca, dancehall et zouk, mais le moment bouyon garde une charge particulière : c'est le son de Roseau, de Grand Bay et du Mas Domnik.",
  ),
  (
    "Pourquoi la diaspora compte-t-elle pour le bouyon ?",
    "Parce que la diaspora consomme, partage et finance le bouyon moderne. Les réseaux sociaux ont remplacé les cassettes d'autrefois : un riddim né en Dominique fait le tour du monde en quelques heures. C'est aussi pour ce public que <a href=\"/bouyon-shattaz.html\">Bouyon Shattaz</a> publie en anglais comme en français, et que ce site existe en deux langues.",
  ),
  (
    "Où écouter du bouyon à Paris ?",
    "Dans les soirées antillaises de la capitale, qui concentre la plus grande diaspora antillaise d'Europe. Le bouyon y a trouvé une scène : soirées dédiées, DJ spécialisés, producteurs qui fabriquent les riddims du moment et public qui réclame chaque nouveauté. Un titre né en Dominique ou en Gwada y est souvent testé par les DJ, poussé sur les réseaux, puis certifié sur le marché français. Voir <a href=\"/bouyon-paris.html\">bouyon à Paris</a>.",
  ),
  (
    "Existe-t-il un prix bouyon à New York ?",
    "Oui : les Caribbean Music Awards ont une catégorie Bouyon Artist of the Year. Leur troisième édition s'est tenue le 28 août 2025 à Brooklyn, New York, avec neuf nommés publiés en juin 2025, dont Asa Bantan, Kenny G, Trilla G, Triple K et Pudaz. Que le bouyon ait sa propre catégorie devant un public de diaspora montre que le genre né en Dominique est devenu une case officielle. Voir <a href=\"/kenny-g-dominica.html\">Kenny G</a>.",
  ),
  (
    "Quels groupes bouyon jouent dans les carnavals de la diaspora ?",
    "TK International, aussi appelé Triple Kay, en est l'exemple le mieux documenté. Le site officiel de ce groupe bouyon de la Dominique cite Houston Carifest, Caribana à Toronto, le carnaval de Notting Hill au Royaume-Uni, le carnaval de Miami et la fête antillaise de New York parmi ses scènes. Pour le public de la diaspora, c'est le son de Roseau joué en direct. Voir <a href=\"/tk-international.html\">TK International</a>.",
  ),
  (
    "Des artistes bouyon ont-ils chanté au carnaval de Notting Hill ?",
    "Oui. Ebony Empress, artiste bouyon originaire de Lagoon, à Portsmouth, en Dominique, cite parmi ses scènes le carnaval de Notting Hill et le week-end de la fête du Travail à New York. Elle raconte que son souvenir le plus marquant reste la route de Notting Hill, devant des milliers de personnes chantant et dansant sur sa musique. Triple Kay cite aussi Notting Hill parmi ses carnavals. Voir <a href=\"/ebony-empress.html\">Ebony Empress</a>.",
  ),
  (
    "Quels titres bouyon passent dans les carnavals de Toronto et de Miami ?",
    "« What She Like », de Trixzmigos avec Hussey, en est un exemple documenté. Le titre figure dans les tracklists publiées des mix Toronto Carnival 2025 et Miami Carnival 2025 de DJ BuzzB, dans le Bouyon Passport 2026 de DJ Close et dans un mix Miami Carnival de I AM SONICBOOM, qui l'annonce comme un titre bouyon. Les DJ de carnaval sont le premier relais du bouyon dans la diaspora. Voir <a href=\"/hussey.html\">Hussey</a>.",
  ),
  (
    "Le J'ouvert se fête-t-il aussi dans la diaspora ?",
    "Oui. Le J'ouvert, la fête de l'aube qui ouvre les jours gras, vit dans tout le monde créole et caribéen, de Trinidad à la Dominique, et jusqu'aux carnavals de la diaspora à Brooklyn et à Londres. En Dominique, ce sont les sound systems et les groupes qui y jouent le bouyon de l'année jusqu'au matin. Voir la page <a href=\"/jouvert.html\">J'ouvert</a>.",
  ),
  (
    "Comment suivre le bouyon quand on vit loin de la Dominique ?",
    "Avec la Bouyon Road Mix de Bouyon Shattaz, sur Spotify et YouTube, qui rassemble les nouveautés de la Dominique et des Antilles françaises, le bouyon soca, les riddims du moment et les classiques du carnaval. Le compte Instagram @bouyonshattaz publie l'actualité du genre en français et en anglais : commentez ROAD MIX pour recevoir la playlist en message privé. Voir la <a href=\"/playlist-bouyon.html\">playlist bouyon</a>.",
  )
]),
]
