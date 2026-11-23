# J1 — Prise en main de Claude Code

Prérequis : le README est déroulé jusqu'au `dbt build` (1 test en échec attendu). Travaillez en mode `default` (Manual).

---

## Exercice 1.1 — Premier contact avec RetailCo (30 min)

1. Lancez `claude` à la racine du dépôt. Vérifiez avec `/status` (ou les informations affichées au démarrage) le modèle et le dossier.
2. Posez ces questions **sans rien expliquer d'autre** et observez quels fichiers Claude ouvre :
   - « Que fait ce projet ? Donne l'architecture en 5 lignes. »
   - « Quelles sont les sources de données et combien de lignes contient chacune ? »
   - « Lance les tests unitaires et le `dbt build`, puis résume les résultats. »
3. Demandez : « lis le fichier .env ». Que se passe-t-il ? Pourquoi ? (indice : `.claude/settings.json`)
4. Faites défiler les modes avec `Maj+Tab`. Notez le nom de chaque mode.
5. Tapez `/context` : qu'est-ce qui occupe déjà la fenêtre de contexte ?

À noter pour le débrief : une chose qui vous a surpris, une chose qui vous inquiète.

🚀 Pour aller plus loin : `claude -p "combien de modèles dbt contient ce projet ?" --output-format json` — à quoi pourrait servir ce mode ?

---

## Exercice 1.2 — Réécrire des prompts (15 min)

Réécrivez chaque prompt selon la grille **Contexte → Objectif → Contraintes → Vérification**, testez les deux versions (avec `/clear` entre chaque) et comparez le nombre d'actions et le résultat.

| Prompt faible | Votre version |
| --- | --- |
| « Ajoute des tests. » | |
| « Le pipeline est lent, optimise. » | |
| « Fais un modèle dbt pour les ventes par produit. » | |

Ne commitez rien : `git checkout .` pour annuler après l'exercice (ou `Échap` ×2 → revenir en arrière).

---

## Exercice 1.3 — Écrire le `CLAUDE.md` du projet (30 min)

1. Lancez `/init` et lisez le `CLAUDE.md` généré.
2. Interrogez Claude sur les **données** (pas sur le code) pour trouver ce que `/init` ne pouvait pas deviner, par exemple :
   - « Quels formats de montants trouve-t-on dans `data/raw/orders.csv` ? Donne des comptes, pas des lignes. »
   - « Un `order_id` peut-il apparaître plusieurs fois dans `orders.csv` ? Pourquoi ? »
   - « Combien de paiements par commande au maximum ? »
   - « Que signifie `FX_TO_EUR` dans `config.py` ? »
3. Ajoutez au `CLAUDE.md` une section **« Pièges métier »** et une section **« Sécurité »**. Restez sous 80 lignes.
4. Test : `/clear`, puis « comment dois-je joindre les paiements aux commandes ? ». La réponse utilise-t-elle votre `CLAUDE.md` ?
5. Créez un `CLAUDE.local.md` avec une préférence personnelle (ex. « réponds en français, sois concis ») et vérifiez qu'il est bien ignoré par Git.

---

## Exercice 1.4 — Plan Mode (15 min)

Fonctionnalité : ajouter au pipeline une option `--since AAAA-MM-JJ` qui ne charge que les commandes passées à partir de cette date.

1. Passez en Plan Mode (`Maj+Tab`).
2. Demandez un plan : fichiers impactés, tests à écrire, cas limites (date invalide, date future, format).
3. **Faites valider le plan par votre voisin** et amendez-le au moins une fois.
4. Sortez du Plan Mode et faites implémenter, test compris. Vérifiez avec `pytest -q`.
5. Relisez le diff (`git diff`). Tout ce qui a changé était-il prévu dans le plan ?
