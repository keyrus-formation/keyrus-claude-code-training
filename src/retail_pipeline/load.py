"""Chargement : DuckDB en local (formation), Snowflake en option.

DuckDB joue le rôle de l'entrepôt pendant les exercices pour que chacun puisse
travailler sans compte Snowflake. Le même code SQL dbt tourne sur les deux
(voir dbt_project/profiles.yml).
"""

from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd

from .config import WAREHOUSE_PATH, SnowflakeSettings


def load_to_duckdb(tables: dict[str, pd.DataFrame], schema: str = "raw",
                   db_path: Path = WAREHOUSE_PATH) -> None:
    con = duckdb.connect(str(db_path))
    try:
        con.execute(f"create schema if not exists {schema}")
        for name, df in tables.items():
            con.register("tmp_df", df)
            con.execute(f"create or replace table {schema}.{name} as select * from tmp_df")
            con.unregister("tmp_df")
    finally:
        con.close()


def load_to_snowflake(tables: dict[str, pd.DataFrame]) -> None:  # pragma: no cover
    """Chargement Snowflake via write_pandas (nécessite snowflake-connector-python[pandas])."""
    settings = SnowflakeSettings()
    if not settings.is_configured:
        raise RuntimeError("Variables SNOWFLAKE_* absentes : voir .env.example")
    import snowflake.connector
    from snowflake.connector.pandas_tools import write_pandas

    con = snowflake.connector.connect(
        account=settings.account, user=settings.user, password=settings.password,
        role=settings.role, warehouse=settings.warehouse,
        database=settings.database, schema=settings.schema,
    )
    try:
        for name, df in tables.items():
            write_pandas(con, df, table_name=name.upper(), auto_create_table=True,
                         overwrite=True)
    finally:
        con.close()
