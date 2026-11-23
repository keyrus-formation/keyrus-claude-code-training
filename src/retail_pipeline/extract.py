"""Extraction : lecture des fichiers bruts déposés par les systèmes sources."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .config import RAW_DIR

SOURCES = ["customers", "orders", "order_lines", "payments", "products"]


def read_source(name: str, raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Lit un fichier source en texte brut (aucun typage à ce stade)."""
    if name not in SOURCES:
        raise ValueError(f"Source inconnue : {name!r}. Attendu : {SOURCES}")
    path = raw_dir / f"{name}.csv"
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def read_all(raw_dir: Path = RAW_DIR) -> dict[str, pd.DataFrame]:
    return {name: read_source(name, raw_dir) for name in SOURCES}
