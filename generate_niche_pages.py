#!/usr/bin/env python3
"""
generate_niche_pages.py
Génère les 10 pages niche parent manquantes /agences/[niche]/index.html
FAQ accordéon + grille 50 villes + JSON-LD BreadcrumbList + FAQPage.
Usage : python3 generate_niche_pages.py
"""

import os, hashlib, json
import xml.etree.ElementTree as ET
from datetime import date
import importlib.util

# ─── Import NICHES + CITIES depuis generate_niche_city_pages.py ──────────────
_dir = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "gncm", os.path.join(_dir, "generate_niche_city_pages.py"))
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
NICHES = _mod.NICHES
CITIES = _mod.CITIES

NEW_NICHES = [
    'restaurants', 'solaire', 'dentistes', 'therapeutes', 'avocats',
    'salons-coiffure', 'e-commerce', 'garages-auto', 'kines-osteos',
    'plombiers-electriciens'
]

# ─── DONNÉES SUPPLÉMENTAIRES PAR NICHE ───────────────────────────────────────

NICHE_EXTRAS = {
    'restaurants': {
        'hero_lead': "Un restaurant plein le week-end mais vide en semaine. Des clients satisfaits qui ne reviennent pas. Des avis Google qui stagnent à 18 alors que le concurrent en a 150. Ce ne sont pas des problèmes de qualité — c'est un problème d'automatisation commerciale.",
        'market_cards': [
            ('Taille du marché', "175 000 restaurants en France dont 90% de TPE sans équipe marketing. Un marché ultra-fragmenté où le premier à apporter un système commercial se démarque immédiatement."),
            ("Chiffre d'affaires moyen", "200 000 à 600 000 €/an pour un restaurant de taille moyenne. Marges nettes de 8-15%. Le ROI d'un système de fidélisation est visible dès le premier mois."),
            ('Équipement numérique', "Un logiciel de caisse (Lightspeed, Zelty), parfois une solution de réservation (LaFourchette). Zéro CRM, zéro séquence de relance, zéro automatisation de fidélisation."),
            ('Profil client', "18-65 ans, local, visite 2 à 8 fois par an. Très réactif aux offres SMS (taux d'ouverture >90%). Décide sur Google Reviews avant de choisir."),
        ],
        'problem_lead': "La restauration a trois fuites de revenus systématiques. Elles sont universelles, immédiates, et mesurables. Un système IA les ferme toutes les trois.",
        'infra_lead': "Tout tourne dans GoHighLevel. Le propriétaire voit revenir ses anciens clients et ses créneaux se remplir — sans toucher à quoi que ce soit.",
        'infra4': ('📊', 'Dashboard propriétaire + reporting mensuel', "Le propriétaire reçoit un rapport mensuel automatique : nouveaux clients, taux de retour, avis collectés, no-shows évités. Le ROI est documenté — le retainer ne se discute plus."),
        'ticket_note': "Les restaurants avec plus de 200 couverts/jour acceptent plus facilement des tickets à 4 000-5 000 €. Pour les plus petits établissements, un setup à 2 000-2 500 € avec retainer 400 €/mois reste très ROI positif.",
        'faqs': [
            ("Combien peut-on facturer un restaurant pour une infrastructure IA ?", "Un setup complet (fidélisation SMS/email, automatisation avis Google, rappel réservations) se facture entre 2 000 et 5 000 €. Le retainer mensuel tourne entre 400 et 900 €/mois. Les restaurants avec fort volume (>200 couverts/jour) acceptent plus facilement des tickets à 4 000-5 000 €."),
            ("Comment approcher un restaurateur pour lui vendre de l'IA ?", "L'angle qui fonctionne : parler de clients perdus et d'avis Google, pas d'IA. Concrètement : \"Vos clients satisfaits ne reviennent pas faute de relance, et vous avez 18 avis alors que le restaurant d'en face en a 120.\" C'est une réalité qu'ils vivent chaque semaine. Le cold outreach Instagram ou visite directe fonctionne bien."),
            ("Est-ce que les restaurants ont le budget pour une agence IA ?", "Un restaurant qui fait 300 000 €/an génère ~30 000 à 45 000 € de résultat net. Un setup à 2 500 € + 500 €/mois représente moins de 3% de ce résultat. Si le système ramène 20 couverts supplémentaires par semaine à 25 €/couvert, le ROI est évident dès le mois 1."),
            ("Quel type d'infrastructure IA livre-t-on concrètement à un restaurant ?", "L'infrastructure standard : séquence SMS post-visite à J+14 et J+45, demande d'avis Google automatique après chaque repas, rappel de réservation J-2 pour réduire les no-shows, et pipeline de gestion des clients VIP. Tout configuré dans GoHighLevel sans coder."),
            ("Combien de temps avant de voir des résultats dans la restauration ?", "Les avis Google s'accumulent dès la première semaine. Le taux de no-show baisse dès la deuxième semaine. Le taux de retour de la clientèle est mesurable à 30 jours. C'est une des niches avec le ROI le plus visible et le plus rapide."),
        ],
    },
    'solaire': {
        'hero_lead': "Les leads achetés à 70 € partagés avec 4 concurrents. Un devis envoyé sans relance. Des appels entrants non qualifiés. Voici pourquoi les installateurs solaires sont prêts à payer pour un système d'acquisition propre — et ce que ça représente pour une agence IA.",
        'market_cards': [
            ('Taille du marché', "4 500 installateurs photovoltaïques actifs en France, pour un marché de 3,5 milliards d'euros qui a triplé entre 2020 et 2024. La demande résidentielle est portée par les aides MaPrimeRénov'."),
            ('Modèle économique', "Un installateur résidentiel génère 1 500 à 5 000 € de marge par installation. Une agence IA qui réduit le coût d'acquisition de 70 € (plateforme) à 20 € (système propre) génère un ROI immédiat sur chaque chantier."),
            ('Équipement numérique', "La quasi-totalité achetent leurs leads sur des plateformes (Hellio, Énergie Prime). Zéro système propre d'acquisition, zéro relance de devis automatique, zéro qualification en amont."),
            ('Profil client', "Propriétaires de maison individuelle, 35-65 ans, souvent ruraux ou périurbains. Décident sur recommandation et Google. Délai de décision de 2 à 4 semaines entre le premier contact et la signature."),
        ],
        'problem_lead': "Le solaire a un problème d'acquisition structurel. Les installateurs le savent — et n'ont pas la solution. Trois douleurs universelles dans cette niche.",
        'infra_lead': "L'objectif : générer des leads qualifiés en propre, réduire le coût d'acquisition, et convertir plus de devis. Tout dans GoHighLevel, sans coder.",
        'infra4': ('📊', 'Tracking performance — coût lead propre vs plateforme', "Dashboard mensuel comparant le coût par RDV généré en propre vs le coût des leads achetés. L'installateur voit concrètement l'économie réalisée chaque mois. Justifie le retainer sans discussion."),
        'ticket_note': "Les installateurs avec plus de 20 chantiers/mois ont les moyens d'un ticket à 5 000-6 000 €. Pour les plus petits, un setup à 2 500-3 000 € reste rentable dès le 2ème chantier supplémentaire généré.",
        'faqs': [
            ("Combien peut-on facturer un installateur solaire pour une infrastructure IA ?", "Un setup complet (chatbot qualification, funnel Meta Ads, séquence relance devis) se facture entre 2 500 et 6 000 €. Le retainer mensuel tourne entre 500 et 1 200 €/mois. Les installateurs qui font 20+ chantiers/mois acceptent facilement des tickets à 5 000-6 000 €."),
            ("Comment approcher un installateur solaire pour lui vendre de l'IA ?", "L'angle direct : \"Vous achetez des leads à 70 € partagés avec 4 concurrents. Je vous construis un système qui génère vos propres leads à 15-20 €, non partagés, pré-qualifiés.\" C'est une conversation sur les marges — pas sur la technologie. Fonctionne immédiatement."),
            ("Comment se différencier des plateformes de leads dans le solaire ?", "L'argument clé : les leads de plateforme sont partagés (3 à 5 installateurs reçoivent le même contact), non qualifiés (surface, orientation, budget non filtrés), et coûtent 60-90 €. Votre système génère des leads exclusifs, pré-qualifiés, à 15-25 €. L'avantage est immédiatement quantifiable."),
            ("Faut-il connaître le secteur solaire pour cibler cette niche ?", "Non. Ce qui compte, c'est de comprendre les douleurs (leads partagés coûteux, devis non relancés, appels non qualifiés) et quelques termes clés (MaPrimeRénov', puissance crête, installation résidentielle vs commercial). Ça s'apprend en quelques jours."),
            ("Quel type d'infrastructure livre-t-on concrètement à un installateur solaire ?", "Le setup standard : chatbot de qualification zone/toiture/budget, funnel Meta Ads propriétaires dans la zone d'intervention, séquence relance devis J+3/J+7/J+14, et dashboard de comparaison coût lead propre vs plateforme. Configuré dans GoHighLevel sans coder."),
        ],
    },
    'dentistes': {
        'hero_lead': "Un cabinet dentaire perd entre 1 000 et 2 500 €/semaine en no-shows non rappelés et en rappels de soins jamais effectués. Ce n'est pas un problème de qualité de soins — c'est un problème d'automatisation. Et c'est une opportunité directe pour une agence IA.",
        'market_cards': [
            ('Taille du marché', "42 000 chirurgiens-dentistes en France pour un marché de 12 milliards d'euros. La douleur est universelle : no-shows et rappels de soins jamais faits."),
            ("Chiffre d'affaires moyen", "400 000 à 800 000 €/an pour un cabinet de 2 à 3 praticiens. Un no-show évité = 200-300 € récupérés. À 5 no-shows/semaine évités, c'est 50 000-75 000 € récupérés par an."),
            ('Équipement numérique', "Un logiciel de gestion (Doctolib, Desmos ou Logos). Zéro relance automatique, zéro rappel de soins, zéro système d'acquisition de nouveaux patients."),
            ('Profil client', "Praticiens libéraux souvent débordés, avec peu de temps pour le commercial. Comprennent immédiatement les chiffres du no-show. Sensibles à l'argument de la réputation Google pour attirer de nouveaux patients."),
        ],
        'problem_lead': "Trois problèmes mesurables, universels, avec un ROI direct. C'est ce qui rend la niche dentaire si accessible pour une agence IA.",
        'infra_lead': "L'infrastructure s'intègre à côté de Doctolib, sans le remplacer. Le cabinet ne change pas ses habitudes — il voit son agenda se remplir et ses patients revenir plus souvent.",
        'infra4': ('📊', 'Dashboard mensuel — no-shows évités & rappels effectués', "Rapport mensuel automatique : nombre de no-shows évités vs mois précédent, rappels de soins effectués, nouveaux avis Google collectés. Le ROI est documenté — le retainer se justifie seul."),
        'ticket_note': "Les cabinets de groupe (2+ praticiens) avec 800 000 €+ de CA acceptent facilement des tickets à 5 000-7 000 €. Les cabinets solos commencent souvent à 3 000-4 000 € setup.",
        'faqs': [
            ("Combien peut-on facturer un cabinet dentaire pour une infrastructure IA ?", "Un setup complet (rappels RDV, relances soins, avis Google) se facture entre 3 000 et 7 000 €. Le retainer mensuel tourne entre 600 et 1 400 €/mois. Les cabinets de groupe (2+ praticiens, >600 000 €/an) acceptent plus facilement les tickets élevés."),
            ("Comment approcher un dentiste pour lui vendre de l'IA ?", "L'angle des chiffres fonctionne immédiatement : \"Vous perdez entre 1 000 et 2 000 € par semaine en no-shows et en rappels de soins jamais effectués. Mon système réduit les no-shows de 60% et déclenche les rappels automatiquement.\" C'est concret, chiffré, et sans jargon IA."),
            ("Faut-il connaître la dentisterie pour cibler cette niche ?", "Non. Il suffit de comprendre quelques termes (détartrage, implant, acte prophylactique) et de savoir que les rappels à 6/12 mois sont systématiquement oubliés. Tout le reste se comprend en 2-3 conversations avec des praticiens."),
            ("Quel type d'infrastructure livre-t-on concrètement à un cabinet dentaire ?", "Le setup standard : rappel RDV automatique J-2 et J-1 par SMS, séquence relance soins à 6 et 12 mois post-acte, demande d'avis Google automatique après chaque consultation. Le tout configuré dans GoHighLevel, sans modifier Doctolib."),
            ("Comment intégrer une infrastructure IA sans perturber les habitudes du cabinet ?", "GoHighLevel s'installe en parallèle de Doctolib — pas à la place. Les patients continuent à prendre RDV comme avant. Le système intervient uniquement pour les rappels, relances et avis. Zéro changement pour le praticien, 100% de résultats en plus."),
        ],
    },
    'therapeutes': {
        'hero_lead': "Sally est passée de salariée sans expérience en agence à 18 000 €/mois en ciblant les thérapeutes. La raison : 30 000 praticiens qui dépendent du bouche-à-oreille pour remplir leur agenda, et aucun n'a de système commercial pour le remplacer.",
        'market_cards': [
            ('Taille du marché', "Plus de 30 000 praticiens bien-être actifs en France : psychologues, coachs, sophrologues, hypnothérapeutes, thérapeutes PNL. Marché de 1,2 milliard d'euros, en croissance de 12% par an."),
            ("Chiffre d'affaires moyen", "50 000 à 120 000 €/an pour un praticien solo à temps plein. Les coachs certifiés haut de gamme dépassent souvent 150 000 €. Marges nettes de 60-75% — le budget pour un système d'automatisation est là."),
            ('Équipement numérique', "Un outil de prise de RDV (Calendly), parfois un site vitrine. Aucun CRM, aucune séquence email structurée, aucune relance automatique des leads qui se renseignent."),
            ('Profil client', "75% de femmes, 28-55 ans. Actives sur Instagram, présentes sur LinkedIn pour les coachs B2B. L'approche doit être authentique, pas commerciale."),
        ],
        'problem_lead': "La thérapie et le coaching ont trois freins commerciaux structurels. Ils sont universels dans la niche — et chacun a une solution directe.",
        'infra_lead': "L'infrastructure doit être discrète et alignée avec le positionnement du praticien. Pas de chatbot agressif — un système qui filtre, relance et référence, de façon fluide.",
        'infra4': ('📊', 'Pipeline CRM + reporting remplissage agenda', "Vue en temps réel : leads en attente, RDV confirmés, taux de conversion sur les demandes entrantes. Rapport mensuel sur l'évolution du taux de remplissage. Le praticien voit enfin d'où viennent ses clients."),
        'ticket_note': "Les coachs B2B haut de gamme (>100 000 €/an) acceptent facilement des tickets à 4 000-5 000 €. Les thérapeutes bien-être commencent plus souvent à 2 000-3 000 € setup.",
        'faqs': [
            ("Combien peut-on facturer un thérapeute ou un coach pour une infrastructure IA ?", "Un setup complet (chatbot de qualification, séquence nurturing, pipeline GHL) se facture entre 2 000 et 5 000 €. Le retainer mensuel tourne entre 500 et 1 200 €/mois. Les coachs B2B avec des tickets clients >5 000 € acceptent facilement des setups à 4 000-5 000 €."),
            ("Comment approcher un thérapeute ou un coach pour lui vendre de l'IA ?", "Ne pas mentionner l'IA. L'angle qui fonctionne : \"Combien de personnes se renseignent sur vos services chaque mois mais ne prennent jamais RDV ?\" Puis proposer un système de nurturing qui relance automatiquement ces prospects. Le vocabulaire : système commercial, flux de clients, automatisation — pas IA."),
            ("La niche thérapie est-elle éthique à démarcher commercialement ?", "Oui, si l'approche est alignée avec les valeurs du praticien. L'objectif n'est pas de pousser des ventes agressives — c'est d'automatiser la qualification et le suivi pour que le praticien se concentre sur les clients vraiment alignés. La transparence et le respect du rythme du prospect sont au cœur du système."),
            ("Quel type d'infrastructure livre-t-on à un thérapeute ou un coach ?", "Le setup standard : chatbot de qualification sur site et DMs Instagram (filtre problématique, budget, disponibilité), séquence email/SMS nurturing sur 14-21 jours pour les leads non convertis, pipeline GHL pour suivre toutes les demandes, avis automatiques après chaque accompagnement."),
            ("Faut-il comprendre la psychologie ou le coaching pour cibler cette niche ?", "Non. Il suffit de comprendre le cycle commercial du praticien : les prospects arrivent via le contenu et le bouche-à-oreille, hésitent longtemps avant de s'engager, et ne sont jamais relancés. Savoir parler de \"remplissage d'agenda\" et de \"clients qualifiés\" suffit."),
        ],
    },
    'avocats': {
        'hero_lead': "Un cabinet d'avocats perd 40 à 60% de ses leads entrants par manque de réponse rapide et de suivi. Le premier cabinet qui automatise sa qualification dans sa ville capte une longueur d'avance structurelle sur tous ses concurrents.",
        'market_cards': [
            ('Taille du marché', "20 000 cabinets d'avocats en France pour un marché de 8 milliards d'euros. Les cabinets généralistes TPE et les spécialistes droit de la famille/travail/commercial sont les meilleures cibles."),
            ("Chiffre d'affaires moyen", "150 000 à 500 000 €/an pour un cabinet solo à 3 associés. Taux horaire moyen : 180-350 €/h. Un système qui économise 5h de qualification par semaine = 4 000-7 000 €/mois de valeur directe."),
            ('Équipement numérique', "Logiciel de gestion de dossiers (Clio, Jarvis Legal), boîte email. Aucune qualification automatisée, aucun suivi des prospects froids, aucune réponse automatique aux demandes entrantes."),
            ('Profil client', "Avocats libéraux de 35-55 ans, souvent sceptiques face au \"marketing\". L'angle : parler de ROI chiffré (temps récupéré, dossiers supplémentaires signés) plutôt que de \"croissance digitale\"."),
        ],
        'problem_lead': "Le cabinet d'avocats est une entreprise de service comme les autres — avec les mêmes problèmes commerciaux que les autres. Trois douleurs immédiates et mesurables.",
        'infra_lead': "L'infrastructure est pensée pour un cabinet où les avocats ont un taux horaire élevé et ne peuvent pas se permettre de passer du temps à qualifier des prospects hors cible.",
        'infra4': ('📊', 'Dashboard dossiers + prospects + avis Google', "Vue en temps réel sur les demandes entrantes, prospects qualifiés et dossiers actifs. Rapport mensuel sur les avis collectés et la position Google Business. Le cabinet documente sa croissance."),
        'ticket_note': "Les cabinets avec 3+ associés et >300 000 €/an de CA acceptent facilement des tickets à 5 000-8 000 €. Les avocats solos commencent souvent à 2 500-3 500 € setup.",
        'faqs': [
            ("Combien peut-on facturer un cabinet d'avocats pour une infrastructure IA ?", "Un setup complet (qualification automatique, suivi prospects froids, avis Google) se facture entre 2 500 et 8 000 €. Le retainer mensuel tourne entre 600 et 1 500 €/mois. Les cabinets de 3+ associés avec >300 000 €/an de CA acceptent les tickets élevés."),
            ("Comment approcher un avocat pour lui vendre de l'IA ?", "L'angle du temps facturable : \"Combien d'heures par semaine passez-vous à qualifier des prospects hors cible ou à répondre à des demandes sans suite ?\" Puis montrer qu'un système de qualification automatique libère 5-8h/semaine de temps facturable. C'est 4 000 à 6 000 €/mois de valeur directe."),
            ("Les avocats sont-ils ouverts aux solutions digitales ?", "Les avocats de 40-55 ans peuvent être sceptiques. L'approche : ne jamais dire \"IA\" ou \"automatisation\" — parler de \"système de qualification\", \"pipeline de prospects\", \"réponse en moins de 5 minutes\". Les résultats chiffrés (temps gagné, dossiers supplémentaires) font la vente."),
            ("Quel type d'infrastructure livre-t-on concrètement à un cabinet d'avocats ?", "Le setup standard : chatbot de filtrage par domaine/urgence/budget sur le site, séquence de relance prospects froids J+3/J+7/J+21 avec ressources légales utiles, pipeline CRM GoHighLevel, automatisation avis Google après chaque dossier clos."),
            ("Faut-il connaître le droit pour cibler la niche avocats ?", "Non. Il suffit de comprendre les domaines principaux (droit de la famille, droit du travail, droit commercial) et le vocabulaire de base (dossier, consultation, honoraires, cabinet solo vs cabinet d'associés). L'angle commercial (qualification, délai de réponse, suivi) est identique à toutes les professions libérales."),
        ],
    },
    'salons-coiffure': {
        'hero_lead': "85 000 salons de coiffure et barbershops en France. L'agenda plein le samedi, vide en semaine. Des clients qui ne reviennent pas assez souvent. Une douleur simple, mesurable, universelle — et un ticket d'entrée accessible pour une première agence IA locale.",
        'market_cards': [
            ('Taille du marché', "85 000 salons de coiffure et barbershops en France, pour un marché de 5 milliards d'euros. C'est le secteur avec la plus forte densité de commerce local après la restauration."),
            ("Chiffre d'affaires moyen", "80 000 à 250 000 €/an pour un salon de 2 à 4 coiffeurs. Un système qui augmente la fréquence de visite de 10% = +8 000 à 25 000 €/an directement."),
            ('Équipement numérique', "Logiciel de réservation (Planity, Booksy), parfois Instagram actif. Aucune relance de clients inactifs, aucun programme de fidélisation automatisé, aucune gestion proactive de l'agenda semaine."),
            ('Profil client', "Propriétaires de 30-50 ans, souvent formés métier mais pas commerciaux. Comprennent immédiatement les chiffres de fréquence de visite. Sensibles à l'argument \"client qui revient moins souvent = argent perdu\"."),
        ],
        'problem_lead': "La coiffure a trois problèmes commerciaux simples. Pas techniques — juste pas automatisés. Chacun a une solution directe.",
        'infra_lead': "L'infrastructure tourne en parallèle de Planity ou Booksy. Le propriétaire ne change rien — il voit juste son agenda se remplir en semaine et ses clients revenir plus souvent.",
        'infra4': ('📊', "Dashboard fidélisation — fréquence de visite & remplissage agenda", "Vue mensuelle sur la fréquence de visite par prestation, le taux de remplissage semaine vs week-end, et les avis Google collectés. Le propriétaire voit enfin l'impact de son investissement."),
        'ticket_note': "Les salons avec 3+ coiffeurs et >200 000 €/an de CA acceptent les tickets à 3 000-4 000 €. Les barbershops et petits salons commencent souvent à 1 500-2 000 € setup. Un ticket plus accessible = porte d'entrée pour une première agence locale.",
        'faqs': [
            ("Combien peut-on facturer un salon de coiffure pour une infrastructure IA ?", "Un setup complet (relances SMS clients inactifs, remplissage agenda semaine, avis Google) se facture entre 1 500 et 4 000 €. Le retainer mensuel tourne entre 400 et 800 €/mois. Le ticket plus bas que d'autres niches en fait un excellent point d'entrée pour une première agence."),
            ("Comment approcher un salon de coiffure ou un barbershop ?", "L'angle direct : \"Vos clients reviennent en moyenne toutes les 10 semaines. Avec un système de relance au bon moment, vous les faites revenir toutes les 6-7 semaines. Pour un salon de 100 clients actifs, ça fait 15 000-20 000 € de CA supplémentaire par an.\" C'est un calcul qu'ils font en 30 secondes."),
            ("Faut-il connaître la coiffure pour cibler cette niche ?", "Non. Il suffit de comprendre les types de prestations (coupe, couleur/balayage, barbe) et leurs fréquences naturelles. Ça s'apprend en une journée. L'angle commercial (fréquence de visite, agenda semaine vide, clients perdus) est identique à toutes les niches locales."),
            ("Quel type d'infrastructure livre-t-on concrètement à un salon de coiffure ?", "Le setup standard : séquence SMS relance personnalisée par type de prestation (J+35 pour coupe, J+42 pour couleur), offre ciblée pour remplir les créneaux semaine le lundi matin, demande d'avis automatique après chaque prestation. Tout dans GoHighLevel, sans modifier Planity ou Booksy."),
            ("Comment justifier le retainer mensuel face à un propriétaire de salon ?", "Le ROI est simple à calculer : si le système génère 3 visites supplémentaires par semaine à 40 € de panier moyen, c'est 480 € de CA additionnel par semaine — soit 2 000 €/mois. Face à un retainer de 400-600 €/mois, la conversation est facile."),
        ],
    },
    'e-commerce': {
        'hero_lead': "78% des visiteurs qui ajoutent un produit au panier n'achètent jamais. 60% des clients ne commandent qu'une seule fois. Ce n'est pas un problème de produit — c'est un problème d'automatisation. Et c'est mesurable dès le premier mois.",
        'market_cards': [
            ('Taille du marché', "200 000 boutiques e-commerce actives en France, dont 85% sont des TPE avec moins de 5 employés. Marché de 160 milliards d'euros, avec une croissance annuelle de 8-10%."),
            ("Chiffre d'affaires moyen", "50 000 à 500 000 €/an pour une boutique TPE. Marges nettes de 20-40%. Un taux de récupération de panier de 10% sur une boutique qui génère 500 paniers abandonnés/mois = 50 ventes supplémentaires."),
            ('Équipement numérique', "Shopify ou WooCommerce pour la boutique. Klaviyo ou Mailchimp parfois installés — mais pas configurés. Aucune séquence de relance panier automatique, aucun win-back client, aucun post-achat structuré."),
            ('Profil client', "Entrepreneurs solo ou équipes de 2-3 personnes. Comprennent les métriques (taux de conversion, panier moyen, CLV). Sensibles à l'argument du ROI direct et mesurable."),
        ],
        'problem_lead': "L'e-commerce a trois fuites de revenus mesurables, récurrentes, et corrigeables avec des séquences automatisées. Trois opportunités directes pour une agence IA.",
        'infra_lead': "Tout s'intègre à Shopify/WooCommerce via GoHighLevel. Le propriétaire voit ses métriques s'améliorer semaine après semaine — sans toucher au site.",
        'infra4': ('📊', 'Dashboard e-commerce — paniers récupérés & CLV', "Tableau de bord mensuel : paniers abandonnés récupérés, taux de réachat clients, avis collectés, CLV moyen avant/après. Le ROI est documenté en temps réel — le retainer se justifie avec les chiffres."),
        'ticket_note': "Les boutiques avec >100 000 €/an de CA et >500 commandes/mois acceptent facilement des tickets à 4 000-6 000 €. Les petites boutiques commencent à 2 000-3 000 € setup. L'e-commerce est une niche où le retainer peut être indexé sur les performances.",
        'faqs': [
            ("Combien peut-on facturer un e-commerce pour une infrastructure IA ?", "Un setup complet (relance panier, win-back clients, post-achat) se facture entre 2 000 et 6 000 €. Le retainer mensuel tourne entre 500 et 1 500 €/mois. Les boutiques avec >100 000 €/an de CA acceptent les tickets élevés, surtout si le retainer est partiellement indexé sur les performances."),
            ("Comment approcher un propriétaire de boutique e-commerce ?", "L'angle chiffré : \"Combien de paniers abandonnés avez-vous par mois ? À [panier moyen] € et un taux de récupération de 10%, un système de relance vous rapporte [X] € par mois.\" La conversation démarre sur les métriques — pas sur la technologie."),
            ("Un retainer basé sur la performance est-il possible en e-commerce ?", "Oui — c'est même la structure idéale pour convertir facilement. Setup fixe + retainer incluant un % sur les ventes récupérées au-delà d'un seuil. Le client prend moins de risque, vous capturez plus de valeur si le système performe. Modèle à proposer aux boutiques avec >200 commandes/mois."),
            ("Quel type d'infrastructure livre-t-on concrètement à un e-commerce ?", "Le setup standard : séquence relance panier abandonné en 1h/24h/72h (email + SMS), séquence win-back clients inactifs à 45/90/180 jours, séquence post-achat avec cross-sell à J+7 et demande d'avis à J+3. Intégration Shopify/WooCommerce via GoHighLevel."),
            ("Faut-il connaître le e-commerce pour cibler cette niche ?", "Non, mais des bases en métriques e-commerce sont utiles : taux d'abandon panier, CLV, taux de réachat. Klaviyo, Mailchimp, et GoHighLevel sont les outils standards. L'angle est le même pour toutes les boutiques : récupérer les ventes perdues et augmenter la fréquence d'achat."),
        ],
    },
    'garages-auto': {
        'hero_lead': "Chaque véhicule a des échéances prévisibles et connues. Le contrôle technique, la révision annuelle, la vidange. Ces rendez-vous ne s'inventent pas — ils se rappellent automatiquement. Et 40 à 60% des garages perdent leurs clients parce qu'ils ne le font pas.",
        'market_cards': [
            ('Taille du marché', "35 000 garages automobiles et carrosseries indépendants en France. Le marché de l'entretien auto représente 18 milliards d'euros par an. Le client revient naturellement — s'il est rappelé au bon moment."),
            ("Chiffre d'affaires moyen", "200 000 à 600 000 €/an pour un garage de 2 à 4 mécaniciens. Panier moyen révision : 180-250 €. Un système qui rappelle 50 clients supplémentaires par an = 9 000-12 500 € de CA additionnel direct."),
            ('Équipement numérique', "Logiciel de gestion atelier (Autovisio, Winmotor). Aucun CRM, aucun rappel automatique de révision ou CT, aucune demande d'avis Google automatique."),
            ('Profil client', "Garagistes de 35-55 ans, souvent techniciens de formation. Comprennent immédiatement les chiffres (client perdu = X révisions perdues par an). Sceptiques face au digital mais convaincus par un ROI simple et direct."),
        ],
        'problem_lead': "Le garage a une caractéristique unique : chaque acte génère un prochain RDV prévisible. Trois fuites à automatiser pour capturer tout ce potentiel.",
        'infra_lead': "L'infrastructure tourne en parallèle du logiciel d'atelier. Le garagiste ne change rien — les rappels partent tout seuls, les avis s'accumulent, les appels manqués ne sont plus perdus.",
        'infra4': ('📊', 'Dashboard fidélisation — taux de retour & avis Google', "Rapport mensuel : clients revenus en révision vs mois précédent, avis Google collectés, appels manqués capturés. Le garage voit son taux de rétention augmenter mois après mois."),
        'ticket_note': "Les garages avec >3 mécaniciens et >400 000 €/an de CA acceptent les tickets à 3 500-5 000 €. Les garages solos commencent souvent à 2 000-2 500 € setup.",
        'faqs': [
            ("Combien peut-on facturer un garage automobile pour une infrastructure IA ?", "Un setup complet (rappels révision/CT, capture appels manqués, avis Google) se facture entre 2 000 et 5 000 €. Le retainer mensuel tourne entre 400 et 1 000 €/mois. Le ROI direct (revenus récurrents récupérés) rend la vente simple."),
            ("Comment approcher un garagiste pour lui vendre de l'IA ?", "L'angle du client perdu : \"Combien de clients avez-vous qui sont venus faire une vidange l'année dernière mais ne sont pas revenus pour la révision ? Pour un garage de 500 clients actifs, c'est typiquement 200-300 clients perdus par an.\" Puis montrer le système de rappel automatique."),
            ("Faut-il connaître l'automobile pour cibler cette niche ?", "Non. Il suffit de connaître les échéances standard (révision annuelle, CT tous les 2 ans, vidange 1-2 fois par an) et d'utiliser le bon vocabulaire (atelier, mécanicien, diagnostic, véhicule en attente). Ça s'apprend en 2-3 conversations."),
            ("Quel type d'infrastructure livre-t-on concrètement à un garage ?", "Le setup standard : rappel SMS automatique à J+330 (révision annuelle) ou selon l'échéance CT, SMS automatique 5 minutes après tout appel manqué, demande d'avis Google 1h après la remise des clés, pipeline GHL pour suivre les clients actifs et inactifs."),
            ("Comment convaincre un garagiste sceptique face au digital ?", "Ne pas parler de digital ou d'IA. Parler uniquement de ce qu'il voit concrètement : \"Chaque client qui revient pour sa révision vaut 180-250 €. Mon système vous fait revenir 30-50 clients de plus par an — soit 5 000-12 500 € de CA supplémentaire. Le setup est à 2 500 €. Vous êtes rentable au deuxième client.\""),
        ],
    },
    'kines-osteos': {
        'hero_lead': "Les kinés et ostéos ont une liste d'attente mais perdent 30 à 50% de leurs patients potentiels récurrents faute de suivi post-protocole. Ce n'est pas un manque de patients — c'est un manque d'automatisation. Et une opportunité directe pour une agence IA.",
        'market_cards': [
            ('Taille du marché', "Plus de 120 000 masseurs-kinésithérapeutes en France, pour un marché de 4 milliards d'euros. Les ostéopathes représentent 30 000 praticiens supplémentaires. Majorité en libéral, souvent en liste d'attente."),
            ("Chiffre d'affaires moyen", "60 000 à 150 000 €/an pour un kiné libéral. Le coût d'un créneau vide (annulation non remplacée) : 50-70 €. À 3 annulations/semaine non remplacées, c'est 8 000-11 000 € perdus par an."),
            ('Équipement numérique', "Doctolib pour la prise de RDV, logiciel de bilan. Aucune liste d'attente automatisée, aucun suivi post-protocole, aucun programme de prévention actif."),
            ('Profil client', "Praticiens libéraux de 28-55 ans, souvent débordés. Sensibles à l'argument des créneaux vides et des patients qui rechutent chez un autre praticien."),
        ],
        'problem_lead': "La kinésithérapie et l'ostéopathie ont trois fuites de revenus structurelles. Chacune a une solution directe et automatisable.",
        'infra_lead': "L'infrastructure s'installe en parallèle de Doctolib. Le praticien ne change pas ses habitudes — les relances partent automatiquement et les créneaux vides se remplissent.",
        'infra4': ('📊', 'Dashboard patients — taux de retour & remplissage créneaux', "Rapport mensuel : patients revenus en préventif, créneaux d'annulation remplacés, avis collectés. Le praticien voit l'impact sur son agenda et son CA mois après mois."),
        'ticket_note': "Les cabinets de groupe (2+ praticiens) et les kinés avec liste d'attente longue acceptent les tickets à 3 000-5 000 €. Les ostéos solos commencent souvent à 2 000-2 500 € setup.",
        'faqs': [
            ("Combien peut-on facturer un kinésithérapeute ou un ostéopathe pour une infrastructure IA ?", "Un setup complet (suivi post-protocole, liste d'attente, avis Google) se facture entre 2 000 et 5 000 €. Le retainer mensuel tourne entre 400 et 1 000 €/mois. Le ROI direct (créneaux récupérés + patients récurrents) rend la vente simple."),
            ("Comment approcher un kiné ou un ostéo pour lui vendre de l'IA ?", "L'angle des créneaux vides : \"Combien d'annulations avez-vous par semaine qui restent vides ? À 60 € par séance et 3 annulations/semaine, c'est 9 000 € perdus par an.\" Puis montrer le système de liste d'attente automatique. La douleur est immédiate et chiffrée."),
            ("Faut-il connaître la kinésithérapie pour cibler cette niche ?", "Non. Il suffit de comprendre le fonctionnement d'un protocole (nombre de séances, fréquence, objectifs) et les termes de base (ordonnance médicale, bilan initial, protocole lombaire). L'angle commercial (créneaux vides, patients perdus post-protocole, prévention) est le même partout."),
            ("Quel type d'infrastructure livre-t-on à un kiné ou un ostéo ?", "Le setup standard : séquence suivi post-protocole J+15/J+30/J+90 avec exercices et bilan, notification automatique de la liste d'attente sur chaque annulation, demande d'avis Google en fin de protocole, pipeline GHL pour suivre les protocoles en cours."),
            ("Comment intégrer une infrastructure IA sans perturber le cabinet ?", "Le système fonctionne en parallèle de Doctolib — pas à la place. Doctolib gère les RDV, GoHighLevel gère les relances et communications automatiques. Zéro changement pour le praticien dans son quotidien."),
        ],
    },
    'plombiers-electriciens': {
        'hero_lead': "Arnaud était en SMMA depuis 7 ans avec 20 clients épuisants. Il a pivoté vers les artisans et l'habitat. Résultat : 8 000 €+/mois avec beaucoup moins de clients. La niche artisans est massive, accessible, et la concurrence IA est quasi nulle.",
        'market_cards': [
            ('Taille du marché', "200 000 plombiers, électriciens et artisans du second œuvre en France. La majorité sont des TPE de 1 à 3 personnes. Le marché de l'entretien et rénovation résidentielle représente 60 milliards d'euros."),
            ("Chiffre d'affaires moyen", "80 000 à 300 000 €/an pour un artisan solo à 2-3 compagnons. Panier moyen : 500-2 000 € par chantier. La perte d'un appel manqué représente souvent 300-1 000 € de devis potentiel."),
            ('Équipement numérique', "Parfois un logiciel de devis (Batigest, Obat). Aucun CRM, aucun système de rappel automatique, aucune demande d'avis Google structurée. La plupart gèrent leurs prospects sur carnet ou mémoire."),
            ('Profil client', "Artisans de 30-55 ans, souvent sur chantier toute la journée. Comprennent immédiatement l'argument de l'appel manqué. Sceptiques face au digital — convaincus uniquement par du concret et du ROI direct."),
        ],
        'problem_lead': "Le plombier et l'électricien ont trois problèmes commerciaux simples. Pas techniques. Juste pas automatisés. Chacun a une solution directe.",
        'infra_lead': "L'infrastructure est pensée pour un artisan qui est sur chantier toute la journée. Zéro intervention manuelle — tout part automatiquement.",
        'infra4': ('📊', 'Dashboard artisan — appels capturés & avis collectés', "Rapport mensuel : appels manqués capturés, devis relancés et signés, avis Google collectés. L'artisan voit son taux de conversion et sa note Google progresser chaque mois."),
        'ticket_note': "Les entreprises avec 2+ compagnons et >200 000 €/an de CA acceptent les tickets à 3 000-5 000 €. Les artisans solos commencent souvent à 2 000-2 500 € setup. Un ticket accessible = porte d'entrée facile dans cette niche à fort volume.",
        'faqs': [
            ("Combien peut-on facturer un plombier ou un électricien pour une infrastructure IA ?", "Un setup complet (réponse appel manqué, relance devis, avis Google) se facture entre 2 000 et 5 000 €. Le retainer mensuel tourne entre 400 et 1 000 €/mois. ROI direct : si le système récupère 1 devis/semaine à 800 € de panier moyen, le retainer est rentabilisé en 2 semaines."),
            ("Comment approcher un plombier ou un électricien pour lui vendre de l'IA ?", "L'angle de l'appel manqué : \"La semaine dernière, combien de fois votre téléphone a sonné quand vous étiez sur le pont ?\" Puis montrer le SMS automatique en 3 minutes. La démonstration dure 30 secondes et convainc immédiatement."),
            ("Les artisans sont-ils sceptiques face au digital ?", "Oui, la majorité. La clé : ne jamais parler d'IA, d'automatisation ou de digital. Parler uniquement de ce qu'ils voient : \"Plus d'appels manqués perdus, plus de devis signés, plus d'avis Google.\" Résultat concret, pas technologie."),
            ("Quel type d'infrastructure livre-t-on concrètement à un artisan ?", "Le setup standard : SMS automatique 3 minutes après tout appel manqué, séquence relance devis J+3/J+7 via SMS et email simple, demande d'avis Google le lendemain de la fin du chantier, pipeline GHL pour suivre les devis en cours."),
            ("Comment justifier le retainer mensuel face à un artisan sceptique ?", "Calcul direct : \"Mon système vous récupère en moyenne 2 devis supplémentaires par mois. À 700 € de panier moyen, ça fait 1 400 €/mois de CA additionnel. Mon retainer est à 500 €. La différence, c'est votre marge.\" Le calcul est fait en 10 secondes."),
        ],
    },
}


