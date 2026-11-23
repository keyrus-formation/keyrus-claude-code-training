"""Tests existants : ils passent… et pourtant le code contient des bugs.

Leçon de l'exercice J3 : une suite verte ne prouve que ce qu'elle teste.
"""

import pandas as pd

from retail_pipeline.transform import clean_customers, parse_amount


def test_parse_amount_dot_decimal():
    assert parse_amount("12.50") == 12.5


def test_parse_amount_comma_decimal():
    assert parse_amount("12,50") == 12.5


def test_parse_amount_empty_returns_none():
    assert parse_amount("") is None


def test_clean_customers_lowercases_email():
    df = pd.DataFrame([{"customer_id": "C1", "first_name": "A", "last_name": "B",
                        "email": " A.B@EXAMPLE.COM ", "city": "Paris", "segment": "B2C",
                        "signup_date": "2024-01-01"}])
    assert clean_customers(df).loc[0, "email"] == "a.b@example.com"
