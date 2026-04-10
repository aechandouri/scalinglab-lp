#!/usr/bin/env python3
"""
generate_problematiques_pages.py
Génère /agences/comment-[slug]/index.html — 4ème axe SEO (10 pages problématiques).
Target queries: "comment créer une offre agence IA", "comment booker des appels qualifiés agence IA", etc.
Usage : python3 generate_problematiques_pages.py
"""

import os, hashlib, json, re
import xml.etree.ElementTree as ET
from datetime import date

# ─── Répertoires ─────────────────────────────────────────────────────────────
_dir = os.path.dirname(os.path.abspath(__file__))
AGENCES_DIR = os.path.join(_dir, "agences")
SITEMAP_PATH = os.path.join(_dir, "sitemap.xml")
YT_JSON_PATH = "/Users/hagravolontaire/story-generator/inputs/youtube/Youtubev2.json"
BASE_URL = "https://lescalinglab.com"

# ─── YouTube data ─────────────────────────────────────────────────────────────
with open(YT_JSON_PATH, encoding="utf-8") as f:
    YT_DATA = json.load(f)

def yt_excerpt(title_fragment, max_chars=400):
    """Trouve la vidéo dont le titre contient title_fragment et retourne un extrait du transcript."""
    for item in YT_DATA:
        if title_fragment.lower() in item.get("videoTitle", "").lower():
            text = item.get("text", "")
            # Prend un passage de milieu du texte, évite le début générique
            start = min(200, len(text) // 4)
            return text[start:start + max_chars].strip()
    return ""

def yt_url(title_fragment):
    for item in YT_DATA:
        if title_fragment.lower() in item.get("videoTitle", "").lower():
            return item.get("videoUrl", "")
    return ""

def yt_title(title_fragment):
    for item in YT_DATA:
        if title_fragment.lower() in item.get("videoTitle", "").lower():
            return item.get("videoTitle", "")
    return title_fragment

# ─── 10 PROBLÉMATIQUES ────────────────────────────────────────────────────────
PROBLEMATIQUES = {
    "comment-creer-offre-agence-ia": {
        "slug":      "comment-creer-offre-agence-ia",
        "h1":        "Comment créer une offre irrésistible pour ton agence IA",
        "title_tag": "Comment créer une offre agence IA à 10k€+ | Scaling Lab'",
        "meta_desc": "La méthode pour construire une offre d'agence IA que tes clients ne peuvent pas refuser — positionnement, valeur, prix. Par Abdé Chan.",
        "hero_lead":  "La majorité des agences IA restent bloquées sous 5k€/mois non pas parce qu'elles manquent de compétences techniques, mais parce qu'elles vendent une prestation au lieu de vendre un résultat.",
        "problem":   "Ton offre ressemble à celle de 95% des agences — et le prospect ne voit aucune raison de te choisir toi.",
        "problem_list": [
            "Tu proposes «&nbsp;automatisation IA&nbsp;» sans résultat mesurable — le prospect ne comprend pas la valeur",
            "Tu te positionnes comme un prestataire technique plutôt que comme un partenaire de croissance",
            "Ton prix est basé sur ton temps, pas sur la transformation que tu apportes",
            "Tu n'as pas de niche claire — tu t'adresses à tout le monde, ce qui ne convainc personne",
        ],
        "method_title": "La méthode Scaling Lab' : offre axée résultat",
        "method_steps": [
            ("Choisir une niche verticale spécifique", "Pas «&nbsp;restaurants&nbsp;», mais «&nbsp;restaurants gastronomiques 50-200 couverts&nbsp;». La spécificité = crédibilité immédiate."),
            ("Définir le résultat livré, pas la prestation", "«&nbsp;15 RDV qualifiés en 30 jours via l'IA&nbsp;» vaut 10 000× «&nbsp;mise en place d'un chatbot&nbsp;». Le client paie un résultat, pas des heures."),
            ("Construire le stack qui délivre ce résultat", "Meta/Google Ads → agent IA de qualification → séquence de pré-vente automatisée dans GoHighLevel. Clé en main, pas de code nécessaire."),
            ("Pricer à la valeur, pas au temps", "Si tu génères 30k€ de CA à ton client, 5 000€ de setup + 1 500€/mois est une évidence. Arrête de penser en coût horaire."),
        ],
        "yt_fragment":  "je crée une offre IA à 10k€",
        "yt_fragment2": "la raison pour laquelle t'es bloqué sous 10k",
        "stat_a": ("27 000 €/mois", "revenus d'agence d'Abdé Chan"),
        "stat_b": ("10 000 → 30 000 €", "ticket setup Ryan (BTP)"),
        "stat_c": ("×3,8", "médiane revenus en 6 mois"),
        "faqs": [
            ("Comment différencier son offre des autres agences IA ?",
             "En vendant un résultat chiffré sur une niche précise, pas une prestation technique. «&nbsp;15 RDV qualifiés pour centres esthétiques en 30 jours, garanti&nbsp;» bat «&nbsp;automatisation IA GoHighLevel&nbsp;» à chaque fois."),
            ("Quel est le bon prix pour une offre d'agence IA ?",
             "Un setup entre 2 000 et 15 000 € selon la complexité de l'infrastructure + 500 à 2 000 €/mois de retainer. Le programme Scaling Lab' cible 3 000 à 8 000 € de ticket moyen."),
            ("Faut-il savoir coder pour livrer une offre IA ?",
             "Non. Toute l'infrastructure se construit avec GoHighLevel, Make et les APIs IA — aucune ligne de code. Si tu sais utiliser un navigateur, tu peux livrer ces systèmes."),
            ("Combien de temps pour construire son offre ?",
             "Dans le programme, le positionnement offre est finalisé en 2 à 4 semaines. Le premier client suit généralement dans les 30 à 60 jours."),
            ("Peut-on vendre une offre IA sans avoir de cas clients ?",
             "Oui — en utilisant les résultats d'autres élèves du programme comme preuves sociales de la méthode, et en proposant un premier client à tarif pilote contre témoignage. C'est exactement comme ça qu'Abdé a démarré."),
        ],
        "related_niches": ["centres-esthetiques", "btp-construction", "immobilier", "coaching-consultants", "experts-comptables"],
    },
    "comment-choisir-niche-agence-ia": {
        "slug":      "comment-choisir-niche-agence-ia",
        "h1":        "Comment choisir la bonne niche pour ton agence IA",
        "title_tag": "Comment choisir sa niche agence IA en 2025 | Scaling Lab'",
        "meta_desc": "Comment choisir une niche rentable pour ton agence IA — critères de sélection, niches validées, erreurs à éviter. Par Abdé Chan.",
        "hero_lead":  "La niche n'est pas une prison — c'est un avantage concurrentiel. Les agences qui se niches sur un secteur fermé leurs concurrents non niches dans les 6 mois.",
        "problem":   "Tu cibles tout le monde — et personne ne te répond.",
        "problem_list": [
            "Tu t'adresses à «&nbsp;toutes les PME&nbsp;» — ce qui veut dire que ton message ne résonne avec personne",
            "Tu changes de niche chaque mois selon ce que tu lis sur LinkedIn",
            "Tu penses que ton marché est saturé alors que 80% des business locaux n'ont aucune IA",
            "Tu n'as pas de connaissance sectorielle et tu ne sais pas quoi promettre à ton prospect",
        ],
        "method_title": "Les 5 critères pour une niche rentable en 2025",
        "method_steps": [
            ("Volume suffisant", "Au moins 10 000 établissements en France. Restaurants (175k), BTP (440k), plombiers/électriciens (200k), coiffure (85k) — tous validés."),
            ("Pain point fort et mesurable", "Le client perd de l'argent de manière identifiable : leads non relancés, no-shows, paniers abandonnés, devis non suivis. Ce que tu règles doit être quantifiable."),
            ("Capacité à payer (ticket ≥ 2 000 €)", "Évite les niches avec marges serrées. Priorise : dentistes, avocats, agences immo, solaire, centres esthétiques, BTP — des secteurs à revenu par client élevé."),
            ("Faible sophistication IA actuelle", "Si le secteur est déjà blindé de solutions IA, entre dans une niche adjacente. En 2025, 75+ niches sont encore quasi-vierges."),
            ("Référençabilité", "Une niche où les clients se parlent entre eux (associations pros, salons, réseaux). Un cas client dans le secteur = 5 prospects chauds instantanément."),
        ],
        "yt_fragment":  "Faut-il vraiment se nicher",
        "yt_fragment2": "Regarde cette vidéo si tu penses que ton marché est saturé",
        "stat_a": ("75+", "niches validées dans le programme"),
        "stat_b": ("15 niches", "couvertes sur lescalinglab.com/agences/"),
        "stat_c": ("100j", "délai moyen premier système complet"),
        "faqs": [
            ("Faut-il vraiment se nicher pour réussir avec une agence IA ?",
             "Oui. Abdé Chan l'a démontré scientifiquement dans une vidéo YouTube dédiée : une agence nichée sur 1 secteur ferme ses concurrents généralistes dans les 6 mois. La spécificité = crédibilité = closing plus facile."),
            ("Quelle est la meilleure niche pour démarrer une agence IA ?",
             "Les niches les plus accessibles pour débuter : BTP/construction (440k entreprises, pain point leads non suivis), centres esthétiques (13k cabinets, Louis a fait 3k→58k€/mois), thérapeutes (30k praticiens, Sally 0→18k€/mois)."),
            ("Mon marché est-il vraiment saturé ?",
             "Non. En 2025, moins de 5% des business locaux francophones utilisent une IA pour leur acquisition. La saturation est une excuse. Ce qui est saturé : les SMMA bas de gamme. Ce qui est vierge : les infrastructures IA clé en main à 3 000-8 000 €."),
            ("Peut-on changer de niche en cours de route ?",
             "Possible mais coûteux. Chaque changement remet à zéro ta réputation sectorielle. Choisir une niche solide dès le départ est l'un des 3 premiers travaux du programme."),
            ("Combien de niches peut-on cibler simultanément ?",
             "Une seule au départ. Abdé Chan l'impose : une niche, une offre, un avatar. La diversification vient après le premier client, pas avant."),
        ],
        "related_niches": ["centres-esthetiques", "btp-construction", "therapeutes", "solaire", "dentistes"],
    },
    "comment-generer-trafic-agence-ia": {
        "slug":      "comment-generer-trafic-agence-ia",
        "h1":        "Comment générer du trafic qualifié pour une agence IA",
        "title_tag": "Comment générer du trafic pour une agence IA | Scaling Lab'",
        "meta_desc": "Les 3 canaux d'acquisition validés pour une agence IA en 2025 — Meta Ads, cold outreach, contenu B2B. Par Abdé Chan (27k€/mois d'agence).",
        "hero_lead":  "La technique IA ne fait pas de mal. Ce qui tue 99% des agences : l'incapacité à générer des prospects réguliers. Le trafic est la compétence n°1.",
        "problem":   "Tu maîtrises GoHighLevel mais ton pipeline est vide depuis 3 semaines.",
        "problem_list": [
            "Tu passes 80% de ton temps à apprendre la technique et 0% à prospecter",
            "Tu attends que des clients arrivent «&nbsp;naturellement&nbsp;» via ton profil LinkedIn",
            "Tu as testé un canal une semaine et conclu que «&nbsp;ça ne marche pas&nbsp;»",
            "Tu n'as pas de système d'acquisition — tu envoies des messages quand tu penses y penser",
        ],
        "method_title": "Le système multicanal 3 axes",
        "method_steps": [
            ("Meta Ads (acquisition payante)", "La VSL vidéo + landing page simple. Coût par appel qualifié cible : 49€ (record d'Abdé, divisé par 3 vs son point de départ à 153€). Budget minimal : 1 500€/mois pour tester."),
            ("Cold outreach ciblé", "Séquence email/LinkedIn personnalisée sur 7 touchpoints. Pas du volume — de la pertinence. 30 emails/jour sur un ICP précis génèrent plus d'appels que 300 emails génériques."),
            ("Contenu B2B ciblé niche", "1 vidéo courte par semaine qui parle directement au douleur de ta niche. Pas de personal branding générique — du contenu qui génère des inbounds du secteur ciblé."),
            ("La règle des 2 canaux minimum", "Abdé l'exige : tu dois opérer au moins 2 des 3 canaux simultanément. Un seul canal = un seul point de défaillance. Deux canaux = stabilité du pipeline."),
        ],
        "yt_fragment":  "j'ai divisé par 3 mon coût par appel",
        "yt_fragment2": "la VSL qui génère 35-50 appels",
        "stat_a": ("49 €", "coût par appel qualifié d'Abdé Chan"),
        "stat_b": ("35–50 appels", "générés/mois avec la bonne VSL"),
        "stat_c": ("×3", "réduction du CPL avec la méthode"),
        "faqs": [
            ("Quelle est la meilleure source de leads pour une agence IA ?",
             "La combinaison Meta Ads + cold outreach est la plus robuste en 2025. Les Ads génèrent du volume, l'outreach génère de la qualité. Le contenu B2B génère des inbounds chauds sur 3 à 6 mois."),
            ("Quel budget pub faut-il pour lancer une agence IA ?",
             "1 500 à 3 000 €/mois est le seuil de test viable pour les Meta Ads. Sans ce budget, concentre-toi sur le cold outreach (coût : 0) et le contenu organique jusqu'à avoir des revenus récurrents."),
            ("Comment créer une VSL qui génère des appels ?",
             "Abdé a une vidéo entière dédiée sur YouTube. Les 4 éléments clés : crochet en 5 secondes, problème du prospect verbalisé exactement comme il le vit, preuve sociale chiffrée, CTA direct."),
            ("Combien de temps avant d'avoir son premier appel de vente ?",
             "En cold outreach, 2 à 4 semaines avec une séquence bien construite. En Ads, 1 à 2 semaines avec le bon angle. Dans le programme, la majorité des élèves ont leur premier appel en moins de 30 jours."),
            ("Faut-il faire du SEO pour une agence IA ?",
             "Pas prioritaire au départ. Le SEO est un canal lent (6-12 mois pour des résultats). Pour les premiers 0 à 10k€/mois, priorise les canaux d'acquisition rapides : outreach + Ads."),
        ],
        "related_niches": ["immobilier", "btp-construction", "solaire", "restaurants", "e-commerce"],
    },
    "comment-booker-appels-qualifies-agence-ia": {
        "slug":      "comment-booker-appels-qualifies-agence-ia",
        "h1":        "Comment booker des appels de vente qualifiés pour ton agence IA",
        "title_tag": "Comment booker des appels qualifiés agence IA | Scaling Lab'",
        "meta_desc": "Système pour remplir ton calendrier d'appels qualifiés — VSL, séquences outreach, qualification IA. Par Abdé Chan.",
        "hero_lead":  "Avoir une belle infrastructure GoHighLevel sans appels dans le calendrier, c'est avoir un restaurant cinq étoiles vide. Les appels qualifiés sont l'oxygène de l'agence.",
        "problem":   "Tu as une offre, tu as une page de vente — mais ton calendrier Calendly reste désespérément vide.",
        "problem_list": [
            "Tu envoies des DMs sans système — quelques messages le lundi, rien le reste de la semaine",
            "Ta page de réservation convertit à 2% parce que le prospect ne comprend pas ce qu'il va obtenir",
            "Tu cibles un trop large public — les gens qui bookent ne sont pas qualifiés et font perdre du temps",
            "Tu n'as pas de VSL ou de séquence de nurturing pour chauffer les prospects avant l'appel",
        ],
        "method_title": "Le système complet book-to-close",
        "method_steps": [
            ("La page de réservation qualifiante", "Un formulaire de pré-qualification en 5 questions élimine 60% des non-qualifiés avant l'appel. Tu n'acceptes que les prospects qui cochent les critères ICP."),
            ("La VSL de 5 à 15 minutes", "Vidéo courte qui explique ta méthode, montre un résultat client, et pose le contexte de l'appel. Un prospect qui a regardé la VSL arrive avec 80% de l'éducation faite."),
            ("La séquence de confirmation automatisée", "Rappel SMS + email 24h avant + 1h avant. Taux de no-show moyen sans séquence : 30 à 50%. Avec séquence : moins de 10%."),
            ("Le scoring IA des leads entrants", "Dans GoHighLevel, un agent IA peut scorer chaque lead entrant selon ses réponses au formulaire et déclencher automatiquement la relance ou la mise en attente."),
        ],
        "yt_fragment":  "j'ai divisé par 3 mon coût par appel",
        "yt_fragment2": "la VSL qui génère 35-50 appels",
        "stat_a": ("153€ → 49€", "coût/appel réduit par 3 par Abdé Chan"),
        "stat_b": ("-40%", "no-shows avec séquence de confirmation"),
        "stat_c": ("35–50", "appels/mois avec la méthode VSL"),
        "faqs": [
            ("Comment réduire le coût par appel qualifié ?",
             "La combinaison VSL + formulaire de pré-qualification + reciblage Ads est la méthode d'Abdé — passé de 153€ à 49€/appel. Chaque élément du funnel compte."),
            ("Comment éviter les no-shows en appel de vente ?",
             "Séquence automatisée : confirmation immédiate par email + SMS, rappel J-1, rappel H-1. Un lien de replanification direct. Résultat : moins de 10% de no-shows vs 30-50% sans système."),
            ("Faut-il une page de réservation dédiée ?",
             "Oui. Une page qui explique ce que le prospect va obtenir de l'appel + un formulaire de 4-6 questions de pré-qualification. Sans qualification, tu passes des heures avec des prospects non sérieux."),
            ("Comment qualifier les leads entrants automatiquement ?",
             "Un agent IA dans GoHighLevel peut analyser les réponses au formulaire, scorer chaque lead, et déclencher différentes séquences selon le score. Un prospect à fort potentiel reçoit un appel personnalisé, un prospect froid reçoit un nurturing automatique."),
            ("Combien d'appels par semaine faut-il viser ?",
             "5 à 10 appels qualifiés par semaine est un objectif réaliste avec un système en place. À un taux de closing de 30%, ça représente 1 à 3 nouveaux clients par semaine."),
        ],
        "related_niches": ["centres-esthetiques", "dentistes", "avocats", "experts-comptables", "coaching-consultants"],
    },
    "comment-closer-appels-vente-agence-ia": {
        "slug":      "comment-closer-appels-vente-agence-ia",
        "h1":        "Comment closer en appel de vente pour une agence IA",
        "title_tag": "Comment closer ses appels de vente agence IA | Scaling Lab'",
        "meta_desc": "Script et méthode pour closer 30 à 40% de ses appels de vente en agence IA — les 7 leviers psychologiques. Par Abdé Chan.",
        "hero_lead":  "La vente n'est pas un talent inné. C'est un script qu'on maîtrise. Les meilleurs closeurs d'agences IA suivent un processus reproductible, pas une improvisation.",
        "problem":   "Tu as des appels. Ils se terminent par «&nbsp;je vais y réfléchir&nbsp;». Tu ne sais pas pourquoi ils ne signent pas.",
        "problem_list": [
            "Tu présentes ton offre trop tôt — avant d'avoir compris le problème réel du prospect",
            "Tu ne quantifies pas le coût du statu quo — le prospect ne ressent pas l'urgence",
            "Tu réponds aux objections au lieu de les prévenir dans la structure de l'appel",
            "Tu te tais quand il faut continuer et tu continues quand il faut se taire",
        ],
        "method_title": "Le framework de closing en 5 phases",
        "method_steps": [
            ("Phase 1 : Rapport et cadrage (5 min)", "Poser le contexte de l'appel, confirmer les attentes, créer de la sécurité psychologique. Les 5 premières minutes déterminent 80% du résultat."),
            ("Phase 2 : Diagnostic profond (15 min)", "10 à 15 questions ouvertes sur la situation actuelle, les objectifs, les obstacles, les coûts de l'inaction. Laisse le prospect verbaliser sa douleur."),
            ("Phase 3 : Présentation axée résultat (10 min)", "Adapte la présentation de l'offre aux points de douleur identifiés. Pas un pitch générique — une solution au problème exact qu'il vient d'expliquer."),
            ("Phase 4 : Traitement des objections (5 min)", "Les 4 objections universelles : prix, timing, confiance, décision. Anticipe-les dans la présentation pour ne pas les affronter en fin d'appel."),
            ("Phase 5 : Closing et next step clair (5 min)", "Ne termine jamais un appel sans une prochaine étape définie. Contrat signé, ou date de relance fixée, ou raison claire de l'abandon."),
        ],
        "yt_fragment":  "comment je vends (sans effort) avec la dark psychology",
        "yt_fragment2": "51 min pour closer TOUS tes appels",
        "stat_a": ("30–40%", "taux de closing garanti par la méthode"),
        "stat_b": ("51 min", "durée d'appel idéale selon Abdé Chan"),
        "stat_c": ("7 leviers", "psychologiques du script de vente"),
        "faqs": [
            ("Quel est le taux de closing normal pour une agence IA ?",
             "Avec des prospects bien qualifiés et un script maîtrisé, 30 à 40% est l'objectif. Abdé garantit ce taux à ses élèves avec la méthode enseignée dans le programme."),
            ("Comment gérer l'objection prix en appel de vente ?",
             "Ne jamais défendre son prix — montrer la valeur. Si le prospect dit «&nbsp;c'est trop cher&nbsp;», tu n'as pas suffisamment quantifié ce qu'il perd actuellement et ce qu'il gagne avec ton infrastructure."),
            ("Faut-il envoyer une proposition après l'appel ?",
             "Non au sens classique du terme. L'offre doit être présentée et acceptée pendant l'appel. Un PDF envoyé après l'appel est généralement ignoré. Si le prospect a besoin de «&nbsp;réfléchir&nbsp;», le closing a échoué pendant l'appel."),
            ("Comment dépasser l'objection 'je vais en parler à mon associé' ?",
             "L'inclure dans l'appel si possible, sinon décrocher un engagement conditionnel fort : «&nbsp;Si votre associé est ok, vous signez demain ?&nbsp;» + relance calendée. Sans engagement conditionnel, l'opportunité meurt."),
            ("Peut-on closer par email ou message ?",
             "Rarement pour des tickets > 2 000 €. L'appel vidéo est le minimum pour créer la confiance nécessaire. Certains élèves closent par WhatsApp sur des petits tickets (< 1 500€) mais c'est l'exception."),
        ],
        "related_niches": ["btp-construction", "immobilier", "avocats", "solaire", "coaching-consultants"],
    },
    "comment-livrer-clients-agence-ia": {
        "slug":      "comment-livrer-clients-agence-ia",
        "h1":        "Comment livrer ses clients avec une agence IA — sans te noyer",
        "title_tag": "Comment livrer ses clients agence IA sans se noyer | Scaling Lab'",
        "meta_desc": "Système de livraison d'infrastructure IA pour agences — GoHighLevel, onboarding, suivi, rapport automatisé. Par Abdé Chan.",
        "hero_lead":  "Une agence qui ne livre pas est une agence qui s'effondre. La réputation se construit sur les résultats clients — pas sur les promesses commerciales.",
        "problem":   "Tu as des clients mais tu passes 60 heures par semaine à les gérer manuellement.",
        "problem_list": [
            "Pas de processus d'onboarding structuré — chaque client repart de zéro et tu réexpliques les mêmes choses",
            "Tu livres des prestations personnalisées pour chaque client au lieu d'un produit reproductible",
            "Aucun reporting automatisé — le client ne voit pas les résultats et commence à douter",
            "Tu dépends de toi-même pour tout — aucun délégation possible sans tout refaire",
        ],
        "method_title": "Le système de livraison industrialisé",
        "method_steps": [
            ("L'infrastructure GoHighLevel en snapshot", "Un snapshot GoHighLevel par niche = ton produit reproductible. Chaque nouveau client dans la même niche reçoit le même setup en 2-3 jours vs 3-4 semaines custom."),
            ("L'onboarding en 7 jours", "Checklist d'onboarding standardisée : accès, paramétrage Meta Ads, configuration du chatbot, tests. Le client est opérationnel en 1 semaine."),
            ("Le reporting automatisé mensuel", "Tableau de bord GoHighLevel partagé avec le client + rapport automatique par email le 1er de chaque mois. Le client voit les chiffres sans que tu aies à les recompiler manuellement."),
            ("Les rituels de suivi", "Call mensuel de 30 minutes pour analyser les métriques et identifier les optimisations. Slack pour les questions rapides. Réponse garantie sous 24h."),
        ],
        "yt_fragment":  "Comment Dylan est passé de 2,5k/mois à 17k/mois",
        "yt_fragment2": "Comment j'ai réduit mon taux de churn",
        "stat_a": ("7 jours", "pour un client opérationnel avec la méthode"),
        "stat_b": ("3 personnes", "dans l'agence d'Abdé pour 30k€/mois"),
        "stat_c": ("86%", "marges nettes agence Qualifieds"),
        "faqs": [
            ("Comment livrer une infrastructure IA sans être développeur ?",
             "GoHighLevel + Make + APIs IA font tout sans code. Un snapshot de l'infrastructure par niche = déploiement en 2-3 jours. Abdé Chan livre ses clients sans écrire une ligne de code depuis 3 ans."),
            ("Combien de clients peut-on gérer en même temps ?",
             "Avec des systèmes de livraison industrialisés, 8 à 15 clients simultanément est gérable seul. Abdé gère 350k€/an à 3 personnes. La clé : un produit reproductible, pas du custom à chaque fois."),
            ("Comment prouver les résultats à ses clients ?",
             "Tableau de bord GoHighLevel partagé en temps réel + rapport mensuel automatique. Les chiffres parlent d'eux-mêmes : nombre de leads générés, appels bookés, taux de qualification. Le client voit son ROI sans intervention manuelle."),
            ("Que faire quand un client ne voit pas de résultats ?",
             "Protocole de revue mensuelle : identifier le maillon faible (trafic, qualification, taux de closing). Modifier une variable à la fois. Si les résultats ne suivent pas après ajustements, le programme propose une garantie résultat."),
            ("Faut-il externaliser la livraison pour scaler ?",
             "Pas immédiatement. Industrialise d'abord ton produit jusqu'à ce qu'il soit reproductible à 90% sans toi. Ensuite seulement, recrute un technicien pour les déploiements. Abdé Chan a attendu d'être à 10k+/mois avant d'embaucher."),
        ],
        "related_niches": ["centres-esthetiques", "btp-construction", "immobilier", "dentistes", "garages-auto"],
    },
    "comment-reduire-churn-agence-ia": {
        "slug":      "comment-reduire-churn-agence-ia",
        "h1":        "Comment réduire le churn et garder ses clients en agence IA",
        "title_tag": "Comment réduire le churn agence IA | Scaling Lab'",
        "meta_desc": "Méthode pour réduire le taux de churn et maximiser la LTV de ses clients en agence IA — par Abdé Chan.",
        "hero_lead":  "Acquérir un client coûte 5 à 10 fois plus cher que le garder. Une agence avec 30% de churn mensuel construit sur du sable — peu importe combien elle signe.",
        "problem":   "Tu signes 2 clients et tu en perds 1 par mois. La croissance s'annule.",
        "problem_list": [
            "Tes clients ne voient pas les résultats parce que tu n'as pas de système de reporting",
            "L'enthousiasme du début s'érode — le client oublie pourquoi il t'a signé",
            "Aucun système de feedback — tu découvres qu'un client veut partir 48h avant l'annulation",
            "Tu n'as pas de moment «&nbsp;wow&nbsp;» dans les 30 premiers jours qui crée l'ancrage émotionnel",
        ],
        "method_title": "Le système anti-churn en 3 niveaux",
        "method_steps": [
            ("Niveau 1 : Le premier résultat en 14 jours", "Le «&nbsp;first win&nbsp;» dans les 2 premières semaines ancre la confiance. Même petit (10 leads générés, 2 appels bookés), il prouve que ça fonctionne. Sans first win, le churn commence à se préparer."),
            ("Niveau 2 : Le reporting comme levier de rétention", "Un tableau de bord que le client peut consulter en autonomie + rapport mensuel avec comparaison vs mois précédent. Le client qui voit ses chiffres grandir ne part pas."),
            ("Niveau 3 : Le système de feedback proactif", "Pulse mensuel automatique (3 questions courtes). Si la satisfaction descend, tu interviens avant la décision de résiliation. Abdé l'a fait et a divisé son taux de churn par 2."),
        ],
        "yt_fragment":  "Comment j'ai réduit mon taux de churn par 2",
        "yt_fragment2": "Comment Dylan est passé de 2,5k/mois à 17k/mois",
        "stat_a": ("÷2", "churn réduit par 2 par la méthode d'Abdé"),
        "stat_b": ("14 jours", "pour le premier résultat client"),
        "stat_c": ("86%", "marges maintenues à 350k€/an"),
        "faqs": [
            ("Quel est un taux de churn normal pour une agence IA ?",
             "Moins de 5% par mois est l'objectif. Soit moins de 1 client sur 20 qui part chaque mois. Abdé Chan cible moins de 3% après avoir mis en place ses systèmes de rétention."),
            ("Comment savoir qu'un client risque de partir ?",
             "Les signaux : il répond plus lentement, il pose moins de questions, il saute des calls mensuels. Un système de feedback automatique (pulse check mensuel) détecte ces signaux avant qu'ils deviennent une décision."),
            ("Peut-on récupérer un client qui veut partir ?",
             "Souvent oui, si tu interviens à temps. Un appel de diagnostic immédiat, une solution concrète proposée dans les 48h, et un geste commercial (mois offert, audit gratuit) suffisent dans 40 à 60% des cas."),
            ("Comment augmenter la LTV de ses clients ?",
             "Upsell naturel : une fois le premier résultat livré, propose le service complémentaire (Ads si tu as commencé par chatbot, CRM si tu as commencé par Ads). Le client satisfait accepte l'upsell dans 50%+ des cas."),
            ("Faut-il des contrats longue durée pour éviter le churn ?",
             "6 mois minimum est le standard dans le programme. Un engagement clair dès le départ + une garantie résultat rassure le client et sécurise ton revenu récurrent."),
        ],
        "related_niches": ["centres-esthetiques", "coaching-consultants", "e-commerce", "salons-coiffure", "kines-osteos"],
    },
    "comment-facturer-plus-fort-agence-ia": {
        "slug":      "comment-facturer-plus-fort-agence-ia",
        "h1":        "Comment facturer plus fort avec ton agence IA — de 500 à 5 000 €",
        "title_tag": "Comment facturer plus fort en agence IA | Scaling Lab'",
        "meta_desc": "Comment augmenter ses tarifs en agence IA — de 500-1500€ à 3000-8000€ par client. Méthode de pricing axé valeur par Abdé Chan.",
        "hero_lead":  "La différence entre 500 € et 5 000 € pour le même travail, c'est uniquement le positionnement, l'offre et la confiance — pas la complexité technique.",
        "problem":   "Tu travailles 60 heures par semaine pour 3 000 €/mois alors que la même infrastructure vaut 10 fois plus ailleurs.",
        "problem_list": [
            "Tu fixes tes prix en regardant ce que font tes concurrents sur LinkedIn — et tout le monde est au plancher",
            "Tu penses que le client ne peut pas payer plus — mais tu ne lui as jamais proposé",
            "Tu vends une prestation technique et non une transformation commerciale",
            "Tu as peur d'augmenter — et cette peur coûte des dizaines de milliers d'euros par an",
        ],
        "method_title": "Le framework de pricing à la valeur",
        "method_steps": [
            ("Calculer la valeur générée, pas ton coût", "Si ton infrastructure génère 5 RDV/mois à ton client, et que son taux de closing est de 30% à 2 000 € de ticket : 5×0.3×2 000 = 3 000 €/mois de CA supplémentaire. Facturer 1 500 €/mois est une évidence."),
            ("Présenter le ROI avant le prix", "Montre d'abord ce que le client gagne. Quand le ROI est clair (3x minimum), le prix devient une formalité. Abdé enseigne : présente la valeur, puis le prix. Jamais l'inverse."),
            ("Structurer un ticket en 3 niveaux", "Setup unique : 3 000-8 000 €. Retainer mensuel : 1 000-2 500 €. Upsell additionnel : +1 500-3 000 €. Trois niveaux de revenus par client."),
            ("La psychologie du prix haut", "Un prix élevé qualifie les clients sérieux. Les clients à 500 €/mois sont 3x plus chronophages que les clients à 3 000 €/mois. Monter les prix réduit souvent la charge de travail."),
        ],
        "yt_fragment":  "30 Milles balles en vendant",
        "yt_fragment2": "tu expliques à ton élève comment transformer un client à 3k€ en client à 7k€",
        "stat_a": ("2k–15k€", "fourchette setup projet dans le programme"),
        "stat_b": ("30 000 €", "contrat signé par Ryan (BTP)"),
        "stat_c": ("×2,3", "ticket moyen élèves après le programme"),
        "faqs": [
            ("Comment justifier des prix élevés à ses clients ?",
             "En quantifiant le ROI avant de présenter le prix. Si ton infrastructure génère 8 RDV/mois au client avec un ticket moyen de 3k€, 15 000€ de setup est justifiable en quelques secondes."),
            ("À partir de quel niveau d'expérience peut-on facturer 5k€+ ?",
             "Dès le deuxième ou troisième client si tu as un cas client à montrer. La première infrastructure peut être vendue à 1 500-2 500 € contre témoignage vidéo. La deuxième à 3 000-5 000 €. La troisième à 5 000-10 000 €."),
            ("Comment annoncer une hausse de prix à ses anciens clients ?",
             "Tu n'augmentes pas les anciens clients — tu construis le nouveau prix pour les nouveaux clients. Les anciens continuent au même tarif jusqu'à renouvellement, où tu proposes le nouveau pack. Aucun choc, aucune friction."),
            ("Comment upsell un client existant ?",
             "Attends le premier résultat significatif (généralement 30-60 jours). Présente le service complémentaire comme une «&nbsp;prochaine étape logique&nbsp;» basée sur les résultats obtenus. Le client satisfait dit oui dans plus de 50% des cas."),
            ("Quel est le bon ticket pour démarrer ?",
             "Abdé recommande 1 500-2 500€ pour le premier client (pour apprendre à livrer), puis 3 000-5 000€ pour le deuxième et au-delà. Jamais en dessous de 1 000€ — en dessous, tu travailles à perte compte tenu du temps investi."),
        ],
        "related_niches": ["btp-construction", "solaire", "dentistes", "avocats", "immobilier"],
    },
    "comment-scaler-agence-ia-50k": {
        "slug":      "comment-scaler-agence-ia-50k",
        "h1":        "Comment scaler son agence IA au-delà de 10k€/mois",
        "title_tag": "Comment scaler une agence IA à 50k€/mois | Scaling Lab'",
        "meta_desc": "La stratégie pour passer de 10k à 50k€/mois avec une agence IA — systèmes, recrutement, délégation. Par Abdé Chan.",
        "hero_lead":  "Le passage de 10k à 50k€/mois n'est pas linéaire. Ce qui t'a amené à 10k va t'empêcher d'aller plus loin — si tu ne changes pas ta structure.",
        "problem":   "Tu es à 10k€/mois mais tu travailles comme un salarié 60h/semaine et tu ne sais pas comment déléguer sans tout casser.",
        "problem_list": [
            "Tu es le goulot d'étranglement de ton agence — tout passe par toi",
            "Tu veux recruter mais tu as peur de perdre la qualité ou de manager mal",
            "Tes processus ne sont pas documentés — impossible de déléguer ce que tu n'as pas formalisé",
            "Tu n'as pas distingué les activités qui génèrent du revenu de celles qui en consomment",
        ],
        "method_title": "Le framework de scale en 4 phases",
        "method_steps": [
            ("Phase 1 : Industrialiser le produit (0-10k)", "Un snapshot GoHighLevel par niche, un onboarding standardisé, un reporting automatique. Ton produit doit être livrable sans toi avant de recruter."),
            ("Phase 2 : Déléguer la livraison (10-25k)", "Recruter un technicien junior pour les déploiements. Ton rôle : vente et stratégie client. Sa mission : exécution technique. ROI immédiat si ta livraison est documentée."),
            ("Phase 3 : Déléguer l'acquisition (25-50k)", "Un closer junior ou un setter qui gère les premières étapes du funnel. Tu closes uniquement les gros deals. Coût : 1 000-2 000 €/mois + commission. ROI : 3x minimum."),
            ("Phase 4 : Piloter par les métriques (50k+)", "Tu n'exécutes plus — tu analyses les KPIs et tu décides. Abdé a atteint cette phase à 3 personnes et 350k€/an. La structure prime sur le volume."),
        ],
        "yt_fragment":  "Pourquoi abandonner ton agence IA à 10k/mois",
        "yt_fragment2": "L'IA va enterrer 99% des agences",
        "stat_a": ("350k€/an", "revenue agence Qualifieds à 3 personnes"),
        "stat_b": ("86%", "marges nettes maintenues en scalant"),
        "stat_c": ("3 recrutements", "pour passer de 10k à 30k€/mois"),
        "faqs": [
            ("Quand est-il temps de recruter dans son agence IA ?",
             "Quand tu passes plus de 20% de ton temps sur des tâches répétitives et documentables. En pratique : autour de 8 000-12 000€/mois de revenu récurrent, quand tu as un produit industrialisé à déléguer."),
            ("Comment recruter sans prendre de risque financier ?",
             "Commence par un technicien en freelance ou à mi-temps sur mission spécifique. Pas de CDI immédiat. Teste la délégation sur 2-3 clients. Si ça fonctionne, fidélise. Si ça ne fonctionne pas, tu n'as pas de charge fixe à absorber."),
            ("Peut-on scaler une agence IA en restant seul ?",
             "Jusqu'à 15 000-20 000€/mois avec des systèmes très industrialisés. Au-delà, la limite physique arrive. Abdé est passé à 30k€+/mois en introduisant 2 personnes au bon moment."),
            ("Quel est le premier recrutement à faire ?",
             "Un technicien GoHighLevel. C'est la tâche la plus consommatrice de temps, la plus documentable, et la plus facile à déléguer. Une fois la livraison déléguée, tu te concentres sur la vente — qui est le seul levier de croissance."),
            ("Comment maintenir les marges en scalant ?",
             "En industrialisant avant de recruter. Chaque recrutement doit être justifié par un calcul ROI simple : le coût du recrutement doit être amorti en moins de 3 mois par le revenu supplémentaire généré."),
        ],
        "related_niches": ["btp-construction", "centres-esthetiques", "immobilier", "solaire", "e-commerce"],
    },
    "comment-garantir-resultats-clients-agence-ia": {
        "slug":      "comment-garantir-resultats-clients-agence-ia",
        "h1":        "Comment garantir des résultats à ses clients en agence IA",
        "title_tag": "Comment garantir des résultats clients agence IA | Scaling Lab'",
        "meta_desc": "Comment proposer une garantie résultat crédible en agence IA — structure, conditions, communication. Par Abdé Chan (Scaling Lab').",
        "hero_lead":  "La garantie résultat n'est pas un risque — c'est un avantage concurrentiel. Une agence qui garantit ses résultats ferme 2 à 3 fois plus que ses concurrents qui ne garantissent rien.",
        "problem":   "Le prospect hésite. Il a peur d'investir sans certitude de retour sur investissement.",
        "problem_list": [
            "Tu n'as pas de garantie — et le prospect perçoit ça comme un manque de confiance dans ton produit",
            "Tu as peur de promettre des résultats parce que tu n'as pas encore assez confiance dans ta livraison",
            "Tu ne sais pas comment structurer une garantie qui te protège sans te ruiner",
            "Tu penses que la garantie va te coûter de l'argent — mais sans elle, tu perds la vente",
        ],
        "method_title": "Structurer une garantie résultat sans risque",
        "method_steps": [
            ("Définir l'indicateur garanti", "Pas «&nbsp;les résultats&nbsp;» en général — une métrique spécifique et mesurable : «&nbsp;15 leads qualifiés dans les 30 premiers jours ou on travaille gratuitement jusqu'à atteindre cet objectif&nbsp;»."),
            ("Conditionner la garantie à l'exécution client", "La garantie n'est activable que si le client a respecté les conditions : budget Ads minimum maintenu, réponse aux leads sous 30 minutes, suivi des protocoles d'appel. Ça protège l'agence et responsabilise le client."),
            ("La garantie comme argument de closing", "Présenter la garantie en fin de présentation, après que le ROI a été exposé. Elle lève la dernière objection (le risque) et transforme l'hésitation en décision."),
            ("Le plan de récupération si les résultats ne viennent pas", "Un protocole de diagnostic en 48h, des ajustements identifiés, un plan d'action partagé avec le client. La garantie active montre que tu es engagé — pas que tu as échoué."),
        ],
        "yt_fragment":  "j'ai divisé par 3 mon coût par appel",
        "yt_fragment2": "comment je vends (sans effort) avec la dark psychology",
        "stat_a": ("×2–3", "taux de closing avec garantie vs sans"),
        "stat_b": ("30 jours", "délai standard pour le first win"),
        "stat_c": ("100%", "des élèves ont une garantie résultat"),
        "faqs": [
            ("Quel type de garantie proposer en agence IA ?",
             "La plus efficace : garantie de résultat conditionnel. «&nbsp;15 RDV en 30 jours, ou on continue gratuitement jusqu'à les obtenir.&nbsp;» Elle prouve ta confiance, responsabilise le client, et est activable uniquement si les conditions sont respectées."),
            ("La garantie ne risque-t-elle pas de me coûter cher ?",
             "Moins de 5% des clients activent la garantie avec un système bien construit. Et quand ils l'activent, c'est une opportunité d'optimisation, pas une perte. Un client récupéré grâce à la garantie est un client qui témoigne."),
            ("Comment communiquer la garantie en appel de vente ?",
             "Après la présentation de l'offre et du ROI. Jamais en ouverture. «&nbsp;Et pour vous retirer tout risque...&nbsp;» — le prospect qui hésite encore signe à ce moment-là dans 70% des cas."),
            ("Faut-il mettre la garantie par écrit dans le contrat ?",
             "Oui. Les conditions de déclenchement, les métriques mesurées, le délai, et les obligations des deux parties doivent être contractualisés. Ça protège l'agence autant que le client."),
            ("Comment le programme Scaling Lab' gère-t-il sa propre garantie ?",
             "La garantie résultat du Scaling Lab' est présentée sur appel après validation du profil candidat — elle n'est pas publiée publiquement. Ce modèle de garantie sélective est enseigné comme une des tactiques de closing du programme."),
        ],
        "related_niches": ["centres-esthetiques", "coaching-consultants", "btp-construction", "dentistes", "therapeutes"],
    },
    # ── 15 nouvelles problématiques ────────────────────────────────────────
    "comment-creer-vsl-agence-ia": {
        "slug":      "comment-creer-vsl-agence-ia",
        "h1":        "Comment créer une VSL qui génère 35-50 appels/mois pour ton agence IA",
        "title_tag": "Comment créer une VSL agence IA | Scaling Lab'",
        "meta_desc": "Guide complet pour créer une VSL qui remplit ton calendrier d'appels — structure, script, distribution. Par Abdé Chan.",
        "hero_lead":  "Une VSL bien construite travaille pour toi 24h/24 — pendant que tu dors, elle qualifie, convainc et déclenche les prises de RDV. C'est le levier d'acquisition le plus scalable qu'une agence IA puisse avoir.",
        "problem":   "Tu n'as pas de VSL — ou tu en as une qui ne convertit pas.",
        "problem_list": [
            "Tu expliques ton offre de vive voix à chaque prospect, ce qui consomme ton énergie sans scalabilité",
            "Ta vidéo d'accroche parle de toi et de ton agence — et non du problème du prospect",
            "Tu n'as pas de structure narrative claire : le prospect ne comprend pas ce qu'il va obtenir de l'appel",
            "Ta VSL est trop longue (> 20 min) ou trop courte (< 4 min) et perd l'attention",
        ],
        "method_title": "La structure VSL en 6 blocs qui convertit",
        "method_steps": [
            ("Bloc 1 : Crochet en 10 secondes", "Verbalise exactement le problème du prospect dans ses mots. «&nbsp;Si tu es [cible] et que tu galères à [problème exact]...&nbsp;» — il doit se sentir vu immédiatement."),
            ("Bloc 2 : Agitation du problème (2 min)", "Montre les conséquences du statu quo : combien ça coûte de ne pas agir. Pas d'hyperboles — des chiffres réels. «&nbsp;80% des leads immobiliers ne reçoivent jamais de suivi après J+2.&nbsp;»"),
            ("Bloc 3 : La solution et son mécanisme (3 min)", "Présente l'infrastructure IA en termes de résultat. Pas «&nbsp;un chatbot GoHighLevel&nbsp;» — «&nbsp;un système qui qualifie et book des RDV pendant que tu travailles.&nbsp;»"),
            ("Bloc 4 : Preuve sociale (2 min)", "1 à 2 cas clients chiffrés. Abdé utilise Louis (58k€/mois), Ryan (30k€ contrat BTP), Sally (18k€/mois). La preuve concrète lève 80% des objections avant l'appel."),
            ("Bloc 5 : CTA avec qualification (30 sec)", "Dis exactement ce qui va se passer lors de l'appel. Présente le formulaire de qualification comme une sélection, pas comme une vente. Le prospect doit avoir l'impression de candidater."),
            ("Bloc 6 : Distribution multicanal", "Héberge sur YouTube (non répertorié), distribue en Meta Ads et via email séquence. La même VSL peut servir de publicité + landing + nurturing."),
        ],
        "yt_fragment":  "la VSL qui génère 35-50 appels",
        "yt_fragment2": "j'ai divisé par 3 mon coût par appel",
        "stat_a": ("35–50", "appels qualifiés/mois avec la bonne VSL"),
        "stat_b": ("49 €", "coût par appel qualifié d'Abdé Chan"),
        "stat_c": ("5–15 min", "durée optimale d'une VSL agence IA"),
        "faqs": [
            ("Quelle est la durée idéale d'une VSL pour une agence IA ?", "5 à 15 minutes. En dessous de 5 min, pas assez de contenu pour qualifier. Au-delà de 20 min, tu perds 80% de l'audience. La VSL d'Abdé est autour de 12 minutes."),
            ("Faut-il apparaître en vidéo ou peut-on faire une VSL en slides ?", "Les deux fonctionnent, mais une VSL face caméra avec toi ou ton founder convertit mieux — elle crée la confiance personnelle. Les slides seules fonctionnent si le copywriting est excellent."),
            ("Comment distribuer sa VSL sans budget pub ?", "Partage organique LinkedIn + emails froids avec lien vidéo + stories Instagram = 0€. Les Ads viennent amplifier ce qui fonctionne déjà organiquement. Ne commence pas par les Ads si ta VSL ne convertit pas à froid."),
            ("Comment mesurer si sa VSL convertit ?", "Taux de complétion (objectif > 40%), taux de clic sur le CTA (objectif > 15%), taux de candidature sur le formulaire (objectif > 60% des cliqueurs). Si l'un de ces chiffres est faible, tu sais quel bloc réviser."),
            ("Peut-on utiliser la même VSL pour plusieurs niches ?", "Non. Une VSL générique ne résonne avec personne. Crée une VSL par niche cible — le crochet et les preuves sociales doivent être 100% spécifiques au secteur."),
        ],
        "related_niches": ["centres-esthetiques", "btp-construction", "solaire", "dentistes", "immobilier"],
    },
    "comment-prospecter-cold-outreach-agence-ia": {
        "slug":      "comment-prospecter-cold-outreach-agence-ia",
        "h1":        "Comment prospecter en cold outreach pour remplir son pipeline agence IA",
        "title_tag": "Comment prospecter en cold outreach agence IA | Scaling Lab'",
        "meta_desc": "Système de cold outreach pour agence IA — email, LinkedIn, séquence en 7 touchpoints. Par Abdé Chan.",
        "hero_lead":  "Le cold outreach est le canal d'acquisition le moins coûteux et le plus contrôlable qu'une agence IA puisse opérer. Mais fait sans système, il ne produit rien.",
        "problem":   "Tu envoies des messages en vrac et tu reçois des refus ou du silence.",
        "problem_list": [
            "Ton premier message commence par «&nbsp;Bonjour, je m'appelle...&nbsp;» — et le prospect ferme immédiatement",
            "Tu n'as pas de séquence multi-touchpoints — un seul message sans relance est ignoré à 90%",
            "Tu cibles trop large — «&nbsp;PME de moins de 50 personnes&nbsp;» n'est pas un ICP",
            "Tu n'as aucune personnalisation — les prospects sentent l'automatisation de masse",
        ],
        "method_title": "La séquence cold outreach en 7 touchpoints",
        "method_steps": [
            ("Définir un ICP ultra-précis", "Pas «&nbsp;restaurants&nbsp;» — «&nbsp;restaurants gastronomiques 40-120 couverts, Paris/Lyon/Bordeaux, actifs sur Instagram avec > 1k abonnés.&nbsp;» La précision × la pertinence = les réponses."),
            ("Le message J1 : pattern interrupt", "Commence par un insight sur leur business, pas sur le tien. «&nbsp;J'ai vu que vous répondez à vos DMs Instagram en moyenne 4h après — 60% de vos leads partent avant ça.&nbsp;» Source : leur propre contenu."),
            ("Relance J3 : valeur pure", "Envoie un mini-audit gratuit ou un exemple concret d'un client similaire. Pas de pitch — de la valeur non sollicitée. Ça prouve la compétence avant même l'appel."),
            ("Touchpoints J7, J10, J14 : variation de canal", "Email → LinkedIn DM → Instagram DM si applicable. Chaque touchpoint ajoute une preuve ou une perspective différente. Pas de relance du type «&nbsp;juste pour m'assurer que vous avez bien reçu...&nbsp;»"),
            ("Le breakup email J21", "«&nbsp;Je vais clore ce sujet de mon côté. Si jamais vous souhaitez explorer comment [résultat spécifique], la porte reste ouverte.&nbsp;» Ce message génère souvent des réponses de prospects qui suivaient sans répondre."),
        ],
        "yt_fragment":  "j'ai divisé par 3 mon coût par appel",
        "yt_fragment2": "la raison pour laquelle t'es bloqué sous 10k",
        "stat_a": ("7", "touchpoints dans la séquence optimale"),
        "stat_b": ("2–4 sem.", "avant le premier appel en cold outreach ciblé"),
        "stat_c": ("0 €", "coût du canal cold email/LinkedIn"),
        "faqs": [
            ("Combien d'emails froids envoyer par jour ?", "30 à 50 emails ultra-ciblés par jour > 500 emails génériques. La qualité de ciblage prime sur le volume — un email à 50 prospects parfaits génère plus de réponses qu'un blast à 500 PME random."),
            ("Quel outil utiliser pour le cold outreach ?", "Lemlist ou Instantly pour l'email (rotation de domaines + warm-up). LinkedIn Sales Navigator pour l'enrichissement. Apollo ou Hunter.io pour les emails. Tout ça intégrable dans GoHighLevel."),
            ("Comment éviter de finir en spam ?", "Warm-up du domaine (minimum 4 semaines), taux d'ouverture > 40% requis, variation des objets, liste propre (< 5% bounce rate). Ne jamais envoyer depuis ton domaine principal."),
            ("Quel taux de réponse est normal en cold outreach ?", "3 à 8% de taux de réponse est correct. 1 à 2% de conversion en appel est réaliste. Sur 200 emails/semaine bien ciblés : 6 à 16 réponses, 2 à 4 appels. En cumulatif sur 4 semaines : 8 à 16 appels."),
            ("Cold email ou LinkedIn en priorité pour une agence IA ?", "Les deux ensemble. LinkedIn pour les secteurs B2B (consultants, avocats, comptables). Email pour les secteurs locaux (dentistes, centres esthétiques, BTP). La combinaison des deux double le taux de réponse."),
        ],
        "related_niches": ["experts-comptables", "avocats", "coaching-consultants", "immobilier", "solaire"],
    },
    "comment-upsell-clients-agence-ia": {
        "slug":      "comment-upsell-clients-agence-ia",
        "h1":        "Comment upseller ses clients et passer de 3k€ à 7k€+ par client",
        "title_tag": "Comment upsell ses clients agence IA | Scaling Lab'",
        "meta_desc": "Stratégie pour doubler le ticket moyen de chaque client en agence IA — moment, argument, structure de l'upsell. Par Abdé Chan.",
        "hero_lead":  "Le client existant est ton meilleur prospect. Il a déjà payé, il te fait déjà confiance. Un upsell bien construit double ton chiffre d'affaires sans ajouter un seul nouveau client.",
        "problem":   "Tu restes à 1 500-2 500 €/client alors que tu pourrais facturer 5 000-8 000 € au même client.",
        "problem_list": [
            "Tu ne proposes jamais de service supplémentaire parce que tu as peur de perturber la relation",
            "Tu upselles trop tôt — avant que le premier résultat soit livré",
            "Ton upsell n'est pas logique — il n'est pas dans la continuité directe du service initial",
            "Tu proposes un upsell sans lier au ROI déjà généré pour le client",
        ],
        "method_title": "Le framework upsell en 3 temps",
        "method_steps": [
            ("Moment 1 : Après le premier résultat significatif", "Attends que le client ait vu ses premiers vrais résultats (leads générés, appels bookés, CA supplémentaire). Le bon moment : entre J+30 et J+60. Trop tôt = méfiance. Trop tard = inertie."),
            ("L'argument : continuité logique", "Ne vends pas un service supplémentaire — vends la prochaine étape naturelle. «&nbsp;Maintenant que ton système de génération de RDV tourne, les leads entrants ont besoin d'être relancés automatiquement. C'est le module suivant.&nbsp;»"),
            ("La structure : ROI d'abord", "Commence par rappeler ce que tu as déjà généré : «&nbsp;En 45 jours, on t'a généré 18 RDV qualifiés pour 1 200 €/mois. L'étape suivante permettrait d'augmenter ton taux de closing de 30% — ça représente X€ de CA supplémentaire.&nbsp;» Présente le prix en dernier."),
        ],
        "yt_fragment":  "tu expliques à ton élève comment transformer un client à 3k€ en client à 7k€",
        "yt_fragment2": "Comment j'ai réduit mon taux de churn par 2",
        "stat_a": ("×2,3", "ticket moyen après upsell selon la méthode"),
        "stat_b": ("50%+", "des clients satisfaits acceptent un upsell logique"),
        "stat_c": ("30–60j", "délai optimal avant le premier upsell"),
        "faqs": [
            ("Quoi upseller en premier à un client agence IA ?", "Le service complémentaire le plus logique. Si tu as installé la génération de leads (Ads + chatbot), l'upsell naturel est la gestion des relances et du nurturing. Si tu as commencé par le chatbot, l'upsell est les Ads pour alimenter le chatbot."),
            ("Comment chiffrer la valeur de l'upsell pour le client ?", "Identifie une métrique que le service supplémentaire va améliorer (taux de conversion, valeur panier, taux de rétention) et calcule l'impact financier. Le client perçoit immédiatement le ROI de l'investissement."),
            ("Peut-on upseller un client qui se plaint ?", "Non. Résous d'abord le problème actuel, livre le résultat promis. Un upsell sur un client insatisfait accélère le churn. Attends toujours que la satisfaction soit revenue avant de proposer autre chose."),
            ("À quelle fréquence peut-on upseller ?", "1 upsell par trimestre maximum pour un même client. Trop fréquent = impression d'être vendu à tout le temps. L'espace entre les upsells permet au client de voir les résultats de chaque service avant d'en ajouter un."),
            ("Comment présenter l'upsell sans paraître cupide ?", "Présente-le comme une recommandation basée sur les données. «&nbsp;En regardant tes chiffres de ce mois, j'ai identifié une opportunité que tu laisses sur la table — voilà ce qu'on peut faire.&nbsp;» Tu es consultant, pas vendeur."),
        ],
        "related_niches": ["centres-esthetiques", "dentistes", "coaching-consultants", "e-commerce", "immobilier"],
    },
    "comment-passer-smma-agence-ia": {
        "slug":      "comment-passer-smma-agence-ia",
        "h1":        "Comment passer de SMMA à agence IA sans perdre ses revenus",
        "title_tag": "Comment passer de SMMA à agence IA | Scaling Lab'",
        "meta_desc": "La méthode pour transitionner de SMMA vers l'agence IA — sans couper ses revenus ni perdre ses clients. Par Abdé Chan.",
        "hero_lead":  "Des milliers d'agences SMMA stagnent à 2 000-5 000 €/mois sur des clients épuisants. La transition vers l'IA permet de multiplier le ticket par 3-5 avec les mêmes clients.",
        "problem":   "Tu gères 10-20 clients à 500 €/mois, tu travailles 60h/semaine, et les marges fondent.",
        "problem_list": [
            "Tu vends du temps (gestion de réseaux, contenu) et non des résultats — impossible de justifier plus de 1 000 €/mois",
            "Tu as peur de perdre tes clients actuels en changeant d'offre",
            "Tu ne sais pas comment passer d'une offre de service à une offre d'infrastructure",
            "Tu penses que tes clients SMMA n'ont pas le budget pour une infrastructure IA — faux",
        ],
        "method_title": "La transition SMMA → agence IA en 3 phases",
        "method_steps": [
            ("Phase 1 : Identifier les 2-3 meilleurs clients", "Parmi tes clients actuels, lesquels sont dans une niche avec un vrai pain point IA (leads perdus, no-shows, abandon panier) ? Ce sont tes premiers clients pilotes pour l'offre IA."),
            ("Phase 2 : Proposer l'upgrade sur un client existant", "«&nbsp;Je suis en train de développer un nouveau service pour les [niche]. Je cherche 1-2 clients pilotes pour tester ça à tarif préférentiel. Intéressé ?&nbsp;» Le client te connaît déjà — le closing est 5x plus facile."),
            ("Phase 3 : Documenter les résultats et pivoter l'offre", "Le cas client pilote devient ta preuve sociale. Tu peux alors upgrader les autres clients et acquérir de nouveaux clients avec le même argument. L'ancien MRR SMMA est conservé pendant la transition."),
        ],
        "yt_fragment":  "ton élève comprend comment faire la transition de SMMA vers Agence IA",
        "yt_fragment2": "30 Milles balles en vendant une infrastructure de croissance",
        "stat_a": ("×3,8", "revenus médians des élèves en 6 mois"),
        "stat_b": ("2 000 → 8 000 €", "ticket SMMA → agence IA (Arnaud)"),
        "stat_c": ("1 client", "pilote suffit pour valider la transition"),
        "faqs": [
            ("Faut-il garder ses clients SMMA pendant la transition ?", "Oui, au minimum les 2-3 meilleurs. Ils servent de revenus de transition ET de premiers clients IA. Tu ne coupes pas les ponts — tu construis la nouvelle offre dessus."),
            ("Comment expliquer la transition à ses clients actuels ?", "Tu ne 'changes' pas d'offre — tu 'évolues' ton service. «&nbsp;Je déploie maintenant des infrastructures IA en complément de la gestion de réseaux — les clients qui testent voient 30-50% de leads en plus.&nbsp;»"),
            ("Faut-il garder les services SMMA en parallèle ?", "6 mois maximum. Passé ce délai, les services SMMA bas de gamme épuisent sans rentabilité. L'objectif est que l'agence IA génère plus que le SMMA dans les 6 premiers mois."),
            ("Quel est le bon moment pour faire la transition ?", "Dès que possible. Arnaud l'a fait après 7 ans de SMMA épuisant à 2k€/mois — il est passé à 8k€+ en quelques mois avec moins de clients. Plus tu attends, plus tu laisses de l'argent sur la table."),
            ("Peut-on faire la transition seul sans coaching ?", "Techniquement oui. En pratique, la majorité des SMMA qui tentent la transition seuls se retrouvent avec un mix incohérent des deux offres et ne closent ni l'un ni l'autre. Un accompagnement accélère de 6-12 mois le process."),
        ],
        "related_niches": ["centres-esthetiques", "btp-construction", "restaurants", "salons-coiffure", "garages-auto"],
    },
    "comment-utiliser-gohighlevel-agence-ia": {
        "slug":      "comment-utiliser-gohighlevel-agence-ia",
        "h1":        "Comment utiliser GoHighLevel pour lancer et scaler son agence IA",
        "title_tag": "Comment utiliser GoHighLevel agence IA | Scaling Lab'",
        "meta_desc": "GoHighLevel pour agence IA — setup, snapshots, automatisations, reporting client. Guide pratique par Abdé Chan.",
        "hero_lead":  "GoHighLevel est le seul outil dont tu as besoin pour livrer une infrastructure IA complète à un client — sans coder. Mais sa puissance ne s'improvise pas.",
        "problem":   "Tu as un compte GoHighLevel mais tu n'en utilises que 10% et tu livres tout manuellement.",
        "problem_list": [
            "Tu ne sais pas quelles automatisations activer en premier pour chaque niche",
            "Tu n'as pas de snapshot réutilisable — tu reconfigures tout à zéro pour chaque nouveau client",
            "Tu n'utilises pas les fonctionnalités IA natives (bot de qualification, voice AI)",
            "Tes clients ne voient pas leurs résultats — pas de dashboard, pas de rapport auto",
        ],
        "method_title": "Le setup GoHighLevel en 4 couches",
        "method_steps": [
            ("Couche 1 : Acquisition", "Formulaires + landing pages dans GHL. Intégration Meta Ads / Google Ads. Webhooks pour capturer les leads entrants depuis tous les canaux. Délai de mise en place : 4-6 heures par client."),
            ("Couche 2 : Qualification IA", "Chatbot de qualification dans le chat widget ou les SMS. Le bot pose 4-6 questions, score le lead, et le route vers un calendrier ou une séquence de nurturing selon le score."),
            ("Couche 3 : Nurturing automatisé", "Séquence email + SMS multi-touchpoints. Le prospect qui n'est pas prêt entre dans un nurturing de 30-60 jours. Il est relancé automatiquement jusqu'à ce qu'il soit prêt à booker."),
            ("Couche 4 : Dashboard client", "Tableau de bord en accès lecture pour le client. Il voit en temps réel : leads générés, taux de qualification, appels bookés, CA en cours. Rapport mensuel automatique le 1er de chaque mois."),
        ],
        "yt_fragment":  "30 Milles balles en vendant une infrastructure de croissance",
        "yt_fragment2": "Comment Dylan est passé de 2,5k/mois à 17k/mois",
        "stat_a": ("4–6h", "pour déployer un client avec un snapshot"),
        "stat_b": ("86%", "marges avec le stack GHL"),
        "stat_c": ("3 personnes", "agence d'Abdé à 350k€/an sur GHL"),
        "faqs": [
            ("GoHighLevel est-il difficile à apprendre ?", "La courbe d'apprentissage est de 3 à 6 semaines pour maîtriser les fonctionnalités essentielles. Abdé enseigne le setup dans le programme — du onboarding client à la livraison complète en moins de 2 semaines."),
            ("GoHighLevel remplace-t-il tous les autres outils ?", "Pour 90% des besoins d'une agence IA : oui. CRM, landing pages, email marketing, SMS, chatbot, calendrier, reporting. L'intégration avec Make/n8n pour les automatisations complexes couvre le reste."),
            ("Combien coûte GoHighLevel ?", "97$/mois (plan Starter) ou 297$/mois (plan Agency Unlimited). En agence, tu peux héberger des dizaines de clients sur un seul compte Agency Unlimited — le ROI est immédiat dès le 2e client."),
            ("Faut-il créer un snapshot par niche ?", "Oui. Un snapshot centres esthétiques, un snapshot BTP, un snapshot immobilier... Chaque snapshot contient les automatisations, templates d'emails et pipelines pré-configurés pour la niche. Déploiement en 4-6h au lieu de 30-40h custom."),
            ("GoHighLevel peut-il gérer les intégrations Meta Ads ?", "Oui. Intégration native Meta Ads pour capturer les leads Facebook/Instagram directement dans le CRM. Workflows automatiques déclenchés à la réception de chaque lead. Taux de contact en moins de 5 minutes."),
        ],
        "related_niches": ["centres-esthetiques", "btp-construction", "immobilier", "dentistes", "restaurants"],
    },
    "comment-decrocher-premier-client-agence-ia": {
        "slug":      "comment-decrocher-premier-client-agence-ia",
        "h1":        "Comment décrocher son premier client en agence IA — de zéro à premier contrat",
        "title_tag": "Comment décrocher son premier client agence IA | Scaling Lab'",
        "meta_desc": "La méthode pour signer son premier client en agence IA — positionnement, approche, offre pilote. Par Abdé Chan.",
        "hero_lead":  "Le premier client est le plus difficile et le plus important. Il t'apprend plus en 30 jours que 6 mois de formation — et il devient ta première preuve sociale.",
        "problem":   "Tu as une offre, tu as les outils, mais ton premier vrai client tarde à arriver.",
        "problem_list": [
            "Tu attends d'avoir «&nbsp;tout parfait&nbsp;» avant de prospecter — la perfection est une procrastination déguisée",
            "Tu n'as pas de preuve sociale, donc tu proposes des prix trop bas qui disqualifient ta crédibilité",
            "Tu cibles les mauvaises personnes (inconnus sur LinkedIn) au lieu de commencer par ton réseau proche",
            "Tu n'as pas de landing page ni de page de réservation — les prospects intéressés ne savent pas comment aller plus loin",
        ],
        "method_title": "La stratégie premier client en 4 étapes",
        "method_steps": [
            ("Étape 1 : Liste de 20 contacts chauds", "Qui autour de toi connaît des business locaux ? Famille, amis, anciens collègues, réseaux pro. 20 contacts chaleureux bien briefés valent mieux que 500 cold emails. L'objectif : une introduction, pas une vente."),
            ("Étape 2 : L'offre pilote stratégique", "Propose un premier client à tarif réduit (50-70% du tarif normal) contre témoignage vidéo et droit d'utiliser les résultats en commercial. Ce n'est pas «&nbsp;travailler gratis&nbsp;» — c'est acheter une preuve sociale."),
            ("Étape 3 : L'audit gratuit pour ouvrir la porte", "Offre un audit de 30 minutes qui montre au prospect combien de leads il perd chaque mois. 3 chiffres concrets suffisent. L'audit positionne ton expertise avant même l'offre."),
            ("Étape 4 : Livrer + documenter", "Livre le premier client avec soin. Documente chaque étape : screenshots, métriques, témoignage. Ce premier case study devient l'argument de closing de tes 50 prochains prospects."),
        ],
        "yt_fragment":  "De 0 à 27'000€ /mois avec l'IA (mon histoire)",
        "yt_fragment2": "la raison pour laquelle t'es bloqué sous 10k",
        "stat_a": ("39 jours", "record pour le premier client dans le programme"),
        "stat_b": ("100 jours", "délai moyen avant premier système complet"),
        "stat_c": ("1 cas client", "suffit pour closer les 10 suivants"),
        "faqs": [
            ("Doit-on avoir une landing page avant de chercher son premier client ?", "Non. Une page Notion ou un simple PDF d'offre suffisent pour les premières approches. La landing page vient quand tu as un premier témoignage à y mettre."),
            ("Quel tarif pour le premier client ?", "1 500 à 2 500 € de setup contre témoignage vidéo et droit de réutiliser les résultats. Jamais gratuit — un client qui ne paie pas ne s'engage pas."),
            ("Et si le premier client ne donne pas de résultats ?", "Ça fait partie du processus d'apprentissage. Dans le programme, Abdé accompagne chaque élève pour diagnostiquer et corriger rapidement. Le premier client est souvent imparfait — c'est normal et attendu."),
            ("Doit-on avoir tout appris avant de chercher son premier client ?", "Non. Tu apprends 10x plus vite avec un vrai client que dans n'importe quel cours. La règle d'Abdé : commence à prospecter dès que tu sais livrer les bases. Le reste s'apprend en faisant."),
            ("Comment trouver son premier client sans réseau ?", "LinkedIn + cold email sur une niche ultra-précise dans ta ville. Propose l'audit gratuit comme premier contact. Dans une petite ville, 30 emails ciblés génèrent souvent 3-5 audits dans la première semaine."),
        ],
        "related_niches": ["centres-esthetiques", "btp-construction", "restaurants", "garages-auto", "salons-coiffure"],
    },
    "comment-construire-credibilite-agence-ia": {
        "slug":      "comment-construire-credibilite-agence-ia",
        "h1":        "Comment construire sa crédibilité en agence IA sans expérience au départ",
        "title_tag": "Comment construire sa crédibilité agence IA | Scaling Lab'",
        "meta_desc": "Stratégie pour construire une crédibilité d'agence IA rapidement — preuves sociales, contenu, portfolio. Par Abdé Chan.",
        "hero_lead":  "La crédibilité ne vient pas des années d'expérience — elle vient des preuves. Et les preuves, ça se construit dès le premier client.",
        "problem":   "Tu n'as pas de cas clients, et les prospects te demandent des références que tu n'as pas encore.",
        "problem_list": [
            "Tu n'as aucun témoignage client — tu es pris dans le paradoxe «&nbsp;pas de client sans preuve, pas de preuve sans client&nbsp;»",
            "Ton profil LinkedIn ne reflète pas ton expertise — aucun contenu, aucune réalisation visible",
            "Tu te présentes comme «&nbsp;agence IA&nbsp;» sans spécialisation claire — pas crédible",
            "Tu n'utilises pas les résultats du programme ou les preuves des autres élèves comme références de méthode",
        ],
        "method_title": "Les 4 piliers de crédibilité",
        "method_steps": [
            ("Pilier 1 : Le cas client pilote", "Un premier client même à tarif réduit avec résultats documentés (screenshots GHL, métriques, témoignage vidéo). Une seule preuve concrète vaut mieux que 10 certifications."),
            ("Pilier 2 : Le contenu de niche ciblé", "2 posts LinkedIn/semaine qui montrent ton process ou tes résultats. Pas de personal branding générique — du contenu spécifique à ta niche cible. Les prospects de la niche te trouvent et te suivent organiquement."),
            ("Pilier 3 : L'audit gratuit comme démonstration", "Un audit de 20-30 minutes qui révèle 3 chiffres concrets sur la perte de revenus du prospect. Tu prouves ton expertise avant même d'être payé."),
            ("Pilier 4 : L'association à une méthode reconnue", "Dans le programme Scaling Lab', les élèves peuvent se présenter comme «&nbsp;formé par Abdé Chan&nbsp;» et utiliser les résultats collectifs (723k$ générés, 115+ agences, ×3.8 de revenus) comme contexte de méthode."),
        ],
        "yt_fragment":  "De 0 à 27'000€ /mois avec l'IA (mon histoire)",
        "yt_fragment2": "30 Milles balles en vendant une infrastructure de croissance",
        "stat_a": ("1 cas client", "suffit pour fermer les 10 suivants"),
        "stat_b": ("723k$", "générés par l'agence d'Abdé (preuve de méthode)"),
        "stat_c": ("115+", "agences accompagnées dans le programme"),
        "faqs": [
            ("Comment convaincre sans témoignage client ?", "Utilise les résultats des élèves du programme (avec accord) + les données sectorielles (% de leads perdus, coûts des no-shows) + ton propre audit gratuit. La combinaison des trois suffit pour convaincre les premiers clients."),
            ("Faut-il créer une page web professionnelle avant de prospecter ?", "Une landing page simple avec l'offre, 1-2 cas clients ou témoignages de méthode, et un lien de réservation. Elle n'a pas besoin d'être parfaite — elle doit juste exister pour crédibiliser les approches cold."),
            ("La crédibilité sur LinkedIn est-elle importante pour vendre à des clients locaux ?", "Modérément. Pour les business locaux (dentistes, artisans), la recommandation et l'approche directe priment. LinkedIn est utile pour les cibles B2B (consultants, avocats, experts-comptables)."),
            ("Comment utiliser les résultats d'autres élèves du programme ?", "En contexte de méthode, pas en les présentant comme tes propres résultats. «&nbsp;La méthode que j'utilise a généré X pour des agences similaires à la vôtre...&nbsp;» C'est honnête et convaincant."),
            ("Combien de temps pour construire une crédibilité suffisante ?", "4 à 8 semaines avec un premier client pilote documenté + 8 posts LinkedIn ciblés + 1 témoignage vidéo. À partir de là, le second client est 3x plus facile à closer que le premier."),
        ],
        "related_niches": ["coaching-consultants", "experts-comptables", "avocats", "immobilier", "solaire"],
    },
    "comment-gerer-objection-prix-agence-ia": {
        "slug":      "comment-gerer-objection-prix-agence-ia",
        "h1":        "Comment gérer l'objection prix et ne plus baisser ses tarifs",
        "title_tag": "Comment gérer l'objection prix agence IA | Scaling Lab'",
        "meta_desc": "Les techniques pour répondre à 'c'est trop cher' sans baisser son prix — 7 leviers psychologiques. Par Abdé Chan.",
        "hero_lead":  "L'objection prix n'est presque jamais une question d'argent. C'est une question de valeur perçue. Et la valeur perçue, tu peux la construire pendant l'appel.",
        "problem":   "Tu entends «&nbsp;c'est trop cher&nbsp;» et tu baisses ton prix ou tu perds le deal.",
        "problem_list": [
            "Tu annonces ton prix avant d'avoir quantifié la valeur — l'ordre est inversé",
            "Tu te défends au lieu de comprendre — «&nbsp;c'est cher&nbsp;» n'est pas une question de budget, c'est un signal de manque de confiance ou de valeur",
            "Tu n'as pas calculé ensemble le coût du statu quo — le prospect ne voit pas ce qu'il perd en ne faisant rien",
            "Tu interprètes l'objection comme un refus définitif — c'est souvent une invitation à mieux expliquer",
        ],
        "method_title": "Les 5 techniques pour gérer l'objection prix",
        "method_steps": [
            ("1. Isoler l'objection", "«&nbsp;Si le prix n'était pas un problème, est-ce que vous seriez prêt à aller de l'avant ?&nbsp;» Si oui : tu travailles sur le prix. Si non : il y a une autre objection cachée — trouve-la d'abord."),
            ("2. Quantifier le coût du statu quo", "«&nbsp;En gardant votre système actuel encore 6 mois, combien de leads non relancés représentent pour vous ?&nbsp;» Force le prospect à chiffrer lui-même ce qu'il perd. Le prix devient soudain relatif."),
            ("3. Comparer à la bonne référence", "Comparer 5 000 € au salaire d'un commercial (25-35k€/an) ou au coût d'une agence traditionnelle (15-30k€/an). La référence change complètement la perception."),
            ("4. Décomposer en mensuel", "5 000 € de setup + 1 500 €/mois = 6 500 € le premier mois, 1 500 €/mois ensuite. Présenté ainsi, ça représente moins qu'un poste marketing à temps partiel."),
            ("5. Le test de valeur inversé", "«&nbsp;Si ce système vous génère 8 RDV qualifiés/mois supplémentaires à votre taux de closing actuel, combien ça représente pour vous ?&nbsp;» Le prospect calcule lui-même pourquoi c'est une bonne affaire."),
        ],
        "yt_fragment":  "comment je vends (sans effort) avec la dark psychology",
        "yt_fragment2": "51 min pour closer TOUS tes appels",
        "stat_a": ("70%", "des objections prix résolues avec ces techniques"),
        "stat_b": ("5 000 €", "ticket moyen dans le programme après maîtrise"),
        "stat_c": ("vs 25k€/an", "coût d'un commercial = mise en perspective"),
        "faqs": [
            ("Doit-on jamais baisser son prix ?", "Jamais en réponse à une objection directe — c'est une capitulation qui détruit ta crédibilité. Si tu dois ajuster, propose une offre différente (moins de services) pour un prix inférieur, pas un discount gratuit."),
            ("Comment répondre à 'je dois y réfléchir' ?", "'Je comprends. Qu'est-ce qui vous ferait hésiter encore ?' puis silence. 'Je dois y réfléchir' est toujours soit un manque de confiance, soit une autre objection cachée, soit un besoin de validation externe."),
            ("Peut-on proposer des facilités de paiement ?", "Oui, et ça peut débloquer des deals. 3x sans frais ou setup divisé en 2 versements. Attention : le total ne doit pas changer — on facilite le financement, on ne réduit pas le prix."),
            ("Comment éviter l'objection prix avant qu'elle arrive ?", "En quantifiant la valeur tout au long de l'appel de vente, bien avant d'annoncer le prix. Quand le ROI est évident, le prix suit naturellement."),
            ("L'objection prix est-elle différente selon la niche ?", "Oui. Les artisans BTP ont une culture du devis compétitif — l'objection est fréquente. Les dentistes et avocats comprennent mieux la valeur ajoutée — l'objection est moins fréquente. Adapte ta mise en contexte selon la niche."),
        ],
        "related_niches": ["btp-construction", "solaire", "plombiers-electriciens", "garages-auto", "restaurants"],
    },
    "comment-creer-contenu-b2b-agence-ia": {
        "slug":      "comment-creer-contenu-b2b-agence-ia",
        "h1":        "Comment créer du contenu B2B qui génère des inbounds pour ton agence IA",
        "title_tag": "Comment créer du contenu B2B agence IA | Scaling Lab'",
        "meta_desc": "Stratégie de contenu B2B pour agence IA — formats, fréquence, plateformes. Par Abdé Chan.",
        "hero_lead":  "Le bon contenu B2B attire des prospects qui te connaissent déjà avant même de te parler. Ces inbounds sont 3x plus faciles à closer que les cold leads.",
        "problem":   "Tu ne publies pas de contenu ou tu publies du personal branding générique qui ne parle pas à tes prospects.",
        "problem_list": [
            "Tu parles de toi et de ton quotidien, pas des problèmes de tes clients cibles",
            "Tu publies de manière irrégulière — 3 posts en 2 semaines, puis silence pendant 3 semaines",
            "Tu n'as pas de format récurrent qui t'identifie — chaque post est différent, sans fil directeur",
            "Tu mesures les likes, pas les leads — les likes ne paient pas tes factures",
        ],
        "method_title": "Le système de contenu B2B en 3 piliers",
        "method_steps": [
            ("Pilier 1 : Le contenu éducatif niche", "1 post par semaine qui révèle un insight spécifique à ta niche cible. «&nbsp;Pourquoi 70% des centres esthétiques perdent leurs leads le week-end.&nbsp;» Tes prospects de la niche partagent, commentent, et te contactent."),
            ("Pilier 2 : Le contenu preuve sociale", "1 post tous les 15 jours avec un résultat client ou un avant/après chiffré. Pas de texte générique — des captures d'écran, des métriques, des témoignages verbatim."),
            ("Pilier 3 : Le contenu d'autorité", "1 vidéo courte par mois qui démonte un mythe ou révèle une contre-intuition dans ton secteur. Ce format génère des partages hors réseau et te positionne en expert sectoriel."),
        ],
        "yt_fragment":  "j'ai divisé par 3 mon coût par appel",
        "yt_fragment2": "la raison pour laquelle t'es bloqué sous 10k",
        "stat_a": ("×3", "facilité de closing sur les inbounds vs cold"),
        "stat_b": ("2 posts/sem.", "minimum pour un flux d'inbounds régulier"),
        "stat_c": ("3–6 mois", "délai avant les premiers inbounds réguliers"),
        "faqs": [
            ("Quelle plateforme prioriser pour son contenu B2B agence IA ?", "LinkedIn pour les niches B2B (consultants, comptables, avocats). Instagram/TikTok pour les niches B2C locales (dentistes, esthétique, restaurants). YouTube pour le contenu longue durée et la VSL."),
            ("Combien de temps par semaine pour créer du contenu ?", "2 à 3 heures par semaine suffisent pour 2-3 posts LinkedIn + 1 reel court. Batch tes contenus le lundi (plan + script) et le jeudi (tournage + publication). Ne publie pas à la volée."),
            ("Peut-on sous-traiter la création de contenu ?", "Oui, après avoir créé tes 20 premiers posts toi-même. Tu dois d'abord comprendre ce qui résonne avec ton audience avant de déléguer. Un ghostwriter sans ligne directrice produit du contenu générique qui ne convertit pas."),
            ("Comment mesurer l'impact du contenu sur son pipeline ?", "Demande systématiquement à chaque nouveau prospect comment il t'a découvert. Suit le nombre d'inbounds par mois. Objectif : 20-30% des leads viennent du contenu au bout de 6 mois de publication régulière."),
            ("Le contenu peut-il remplacer la prospection active ?", "Pas avant d'avoir 6-12 mois d'historique de publication. Le contenu est un canal de renforcement, pas un canal de démarrage. Commence par l'outreach + Ads, et construis le contenu en parallèle pour le long terme."),
        ],
        "related_niches": ["coaching-consultants", "experts-comptables", "avocats", "solaire", "immobilier"],
    },
    "comment-piloter-kpis-agence-ia": {
        "slug":      "comment-piloter-kpis-agence-ia",
        "h1":        "Comment piloter ses KPIs et scaler son agence IA par les données",
        "title_tag": "Comment piloter ses KPIs agence IA | Scaling Lab'",
        "meta_desc": "Les 8 métriques clés à suivre pour piloter une agence IA vers 30k€/mois. Par Abdé Chan.",
        "hero_lead":  "Les agences qui scalent regardent leurs chiffres tous les jours. Les agences qui stagnent travaillent à l'instinct. Les données ne mentent pas.",
        "problem":   "Tu travailles beaucoup mais tu ne sais pas précisément ce qui fonctionne ou ne fonctionne pas.",
        "problem_list": [
            "Tu pilotes ton agence au ressenti — tu n'as pas de dashboard avec des métriques clés",
            "Tu te focalises sur le CA sans regarder les marges — une agence à 10k€ de CA et 2k€ de marge n'est pas une agence viable",
            "Tu ne connais pas ton coût d'acquisition client (CAC) ni ta valeur vie client (LTV)",
            "Tu ne sais pas quelle activité génère le plus de revenus — donc tu ne sais pas où mettre ton énergie",
        ],
        "method_title": "Les 8 KPIs à suivre chaque semaine",
        "method_steps": [
            ("Acquisition : Leads, CPL, Appels", "Leads entrants cette semaine / Coût par lead (CPL) / Appels bookés. Objectifs : CPL < 30€ en cold outreach, < 60€ en Ads. Taux de booking > 40% des leads."),
            ("Vente : Taux de closing, Ticket moyen", "Appels passés / Contrats signés = taux de closing (objectif : > 30%). Ticket moyen setup + LTV retainer. Un taux bas = problème de qualification. Un ticket bas = problème de positionnement."),
            ("Livraison : Marges, Temps/client, NPS", "Marge nette par client = CA - coût outils - temps × tarif horaire fictif. Temps moyen par client par semaine. Score NPS mensuel. Si les marges baissent : tu sur-livres ou tu sous-factures."),
            ("Rétention : Churn rate, LTV, MRR", "Clients perdus / Clients totaux = churn. MRR (Monthly Recurring Revenue). LTV = ticket moyen × durée de vie client. Objectif : churn < 5%/mois, LTV > 6 000 €."),
        ],
        "yt_fragment":  "Pourquoi abandonner ton agence IA à 10k/mois",
        "yt_fragment2": "Comment j'ai réduit mon taux de churn par 2",
        "stat_a": ("8 KPIs", "à suivre chaque semaine"),
        "stat_b": ("< 5%", "taux de churn mensuel cible"),
        "stat_c": ("LTV > 6k€", "objectif par client"),
        "faqs": [
            ("Quel outil utiliser pour piloter ses KPIs ?", "Un tableau Notion ou Google Sheets suffit au départ. Le CRM GoHighLevel intègre les métriques d'acquisition et de pipeline. Pour les métriques de livraison et marges, un tableur simple mis à jour chaque lundi est suffisant."),
            ("À quelle fréquence réviser ses KPIs ?", "Métriques d'acquisition : chaque semaine. Métriques de vente : après chaque appel. Métriques de livraison et rétention : une fois par mois. Ne te perds pas dans les données quotidiennes — hebdomadaire est le bon rythme."),
            ("Quel est le KPI le plus important pour une agence IA en démarrage ?", "Le nombre d'appels de vente qualifiés par semaine. C'est le seul indicateur qui prédit directement les revenus à 30 jours. Tout le reste (contenu, outils, formation) est secondaire si ce chiffre est à zéro."),
            ("Comment interpréter un taux de closing bas ?", "3 causes possibles : qualification trop laxiste (tu parles à des non-qualifiés), offre pas adaptée au prospect, ou script de vente défaillant. Commence par écouter tes enregistrements d'appels pour diagnostiquer."),
            ("Faut-il partager ses KPIs avec ses clients ?", "Oui, les KPIs qui les concernent. Tableau de bord en lecture seule avec leur nombre de leads, taux de qualification, et RDV bookés. Les clients qui voient leurs résultats en temps réel ne partent pas."),
        ],
        "related_niches": ["centres-esthetiques", "btp-construction", "e-commerce", "solaire", "coaching-consultants"],
    },
    "comment-automatiser-prospection-agence-ia": {
        "slug":      "comment-automatiser-prospection-agence-ia",
        "h1":        "Comment automatiser sa prospection pour générer des leads en pilote automatique",
        "title_tag": "Comment automatiser sa prospection agence IA | Scaling Lab'",
        "meta_desc": "Automatiser sa prospection en agence IA — outils, séquences, enrichissement. Par Abdé Chan.",
        "hero_lead":  "La prospection manuelle est la première chose à automatiser dans une agence IA. Un système bien construit génère des appels pendant que tu livres tes clients actuels.",
        "problem":   "Tu prospectes manuellement ou tu ne prospectes pas — les deux détruisent ta croissance.",
        "problem_list": [
            "Tu passes 3-4 heures par jour à chercher des contacts et envoyer des messages manuellement",
            "Ta prospection s'arrête quand tu as des clients à gérer — le pipeline se vide",
            "Tu n'as pas de système de qualification automatique — tu passes du temps avec des prospects non ciblés",
            "Tu n'utilises pas les outils IA pour personnaliser à grande échelle",
        ],
        "method_title": "Le système de prospection automatisé",
        "method_steps": [
            ("Étape 1 : Base de données enrichie automatiquement", "Apollo.io ou Findymail + Sales Navigator pour scraper des listes de prospects ultra-ciblés. 500 prospects enrichis (email + LinkedIn + téléphone) en 2 heures. Re-enrichissement automatique chaque semaine."),
            ("Étape 2 : Séquence email automatisée", "Lemlist ou Instantly pour envoyer des séquences personnalisées à l'IA. La personnalisation IA (ligne d'ouverture basée sur le profil LinkedIn) double le taux de réponse vs template générique."),
            ("Étape 3 : Qualification automatique dans GHL", "Les réponses positives déclenchent un workflow GHL : email de booking + rappel SMS + qualification bot. Le prospect est guidé vers ton calendrier sans intervention manuelle."),
            ("Étape 4 : Reporting automatique hebdomadaire", "Dashboard Make/n8n qui compile chaque lundi : emails envoyés, taux d'ouverture, taux de réponse, appels bookés. Tu sais exactement ce qui fonctionne sans manipulation manuelle des données."),
        ],
        "yt_fragment":  "j'ai divisé par 3 mon coût par appel",
        "yt_fragment2": "en 23s tu lui expliques comment éviter le piège des automati",
        "stat_a": ("2h", "pour créer une base de 500 prospects enrichis"),
        "stat_b": ("×2", "taux de réponse avec personnalisation IA"),
        "stat_c": ("0 min/jour", "une fois le système lancé"),
        "faqs": [
            ("Quels outils pour automatiser sa prospection ?", "Stack recommandé : Apollo.io (enrichissement) + Lemlist (séquences email) + LinkedIn Sales Navigator (ciblage) + GoHighLevel (qualification + booking). Budget total : 150-250 €/mois."),
            ("L'automatisation remplace-t-elle la personnalisation ?", "Non — elle la rend scalable. Les outils IA génèrent des lignes d'ouverture personnalisées basées sur le profil LinkedIn du prospect. Le résultat : des emails qui semblent écrits main à la main mais envoyés à 100 prospects/jour."),
            ("La prospection automatisée fonctionne-t-elle pour les business locaux ?", "Oui, avec les bons outils de scraping local (Google Maps, Pages Jaunes scrapers). Tu cibles les dentistes de Paris, les artisans BTP de Lyon, les centres esthétiques de Bordeaux — avec des emails personnalisés selon leur fiche Google."),
            ("Faut-il chauffer ses domaines avant d'automatiser ?", "Obligatoire. 3 à 4 semaines de warm-up avec Mailwarm ou Warmbox avant d'envoyer le premier email de prospection. Sans warm-up, tes emails finissent en spam dès le premier jour."),
            ("Peut-on automatiser le cold calling ?", "Avec les voice AI agents de GoHighLevel, oui. Un agent vocal appelle les prospects qui ont ouvert ton email mais n'ont pas répondu, qualifie en 90 secondes, et book directement dans ton calendrier si qualifié."),
        ],
        "related_niches": ["btp-construction", "restaurants", "plombiers-electriciens", "garages-auto", "salons-coiffure"],
    },
    "comment-creer-landing-page-agence-ia": {
        "slug":      "comment-creer-landing-page-agence-ia",
        "h1":        "Comment créer une landing page qui convertit pour une agence IA",
        "title_tag": "Comment créer une landing page agence IA | Scaling Lab'",
        "meta_desc": "Structure d'une landing page haute conversion pour agence IA — sections, copywriting, CTA. Par Abdé Chan.",
        "hero_lead":  "Ta landing page est ton vendeur le plus efficace — il travaille 24h/24, ne prend pas de vacances, et répond instantanément. Mais seulement si elle est construite dans le bon ordre.",
        "problem":   "Ta landing page parle de ton agence, pas du problème de ton prospect — personne ne lit.",
        "problem_list": [
            "Tu commences par te présenter au lieu de commencer par le problème du prospect",
            "Aucune preuve sociale visible au-dessus de la ligne de flottaison",
            "Un seul CTA vague («&nbsp;Contactez-nous&nbsp;») sans formulaire de qualification",
            "La page est trop longue et trop chargée — le prospect n'arrive pas au CTA",
        ],
        "method_title": "La structure en 7 sections qui convertit",
        "method_steps": [
            ("Section 1 : Hero — le problème en 1 phrase", "H1 = le problème du prospect. Pas ton nom, pas ton offre. «&nbsp;Vos leads dentaires arrivent et disparaissent faute de relance automatique — voici comment stopper l'hémorragie.&nbsp;»"),
            ("Section 2 : Preuve sociale immédiate", "3 chiffres clés ou 1 témoignage client court, immédiatement sous le hero. Le prospect doit voir une preuve avant même de scroller."),
            ("Section 3 : Agitation du problème", "3 bullet points qui décrivent exactement la douleur quotidienne. Chaque bullet = une situation que le prospect vit tous les jours. Il doit se reconnaître."),
            ("Section 4 : La solution et le mécanisme", "L'infrastructure IA expliquée en termes de résultat, pas de technique. Schéma ou animation du système. 3 étapes maximum."),
            ("Section 5 : Résultats détaillés", "1-2 cas clients avec chiffres. Avant/après. Délai. Niche spécifique. La preuve la plus proche du prospect en termes de secteur."),
            ("Section 6 : FAQ", "5-8 questions qui lèvent les objections classiques. Prix, timing, garantie, compétences requises."),
            ("Section 7 : CTA + formulaire de qualification", "Formulaire 4-5 questions. Bouton = «&nbsp;Vérifier mon éligibilité&nbsp;» ou «&nbsp;Réserver mon audit gratuit&nbsp;». Jamais «&nbsp;Envoyer&nbsp;» ou «&nbsp;Soumettre&nbsp;»."),
        ],
        "yt_fragment":  "comment structurer une landing page qui convertit",
        "yt_fragment2": "la VSL qui génère 35-50 appels",
        "stat_a": ("7 sections", "structure optimale d'une LP agence IA"),
        "stat_b": (">40%", "taux de conversion des cliqueurs en candidats"),
        "stat_c": ("H1", "= le problème du prospect, pas ton nom"),
        "faqs": [
            ("Faut-il afficher ses prix sur la landing page ?", "Non pour une agence IA. Le prix se discute sur appel après qualification. Afficher un prix sur la LP filtre les bons prospects et donne un avantage de négociation aux mauvais."),
            ("Quelle longueur pour une landing page agence IA ?", "Pour un service > 2 000 €, une LP longue (1 500-3 000 mots) convertit mieux qu'une LP courte. Le prospect a besoin d'être éduqué et convaincu avant de s'engager sur un appel."),
            ("GHL ou autre outil pour créer sa landing page ?", "GoHighLevel pour les agences qui livrent sur GHL — la cohérence de l'outil renforce la crédibilité. Carrd ou Webflow pour une page autonome plus rapide à créer. Évite WordPress sans page builder — trop lent."),
            ("Comment tester si sa landing page convertit ?", "Mesure : taux de scroll > 60% (la majorité finit la page), taux de clic sur le CTA > 8% des visiteurs, taux de completion du formulaire > 50% des cliqueurs. Si l'un est faible, la section correspondante est le problème."),
            ("La landing page est-elle indispensable dès le début ?", "Pour la prospection directe et les appels référés, non. Pour les Ads et le contenu organique, oui. Ne crée ta LP qu'une fois que tu as validé ton offre oralement avec les 2-3 premiers clients."),
        ],
        "related_niches": ["centres-esthetiques", "dentistes", "solaire", "coaching-consultants", "immobilier"],
    },
    "comment-negocier-contrats-agence-ia": {
        "slug":      "comment-negocier-contrats-agence-ia",
        "h1":        "Comment négocier et structurer ses contrats pour une agence IA",
        "title_tag": "Comment négocier ses contrats agence IA | Scaling Lab'",
        "meta_desc": "Structure contractuelle pour agence IA — clauses essentielles, durée, garantie, conditions de résiliation. Par Abdé Chan.",
        "hero_lead":  "Un bon contrat protège l'agence ET le client. Il cadre les attentes, prévient les litiges, et garantit le MRR sur la durée.",
        "problem":   "Tu travailles sans contrat ou avec un contrat générique qui ne te protège pas.",
        "problem_list": [
            "Pas de clause sur les obligations du client — s'il ne met pas son budget Ads, tu portes la responsabilité des mauvais résultats",
            "Durée de contrat trop courte (1 mois) — le client part avant que les résultats arrivent",
            "Pas de clause de propriété intellectuelle sur les snapshots et workflows que tu as créés",
            "Conditions de résiliation inexistantes — un client peut partir du jour au lendemain sans préavis",
        ],
        "method_title": "Les 5 clauses essentielles d'un contrat agence IA",
        "method_steps": [
            ("Clause 1 : Durée et préavis", "6 mois minimum avec préavis de 30 jours. Justification : les résultats prennent 60-90 jours à se matérialiser. Un contrat de 1 mois condamne l'agence à un churn structurel."),
            ("Clause 2 : Obligations du client", "Budget Ads minimum maintenu, réponse aux leads sous X heures, accès fournis dans les 48h. Si le client ne respecte pas ces conditions, la garantie résultat ne s'applique pas."),
            ("Clause 3 : Propriété des assets", "Les snapshots GHL, workflows, et templates restent la propriété de l'agence. Le client a un droit d'usage pendant la durée du contrat. En cas de résiliation, les assets ne sont pas transférables sauf accord et paiement supplémentaire."),
            ("Clause 4 : Modalités de paiement", "Setup facturé à la signature (50% à la commande, 50% à la livraison). Retainer prélevé le 1er de chaque mois en prélèvement automatique. Les impayés suspendent le service après 5 jours."),
            ("Clause 5 : Résultats et garantie", "Décrire précisément la métrique garantie (exemple : «&nbsp;15 leads qualifiés/mois&nbsp;»), le délai de garantie (30 jours après activation), et les conditions d'application (obligations client respectées)."),
        ],
        "yt_fragment":  "30 Milles balles en vendant une infrastructure de croissance",
        "yt_fragment2": "comment je vends (sans effort) avec la dark psychology",
        "stat_a": ("6 mois", "durée de contrat minimale recommandée"),
        "stat_b": ("50/50", "paiement setup : acompte + solde livraison"),
        "stat_c": ("5 clauses", "essentielles dans tout contrat agence IA"),
        "faqs": [
            ("Faut-il faire valider son contrat par un avocat ?", "Recommandé pour les contrats > 5 000 €. Pour les premiers clients, un template bien construit suffit. Des sites comme LegalPlace ou Legalstart proposent des templates CGPS personnalisables."),
            ("Comment présenter le contrat sans faire peur au client ?", "Présente-le comme une protection mutuelle : «&nbsp;Ce contrat garantit vos droits si nous ne livrons pas les résultats — il cadre aussi ce dont nous avons besoin de votre côté pour y arriver.&nbsp;»"),
            ("Que faire si un client refuse de signer un contrat ?", "C'est un signal d'alarme. Un client qui refuse de s'engager par contrat 6 mois n'est probablement pas prêt à payer le retainer au 2e mois non plus. Mieux vaut refuser que de travailler sans cadre."),
            ("Comment gérer les impayés ?", "Clause de suspension automatique à J+5 impayé. Lettre de mise en demeure à J+15. Accès GHL coupé si aucun règlement à J+30. La majorité des impayés se règlent à la première suspension."),
            ("Peut-on travailler en dehors des contrats pour des clients référents ?", "Pour un premier client pilote, oui — un bon de commande simple suffit. Mais dès que tu vises la récurrence et les > 2 000 €/mois par client, un contrat structuré est indispensable."),
        ],
        "related_niches": ["avocats", "experts-comptables", "coaching-consultants", "immobilier", "solaire"],
    },
    "comment-eviter-erreurs-agence-ia": {
        "slug":      "comment-eviter-erreurs-agence-ia",
        "h1":        "Les 5 erreurs qui tuent les agences IA — et comment les éviter",
        "title_tag": "Comment éviter les erreurs agence IA | Scaling Lab'",
        "meta_desc": "Les 5 erreurs fatales des agences IA en 2025 — et les corrections exactes pour chacune. Par Abdé Chan.",
        "hero_lead":  "99% des agences IA qui échouent font les mêmes 5 erreurs. Les identifier tôt te fait gagner 6 à 12 mois sur ta courbe d'apprentissage.",
        "problem":   "Tu travailles dur mais ta croissance stagne — sans savoir exactement pourquoi.",
        "problem_list": [
            "Tu changes de stratégie chaque semaine en suivant les dernières tendances LinkedIn",
            "Tu vends de la technologie plutôt que des résultats — tes prospects ne comprennent pas pourquoi te payer",
            "Tu consacres 80% de ton temps à la technique et 20% à la vente — c'est l'inverse qu'il faudrait",
            "Tu n'as pas de niche claire — «&nbsp;toutes les PME&nbsp;» n'est pas un marché cible",
        ],
        "method_title": "Les 5 corrections exactes",
        "method_steps": [
            ("Erreur 1 : Vendre de l'IA au lieu de vendre des résultats", "Correction : reformuler toute l'offre en résultats mesurables. «&nbsp;15 RDV qualifiés en 30 jours&nbsp;» au lieu de «&nbsp;chatbot IA GoHighLevel&nbsp;». Le client achète un résultat, pas un outil."),
            ("Erreur 2 : Négliger l'acquisition au profit de la technique", "Correction : minimum 2 heures par jour de prospection active jusqu'à 5k€/mois de MRR. Zéro formation technique sans prospection en parallèle. Les outils ne génèrent pas de clients."),
            ("Erreur 3 : Sous-estimer le niveau requis pour closer", "Correction : pratiquer le script de vente à froid, enregistrer et réécouter chaque appel, identifier 1 point d'amélioration par appel. Le closing est un muscle — ça s'entraîne."),
            ("Erreur 4 : Changer de niche à chaque client difficile", "Correction : choisir 1 niche sur 3 mois minimum avant d'en sortir. La réputation sectorielle se construit dans la durée. Les premières 4 semaines dans une niche sont toujours les plus difficiles."),
            ("Erreur 5 : Travailler sans système de reporting client", "Correction : tableau de bord GHL partagé + rapport mensuel automatique dès le premier client. Les clients qui voient leurs résultats ne partent pas."),
        ],
        "yt_fragment":  "la raison pour laquelle t'es bloqué sous 10k",
        "yt_fragment2": "en 23s tu lui expliques comment éviter le piège des automati",
        "stat_a": ("5 erreurs", "communes à 99% des agences IA qui stagnent"),
        "stat_b": ("2h/jour", "de prospection minimum avant 5k€/mois"),
        "stat_c": ("3 mois", "durée minimum sur une niche avant d'en changer"),
        "faqs": [
            ("Quelle est l'erreur la plus fréquente des agences IA débutantes ?", "Vendre de la technologie au lieu de vendre des résultats. 'Je fais de l'automatisation IA' ne provoque aucun achat. 'Je génère 15 RDV qualifiés/mois pour vos commerciaux' provoque une curiosité immédiate."),
            ("Est-ce qu'on peut réussir en agence IA sans vendre activement ?", "Non. L'inbound et le contenu organic arrivent après 6-12 mois de publication régulière. En dessous de 10k€/mois de MRR, la prospection active est non-négociable. Il n'y a pas de shortcut."),
            ("Comment savoir si on est dans la bonne niche ?", "Après 30 jours de prospection active dans une niche : si tu n'as pas obtenu 1 appel intéressé sur 100 contacts, la niche est trop compétitive ou ton message est trop générique. Ajuste le message avant de changer de niche."),
            ("L'erreur de pricing peut-elle couler une agence ?", "Oui. Sous-pricer attire des clients exigeants avec peu de budget. Sur-pricer sans preuve sociale crée de la méfiance. Le bon prix : le plus élevé que tu peux justifier avec les preuves dont tu disposes aujourd'hui."),
            ("Combien de temps pour corriger une de ces erreurs ?", "Entre 2 semaines (reformulation de l'offre) et 3 mois (construction de la réputation niche). Les corrections rapides : offre, message, script. Les corrections longues : réputation, contenu, réseau."),
        ],
        "related_niches": ["centres-esthetiques", "btp-construction", "restaurants", "coaching-consultants", "plombiers-electriciens"],
    },
}

# ─── NICHES (light version pour les liens) ─────────────────────────────────
NICHE_TITLES = {
    'centres-esthetiques':    'Centres esthétiques',
    'btp-construction':       'BTP & construction',
    'immobilier':             'Immobilier',
    'experts-comptables':     'Experts-comptables',
    'coaching-consultants':   'Coaching & consultants',
    'restaurants':            'Restaurants',
    'solaire':                'Solaire & photovoltaïque',
    'dentistes':              'Dentistes',
    'therapeutes':            'Thérapeutes & bien-être',
    'avocats':                'Avocats',
    'salons-coiffure':        'Salons de coiffure',
    'e-commerce':             'E-commerce',
    'garages-auto':           'Garages automobiles',
    'kines-osteos':           'Kinés & ostéopathes',
    'plombiers-electriciens': 'Plombiers & électriciens',
}

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def pid(slug):
    return 'gpb_' + hashlib.md5(slug.encode()).hexdigest()[:8]


def faq_ld_str(faqs, title_h1):
    items = [
        {
            "@type": "Question",
            "name":  q,
            "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}
        }
        for q, a in faqs
    ]
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": items
    }, ensure_ascii=False, indent=2)


