"""Export CRM des clients à risque (cas pratique J4), sans donnée personnelle en clair.

    python -m retail_pipeline.export_at_risk --out exports/clients_a_risque.csv
"""

from __future__ import annotations

import argparse
import hashlib
import logging
from pathlib import Path

import duckdb
import pandas as pd

from .config import WAREHOUSE_PATH

log = logging.getLogger(__name__)

EXPORT_COLUMNS = ["customer_key", "segment", "days_since_last_order",
                  "orders_last_12m", "revenue_last_12m"]


def pseudonymize_email(email: str | None) -> str | None:
    """SHA-256 de l'email normalisé (minuscules, sans espaces). None si email absent."""
    if email is None or pd.isna(email):
        return None
    normalized = str(email).strip().lower()
    if not normalized:
        return None
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def build_export(at_risk: pd.DataFrame) -> pd.DataFrame:
    """Filtre les clients à risque et ne garde que les colonnes autorisées."""
    df = at_risk.loc[at_risk["is_at_risk"].astype(bool)].copy()
    df["customer_key"] = df["email"].map(pseudonymize_email)
    missing = int(df["customer_key"].isna().sum())
    if missing:
        log.warning("%d clients à risque sans email : exclus de l'export CRM", missing)
    df = df.dropna(subset=["customer_key"])
    return (df[EXPORT_COLUMNS]
            .sort_values("revenue_last_12m", ascending=False)
            .reset_index(drop=True))


def read_mart(db_path: Path = WAREHOUSE_PATH) -> pd.DataFrame:
    with duckdb.connect(str(db_path), read_only=True) as con:
        return con.sql("select * from marts.mart_customers_at_risk").df()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("exports/clients_a_risque.csv"))
    out = ap.parse_args().out
    out.parent.mkdir(parents=True, exist_ok=True)
    export = build_export(read_mart())
    export.to_csv(out, index=False)
    log.info("%d clients à risque exportés vers %s", len(export), out)


if __name__ == "__main__":
    main()
