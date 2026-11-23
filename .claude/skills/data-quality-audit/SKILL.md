---
name: data-quality-audit
description: Audite la qualité d'une table ou d'un fichier de données (nulls, doublons, valeurs hors domaine, dates futures, intégrité référentielle) et propose des tests. Use when the user asks to profile, audit or check the quality of a dataset.
argument-hint: "[table ou fichier]"
context: fork
agent: Explore
---

# Audit de qualité de données

Cible : $ARGUMENTS

Tu travailles en **lecture seule**. N'affiche jamais plus de 20 lignes de données brutes :
les données clients sont confidentielles, préfère des agrégats (comptes, min/max, distributions).

## Profilage

Pour chaque colonne, calcule avec DuckDB (`python -c "import duckdb; …"` sur `data/retail.duckdb`
ou directement sur le CSV avec `read_csv_auto`) :
- type inféré, nombre de valeurs nulles ou vides, nombre de valeurs distinctes ;
- pour les numériques : min, max, nombre de valeurs négatives ;
- pour les dates : min, max, nombre de dates dans le futur ;
- pour les textes : formats atypiques (ex. montants `1 234,50`, emails en majuscules).

## Contrôles métier

- unicité de la clé présumée (et si doublons : sont-ils exacts ou des versions successives ?) ;
- intégrité référentielle vers les tables liées ;
- cohérence entre tables (ex. somme des paiements vs montant de la commande).

## Restitution

Un tableau Markdown : `colonne | problème | nb lignes | sévérité (bloquant / à surveiller) | test proposé`,
puis le YAML dbt (`data_tests`) ou les fonctions Python (`retail_pipeline/quality.py`) correspondants.
