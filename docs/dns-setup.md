# wize.be : configuration DNS

Registre : DNS Belgium (.be). **Registrar et DNS : OVH** (serveurs `dns18.ovh.net`, `ns18.ovh.net`, DNSSEC actif).
Les e-mails sont chez Microsoft 365 : ne jamais toucher aux enregistrements MX, SPF, `autodiscover`.

## Pourquoi pas la redirection OVH

La « redirection web » d'OVH renvoie `wize.be` vers `www` depuis les serveurs d'hébergement OVH
(`cluster123.hosting.ovh.net`), qui présentent leur propre certificat, pas celui de `wize.be` :
d'où l'erreur de certificat. Solution retenue : les deux noms pointent directement vers Azure,
qui émet et renouvelle gratuitement un certificat pour chacun, puis Azure redirige `wize.be`
vers `www.wize.be` (domaine par défaut).

OVH ne propose pas d'enregistrement ALIAS/ANAME à la racine. On utilise donc un enregistrement `A`
vers l'IP stable de la Static Web App (méthode documentée par Microsoft). Seule contrepartie :
le domaine nu est servi depuis la région West Europe au lieu du réseau mondial, sans impact pour
un site belge, et la redirection vers `www` renvoie ensuite sur le réseau mondial.

## Zone OVH cible

| Sous-domaine | Type | Cible | Action |
|---|---|---|---|
| *(vide)* `wize.be` | A | `137.74.229.68` | **supprimer** (ancien WordPress OVH) |
| *(vide)* `wize.be` | AAAA | `2001:41d0:301:10::23` | **supprimer** (sinon les clients IPv6 tombent sur OVH) |
| `www` | A / AAAA / CNAME existants | OVH | **supprimer** |
| *(vide)* `wize.be` | A | `20.8.132.166` | **ajouter** (IP stable de `wize-web`) |
| `www` | CNAME | `happy-field-07b824603.6.azurestaticapps.net.` | **ajouter** |
| `_dnsauth` | TXT | `_uggruqrxwqowdy5yzpofwrnmx4olphr` | **ajouter** (validation `wize.be`) |
| `_dnsauth.www` | TXT | `_flfde94kvbf014exjsxz73sbhecbcf9` | **ajouter** (validation `www.wize.be`) |
| `ftp` | CNAME | `wize.be.` | supprimer (plus de FTP) |

Dans le Manager OVH, onglet **Redirection** du domaine : supprimer toute redirection web existante
(elle crée elle-même des enregistrements A vers OVH).

Les codes TXT expirent après quelques jours. S'ils ont expiré, en regénérer :

```bash
az staticwebapp hostname set -n wize-web -g rg-wize-prod --subscription 09d4272a-aebe-460c-8431-90d8d3c808b2 --hostname wize.be --validation-method dns-txt-token --no-wait
az staticwebapp hostname show -n wize-web -g rg-wize-prod --subscription 09d4272a-aebe-460c-8431-90d8d3c808b2 --hostname wize.be --query validationToken -o tsv
```

## Après propagation (quelques minutes à quelques heures)

1. Vérifier : `az staticwebapp hostname list -n wize-web -g rg-wize-prod --subscription 09d4272a-aebe-460c-8431-90d8d3c808b2 -o table` : les deux noms en `Ready`.
2. Portail Azure, `wize-web` > **Custom domains** > `www.wize.be` > **Set default** : `wize.be` redirige alors en 301 vers `https://www.wize.be`.
3. Les TXT `_dnsauth` peuvent rester (inoffensifs) ou être supprimés après validation.
4. Contrôle : `curl -sI https://wize.be` (301 vers www) et `curl -sI https://www.wize.be` (200).
