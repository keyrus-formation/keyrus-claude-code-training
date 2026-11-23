# J4 — Industrialiser et livrer

---

## Exercice 4.1 — De la branche à la PR relue (20 min)

À partir de votre branche de corrections de J3 :

1. Vérifiez que chaque correctif est dans un commit séparé, au format `type(scope): message` (sinon : faites réorganiser l'historique par Claude, **sur votre branche uniquement**).
2. « Utilise le subagent data-reviewer pour relire mes changements. » Traitez les remarques bloquantes.
3. Lancez aussi `/security-review` : qu'est-ce qui est vérifié ?
4. Faites rédiger la description de PR (contexte, cause, correctif, impact chiffré, tests, usage de Claude Code) puis **relisez-la et corrigez-la vous-même**.
5. Créez la PR avec `gh pr create`. Attendez la CI. Si la relecture automatique de Claude commente, répondez-lui avec `@claude` dans la PR.

---

## Exercice 4.2 — Cas pratique de bout en bout (95 min, binômes)

> La direction commerciale de RetailCo veut identifier chaque mois les **clients à risque de départ** pour déclencher une campagne de rétention.
> Un client est « à risque » s'il n'a passé aucune commande depuis plus de **90 jours** (**60 jours** pour les VIP), alors qu'il a passé
> **au moins 2 commandes** dans les 12 mois précédents.
> Livrables : une table dbt exploitable par l'équipe BI, et un export CSV quotidien pour l'outil CRM **sans donnée personnelle en clair**.

### Jalons

| # | Jalon | Livrable | ✔ |
| --- | --- | --- | --- |
| 1 | **Cadrage** (10 min) — posez vos questions au métier (le formateur) | `docs/cas_pratique.md` : hypothèses, définitions, date de référence, grain | |
| 2 | **Exploration et plan** (15 min) — Plan Mode | Plan validé par le formateur : modèles réutilisés, fichiers créés, tests | |
| 3 | **Modèle dbt** (25 min) | `marts/mart_customers_at_risk.sql` + YAML (grain, tests) ; `dbt build` vert | |
| 4 | **Export Python** (20 min) | `src/retail_pipeline/export_at_risk.py` + tests ; identifiant client pseudonymisé | |
| 5 | **Livraison** (15 min) | Branche, relecture `data-reviewer`, PR décrite, CI verte | |
| 6 | **Bilan** (5 min) | Relevé `/usage` ; une ligne ajoutée au `CLAUDE.md` ou un skill proposé | |

### Exigences

- Le résultat doit être **reproductible** : même entrée, même date de référence → même sortie.
- Les commandes annulées et les dates futures ne doivent pas fausser le calcul.
- Aucun nom ni email en clair dans l'export ; aucune donnée client affichée en entier dans la conversation.
- Tests : au minimum `unique`/`not_null` sur la clé, un test de la règle métier, des tests pytest de l'export.

### Restitution (5 min par binôme)

Votre plan initial, ce que Claude a bien fait, ce que vous avez dû corriger, le coût de la session, ce que vous changeriez dans le `CLAUDE.md` ou les skills du projet.
