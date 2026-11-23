"""Contrôles de qualité de données exécutés après la transformation.

Volontairement incomplet : l'exercice J3 consiste à le compléter avec Claude Code.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class CheckResult:
    name: str
    passed: bool
    failing_rows: int
    detail: str = ""


def check_unique(df: pd.DataFrame, column: str) -> CheckResult:
    dups = int(df[column].duplicated().sum())
    return CheckResult(f"unique({column})", dups == 0, dups)


def check_not_null(df: pd.DataFrame, column: str) -> CheckResult:
    nulls = int(df[column].isna().sum())
    return CheckResult(f"not_null({column})", nulls == 0, nulls)


# TODO (exercice J3) :
#   - check_accepted_values(df, column, values)
#   - check_range(df, column, min_value, max_value)
#   - check_no_future_dates(df, column)
#   - check_referential_integrity(child, parent, key)


def run_order_checks(orders: pd.DataFrame) -> list[CheckResult]:
    return [
        check_unique(orders, "order_id"),
        check_not_null(orders, "customer_id"),
    ]
