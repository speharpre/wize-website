# wize.be : inventaire infrastructure

Site vitrine statique (HTML/CSS/JS, sans framework) de WIZE SRL. Remplace le WordPress hébergé chez OVH.

## Azure

Tenant WIZE `6a608c76-405f-4bf8-93ca-2597c642540a`.
Souscription : **Microsoft Partner Network** `09d4272a-aebe-460c-8431-90d8d3c808b2`.
(La souscription « Microsoft Azure (wizecloud) » `6105a567-…` est gelée pour inactivité : rien n'y est créé.)

| Ressource | Nom | Groupe | Détail |
|---|---|---|---|
| Static Web App | `wize-web` | `rg-wize-prod` | **Free** (0 €), westeurope, `happy-field-07b824603.6.azurestaticapps.net`, IP stable `20.8.132.166` |

Limites du plan Free : 2 domaines personnalisés (utilisés : `wize.be`, `www.wize.be`), 250 Mo, 100 Go de bande
passante/mois, pas de SLA. Passage au plan Standard possible depuis le portail (*Hosting plan*) sans redéploiement.

## GitHub

- Repo : `speharpre/wize-website` (public), branche `main`.
- Secret Actions : `AZURE_STATIC_WEB_APPS_API_TOKEN` (jeton de déploiement de `wize-web`).
  Rotation : `az staticwebapp secrets reset-api-key -n wize-web -g rg-wize-prod --subscription 09d4272a-aebe-460c-8431-90d8d3c808b2`,
  puis `gh secret set AZURE_STATIC_WEB_APPS_API_TOKEN -R speharpre/wize-website` avec la nouvelle valeur.

## DNS et e-mail

Registrar et DNS : OVH. E-mail : Microsoft 365 (MX `wize-be.mail.protection.outlook.com`). Voir `docs/dns-setup.md`.

## Ancien site

WordPress OVH (`cluster123.hosting.ovh.net`, IP `137.74.229.68`). À résilier chez OVH une fois le nouveau site
en ligne sur les deux domaines (garder le nom de domaine et la zone DNS chez OVH).

## Monitoring

Échec de déploiement = e-mail GitHub Actions. Pas de backend, donc pas de health-check.
