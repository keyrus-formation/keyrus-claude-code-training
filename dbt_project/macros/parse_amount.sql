{#
  Convertit un montant texte ('1234.50' ou '1 234,50') en numérique,
  de façon portable DuckDB / Snowflake. Renvoie NULL si illisible.
#}
{% macro parse_amount(column) -%}
    {%- if target.type == 'snowflake' -%}
        try_to_number(replace(replace({{ column }}, ' ', ''), ',', '.'), 12, 2)
    {%- else -%}
        try_cast(replace(replace({{ column }}, ' ', ''), ',', '.') as decimal(12, 2))
    {%- endif -%}
{%- endmacro %}

{# Schéma personnalisé : garde les noms de schéma tels quels (staging, marts) #}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}{{ target.schema }}{%- else -%}{{ custom_schema_name | trim }}{%- endif -%}
{%- endmacro %}
