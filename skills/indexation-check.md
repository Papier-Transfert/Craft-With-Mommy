# Skill: Indexation Check

Documentation du système de suivi d'indexation. Le système tourne en
**automatique chaque nuit** via cron — ce skill n'est PAS appelé par le cron
quotidien (qui n'utilise pas Claude). Il sert de manuel pour les interventions
manuelles ou les debug.

## Quand utiliser ce skill

- Tu (Claude) es invoqué manuellement pour debug un comportement du système.
- Tu dois faire un run forcé d'inspection sur quelques URLs.
- Tu dois investiguer un problème remonté dans `indexation/report.md`.
- Tu dois mettre à jour manuellement `state.json` (ex: marquer une URL comme
  indexée après vérification GSC).

## Architecture rapide

- **Script principal** : `tools/check_indexation.py` (Python pur, pas de
  dépendance à Claude).
- **Cron** : `/home/claudeuser/run_indexation.sh` lancé à 03:00 UTC.
- **Mémoire** : `indexation/state.json` (versionnée Git).
- **Rapport** : `indexation/report.md` (versionné Git).
- **Détails complets** : voir `indexation/README.md`.

## Commandes utiles

```bash
# Test sans effet (dry-run)
python3 /var/www/craft-with-mommy/tools/check_indexation.py --dry-run

# Run réel limité à N URLs (ex: test rapide)
python3 /var/www/craft-with-mommy/tools/check_indexation.py --limit 3

# Run réel complet (10 URLs)
python3 /var/www/craft-with-mommy/tools/check_indexation.py

# Inspecter le log
tail -100 /home/claudeuser/logs/indexation-agent.log

# Voir l'état actuel
jq '.stats' /var/www/craft-with-mommy/indexation/state.json
jq '.articles | to_entries | map(select(.value.problem != null)) | length' \
  /var/www/craft-with-mommy/indexation/state.json
```

## Règles

- Ne **jamais** soumettre la même URL plus d'une fois par jour à l'Indexing API
  (le script gère ça via `indexing_api_last_push`).
- Ne **jamais** committer `tools/gsc-credentials.json` — il est dans
  `.gitignore`, vérifier après chaque PR.
- Si `state.json` est mis à jour à la main, conserver le format JSON valide et
  pretty-printed avec `json.dumps(..., indent=2, ensure_ascii=False)`.
- Les commits du système se font automatiquement par le wrapper avec le message
  `"Indexation report YYYY-MM-DD"`. Si tu fais une modif manuelle, utiliser un
  message différent pour distinguer.

## Quotas et caps

- **Google Indexing API** : 200 req/jour (quota Google), on s'autoplafonne à
  **5/jour** par sécurité.
- **IndexNow** : pas de quota, mais on respecte le rythme d'1 push/URL/jour
  pour rester poli.
- **HTTP requests** locales (les checks `requests.get`) : aucune limite.

## Diagnostiquer un échec

Si le log montre une erreur Indexing API du type `403 Failed to verify URL
ownership` :
1. Vérifier que `tools/gsc-credentials.json` existe et est valide.
2. Vérifier que le fichier `google33a09ddb235ab1ad.html` est toujours servi à
   la racine du site (Google peut révoquer la vérification si le fichier
   disparaît).
3. Re-vérifier la propriété via le script Node de `C:\Users\t1del\sa-test\` si
   disponible.

Si IndexNow échoue avec une 422 ou 403 :
1. Vérifier que `https://www.craft-with-mommy.com/{key}.txt` retourne 200 avec
   la clé en clair.
2. La clé dans `indexation/indexnow.key` doit correspondre au nom du fichier
   `.txt` à la racine du site.
