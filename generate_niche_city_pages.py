#!/usr/bin/env python3
"""
generate_niche_city_pages.py
Génère /agences/[niche]/[ville]/index.html — SEO programmatique francophonie.
Usage : python3 generate_niche_city_pages.py
"""

import os
import hashlib
import xml.etree.ElementTree as ET
from datetime import date
from math import ceil

# ─── DONNÉES NICHES ─────────────────────────────────────────────────────────

NICHES = {
    'centres-esthetiques': {
        'label': 'Centres esthétiques &amp; médecine esthétique',
        'label_raw': 'Centres esthétiques & médecine esthétique',
        'title_short': 'Centres esthétiques',
        'pill_text': 'Analyse de niche · Centres esthétiques',
        'h1_line1': 'Agence IA pour les centres esthétiques',
        'stat1_num': '13 000', 'stat1_label': 'Établissements en France',
        'stat2_num': '&lt;20%', 'stat2_label': 'Utilisent un CRM',
        'stat3_num': '4-8k€', 'stat3_label': 'Ticket setup typique',
        'national_count': 13000,
        'market_body': 'Les centres esthétiques et cliniques de médecine esthétique représentent 3,5 milliards d\'euros en France, avec une croissance de 7 à 12% par an. La demande est là. La structure commerciale pour la capter, non.',
        'pain1_title': 'Le bouche-à-oreille plafonne la croissance',
        'pain1_body': '60-70% des clients viennent de recommandations. Ça semble positif, mais ça signifie qu\'il n\'y a aucun levier scalable. Le cabinet ne peut pas décider de croître de 30% en un trimestre si tout repose sur le réseau existant.',
        'pain2_title': 'Les leads entrants disparaissent le soir et le week-end',
        'pain2_body': 'Messages Instagram, appels, demandes de devis — personne ne répond dans la demi-heure. Le prospect rappelle un concurrent ou oublie. Ce n\'est pas un manque de motivation, c\'est un manque de disponibilité structurelle.',
        'pain3_title': 'Les retouches ne sont jamais relancées',
        'pain3_body': 'Un acte botox ou filler génère un retour naturel à 90-120 jours. Sans relance automatique à J+90/J+100/J+110, 40-60% de ces retours potentiels n\'ont jamais lieu. Du chiffre d\'affaires qui disparaît sans que le cabinet s\'en aperçoive.',
        'infra1_title': 'Chatbot 24/7 DMs Instagram & formulaires',
        'infra1_body': 'Qualification automatique des demandes entrantes — type d\'acte, budget, disponibilité. Les leads chauds reçoivent un lien de réservation direct. Le cabinet n\'intervient que pour valider.',
        'infra2_title': 'Séquence relances retouches J+90/J+100/J+110',
        'infra2_body': 'SMS et email automatiques déclenchés après chaque acte. Taux de retour retouches : +35-50% vs sans système.',
        'infra3_title': 'Pipeline GHL + dashboard suivi',
        'infra3_body': 'Tous les leads, RDV et actes en cours dans une seule interface. Vue en temps réel sur le chiffre d\'affaires en cours de génération.',
        'ticket_setup': '4 000 – 8 000 €',
        'ticket_retainer': '800 – 1 500 €',
        'student_initials': 'L',
        'student_name': 'Louis',
        'student_before': '3 000 €',
        'student_after': '58 000 €',
        'student_delay': '~8 mois',
        'student_niche': 'Niche centres esthétiques',
        'student_desc': 'Louis est passé de 3 000 à 58 000 €/mois en ciblant les centres esthétiques. L\'angle : automatiser la capture de leads et les relances retouches. Des cabinets avec de la demande et aucun système commercial.',
        'parent_page_name': 'Centres esthétiques',
    },
    'btp-construction': {
        'label': 'BTP &amp; construction',
        'label_raw': 'BTP & construction',
        'title_short': 'BTP & Construction',
        'pill_text': 'Analyse de niche · BTP & construction',
        'h1_line1': 'Agence IA pour le BTP & la construction',
        'stat1_num': '440 000', 'stat1_label': 'Entreprises en France',
        'stat2_num': '&lt;30%', 'stat2_label': 'Taux conversion devis',
        'stat3_num': '2,5-7k€', 'stat3_label': 'Ticket setup typique',
        'national_count': 440000,
        'market_body': 'Le BTP représente 1 400 milliards d\'euros de chiffre d\'affaires cumulé en France. 440 000 entreprises, dont une majorité de TPE artisanales sans aucun système commercial structuré — et des carnets de commandes qui se vident par vagues.',
        'pain1_title': 'Les appels manqués sur chantier font perdre des contrats',
        'pain1_body': 'Un artisan en intervention ne peut pas répondre au téléphone. 20% des appels entrants ne sont jamais rappelés. Chaque appel manqué, c\'est un prospect qui appelle le concurrent suivant dans sa liste.',
        'pain2_title': 'Les devis partent sans jamais être relancés',
        'pain2_body': 'Le taux de conversion moyen sur devis est inférieur à 30%. La majorité des artisans envoient un devis et attendent. Sans relance à J+3, J+7 et J+14, les prospects refroidissent et signent ailleurs.',
        'pain3_title': 'La charge mentale bloque toute prospection proactive',
        'pain3_body': 'Entre les chantiers, les équipes, les fournisseurs et la facturation, il ne reste plus de temps pour aller chercher de nouveaux clients. Le carnet se vide par vagues, et la prospection reprend seulement quand c\'est urgent.',
        'infra1_title': 'Capture appels manqués + formulaire site',
        'infra1_body': 'Tout appel manqué déclenche un SMS automatique au prospect dans les 5 minutes. Le formulaire site qualifie type de travaux, surface, délai. Taux de rappel : ×3 vs sans système.',
        'infra2_title': 'Séquences relance devis J+3 / J+7 / J+14',
        'infra2_body': 'Email + SMS automatiques après chaque envoi de devis. Le taux de conversion moyen passe de 28% à 42-48% avec 3 relances bien timées.',
        'infra3_title': 'Pipeline GHL + automatisation avis Google',
        'infra3_body': 'Chaque chantier terminé déclenche une demande d\'avis automatique. Les avis Google sont le premier levier de confiance dans le BTP local.',
        'ticket_setup': '2 500 – 7 000 €',
        'ticket_retainer': '500 – 1 500 €',
        'student_initials': 'R&amp;J',
        'student_name': 'Ryan &amp; Julien',
        'student_before': '5 000 €',
        'student_after': '40 000 €+',
        'student_delay': '3 mois',
        'student_niche': 'Niche BTP &amp; habitat',
        'student_desc': 'Ryan &amp; Julien ont ciblé le BTP et l\'habitat dès le début du programme. En 3 mois, ils sont passés de 5 000 à 40 000 €+ contractualisés sur un seul mois. Le BTP est une niche à fort volume et faible concurrence IA.',
        'parent_page_name': 'BTP & Construction',
    },
    'immobilier': {
        'label': 'Immobilier',
        'label_raw': 'Immobilier',
        'title_short': 'Immobilier',
        'pill_text': 'Analyse de niche · Immobilier',
        'h1_line1': 'Agence IA pour les agences immobilières',
        'stat1_num': '33 000', 'stat1_label': 'Agences en France',
        'stat2_num': '80%', 'stat2_label': 'Leads perdus après 2h',
        'stat3_num': '3-9k€', 'stat3_label': 'Ticket setup typique',
        'national_count': 33000,
        'market_body': 'L\'immobilier résidentiel représente 1 000 milliards d\'euros de transactions par an en France. 33 000 agences — dont la majorité répondent à leurs leads en 4 à 6 heures en moyenne. Le délai de réponse est le seul différenciateur qui compte.',
        'pain1_title': 'Le délai de réponse tue la conversion',
        'pain1_body': '80% des leads immobiliers sont perdus si la réponse dépasse 2 heures. Le délai moyen en agence est de 4 à 6 heures. 75% des prospects contactent plusieurs agences simultanément — celui qui répond en premier signe.',
        'pain2_title': 'Les agents passent 80% de leur temps en administratif',
        'pain2_body': 'Qualification acheteurs, relances vendeurs, comptes-rendus de visite, suivi de dossier — tout ça se fait manuellement. Il ne reste plus de temps pour la prospection de nouveaux mandats.',
        'pain3_title': 'Les mandats sont perdus faute de suivi',
        'pain3_body': '35 à 45% des mandats exclusifs n\'aboutissent pas à une vente. Le vendeur signe avec un concurrent qui a mieux suivi. Sans pipeline automatisé, les relances tombent dans les oubliettes.',
        'infra1_title': 'Qualification instantanée des leads entrants (<5 min)',
        'infra1_body': 'Chatbot sur le site et sur les portails (SeLoger, LeBonCoin) qui qualifie budget, type de bien, délai et projet. Les leads chauds arrivent pré-qualifiés dans l\'agenda de l\'agent.',
        'infra2_title': 'Suivi automatique des mandats et prospects froids',
        'infra2_body': 'Rapport hebdo automatique aux vendeurs sur les visites et retours. Séquence de nurturing pour les prospects acheteurs qui ne sont pas encore décidés.',
        'infra3_title': 'Pipeline GHL — vue en temps réel sur tous les dossiers',
        'infra3_body': 'Toutes les opportunités actives dans un tableau de bord. Alertes automatiques sur les mandats sans activité depuis X jours.',
        'ticket_setup': '3 000 – 9 000 €',
        'ticket_retainer': '700 – 2 000 €',
        'student_initials': '→',
        'student_name': 'Programme Scaling Lab\'',
        'student_before': '',
        'student_after': '',
        'student_delay': '',
        'student_niche': 'Niche immobilier',
        'student_desc': 'L\'immobilier est une des niches les plus enseignées dans le programme. Les agences ont le budget, comprennent la valeur d\'un système de qualification rapide, et les mandats perdus constituent une douleur immédiate et mesurable.',
        'parent_page_name': 'Immobilier',
    },
    'experts-comptables': {
        'label': 'Experts-comptables',
        'label_raw': 'Experts-comptables',
        'title_short': 'Experts-Comptables',
        'pill_text': 'Analyse de niche · Experts-comptables',
        'h1_line1': 'Agence IA pour les experts-comptables',
        'stat1_num': '22 000', 'stat1_label': 'Cabinets en France',
        'stat2_num': '83%', 'stat2_label': 'Servent des TPE',
        'stat3_num': '2-7k€', 'stat3_label': 'Ticket setup typique',
        'national_count': 22000,
        'market_body': 'La profession comptable en France compte 22 000 cabinets pour 16 milliards d\'euros de chiffre d\'affaires global. 83% de leur clientèle sont des TPE et indépendants. Un marché captif, mais en sous-exploitation commerciale totale.',
        'pain1_title': 'Les leads entrent dans la boîte mail et ne ressortent pas',
        'pain1_body': 'Un prospect envoie un email de demande de devis. Il attend 3 à 5 jours. La réponse arrive sans qualification de son besoin réel. 40-60% de ces leads ne convertissent jamais faute de suivi structuré.',
        'pain2_title': 'La saisonnalité fiscale bloque la prospection 4 mois par an',
        'pain2_body': 'De janvier à avril : bilans, liasses fiscales, déclarations. Impossible de prospecter. Et en mai, quand le flux se libère, il n\'y a aucun pipeline chaud pour convertir rapidement.',
        'pain3_title': 'Invisible sur Google pour les nouvelles entreprises',
        'pain3_body': 'Une entreprise qui se crée cherche un expert-comptable sur Google. Le cabinet local n\'apparaît pas — pas de fiche optimisée, pas de contenu local, pas de système d\'avis. Le prospect signe avec un cabinet 100% en ligne.',
        'infra1_title': 'Chatbot de qualification sur le site du cabinet',
        'infra1_body': 'Filtre type de structure (SASU, SCI, auto-entrepreneur), régime fiscal, besoin prioritaire. Les prospects qualifiés reçoivent un lien de RDV automatique. L\'associé reçoit une fiche complète avant l\'appel.',
        'infra2_title': 'Séquences nurturing hors-saison (mai–décembre)',
        'infra2_body': 'Pipeline de prospects chauds construit pendant les 8 mois calmes, prêt à convertir en janvier. Email + SMS automatiques toutes les 3 semaines sur les leads non encore signés.',
        'infra3_title': 'Visibilité locale Google + collecte d\'avis automatique',
        'infra3_body': 'Chaque nouveau client signé déclenche une demande d\'avis Google automatique. En 6 mois, un cabinet peut passer de 4 à 40+ avis et remonter dans les résultats locaux.',
        'ticket_setup': '2 000 – 7 000 €',
        'ticket_retainer': '500 – 1 500 €',
        'student_initials': 'A',
        'student_name': 'Abdou',
        'student_before': '0',
        'student_after': '15 000 $',
        'student_delay': '6 mois',
        'student_niche': 'Niche comptables (marché US)',
        'student_desc': 'Abdou est parti de zéro et a atteint 15 000 $/mois en 6 mois en ciblant les cabinets comptables. La clé : ne jamais dire "IA" — parler uniquement de CRM, automatisation commerciale, et nouveaux clients.',
        'parent_page_name': 'Experts-Comptables',
    },
    'coaching-consultants': {
        'label': 'Coaching, consulting &amp; infopreneurs',
        'label_raw': 'Coaching, consulting & infopreneurs',
        'title_short': 'Coaching & Consultants',
        'pill_text': 'Analyse de niche · Coaching & consultants',
        'h1_line1': 'Agence IA pour les coachs & consultants',
        'stat1_num': '750M€', 'stat1_label': 'Marché en France',
        'stat2_num': '80%', 'stat2_label': 'Gagnent &lt;1 000€/mois',
        'stat3_num': '3-8k€', 'stat3_label': 'Ticket setup typique',
        'national_count': 15000,
        'market_body': 'Le marché du coaching et de l\'infopreneuriat en France pèse 750 millions d\'euros et croît de 10 à 12% par an. Plus de 15 000 professionnels actifs — mais 80% n\'ont aucun système commercial structuré pour générer des leads qualifiés en continu.',
        'pain1_title': 'Aucun système pour générer des leads qualifiés en continu',
        'pain1_body': 'La majorité des coachs génèrent leurs clients via le contenu organique et le bouche-à-oreille. Ça plafonne rapidement. 80% abandonnent dans les 12 à 18 mois faute de stratégie commerciale scalable.',
        'pain2_title': 'Les prospects arrivent mais ne sont jamais relancés',
        'pain2_body': 'Un coach qui publie du contenu génère de l\'intérêt : commentaires, DMs, inscriptions à la liste. Sans séquence de nurturing structurée, ces contacts refroidissent en quelques jours. La relance manuelle est chronophage et souvent abandonnée.',
        'pain3_title': 'Zéro qualification avant l\'appel découverte',
        'pain3_body': '8 appels par semaine dont 5 avec des gens hors budget ou hors cible = 5 à 7 heures perdues pour rien. Un chatbot de pré-qualification filtre avant le premier contact humain.',
        'infra1_title': 'Chatbot de qualification DMs Instagram / page de capture',
        'infra1_body': 'Pose 4 à 5 questions (niche, problématique, budget, délai). Les prospects qualifiés reçoivent un lien Calendly automatique. Les autres reçoivent du contenu de nurturing.',
        'infra2_title': 'Séquence email/SMS nurturing 14-21 jours',
        'infra2_body': '6 à 8 emails sur 3 semaines + SMS de relance à J+7 et J+14. Taux de prise de RDV sur liste froide : de 3-5% à 12-18%.',
        'infra3_title': 'Pipeline CRM GoHighLevel',
        'infra3_body': 'Toutes les conversations, leads qualifiés, RDV et deals en cours dans une interface. Vue pipeline en colonnes, alertes sur les prospects sans activité depuis X jours.',
        'ticket_setup': '3 000 – 8 000 €',
        'ticket_retainer': '700 – 1 500 €',
        'student_initials': 'A&amp;M',
        'student_name': 'Arthur &amp; Matis',
        'student_before': '1 000 €',
        'student_after': '10 000 €',
        'student_delay': '110 jours',
        'student_niche': 'Niche infopreneurs &amp; coaching',
        'student_desc': 'Arthur &amp; Matis ont ciblé les coachs et infopreneurs dès le début. En 110 jours, ils sont passés de 1 000 à 10 000 €/mois. La niche est accessible, les clients comprennent la valeur d\'un système commercial.',
        'parent_page_name': 'Coaching & Consultants',
    },
    'restaurants': {
        'label': 'Restauration &amp; food service',
        'label_raw': 'Restauration & food service',
        'title_short': 'Restaurants',
        'pill_text': 'Analyse de niche · Restauration',
        'h1_line1': 'Agence IA pour les restaurants',
        'stat1_num': '175 000', 'stat1_label': 'Restaurants en France',
        'stat2_num': '70%', 'stat2_label': 'Clients perdus sans relance',
        'stat3_num': '2-5k€', 'stat3_label': 'Ticket setup typique',
        'national_count': 175000,
        'market_body': 'La restauration est le secteur avec la plus forte densité de TPE en France : 175 000 établissements, dont 80% sont gérés sans équipe marketing. La clientèle est locale, la demande est là — mais 70% des clients qui ne reviennent pas le font uniquement par manque de sollicitation.',
        'pain1_title': 'Les clients satisfaits ne reviennent pas — faute de relance',
        'pain1_body': 'Un client satisfait qui ne reçoit aucun message de suivi ne reviendra pas spontanément dans 70% des cas. Sans séquence SMS ou email post-visite avec une offre de retour, le chiffre d\'affaires de fidélisation est structurellement sous-exploité.',
        'pain2_title': 'Réputation Google mal gérée — avis manquants ou sans réponse',
        'pain2_body': 'Un restaurant avec moins de 50 avis Google est invisible face à ses concurrents. La majorité des propriétaires ne demandent jamais d\'avis à leurs clients — par manque de système. Résultat : les mauvais avis dominent et la note stagne.',
        'pain3_title': 'No-show et réservations non confirmées — 15-20% des créneaux perdus',
        'pain3_body': 'Entre 15 et 20% des tables réservées ne sont jamais honorées. Sans rappel automatique J-1 et J-2, les propriétaires ne peuvent pas réaffecter ces créneaux. Du chiffre d\'affaires perdu chaque week-end.',
        'infra1_title': 'Séquence SMS fidélisation post-visite J+14 & J+45',
        'infra1_body': 'Un SMS automatique 2 semaines après la visite avec une offre ciblée (menu du moment, soirée spéciale). Taux de retour sur clients passés : +25-40% vs sans système.',
        'infra2_title': 'Automatisation avis Google après chaque repas',
        'infra2_body': 'Demande d\'avis automatique via SMS 2h après la visite. Un restaurant peut passer de 30 à 150 avis en 3 mois. L\'algorithme Google booste automatiquement la visibilité locale.',
        'infra3_title': 'Rappel de réservation automatique J-2 et J-1',
        'infra3_body': 'SMS de confirmation envoyé J-2 avec option de report. Réduction des no-shows de 50-65%. Les créneaux libérés sont proposés à une liste d\'attente automatique.',
        'ticket_setup': '2 000 – 5 000 €',
        'ticket_retainer': '400 – 900 €',
        'student_initials': '→',
        'student_name': 'Programme Scaling Lab\'',
        'student_before': '',
        'student_after': '',
        'student_delay': '',
        'student_niche': 'Niche restauration',
        'student_desc': 'La restauration est une des niches à fort volume enseignées dans le programme. Les propriétaires comprennent immédiatement la valeur d\'un système qui ramène leurs anciens clients et réduit les no-shows — deux douleurs quotidiennes avec un ROI mesurable dès le premier mois.',
        'parent_page_name': 'Restaurants',
    },
    'solaire': {
        'label': 'Installateurs solaires &amp; photovoltaïque',
        'label_raw': 'Installateurs solaires & photovoltaïque',
        'title_short': 'Solaire & Photovoltaïque',
        'pill_text': 'Analyse de niche · Solaire & photovoltaïque',
        'h1_line1': 'Agence IA pour les installateurs solaires',
        'stat1_num': '4 500', 'stat1_label': 'Installateurs actifs en France',
        'stat2_num': '×3', 'stat2_label': 'Croissance du marché 2020–2024',
        'stat3_num': '2,5-6k€', 'stat3_label': 'Ticket setup typique',
        'national_count': 4500,
        'market_body': 'Le marché du photovoltaïque en France a triplé entre 2020 et 2024. Plus de 4 500 installateurs actifs — et une demande portée par les aides d\'État. Le problème : la quasi-totalité achètent leurs leads sur des plateformes tierces à 60-90€ pièce, partagés avec 3 à 5 concurrents.',
        'pain1_title': 'Dépendance aux leads achetés — coûteux, partagés, mal qualifiés',
        'pain1_body': 'Les agrégateurs vendent des leads photovoltaïque entre 60 et 90€ pièce — et les revendent à plusieurs installateurs simultanément. C\'est une course au premier contact, avec des marges compressées et aucun actif commercial propre.',
        'pain2_title': 'Devis envoyés sans relance — taux de conversion sous 30%',
        'pain2_body': 'Après la visite technique, l\'installateur envoie le devis et attend. Sans relance à J+3, J+7 et J+14, les prospects refroidissent. Le concurrent qui relance en premier signe.',
        'pain3_title': 'Appels entrants non qualifiés — hors zone, sans budget, toiture inadaptée',
        'pain3_body': '40 à 60% du temps commercial est perdu à qualifier des prospects qui ne convertiront jamais : hors zone d\'intervention, locataires, toitures non adaptées ou budget trop faible. Un chatbot de pré-qualification élimine ce gâchis.',
        'infra1_title': 'Chatbot de pré-qualification zone / toiture / budget',
        'infra1_body': 'Filtre en amont : département d\'intervention, type et orientation de toiture, surface, budget estimé. Seules les demandes viables arrivent à l\'installateur. Gain de temps : 5-8h/semaine.',
        'infra2_title': 'Séquence relance devis J+3 / J+7 / J+14 SMS+email',
        'infra2_body': 'Chaque devis envoyé déclenche une séquence automatique. Taux de conversion : de 28% à 45-55% avec 3 relances bien timées.',
        'infra3_title': 'Funnel Meta Ads + IA → RDV visite technique qualifié',
        'infra3_body': 'Publicités Meta ciblées propriétaires dans la zone d\'intervention. L\'IA qualifie les clics et ne book que les prospects éligibles. Coût par RDV qualifié : 15-30€ vs 60-90€ sur plateforme.',
        'ticket_setup': '2 500 – 6 000 €',
        'ticket_retainer': '500 – 1 200 €',
        'student_initials': '→',
        'student_name': 'Programme Scaling Lab\'',
        'student_before': '',
        'student_after': '',
        'student_delay': '',
        'student_niche': 'Niche solaire & photovoltaïque',
        'student_desc': 'Le solaire est une niche à haute valeur et faible concurrence IA. Les installateurs ont le budget, comprennent la notion de ROI sur leads, et la douleur des leads partagés achetés à prix fort est immédiate et universelle. Un des meilleurs angles pour démarrer une agence en 2025.',
        'parent_page_name': 'Solaire & Photovoltaïque',
    },
    'dentistes': {
        'label': 'Cabinets dentaires',
        'label_raw': 'Cabinets dentaires',
        'title_short': 'Dentistes & Cabinets Dentaires',
        'pill_text': 'Analyse de niche · Cabinets dentaires',
        'h1_line1': 'Agence IA pour les cabinets dentaires',
        'stat1_num': '42 000', 'stat1_label': 'Chirurgiens-dentistes en France',
        'stat2_num': '20-25%', 'stat2_label': 'Taux de no-show moyen',
        'stat3_num': '3-7k€', 'stat3_label': 'Ticket setup typique',
        'national_count': 42000,
        'market_body': 'La France compte 42 000 chirurgiens-dentistes pour un marché de 12 milliards d\'euros. Chaque cabinet gère en moyenne 1 500 patients actifs — et perd entre 200 et 400€ par no-show, chaque semaine, faute de rappel automatisé.',
        'pain1_title': 'No-show et annulations tardives — 20-25% des créneaux perdus',
        'pain1_body': 'Un cabinet dentaire perd entre 5 et 8 créneaux par semaine à cause des no-shows. À 200-300€ par acte moyen, c\'est 1 000 à 2 400€ perdus chaque semaine. Sans rappel automatique, ce chiffre ne bouge pas.',
        'pain2_title': 'Rappels de soins jamais effectués — détartrage, suivi, implant',
        'pain2_body': '40 à 60% des patients qui ont besoin d\'un rappel à 6 ou 12 mois ne reviennent pas parce que personne ne les a contactés. Les assistantes sont débordées. Sans automatisation, ces rappels ne se font tout simplement pas.',
        'pain3_title': 'Zéro système d\'acquisition de nouveaux patients',
        'pain3_body': 'La quasi-totalité des dentistes dépendent uniquement du bouche-à-oreille. Les cabinets avec peu d\'avis Google sont invisibles pour toute personne qui déménage ou cherche un nouveau praticien. Un actif numérique inexploité.',
        'infra1_title': 'Rappel RDV automatique J-2 et J-1 par SMS — no-show divisé par 3',
        'infra1_body': 'SMS automatiques J-2 avec option de report, J-1 de confirmation. Les créneaux annulés à 48h sont immédiatement proposés sur liste d\'attente. Taux de no-show : de 22% à moins de 8%.',
        'infra2_title': 'Séquence relance rappels de soins à 6 et 12 mois post-acte',
        'infra2_body': 'Chaque acte déclenche une relance automatique SMS + email à 5 mois (pour rappel 6 mois) et 11 mois (rappel 1 an). Taux de retour sur rappels de soins : +40-60%.',
        'infra3_title': 'Automatisation avis Google + pipeline de nouveaux patients',
        'infra3_body': 'Demande d\'avis automatique après chaque consultation. En 3 mois, un cabinet peut passer de 20 à 100+ avis. Associé à une fiche Google Business optimisée, la visibilité locale double.',
        'ticket_setup': '3 000 – 7 000 €',
        'ticket_retainer': '600 – 1 400 €',
        'student_initials': '→',
        'student_name': 'Programme Scaling Lab\'',
        'student_before': '',
        'student_after': '',
        'student_delay': '',
        'student_niche': 'Niche cabinets dentaires',
        'student_desc': 'Les cabinets dentaires ont un ROI immédiat et mesurable : chaque no-show évité = 200-300€ récupérés. Le ticket est élevé, les praticiens comprennent les chiffres, et la douleur est quotidienne. Une des niches les plus simples à vendre pour une agence IA débutante.',
        'parent_page_name': 'Dentistes & Cabinets Dentaires',
    },
    'therapeutes': {
        'label': 'Thérapeutes &amp; praticiens bien-être',
        'label_raw': 'Thérapeutes & praticiens bien-être',
        'title_short': 'Thérapeutes & Bien-Être',
        'pill_text': 'Analyse de niche · Thérapeutes & bien-être',
        'h1_line1': 'Agence IA pour les thérapeutes & praticiens',
        'stat1_num': '30 000', 'stat1_label': 'Praticiens en France',
        'stat2_num': '90%', 'stat2_label': 'Dépendent du bouche-à-oreille',
        'stat3_num': '2-5k€', 'stat3_label': 'Ticket setup typique',
        'national_count': 30000,
        'market_body': 'Le marché du bien-être et de la thérapie en France compte plus de 30 000 praticiens actifs : psychologues, coachs certifiés, thérapeutes, hypnothérapeutes, sophrologues. La demande est en forte croissance — mais 90% de ces praticiens dépendent exclusivement du bouche-à-oreille pour remplir leur agenda.',
        'pain1_title': 'Bouche-à-oreille exclusif — croissance structurellement plafonnée',
        'pain1_body': '90% des thérapeutes n\'ont aucun levier commercial autre que les recommandations. Ça marche jusqu\'à un certain niveau, puis ça plafonne. Impossible de décider de remplir son agenda en 30 jours si tout repose sur le réseau.',
        'pain2_title': 'Les prospects qui se renseignent ne sont jamais relancés',
        'pain2_body': 'Un visiteur du site qui laisse ses coordonnées pour se renseigner n\'est pas rappelé dans l\'heure. Il contacte un autre praticien. Sans séquence de nurturing automatique, 60-70% de ces leads disparaissent en 48h.',
        'pain3_title': 'Zéro qualification avant le premier appel — du temps perdu chaque semaine',
        'pain3_body': 'Des appels de 20-30 minutes avec des gens hors cible (mauvaise spécialité, hors budget, fausse urgence) représentent 3 à 5 heures perdues par semaine. Un chatbot de pré-qualification élimine ce gâchis.',
        'infra1_title': 'Chatbot de qualification sur site + DMs Instagram',
        'infra1_body': 'Questions de filtrage : type de problématique, modalité souhaitée (présentiel/distanciel), disponibilité, budget. Les candidats qualifiés reçoivent un lien de réservation automatique.',
        'infra2_title': 'Séquence email/SMS nurturing 14 jours sur leads non convertis',
        'infra2_body': '5 à 7 emails sur 2 semaines + 2 SMS de relance. Taux de prise de premier RDV sur liste froide : de 5% à 18-25%.',
        'infra3_title': 'Pipeline GHL + automatisation avis et réputation',
        'infra3_body': 'Toutes les demandes, RDV et séances en cours dans un tableau de bord. Avis Google automatiques après chaque consultation. En 3 mois, domination des recherches locales.',
        'ticket_setup': '2 000 – 5 000 €',
        'ticket_retainer': '500 – 1 200 €',
        'student_initials': 'S',
        'student_name': 'Sally',
        'student_before': '0',
        'student_after': '18 000 €',
        'student_delay': 'quelques mois',
        'student_niche': 'Niche thérapeutes &amp; bien-être',
        'student_desc': 'Sally est partie de zéro — salariée sans expérience en agence — pour atteindre 18 000 €/mois en ciblant les thérapeutes et praticiens bien-être. La niche comprend immédiatement la valeur d\'un système qui remplace le bouche-à-oreille imprévisible par un flux de clients qualifiés.',
        'parent_page_name': 'Thérapeutes & Bien-Être',
    },
    'avocats': {
        'label': 'Cabinets d\'avocats',
        'label_raw': 'Cabinets d\'avocats',
        'title_short': 'Avocats & Cabinets Juridiques',
        'pill_text': 'Analyse de niche · Avocats',
        'h1_line1': 'Agence IA pour les cabinets d\'avocats',
        'stat1_num': '20 000', 'stat1_label': 'Cabinets en France',
        'stat2_num': '40-60%', 'stat2_label': 'Leads perdus faute de suivi',
        'stat3_num': '2,5-8k€', 'stat3_label': 'Ticket setup typique',
        'national_count': 20000,
        'market_body': 'La profession d\'avocat en France compte 20 000 cabinets pour 8 milliards d\'euros de chiffre d\'affaires. La compétition pour les nouveaux clients est féroce — et pourtant, 80% des cabinets n\'ont aucun système commercial pour qualifier et convertir les prospects entrants.',
        'pain1_title': 'Prospects entrants non qualifiés — du temps facturable perdu',
        'pain1_body': 'Un cabinet reçoit des demandes par email, téléphone, formulaire — sans filtre. 40 à 60% de ces contacts sont hors expertise, hors budget ou hors urgence. Ce temps de qualification représente 5 à 10 heures par semaine pour l\'avocat lui-même.',
        'pain2_title': 'Délai de réponse = prospect perdu (marché ultra-concurrentiel)',
        'pain2_body': 'En droit de la famille, du travail ou commercial, le prospect contacte 3 à 5 cabinets simultanément. Le premier à répondre avec une proposition claire empoche le dossier. La moyenne de réponse en cabinet : 24 à 72 heures.',
        'pain3_title': 'Aucun suivi des prospects froids — pipeline qui disparaît',
        'pain3_body': 'Un prospect qui ne signe pas immédiatement est rarement relancé. Sans système de suivi, 70% des contacts entrants sont perdus en moins d\'une semaine. Pourtant, 30% de ces prospects finissent par signer — chez un concurrent qui a relancé.',
        'infra1_title': 'Chatbot de qualification — filtrage par domaine et urgence',
        'infra1_body': 'Le chatbot filtre domaine de droit, type de problème, urgence et budget avant tout contact humain. L\'avocat reçoit une fiche client complète avant le premier appel. Temps gagné : 5 à 8h/semaine.',
        'infra2_title': 'Séquence relance prospects froids J+3 / J+7 / J+21',
        'infra2_body': 'Email automatique avec ressource utile (guide, checklist légale liée à leur problème). Maintient le cabinet top-of-mind. Taux de conversion sur prospects froids relancés : ×2 à ×3.',
        'infra3_title': 'Pipeline CRM + automatisation avis Google',
        'infra3_body': 'Tous les dossiers en cours, prospects qualifiés et leads en attente dans une interface. Demande d\'avis automatique après chaque dossier clos. La réputation digitale est le premier filtre de qualification naturelle.',
        'ticket_setup': '2 500 – 8 000 €',
        'ticket_retainer': '600 – 1 500 €',
        'student_initials': '→',
        'student_name': 'Programme Scaling Lab\'',
        'student_before': '',
        'student_after': '',
        'student_delay': '',
        'student_niche': 'Niche cabinets juridiques',
        'student_desc': 'Les avocats ont un ticket horaire élevé et une douleur concrète : du temps facturable perdu en qualification de prospects hors cible. Le premier cabinet qui implémente un système de qualification automatique dans sa ville capte une longueur d\'avance structurelle sur tous ses concurrents.',
        'parent_page_name': 'Avocats & Cabinets Juridiques',
    },
    'salons-coiffure': {
        'label': 'Salons de coiffure &amp; barbershops',
        'label_raw': 'Salons de coiffure & barbershops',
        'title_short': 'Coiffure & Barbershops',
        'pill_text': 'Analyse de niche · Coiffure & barbershops',
        'h1_line1': 'Agence IA pour les salons de coiffure',
        'stat1_num': '85 000', 'stat1_label': 'Salons en France',
        'stat2_num': '40-50%', 'stat2_label': 'Créneaux vides en semaine',
        'stat3_num': '1,5-4k€', 'stat3_label': 'Ticket setup typique',
        'national_count': 85000,
        'market_body': 'Avec 85 000 salons de coiffure et barbershops en France, c\'est un des secteurs les plus fragmentés du commerce local. La douleur principale est universelle : les clients satisfaits reviennent quand ils y pensent. Sans relance automatique, l\'intervalle entre deux visites s\'allonge — et les revenus stagnent.',
        'pain1_title': 'Les clients ne sont jamais relancés pour leur prochain passage',
        'pain1_body': 'Un client couleur ou balayage doit revenir dans 6 à 8 semaines. Un client coupe toutes les 4 à 6 semaines. Sans relance automatique au bon moment, l\'intervalle moyen passe à 10-12 semaines. Chaque semaine de décalage = du chiffre d\'affaires perdu.',
        'pain2_title': 'L\'agenda est plein le samedi mais vide en semaine',
        'pain2_body': 'Les créneaux de semaine sont sous-remplis en moyenne à 40-50%. La majorité des salons n\'ont aucun système pour proposer proactivement ces créneaux à leur base de clients existants.',
        'pain3_title': 'Aucun programme de fidélisation actif — clients perdus en silence',
        'pain3_body': 'Un client qui change de salon ne le dit jamais. Il disparaît. Sans suivi actif, le salon perd 15 à 25% de sa clientèle chaque année sans s\'en apercevoir.',
        'infra1_title': 'Séquence SMS relance personnalisée selon le type de prestation',
        'infra1_body': 'J+42 pour couleur/balayage, J+35 pour coupe, J+21 pour barbe. Message personnalisé avec proposition de créneau. Taux de rebooking automatique : +35-50% vs sans relance.',
        'infra2_title': 'Remplissage de l\'agenda semaine via offres ciblées',
        'infra2_body': 'Chaque lundi, SMS automatique aux clients inactifs depuis 6+ semaines avec proposition de créneau en semaine. Taux de remplissage semaine : +20-30%.',
        'infra3_title': 'Pipeline GHL + automatisation avis Google',
        'infra3_body': 'Suivi des clients actifs/inactifs, historique des prestations, déclenchement automatique des relances. Après chaque prestation, demande d\'avis discrète par SMS.',
        'ticket_setup': '1 500 – 4 000 €',
        'ticket_retainer': '400 – 800 €',
        'student_initials': '→',
        'student_name': 'Programme Scaling Lab\'',
        'student_before': '',
        'student_after': '',
        'student_delay': '',
        'student_niche': 'Niche coiffure & barbershops',
        'student_desc': 'La coiffure est une niche à très fort volume avec une douleur immédiate : les clients satisfaits qui ne reviennent pas assez souvent. Le ticket setup est plus accessible que d\'autres niches, ce qui en fait un excellent point d\'entrée pour une première agence IA locale.',
        'parent_page_name': 'Coiffure & Barbershops',
    },
    'e-commerce': {
        'label': 'E-commerce &amp; boutiques en ligne',
        'label_raw': 'E-commerce & boutiques en ligne',
        'title_short': 'E-Commerce',
        'pill_text': 'Analyse de niche · E-commerce',
        'h1_line1': 'Agence IA pour les e-commerces',
        'stat1_num': '200 000', 'stat1_label': 'Boutiques en ligne en France',
        'stat2_num': '78%', 'stat2_label': 'Taux d\'abandon de panier',
        'stat3_num': '2-6k€', 'stat3_label': 'Ticket setup typique',
        'national_count': 200000,
        'market_body': 'La France compte plus de 200 000 sites e-commerce actifs. 85% sont des TPE avec moins de 5 employés. Le problème structurel : 78% des visiteurs qui ajoutent un produit au panier n\'achètent jamais — et aucun système ne les relance.',
        'pain1_title': '78% des paniers abandonnés sans relance automatique',
        'pain1_body': 'La moyenne d\'abandon de panier en France est de 78%. Sans séquence de relance en 1h / 24h / 72h, ces acheteurs potentiels sont perdus. À 100€ de panier moyen, 1 000 paniers abandonnés/mois représentent 80-150 ventes supplémentaires récupérables.',
        'pain2_title': 'Clients one-shot jamais réactivés — base email inexploitée',
        'pain2_body': '60% des clients d\'un e-commerce ne commandent qu\'une seule fois. La base email s\'accumule mais n\'est jamais travaillée. Sans séquence win-back à 45, 90 et 180 jours, ces clients partent chez un concurrent sans même s\'en rendre compte.',
        'pain3_title': 'Zéro séquence post-achat — opportunités d\'upsell systématiquement ratées',
        'pain3_body': 'La période post-achat est le meilleur moment pour proposer un produit complémentaire ou obtenir un avis. Sans automatisation, ce moment est systématiquement raté : pas d\'avis, pas d\'upsell, client qui oublie la marque en 3 semaines.',
        'infra1_title': 'Séquence relance panier abandonné — 1h / 24h / 72h',
        'infra1_body': 'Email + SMS automatiques avec l\'image du produit, un argument de réassurance et une réduction d\'urgence (optionnelle). Taux de récupération panier : 8-15% des abandons.',
        'infra2_title': 'Séquence win-back clients inactifs (45 / 90 / 180 jours)',
        'infra2_body': 'Segmentation automatique des clients selon leur dernière commande. Email de réactivation avec offre personnalisée. Taux de réactivation sur clients dormants de 45-90 jours : 5-12%.',
        'infra3_title': 'Post-achat automatisé — cross-sell + collecte d\'avis',
        'infra3_body': 'J+3 : contenu / conseil d\'utilisation. J+7 : demande d\'avis. J+14 : recommandation produit complémentaire. Customer Lifetime Value en hausse de 25-40%.',
        'ticket_setup': '2 000 – 6 000 €',
        'ticket_retainer': '500 – 1 500 €',
        'student_initials': '→',
        'student_name': 'Programme Scaling Lab\'',
        'student_before': '',
        'student_after': '',
        'student_delay': '',
        'student_niche': 'Niche e-commerce',
        'student_desc': 'L\'e-commerce est une niche à ROI directement mesurable : chaque panier abandonné récupéré = revenus additionnels. Les propriétaires de boutiques comprennent les métriques et mesurent facilement l\'impact. Un des meilleurs profils clients pour construire un retainer durable basé sur la performance.',
        'parent_page_name': 'E-Commerce',
    },
    'garages-auto': {
        'label': 'Garages automobiles &amp; carrosseries',
        'label_raw': 'Garages automobiles & carrosseries',
        'title_short': 'Garages Automobiles',
        'pill_text': 'Analyse de niche · Garages automobiles',
        'h1_line1': 'Agence IA pour les garages automobiles',
        'stat1_num': '35 000', 'stat1_label': 'Garages indépendants en France',
        'stat2_num': '40-60%', 'stat2_label': 'Clients perdus sans rappel révision',
        'stat3_num': '2-5k€', 'stat3_label': 'Ticket setup typique',
        'national_count': 35000,
        'market_body': 'France compte 35 000 garages automobiles et carrosseries indépendants. Ce secteur a une caractéristique unique : chaque véhicule a des échéances prévisibles et connues — contrôle technique, révision, vidange. Ces rendez-vous ne s\'inventent pas, ils se rappellent automatiquement.',
        'pain1_title': 'Le rappel CT et révision n\'est jamais automatisé — 40-60% des clients partent',
        'pain1_body': 'Chaque client qui passe sa vidange représente un futur RDV dans 12 mois — qui n\'est jamais rappelé. 40 à 60% des clients vont ailleurs ou oublient simplement. Du chiffre d\'affaires récurrent qui part à la concurrence par inaction.',
        'pain2_title': 'Appels manqués sur le pont — le prospect appelle le garage d\'à côté',
        'pain2_body': 'Un garagiste sous ses voitures ne répond pas au téléphone. 25-30% des appels ne sont pas pris. Sans message SMS automatique dans les 5 minutes, le client appelle le garage suivant. Chaque appel manqué = un devis potentiellement perdu.',
        'pain3_title': 'Aucun avis Google malgré une base de clients fidèles',
        'pain3_body': 'Le garage local a souvent 200 à 500 clients réguliers — et 15 avis Google. Sans système de demande automatique, les clients satisfaits ne pensent pas à laisser un avis. Les garages avec 100+ avis captent tous les nouveaux clients locaux.',
        'infra1_title': 'Rappel automatique révision / CT à la bonne date',
        'infra1_body': 'Chaque visite déclenche un rappel SMS programmé à J+330 (révision annuelle) ou selon l\'échéance CT. Taux de retour sur rappels automatiques : +45-60% vs sans système.',
        'infra2_title': 'Capture appel manqué + SMS automatique en 5 minutes',
        'infra2_body': 'Tout appel manqué déclenche un SMS automatique. Le client rappelle ou prend RDV en ligne. Taux de contact retrouvé : 60-70% des appels manqués.',
        'infra3_title': 'Automatisation avis Google + pipeline client',
        'infra3_body': 'SMS automatique 1h après la remise des clés avec lien Google avis. En 6 mois, un garage peut passer de 20 à 150+ avis et dominer les recherches locales.',
        'ticket_setup': '2 000 – 5 000 €',
        'ticket_retainer': '400 – 1 000 €',
        'student_initials': '→',
        'student_name': 'Programme Scaling Lab\'',
        'student_before': '',
        'student_after': '',
        'student_delay': '',
        'student_niche': 'Niche garages automobiles',
        'student_desc': 'Le garage automobile est une des niches les plus simples à pitcher : le ROI est immédiat (rappels CT = clients récurrents), les propriétaires comprennent les chiffres, et la concurrence IA est quasi nulle. Un excellent marché pour une première agence IA locale.',
        'parent_page_name': 'Garages Automobiles',
    },
    'kines-osteos': {
        'label': 'Kinésithérapeutes &amp; ostéopathes',
        'label_raw': 'Kinésithérapeutes & ostéopathes',
        'title_short': 'Kinés & Ostéopathes',
        'pill_text': 'Analyse de niche · Kinés & ostéopathes',
        'h1_line1': 'Agence IA pour les kinésithérapeutes & ostéopathes',
        'stat1_num': '120 000', 'stat1_label': 'Praticiens en France',
        'stat2_num': '30-50%', 'stat2_label': 'Patients perdus post-protocole',
        'stat3_num': '2-5k€', 'stat3_label': 'Ticket setup typique',
        'national_count': 120000,
        'market_body': 'La France compte plus de 120 000 masseurs-kinésithérapeutes et ostéopathes. La majorité exercent en libéral et ont une liste d\'attente. Mais sans suivi de fin de protocole, les patients disparaissent — et rechutent chez un autre praticien.',
        'pain1_title': 'Fin de protocole sans suivi — rechute et perte du patient',
        'pain1_body': 'Un patient qui termine un protocole pour une lombalgie ne reçoit jamais de suivi. Sans rappel à 30 et 90 jours, il ne consulte qu\'en cas de rechute — parfois chez un autre praticien. 30 à 50% des patients potentiellement récurrents sont ainsi perdus chaque année.',
        'pain2_title': 'Annulations non remplacées — créneaux vides chaque semaine',
        'pain2_body': 'Un kiné ou ostéo perd entre 2 et 5 créneaux par semaine en annulations. Sans liste d\'attente automatisée, ces créneaux restent vides. À 50-70€ par séance, c\'est 100 à 350€ perdus chaque semaine.',
        'pain3_title': 'Aucun programme de prévention générant des consultations récurrentes',
        'pain3_body': 'Les patients ne consultent que quand ça fait mal. Sans programme de suivi préventif automatisé (exercices à J+15, bilan à J+45), le praticien attend la rechute au lieu de créer une relation continue.',
        'infra1_title': 'Séquence suivi post-protocole J+15 / J+30 / J+90',
        'infra1_body': 'Message automatique avec exercices de maintien, bilan de santé et proposition de séance de contrôle. Taux de retour en préventif : +35-50% sur patients sortis de protocole.',
        'infra2_title': 'Notification automatique liste d\'attente en cas d\'annulation',
        'infra2_body': 'Chaque annulation déclenche instantanément un SMS aux 5 premiers patients en liste d\'attente. Taux de remplacement de créneaux : 60-75% des annulations.',
        'infra3_title': 'Pipeline GHL + automatisation avis',
        'infra3_body': 'Suivi des protocoles en cours, rappels programmés et gestion des listes d\'attente dans une interface. Demande d\'avis automatique en fin de protocole.',
        'ticket_setup': '2 000 – 5 000 €',
        'ticket_retainer': '400 – 1 000 €',
        'student_initials': '→',
        'student_name': 'Programme Scaling Lab\'',
        'student_before': '',
        'student_after': '',
        'student_delay': '',
        'student_niche': 'Niche kinés & ostéopathes',
        'student_desc': 'Les kinés et ostéos ont une douleur simple à pitcher : des créneaux annulés non remplacés et des patients qui ne reviennent pas en préventif. L\'automatisation des relances post-protocole est le produit le plus facile à vendre dans cette niche — ROI visible en quelques semaines.',
        'parent_page_name': 'Kinés & Ostéopathes',
    },
    'plombiers-electriciens': {
        'label': 'Plombiers, électriciens &amp; artisans du second œuvre',
        'label_raw': 'Plombiers, électriciens & artisans',
        'title_short': 'Plombiers & Électriciens',
        'pill_text': 'Analyse de niche · Plombiers & électriciens',
        'h1_line1': 'Agence IA pour les plombiers & électriciens',
        'stat1_num': '200 000', 'stat1_label': 'Artisans en France',
        'stat2_num': '25-30%', 'stat2_label': 'Appels manqués non rappelés',
        'stat3_num': '2-5k€', 'stat3_label': 'Ticket setup typique',
        'national_count': 200000,
        'market_body': 'Les plombiers, électriciens et artisans du second œuvre représentent 200 000 entreprises en France. La grande majorité sont des TPE de 1 à 3 personnes — débordées en période de pointe, sans aucun système pour ne pas perdre de leads entre deux chantiers.',
        'pain1_title': 'Appels urgence manqués le soir et le week-end — le client va chez un concurrent',
        'pain1_body': 'Une fuite d\'eau le samedi soir, une panne électrique le dimanche : le client appelle 3 artisans. Celui qui répond en premier a le chantier. Un artisan seul ne peut pas être disponible 24/7. Sans réponse automatique dans les 3 minutes, le prospect est parti.',
        'pain2_title': 'Devis envoyés sans relance — taux de conversion structurellement bas',
        'pain2_body': 'Un artisan envoie un devis et attend. Le prospect compare avec 2 ou 3 autres. Sans relance à J+3 et J+7, le devis refroidit et le client signe avec le concurrent qui a relancé. Pourtant, 70% des prospects finissent par signer l\'un des devis reçus.',
        'pain3_title': 'Aucun avis Google malgré des dizaines de clients satisfaits',
        'pain3_body': 'Les clients satisfaits ne pensent pas à laisser un avis spontanément. Sans système automatique, la fiche Google reste à 12 avis pendant 3 ans — alors qu\'un concurrent qui relance systématiquement accumule 100+ avis et capte tous les nouveaux clients locaux.',
        'infra1_title': 'Réponse automatique appel manqué en 3 minutes',
        'infra1_body': 'Tout appel non décroché déclenche un SMS automatique : "Je suis en intervention, je vous rappelle d\'ici [X] heures. Pour une urgence, cliquez ici." Taux de prospects retenus vs appel manqué sans réponse : ×4.',
        'infra2_title': 'Séquence relance devis J+3 / J+7 via SMS + email',
        'infra2_body': 'Relance automatique après chaque devis envoyé. Message simple avec photo d\'un chantier similaire et disponibilité. Taux de conversion : de 28% à 45-55%.',
        'infra3_title': 'Automatisation avis Google post-chantier',
        'infra3_body': 'SMS automatique le lendemain de la fin du chantier avec lien Google avis. En 6 mois, un artisan peut passer de 15 à 80-100 avis et dominer les recherches locales sur sa zone.',
        'ticket_setup': '2 000 – 5 000 €',
        'ticket_retainer': '400 – 1 000 €',
        'student_initials': 'Ar',
        'student_name': 'Arnaud',
        'student_before': '2 000 €',
        'student_after': '8 000 €+',
        'student_delay': 'quelques mois',
        'student_niche': 'Niche artisans &amp; habitat',
        'student_desc': 'Arnaud était en SMMA depuis 7 ans avec 20 clients épuisants à 100-300€/mois. Il a pivoté vers les artisans et l\'habitat avec le Scaling Lab\'. Résultat : 8 000 €+/mois avec beaucoup moins de clients et des marges bien supérieures.',
        'parent_page_name': 'Plombiers & Électriciens',
    },
}