def faq_accordion_html(faqs):
    parts = []
    for i, (q, a) in enumerate(faqs):
        border = 'border-bottom:none;' if i == len(faqs) - 1 else ''
        parts.append(f"""      <div class="faq-item" style="{border}">
        <button class="faq-q" onclick="toggleFaq(this)">
          {q}
          <svg class="faq-chevron" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="rgba(200,196,255,0.5)" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
        <div class="faq-a">{a}</div>
      </div>""")
    return '\n'.join(parts)


def method_steps_html(steps):
    cards = []
    for i, (title, body) in enumerate(steps):
        cards.append(f"""      <div style="display:flex;gap:20px;align-items:flex-start;padding:24px;background:rgba(12,12,30,0.65);border:1px solid rgba(30,30,56,0.8);border-radius:14px;">
        <div style="flex-shrink:0;width:36px;height:36px;background:linear-gradient(135deg,#3B2FE8,#6055FF);border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Oswald',sans-serif;font-weight:700;font-size:16px;color:#fff;">{i+1}</div>
        <div>
          <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:16px;color:#fff;text-transform:uppercase;letter-spacing:0.03em;margin-bottom:8px;">{title}</div>
          <div style="font-size:15px;color:rgba(255,255,255,0.65);line-height:1.65;">{body}</div>
        </div>
      </div>""")
    return '\n'.join(cards)


