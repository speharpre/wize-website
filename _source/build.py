#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère toutes les pages HTML de wize.be à partir de _source/content.py.

Usage : python3 _source/build.py   (depuis la racine du repo)
Les pages générées sont commitées. Ne jamais éditer une page générée à la main.
"""
import os
import re
import sys
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from content import LANGS, PRIVACY, COOKIES, COMPANY, LAST_UPDATED  # noqa: E402

SITE = "https://www.wize.be"
ASSET_V = "20261017"  # incrémenter après toute modification de wize.css ou wize.js
YEAR = "2026"
ORDER = ["en", "fr", "nl"]


def icon(name):
    svg = open(os.path.join(HERE, "icons", name + ".svg"), encoding="utf-8").read().strip()
    return svg.replace("<svg ", '<svg class="icon" aria-hidden="true" focusable="false" ', 1)


def out(path, html):
    full = os.path.join(ROOT, path.strip("/"), "index.html") if not path.endswith(".html") else os.path.join(ROOT, path.strip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("  ", os.path.relpath(full, ROOT))


def alternates(key):
    links = ['<link rel="alternate" hreflang="%s" href="%s%s">' % (LANGS[l]["hreflang"], SITE, LANGS[l][key]) for l in ORDER]
    links.append('<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, LANGS["en"][key]))
    return "\n".join(links)


def head(t, key, title, description, robots="index, follow"):
    url = SITE + t[key]
    return f"""<!doctype html>
<html lang="{t['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
{alternates(key)}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Wize">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/img/og-wize.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="theme-color" content="#FAFBFC" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0A0F1A" media="(prefers-color-scheme: dark)">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="icon" href="/assets/img/icon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/geist-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/wize.css?v={ASSET_V}">
<script src="/assets/js/wize.js?v={ASSET_V}" defer></script>
"""


def header(lang, t, key, home_page):
    def nav_href(anchor):
        return anchor if home_page else t["home"] + anchor
    links = "\n".join(f'        <li><a href="{nav_href(a)}">{escape(label)}</a></li>' for a, label in t["nav"])
    langs = "\n".join(
        f'        <a href="{LANGS[l][key]}" hreflang="{LANGS[l]["hreflang"]}" lang="{LANGS[l]["html_lang"]}"'
        + (' aria-current="true"' if l == lang else "") + f'>{l.upper()}</a>'
        for l in ORDER)
    contact = nav_href(t["nav"][2][0])
    return f"""<a class="skip" href="#main">{escape(t['skip'])}</a>
<div class="top-sentinel" aria-hidden="true"></div>
<header class="site-header">
  <div class="wrap header-in">
    <a class="brand" href="{t['home']}" aria-label="Wize"><img src="/assets/img/icon-192.png" width="34" height="34" alt=""><span>WIZE</span></a>
    <button class="nav-toggle" type="button" aria-controls="nav" aria-expanded="false">
      <span class="sr-only">{escape(t['menu'])}</span>{icon('list').replace('class="icon"', 'class="icon i-open"')}{icon('x').replace('class="icon"', 'class="icon i-close"')}
    </button>
    <nav class="nav" id="nav" aria-label="Navigation">
      <ul class="nav-links">
{links}
      </ul>
      <div class="lang" role="group" aria-label="{escape(t['lang_label'])}">
{langs}
      </div>
      <a class="btn btn-primary" href="{contact}">{escape(t['cta'])}</a>
    </nav>
  </div>
</header>
"""


def footer(t):
    c = COMPANY
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="{t['home']}" aria-label="Wize"><img src="/assets/img/icon-192.png" width="30" height="30" alt="" loading="lazy"><span>WIZE</span></a>
        <p>{escape(t['footer_tagline'])}</p>
      </div>
      <div>
        <p>{c['name']}</p>
        <p>{escape(c['street'])}, {c['city']}, {escape(t['country'])}</p>
        <p>{t['vat_label']} {c['vat']}</p>
        <p>IBAN {c['iban']} (ING)</p>
      </div>
      <nav aria-label="{escape(t['footer_legal'])}">
        <ul class="footer-links">
          <li><a href="{t['privacy']}">{escape(t['privacy_label'])}</a></li>
          <li><a href="{t['cookies']}">{escape(t['cookies_label'])}</a></li>
          <li><a href="mailto:{c['email']}">{c['email']}</a></li>
        </ul>
      </nav>
    </div>
    <p class="footer-bottom">&copy; {YEAR} Wize.be. {escape(t['rights'])}</p>
  </div>
</footer>
</body>
</html>
"""