# ─── HELPERS ─────────────────────────────────────────────────────────────────

def pid(slug):
    return 'gp_' + hashlib.md5(slug.encode()).hexdigest()[:8]


def city_grid_html(slug):
    france = [c for c in CITIES if c['country'] == 'France']
    intl   = [c for c in CITIES if c['country'] != 'France']

    def city_link(c):
        url = f"https://lescalinglab.com/agences/{slug}/{c['slug']}/"
        return (f'<a href="{url}" '
                f'style="display:inline-flex;padding:7px 14px;background:rgba(12,12,30,0.6);'
                f'border:1px solid rgba(30,30,56,0.7);border-radius:100px;font-size:13px;'
                f'color:rgba(255,255,255,0.5);font-family:\'Inter\',sans-serif;'
                f'transition:color 0.2s ease,border-color 0.2s ease;" '
                f'onmouseover="this.style.color=\'#fff\';this.style.borderColor=\'rgba(96,85,255,0.4)\'" '
                f'onmouseout="this.style.color=\'rgba(255,255,255,0.5)\';this.style.borderColor=\'rgba(30,30,56,0.7)\'">'
                f'{c["name"]}</a>')

    france_links = '\n        '.join(city_link(c) for c in france)
    intl_links   = '\n        '.join(city_link(c) for c in intl)

    return f"""
<hr class="section-divider" />

<!-- ═══ COUVERTURE GÉOGRAPHIQUE ═══ -->
<section style="padding:72px 32px;background:rgba(12,12,30,0.2);">
  <div style="max-width:860px;margin:0 auto;">
    <div class="label" style="margin-bottom:16px;">Couverture géographique</div>
    <h2 class="heading-oswald" style="font-size:clamp(20px,2.5vw,30px);color:#fff;margin-bottom:16px;">Cette niche dans toutes les villes francophones</h2>
    <p style="font-size:15px;line-height:1.75;color:rgba(255,255,255,0.45);margin-bottom:40px;max-width:640px;">L'agence IA se gère en 100% remote — peu importe où se trouvent tes clients. Voici les pages dédiées à chaque ville francophone.</p>

    <div style="margin-bottom:12px;font-size:11px;font-family:'Oswald',sans-serif;font-weight:500;letter-spacing:0.18em;text-transform:uppercase;color:rgba(200,196,255,0.35);">France — 30 villes</div>
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:32px;">
        {france_links}
    </div>

    <div style="margin-bottom:12px;font-size:11px;font-family:'Oswald',sans-serif;font-weight:500;letter-spacing:0.18em;text-transform:uppercase;color:rgba(200,196,255,0.35);">Francophonie internationale — 20 villes</div>
    <div style="display:flex;flex-wrap:wrap;gap:8px;">
        {intl_links}
    </div>
  </div>
</section>"""