def problem_list_html(items):
    parts = []
    for item in items:
        parts.append(f"""        <li style="display:flex;align-items:flex-start;gap:12px;font-size:15px;color:rgba(255,255,255,0.65);line-height:1.6;">
          <span style="flex-shrink:0;width:20px;height:20px;background:rgba(239,68,68,0.15);border:1px solid rgba(239,68,68,0.3);border-radius:50%;display:flex;align-items:center;justify-content:center;margin-top:2px;font-size:11px;color:rgba(239,68,68,0.8);">✕</span>
          {item}
        </li>""")
    return '\n'.join(parts)


def related_niches_html(slugs):
    cards = []
    for slug in slugs:
        title = NICHE_TITLES.get(slug, slug)
        url = f"https://lescalinglab.com/agences/{slug}/"
        cards.append(f"""      <a href="{url}" style="display:block;padding:16px 20px;background:rgba(12,12,30,0.65);border:1px solid rgba(30,30,56,0.8);border-radius:12px;text-decoration:none;transition:border-color 0.3s,box-shadow 0.3s;" onmouseover="this.style.borderColor='rgba(74,59,255,0.4)';this.style.boxShadow='0 8px 24px rgba(59,47,232,0.1)'" onmouseout="this.style.borderColor='rgba(30,30,56,0.8)';this.style.boxShadow=''">
        <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:14px;color:#fff;text-transform:uppercase;letter-spacing:0.03em;">{title}</div>
        <div style="font-size:12px;color:rgba(96,85,255,0.7);margin-top:4px;font-family:'Oswald',sans-serif;letter-spacing:0.08em;text-transform:uppercase;">Explorer la niche →</div>
      </a>""")
    return '\n'.join(cards)


