"""Rapport mensuel du chiffre d'affaires par catégorie (remplace legacy_report.py).

Même résultat que l'historique, calculé en une requête DuckDB vectorisée
(≈ 90 s → < 1 s sur le jeu de formation).

    python -m retail_pipeline.monthly_report data/raw
"""

from __future__ import annotations

import argparse
from pathlib import Path

import duckdb
import pandas as pd

QUERY = """
with raw_orders as (
    select *, row_number() over () as file_row
    from read_csv('{raw}/orders.csv', all_varchar = true, header = true)
),
orders as (                           -- comme l'historique : 1re occurrence dans le fichier
    select order_id, status, order_ts
    from raw_orders
    qualify row_number() over (partition by order_id order by file_row) = 1
)
select
    substr(o.order_ts, 1, 7)                                    as mois,
    p.category                                                  as categorie,
    round(sum(cast(l.quantity as integer) * cast(l.unit_price as double)), 2) as ca
from read_csv('{raw}/order_lines.csv', all_varchar = true, header = true) l
join orders o using (order_id)
join read_csv('{raw}/products.csv', all_varchar = true, header = true) p using (product_id)
where o.status <> 'cancelled'
group by 1, 2
order by 1, 2
"""


def monthly_revenue_by_category(raw_dir: Path) -> pd.DataFrame:
    """CA mensuel par catégorie, commandes annulées exclues."""
    return duckdb.sql(QUERY.format(raw=Path(raw_dir).as_posix())).df()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("raw_dir", type=Path)
    print(monthly_revenue_by_category(ap.parse_args().raw_dir).to_string(index=False))


if __name__ == "__main__":
    main()
