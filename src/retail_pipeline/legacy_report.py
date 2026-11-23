# Rapport mensuel historique — écrit en 2019 par un prestataire, jamais revu.
# Support de l'exercice J2 « optimisation » : lent, difficile à tester, non typé.
import pandas as pd
import sys

def rapport(chemin):
    o = pd.read_csv(chemin + "/orders.csv", dtype=str, keep_default_na=False)
    l = pd.read_csv(chemin + "/order_lines.csv", dtype=str, keep_default_na=False)
    p = pd.read_csv(chemin + "/products.csv", dtype=str, keep_default_na=False)
    res = {}
    for i, row in l.iterrows():
        cmd = o[o["order_id"] == row["order_id"]]
        if len(cmd) == 0:
            continue
        cmd = cmd.iloc[0]
        if cmd["status"] == "cancelled":
            continue
        mois = cmd["order_ts"][0:7]
        prod = p[p["product_id"] == row["product_id"]].iloc[0]
        cat = prod["category"]
        k = mois + "|" + cat
        if k not in res:
            res[k] = 0
        res[k] = res[k] + int(row["quantity"]) * float(row["unit_price"])
    out = []
    for k in res:
        out.append({"mois": k.split("|")[0], "categorie": k.split("|")[1], "ca": round(res[k], 2)})
    df = pd.DataFrame(out).sort_values(["mois", "categorie"])
    return df

if __name__ == "__main__":
    print(rapport(sys.argv[1]).to_string())