def home(lang):
    t = LANGS[lang]
    c = COMPANY
    a_id, s_id, c_id = (x[0][1:] for x in t["nav"])
    pillars = "\n".join(
        f"""        <li class="pillar c-{color} reveal d{i}">
          <span class="pillar-ico">{icon(ic)}</span>
          <div><strong>{escape(name)}</strong><span>{escape(desc)}</span></div>
        </li>""" for i, (ic, color, name, desc) in enumerate(t["pillars"]))
    cards = []
    for i, (ic, title, body, offers) in enumerate(t["services"]):
        cls = ["card card-lg", "card card-emerald", "card card-magenta"][i]
        lis = "\n".join(f"            <li>{icon('check')}<span>{escape(o)}</span></li>" for o in offers)
        cards.append(f"""        <article class="{cls} reveal d{i}">
          <span class="card-ico">{icon(ic)}</span>
          <h3>{escape(title)}</h3>
          <p>{escape(body)}</p>
          <ul class="offers">
{lis}
          </ul>
        </article>""")
    body_paras = "\n".join(f"        <p class=\"lead\">{escape(p)}</p>" for p in t["approach_body"])
    ld = ('{"@context":"https://schema.org","@type":"ProfessionalService","name":"Wize","legalName":"WIZE SRL",'
          f'"url":"{SITE}{t["home"]}","logo":"{SITE}/assets/img/icon-512.png","email":"{c["email"]}","telephone":"{c["phone_href"]}",'
          '"vatID":"BE0691653847","address":{"@type":"PostalAddress","streetAddress":"All\\u00e9e des Chanterelles 14B",'
          '"postalCode":"5101","addressLocality":"Erpent","addressCountry":"BE"}}')
    html = head(t, "home", t["title"], t["description"])
    html += f'<script type="application/ld+json">{ld}</script>\n</head>\n<body>\n'
    html += header(lang, t, "home", True)
    html += f"""<main id="main">
  <section class="hero">
    <div class="wrap hero-grid">
      <div>
        <h1>{escape(t['hero_l1'])} <span>{escape(t['hero_l2'])}</span></h1>
        <p class="hero-sub">{escape(t['hero_sub'])}</p>
        <div class="hero-ctas">
          <a class="btn btn-primary" href="#{c_id}">{escape(t['cta'])}{icon('arrow-right')}</a>
          <a class="btn btn-ghost" href="#{s_id}">{escape(t['hero_secondary'])}</a>
        </div>
      </div>
      <div class="hero-visual">
        <picture>
          <source srcset="/assets/img/wize-mark.webp" type="image/webp">
          <img src="/assets/img/wize-mark.png" width="640" height="372" alt="{escape(t['hero_alt'])}" fetchpriority="high">
        </picture>
      </div>
    </div>
  </section>

  <section class="section approach" id="{a_id}" aria-labelledby="{a_id}-t">
    <div class="wrap approach-grid">
      <div class="reveal">
        <span class="eyebrow">{escape(t['approach_eyebrow'])}</span>
        <h2 class="section-title" id="{a_id}-t">{escape(t['approach_title'])}</h2>
{body_paras}
      </div>
      <ul class="pillars">
{pillars}
      </ul>
    </div>
  </section>

  <section class="section services" id="{s_id}" aria-labelledby="{s_id}-t">
    <div class="wrap">
      <div class="services-head reveal">
        <h2 class="section-title" id="{s_id}-t">{escape(t['services_title'])}</h2>
        <p class="lead">{escape(t['services_lead'])}</p>
      </div>
      <div class="bento">
{chr(10).join(cards)}
      </div>
    </div>
  </section>

  <section class="cta-band" aria-labelledby="band-t">
    <div class="wrap">
      <div class="cta-box reveal">
        <div>
          <h2 id="band-t">{escape(t['band_title'])}</h2>
          <p>{escape(t['band_body'])}</p>
        </div>
        <a class="btn" href="#{c_id}">{escape(t['cta'])}{icon('arrow-right')}</a>
      </div>
    </div>
  </section>

  <section class="section contact" id="{c_id}" aria-labelledby="{c_id}-t">
    <div class="wrap contact-grid">
      <div class="reveal">
        <h2 class="section-title" id="{c_id}-t">{escape(t['contact_title'])}</h2>
        <p class="lead">{escape(t['contact_body'])}</p>
      </div>
      <ul class="contact-list reveal d1">
        <li><a href="mailto:{c['email']}"><span class="ico">{icon('envelope-simple')}</span><span><span class="k">{escape(t['k_email'])}</span><span class="v">{c['email']}</span></span><span class="go">{icon('arrow-up-right')}</span></a></li>
        <li><a href="tel:{c['phone_href']}"><span class="ico">{icon('phone')}</span><span><span class="k">{escape(t['k_phone'])}</span><span class="v">{c['phone']}</span></span><span class="go">{icon('arrow-up-right')}</span></a></li>
        <li><a href="{c['maps']}" rel="noopener" target="_blank"><span class="ico">{icon('map-pin')}</span><span><span class="k">{escape(t['k_address'])}</span><span class="v">{escape(c['street'])}, {c['city']}</span></span><span class="go">{icon('arrow-up-right')}</span></a></li>
      </ul>
    </div>
  </section>
</main>
"""
    html += footer(t)
    out(t["home"], html)


