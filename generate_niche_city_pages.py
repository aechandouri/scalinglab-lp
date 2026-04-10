#!/usr/bin/env python3
"""
generate_niche_city_pages.py
Génère /agences/[niche]/[ville]/index.html pour le SEO programmatique.
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
}

# ─── DONNÉES VILLES ──────────────────────────────────────────────────────────

CITIES = [
    {'slug': 'paris',        'name': 'Paris',        'region': 'Île-de-France',              'pop': 2161000},
    {'slug': 'marseille',    'name': 'Marseille',    'region': 'Provence-Alpes-Côte d\'Azur','pop': 870731},
    {'slug': 'lyon',         'name': 'Lyon',         'region': 'Auvergne-Rhône-Alpes',       'pop': 522228},
    {'slug': 'toulouse',     'name': 'Toulouse',     'region': 'Occitanie',                  'pop': 479553},
    {'slug': 'nice',         'name': 'Nice',         'region': 'Provence-Alpes-Côte d\'Azur','pop': 342522},
    {'slug': 'nantes',       'name': 'Nantes',       'region': 'Pays de la Loire',           'pop': 320732},
    {'slug': 'montpellier',  'name': 'Montpellier',  'region': 'Occitanie',                  'pop': 295542},
    {'slug': 'strasbourg',   'name': 'Strasbourg',   'region': 'Grand Est',                  'pop': 285083},
    {'slug': 'bordeaux',     'name': 'Bordeaux',     'region': 'Nouvelle-Aquitaine',         'pop': 257804},
    {'slug': 'lille',        'name': 'Lille',        'region': 'Hauts-de-France',            'pop': 236234},
]

FRANCE_POP = 68_000_000

# ─── HELPERS ─────────────────────────────────────────────────────────────────

def pattern_id(niche_slug, city_slug):
    h = hashlib.md5(f"{niche_slug}-{city_slug}".encode()).hexdigest()[:8]
    return f"gp_{h}"

def local_count(national, city_pop):
    """Estimation locale basée sur ratio population."""
    raw = national * city_pop / FRANCE_POP
    # Arrondi à la dizaine la plus proche
    if raw < 50:
        return max(int(round(raw / 5) * 5), 5)
    elif raw < 200:
        return int(round(raw / 10) * 10)
    elif raw < 2000:
        return int(round(raw / 50) * 50)
    else:
        return int(round(raw / 100) * 100)

def fmt_count(n):
    """Format nombre avec séparateur milliers (espace)."""
    return f"{n:,}".replace(",", "\u202f")  # espace fine insécable

# ─── GÉNÉRATEUR HTML ─────────────────────────────────────────────────────────

def generate_page(niche_slug, niche, city):
    n = niche
    c = city
    pid = pattern_id(niche_slug, c['slug'])
    lcount = local_count(n['national_count'], c['pop'])
    lcount_fmt = fmt_count(lcount)
    canonical = f"https://lescalinglab.com/agences/{niche_slug}/{c['slug']}/"
    today = date.today().isoformat()

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{n['title_short']} à {c['name']} — Agence IA | Scaling Lab'</title>
  <meta name="description" content="Environ {lcount_fmt} établissements {n['label_raw'].lower()} à {c['name']} et en {c['region']}. Voici comment lancer une agence IA dans cette niche localement — l'opportunité, ce qu'on vend, et le ticket moyen." />
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
      <span class="display-bold" style="font-size:clamp(20px,2.8vw,38px);display:block;line-height:1.1;background:linear-gradient(135deg,#C8C4FF 0%,#6055FF 50%,#3B2FE8 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-top:8px;">environ {lcount_fmt} établissements dans la région</span>
    </h1>
    <p style="font-size:17px;line-height:1.75;color:rgba(255,255,255,0.55);max-width:640px;margin-bottom:40px;">
      {c['name']} et la région {c['region']} concentrent environ {lcount_fmt} {n['label_raw'].lower()}. La majorité n'ont aucun système pour capter et convertir leurs leads automatiquement. C'est exactement l'opportunité qu'on enseigne au Scaling Lab'.
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
    <h2 class="heading-oswald" style="font-size:clamp(20px,2.8vw,32px);color:#fff;margin-bottom:16px;">Pourquoi c'est une niche à fort potentiel en {c['region']}</h2>
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
      Ces problèmes sont identiques à {c['name']} comme partout en France. Ce qui change, c'est que localement la concurrence IA est quasi nulle.
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

    # Supprimer les entrées ville déjà présentes (re-run safe)
    existing_locs = {url.find(f'{{{ns}}}loc').text for url in root.findall(f'{{{ns}}}url')}
    for url in generated_urls:
        if url not in existing_locs:
            url_el = ET.SubElement(root, f'{{{ns}}}url')
            ET.SubElement(url_el, f'{{{ns}}}loc').text = url
            ET.SubElement(url_el, f'{{{ns}}}lastmod').text = today
            ET.SubElement(url_el, f'{{{ns}}}changefreq').text = 'monthly'
            ET.SubElement(url_el, f'{{{ns}}}priority').text = '0.6'

    # Indent propre
    ET.indent(tree, space='  ')
    tree.write(sitemap_path, encoding='UTF-8', xml_declaration=True)

    print(f"\n✅ {count} pages générées")
    print(f"✅ sitemap.xml mis à jour ({len(generated_urls)} nouvelles URLs)")
    print(f"\nURLs pour IndexNow :")
    for u in generated_urls:
        print(f"  {u}")

    # ─── Fichier JSON des URLs pour IndexNow ───
    indexnow_path = os.path.join(base_dir, 'indexnow_urls.json')
    with open(indexnow_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(generated_urls, f, ensure_ascii=False, indent=2)
    print(f"\n✅ indexnow_urls.json créé ({len(generated_urls)} URLs)")

if __name__ == '__main__':
    main()
