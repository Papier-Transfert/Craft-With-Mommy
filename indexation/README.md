# Indexation Tracking System

Système de suivi et accélération d'indexation Google pour craft-with-mommy.com.

## Vue d'ensemble

Un script Python (`tools/check_indexation.py`) tourne automatiquement chaque
nuit à **03:00 UTC** sur Hetzner. Il fait deux choses :

1. **Monitoring** — pour 10 articles par jour : vérifie HTTP 200, absence de
   `noindex`, canonical correct, présence dans le sitemap. Maintient le suivi
   dans `state.json`.

2. **Accélération d'indexation** — pour les articles techniquement propres :
   soumission à **Google Indexing API** (cap 5/jour) et **IndexNow** (Bing,
   Yandex).

L'agent n'utilise plus le quota Anthropic — c'est du Python pur, pas de Claude
dans le cron.

## Fichiers

- `state.json` — source de vérité. 1 entrée par URL avec son historique de
  checks et de pushes. Mis à jour à chaque run.
- `report.md` — rapport humain regénéré à chaque run. Stats globales + URLs
  traitées du jour + URLs avec problèmes + URLs à inspecter manuellement dans
  Google Search Console.
- `indexnow.key` — clé partagée IndexNow (Bing/Yandex). Copie également
  déployée à la racine du site sous `https://www.craft-with-mommy.com/{key}.txt`.

## Sélection des 10 URLs par run

Priorité décroissante :

1. URLs jamais traitées (rattrapage du backlog initial).
2. URLs marquées `gsc_indexed = "no"` ou `"unknown"` et `last_checked > 7 jours`.
3. URLs marquées `gsc_indexed = "yes"` et `last_checked > 60 jours` (sanity
   rotation).

## Limitation connue — état d'indexation Google

L'API Google Search Console URL Inspection est bloquée pour ce Service Account
(limitation côté Google ACL, indépendante du site). L'agent ne peut donc pas
vérifier automatiquement si une URL est indexée par Google.

→ Le rapport `report.md` génère pour chaque URL un **lien direct vers
l'inspection GSC web UI**. Tu cliques, GSC répond en 2 secondes si l'URL est
indexée ou pas. Tu peux mettre à jour `state.json` manuellement (champ
`gsc_indexed: "yes"`) une fois la vérification faite, ou laisser `unknown`.

## Exécution manuelle

```bash
# Run normal (10 URLs)
python3 tools/check_indexation.py

# Test sans appels API ni écritures
python3 tools/check_indexation.py --dry-run

# Limiter à N URLs
python3 tools/check_indexation.py --limit 3
```

Le wrapper bash `/home/claudeuser/run_indexation.sh` (sur Hetzner uniquement,
hors repo) gère le lock, le log, et le commit/push automatique.

## Setup requis (déjà fait)

- Service Account Google `craft-indexation-agent@craft-with-mommy-blog-images.iam.gserviceaccount.com`
  vérifié comme propriétaire du site via Site Verification API.
- Clé JSON du SA déposée à `tools/gsc-credentials.json` (gitignored).
- APIs activées : Indexing API + Site Verification API + (Search Console API,
  partiellement utilisable).
- Fichier de vérification Google `google33a09ddb235ab1ad.html` à la racine.
- Fichier IndexNow `{key}.txt` à la racine (déployé sur Vercel).