def render_sections(sections, t):
    parts = []
    for title, paras in sections:
        parts.append(f"    <h2>{escape(title)}</h2>")
        for p in paras:
            if isinstance(p, list):
                parts.append("    <ul>\n" + "\n".join(f"      <li>{x}</li>" for x in p) + "\n    </ul>")
            else:
                parts.append("    <p>" + p.replace("{cookies}", t["cookies"]) + "</p>")
    return "\n".join(parts)


def legal(lang, key, data):
    t = LANGS[lang]
    title, sections = data[lang]
    html = head(t, key, f"{title} | Wize", f"{title}, WIZE SRL.", robots="noindex, follow")
    html += "</head>\n<body>\n" + header(lang, t, key, False)
    html += f"""<main id="main" class="legal">
  <div class="wrap">
    <a class="back" href="{t['home']}">{icon('arrow-right')}{escape(t['back'])}</a>
    <h1>{escape(title)}</h1>
    <p class="updated">{escape(t['updated'])} : {LAST_UPDATED[lang]}</p>
{render_sections(sections, t)}
  </div>
</main>
""".replace(" : " + LAST_UPDATED[lang], (" : " if lang == "fr" else ": ") + LAST_UPDATED[lang])
    html += footer(t)
    out(t[key], html)


def notfound():
    t = LANGS["en"]
    html = head(t, "home", "Page not found | Wize", t["nf_body"], robots="noindex")
    html = html.replace(f'<link rel="canonical" href="{SITE}/">\n', "")
    html += "</head>\n<body>\n" + header("en", t, "home", False)
    links = " ".join(f'<a class="btn {"btn-primary" if l == "en" else "btn-ghost"}" href="{LANGS[l]["home"]}" lang="{LANGS[l]["html_lang"]}">{escape(LANGS[l]["back"])}</a>' for l in ORDER)
    html += f"""<main id="main" class="notfound">
  <div class="wrap">
    <h1>{escape(t['nf_title'])}</h1>
    <p>{escape(t['nf_body'])}<br><span lang="fr">{escape(LANGS['fr']['nf_body'])}</span><br><span lang="nl">{escape(LANGS['nl']['nf_body'])}</span></p>
    <div class="hero-ctas center">{links}</div>
  </div>
</main>
"""
    html += footer(t)
    out("404.html", html)


def sitemap():
    urls = []
    for l in ORDER:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{LANGS[x]["hreflang"]}" href="{SITE}{LANGS[x]["home"]}"/>' for x in ORDER)
        urls.append(f'  <url><loc>{SITE}{LANGS[l]["home"]}</loc>{alts}</url>')
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + "\n".join(urls) + "\n</urlset>\n")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(xml)
    print("   sitemap.xml")


def check_dashes():
    bad = []
    for dirpath, _, files in os.walk(ROOT):
        if any(p in dirpath for p in (".git", "_source", "docs", "node_modules")):
            continue
        for f in files:
            if f.endswith(".html"):
                s = open(os.path.join(dirpath, f), encoding="utf-8").read()
                if re.search("[–—]", s):
                    bad.append(os.path.join(dirpath, f))
    if bad:
        sys.exit("Tiret cadratin trouvé dans : " + ", ".join(bad))


if __name__ == "__main__":
    print("Génération :")
    for l in ORDER:
        home(l)
        legal(l, "privacy", PRIVACY)
        legal(l, "cookies", COOKIES)
    notfound()
    sitemap()
    check_dashes()
    print("OK")