# ─── DONNÉES VILLES ──────────────────────────────────────────────────────────

CITIES = [
    # ── France — Top 10 ─────────────────────────────────────────────────────
    {'slug': 'paris',                   'name': 'Paris',                   'region': 'Île-de-France',               'country': 'France', 'pop': 2161000},
    {'slug': 'marseille',               'name': 'Marseille',               'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 870731},
    {'slug': 'lyon',                    'name': 'Lyon',                    'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 522228},
    {'slug': 'toulouse',                'name': 'Toulouse',                'region': 'Occitanie',                   'country': 'France', 'pop': 479553},
    {'slug': 'nice',                    'name': 'Nice',                    'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 342522},
    {'slug': 'nantes',                  'name': 'Nantes',                  'region': 'Pays de la Loire',            'country': 'France', 'pop': 320732},
    {'slug': 'montpellier',             'name': 'Montpellier',             'region': 'Occitanie',                   'country': 'France', 'pop': 295542},
    {'slug': 'strasbourg',              'name': 'Strasbourg',              'region': 'Grand Est',                   'country': 'France', 'pop': 285083},
    {'slug': 'bordeaux',                'name': 'Bordeaux',                'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 257804},
    {'slug': 'lille',                   'name': 'Lille',                   'region': 'Hauts-de-France',             'country': 'France', 'pop': 236234},
    # ── France — 11-30 ──────────────────────────────────────────────────────
    {'slug': 'rennes',                  'name': 'Rennes',                  'region': 'Bretagne',                    'country': 'France', 'pop': 222567},
    {'slug': 'reims',                   'name': 'Reims',                   'region': 'Grand Est',                   'country': 'France', 'pop': 183113},
    {'slug': 'le-havre',                'name': 'Le Havre',                'region': 'Normandie',                   'country': 'France', 'pop': 173111},
    {'slug': 'saint-etienne',           'name': 'Saint-Étienne',           'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 172950},
    {'slug': 'toulon',                  'name': 'Toulon',                  'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 169561},
    {'slug': 'grenoble',                'name': 'Grenoble',                'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 159183},
    {'slug': 'dijon',                   'name': 'Dijon',                   'region': 'Bourgogne-Franche-Comté',     'country': 'France', 'pop': 156254},
    {'slug': 'angers',                  'name': 'Angers',                  'region': 'Pays de la Loire',            'country': 'France', 'pop': 154508},
    {'slug': 'nimes',                   'name': 'Nîmes',                   'region': 'Occitanie',                   'country': 'France', 'pop': 151075},
    {'slug': 'villeurbanne',            'name': 'Villeurbanne',            'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 151000},
    {'slug': 'aix-en-provence',         'name': 'Aix-en-Provence',        'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 148046},
    {'slug': 'clermont-ferrand',        'name': 'Clermont-Ferrand',        'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 145881},
    {'slug': 'brest',                   'name': 'Brest',                   'region': 'Bretagne',                    'country': 'France', 'pop': 140064},
    {'slug': 'le-mans',                 'name': 'Le Mans',                 'region': 'Pays de la Loire',            'country': 'France', 'pop': 143521},
    {'slug': 'tours',                   'name': 'Tours',                   'region': 'Centre-Val de Loire',         'country': 'France', 'pop': 136500},
    {'slug': 'annecy',                  'name': 'Annecy',                  'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 133800},
    {'slug': 'amiens',                  'name': 'Amiens',                  'region': 'Hauts-de-France',             'country': 'France', 'pop': 133914},
    {'slug': 'limoges',                 'name': 'Limoges',                 'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 128068},
    {'slug': 'perpignan',               'name': 'Perpignan',               'region': 'Occitanie',                   'country': 'France', 'pop': 121158},
    {'slug': 'boulogne-billancourt',    'name': 'Boulogne-Billancourt',    'region': 'Île-de-France',               'country': 'France', 'pop': 120200},
    # ── France — 31-60 ──────────────────────────────────────────────────────
    {'slug': 'metz',                    'name': 'Metz',                    'region': 'Grand Est',                   'country': 'France', 'pop': 118586},
    {'slug': 'besancon',                'name': 'Besançon',                'region': 'Bourgogne-Franche-Comté',     'country': 'France', 'pop': 116914},
    {'slug': 'orleans',                 'name': 'Orléans',                 'region': 'Centre-Val de Loire',         'country': 'France', 'pop': 116400},
    {'slug': 'rouen',                   'name': 'Rouen',                   'region': 'Normandie',                   'country': 'France', 'pop': 113100},
    {'slug': 'argenteuil',              'name': 'Argenteuil',              'region': 'Île-de-France',               'country': 'France', 'pop': 112000},
    {'slug': 'saint-denis',             'name': 'Saint-Denis',             'region': 'Île-de-France',               'country': 'France', 'pop': 111000},
    {'slug': 'montreuil',               'name': 'Montreuil',               'region': 'Île-de-France',               'country': 'France', 'pop': 109000},
    {'slug': 'mulhouse',                'name': 'Mulhouse',                'region': 'Grand Est',                   'country': 'France', 'pop': 108900},
    {'slug': 'caen',                    'name': 'Caen',                    'region': 'Normandie',                   'country': 'France', 'pop': 107200},
    {'slug': 'nancy',                   'name': 'Nancy',                   'region': 'Grand Est',                   'country': 'France', 'pop': 104600},
    {'slug': 'roubaix',                 'name': 'Roubaix',                 'region': 'Hauts-de-France',             'country': 'France', 'pop': 98700},
    {'slug': 'tourcoing',               'name': 'Tourcoing',               'region': 'Hauts-de-France',             'country': 'France', 'pop': 97600},
    {'slug': 'vitry-sur-seine',         'name': 'Vitry-sur-Seine',         'region': 'Île-de-France',               'country': 'France', 'pop': 94000},
    {'slug': 'creteil',                 'name': 'Créteil',                 'region': 'Île-de-France',               'country': 'France', 'pop': 91000},
    {'slug': 'nanterre',                'name': 'Nanterre',                'region': 'Île-de-France',               'country': 'France', 'pop': 91000},
    {'slug': 'avignon',                 'name': 'Avignon',                 'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 90200},
    {'slug': 'dunkerque',               'name': 'Dunkerque',               'region': 'Hauts-de-France',             'country': 'France', 'pop': 90500},
    {'slug': 'poitiers',                'name': 'Poitiers',                'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 89000},
    {'slug': 'asnieres-sur-seine',      'name': 'Asnières-sur-Seine',      'region': 'Île-de-France',               'country': 'France', 'pop': 87500},
    {'slug': 'versailles',              'name': 'Versailles',              'region': 'Île-de-France',               'country': 'France', 'pop': 87000},
    {'slug': 'colombes',                'name': 'Colombes',                'region': 'Île-de-France',               'country': 'France', 'pop': 87000},
    {'slug': 'aubervilliers',           'name': 'Aubervilliers',           'region': 'Île-de-France',               'country': 'France', 'pop': 86000},
    {'slug': 'courbevoie',              'name': 'Courbevoie',              'region': 'Île-de-France',               'country': 'France', 'pop': 84800},
    {'slug': 'rueil-malmaison',         'name': 'Rueil-Malmaison',         'region': 'Île-de-France',               'country': 'France', 'pop': 84200},
    {'slug': 'saint-maur-des-fosses',   'name': 'Saint-Maur-des-Fossés',   'region': 'Île-de-France',               'country': 'France', 'pop': 82000},
    {'slug': 'aulnay-sous-bois',        'name': 'Aulnay-sous-Bois',        'region': 'Île-de-France',               'country': 'France', 'pop': 82000},
    {'slug': 'pau',                     'name': 'Pau',                     'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 81000},
    {'slug': 'la-rochelle',             'name': 'La Rochelle',             'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 79800},
    {'slug': 'champigny-sur-marne',     'name': 'Champigny-sur-Marne',     'region': 'Île-de-France',               'country': 'France', 'pop': 77500},
    {'slug': 'beziers',                 'name': 'Béziers',                 'region': 'Occitanie',                   'country': 'France', 'pop': 77000},
    # ── France — 61-90 ──────────────────────────────────────────────────────
    {'slug': 'calais',                  'name': 'Calais',                  'region': 'Hauts-de-France',             'country': 'France', 'pop': 74500},
    {'slug': 'antibes',                 'name': 'Antibes',                 'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 75000},
    {'slug': 'villeneuve-d-ascq',       'name': 'Villeneuve-d\'Ascq',      'region': 'Hauts-de-France',             'country': 'France', 'pop': 65000},
    {'slug': 'saint-nazaire',           'name': 'Saint-Nazaire',           'region': 'Pays de la Loire',            'country': 'France', 'pop': 67000},
    {'slug': 'merignac',                'name': 'Mérignac',                'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 73000},
    {'slug': 'ajaccio',                 'name': 'Ajaccio',                 'region': 'Corse',                       'country': 'France', 'pop': 71000},
    {'slug': 'colmar',                  'name': 'Colmar',                  'region': 'Grand Est',                   'country': 'France', 'pop': 68000},
    {'slug': 'villejuif',               'name': 'Villejuif',               'region': 'Île-de-France',               'country': 'France', 'pop': 70000},
    {'slug': 'cannes',                  'name': 'Cannes',                  'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 69800},
    {'slug': 'levallois-perret',        'name': 'Levallois-Perret',        'region': 'Île-de-France',               'country': 'France', 'pop': 69500},
    {'slug': 'drancy',                  'name': 'Drancy',                  'region': 'Île-de-France',               'country': 'France', 'pop': 68000},
    {'slug': 'issy-les-moulineaux',     'name': 'Issy-les-Moulineaux',     'region': 'Île-de-France',               'country': 'France', 'pop': 67500},
    {'slug': 'venissieux',              'name': 'Vénissieux',              'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 66000},
    {'slug': 'noisy-le-grand',          'name': 'Noisy-le-Grand',          'region': 'Île-de-France',               'country': 'France', 'pop': 67000},
    {'slug': 'bourges',                 'name': 'Bourges',                 'region': 'Centre-Val de Loire',         'country': 'France', 'pop': 66000},
    {'slug': 'cergy',                   'name': 'Cergy',                   'region': 'Île-de-France',               'country': 'France', 'pop': 65000},
    {'slug': 'la-seyne-sur-mer',        'name': 'La Seyne-sur-Mer',        'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 64000},
    {'slug': 'pessac',                  'name': 'Pessac',                  'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 64000},
    {'slug': 'valence',                 'name': 'Valence',                 'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 63000},
    {'slug': 'quimper',                 'name': 'Quimper',                 'region': 'Bretagne',                    'country': 'France', 'pop': 63000},
    {'slug': 'ivry-sur-seine',          'name': 'Ivry-sur-Seine',          'region': 'Île-de-France',               'country': 'France', 'pop': 62500},
    {'slug': 'neuilly-sur-seine',       'name': 'Neuilly-sur-Seine',       'region': 'Île-de-France',               'country': 'France', 'pop': 62000},
    {'slug': 'troyes',                  'name': 'Troyes',                  'region': 'Grand Est',                   'country': 'France', 'pop': 62000},
    {'slug': 'pantin',                  'name': 'Pantin',                  'region': 'Île-de-France',               'country': 'France', 'pop': 61000},
    {'slug': 'lorient',                 'name': 'Lorient',                 'region': 'Bretagne',                    'country': 'France', 'pop': 59000},
    {'slug': 'chambery',                'name': 'Chambéry',                'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 59000},
    {'slug': 'montauban',               'name': 'Montauban',               'region': 'Occitanie',                   'country': 'France', 'pop': 60000},
    {'slug': 'hyeres',                  'name': 'Hyères',                  'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 58000},
    {'slug': 'epinay-sur-seine',        'name': 'Épinay-sur-Seine',        'region': 'Île-de-France',               'country': 'France', 'pop': 55000},
    {'slug': 'fontenay-sous-bois',      'name': 'Fontenay-sous-Bois',      'region': 'Île-de-France',               'country': 'France', 'pop': 55000},
    # ── France — 91-120 ─────────────────────────────────────────────────────
    {'slug': 'la-roche-sur-yon',        'name': 'La Roche-sur-Yon',        'region': 'Pays de la Loire',            'country': 'France', 'pop': 57000},
    {'slug': 'vannes',                  'name': 'Vannes',                  'region': 'Bretagne',                    'country': 'France', 'pop': 56000},
    {'slug': 'niort',                   'name': 'Niort',                   'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 57000},
    {'slug': 'saint-quentin',           'name': 'Saint-Quentin',           'region': 'Hauts-de-France',             'country': 'France', 'pop': 55000},
    {'slug': 'meaux',                   'name': 'Meaux',                   'region': 'Île-de-France',               'country': 'France', 'pop': 56000},
    {'slug': 'narbonne',                'name': 'Narbonne',                'region': 'Occitanie',                   'country': 'France', 'pop': 54000},
    {'slug': 'frejus',                  'name': 'Fréjus',                  'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 56000},
    {'slug': 'cholet',                  'name': 'Cholet',                  'region': 'Pays de la Loire',            'country': 'France', 'pop': 55000},
    {'slug': 'clamart',                 'name': 'Clamart',                 'region': 'Île-de-France',               'country': 'France', 'pop': 53000},
    {'slug': 'beauvais',                'name': 'Beauvais',                'region': 'Hauts-de-France',             'country': 'France', 'pop': 56000},
    {'slug': 'arles',                   'name': 'Arles',                   'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 53000},
    {'slug': 'evreux',                  'name': 'Évreux',                  'region': 'Normandie',                   'country': 'France', 'pop': 51000},
    {'slug': 'sartrouville',            'name': 'Sartrouville',            'region': 'Île-de-France',               'country': 'France', 'pop': 51000},
    {'slug': 'massy',                   'name': 'Massy',                   'region': 'Île-de-France',               'country': 'France', 'pop': 48000},
    {'slug': 'montrouge',               'name': 'Montrouge',               'region': 'Île-de-France',               'country': 'France', 'pop': 50000},
    {'slug': 'vincennes',               'name': 'Vincennes',               'region': 'Île-de-France',               'country': 'France', 'pop': 50000},
    {'slug': 'albi',                    'name': 'Albi',                    'region': 'Occitanie',                   'country': 'France', 'pop': 49000},
    {'slug': 'laval',                   'name': 'Laval',                   'region': 'Pays de la Loire',            'country': 'France', 'pop': 49000},
    {'slug': 'bayonne',                 'name': 'Bayonne',                 'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 50000},
    {'slug': 'bobigny',                 'name': 'Bobigny',                 'region': 'Île-de-France',               'country': 'France', 'pop': 52000},
    {'slug': 'brive-la-gaillarde',      'name': 'Brive-la-Gaillarde',      'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 47000},
    {'slug': 'blois',                   'name': 'Blois',                   'region': 'Centre-Val de Loire',         'country': 'France', 'pop': 47000},
    {'slug': 'carcassonne',             'name': 'Carcassonne',             'region': 'Occitanie',                   'country': 'France', 'pop': 47000},
    {'slug': 'charleville-mezieres',    'name': 'Charleville-Mézières',    'region': 'Grand Est',                   'country': 'France', 'pop': 48000},
    {'slug': 'vaulx-en-velin',          'name': 'Vaulx-en-Velin',          'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 47000},
    {'slug': 'tarbes',                  'name': 'Tarbes',                  'region': 'Occitanie',                   'country': 'France', 'pop': 44000},
    {'slug': 'belfort',                 'name': 'Belfort',                 'region': 'Bourgogne-Franche-Comté',     'country': 'France', 'pop': 46000},
    {'slug': 'aubagne',                 'name': 'Aubagne',                 'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 46000},
    {'slug': 'cagnes-sur-mer',          'name': 'Cagnes-sur-Mer',          'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 46000},
    {'slug': 'saint-malo',              'name': 'Saint-Malo',              'region': 'Bretagne',                    'country': 'France', 'pop': 46000},
    # ── France — 121-150 ────────────────────────────────────────────────────
    {'slug': 'saint-brieuc',            'name': 'Saint-Brieuc',            'region': 'Bretagne',                    'country': 'France', 'pop': 46000},
    {'slug': 'chalon-sur-saone',        'name': 'Chalon-sur-Saône',        'region': 'Bourgogne-Franche-Comté',     'country': 'France', 'pop': 46000},
    {'slug': 'istres',                  'name': 'Istres',                  'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 43000},
    {'slug': 'salon-de-provence',       'name': 'Salon-de-Provence',       'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 43000},
    {'slug': 'chalons-en-champagne',    'name': 'Châlons-en-Champagne',    'region': 'Grand Est',                   'country': 'France', 'pop': 43000},
    {'slug': 'angouleme',               'name': 'Angoulême',               'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 43000},
    {'slug': 'chateauroux',             'name': 'Châteauroux',             'region': 'Centre-Val de Loire',         'country': 'France', 'pop': 44000},
    {'slug': 'valenciennes',            'name': 'Valenciennes',            'region': 'Hauts-de-France',             'country': 'France', 'pop': 44000},
    {'slug': 'caluire-et-cuire',        'name': 'Caluire-et-Cuire',        'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 43000},
    {'slug': 'arras',                   'name': 'Arras',                   'region': 'Hauts-de-France',             'country': 'France', 'pop': 42000},
    {'slug': 'gap',                     'name': 'Gap',                     'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 41000},
    {'slug': 'thionville',              'name': 'Thionville',              'region': 'Grand Est',                   'country': 'France', 'pop': 41000},
    {'slug': 'boulogne-sur-mer',        'name': 'Boulogne-sur-Mer',        'region': 'Hauts-de-France',             'country': 'France', 'pop': 42000},
    {'slug': 'douai',                   'name': 'Douai',                   'region': 'Hauts-de-France',             'country': 'France', 'pop': 41000},
    {'slug': 'saint-priest',            'name': 'Saint-Priest',            'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 42000},
    {'slug': 'compiegne',               'name': 'Compiègne',               'region': 'Hauts-de-France',             'country': 'France', 'pop': 40000},
    {'slug': 'cherbourg-en-cotentin',   'name': 'Cherbourg-en-Cotentin',   'region': 'Normandie',                   'country': 'France', 'pop': 79000},
    {'slug': 'bron',                    'name': 'Bron',                    'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 40000},
    {'slug': 'chartres',                'name': 'Chartres',                'region': 'Centre-Val de Loire',         'country': 'France', 'pop': 38000},
    {'slug': 'la-ciotat',               'name': 'La Ciotat',               'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 36000},
    {'slug': 'poissy',                  'name': 'Poissy',                  'region': 'Île-de-France',               'country': 'France', 'pop': 38000},
    {'slug': 'echirolles',              'name': 'Échirolles',              'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 36000},
    {'slug': 'villefranche-sur-saone',  'name': 'Villefranche-sur-Saône',  'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 35000},
    {'slug': 'auxerre',                 'name': 'Auxerre',                 'region': 'Bourgogne-Franche-Comté',     'country': 'France', 'pop': 35000},
    {'slug': 'roanne',                  'name': 'Roanne',                  'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 35000},
    {'slug': 'epinal',                  'name': 'Épinal',                  'region': 'Grand Est',                   'country': 'France', 'pop': 31000},
    {'slug': 'lens',                    'name': 'Lens',                    'region': 'Hauts-de-France',             'country': 'France', 'pop': 31000},
    {'slug': 'maubeuge',                'name': 'Maubeuge',                'region': 'Hauts-de-France',             'country': 'France', 'pop': 32000},
    {'slug': 'alencon',                 'name': 'Alençon',                 'region': 'Normandie',                   'country': 'France', 'pop': 27000},
    {'slug': 'montlucon',               'name': 'Montluçon',               'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 37000},
    {'slug': 'macon',                   'name': 'Mâcon',                   'region': 'Bourgogne-Franche-Comté',     'country': 'France', 'pop': 34000},
    # ── France — 151-180 ────────────────────────────────────────────────────
    {'slug': 'agen',                    'name': 'Agen',                    'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 33000},
    {'slug': 'mont-de-marsan',          'name': 'Mont-de-Marsan',          'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 31000},
    {'slug': 'perigueux',               'name': 'Périgueux',               'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 28000},
    {'slug': 'cahors',                  'name': 'Cahors',                  'region': 'Occitanie',                   'country': 'France', 'pop': 20000},
    {'slug': 'rodez',                   'name': 'Rodez',                   'region': 'Occitanie',                   'country': 'France', 'pop': 24000},
    {'slug': 'auch',                    'name': 'Auch',                    'region': 'Occitanie',                   'country': 'France', 'pop': 22000},
    {'slug': 'saintes',                 'name': 'Saintes',                 'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 26000},
    {'slug': 'la-rochelle',             'name': 'La Rochelle',             'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 79800} if False else None,
    {'slug': 'cognac',                  'name': 'Cognac',                  'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 18000},
    {'slug': 'saint-nazaire',           'name': 'Saint-Nazaire',           'region': 'Pays de la Loire',            'country': 'France', 'pop': 67000} if False else None,
    {'slug': 'lorient',                 'name': 'Lorient',                 'region': 'Bretagne',                    'country': 'France', 'pop': 59000} if False else None,
    {'slug': 'quimper',                 'name': 'Quimper',                 'region': 'Bretagne',                    'country': 'France', 'pop': 63000} if False else None,
    {'slug': 'saint-nazaire',           'name': 'Saint-Nazaire',           'region': 'Pays de la Loire',            'country': 'France', 'pop': 67000} if False else None,
    {'slug': 'soissons',                'name': 'Soissons',                'region': 'Hauts-de-France',             'country': 'France', 'pop': 28000},
    {'slug': 'laon',                    'name': 'Laon',                    'region': 'Hauts-de-France',             'country': 'France', 'pop': 25000},
    {'slug': 'creil',                   'name': 'Creil',                   'region': 'Hauts-de-France',             'country': 'France', 'pop': 36000},
    {'slug': 'senlis',                  'name': 'Senlis',                  'region': 'Hauts-de-France',             'country': 'France', 'pop': 17000},
    {'slug': 'chateaudun',              'name': 'Châteaudun',              'region': 'Centre-Val de Loire',         'country': 'France', 'pop': 13000},
    {'slug': 'vendome',                 'name': 'Vendôme',                 'region': 'Centre-Val de Loire',         'country': 'France', 'pop': 18000},
    {'slug': 'lons-le-saunier',         'name': 'Lons-le-Saunier',         'region': 'Bourgogne-Franche-Comté',     'country': 'France', 'pop': 17000},
    {'slug': 'vesoul',                  'name': 'Vesoul',                  'region': 'Bourgogne-Franche-Comté',     'country': 'France', 'pop': 15000},
    {'slug': 'dole',                    'name': 'Dole',                    'region': 'Bourgogne-Franche-Comté',     'country': 'France', 'pop': 23000},
    {'slug': 'pontarlier',              'name': 'Pontarlier',              'region': 'Bourgogne-Franche-Comté',     'country': 'France', 'pop': 19000},
    {'slug': 'montbeliard',             'name': 'Montbéliard',             'region': 'Bourgogne-Franche-Comté',     'country': 'France', 'pop': 25000},
    {'slug': 'colmar',                  'name': 'Colmar',                  'region': 'Grand Est',                   'country': 'France', 'pop': 68000} if False else None,
    {'slug': 'haguenau',                'name': 'Haguenau',                'region': 'Grand Est',                   'country': 'France', 'pop': 36000},
    {'slug': 'saverne',                 'name': 'Saverne',                 'region': 'Grand Est',                   'country': 'France', 'pop': 12000},
    {'slug': 'forbach',                 'name': 'Forbach',                 'region': 'Grand Est',                   'country': 'France', 'pop': 21000},
    {'slug': 'saint-avold',             'name': 'Saint-Avold',             'region': 'Grand Est',                   'country': 'France', 'pop': 16000},
    {'slug': 'bar-le-duc',              'name': 'Bar-le-Duc',              'region': 'Grand Est',                   'country': 'France', 'pop': 15000},
    {'slug': 'saint-dizier',            'name': 'Saint-Dizier',            'region': 'Grand Est',                   'country': 'France', 'pop': 24000},
    {'slug': 'chaumont',                'name': 'Chaumont',                'region': 'Grand Est',                   'country': 'France', 'pop': 21000},
    {'slug': 'vittel',                  'name': 'Vittel',                  'region': 'Grand Est',                   'country': 'France', 'pop': 5000},
    # ── France — 181-210 ────────────────────────────────────────────────────
    {'slug': 'saint-omer',              'name': 'Saint-Omer',              'region': 'Hauts-de-France',             'country': 'France', 'pop': 14000},
    {'slug': 'bethune',                 'name': 'Béthune',                 'region': 'Hauts-de-France',             'country': 'France', 'pop': 25000},
    {'slug': 'cambrai',                 'name': 'Cambrai',                 'region': 'Hauts-de-France',             'country': 'France', 'pop': 33000},
    {'slug': 'abbeville',               'name': 'Abbeville',               'region': 'Hauts-de-France',             'country': 'France', 'pop': 23000},
    {'slug': 'saint-quentin',           'name': 'Saint-Quentin',           'region': 'Hauts-de-France',             'country': 'France', 'pop': 55000} if False else None,
    {'slug': 'hazebrouck',              'name': 'Hazebrouck',              'region': 'Hauts-de-France',             'country': 'France', 'pop': 21000},
    {'slug': 'rouen',                   'name': 'Rouen',                   'region': 'Normandie',                   'country': 'France', 'pop': 113100} if False else None,
    {'slug': 'caen',                    'name': 'Caen',                    'region': 'Normandie',                   'country': 'France', 'pop': 107200} if False else None,
    {'slug': 'dieppe',                  'name': 'Dieppe',                  'region': 'Normandie',                   'country': 'France', 'pop': 29000},
    {'slug': 'elbeuf',                  'name': 'Elbeuf',                  'region': 'Normandie',                   'country': 'France', 'pop': 17000},
    {'slug': 'flers',                   'name': 'Flers',                   'region': 'Normandie',                   'country': 'France', 'pop': 16000},
    {'slug': 'argentan',                'name': 'Argentan',                'region': 'Normandie',                   'country': 'France', 'pop': 15000},
    {'slug': 'lisieux',                 'name': 'Lisieux',                 'region': 'Normandie',                   'country': 'France', 'pop': 20000},
    {'slug': 'bayeux',                  'name': 'Bayeux',                  'region': 'Normandie',                   'country': 'France', 'pop': 13000},
    {'slug': 'saint-lo',                'name': 'Saint-Lô',                'region': 'Normandie',                   'country': 'France', 'pop': 20000},
    {'slug': 'avranches',               'name': 'Avranches',               'region': 'Normandie',                   'country': 'France', 'pop': 7000},
    {'slug': 'falaise',                 'name': 'Falaise',                 'region': 'Normandie',                   'country': 'France', 'pop': 8000},
    {'slug': 'quimperle',               'name': 'Quimperlé',               'region': 'Bretagne',                    'country': 'France', 'pop': 12000},
    {'slug': 'morlaix',                 'name': 'Morlaix',                 'region': 'Bretagne',                    'country': 'France', 'pop': 14000},
    {'slug': 'pontivy',                 'name': 'Pontivy',                 'region': 'Bretagne',                    'country': 'France', 'pop': 14000},
    {'slug': 'lannion',                 'name': 'Lannion',                 'region': 'Bretagne',                    'country': 'France', 'pop': 20000},
    {'slug': 'ploemeur',                'name': 'Ploemeur',                'region': 'Bretagne',                    'country': 'France', 'pop': 18000},
    {'slug': 'saint-herblain',          'name': 'Saint-Herblain',          'region': 'Pays de la Loire',            'country': 'France', 'pop': 46000},
    {'slug': 'saumur',                  'name': 'Saumur',                  'region': 'Pays de la Loire',            'country': 'France', 'pop': 27000},
    {'slug': 'mayenne',                 'name': 'Mayenne',                 'region': 'Pays de la Loire',            'country': 'France', 'pop': 13000},
    {'slug': 'chateau-gontier',         'name': 'Château-Gontier',         'region': 'Pays de la Loire',            'country': 'France', 'pop': 12000},
    {'slug': 'saint-nazaire',           'name': 'Saint-Nazaire',           'region': 'Pays de la Loire',            'country': 'France', 'pop': 67000} if False else None,
    {'slug': 'vitre',                   'name': 'Vitré',                   'region': 'Bretagne',                    'country': 'France', 'pop': 19000},
    {'slug': 'fougeres',                'name': 'Fougères',                'region': 'Bretagne',                    'country': 'France', 'pop': 20000},
    {'slug': 'lamballe',                'name': 'Lamballe',                'region': 'Bretagne',                    'country': 'France', 'pop': 13000},
    # ── France — 211-240 ────────────────────────────────────────────────────
    {'slug': 'vichy',                   'name': 'Vichy',                   'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 25000},
    {'slug': 'issoire',                 'name': 'Issoire',                 'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 13000},
    {'slug': 'riom',                    'name': 'Riom',                    'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 18000},
    {'slug': 'aurillac',                'name': 'Aurillac',                'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 27000},
    {'slug': 'le-puy-en-velay',         'name': 'Le Puy-en-Velay',         'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 19000},
    {'slug': 'moulins',                 'name': 'Moulins',                 'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 19000},
    {'slug': 'bourg-en-bresse',         'name': 'Bourg-en-Bresse',         'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 40000},
    {'slug': 'amboise',                 'name': 'Amboise',                 'region': 'Centre-Val de Loire',         'country': 'France', 'pop': 13000},
    {'slug': 'chatellerault',           'name': 'Châtellerault',           'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 32000},
    {'slug': 'saint-jean-de-luz',       'name': 'Saint-Jean-de-Luz',       'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 13000},
    {'slug': 'dax',                     'name': 'Dax',                     'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 21000},
    {'slug': 'pau',                     'name': 'Pau',                     'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 81000} if False else None,
    {'slug': 'arcachon',                'name': 'Arcachon',                'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 12000},
    {'slug': 'perigueux',               'name': 'Périgueux',               'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 28000} if False else None,
    {'slug': 'rochefort',               'name': 'Rochefort',               'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 24000},
    {'slug': 'saint-georges-de-didonne', 'name': 'Royan',                  'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 18000},
    {'slug': 'marmande',                'name': 'Marmande',                'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 18000},
    {'slug': 'bergerac',                'name': 'Bergerac',                'region': 'Nouvelle-Aquitaine',          'country': 'France', 'pop': 25000},
    {'slug': 'figeac',                  'name': 'Figeac',                  'region': 'Occitanie',                   'country': 'France', 'pop': 10000},
    {'slug': 'millau',                  'name': 'Millau',                  'region': 'Occitanie',                   'country': 'France', 'pop': 22000},
    {'slug': 'sete',                    'name': 'Sète',                    'region': 'Occitanie',                   'country': 'France', 'pop': 44000},
    {'slug': 'ales',                    'name': 'Alès',                    'region': 'Occitanie',                   'country': 'France', 'pop': 41000},
    {'slug': 'montpellier',             'name': 'Montpellier',             'region': 'Occitanie',                   'country': 'France', 'pop': 295542} if False else None,
    {'slug': 'lunel',                   'name': 'Lunel',                   'region': 'Occitanie',                   'country': 'France', 'pop': 26000},
    {'slug': 'castres',                 'name': 'Castres',                 'region': 'Occitanie',                   'country': 'France', 'pop': 43000},
    {'slug': 'pamiers',                 'name': 'Pamiers',                 'region': 'Occitanie',                   'country': 'France', 'pop': 16000},
    {'slug': 'foix',                    'name': 'Foix',                    'region': 'Occitanie',                   'country': 'France', 'pop': 10000},
    {'slug': 'lourdes',                 'name': 'Lourdes',                 'region': 'Occitanie',                   'country': 'France', 'pop': 14000},
    {'slug': 'toulon',                  'name': 'Toulon',                  'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 169561} if False else None,
    {'slug': 'draguignan',              'name': 'Draguignan',              'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 40000},
    # ── France — 241-270 ────────────────────────────────────────────────────
    {'slug': 'martigues',               'name': 'Martigues',               'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 48000},
    {'slug': 'arles',                   'name': 'Arles',                   'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 53000} if False else None,
    {'slug': 'brignoles',               'name': 'Brignoles',               'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 16000},
    {'slug': 'manosque',                'name': 'Manosque',                'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 23000},
    {'slug': 'digne-les-bains',         'name': 'Digne-les-Bains',         'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 16000},
    {'slug': 'grasse',                  'name': 'Grasse',                  'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 52000},
    {'slug': 'vence',                   'name': 'Vence',                   'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 19000},
    {'slug': 'menton',                  'name': 'Menton',                  'region': 'Provence-Alpes-Côte d\'Azur', 'country': 'France', 'pop': 29000},
    {'slug': 'monaco',                  'name': 'Monaco',                  'region': 'Monaco',                      'country': 'France', 'pop': 37000},
    {'slug': 'bastia',                  'name': 'Bastia',                  'region': 'Corse',                       'country': 'France', 'pop': 43000},
    {'slug': 'cayenne',                 'name': 'Cayenne',                 'region': 'Guyane',                      'country': 'France', 'pop': 66000},
    {'slug': 'pointe-a-pitre',          'name': 'Pointe-à-Pitre',          'region': 'Guadeloupe',                  'country': 'France', 'pop': 16000},
    {'slug': 'basse-terre',             'name': 'Basse-Terre',             'region': 'Guadeloupe',                  'country': 'France', 'pop': 11000},
    {'slug': 'saint-pierre-reunion',    'name': 'Saint-Pierre',            'region': 'La Réunion',                  'country': 'France', 'pop': 82000},
    {'slug': 'thionville',              'name': 'Thionville',              'region': 'Grand Est',                   'country': 'France', 'pop': 41000} if False else None,
    {'slug': 'montbeliard',             'name': 'Montbéliard',             'region': 'Bourgogne-Franche-Comté',     'country': 'France', 'pop': 25000} if False else None,
    {'slug': 'annemasse',               'name': 'Annemasse',               'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 33000},
    {'slug': 'cluses',                  'name': 'Cluses',                  'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 18000},
    {'slug': 'thonon-les-bains',        'name': 'Thonon-les-Bains',        'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 35000},
    {'slug': 'aix-les-bains',           'name': 'Aix-les-Bains',           'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 30000},
    {'slug': 'saint-martin-d-heres',    'name': 'Saint-Martin-d\'Hères',   'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 37000},
    {'slug': 'voiron',                  'name': 'Voiron',                  'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 20000},
    {'slug': 'bourgoin-jallieu',        'name': 'Bourgoin-Jallieu',        'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 30000},
    {'slug': 'romans-sur-isere',        'name': 'Romans-sur-Isère',        'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 34000},
    {'slug': 'vienne',                  'name': 'Vienne',                  'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 30000},
    {'slug': 'oyonnax',                 'name': 'Oyonnax',                 'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 22000},
    {'slug': 'pont-de-claix',           'name': 'Pont-de-Claix',           'region': 'Auvergne-Rhône-Alpes',        'country': 'France', 'pop': 11000},
    # ── Belgique (7 villes) ─────────────────────────────────────────────────
    {'slug': 'bruxelles',               'name': 'Bruxelles',               'region': 'Bruxelles-Capitale',          'country': 'Belgique', 'pop': 1208542},
    {'slug': 'charleroi',               'name': 'Charleroi',               'region': 'Province de Hainaut',         'country': 'Belgique', 'pop': 202604},
    {'slug': 'liege',                   'name': 'Liège',                   'region': 'Province de Liège',           'country': 'Belgique', 'pop': 196806},
    {'slug': 'namur',                   'name': 'Namur',                   'region': 'Province de Namur',           'country': 'Belgique', 'pop': 111240},
    {'slug': 'mons',                    'name': 'Mons',                    'region': 'Province de Hainaut',         'country': 'Belgique', 'pop': 95000},
    {'slug': 'la-louviere',             'name': 'La Louvière',             'region': 'Province de Hainaut',         'country': 'Belgique', 'pop': 80000},
    {'slug': 'tournai',                 'name': 'Tournai',                 'region': 'Province de Hainaut',         'country': 'Belgique', 'pop': 69000},
    # ── Suisse (7 villes) ───────────────────────────────────────────────────
    {'slug': 'geneve',                  'name': 'Genève',                  'region': 'Canton de Genève',            'country': 'Suisse', 'pop': 203856},
    {'slug': 'lausanne',                'name': 'Lausanne',                'region': 'Canton de Vaud',              'country': 'Suisse', 'pop': 138905},
    {'slug': 'berne',                   'name': 'Berne',                   'region': 'Canton de Berne',             'country': 'Suisse', 'pop': 133800},
    {'slug': 'sion',                    'name': 'Sion',                    'region': 'Canton du Valais',            'country': 'Suisse', 'pop': 34000},
    {'slug': 'neuchatel',               'name': 'Neuchâtel',               'region': 'Canton de Neuchâtel',         'country': 'Suisse', 'pop': 43000},
    {'slug': 'fribourg',                'name': 'Fribourg',                'region': 'Canton de Fribourg',          'country': 'Suisse', 'pop': 38403},
    {'slug': 'yverdon-les-bains',       'name': 'Yverdon-les-Bains',       'region': 'Canton de Vaud',              'country': 'Suisse', 'pop': 30000},
    # ── Luxembourg ──────────────────────────────────────────────────────────
    {'slug': 'luxembourg',              'name': 'Luxembourg',              'region': 'Luxembourg',                  'country': 'Luxembourg', 'pop': 125000},
    # ── Canada / Québec (3 villes) ──────────────────────────────────────────
    {'slug': 'montreal',                'name': 'Montréal',                'region': 'Québec',                      'country': 'Canada', 'pop': 1762949},
    {'slug': 'quebec',                  'name': 'Québec',                  'region': 'Québec',                      'country': 'Canada', 'pop': 549459},
    {'slug': 'ottawa',                  'name': 'Ottawa',                  'region': 'Ontario',                     'country': 'Canada', 'pop': 994837},
    # ── Maroc (6 villes) ────────────────────────────────────────────────────
    {'slug': 'casablanca',              'name': 'Casablanca',              'region': 'Grand Casablanca-Settat',     'country': 'Maroc', 'pop': 3752000},
    {'slug': 'rabat',                   'name': 'Rabat',                   'region': 'Rabat-Salé-Kénitra',          'country': 'Maroc', 'pop': 577827},
    {'slug': 'marrakech',               'name': 'Marrakech',               'region': 'Marrakech-Safi',              'country': 'Maroc', 'pop': 928850},
    {'slug': 'fes',                     'name': 'Fès',                     'region': 'Fès-Meknès',                  'country': 'Maroc', 'pop': 1150000},
    {'slug': 'tanger',                  'name': 'Tanger',                  'region': 'Tanger-Tétouan-Al Hoceïma',  'country': 'Maroc', 'pop': 947000},
    {'slug': 'agadir',                  'name': 'Agadir',                  'region': 'Souss-Massa',                 'country': 'Maroc', 'pop': 600000},
    # ── Algérie (2 villes) ──────────────────────────────────────────────────
    {'slug': 'alger',                   'name': 'Alger',                   'region': 'Alger',                       'country': 'Algérie', 'pop': 3415811},
    {'slug': 'oran',                    'name': 'Oran',                    'region': 'Oran',                        'country': 'Algérie', 'pop': 803000},
    # ── Tunisie (2 villes) ──────────────────────────────────────────────────
    {'slug': 'tunis',                   'name': 'Tunis',                   'region': 'Gouvernorat de Tunis',        'country': 'Tunisie', 'pop': 638845},
    {'slug': 'sfax',                    'name': 'Sfax',                    'region': 'Gouvernorat de Sfax',         'country': 'Tunisie', 'pop': 330000},
    # ── La Réunion (1 ville) ────────────────────────────────────────────────
    {'slug': 'saint-denis-reunion',     'name': 'Saint-Denis',             'region': 'La Réunion',                  'country': 'La Réunion', 'pop': 145741},
    # ── Martinique (1 ville) ────────────────────────────────────────────────
    {'slug': 'fort-de-france',          'name': 'Fort-de-France',          'region': 'Martinique',                  'country': 'Martinique', 'pop': 79473},
    # ── Sénégal (1 ville) ───────────────────────────────────────────────────
    {'slug': 'dakar',                   'name': 'Dakar',                   'region': 'Région de Dakar',             'country': 'Sénégal', 'pop': 3137196},
    # ── Côte d'Ivoire (1 ville) ─────────────────────────────────────────────
    {'slug': 'abidjan',                 'name': 'Abidjan',                 'region': 'District Autonome d\'Abidjan', 'country': 'Côte d\'Ivoire', 'pop': 5334000},
]
# Filtrer les None (entrées désactivées pour dédoublonnage)
CITIES = [c for c in CITIES if c is not None]

FRANCE_POP = 68_000_000

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def pattern_id(niche_slug, city_slug):
    h = hashlib.md5(f"{niche_slug}-{city_slug}".encode()).hexdigest()[:8]
    return f"gp_{h}"

def local_count(national, city_pop):
    raw = national * city_pop / FRANCE_POP
    if raw < 50:
        return max(int(round(raw / 5) * 5), 5)
    elif raw < 200:
        return int(round(raw / 10) * 10)
    elif raw < 2000:
        return int(round(raw / 50) * 50)
    else:
        return int(round(raw / 100) * 100)

def fmt_count(n):
    return f"{n:,}".replace(",", "\u202f")

# ─── GÉNÉRATEUR HTML ─────────────────────────────────────────────────────────

def generate_page(niche_slug, niche, city):
    n = niche
    c = city
    pid = pattern_id(niche_slug, c['slug'])
    lcount = local_count(n['national_count'], c['pop'])
    lcount_fmt = fmt_count(lcount)
    canonical = f"https://lescalinglab.com/agences/{niche_slug}/{c['slug']}/"
    today = date.today().isoformat()

    is_france = c.get('country', 'France') == 'France'
    city_geo = c['region'] if is_france else c['country']
    city_ctx = f"la région {c['region']}" if is_france else c['country']
    city_prepo = f"en {c['region']}" if is_france else f"en {c['country']}"
    francophonie_txt = "partout en France" if is_france else "partout dans la francophonie"

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{n['title_short']} à {c['name']} — Agence IA | Scaling Lab'</title>
  <meta name="description" content="Environ {lcount_fmt} établissements {n['label_raw'].lower()} à {c['name']} {city_prepo}. Voici comment lancer une agence IA dans cette niche localement — l'opportunité, ce qu'on vend, et le ticket moyen." />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:title" content="{n['title_short']} à {c['name']} — Agence IA | Scaling Lab'" />
  <meta property="og:description" content="~{lcount_fmt} établissements {n['label_raw'].lower()} à {c['name']}. L'opportunité agence IA dans cette niche et dans cette ville." />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:type" content="article" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type":"ListItem","position":1,"name":"Accueil","item":"https://lescalinglab.com/"}},
      {{"@type":"ListItem","position":2,"name":"Niches","item":"https://lescalinglab.com/agences/"}},
      {{"@type":"ListItem","position":3,"name":"{n['parent_page_name']}","item":"https://lescalinglab.com/agences/{niche_slug}/"}},
      {{"@type":"ListItem","position":4,"name":"{c['name']}","item":"{canonical}"}}
    ]
  }}
  </script>

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700;1,900&family=Oswald:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{ extend: {{ colors: {{
        ink: '#06060F', deep: '#0C0C1E',
        primary: '#3B2FE8', bright: '#6055FF', tint: '#C8C4FF'
      }} }} }}
    }}
  </script>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #06060F; color: #fff; font-family: 'Inter', sans-serif; -webkit-font-smoothing: antialiased; }}
    a {{ text-decoration: none; color: inherit; }}
    .display-bold {{ font-family: 'Playfair Display', serif; font-weight: 900; font-style: italic; letter-spacing: -0.04em; line-height: 1; }}
    .heading-oswald {{ font-family: 'Oswald', sans-serif; font-weight: 700; letter-spacing: -0.01em; line-height: 1.05; text-transform: uppercase; }}
    .label {{ font-family: 'Oswald', sans-serif; font-size: 11px; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase; color: #6055FF; }}
    .btn-primary {{
      display: inline-flex; align-items: center; gap: 10px;
      background: linear-gradient(160deg, #5048FF 0%, #3B2FE8 55%, #2E24CC 100%);
      color: #fff; font-family: 'Inter', sans-serif; font-size: 14px; font-weight: 700;
      letter-spacing: 0.02em; padding: 14px 32px; border-radius: 100px;
      border: none; cursor: pointer; position: relative; overflow: hidden; text-decoration: none;
      transition: transform 0.25s cubic-bezier(0.25,0.46,0.45,0.94), box-shadow 0.25s cubic-bezier(0.25,0.46,0.45,0.94);
      box-shadow: 0 0 32px rgba(59,47,232,0.55), 0 6px 24px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.45), inset 0 -1px 0 rgba(0,0,0,0.3);
    }}
    .btn-primary::before {{ content:''; position:absolute; top:0; left:0; right:0; height:48%; background:linear-gradient(180deg,rgba(255,255,255,0.2) 0%,transparent 100%); border-radius:100px 100px 0 0; pointer-events:none; }}
    .btn-primary:hover {{ transform: translateY(-3px) scale(1.03); box-shadow: 0 0 55px rgba(59,47,232,0.7), 0 12px 36px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.55); }}
    .btn-ghost {{
      display: inline-flex; align-items: center; gap: 8px;
      background: rgba(255,255,255,0.04); color: rgba(255,255,255,0.7);
      font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 500;
      padding: 12px 24px; border-radius: 100px; border: 1px solid rgba(255,255,255,0.1);
      transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease; cursor: pointer;
    }}
    .btn-ghost:hover {{ background: rgba(255,255,255,0.08); color: #fff; border-color: rgba(255,255,255,0.2); }}
    .pill {{
      display: inline-flex; align-items: center; gap: 8px;
      font-family: 'Oswald', sans-serif; font-size: 11px; font-weight: 500;
      letter-spacing: 0.18em; text-transform: uppercase; color: rgba(200,196,255,0.8);
      background: rgba(59,47,232,0.15); border: 1px solid rgba(96,85,255,0.3);
      padding: 8px 16px; border-radius: 100px;
    }}
    .pill-dot {{ width: 6px; height: 6px; border-radius: 50%; background: #6055FF; flex-shrink: 0; animation: pulse-dot 2s ease-in-out infinite; }}
    @keyframes pulse-dot {{ 0%,100%{{opacity:1;transform:scale(1)}} 50%{{opacity:0.5;transform:scale(0.75)}} }}
    .glow-card {{ background: rgba(12,12,30,0.7); border: 1px solid rgba(30,30,56,0.8); box-shadow: 0 1px 0 rgba(100,90,255,0.12) inset, 0 0 0 1px rgba(30,30,56,1), 0 20px 60px rgba(0,0,0,0.4); border-radius: 16px; }}
    .glow-card-hover {{ transition: box-shadow 0.3s ease, transform 0.3s ease; }}
    .glow-card-hover:hover {{ box-shadow: 0 1px 0 rgba(100,90,255,0.25) inset, 0 0 0 1px rgba(74,59,255,0.35), 0 24px 60px rgba(59,47,232,0.15), 0 4px 20px rgba(0,0,0,0.5); transform: translateY(-2px); }}
    .stat-card {{ background: rgba(12,12,30,0.6); border: 1px solid rgba(30,30,56,0.7); border-radius: 12px; padding: 20px 24px; text-align: center; }}
    .stat-num {{ font-family: 'Oswald', sans-serif; font-weight: 700; font-size: 28px; background: linear-gradient(135deg,#C8C4FF,#6055FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
    .stat-label {{ font-size: 12px; color: rgba(255,255,255,0.45); margin-top: 4px; }}
    .pain-card {{ background: rgba(12,12,30,0.5); border: 1px solid rgba(59,47,232,0.15); border-radius: 14px; padding: 28px; }}
    .pain-num {{ font-family: 'Oswald', sans-serif; font-weight: 700; font-size: 36px; color: rgba(96,85,255,0.25); line-height: 1; }}
    .infra-item {{ display: flex; gap: 16px; align-items: flex-start; padding: 20px 0; border-bottom: 1px solid rgba(30,30,56,0.6); }}
    .infra-item:last-child {{ border-bottom: none; }}
    .infra-icon {{ width: 36px; height: 36px; border-radius: 8px; background: rgba(59,47,232,0.2); border: 1px solid rgba(96,85,255,0.25); display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 16px; }}
    .result-card {{ background: linear-gradient(135deg, rgba(59,47,232,0.12) 0%, rgba(12,12,30,0.8) 100%); border: 1px solid rgba(96,85,255,0.25); border-radius: 20px; padding: 36px; }}
    .breadcrumb {{ font-size: 12px; color: rgba(255,255,255,0.35); display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }}
    .breadcrumb a:hover {{ color: rgba(255,255,255,0.6); }}
    .hero-bg {{
      background:
        radial-gradient(ellipse 80% 60% at 70% 50%, rgba(43,36,214,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 50% 70% at 20% 80%, rgba(74,59,255,0.08) 0%, transparent 50%),
        #06060F;
    }}
    .section-divider {{ border: none; border-top: 1px solid rgba(30,30,56,0.6); margin: 0; }}
    nav, section, footer {{ position: relative; z-index: 2; }}
    @media (max-width: 768px) {{
      .hide-mobile {{ display: none !important; }}
      .stats-grid {{ grid-template-columns: repeat(2, 1fr) !important; }}
    }}
  </style>
</head>
<body>

<div id="grid-bg" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;overflow:hidden;opacity:0.35;"></div>
<script>
(function(){{
  var el=document.getElementById('grid-bg');
  var id='{pid}';
  var SZ=48,SW=0.5;
  function build(){{
    var W=window.innerWidth,H=window.innerHeight;
    var cols=Math.ceil(W/SZ)+1,rows=Math.ceil(H/SZ)+1;
    var h='',v='';
    for(var i=0;i<=rows;i++) h+='<line x1="0" y1="'+(i*SZ)+'" x2="'+(cols*SZ)+'" y2="'+(i*SZ)+'"/>';
    for(var j=0;j<=cols;j++) v+='<line x1="'+(j*SZ)+'" y1="0" x2="'+(j*SZ)+'" y2="'+(rows*SZ)+'"/>';
    el.innerHTML='<svg width="'+W+'" height="'+H+'" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="'+id+'" cx="60%" cy="40%" r="55%"><stop offset="0%" stop-color="#3B2FE8" stop-opacity="0.55"/><stop offset="60%" stop-color="#3B2FE8" stop-opacity="0.08"/><stop offset="100%" stop-color="#3B2FE8" stop-opacity="0"/></radialGradient></defs><g stroke="url(#'+id+')" stroke-width="'+SW+'" fill="none">'+h+v+'</g></svg>';
  }}
  build();
  window.addEventListener('resize',build);
}})();
</script>

<nav style="position:fixed;top:0;left:0;right:0;z-index:100;backdrop-filter:blur(16px);background:rgba(6,6,15,0.85);border-bottom:1px solid rgba(30,30,56,0.7);">
  <div style="max-width:1100px;margin:0 auto;padding:0 32px;height:64px;display:flex;align-items:center;justify-content:space-between;">
    <a href="https://lescalinglab.com/" style="display:flex;align-items:baseline;">
      <span style="font-family:'Playfair Display',serif;font-style:italic;font-size:22px;font-weight:400;color:rgba(255,255,255,0.8);letter-spacing:-0.02em;">scaling</span><span style="font-family:'Playfair Display',serif;font-style:italic;font-size:22px;font-weight:900;background:linear-gradient(135deg,#E0DEFF,#7B6FFF);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;filter:drop-shadow(0 0 10px rgba(96,85,255,0.4));">lab'</span>
    </a>
    <div class="hide-mobile" style="display:flex;align-items:center;gap:32px;">
      <a href="https://lescalinglab.com/agences/{niche_slug}/" style="font-size:13px;font-weight:500;color:rgba(255,255,255,0.45);" onmouseover="this.style.color='rgba(255,255,255,0.9)'" onmouseout="this.style.color='rgba(255,255,255,0.45)'">{n['title_short']}</a>
      <a href="https://lescalinglab.com/agences/" style="font-size:13px;font-weight:500;color:rgba(255,255,255,0.45);" onmouseover="this.style.color='rgba(255,255,255,0.9)'" onmouseout="this.style.color='rgba(255,255,255,0.45)'">Toutes les niches</a>
    </div>
    <a href="https://lescalinglab.com/#apply" class="btn-primary" style="padding:10px 22px;font-size:13px;">Candidater →</a>
  </div>
</nav>

<section class="hero-bg" style="padding:104px 32px 64px;position:relative;overflow:hidden;">
  <div style="max-width:860px;margin:0 auto;position:relative;z-index:3;">
    <div class="breadcrumb" style="margin-bottom:28px;">
      <a href="https://lescalinglab.com/">Accueil</a><span>›</span>
      <a href="https://lescalinglab.com/agences/">Niches</a><span>›</span>
      <a href="https://lescalinglab.com/agences/{niche_slug}/">{n['parent_page_name']}</a><span>›</span>
      <span style="color:rgba(200,196,255,0.6);">{c['name']}</span>
    </div>
    <div class="pill" style="margin-bottom:28px;width:fit-content;">
      <span class="pill-dot"></span>
      {n['pill_text']} · {c['name']}
    </div>
    <h1 style="margin-bottom:24px;">
      <span class="display-bold" style="font-size:clamp(26px,3.5vw,48px);display:block;line-height:1.05;color:#fff;">{n['title_short']} à {c['name']} :</span>
      <span class="display-bold" style="font-size:clamp(20px,2.8vw,38px);display:block;line-height:1.1;background:linear-gradient(135deg,#C8C4FF 0%,#6055FF 50%,#3B2FE8 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-top:8px;">environ {lcount_fmt} établissements dans {city_ctx}</span>
    </h1>
    <p style="font-size:17px;line-height:1.75;color:rgba(255,255,255,0.55);max-width:640px;margin-bottom:40px;">
      {c['name']} et {city_ctx} concentrent environ {lcount_fmt} {n['label_raw'].lower()}. La majorité n'ont aucun système pour capter et convertir leurs leads automatiquement. C'est exactement l'opportunité qu'on enseigne au Scaling Lab'.
    </p>
    <div class="stats-grid" style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:600px;">
      <div class="stat-card">
        <div class="stat-num">~{lcount_fmt}</div>
        <div class="stat-label">Établissements à {c['name']}</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">{n['stat2_num']}</div>
        <div class="stat-label">{n['stat2_label']}</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">{n['stat3_num']}</div>
        <div class="stat-label">{n['stat3_label']}</div>
      </div>
    </div>
  </div>
</section>

<hr class="section-divider" />

<section style="padding:72px 32px;background:#06060F;">
  <div style="max-width:860px;margin:0 auto;">
    <div class="label" style="margin-bottom:16px;">Le marché à {c['name']}</div>
    <h2 class="heading-oswald" style="font-size:clamp(20px,2.8vw,32px);color:#fff;margin-bottom:16px;">Pourquoi c'est une niche à fort potentiel {city_prepo}</h2>
    <p style="font-size:15px;line-height:1.75;color:rgba(255,255,255,0.5);margin-bottom:40px;max-width:680px;">
      {n['market_body']} À {c['name']}, on estime environ {lcount_fmt} établissements — un bassin largement suffisant pour construire un portefeuille de 5 à 10 clients récurrents.
    </p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;">
      <div class="glow-card glow-card-hover" style="padding:24px;">
        <div style="font-size:12px;color:#6055FF;font-family:'Oswald',sans-serif;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:10px;">Bassin local</div>
        <div style="font-size:14px;line-height:1.7;color:rgba(255,255,255,0.6);">
          Environ {lcount_fmt} {n['label_raw'].lower()} sur {c['name']} et l'agglomération. Un marché adressable concret — pas besoin de prospecter à l'échelle nationale pour construire une agence à 10-20k€/mois.
        </div>
      </div>
      <div class="glow-card glow-card-hover" style="padding:24px;">
        <div style="font-size:12px;color:#6055FF;font-family:'Oswald',sans-serif;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:10px;">Ticket moyen</div>
        <div style="font-size:14px;line-height:1.7;color:rgba(255,255,255,0.6);">
          Setup : {n['ticket_setup']}. Retainer mensuel : {n['ticket_retainer']}/mois. Avec 5 clients actifs sur {c['name']}, un revenu de 5 à 10k€/mois en retainer seul est atteignable en moins de 6 mois.
        </div>
      </div>
      <div class="glow-card glow-card-hover" style="padding:24px;">
        <div style="font-size:12px;color:#6055FF;font-family:'Oswald',sans-serif;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:10px;">Niveau de concurrence IA</div>
        <div style="font-size:14px;line-height:1.7;color:rgba(255,255,255,0.6);">
          Quasi inexistant. Les agences web locales à {c['name']} vendent des sites et du SEO — pas des infrastructures d'automatisation commerciale. Première agence IA à cibler cette niche localement, premier à capter le marché.
        </div>
      </div>
    </div>
  </div>
</section>

<hr class="section-divider" />

<section style="padding:72px 32px;background:rgba(12,12,30,0.3);">
  <div style="max-width:860px;margin:0 auto;">
    <div class="label" style="margin-bottom:16px;">Le problème</div>
    <h2 class="heading-oswald" style="font-size:clamp(20px,2.8vw,32px);color:#fff;margin-bottom:12px;">Les 3 douleurs principales dans cette niche</h2>
    <p style="font-size:15px;line-height:1.75;color:rgba(255,255,255,0.5);margin-bottom:40px;max-width:660px;">
      Ces problèmes sont identiques à {c['name']} comme {francophonie_txt}. Ce qui change, c'est que localement la concurrence IA est quasi nulle.
    </p>
    <div style="display:flex;flex-direction:column;gap:20px;">
      <div class="pain-card">
        <div class="pain-num">01</div>
        <h3 style="font-family:'Oswald',sans-serif;font-size:18px;font-weight:700;text-transform:uppercase;color:#fff;margin:8px 0;">{n['pain1_title']}</h3>
        <p style="font-size:14px;line-height:1.75;color:rgba(255,255,255,0.55);margin-top:8px;">{n['pain1_body']}</p>
      </div>
      <div class="pain-card">
        <div class="pain-num">02</div>
        <h3 style="font-family:'Oswald',sans-serif;font-size:18px;font-weight:700;text-transform:uppercase;color:#fff;margin:8px 0;">{n['pain2_title']}</h3>
        <p style="font-size:14px;line-height:1.75;color:rgba(255,255,255,0.55);margin-top:8px;">{n['pain2_body']}</p>
      </div>
      <div class="pain-card">
        <div class="pain-num">03</div>
        <h3 style="font-family:'Oswald',sans-serif;font-size:18px;font-weight:700;text-transform:uppercase;color:#fff;margin:8px 0;">{n['pain3_title']}</h3>
        <p style="font-size:14px;line-height:1.75;color:rgba(255,255,255,0.55);margin-top:8px;">{n['pain3_body']}</p>
      </div>
    </div>
  </div>
</section>

<hr class="section-divider" />

<section style="padding:72px 32px;background:#06060F;">
  <div style="max-width:860px;margin:0 auto;">
    <div class="label" style="margin-bottom:16px;">L'infrastructure</div>
    <h2 class="heading-oswald" style="font-size:clamp(20px,2.8vw,32px);color:#fff;margin-bottom:12px;">Ce qu'on livre concrètement</h2>
    <p style="font-size:15px;line-height:1.75;color:rgba(255,255,255,0.5);margin-bottom:40px;max-width:660px;">
      Pas de l'IA pour faire de l'IA. Un système commercial qui automatise ce que le client faisait à la main — mal, ou pas du tout.
    </p>
    <div class="glow-card" style="padding:32px;">
      <div class="infra-item">
        <div class="infra-icon">⚡</div>
        <div>
          <div style="font-family:'Oswald',sans-serif;font-size:14px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;color:#fff;margin-bottom:6px;">{n['infra1_title']}</div>
          <div style="font-size:14px;line-height:1.7;color:rgba(255,255,255,0.5);">{n['infra1_body']}</div>
        </div>
      </div>
      <div class="infra-item">
        <div class="infra-icon">📬</div>
        <div>
          <div style="font-family:'Oswald',sans-serif;font-size:14px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;color:#fff;margin-bottom:6px;">{n['infra2_title']}</div>
          <div style="font-size:14px;line-height:1.7;color:rgba(255,255,255,0.5);">{n['infra2_body']}</div>
        </div>
      </div>
      <div class="infra-item">
        <div class="infra-icon">📊</div>
        <div>
          <div style="font-family:'Oswald',sans-serif;font-size:14px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;color:#fff;margin-bottom:6px;">{n['infra3_title']}</div>
          <div style="font-size:14px;line-height:1.7;color:rgba(255,255,255,0.5);">{n['infra3_body']}</div>
        </div>
      </div>
    </div>
    <div style="margin-top:32px;padding:24px;background:rgba(59,47,232,0.08);border:1px solid rgba(96,85,255,0.2);border-radius:14px;">
      <div class="label" style="margin-bottom:12px;">Positionnement tarifaire</div>
      <div style="display:flex;gap:24px;flex-wrap:wrap;">
        <div>
          <div style="font-family:'Oswald',sans-serif;font-size:22px;font-weight:700;color:#C8C4FF;">{n['ticket_setup']}</div>
          <div style="font-size:12px;color:rgba(255,255,255,0.4);margin-top:4px;">Setup unique</div>
        </div>
        <div style="border-left:1px solid rgba(96,85,255,0.2);padding-left:24px;">
          <div style="font-family:'Oswald',sans-serif;font-size:22px;font-weight:700;color:#C8C4FF;">{n['ticket_retainer']}</div>
          <div style="font-size:12px;color:rgba(255,255,255,0.4);margin-top:4px;">Retainer mensuel</div>
        </div>
      </div>
    </div>
  </div>
</section>

<hr class="section-divider" />

<section style="padding:72px 32px;background:rgba(12,12,30,0.3);">
  <div style="max-width:860px;margin:0 auto;">
    <div class="label" style="margin-bottom:16px;">Résultat élève</div>
    <h2 class="heading-oswald" style="font-size:clamp(20px,2.8vw,32px);color:#fff;margin-bottom:40px;">Ce que ça donne en pratique</h2>
    <div class="result-card">
      <div style="display:flex;align-items:flex-start;gap:24px;flex-wrap:wrap;">
        <div style="width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#5048FF,#3B2FE8);display:flex;align-items:center;justify-content:center;font-family:'Oswald',sans-serif;font-weight:700;font-size:16px;color:#fff;flex-shrink:0;">{n['student_initials']}</div>
        <div style="flex:1;min-width:200px;">
          <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:18px;color:#fff;margin-bottom:4px;">{n['student_name']}</div>
          <div style="font-size:12px;color:rgba(200,196,255,0.6);letter-spacing:0.08em;font-family:'Oswald',sans-serif;text-transform:uppercase;">{n['student_niche']}</div>
        </div>
      </div>
      {"" if not n['student_before'] else f'''
      <div style="margin-top:28px;display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:16px;">
        <div style="text-align:center;padding:20px;background:rgba(6,6,15,0.5);border-radius:12px;border:1px solid rgba(30,30,56,0.6);">
          <div style="font-family:'Oswald',sans-serif;font-size:13px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Avant</div>
          <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:24px;color:rgba(255,255,255,0.4);">{n["student_before"]}</div>
          <div style="font-size:11px;color:rgba(255,255,255,0.25);margin-top:4px;">par mois</div>
        </div>
        <div style="text-align:center;padding:20px;background:rgba(6,6,15,0.5);border-radius:12px;border:1px solid rgba(30,30,56,0.6);display:flex;align-items:center;justify-content:center;">
          <div style="font-size:22px;color:rgba(96,85,255,0.5);">→</div>
        </div>
        <div style="text-align:center;padding:20px;background:rgba(59,47,232,0.12);border-radius:12px;border:1px solid rgba(96,85,255,0.3);">
          <div style="font-family:'Oswald',sans-serif;font-size:13px;color:rgba(200,196,255,0.6);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Après</div>
          <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:24px;background:linear-gradient(135deg,#C8C4FF,#6055FF);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{n["student_after"]}</div>
          <div style="font-size:11px;color:rgba(200,196,255,0.4);margin-top:4px;">par mois</div>
        </div>
        <div style="text-align:center;padding:20px;background:rgba(6,6,15,0.5);border-radius:12px;border:1px solid rgba(30,30,56,0.6);">
          <div style="font-family:'Oswald',sans-serif;font-size:13px;color:rgba(255,255,255,0.35);text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Délai</div>
          <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:24px;color:#C8C4FF;">{n["student_delay"]}</div>
        </div>
      </div>
      '''}
      <p style="font-size:14px;line-height:1.75;color:rgba(255,255,255,0.45);margin-top:24px;">{n['student_desc']}</p>
    </div>
  </div>
</section>

<hr class="section-divider" />

<section style="padding:96px 32px;background:#06060F;">
  <div style="max-width:680px;margin:0 auto;text-align:center;">
    <div class="pill" style="margin-bottom:32px;width:fit-content;margin-left:auto;margin-right:auto;">
      <span class="pill-dot"></span>
      Formation Scaling Lab' · {c['name']}
    </div>
    <h2 class="display-bold" style="font-size:clamp(26px,3.5vw,44px);color:#fff;margin-bottom:20px;">
      Prêt à lancer ton agence IA à {c['name']} ?
    </h2>
    <p style="font-size:16px;line-height:1.75;color:rgba(255,255,255,0.45);margin-bottom:40px;max-width:480px;margin-left:auto;margin-right:auto;">
      Le Scaling Lab' t'accompagne de zéro à tes premiers clients dans cette niche — peu importe ta ville de départ. L'agence se gère en 100% remote.
    </p>
    <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;">
      <a href="https://lescalinglab.com/#apply" class="btn-primary" style="font-size:15px;padding:16px 36px;">Candidater au programme →</a>
      <a href="https://lescalinglab.com/agences/{niche_slug}/" class="btn-ghost">Voir la niche complète</a>
    </div>
  </div>
</section>

<footer style="background:#06060F;border-top:1px solid rgba(30,30,56,0.6);padding:40px 32px;">
  <div style="max-width:1100px;margin:0 auto;display:flex;flex-direction:column;align-items:center;gap:20px;text-align:center;">
    <a href="https://lescalinglab.com/" style="display:flex;align-items:baseline;">
      <span style="font-family:'Playfair Display',serif;font-style:italic;font-size:20px;font-weight:400;color:rgba(255,255,255,0.5);">scaling</span><span style="font-family:'Playfair Display',serif;font-style:italic;font-size:20px;font-weight:900;color:rgba(255,255,255,0.5);">lab'</span>
    </a>
    <div style="display:flex;gap:24px;flex-wrap:wrap;justify-content:center;">
      <a href="https://lescalinglab.com/agences/{niche_slug}/" style="font-size:13px;color:rgba(255,255,255,0.3);" onmouseover="this.style.color='rgba(255,255,255,0.6)'" onmouseout="this.style.color='rgba(255,255,255,0.3)'">{n['title_short']}</a>
      <a href="https://lescalinglab.com/agences/" style="font-size:13px;color:rgba(255,255,255,0.3);" onmouseover="this.style.color='rgba(255,255,255,0.6)'" onmouseout="this.style.color='rgba(255,255,255,0.3)'">Toutes les niches</a>
      <a href="https://lescalinglab.com/resultats" style="font-size:13px;color:rgba(255,255,255,0.3);" onmouseover="this.style.color='rgba(255,255,255,0.6)'" onmouseout="this.style.color='rgba(255,255,255,0.3)'">Résultats</a>
      <a href="https://lescalinglab.com/#apply" style="font-size:13px;color:rgba(255,255,255,0.3);" onmouseover="this.style.color='rgba(255,255,255,0.6)'" onmouseout="this.style.color='rgba(255,255,255,0.3)'">Candidater</a>
    </div>
    <p style="font-size:12px;color:rgba(255,255,255,0.15);">© 2025 Scaling Lab'. Tous droits réservés.</p>
  </div>
</footer>

</body>
</html>"""

# ─── GÉNÉRATION + SITEMAP ────────────────────────────────────────────────────

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    agences_dir = os.path.join(base_dir, 'agences')
    sitemap_path = os.path.join(base_dir, 'sitemap.xml')
    today = date.today().isoformat()
    generated_urls = []
    count = 0

    for niche_slug, niche in NICHES.items():
        for city in CITIES:
            out_dir = os.path.join(agences_dir, niche_slug, city['slug'])
            os.makedirs(out_dir, exist_ok=True)
            html = generate_page(niche_slug, niche, city)
            out_path = os.path.join(out_dir, 'index.html')
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html)
            url = f"https://lescalinglab.com/agences/{niche_slug}/{city['slug']}/"
            generated_urls.append(url)
            count += 1
            print(f"  ✓ {niche_slug}/{city['slug']}/")

    # ─── Mise à jour sitemap.xml ───
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns)

    existing_locs = {url.find(f'{{{ns}}}loc').text for url in root.findall(f'{{{ns}}}url')}
    for url in generated_urls:
        if url not in existing_locs:
            url_el = ET.SubElement(root, f'{{{ns}}}url')
            ET.SubElement(url_el, f'{{{ns}}}loc').text = url
            ET.SubElement(url_el, f'{{{ns}}}lastmod').text = today
            ET.SubElement(url_el, f'{{{ns}}}changefreq').text = 'monthly'
            ET.SubElement(url_el, f'{{{ns}}}priority').text = '0.6'

    ET.indent(tree, space='  ')
    tree.write(sitemap_path, encoding='UTF-8', xml_declaration=True)

    print(f"\n✅ {count} pages générées")
    print(f"✅ sitemap.xml mis à jour")

    # ─── Fichier JSON des URLs pour IndexNow ───
    indexnow_path = os.path.join(base_dir, 'indexnow_urls.json')
    with open(indexnow_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(generated_urls, f, ensure_ascii=False, indent=2)
    print(f"✅ indexnow_urls.json créé ({len(generated_urls)} URLs)")

if __name__ == '__main__':
    main()