# ─── GÉNÉRATEUR HTML ──────────────────────────────────────────────────────────

def generate_page(p):
    gp = pid(p['slug'])
    today = date.today().isoformat()

    # YouTube excerpts
    excerpt1 = yt_excerpt(p['yt_fragment'], max_chars=350)
    excerpt2 = yt_excerpt(p['yt_fragment2'], max_chars=350) if p.get('yt_fragment2') else ""
    yt_link1 = yt_url(p['yt_fragment'])
    yt_title1 = yt_title(p['yt_fragment'])
    yt_link2 = yt_url(p['yt_fragment2']) if p.get('yt_fragment2') else ""
    yt_title2 = yt_title(p['yt_fragment2']) if p.get('yt_fragment2') else ""

    faq_ld = faq_ld_str(p['faqs'], p['h1'])
    breadcrumb_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Scaling Lab'", "item": "https://lescalinglab.com/"},
            {"@type": "ListItem", "position": 2, "name": "Agences IA", "item": "https://lescalinglab.com/agences/"},
            {"@type": "ListItem", "position": 3, "name": p['h1'], "item": f"https://lescalinglab.com/agences/{p['slug']}/"},
        ]
    }, ensure_ascii=False, indent=2)

    stat_a, stat_a_label = p['stat_a']
    stat_b, stat_b_label = p['stat_b']
    stat_c, stat_c_label = p['stat_c']

    yt_block1 = ""
    if excerpt1:
        yt_link_attr = f' href="{yt_link1}" target="_blank" rel="noopener"' if yt_link1 else ''
        tag = 'a' if yt_link1 else 'div'
        yt_block1 = f"""    <div style="margin-bottom:32px;">
      <{tag}{yt_link_attr} style="display:block;padding:24px;background:rgba(6,6,15,0.7);border:1px solid rgba(59,47,232,0.3);border-radius:14px;text-decoration:none;position:relative;overflow:hidden;">
        <div style="position:absolute;top:16px;right:16px;background:rgba(255,0,0,0.15);border:1px solid rgba(255,0,0,0.3);border-radius:6px;padding:4px 10px;font-family:'Oswald',sans-serif;font-size:10px;color:rgba(255,100,100,0.8);letter-spacing:0.1em;text-transform:uppercase;">▶ YouTube</div>
        <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:13px;color:#C8C4FF;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:12px;">Abdé Chan — {yt_title1}</div>
        <div style="font-size:15px;color:rgba(255,255,255,0.6);line-height:1.7;font-style:italic;">&laquo;&nbsp;{excerpt1}&nbsp;&raquo;</div>
        {f'<div style="margin-top:12px;font-size:12px;color:rgba(96,85,255,0.7);font-family:Oswald,sans-serif;letter-spacing:0.08em;text-transform:uppercase;">Voir la vidéo complète →</div>' if yt_link1 else ''}
      </{tag}>
    </div>"""

    yt_block2 = ""
    if excerpt2:
        yt_link_attr2 = f' href="{yt_link2}" target="_blank" rel="noopener"' if yt_link2 else ''
        tag2 = 'a' if yt_link2 else 'div'
        yt_block2 = f"""    <div style="margin-bottom:32px;">
      <{tag2}{yt_link_attr2} style="display:block;padding:24px;background:rgba(6,6,15,0.7);border:1px solid rgba(59,47,232,0.3);border-radius:14px;text-decoration:none;position:relative;overflow:hidden;">
        <div style="position:absolute;top:16px;right:16px;background:rgba(255,0,0,0.15);border:1px solid rgba(255,0,0,0.3);border-radius:6px;padding:4px 10px;font-family:'Oswald',sans-serif;font-size:10px;color:rgba(255,100,100,0.8);letter-spacing:0.1em;text-transform:uppercase;">▶ YouTube</div>
        <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:13px;color:#C8C4FF;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:12px;">Abdé Chan — {yt_title2}</div>
        <div style="font-size:15px;color:rgba(255,255,255,0.6);line-height:1.7;font-style:italic;">&laquo;&nbsp;{excerpt2}&nbsp;&raquo;</div>
        {f'<div style="margin-top:12px;font-size:12px;color:rgba(96,85,255,0.7);font-family:Oswald,sans-serif;letter-spacing:0.08em;text-transform:uppercase;">Voir la vidéo complète →</div>' if yt_link2 else ''}
      </{tag2}>
    </div>"""

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>{p['title_tag']}</title>
  <meta name="description" content="{p['meta_desc']}"/>
  <link rel="canonical" href="https://lescalinglab.com/agences/{p['slug']}/"/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Oswald:wght@400;600;700&family=Playfair+Display:ital,wght@1,700&display=swap" rel="stylesheet"/>
  <link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
  <!-- BreadcrumbList -->
  <script type="application/ld+json">{breadcrumb_ld}</script>
  <!-- FAQPage -->
  <script type="application/ld+json">{faq_ld}</script>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{background:#06060F;color:#fff;font-family:'Inter',sans-serif;line-height:1.6;overflow-x:hidden}}
    .container{{max-width:800px;margin:0 auto;padding:0 24px}}
    .container-wide{{max-width:1100px;margin:0 auto;padding:0 24px}}
    nav a{{color:rgba(255,255,255,0.7);text-decoration:none;transition:color 0.2s}}
    nav a:hover{{color:#fff}}
    .btn-primary{{display:inline-block;background:linear-gradient(135deg,#3B2FE8,#6055FF);color:#fff;font-family:'Oswald',sans-serif;font-weight:700;font-size:15px;letter-spacing:0.08em;text-transform:uppercase;padding:16px 40px;border-radius:8px;text-decoration:none;transition:opacity 0.2s,transform 0.2s}}
    .btn-primary:hover{{opacity:0.9;transform:translateY(-1px)}}
    .faq-item{{border-bottom:1px solid rgba(30,30,56,0.8);padding:0}}
    .faq-q{{width:100%;background:none;border:none;color:#fff;font-family:'Inter',sans-serif;font-size:15px;font-weight:600;text-align:left;padding:20px 0;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:16px;line-height:1.4}}
    .faq-a{{display:none;font-size:14px;color:rgba(255,255,255,0.6);line-height:1.7;padding-bottom:20px}}
    .faq-a.open{{display:block}}
    .faq-chevron{{transition:transform 0.3s;flex-shrink:0}}
    .faq-chevron.open{{transform:rotate(180deg)}}
    @media(max-width:640px){{.container,.container-wide{{padding:0 16px}}}}
  </style>
</head>
<body>
  <!-- SVG pattern background -->
  <svg id="{gp}" xmlns="http://www.w3.org/2000/svg" style="position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0;opacity:0.025">
    <defs><pattern id="g{gp}" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0L0 0 0 40" fill="none" stroke="#6055FF" stroke-width="0.5"/></pattern></defs>
    <rect width="100%" height="100%" fill="url(#g{gp})"/>
  </svg>
  <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:radial-gradient(ellipse 80% 60% at 20% 10%,rgba(59,47,232,0.12) 0%,transparent 60%),radial-gradient(ellipse 60% 80% at 80% 80%,rgba(96,85,255,0.08) 0%,transparent 60%);pointer-events:none;z-index:0;"></div>

  <!-- NAV -->
  <nav style="position:relative;z-index:10;padding:20px 32px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(30,30,56,0.6);">
    <a href="https://lescalinglab.com/" style="font-family:'Oswald',sans-serif;font-weight:700;font-size:18px;color:#fff;text-decoration:none;letter-spacing:0.04em;">Scaling Lab'</a>
    <div style="display:flex;gap:24px;align-items:center;">
      <a href="https://lescalinglab.com/agences/" style="font-size:13px;color:rgba(255,255,255,0.55);text-decoration:none;font-family:'Oswald',sans-serif;letter-spacing:0.08em;text-transform:uppercase;">← Agences IA</a>
      <a href="https://lescalinglab.com/resultats" style="font-size:13px;color:rgba(255,255,255,0.55);text-decoration:none;font-family:'Oswald',sans-serif;letter-spacing:0.08em;text-transform:uppercase;">Résultats</a>
      <a href="https://lescalinglab.com/#apply" style="background:linear-gradient(135deg,#3B2FE8,#6055FF);color:#fff;font-family:'Oswald',sans-serif;font-size:12px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:10px 22px;border-radius:6px;text-decoration:none;">Candidater</a>
    </div>
  </nav>

  <!-- BREADCRUMB -->
  <div style="position:relative;z-index:2;padding:14px 32px;border-bottom:1px solid rgba(30,30,56,0.4);">
    <div class="container-wide">
      <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:rgba(255,255,255,0.35);font-family:'Oswald',sans-serif;letter-spacing:0.05em;text-transform:uppercase;flex-wrap:wrap;">
        <a href="https://lescalinglab.com/" style="color:rgba(200,196,255,0.5);text-decoration:none;">Scaling Lab'</a>
        <span>›</span>
        <a href="https://lescalinglab.com/agences/" style="color:rgba(200,196,255,0.5);text-decoration:none;">Agences IA</a>
        <span>›</span>
        <span style="color:rgba(255,255,255,0.6);">{p['h1']}</span>
      </div>
    </div>
  </div>

  <!-- HERO -->
  <section style="position:relative;z-index:2;padding:80px 32px 64px;">
    <div class="container">
      <div style="display:inline-block;background:rgba(59,47,232,0.15);border:1px solid rgba(59,47,232,0.3);border-radius:100px;padding:6px 16px;font-family:'Oswald',sans-serif;font-size:11px;letter-spacing:0.15em;text-transform:uppercase;color:#C8C4FF;margin-bottom:24px;">Méthode Scaling Lab'</div>
      <h1 style="font-family:'Playfair Display',serif;font-style:italic;font-size:clamp(32px,5vw,52px);font-weight:700;line-height:1.15;margin-bottom:24px;letter-spacing:-0.01em;">{p['h1']}</h1>
      <p style="font-size:18px;color:rgba(255,255,255,0.65);line-height:1.75;margin-bottom:40px;">{p['hero_lead']}</p>

      <!-- 3 stats -->
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-bottom:48px;">
        <div style="padding:20px 24px;background:rgba(12,12,30,0.7);border:1px solid rgba(59,47,232,0.25);border-radius:12px;">
          <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:28px;background:linear-gradient(135deg,#C8C4FF,#6055FF);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{stat_a}</div>
          <div style="font-size:12px;color:rgba(255,255,255,0.4);margin-top:4px;">{stat_a_label}</div>
        </div>
        <div style="padding:20px 24px;background:rgba(12,12,30,0.7);border:1px solid rgba(59,47,232,0.25);border-radius:12px;">
          <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:28px;background:linear-gradient(135deg,#C8C4FF,#6055FF);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{stat_b}</div>
          <div style="font-size:12px;color:rgba(255,255,255,0.4);margin-top:4px;">{stat_b_label}</div>
        </div>
        <div style="padding:20px 24px;background:rgba(12,12,30,0.7);border:1px solid rgba(59,47,232,0.25);border-radius:12px;">
          <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:28px;background:linear-gradient(135deg,#C8C4FF,#6055FF);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">{stat_c}</div>
          <div style="font-size:12px;color:rgba(255,255,255,0.4);margin-top:4px;">{stat_c_label}</div>
        </div>
      </div>
    </div>
  </section>

  <!-- PROBLÈME -->
  <section style="position:relative;z-index:2;padding:0 32px 64px;">
    <div class="container">
      <div style="padding:32px;background:rgba(239,68,68,0.05);border:1px solid rgba(239,68,68,0.2);border-radius:16px;margin-bottom:24px;">
        <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:11px;letter-spacing:0.15em;text-transform:uppercase;color:rgba(239,68,68,0.7);margin-bottom:12px;">Le problème réel</div>
        <div style="font-size:18px;font-weight:600;color:rgba(255,255,255,0.9);line-height:1.5;margin-bottom:20px;">{p['problem']}</div>
        <ul style="list-style:none;display:flex;flex-direction:column;gap:12px;">
{problem_list_html(p['problem_list'])}
        </ul>
      </div>
    </div>
  </section>

  <!-- MÉTHODE -->
  <section style="position:relative;z-index:2;padding:0 32px 64px;">
    <div class="container">
      <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:11px;letter-spacing:0.15em;text-transform:uppercase;color:rgba(200,196,255,0.5);margin-bottom:16px;">La méthode</div>
      <h2 style="font-family:'Oswald',sans-serif;font-weight:700;font-size:clamp(22px,3.5vw,32px);text-transform:uppercase;letter-spacing:0.02em;margin-bottom:32px;">{p['method_title']}</h2>
      <div style="display:flex;flex-direction:column;gap:16px;">
{method_steps_html(p['method_steps'])}
      </div>
    </div>
  </section>

  <!-- YOUTUBE EXCERPTS -->
  <section style="position:relative;z-index:2;padding:0 32px 64px;">
    <div class="container">
      <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:11px;letter-spacing:0.15em;text-transform:uppercase;color:rgba(200,196,255,0.5);margin-bottom:20px;">Ce qu'Abdé Chan dit sur le sujet</div>
{yt_block1}
{yt_block2}
    </div>
  </section>

  <!-- NICHES LIÉES -->
  <section style="position:relative;z-index:2;padding:0 32px 64px;">
    <div class="container">
      <hr style="border:none;border-top:1px solid rgba(30,30,56,0.6);margin-bottom:48px;"/>
      <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:11px;letter-spacing:0.15em;text-transform:uppercase;color:rgba(200,196,255,0.5);margin-bottom:16px;">Niches recommandées</div>
      <h2 style="font-family:'Oswald',sans-serif;font-weight:700;font-size:22px;text-transform:uppercase;letter-spacing:0.02em;margin-bottom:24px;">Applique cette méthode dans ta niche</h2>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;">
{related_niches_html(p['related_niches'])}
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section style="position:relative;z-index:2;padding:80px 32px;">
    <div class="container" style="text-align:center;">
      <div style="max-width:600px;margin:0 auto;padding:48px;background:linear-gradient(135deg,rgba(59,47,232,0.15),rgba(96,85,255,0.08));border:1px solid rgba(59,47,232,0.35);border-radius:20px;">
        <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:11px;letter-spacing:0.15em;text-transform:uppercase;color:#C8C4FF;margin-bottom:16px;">Scaling Lab' — Coaching 1-1</div>
        <h2 style="font-family:'Playfair Display',serif;font-style:italic;font-size:clamp(26px,4vw,38px);line-height:1.2;margin-bottom:16px;">Tu veux appliquer cette méthode avec Abdé Chan ?</h2>
        <p style="font-size:15px;color:rgba(255,255,255,0.55);line-height:1.7;margin-bottom:32px;">6 mois de coaching 1-1 · 2 calls/semaine · Slack 24/7 · 3 à 5 places/mois</p>
        <a href="https://lescalinglab.com/#apply" class="btn-primary">Candidater au programme</a>
        <div style="margin-top:16px;font-size:12px;color:rgba(255,255,255,0.3);">Profil validé sur call · Garantie résultat incluse</div>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section style="position:relative;z-index:2;padding:0 32px 80px;">
    <div class="container">
      <hr style="border:none;border-top:1px solid rgba(30,30,56,0.6);margin-bottom:48px;"/>
      <h2 style="font-family:'Oswald',sans-serif;font-weight:700;font-size:clamp(20px,3vw,28px);text-transform:uppercase;letter-spacing:0.02em;margin-bottom:32px;">Questions fréquentes</h2>
      <div style="border:1px solid rgba(30,30,56,0.8);border-radius:14px;overflow:hidden;padding:0 24px;">
{faq_accordion_html(p['faqs'])}
      </div>
    </div>
  </section>

  <!-- FOOTER -->
  <!-- ═══ FOOTER ═══ -->
  <footer style="position:relative;z-index:2;padding:40px 32px;border-top:1px solid rgba(30,30,56,0.6);">
    <div class="container-wide" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;">
      <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:16px;color:rgba(255,255,255,0.8);">Scaling Lab'</div>
      <div style="display:flex;gap:24px;flex-wrap:wrap;">
        <a href="https://lescalinglab.com/" style="font-size:13px;color:rgba(255,255,255,0.35);text-decoration:none;font-family:'Oswald',sans-serif;text-transform:uppercase;letter-spacing:0.08em;">Accueil</a>
        <a href="https://lescalinglab.com/resultats" style="font-size:13px;color:rgba(255,255,255,0.35);text-decoration:none;font-family:'Oswald',sans-serif;text-transform:uppercase;letter-spacing:0.08em;">Résultats</a>
        <a href="https://lescalinglab.com/agences/" style="font-size:13px;color:rgba(255,255,255,0.35);text-decoration:none;font-family:'Oswald',sans-serif;text-transform:uppercase;letter-spacing:0.08em;">Agences IA</a>
        <a href="https://lescalinglab.com/#apply" style="font-size:13px;color:rgba(255,255,255,0.35);text-decoration:none;font-family:'Oswald',sans-serif;text-transform:uppercase;letter-spacing:0.08em;">Candidater</a>
      </div>
      <div style="font-size:12px;color:rgba(255,255,255,0.2);">© {date.today().year} Scaling Lab' · Abdé Chan</div>
    </div>
  </footer>

  <script>
    function toggleFaq(btn) {{
      const a = btn.nextElementSibling;
      const ch = btn.querySelector('.faq-chevron');
      a.classList.toggle('open');
      ch.classList.toggle('open');
    }}
  </script>
</body>
</html>"""
    return html


# ─── SITEMAP ────────────────────────────────────────────────────────────────

def update_sitemap(new_urls):
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    tree = ET.parse(SITEMAP_PATH)
    root = tree.getroot()
    NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    existing = {url.find(f'{{{NS}}}loc').text for url in root.findall(f'{{{NS}}}url')}
    today = date.today().isoformat()
    added = 0
    for u in new_urls:
        if u not in existing:
            url_el = ET.SubElement(root, f'{{{NS}}}url')
            ET.SubElement(url_el, f'{{{NS}}}loc').text = u
            ET.SubElement(url_el, f'{{{NS}}}lastmod').text = today
            ET.SubElement(url_el, f'{{{NS}}}changefreq').text = 'monthly'
            ET.SubElement(url_el, f'{{{NS}}}priority').text = '0.7'
            added += 1
    if added:
        ET.indent(root, space='  ')
        tree.write(SITEMAP_PATH, encoding='utf-8', xml_declaration=True)
    return added


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    new_urls = []
    for slug, p in PROBLEMATIQUES.items():
        out_dir = os.path.join(AGENCES_DIR, slug)
        os.makedirs(out_dir, exist_ok=True)
        html = generate_page(p)
        path = os.path.join(out_dir, "index.html")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        size_kb = os.path.getsize(path) // 1024
        print(f"  ✓ /agences/{slug}/ ({size_kb}KB)")
        new_urls.append(f"{BASE_URL}/agences/{slug}/")

    added = update_sitemap(new_urls)
    print(f"\nSitemap : +{added} URLs ajoutées")

    with open(os.path.join(_dir, "indexnow_problematiques_urls.json"), 'w', encoding='utf-8') as f:
        json.dump(new_urls, f, ensure_ascii=False, indent=2)
    print(f"IndexNow : {len(new_urls)} URLs sauvegardées → indexnow_problematiques_urls.json")
    print(f"\nTotal : {len(PROBLEMATIQUES)} pages problématiques générées")


if __name__ == '__main__':
    main()
