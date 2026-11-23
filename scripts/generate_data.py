"""Génère le jeu de données fictif « RetailCo » utilisé pendant la formation.

Les données sont volontairement imparfaites (doublons, formats de montants
français, valeurs manquantes, dates futures, montants négatifs) pour servir
de support aux exercices de qualité de données et de debugging.

Usage :
    python scripts/generate_data.py            # écrit dans data/raw/
    python scripts/generate_data.py --seed 7   # autre tirage reproductible
"""

from __future__ import annotations

import argparse
import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

FIRST_NAMES = ["Camille", "Louis", "Emma", "Hugo", "Léa", "Jules", "Chloé", "Lucas",
               "Inès", "Nathan", "Manon", "Adam", "Sarah", "Gabriel", "Jade", "Raphaël"]
LAST_NAMES = ["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit",
              "Durand", "Leroy", "Moreau", "Simon", "Laurent", "Lefebvre", "Michel"]
CITIES = ["Paris", "Lyon", "Marseille", "Lille", "Nantes", "Bordeaux", "Toulouse",
          "Strasbourg", "Bruxelles", "Genève"]
SEGMENTS = ["B2C", "B2B", "VIP"]
CATEGORIES = {
    "Épicerie": [("Café grains 1kg", 18.90), ("Thé vert bio", 7.50), ("Chocolat noir", 3.20)],
    "Maison": [("Bougie parfumée", 24.00), ("Plaid laine", 59.90), ("Vase céramique", 34.50)],
    "High-Tech": [("Casque audio", 129.00), ("Chargeur USB-C", 19.99), ("Enceinte BT", 79.00)],
    "Sport": [("Tapis de yoga", 29.90), ("Gourde inox", 22.00), ("Haltères 2x5kg", 45.00)],
}
CHANNELS = ["web", "app", "store"]
CURRENCIES = ["EUR"] * 8 + ["USD", "CHF"]
PAYMENT_METHODS = ["card", "paypal", "transfer", "voucher"]


def fr_amount(x: float) -> str:
    """Formate un montant à la française : '1 234,50'."""
    s = f"{x:,.2f}"  # 1,234.50
    return s.replace(",", " ").replace(".", ",")


def main(seed: int, n_customers: int, n_orders: int) -> None:
    rng = random.Random(seed)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # --- products ---------------------------------------------------------
    products = []
    pid = 1
    for cat, items in CATEGORIES.items():
        for name, price in items:
            products.append({"product_id": f"P{pid:03d}", "product_name": name,
                             "category": cat, "unit_price_eur": f"{price:.2f}"})
            pid += 1
    with open(RAW_DIR / "products.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(products[0]))
        w.writeheader()
        w.writerows(products)

    # --- customers --------------------------------------------------------
    customers = []
    for i in range(1, n_customers + 1):
        fn, ln = rng.choice(FIRST_NAMES), rng.choice(LAST_NAMES)
        email = f"{fn.lower()}.{ln.lower()}{i}@example.com"
        if rng.random() < 0.04:
            email = ""  # email manquant
        elif rng.random() < 0.05:
            email = email.upper()  # casse incohérente
        signup = date(2023, 1, 1) + timedelta(days=rng.randint(0, 900))
        customers.append({
            "customer_id": f"C{i:05d}",
            "first_name": fn,
            "last_name": ln,
            "email": email,
            "city": rng.choice(CITIES) if rng.random() > 0.03 else "",
            "segment": rng.choice(SEGMENTS),
            "signup_date": signup.isoformat(),
        })
    # doublons exacts de clients (problème classique d'extraction CRM)
    customers += rng.sample(customers, k=max(1, n_customers // 50))
    with open(RAW_DIR / "customers.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(customers[0]))
        w.writeheader()
        w.writerows(customers)

    # --- orders -----------------------------------------------------------
    orders = []
    order_lines = []
    payments = []
    base = datetime(2025, 1, 1)
    for i in range(1, n_orders + 1):
        oid = f"O{i:06d}"
        cust = rng.choice(customers[:n_customers])["customer_id"]
        ts = base + timedelta(minutes=rng.randint(0, 60 * 24 * 600))
        currency = rng.choice(CURRENCIES)
        status = rng.choices(["delivered", "shipped", "cancelled", "returned"],
                             weights=[70, 15, 10, 5])[0]
        n_lines = rng.randint(1, 4)
        total = 0.0
        for ln_no in range(1, n_lines + 1):
            p = rng.choice(products)
            qty = rng.randint(1, 3) if rng.random() > 0.12 else rng.randint(6, 20)  # paniers B2B
            price = float(p["unit_price_eur"])
            total += qty * price
            order_lines.append({"order_id": oid, "line_number": ln_no,
                                "product_id": p["product_id"], "quantity": qty,
                                "unit_price": f"{price:.2f}"})
        if rng.random() < 0.01:
            total = -total  # montant négatif (bug source)
        amount = fr_amount(total) if rng.random() < 0.3 else f"{total:.2f}"
        if rng.random() < 0.01:
            amount = ""  # montant manquant
        if rng.random() < 0.005:
            ts = datetime(2031, 1, 1)  # date dans le futur
        orders.append({
            "order_id": oid,
            "customer_id": cust,
            "order_ts": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "channel": rng.choice(CHANNELS),
            "status": status,
            "currency": currency,
            "total_amount": amount,
            "updated_at": (ts + timedelta(hours=rng.randint(0, 48))).strftime("%Y-%m-%d %H:%M:%S"),
        })
        # paiements : parfois fractionnés en 2 (ce qui piège les jointures)
        if status != "cancelled":
            if rng.random() < 0.15:
                half = round(total / 2, 2)
                payments.append({"payment_id": f"PAY{len(payments)+1:07d}", "order_id": oid,
                                 "method": "card", "amount": f"{half:.2f}",
                                 "paid_at": ts.strftime("%Y-%m-%d %H:%M:%S")})
                payments.append({"payment_id": f"PAY{len(payments)+1:07d}", "order_id": oid,
                                 "method": "voucher", "amount": f"{total - half:.2f}",
                                 "paid_at": ts.strftime("%Y-%m-%d %H:%M:%S")})
            else:
                payments.append({"payment_id": f"PAY{len(payments)+1:07d}", "order_id": oid,
                                 "method": rng.choice(PAYMENT_METHODS), "amount": f"{total:.2f}",
                                 "paid_at": ts.strftime("%Y-%m-%d %H:%M:%S")})

    # mises à jour : certaines commandes réapparaissent avec un statut plus récent
    updates = []
    for o in rng.sample(orders, k=n_orders // 20):
        u = dict(o)
        u["status"] = "returned"
        u["updated_at"] = (datetime.strptime(o["updated_at"], "%Y-%m-%d %H:%M:%S")
                           + timedelta(days=rng.randint(3, 20))).strftime("%Y-%m-%d %H:%M:%S")
        updates.append(u)
    all_orders = orders + updates
    rng.shuffle(all_orders)

    for name, rows in [("orders.csv", all_orders), ("order_lines.csv", order_lines),
                       ("payments.csv", payments)]:
        with open(RAW_DIR / name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)

    print(f"OK : {len(products)} produits, {len(customers)} clients, "
          f"{len(all_orders)} lignes commandes, {len(order_lines)} lignes articles, "
          f"{len(payments)} paiements → {RAW_DIR}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--customers", type=int, default=2000)
    ap.add_argument("--orders", type=int, default=20000)
    a = ap.parse_args()
    main(a.seed, a.customers, a.orders)
