---
name: sql-review
description: Relit une requête SQL ou un modèle dbt et signale les bugs de logique, problèmes de performance Snowflake et écarts aux conventions. Use when the user asks to review, audit or optimize SQL.
argument-hint: "[fichier.sql]"
disable-model-invocation: true
---

# Revue SQL

Fichier à relire : $ARGUMENTS

Diff récent sur ce fichier :
!`git diff HEAD -- $ARGUMENTS 2>/dev/null | head -200`

Vérifie, dans cet ordre, et cite chaque fois la ligne concernée :

1. **Exactitude** : grain du résultat, *fan-out* des jointures, `left join` filtré dans le `where`
   (qui devient un `inner join`), `count(*)` vs `count(distinct)`, gestion des `null`
   (`<>` exclut les null), dédoublonnage (version la plus récente ?), fuseaux horaires.
2. **Performance Snowflake** : sous-requêtes corrélées, `select *` sur de grosses tables,
   fonctions sur colonnes filtrées (empêche le pruning), `order by` inutile, `distinct` qui masque un bug de jointure,
   jointures non équi-jointures.
3. **Lisibilité** : CTE nommées, alias explicites, pas de nombres magiques, commentaires sur les règles métier.
4. **Sécurité** : pas d'identifiants en dur, pas de données personnelles exposées inutilement.

Restitue un tableau `sévérité | ligne | problème | correction proposée`, puis la requête corrigée.
Ne modifie pas le fichier sans accord explicite.
