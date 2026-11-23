-- Environnement Snowflake de la formation Claude Code (à exécuter par un administrateur).
-- Principes : moindre privilège, coûts plafonnés, un schéma de travail par participant,
-- aucune donnée client réelle (uniquement le jeu fictif RetailCo).

USE ROLE ACCOUNTADMIN;

-- 1. Plafond de coût : le moniteur suspend l'entrepôt à 100 % du quota
CREATE OR REPLACE RESOURCE MONITOR TRAINING_RM
  WITH CREDIT_QUOTA = 20
  FREQUENCY = MONTHLY
  START_TIMESTAMP = IMMEDIATELY
  TRIGGERS ON 75 PERCENT DO NOTIFY
           ON 100 PERCENT DO SUSPEND;

-- 2. Entrepôt minimal, suspendu après 60 s d'inactivité
CREATE OR REPLACE WAREHOUSE TRAINING_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE
  RESOURCE_MONITOR = TRAINING_RM;

-- 3. Base et schéma des données brutes (lecture seule pour les participants)
CREATE DATABASE IF NOT EXISTS RETAILCO;
CREATE SCHEMA IF NOT EXISTS RETAILCO.RAW;

-- 4. Rôle de formation
USE ROLE SECURITYADMIN;
CREATE ROLE IF NOT EXISTS TRAINING_ROLE;
GRANT USAGE ON WAREHOUSE TRAINING_WH TO ROLE TRAINING_ROLE;
GRANT USAGE ON DATABASE RETAILCO TO ROLE TRAINING_ROLE;
GRANT USAGE ON SCHEMA RETAILCO.RAW TO ROLE TRAINING_ROLE;
GRANT SELECT ON ALL TABLES IN SCHEMA RETAILCO.RAW TO ROLE TRAINING_ROLE;
GRANT SELECT ON FUTURE TABLES IN SCHEMA RETAILCO.RAW TO ROLE TRAINING_ROLE;
-- Les participants créent leurs schémas DEV_<NOM> (cible dbt « snowflake »)
GRANT CREATE SCHEMA ON DATABASE RETAILCO TO ROLE TRAINING_ROLE;

-- 5. Un utilisateur par participant (répéter ; préférer SSO ou paire de clés si disponible)
-- CREATE USER TRAINEE_01 PASSWORD = '<généré>' DEFAULT_ROLE = TRAINING_ROLE
--   DEFAULT_WAREHOUSE = TRAINING_WH MUST_CHANGE_PASSWORD = TRUE;
-- GRANT ROLE TRAINING_ROLE TO USER TRAINEE_01;

-- 6. Chargement des données brutes : depuis un poste formateur
--    python scripts/generate_data.py && python -m retail_pipeline.pipeline --target snowflake
--    (avec un rôle disposant du droit CREATE TABLE sur RETAILCO.RAW)

-- 7. Nettoyage après la formation
-- DROP DATABASE RETAILCO; DROP WAREHOUSE TRAINING_WH; DROP RESOURCE MONITOR TRAINING_RM;
-- DROP ROLE TRAINING_ROLE;  (+ DROP USER TRAINEE_xx)
