"""Contrôles de qualité de données exécutés après la transformation (version complétée)."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime

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


def check_accepted_values(df: pd.DataFrame, column: str, values: Iterable[str]) -> CheckResult:
    allowed = set(values)
    bad = df[column].dropna()
    bad = bad[~bad.isin(allowed)]
    return CheckResult(f"accepted_values({column})", bad.empty, len(bad),
                       f"valeurs inattendues : {sorted(bad.unique())[:5]}" if len(bad) else "")


def check_range(df: pd.DataFrame, column: str, min_value: float | None = None,
                max_value: float | None = None) -> CheckResult:
    s = df[column].dropna()
    mask = pd.Series(False, index=s.index)
    if min_value is not None:
        mask |= s < min_value
    if max_value is not None:
        mask |= s > max_value
    n = int(mask.sum())
    return CheckResult(f"range({column}, {min_value}, {max_value})", n == 0, n)


def check_no_future_dates(df: pd.DataFrame, column: str,
                          now: datetime | None = None) -> CheckResult:
    now = now or datetime.now()
    n = int((pd.to_datetime(df[column]) > now).sum())
    return CheckResult(f"no_future_dates({column})", n == 0, n)


def check_referential_integrity(child: pd.DataFrame, parent: pd.DataFrame,
                                key: str) -> CheckResult:
    orphans = child[key].dropna()
    orphans = orphans[~orphans.isin(set(parent[key]))]
    return CheckResult(f"relationships({key})", orphans.empty, len(orphans))


def run_order_checks(orders: pd.DataFrame,
                     customers: pd.DataFrame | None = None) -> list[CheckResult]:
    results = [
        check_unique(orders, "order_id"),
        check_not_null(orders, "customer_id"),
        check_not_null(orders, "total_amount"),
        check_accepted_values(orders, "status", ["delivered", "shipped", "cancelled", "returned"]),
        check_accepted_values(orders, "currency", ["EUR", "USD", "CHF"]),
        check_range(orders, "total_amount", min_value=0),
        check_no_future_dates(orders, "order_ts"),
    ]
    if customers is not None:
        results.append(check_referential_integrity(orders, customers, "customer_id"))
    return results
