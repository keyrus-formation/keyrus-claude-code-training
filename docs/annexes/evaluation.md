# Évaluation

## Quiz de fin de formation (10 questions, 10 min)

1. **Quelle est la principale différence entre un agent comme Claude Code et un assistant conversationnel ?**
   a) Il utilise un meilleur modèle · b) **Il agit en boucle : collecte du contexte, actions avec des outils, vérification** · c) Il n'envoie pas de données au cloud · d) Il ne se trompe pas
2. **Une règle doit s'appliquer à 100 % (« ne jamais modifier `data/raw/` »). Où la mettre ?**
   a) `CLAUDE.md` · b) Un skill · c) **Une permission `deny` ou un hook `PreToolUse`** · d) Le prompt
3. **Dans quel mode Claude explore-t-il et propose-t-il un plan sans modifier de fichier ?**
   a) `acceptEdits` · b) **`plan`** · c) `dontAsk` · d) `bypassPermissions`
4. **Vous passez d'une correction de bug à une tâche de documentation sans rapport. Le bon geste ?**
   a) Continuer · b) **`/clear`** · c) Changer de modèle · d) Redémarrer l'ordinateur
5. **Un modèle dbt joint les paiements aux commandes et le test `unique` sur `order_id` échoue. Cause la plus probable ?**
   a) Un bug de dbt · b) **Un fan-out : plusieurs paiements par commande, à agréger avant la jointure** · c) Un `NULL` dans `order_id` · d) Un problème de droits
6. **Claude propose de corriger un test en échec en modifiant l'assertion du test. Que faites-vous ?**
   a) J'accepte si la CI passe · b) **Je refuse tant que je n'ai pas établi que le test était faux ; sinon on corrige le code** · c) Je supprime le test · d) J'ajoute un `try/except`
7. **Que contient idéalement un `CLAUDE.md` de projet ?**
   a) La description de chaque fichier · b) **Commandes de build/test, conventions, pièges métier, interdits** · c) Les identifiants de connexion · d) L'historique des sessions
8. **Pour du code client, quel type de compte utiliser ?**
   a) Mon compte Pro personnel · b) **Un compte commercial (Team/Enterprise, API ou cloud), sans entraînement sur les données par défaut** · c) N'importe lequel · d) Un compte gratuit
9. **Quel levier réduit le plus la consommation sur une longue session ?**
   a) Écrire en anglais · b) **Garder le contexte petit : `/clear`, `CLAUDE.md` court, skills à la demande, subagents pour les sorties verbeuses** · c) Désactiver les tests · d) Utiliser toujours Opus
10. **Dans GitHub Actions, comment rendre une relecture automatique de PR sûre et maîtrisée ?**
   a) `bypassPermissions` · b) **Liste blanche d'outils (`--allowedTools`), `--max-turns`, timeout, secret dans les secrets GitHub, revue humaine finale** · c) Clé API dans le workflow · d) Laisser Claude fusionner la PR

Réponses : 1b · 2c · 3b · 4b · 5b · 6b · 7b · 8b · 9b · 10b (mélanger l'ordre des réponses avant distribution).

## Grille d'évaluation du cas pratique (sur 20)

| Critère | Points | Attendu |
| --- | --- | --- |
| Cadrage | 3 | Hypothèses écrites (date de référence, statuts, fenêtre de 365 jours, grain), questions pertinentes au métier |
| Plan | 2 | Plan Mode utilisé, plan validé avant implémentation, tests prévus |
| Exactitude du modèle dbt | 4 | Seuil VIP, annulées exclues, dates futures ignorées, résultat reproductible (pas de `current_date`), pas de fan-out |
| Tests | 3 | Clé `unique`/`not_null`, test de la règle métier, tests pytest de l'export |
| Confidentialité | 3 | Email pseudonymisé après normalisation, aucune donnée personnelle en clair dans l'export ni dans la conversation |
| Livraison | 3 | Commits propres, relecture indépendante, PR décrite (dont usage de Claude), CI verte |
| Retour d'expérience | 2 | Coût relevé, amélioration concrète de `CLAUDE.md` ou d'un skill |
