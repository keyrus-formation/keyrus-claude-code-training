"""Configuration centralisée du pipeline.

Les secrets (identifiants Snowflake) ne sont JAMAIS écrits ici : ils sont lus
depuis les variables d'environnement (voir .env.example).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
WAREHOUSE_PATH = ROOT / "data" / "retail.duckdb"

# Taux de change figés pour la formation (1 unité de devise = x EUR)
FX_TO_EUR: dict[str, float] = {
    "EUR": 1.0,
    "USD": 0.92,
    "CHF": 1.05,
}


@dataclass(frozen=True)
class SnowflakeSettings:
    account: str = field(default_factory=lambda: os.getenv("SNOWFLAKE_ACCOUNT", ""))
    user: str = field(default_factory=lambda: os.getenv("SNOWFLAKE_USER", ""))
    password: str = field(default_factory=lambda: os.getenv("SNOWFLAKE_PASSWORD", ""))
    role: str = field(default_factory=lambda: os.getenv("SNOWFLAKE_ROLE", "TRAINING_ROLE"))
    warehouse: str = field(default_factory=lambda: os.getenv("SNOWFLAKE_WAREHOUSE", "TRAINING_WH"))
    database: str = field(default_factory=lambda: os.getenv("SNOWFLAKE_DATABASE", "RETAILCO"))
    schema: str = field(default_factory=lambda: os.getenv("SNOWFLAKE_SCHEMA", "RAW"))

    @property
    def is_configured(self) -> bool:
        return bool(self.account and self.user)
