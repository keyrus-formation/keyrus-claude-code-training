"""Tests de non-régression des 4 bugs trouvés en J3. Chacun échoue sur le code d'origine."""

import pandas as pd
import pytest

from retail_pipeline.transform import build_order_facts, clean_orders, parse_amount


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("1 234,50", 1234.50),
        ("1 234,50", 1234.50),   # espace insécable (export Excel)
        ("12 345 678,90", 12345678.90),
        ("1234.50", 1234.50),
        ("  ", None),
        ("abc", None),
    ],
)
def test_parse_amount_thousands_separator(raw, expected):
    assert parse_amount(raw) == expected


def _orders(rows):
    base = {"customer_id": "C1", "channel": "web", "currency": "EUR", "total_amount": "10.00",
            "order_ts": "2025-01-01 10:00:00"}
    return pd.DataFrame([{**base, **r} for r in rows])


def test_clean_orders_keeps_latest_version():
    df = _orders([
        {"order_id": "O1", "status": "delivered", "updated_at": "2025-01-02 00:00:00"},
        {"order_id": "O1", "status": "returned", "updated_at": "2025-01-10 00:00:00"},
    ])
    out = clean_orders(df)
    assert len(out) == 1
    assert out.loc[0, "status"] == "returned"


def test_clean_orders_converts_usd_to_eur_by_multiplying():
    df = _orders([{"order_id": "O1", "status": "delivered", "currency": "USD",
                   "total_amount": "100.00", "updated_at": "2025-01-02 00:00:00"}])
    assert clean_orders(df).loc[0, "total_amount_eur"] == pytest.approx(92.0)


def test_build_order_facts_one_row_per_order_with_split_payment():
    orders = clean_orders(_orders([
        {"order_id": "O1", "status": "delivered", "total_amount": "100.00",
         "updated_at": "2025-01-02 00:00:00"},
    ]))
    payments = pd.DataFrame({"order_id": ["O1", "O1"], "amount": [60.0, 40.0]})
    facts = build_order_facts(orders, payments)
    assert len(facts) == 1
    assert facts.loc[0, "paid_amount"] == pytest.approx(100.0)
    assert bool(facts.loc[0, "is_fully_paid"]) is True