def faq_ld_str(faqs):
    items = []
    for q, a in faqs:
        items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}
        })
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items},
                      ensure_ascii=False, indent=2)


def faq_accordion(faqs):
    parts = []
    for i, (q, a) in enumerate(faqs):
        border = 'border-bottom:none;' if i == len(faqs) - 1 else ''
        # escape apostrophes in q for inline onclick attribute context — not needed since we use onclick="toggleFaq(this)"
        parts.append(f"""      <div class="faq-item" style="{border}">
        <button class="faq-q" onclick="toggleFaq(this)">
          {q}
          <svg class="faq-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="rgba(200,196,255,0.5)" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
        <div class="faq-a">{a}</div>
      </div>""")
    return '\n'.join(parts)


def market_cards_html(cards):
    parts = []
    for label, body in cards:
        parts.append(f"""      <div class="glow-card glow-card-hover" style="padding:24px;">
        <div style="font-size:12px;color:#6055FF;font-family:'Oswald',sans-serif;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:10px;">{label}</div>
        <div style="font-size:14px;line-height:1.7;color:rgba(255,255,255,0.6);">{body}</div>
      </div>""")
    return '\n'.join(parts)


# ─── GÉNÉRATEUR HTML ──────────────────────────────────────────────────────────

def generate_page(slug, n, extras):
    gp      = pid(slug)
    today   = date.today().isoformat()
    canonical = f"https://lescalinglab.com/agences/{slug}/"

    faq_ld  = faq_ld_str(extras['faqs'])
    faq_html = faq_accordion(extras['faqs'])
    cities  = city_grid_html(slug)
    mc      = market_cards_html(extras['market_cards'])

    i4_icon, i4_title, i4_body = extras['infra4']

    has_student = bool(n.get('student_before'))
    if has_student:
        student_grid = f"""      <div style="margin-top:28px;display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:16px;">
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
      </div>"""
    else:
        student_grid = ''

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{n['title_short']} &amp; Agence IA — {n['stat1_num']} {n['stat1_label'].lower()} | Scaling Lab'</title>
  <meta name="description" content="{n['stat1_num']} {n['label_raw'].lower()} en France. Comment lancer une agence IA dans cette niche : l'opportunité, ce qu'on vend, le ticket moyen. Cas élève inclus." />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{canonical}" />
  <meta property="og:title" content="Vendre l'IA aux {n['title_short']} — Scaling Lab'" />
  <meta property="og:description" content="{n['stat1_num']} {n['label_raw'].lower()}. {n['stat2_num']} {n['stat2_label'].lower()}. Voici l'opportunité pour une agence IA." />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:type" content="article" />

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type":"ListItem","position":1,"name":"Accueil","item":"https://lescalinglab.com/"}},
      {{"@type":"ListItem","position":2,"name":"Niches","item":"https://lescalinglab.com/agences/"}},
      {{"@type":"ListItem","position":3,"name":"{n['parent_page_name']}","item":"{canonical}"}}
    ]
  }}
  </script>

  <script type="application/ld+json">
  {faq_ld}
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

    .glow-card {{
      background: rgba(12,12,30,0.7); border: 1px solid rgba(30,30,56,0.8);
      box-shadow: 0 1px 0 rgba(100,90,255,0.12) inset, 0 0 0 1px rgba(30,30,56,1), 0 20px 60px rgba(0,0,0,0.4);
      border-radius: 16px;
    }}
    .glow-card-hover {{ transition: box-shadow 0.3s ease, transform 0.3s ease, border-color 0.3s ease; }}
    .glow-card-hover:hover {{ box-shadow: 0 1px 0 rgba(100,90,255,0.25) inset, 0 0 0 1px rgba(74,59,255,0.35), 0 24px 60px rgba(59,47,232,0.15), 0 4px 20px rgba(0,0,0,0.5); transform: translateY(-2px); }}

    .stat-card {{
      background: rgba(12,12,30,0.6); border: 1px solid rgba(30,30,56,0.7);
      border-radius: 12px; padding: 20px 24px; text-align: center;
    }}
    .stat-num {{ font-family: 'Oswald', sans-serif; font-weight: 700; font-size: 28px; background: linear-gradient(135deg,#C8C4FF,#6055FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }}
    .stat-label {{ font-size: 12px; color: rgba(255,255,255,0.45); margin-top: 4px; }}

    .pain-card {{ background: rgba(12,12,30,0.5); border: 1px solid rgba(59,47,232,0.15); border-radius: 14px; padding: 28px; }}
    .pain-num {{ font-family: 'Oswald', sans-serif; font-weight: 700; font-size: 36px; color: rgba(96,85,255,0.25); line-height: 1; }}

    .infra-item {{ display: flex; gap: 16px; align-items: flex-start; padding: 20px 0; border-bottom: 1px solid rgba(30,30,56,0.6); }}
    .infra-item:last-child {{ border-bottom: none; }}
    .infra-icon {{ width: 36px; height: 36px; border-radius: 8px; background: rgba(59,47,232,0.2); border: 1px solid rgba(96,85,255,0.25); display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 16px; }}

    .result-card {{ background: linear-gradient(135deg, rgba(59,47,232,0.12) 0%, rgba(12,12,30,0.8) 100%); border: 1px solid rgba(96,85,255,0.25); border-radius: 20px; padding: 36px; }}

    .faq-item {{ border-bottom: 1px solid rgba(30,30,56,0.6); }}
    .faq-q {{ width: 100%; text-align: left; background: none; border: none; padding: 24px 0; cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 16px; color: rgba(255,255,255,0.85); font-family: 'Inter', sans-serif; font-size: 15px; font-weight: 500; }}
    .faq-q:hover {{ color: #fff; }}
    .faq-a {{ display: none; padding: 0 0 24px; font-size: 14px; line-height: 1.75; color: rgba(255,255,255,0.55); }}
    .faq-item.open .faq-a {{ display: block; }}
    .faq-chevron {{ transition: transform 0.2s ease; flex-shrink: 0; }}
    .faq-item.open .faq-chevron {{ transform: rotate(180deg); }}

    .breadcrumb {{ font-size: 12px; color: rgba(255,255,255,0.35); display: flex; align-items: center; gap: 8px; }}
    .breadcrumb a:hover {{ color: rgba(255,255,255,0.6); }}

    .hero-bg {{
      background:
        radial-gradient(ellipse 80% 60% at 70% 50%, rgba(43,36,214,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 50% 70% at 20% 80%, rgba(74,59,255,0.08) 0%, transparent 50%),
        #06060F;
    }}
    .section-divider {{ border: none; border-top: 1px solid rgba(30,30,56,0.6); margin: 0; }}

    @media (max-width: 768px) {{
      .hide-mobile {{ display: none !important; }}
      .stats-grid {{ grid-template-columns: repeat(2, 1fr) !important; }}
    }}
  </style>
</head>

<body>

<!-- ═══ NAVBAR ═══ -->
<nav style="position:fixed;top:0;left:0;right:0;z-index:100;backdrop-filter:blur(16px);background:rgba(6,6,15,0.85);border-bottom:1px solid rgba(30,30,56,0.7);">
  <div style="max-width:1100px;margin:0 auto;padding:0 32px;height:64px;display:flex;align-items:center;justify-content:space-between;">
    <a href="https://lescalinglab.com/" style="display:flex;align-items:baseline;gap:0;">
      <span style="font-family:'Playfair Display',serif;font-style:italic;font-size:22px;font-weight:400;color:rgba(255,255,255,0.8);letter-spacing:-0.02em;">scaling</span><span style="font-family:'Playfair Display',serif;font-style:italic;font-size:22px;font-weight:900;background:linear-gradient(135deg,#E0DEFF,#7B6FFF);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;filter:drop-shadow(0 0 10px rgba(96,85,255,0.4));">lab'</span>
    </a>
    <div class="hide-mobile" style="display:flex;align-items:center;gap:32px;">
      <a href="https://lescalinglab.com/agences/" style="font-size:13px;font-weight:500;color:rgba(255,255,255,0.45);" onmouseover="this.style.color='rgba(255,255,255,0.9)'" onmouseout="this.style.color='rgba(255,255,255,0.45)'">Toutes les niches</a>
      <a href="https://lescalinglab.com/resultats" style="font-size:13px;font-weight:500;color:rgba(255,255,255,0.45);" onmouseover="this.style.color='rgba(255,255,255,0.9)'" onmouseout="this.style.color='rgba(255,255,255,0.45)'">Résultats élèves</a>
    </div>
    <a href="https://lescalinglab.com/#apply" class="btn-primary" style="padding:10px 22px;font-size:13px;">Candidater →</a>
  </div>
</nav>

<!-- ═══ HERO ═══ -->
<section class="hero-bg" style="padding:104px 32px 64px;position:relative;overflow:hidden;">
  <div style="max-width:860px;margin:0 auto;position:relative;z-index:3;">

    <div class="breadcrumb" style="margin-bottom:28px;">
      <a href="https://lescalinglab.com/">Accueil</a>
      <span>›</span>
      <a href="https://lescalinglab.com/agences/">Niches</a>
      <span>›</span>
      <span style="color:rgba(200,196,255,0.6);">{n['parent_page_name']}</span>
    </div>

    <div class="pill" style="margin-bottom:28px;width:fit-content;">
      <span class="pill-dot"></span>
      {n['pill_text']}
    </div>

    <h1 style="margin-bottom:24px;">
      <span class="display-bold" style="font-size:clamp(28px,4vw,52px);display:block;line-height:1.05;color:#fff;">{n['title_short']} :</span>
      <span class="display-bold" style="font-size:clamp(20px,2.8vw,38px);display:block;line-height:1.1;background:linear-gradient(135deg,#C8C4FF 0%,#6055FF 50%,#3B2FE8 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-top:8px;">{n['stat1_num']} {n['stat1_label'].lower()}, {n['stat2_num']} {n['stat2_label'].lower()}</span>
    </h1>

    <p style="font-size:17px;line-height:1.75;color:rgba(255,255,255,0.55);max-width:640px;margin-bottom:40px;">
      {extras['hero_lead']}
    </p>

    <div class="stats-grid" style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:600px;">
      <div class="stat-card">
        <div class="stat-num">{n['stat1_num']}</div>
        <div class="stat-label">{n['stat1_label']}</div>
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

<!-- ═══ LE MARCHÉ ═══ -->
<section style="padding:72px 32px;background:#06060F;">
  <div style="max-width:860px;margin:0 auto;">
    <div class="label" style="margin-bottom:16px;">Le marché</div>
    <h2 class="heading-oswald" style="font-size:clamp(22px,3vw,34px);color:#fff;margin-bottom:16px;">Pourquoi c'est une niche à fort potentiel</h2>
    <p style="font-size:15px;line-height:1.75;color:rgba(255,255,255,0.5);margin-bottom:40px;max-width:680px;">
      {n['market_body']}
    </p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;">
{mc}
    </div>
  </div>
</section>

<hr class="section-divider" />

<!-- ═══ LES PROBLÈMES ═══ -->
<section style="padding:72px 32px;background:rgba(12,12,30,0.3);">
  <div style="max-width:860px;margin:0 auto;">
    <div class="label" style="margin-bottom:16px;">Le problème</div>
    <h2 class="heading-oswald" style="font-size:clamp(22px,3vw,34px);color:#fff;margin-bottom:12px;">L'acquisition dans cette niche : comment ça marche vraiment</h2>
    <p style="font-size:15px;line-height:1.75;color:rgba(255,255,255,0.5);margin-bottom:40px;max-width:660px;">
      {extras['problem_lead']}
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

<!-- ═══ L'INFRASTRUCTURE ═══ -->
<section style="padding:72px 32px;background:#06060F;">
  <div style="max-width:860px;margin:0 auto;">
    <div class="label" style="margin-bottom:16px;">Ce que tu vends</div>
    <h2 class="heading-oswald" style="font-size:clamp(22px,3vw,34px);color:#fff;margin-bottom:12px;">L'infrastructure IA concrète</h2>
    <p style="font-size:15px;line-height:1.75;color:rgba(255,255,255,0.5);margin-bottom:40px;max-width:660px;">
      {extras['infra_lead']}
    </p>

    <div class="glow-card" style="padding:32px;margin-bottom:32px;">
      <div class="infra-item">
        <div class="infra-icon">⚡</div>
        <div>
          <div style="font-weight:600;font-size:14px;color:#fff;margin-bottom:6px;">{n['infra1_title']}</div>
          <div style="font-size:13px;line-height:1.65;color:rgba(255,255,255,0.5);">{n['infra1_body']}</div>
        </div>
      </div>
      <div class="infra-item">
        <div class="infra-icon">🔄</div>
        <div>
          <div style="font-weight:600;font-size:14px;color:#fff;margin-bottom:6px;">{n['infra2_title']}</div>
          <div style="font-size:13px;line-height:1.65;color:rgba(255,255,255,0.5);">{n['infra2_body']}</div>
        </div>
      </div>
      <div class="infra-item">
        <div class="infra-icon">📣</div>
        <div>
          <div style="font-weight:600;font-size:14px;color:#fff;margin-bottom:6px;">{n['infra3_title']}</div>
          <div style="font-size:13px;line-height:1.65;color:rgba(255,255,255,0.5);">{n['infra3_body']}</div>
        </div>
      </div>
      <div class="infra-item">
        <div class="infra-icon">{i4_icon}</div>
        <div>
          <div style="font-weight:600;font-size:14px;color:#fff;margin-bottom:6px;">{i4_title}</div>
          <div style="font-size:13px;line-height:1.65;color:rgba(255,255,255,0.5);">{i4_body}</div>
        </div>
      </div>
    </div>

    <!-- Ticket -->
    <div style="background:rgba(59,47,232,0.1);border:1px solid rgba(96,85,255,0.2);border-radius:14px;padding:28px;display:flex;gap:32px;flex-wrap:wrap;align-items:center;">
      <div>
        <div style="font-size:11px;font-family:'Oswald',sans-serif;letter-spacing:0.18em;text-transform:uppercase;color:rgba(200,196,255,0.5);margin-bottom:6px;">Ticket setup</div>
        <div style="font-family:'Oswald',sans-serif;font-size:28px;font-weight:700;background:linear-gradient(135deg,#C8C4FF,#6055FF);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{n['ticket_setup']}</div>
      </div>
      <div style="width:1px;height:40px;background:rgba(96,85,255,0.2);flex-shrink:0;" class="hide-mobile"></div>
      <div>
        <div style="font-size:11px;font-family:'Oswald',sans-serif;letter-spacing:0.18em;text-transform:uppercase;color:rgba(200,196,255,0.5);margin-bottom:6px;">Retainer mensuel</div>
        <div style="font-family:'Oswald',sans-serif;font-size:28px;font-weight:700;background:linear-gradient(135deg,#C8C4FF,#6055FF);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{n['ticket_retainer']}/mois</div>
      </div>
      <div style="flex:1;min-width:200px;">
        <div style="font-size:13px;line-height:1.6;color:rgba(255,255,255,0.45);">{extras['ticket_note']}</div>
      </div>
    </div>
  </div>
</section>

<hr class="section-divider" />

<!-- ═══ RÉSULTAT ÉLÈVE ═══ -->
<section style="padding:72px 32px;background:rgba(12,12,30,0.4);">
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
{student_grid}
      <p style="font-size:14px;line-height:1.75;color:rgba(255,255,255,0.45);margin-top:24px;">{n['student_desc']}</p>
    </div>
    <p style="font-size:13px;color:rgba(255,255,255,0.3);margin-top:16px;">
      Résultat individuel — voir tous les cas élèves sur <a href="https://lescalinglab.com/resultats" style="color:rgba(200,196,255,0.5);">lescalinglab.com/resultats</a>
    </p>
  </div>
</section>

<hr class="section-divider" />

<!-- ═══ CTA PROGRAMME ═══ -->
<section style="padding:72px 32px;background:#06060F;">
  <div style="max-width:860px;margin:0 auto;text-align:center;">
    <div class="label" style="margin-bottom:16px;text-align:center;">Le programme</div>
    <h2 class="heading-oswald" style="font-size:clamp(22px,3vw,36px);color:#fff;margin-bottom:16px;">Comment le Scaling Lab' t'aide à conquérir cette niche</h2>
    <p style="font-size:15px;line-height:1.75;color:rgba(255,255,255,0.5);max-width:620px;margin:0 auto 40px;">
      Le programme 1-1 d'Abdé Chan couvre le positionnement sur la niche, la construction de l'infrastructure GHL adaptée, les scripts d'approche, et la vente du premier contrat. 3 à 5 participants par mois maximum.
    </p>
    <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
      <a href="https://lescalinglab.com/#apply" class="btn-primary">Candidater au programme →</a>
      <a href="https://lescalinglab.com/resultats" class="btn-ghost">Voir tous les résultats élèves</a>
    </div>
  </div>
</section>

<hr class="section-divider" />

<!-- ═══ FAQ ═══ -->
<section style="padding:72px 32px;background:rgba(12,12,30,0.3);">
  <div style="max-width:720px;margin:0 auto;">
    <div class="label" style="margin-bottom:16px;">FAQ</div>
    <h2 class="heading-oswald" style="font-size:clamp(20px,2.5vw,30px);color:#fff;margin-bottom:40px;">Questions fréquentes — {n['label_raw'].lower()}</h2>
    <div id="faq-list">
{faq_html}
    </div>
  </div>
</section>
{cities}

<!-- ═══ FOOTER ═══ -->
<footer style="padding:40px 32px;border-top:1px solid rgba(30,30,56,0.8);background:#06060F;">
  <div style="max-width:1100px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;">
    <div style="display:flex;flex-direction:column;gap:5px;">
      <a href="https://lescalinglab.com/" style="display:flex;align-items:baseline;gap:0;">
        <span style="font-family:'Playfair Display',serif;font-style:italic;font-size:20px;font-weight:400;color:rgba(255,255,255,0.5);letter-spacing:-0.02em;">scaling</span><span style="font-family:'Playfair Display',serif;font-style:italic;font-size:20px;font-weight:900;background:linear-gradient(135deg,#E0DEFF,#7B6FFF);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">lab'</span>
      </a>
      <span style="font-family:'Playfair Display',serif;font-style:italic;font-size:11px;color:rgba(200,196,255,0.3);">by Abdé Chan</span>
    </div>
    <p style="font-size:12px;color:rgba(255,255,255,0.22);">© 2026 Scaling Lab' · Accompagnement 1-1 pour Agences IA</p>
  </div>
</footer>

<!-- Animated grid background -->
<script>
(function(){{
  const CELL=40,STROKE='rgba(96,85,255,0.18)',FILL='#5048FF',NUM=30,MAX=0.14,DUR=2800;
  const ns='http://www.w3.org/2000/svg';
  const svg=document.createElementNS(ns,'svg');
  svg.setAttribute('aria-hidden','true');
  svg.style.cssText='position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none;overflow:visible;';
  const defs=document.createElementNS(ns,'defs');
  const pat=document.createElementNS(ns,'pattern');
  pat.setAttribute('id','{gp}');pat.setAttribute('width',CELL);pat.setAttribute('height',CELL);pat.setAttribute('patternUnits','userSpaceOnUse');
  const lp=document.createElementNS(ns,'path');lp.setAttribute('d',`M.5 ${{CELL}}V.5H${{CELL}}`);lp.setAttribute('fill','none');lp.setAttribute('stroke',STROKE);lp.setAttribute('stroke-width','0.5');
  pat.appendChild(lp);defs.appendChild(pat);svg.appendChild(defs);
  const bg=document.createElementNS(ns,'rect');bg.setAttribute('width','100%');bg.setAttribute('height','100%');bg.setAttribute('fill','url(#{gp})');svg.appendChild(bg);
  const grp=document.createElementNS(ns,'g');svg.appendChild(grp);
  document.body.prepend(svg);
  function cols(){{return Math.floor(window.innerWidth/CELL);}}
  function rows(){{return Math.floor(window.innerHeight/CELL);}}
  function spawn(){{
    const r=document.createElementNS(ns,'rect');
    r.setAttribute('width',CELL);r.setAttribute('height',CELL);
    r.setAttribute('x',Math.floor(Math.random()*cols())*CELL);
    r.setAttribute('y',Math.floor(Math.random()*rows())*CELL);
    r.setAttribute('fill',FILL);r.setAttribute('opacity','0');
    grp.appendChild(r);
    let t=performance.now();
    function step(now){{
      const p=(now-t)/DUR;
      if(p<0.5){{r.setAttribute('opacity',p*2*MAX);}}
      else if(p<1){{r.setAttribute('opacity',(1-(p-0.5)*2)*MAX);}}
      else{{grp.removeChild(r);return;}}
      requestAnimationFrame(step);
    }}
    requestAnimationFrame(step);
  }}
  setInterval(()=>{{if(grp.childNodes.length<NUM)spawn();}},DUR/NUM);
}})();
</script>

<!-- FAQ toggle -->
<script>
function toggleFaq(btn){{
  const item=btn.closest('.faq-item');
  item.classList.toggle('open');
}}
</script>

<!-- z-index fix -->
<style>nav, section, footer {{ position: relative; z-index: 2; }}</style>

</body>
</html>"""


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    base_dir   = os.path.dirname(os.path.abspath(__file__))
    agences_dir = os.path.join(base_dir, 'agences')
    sitemap_path = os.path.join(base_dir, 'sitemap.xml')
    today = date.today().isoformat()
    new_urls = []

    for slug in NEW_NICHES:
        niche  = NICHES[slug]
        extras = NICHE_EXTRAS[slug]
        out_dir = os.path.join(agences_dir, slug)
        os.makedirs(out_dir, exist_ok=True)
        html = generate_page(slug, niche, extras)
        out_path = os.path.join(out_dir, 'index.html')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        url = f"https://lescalinglab.com/agences/{slug}/"
        new_urls.append(url)
        print(f"  ✓ agences/{slug}/index.html")

    # ─── Mise à jour sitemap ───
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns_uri = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns_uri)
    existing = {u.find(f'{{{ns_uri}}}loc').text
                for u in root.findall(f'{{{ns_uri}}}url')}
    for url in new_urls:
        if url not in existing:
            el = ET.SubElement(root, f'{{{ns_uri}}}url')
            ET.SubElement(el, f'{{{ns_uri}}}loc').text = url
            ET.SubElement(el, f'{{{ns_uri}}}lastmod').text = today
            ET.SubElement(el, f'{{{ns_uri}}}changefreq').text = 'weekly'
            ET.SubElement(el, f'{{{ns_uri}}}priority').text = '0.8'
    ET.indent(tree, space='  ')
    tree.write(sitemap_path, encoding='UTF-8', xml_declaration=True)

    print(f"\n✅ {len(NEW_NICHES)} pages niche générées")
    print(f"✅ sitemap.xml mis à jour (+{len(new_urls)} URLs)")


if __name__ == '__main__':
    main()
