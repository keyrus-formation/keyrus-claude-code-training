"""Transformations : nettoyage et typage des données brutes.

NOTE FORMATEUR : ce module contient des bugs volontaires (voir
exercises/HD3_testing_debugging_integrations.md). Ne pas corriger avant la session.
"""

from __future__ import annotations

import pandas as pd

from .config import FX_TO_EUR


def parse_amount(value: str) -> float | None:
    """Convertit un montant texte en float.

    Accepte '1234.50' et le format français '1 234,50'.
    Retourne None si la valeur est vide ou illisible.
    """
    if value is None or value == "":
        return None
    try:
        return float(value.replace(",", "."))
    except ValueError:
        return None


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["email"] = out["email"].str.strip().str.lower().replace("", None)
    out["city"] = out["city"].replace("", None)
    out["signup_date"] = pd.to_datetime(out["signup_date"]).dt.date
    out = out.drop_duplicates()
    return out.reset_index(drop=True)


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie les commandes et ne garde que la dernière version de chaque commande."""
    out = df.copy()
    out["order_ts"] = pd.to_datetime(out["order_ts"])
    out["updated_at"] = pd.to_datetime(out["updated_at"])
    out["total_amount"] = out["total_amount"].map(parse_amount)

    # Dédoublonnage : une commande peut apparaître plusieurs fois (mises à jour CDC)
    out = out.sort_values("updated_at").drop_duplicates("order_id", keep="first")

    # Conversion en euros
    out["total_amount_eur"] = out.apply(
        lambda r: r["total_amount"] / FX_TO_EUR[r["currency"]]
        if r["total_amount"] is not None else None,
        axis=1,
    )
    return out.reset_index(drop=True)


def clean_payments(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["amount"] = out["amount"].astype(float)
    out["paid_at"] = pd.to_datetime(out["paid_at"])
    return out


def build_order_facts(orders: pd.DataFrame, payments: pd.DataFrame) -> pd.DataFrame:
    """Une ligne par commande, avec le montant payé."""
    facts = orders.merge(
        payments[["order_id", "amount"]].rename(columns={"amount": "paid_amount"}),
        on="order_id",
        how="left",
    )
    facts["is_fully_paid"] = facts["paid_amount"].round(2) >= facts["total_amount"].round(2)
    return facts
