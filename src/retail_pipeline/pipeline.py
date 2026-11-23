"""Point d'entrée du pipeline : extract → transform → quality → load.

    python -m retail_pipeline.pipeline            # charge les données brutes dans DuckDB
    python -m retail_pipeline.pipeline --target snowflake
"""

from __future__ import annotations

import argparse
import logging

from . import extract, load, quality, transform

log = logging.getLogger("retail_pipeline")


def run(target: str = "duckdb") -> int:
    raw = extract.read_all()
    log.info("Extraction : %s", {k: len(v) for k, v in raw.items()})

    orders = transform.clean_orders(raw["orders"])
    results = quality.run_order_checks(orders)
    for r in results:
        log.info("%-30s %s (%d lignes en échec)", r.name, "OK" if r.passed else "KO",
                 r.failing_rows)

    # On charge le brut : les transformations « officielles » sont faites dans dbt
    if target == "duckdb":
        load.load_to_duckdb(raw)
    elif target == "snowflake":
        load.load_to_snowflake(raw)
    else:
        raise ValueError(target)
    log.info("Chargement %s terminé", target)
    return 0 if all(r.passed for r in results) else 1


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", choices=["duckdb", "snowflake"], default="duckdb")
    raise SystemExit(run(ap.parse_args().target))


if __name__ == "__main__":
    main()
