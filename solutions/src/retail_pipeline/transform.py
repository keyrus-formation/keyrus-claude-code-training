"""Transformations : nettoyage et typage des données brutes (version corrigée)."""

from __future__ import annotations

import re

import pandas as pd

from .config import FX_TO_EUR

_SPACES = re.compile(r"[\s  ]")  # espace, insécable, insécable fine


def parse_amount(value: str | None) -> float | None:
    """Convertit un montant texte en float.

    Accepte '1234.50' et le format français '1 234,50' (espaces ou espaces
    insécables comme séparateurs de milliers). Retourne None si vide ou illisible.
    """
    if value is None:
        return None
    cleaned = _SPACES.sub("", str(value)).replace(",", ".")
    if cleaned == "":
        return None
    try:
        return float(cleaned)
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
    out["total_amount"] = out["total_amount"].map(parse_amount).astype("Float64")

    # Correctif 1 : garder la version la PLUS RÉCENTE de chaque commande
    out = out.sort_values("updated_at").drop_duplicates("order_id", keep="last")

    # Correctif 2 : FX_TO_EUR = valeur d'une unité de devise en EUR → multiplier (vectorisé)
    out["total_amount_eur"] = out["total_amount"] * out["currency"].map(FX_TO_EUR)
    return out.reset_index(drop=True)


def clean_payments(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["amount"] = out["amount"].astype(float)
    out["paid_at"] = pd.to_datetime(out["paid_at"])
    return out


def build_order_facts(orders: pd.DataFrame, payments: pd.DataFrame) -> pd.DataFrame:
    """Une ligne par commande, avec le montant total payé."""
    # Correctif 3 : agréger les paiements au grain commande AVANT la jointure (fan-out)
    paid = (
        payments.groupby("order_id", as_index=False)["amount"].sum()
        .rename(columns={"amount": "paid_amount"})
    )
    facts = orders.merge(paid, on="order_id", how="left", validate="one_to_one")
    facts["paid_amount"] = facts["paid_amount"].fillna(0.0)
    facts["is_fully_paid"] = facts["paid_amount"].round(2) >= facts["total_amount"].round(2)
    return facts
