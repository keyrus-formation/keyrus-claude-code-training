import hashlib

import pandas as pd

from retail_pipeline.export_at_risk import EXPORT_COLUMNS, build_export, pseudonymize_email


def test_pseudonymize_is_normalized_and_stable():
    expected = hashlib.sha256(b"camille.martin1@example.com").hexdigest()
    assert pseudonymize_email(" Camille.Martin1@EXAMPLE.com ") == expected
    assert pseudonymize_email("") is None
    assert pseudonymize_email(None) is None


def test_export_contains_only_at_risk_and_no_personal_data():
    mart = pd.DataFrame({
        "customer_id": ["C1", "C2", "C3"],
        "email": ["a@x.com", "b@x.com", None],
        "segment": ["VIP", "B2C", "B2C"],
        "days_since_last_order": [70, 10, 200],
        "orders_last_12m": [3, 5, 2],
        "revenue_last_12m": [500.0, 900.0, 100.0],
        "is_at_risk": [True, False, True],
    })
    out = build_export(mart)
    assert list(out.columns) == EXPORT_COLUMNS
    assert len(out) == 1                                  # C2 pas à risque, C3 sans email
    flat = out.astype(str).to_string()
    assert "@" not in flat and "C1" not in flat           # ni email ni identifiant en clair
