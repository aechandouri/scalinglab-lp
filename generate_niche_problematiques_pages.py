#!/usr/bin/env python3
"""
generate_niche_problematiques_pages.py
Génère /agences/[niche]/comment-[slug]/index.html — 5ème axe SEO.
15 niches × 24 problématiques = 360 pages croisées.
Usage : python3 generate_niche_problematiques_pages.py
"""

import os, hashlib, json, re, importlib.util
import xml.etree.ElementTree as ET
from datetime import date

# ─── Répertoires ──────────────────────────────────────────────────────────────
_dir   = os.path.dirname(os.path.abspath(__file__))
AGENCES_DIR  = os.path.join(_dir, "agences")
SITEMAP_PATH = os.path.join(_dir, "sitemap.xml")
BASE_URL     = "https://lescalinglab.com"

# ─── Import NICHES depuis generate_niche_city_pages.py ───────────────────────
def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_niche_mod = _load_module("niche_city", os.path.join(_dir, "generate_niche_city_pages.py"))
NICHES = _niche_mod.NICHES

# ─── Import PROBLEMATIQUES depuis generate_problematiques_pages.py ────────────
_prob_mod = _load_module("problematiques", os.path.join(_dir, "generate_problematiques_pages.py"))
PROBLEMATIQUES  = _prob_mod.PROBLEMATIQUES
yt_excerpt      = _prob_mod.yt_excerpt
yt_url          = _prob_mod.yt_url
yt_title        = _prob_mod.yt_title

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def pid(niche_slug, prob_slug):
    key = f"{niche_slug}_{prob_slug}"
    return 'gnp_' + hashlib.md5(key.encode()).hexdigest()[:8]


def strip_html(text):
    return re.sub(r'<[^>]+>', '', text)


