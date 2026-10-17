# wize.be : règles pour Claude

Site vitrine **statique** (HTML/CSS/JS, sans framework) de WIZE SRL, hébergé sur Azure Static Web Apps (plan Free).
Tout push sur `main` est publié en production par GitHub Actions (`.github/workflows/deploy.yml`) en ~1 minute.

## Structure

- Pages **générées** par `_source/build.py` à partir de `_source/content.py` (textes EN/FR/NL) :
  `index.html` (EN), `fr/`, `nl/`, pages légales (`privacy-policy/`, `cookie-policy/`, `fr/vie-privee/`,
  `fr/cookies/`, `nl/privacy/`, `nl/cookies/`), `404.html`, `sitemap.xml`.
  Pour un texte : modifier `_source/content.py`, lancer `python3 _source/build.py`, commiter les pages régénérées.
  La CI refuse un push dont les pages ne sont pas à jour.
- `assets/css/wize.css`, `assets/js/wize.js`, `assets/fonts/` (Geist auto-hébergée), `assets/img/`.
- `_source/icons/` : icônes Phosphor (regular) insérées en SVG inline par le build.
- `staticwebapp.config.json` : en-têtes de sécurité (CSP stricte, aucun script ni style inline),
  cache, redirections des anciennes URL WordPress, page 404.

## Règles

- Pas de framework, de bundler ni de `package.json` sans accord de Stéphane.
- Aucune ressource externe (CDN, Google Fonts, analytics) : la CSP les bloque. Aucun attribut `style=""` ni script inline.
- Après modification de `wize.css` ou `wize.js` : incrémenter `ASSET_V` dans `_source/build.py` (cache immuable d'un an).
- Toute modification de texte dans les **trois langues**. Aucun tiret cadratin (le build échoue s'il en trouve).
- Mobile-first, vérifier à ~375 px et en desktop, en thème clair ET sombre (`python3 -m http.server 4321`).
- Accessibilité : un seul `<h1>` par page, contrastes AA, focus visibles.
- Aucun secret dans le repo. Ne pas modifier `.github/workflows/` ni les enregistrements DNS sans accord.

Infra : `docs/infrastructure-inventory.md`. DNS : `docs/dns-setup.md`.