def faq_ld_str(faqs):
    items = [
        {
            "@type": "Question",
            "name":  q,
            "acceptedAnswer": {"@type": "Answer", "text": strip_html(a)}
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


# ─── Génération des FAQ niche-adaptées ────────────────────────────────────────
def niche_faqs(n, p):
    """Génère 5 FAQs spécifiques à la combinaison niche × problématique."""
    niche_label = n['title_short']
    prob_h1     = p['h1']
    ticket      = n['ticket_setup']
    student     = n['student_name']
    student_before = n.get('student_before', '3 000 €')
    student_after  = n.get('student_after', '20 000 €')

    return [
        (
            f"Est-ce que la méthode «&nbsp;{strip_html(prob_h1)}&nbsp;» s'applique aux {niche_label} ?",
            f"Oui — et c'est même une des niches les plus adaptées. Les {niche_label} ont le budget ({ticket} de setup), la douleur métier mesurable, et une faible concurrence IA en 2025. Abdé Chan enseigne l'application sectorielle complète dans le programme Scaling Lab'."
        ),
        (
            f"Quel budget faut-il pour travailler avec les {niche_label} ?",
            f"Le ticket setup pour les {niche_label} est de {ticket}. Avec un retainer mensuel de {n['ticket_retainer']}. Le ROI client est justifiable en moins de 3 mois pour ce secteur — ce qui facilite considérablement le closing."
        ),
        (
            f"Y a-t-il des cas clients de {student} dans la niche {niche_label} ?",
            f"{student} est passé·e de {student_before} à {student_after}/mois en ciblant les {niche_label}. {n['student_desc']} C'est la preuve sociale utilisée dans le programme."
        ),
        (
            f"Par où commencer pour appliquer cette méthode dans les {niche_label} ?",
            f"Le premier paso : réserver un appel de diagnostic avec l'équipe Scaling Lab' pour valider que ton profil correspond à la niche {niche_label}. Tous les outils, scripts et templates spécifiques à ce secteur sont fournis dans le programme."
        ),
        (
            f"La saturation est-elle un problème dans la niche {niche_label} ?",
            f"Non. Moins de 5% des {niche_label} francophones disposent d'une infrastructure IA en 2025. Le marché est {n.get('stat1_num', 'très large')} établissements — dont la très grande majorité fonctionnent encore sans aucun système d'acquisition automatisé."
        ),
    ]


# ─── Générateur HTML ──────────────────────────────────────────────────────────
def generate_page(n_slug, n, p_slug, p):
    gid   = pid(n_slug, p_slug)
    today = date.today().isoformat()

    niche_label     = n['title_short']
    niche_label_raw = n['label_raw']
    niche_url       = f"{BASE_URL}/agences/{n_slug}/"
    prob_url        = f"{BASE_URL}/agences/{p_slug}/"
    page_url        = f"{BASE_URL}/agences/{n_slug}/{p_slug}/"

    # Titre/meta adaptés à la niche
    title_tag  = f"{strip_html(p['h1'])} — {niche_label} | Scaling Lab'"
    meta_desc  = f"Comment appliquer la méthode {strip_html(p['h1']).lower()} dans les {niche_label}. Système IA clé en main, ticket {n['ticket_setup']}. Par Abdé Chan."
    h1         = f"{strip_html(p['h1'])} — {niche_label}"

    # Extraits YouTube
    excerpt1  = yt_excerpt(p['yt_fragment'], max_chars=320)
    yt_link1  = yt_url(p['yt_fragment'])
    yt_title1 = yt_title(p['yt_fragment'])

    # Méthode steps (réutilisés depuis la prob)
    steps_html = method_steps_html(p['method_steps'])

    # Problèmes spécifiques niche
    niche_problems = [
        f"Les {niche_label} ont {n['pain1_title'].lower()} — sans système IA, ça ne change pas",
        f"{n['pain2_title']} — un problème structurel, pas une question de talent",
        f"La plupart des {niche_label} n'ont aucun outil pour automatiser leur acquisition",
        p['problem_list'][0] if p['problem_list'] else "L'absence de système d'acquisition bloque la croissance",
    ]

    # FAQs niche-adaptées
    faqs = niche_faqs(n, p)
    faq_ld    = faq_ld_str(faqs)
    faq_html  = faq_accordion_html(faqs)

    stat_a, stat_a_label = p['stat_a']
    stat_b, stat_b_label = p['stat_b']
    stat_c, stat_c_label = p['stat_c']

    breadcrumb_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Scaling Lab'",  "item": f"{BASE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Agences IA",    "item": f"{BASE_URL}/agences/"},
            {"@type": "ListItem", "position": 3, "name": niche_label_raw, "item": niche_url},
            {"@type": "ListItem", "position": 4, "name": h1,              "item": page_url},
        ]
    }, ensure_ascii=False, indent=2)

    # Bloc YouTube
    yt_block = ""
    if excerpt1:
        tag  = 'a' if yt_link1 else 'div'
        attr = f' href="{yt_link1}" target="_blank" rel="noopener"' if yt_link1 else ''
        yt_block = f"""    <div style="margin-bottom:32px;">
      <{tag}{attr} style="display:block;padding:24px;background:rgba(6,6,15,0.7);border:1px solid rgba(59,47,232,0.3);border-radius:14px;text-decoration:none;position:relative;overflow:hidden;">
        <div style="position:absolute;top:16px;right:16px;background:rgba(255,0,0,0.15);border:1px solid rgba(255,0,0,0.3);border-radius:6px;padding:4px 10px;font-family:'Oswald',sans-serif;font-size:10px;color:rgba(255,100,100,0.8);letter-spacing:0.1em;text-transform:uppercase;">▶ YouTube</div>
        <div style="font-family:'Oswald',sans-serif;font-size:11px;color:rgba(96,85,255,0.7);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">Abdé Chan — {yt_title1}</div>
        <div style="font-size:14px;color:rgba(255,255,255,0.6);line-height:1.65;font-style:italic;">« {excerpt1} »</div>
      </{tag}>
    </div>"""

    # Case study niche
    student_block = ""
    if n.get('student_before') and n.get('student_after'):
        student_block = f"""    <div style="padding:28px;background:linear-gradient(135deg,rgba(59,47,232,0.12),rgba(96,85,255,0.06));border:1px solid rgba(59,47,232,0.25);border-radius:16px;margin-bottom:32px;">
      <div style="font-family:'Oswald',sans-serif;font-size:11px;color:rgba(96,85,255,0.7);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:12px;">Cas client — {niche_label}</div>
      <div style="display:flex;gap:24px;align-items:center;margin-bottom:16px;flex-wrap:wrap;">
        <div style="text-align:center;">
          <div style="font-family:'Oswald',sans-serif;font-size:28px;font-weight:700;color:rgba(255,255,255,0.4);line-height:1;">{n['student_before']}</div>
          <div style="font-size:11px;color:rgba(255,255,255,0.3);margin-top:4px;">Avant</div>
        </div>
        <div style="font-size:24px;color:rgba(96,85,255,0.5);">→</div>
        <div style="text-align:center;">
          <div style="font-family:'Oswald',sans-serif;font-size:32px;font-weight:900;color:#fff;line-height:1;">{n['student_after']}</div>
          <div style="font-size:11px;color:rgba(96,85,255,0.7);margin-top:4px;">{n['student_delay']}</div>
        </div>
      </div>
      <div style="font-size:14px;color:rgba(255,255,255,0.55);line-height:1.65;">{n['student_desc']}</div>
    </div>"""

    problems_html = problem_list_html(niche_problems)

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title_tag}</title>
  <meta name="description" content="{meta_desc}">
  <link rel="canonical" href="{page_url}">
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- JSON-LD -->
  <script type="application/ld+json">{breadcrumb_ld}</script>
  <script type="application/ld+json">{faq_ld}</script>
  <style>
    *{{box-sizing:border-box;margin:0;padding:0}}
    body{{background:#05050F;color:#fff;font-family:'Inter',sans-serif;}}
    .noise{{position:fixed;inset:0;pointer-events:none;opacity:.025;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");z-index:0}}
    .faq-item{{border-bottom:1px solid rgba(30,30,56,0.8);padding:0}}
    .faq-q{{width:100%;background:none;border:none;color:rgba(255,255,255,0.85);font-family:'Oswald',sans-serif;font-size:16px;font-weight:500;padding:20px 0;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:12px;text-align:left;}}
    .faq-a{{max-height:0;overflow:hidden;font-size:14px;color:rgba(255,255,255,0.55);line-height:1.7;transition:max-height .35s ease,padding .35s ease}}
    .faq-a.open{{max-height:400px;padding-bottom:20px}}
    .faq-chevron{{transition:transform .3s ease;flex-shrink:0}}
    .faq-q.active .faq-chevron{{transform:rotate(180deg)}}
    @media(max-width:768px){{
      .hero-grid{{grid-template-columns:1fr!important}}
      .stats-row{{grid-template-columns:1fr 1fr!important}}
    }}
  </style>
</head>
<body>
<div class="noise"></div>

<!-- NAV -->
<nav style="position:sticky;top:0;z-index:50;background:rgba(5,5,15,0.85);backdrop-filter:blur(12px);border-bottom:1px solid rgba(30,30,56,0.6);padding:0 24px;">
  <div style="max-width:1100px;margin:0 auto;height:60px;display:flex;align-items:center;justify-content:space-between;">
    <a href="{BASE_URL}/" style="font-family:'Oswald',sans-serif;font-size:20px;font-weight:900;color:#fff;text-decoration:none;letter-spacing:-0.02em;">
      SCALING <span style="color:#6055FF;">LAB'</span>
    </a>
    <a href="{BASE_URL}/#apply" style="background:linear-gradient(135deg,#3B2FE8,#6055FF);color:#fff;font-family:'Oswald',sans-serif;font-size:13px;font-weight:700;padding:10px 20px;border-radius:8px;text-decoration:none;letter-spacing:0.06em;text-transform:uppercase;">
      Réserver un appel →
    </a>
  </div>
</nav>

<!-- BREADCRUMB -->
<div style="padding:12px 24px;background:rgba(12,12,30,0.4);">
  <div style="max-width:1100px;margin:0 auto;font-size:12px;color:rgba(255,255,255,0.35);font-family:'Oswald',sans-serif;letter-spacing:0.06em;text-transform:uppercase;">
    <a href="{BASE_URL}/" style="color:rgba(255,255,255,0.35);text-decoration:none;">Scaling Lab'</a>
    <span style="margin:0 8px;opacity:.4;">/</span>
    <a href="{BASE_URL}/agences/" style="color:rgba(255,255,255,0.35);text-decoration:none;">Agences IA</a>
    <span style="margin:0 8px;opacity:.4;">/</span>
    <a href="{niche_url}" style="color:rgba(96,85,255,0.7);text-decoration:none;">{niche_label}</a>
    <span style="margin:0 8px;opacity:.4;">/</span>
    <span style="color:rgba(255,255,255,0.55);">{strip_html(p['h1'])}</span>
  </div>
</div>

<!-- HERO -->
<section style="padding:72px 24px 56px;position:relative;overflow:hidden;">
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(59,47,232,0.18) 0%,transparent 70%);pointer-events:none;"></div>
  <div style="max-width:860px;margin:0 auto;text-align:center;position:relative;z-index:1;">
    <div style="display:inline-flex;align-items:center;gap:8px;background:rgba(59,47,232,0.12);border:1px solid rgba(59,47,232,0.3);border-radius:100px;padding:6px 16px;font-family:'Oswald',sans-serif;font-size:11px;color:rgba(96,85,255,0.8);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:24px;">
      Méthode · {niche_label}
    </div>
    <h1 style="font-family:'Oswald',sans-serif;font-size:clamp(32px,5vw,52px);font-weight:900;line-height:1.05;letter-spacing:-0.025em;margin-bottom:24px;">
      {strip_html(p['h1'])}
      <span style="display:block;color:rgba(96,85,255,0.85);font-size:0.75em;margin-top:8px;">— Spécial {niche_label}</span>
    </h1>
    <p style="font-size:clamp(16px,2vw,19px);color:rgba(255,255,255,0.55);line-height:1.65;max-width:680px;margin:0 auto 36px;">
      {p['hero_lead']} Appliqué aux <strong style="color:rgba(255,255,255,0.75);">{niche_label}</strong>, ce levier est particulièrement puissant : ticket setup {n['ticket_setup']}, douleur métier forte, faible concurrence IA.
    </p>
    <div class="stats-row" style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;max-width:600px;margin:0 auto 36px;">
      <div style="padding:20px;background:rgba(12,12,30,0.7);border:1px solid rgba(30,30,56,0.8);border-radius:12px;text-align:center;">
        <div style="font-family:'Oswald',sans-serif;font-size:28px;font-weight:900;color:#fff;">{stat_a}</div>
        <div style="font-size:11px;color:rgba(255,255,255,0.4);margin-top:4px;line-height:1.4;">{stat_a_label}</div>
      </div>
      <div style="padding:20px;background:rgba(12,12,30,0.7);border:1px solid rgba(30,30,56,0.8);border-radius:12px;text-align:center;">
        <div style="font-family:'Oswald',sans-serif;font-size:28px;font-weight:900;color:#fff;">{stat_b}</div>
        <div style="font-size:11px;color:rgba(255,255,255,0.4);margin-top:4px;line-height:1.4;">{stat_b_label}</div>
      </div>
      <div style="padding:20px;background:rgba(12,12,30,0.7);border:1px solid rgba(30,30,56,0.8);border-radius:12px;text-align:center;">
        <div style="font-family:'Oswald',sans-serif;font-size:28px;font-weight:900;color:#fff;">{stat_c}</div>
        <div style="font-size:11px;color:rgba(255,255,255,0.4);margin-top:4px;line-height:1.4;">{stat_c_label}</div>
      </div>
    </div>
    <a href="{BASE_URL}/#apply" style="display:inline-flex;align-items:center;gap:10px;background:linear-gradient(135deg,#3B2FE8,#6055FF);color:#fff;font-family:'Oswald',sans-serif;font-size:16px;font-weight:700;padding:16px 32px;border-radius:12px;text-decoration:none;letter-spacing:0.06em;text-transform:uppercase;box-shadow:0 8px 32px rgba(59,47,232,0.35);">
      Réserver un appel gratuit
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
    </a>
  </div>
</section>

<!-- PROBLÈME NICHE -->
<section style="padding:56px 24px;background:rgba(8,8,20,0.5);">
  <div style="max-width:800px;margin:0 auto;">
    <div style="font-family:'Oswald',sans-serif;font-size:11px;color:rgba(239,68,68,0.6);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:12px;">Le problème</div>
    <h2 style="font-family:'Oswald',sans-serif;font-size:clamp(24px,3.5vw,34px);font-weight:700;color:#fff;margin-bottom:8px;line-height:1.15;">{p['problem']}</h2>
    <p style="font-size:15px;color:rgba(255,255,255,0.45);margin-bottom:28px;line-height:1.6;">Ce schéma est particulièrement présent dans les <strong style="color:rgba(255,255,255,0.65);">{niche_label}</strong>. Voici pourquoi :</p>
    <ul style="list-style:none;display:flex;flex-direction:column;gap:12px;">
{problems_html}
    </ul>
  </div>
</section>

<!-- DOULEURS NICHE SPÉCIFIQUES -->
<section style="padding:56px 24px;">
  <div style="max-width:800px;margin:0 auto;">
    <div style="font-family:'Oswald',sans-serif;font-size:11px;color:rgba(96,85,255,0.6);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:12px;">Contexte {niche_label}</div>
    <h2 style="font-family:'Oswald',sans-serif;font-size:clamp(22px,3vw,30px);font-weight:700;color:#fff;margin-bottom:28px;line-height:1.2;">Les 3 douleurs structurelles des {niche_label}</h2>
    <div style="display:grid;gap:16px;">
      <div style="padding:24px;background:rgba(12,12,30,0.65);border:1px solid rgba(30,30,56,0.8);border-radius:14px;">
        <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:16px;color:#fff;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.03em;">{n['pain1_title']}</div>
        <div style="font-size:14px;color:rgba(255,255,255,0.55);line-height:1.65;">{n['pain1_body']}</div>
      </div>
      <div style="padding:24px;background:rgba(12,12,30,0.65);border:1px solid rgba(30,30,56,0.8);border-radius:14px;">
        <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:16px;color:#fff;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.03em;">{n['pain2_title']}</div>
        <div style="font-size:14px;color:rgba(255,255,255,0.55);line-height:1.65;">{n['pain2_body']}</div>
      </div>
      <div style="padding:24px;background:rgba(12,12,30,0.65);border:1px solid rgba(30,30,56,0.8);border-radius:14px;">
        <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:16px;color:#fff;margin-bottom:8px;text-transform:uppercase;letter-spacing:0.03em;">{n['pain3_title']}</div>
        <div style="font-size:14px;color:rgba(255,255,255,0.55);line-height:1.65;">{n['pain3_body']}</div>
      </div>
    </div>
  </div>
</section>

<!-- MÉTHODE -->
<section style="padding:56px 24px;background:rgba(8,8,20,0.5);">
  <div style="max-width:800px;margin:0 auto;">
    <div style="font-family:'Oswald',sans-serif;font-size:11px;color:rgba(96,85,255,0.6);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:12px;">La méthode</div>
    <h2 style="font-family:'Oswald',sans-serif;font-size:clamp(22px,3vw,30px);font-weight:700;color:#fff;margin-bottom:28px;line-height:1.2;">{p['method_title']}</h2>
    <div style="display:flex;flex-direction:column;gap:16px;">
{steps_html}
    </div>
  </div>
</section>

<!-- EXTRAIT YOUTUBE -->
{yt_block}

<!-- CAS CLIENT NICHE -->
{student_block}

<!-- INFRASTRUCTURE NICHE -->
<section style="padding:56px 24px;">
  <div style="max-width:800px;margin:0 auto;">
    <div style="font-family:'Oswald',sans-serif;font-size:11px;color:rgba(96,85,255,0.6);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:12px;">Infrastructure · {niche_label}</div>
    <h2 style="font-family:'Oswald',sans-serif;font-size:clamp(22px,3vw,28px);font-weight:700;color:#fff;margin-bottom:28px;line-height:1.2;">Le stack IA déployé dans les {niche_label}</h2>
    <div style="display:grid;gap:16px;">
      <div style="padding:24px;background:rgba(12,12,30,0.65);border:1px solid rgba(59,47,232,0.2);border-radius:14px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
          <div style="width:8px;height:8px;background:#6055FF;border-radius:50%;flex-shrink:0;"></div>
          <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:15px;color:#fff;text-transform:uppercase;letter-spacing:0.03em;">{n['infra1_title']}</div>
        </div>
        <div style="font-size:14px;color:rgba(255,255,255,0.55);line-height:1.65;padding-left:18px;">{n['infra1_body']}</div>
      </div>
      <div style="padding:24px;background:rgba(12,12,30,0.65);border:1px solid rgba(59,47,232,0.2);border-radius:14px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
          <div style="width:8px;height:8px;background:#6055FF;border-radius:50%;flex-shrink:0;"></div>
          <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:15px;color:#fff;text-transform:uppercase;letter-spacing:0.03em;">{n['infra2_title']}</div>
        </div>
        <div style="font-size:14px;color:rgba(255,255,255,0.55);line-height:1.65;padding-left:18px;">{n['infra2_body']}</div>
      </div>
      <div style="padding:24px;background:rgba(12,12,30,0.65);border:1px solid rgba(59,47,232,0.2);border-radius:14px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
          <div style="width:8px;height:8px;background:#6055FF;border-radius:50%;flex-shrink:0;"></div>
          <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:15px;color:#fff;text-transform:uppercase;letter-spacing:0.03em;">{n['infra3_title']}</div>
        </div>
        <div style="font-size:14px;color:rgba(255,255,255,0.55);line-height:1.65;padding-left:18px;">{n['infra3_body']}</div>
      </div>
    </div>
  </div>
</section>

<!-- FAQ -->
<section style="padding:56px 24px;background:rgba(8,8,20,0.5);">
  <div style="max-width:800px;margin:0 auto;">
    <div style="font-family:'Oswald',sans-serif;font-size:11px;color:rgba(96,85,255,0.6);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:12px;">FAQ</div>
    <h2 style="font-family:'Oswald',sans-serif;font-size:clamp(22px,3vw,30px);font-weight:700;color:#fff;margin-bottom:28px;">{niche_label} × Méthode Scaling Lab'</h2>
    <div style="background:rgba(12,12,30,0.65);border:1px solid rgba(30,30,56,0.8);border-radius:16px;padding:0 28px;">
{faq_html}
    </div>
  </div>
</section>

<!-- LIENS INTERNES -->
<section style="padding:48px 24px;">
  <div style="max-width:800px;margin:0 auto;">
    <div style="font-family:'Oswald',sans-serif;font-size:11px;color:rgba(255,255,255,0.3);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:20px;">Pages associées</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
      <a href="{niche_url}" style="display:block;padding:18px 20px;background:rgba(12,12,30,0.65);border:1px solid rgba(30,30,56,0.8);border-radius:12px;text-decoration:none;" onmouseover="this.style.borderColor='rgba(74,59,255,0.4)'" onmouseout="this.style.borderColor='rgba(30,30,56,0.8)'">
        <div style="font-family:'Oswald',sans-serif;font-size:11px;color:rgba(96,85,255,0.6);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;">Niche</div>
        <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:15px;color:#fff;">Agence IA · {niche_label} →</div>
      </a>
      <a href="{prob_url}" style="display:block;padding:18px 20px;background:rgba(12,12,30,0.65);border:1px solid rgba(30,30,56,0.8);border-radius:12px;text-decoration:none;" onmouseover="this.style.borderColor='rgba(74,59,255,0.4)'" onmouseout="this.style.borderColor='rgba(30,30,56,0.8)'">
        <div style="font-family:'Oswald',sans-serif;font-size:11px;color:rgba(96,85,255,0.6);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;">Guide complet</div>
        <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:15px;color:#fff;">{strip_html(p['h1'])} →</div>
      </a>
      <a href="{BASE_URL}/agences/" style="display:block;padding:18px 20px;background:rgba(12,12,30,0.65);border:1px solid rgba(30,30,56,0.8);border-radius:12px;text-decoration:none;" onmouseover="this.style.borderColor='rgba(74,59,255,0.4)'" onmouseout="this.style.borderColor='rgba(30,30,56,0.8)'">
        <div style="font-family:'Oswald',sans-serif;font-size:11px;color:rgba(96,85,255,0.6);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;">Hub</div>
        <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:15px;color:#fff;">Toutes les niches IA →</div>
      </a>
      <a href="{BASE_URL}/#apply" style="display:block;padding:18px 20px;background:linear-gradient(135deg,rgba(59,47,232,0.2),rgba(96,85,255,0.1));border:1px solid rgba(59,47,232,0.3);border-radius:12px;text-decoration:none;" onmouseover="this.style.borderColor='rgba(74,59,255,0.5)'" onmouseout="this.style.borderColor='rgba(59,47,232,0.3)'">
        <div style="font-family:'Oswald',sans-serif;font-size:11px;color:rgba(96,85,255,0.6);letter-spacing:0.1em;text-transform:uppercase;margin-bottom:4px;">Programme</div>
        <div style="font-family:'Oswald',sans-serif;font-weight:700;font-size:15px;color:#fff;">Réserver un appel →</div>
      </a>
    </div>
  </div>
</section>

<!-- CTA FINAL -->
<section style="padding:72px 24px;background:radial-gradient(ellipse 80% 60% at 50% 50%,rgba(59,47,232,0.2) 0%,transparent 70%);">
  <div style="max-width:680px;margin:0 auto;text-align:center;">
    <h2 style="font-family:'Oswald',sans-serif;font-size:clamp(28px,4vw,44px);font-weight:900;color:#fff;line-height:1.1;margin-bottom:16px;">
      Prêt à appliquer cette méthode dans les {niche_label} ?
    </h2>
    <p style="font-size:16px;color:rgba(255,255,255,0.5);line-height:1.65;margin-bottom:32px;">
      Réserve un appel de 30 minutes avec l'équipe Scaling Lab' — on valide ensemble ton profil, ta niche, et le plan d'action pour tes premiers {n['ticket_setup']} de ticket.
    </p>
    <a href="{BASE_URL}/#apply" style="display:inline-flex;align-items:center;gap:10px;background:linear-gradient(135deg,#3B2FE8,#6055FF);color:#fff;font-family:'Oswald',sans-serif;font-size:16px;font-weight:700;padding:18px 40px;border-radius:12px;text-decoration:none;letter-spacing:0.06em;text-transform:uppercase;box-shadow:0 12px 40px rgba(59,47,232,0.4);">
      Réserver mon appel gratuit
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
    </a>
    <p style="font-size:12px;color:rgba(255,255,255,0.25);margin-top:16px;">Sans engagement · Places limitées · Profil qualifié requis</p>
  </div>
</section>

<!-- FOOTER -->
<footer style="padding:40px 24px;border-top:1px solid rgba(30,30,56,0.6);">
  <div style="max-width:1100px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
    <div style="font-family:'Oswald',sans-serif;font-size:18px;font-weight:900;color:#fff;letter-spacing:-0.02em;">
      SCALING <span style="color:#6055FF;">LAB'</span>
    </div>
    <div style="font-size:12px;color:rgba(255,255,255,0.2);">
      Page ID : {gid} · {today}
    </div>
  </div>
</footer>

<script>
  function toggleFaq(btn) {{
    const answer = btn.nextElementSibling;
    btn.classList.toggle('active');
    answer.classList.toggle('open');
  }}
</script>
</body>
</html>"""

    return html


# ─── Update sitemap ────────────────────────────────────────────────────────────
def update_sitemap(new_urls):
    tree = ET.parse(SITEMAP_PATH)
    root = tree.getroot()
    ns   = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns)

    existing = {el.text.strip() for el in root.iter(f'{{{ns}}}loc')}
    added = 0
    today = date.today().isoformat()

    for url in new_urls:
        if url not in existing:
            url_el  = ET.SubElement(root, f'{{{ns}}}url')
            loc_el  = ET.SubElement(url_el, f'{{{ns}}}loc')
            loc_el.text = url
            lm_el   = ET.SubElement(url_el, f'{{{ns}}}lastmod')
            lm_el.text  = today
            pri_el  = ET.SubElement(url_el, f'{{{ns}}}priority')
            pri_el.text = '0.5'
            added  += 1

    if added:
        ET.indent(root, space='  ')
        tree.write(SITEMAP_PATH, encoding='unicode', xml_declaration=True)

    return added


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    new_urls = []
    generated = 0

    for n_slug, n in NICHES.items():
        for p_slug, p in PROBLEMATIQUES.items():
            out_dir = os.path.join(AGENCES_DIR, n_slug, p_slug)
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, "index.html")
            html = generate_page(n_slug, n, p_slug, p)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(html)
            size_kb = len(html.encode()) // 1024
            print(f"  ✓ /agences/{n_slug}/{p_slug}/ ({size_kb}KB)")
            new_urls.append(f"{BASE_URL}/agences/{n_slug}/{p_slug}/")
            generated += 1

    added = update_sitemap(new_urls)
    print(f"\nSitemap : +{added} URLs ajoutées")

    # Sauvegarde IndexNow
    iu_path = os.path.join(_dir, "indexnow_niche_prob_urls.json")
    with open(iu_path, 'w', encoding='utf-8') as f:
        json.dump(new_urls, f, ensure_ascii=False, indent=2)
    print(f"IndexNow : {generated} URLs sauvegardées → indexnow_niche_prob_urls.json")
    print(f"\nTotal : {generated} pages niche×problématique générées")


if __name__ == '__main__':
    main()
