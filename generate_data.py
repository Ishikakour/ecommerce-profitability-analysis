import pandas as pd
import numpy as np
import random

CSV_PATH = "ecommerce_data.csv"
TARGET_AMOUNT = 72000.0
TARGET_QTY = 1017
TARGET_PROFIT = -1469.0


def generate_dataset(path: str = CSV_PATH) -> pd.DataFrame:
    np.random.seed(42)
    random.seed(42)
    n = 150

    states = ["Madhya Pradesh", "Maharashtra", "Uttar Pradesh", "Kerala"]
    state_weights = [0.40, 0.30, 0.20, 0.10]

    payment_modes = ["COD", "UPI", "Credit Card", "Debit Card", "EMI"]
    payment_weights = [0.4287, 0.2468, 0.1347, 0.1170, 0.0728]

    categories = ["Clothing", "Furniture", "Electronics"]
    category_weights = [0.60, 0.21, 0.19]

    customers = ["Vishakha", "Surabhi", "Ayush", "Madhav"]

    sub_categories = {
        "Clothing": ["Saree", "Accessories"],
        "Furniture": ["Bookcases", "Tables"],
        "Electronics": ["Electronic Games"],
    }

    rows = []
    for i in range(n):
        state = np.random.choice(states, p=state_weights)
        payment = np.random.choice(payment_modes, p=payment_weights)
        category = np.random.choice(categories, p=category_weights)
        sub_cat = random.choice(sub_categories[category])
        customer = random.choice(customers)

        qty = random.randint(1, 10)
        price_per_unit = random.uniform(500, 1500)
        amount = qty * price_per_unit

        if category == "Clothing" and state == "Madhya Pradesh" and payment == "COD":
            profit = -random.uniform(200, 800)
        elif category == "Clothing":
            profit = -random.uniform(50, 200)
        else:
            profit = random.uniform(100, 600)

        month = random.choice(["July", "August", "September"])

        rows.append(
            {
                "OrderID": f"ORD-{1000 + i}",
                "Month": month,
                "Quarter": "Qtr 3",
                "State": state,
                "CustomerName": customer,
                "Category": category,
                "SubCategory": sub_cat,
                "PaymentMode": payment,
                "Quantity": qty,
                "Amount": round(amount, 2),
                "Profit": round(profit, 2),
            }
        )

    df = pd.DataFrame(rows)

    df["Amount"] = df["Amount"] * (TARGET_AMOUNT / df["Amount"].sum())
    df["Amount"] = df["Amount"].round(2)
    df.loc[df["Amount"].idxmax(), "Amount"] += round(TARGET_AMOUNT - df["Amount"].sum(), 2)

    qty = df["Quantity"].to_numpy()
    diff = TARGET_QTY - int(qty.sum())
    step = 1 if diff > 0 else -1
    idx = 0
    while diff != 0:
        nxt = qty[idx] + step
        if 1 <= nxt <= 10:
            qty[idx] = nxt
            diff -= step
        idx = (idx + 1) % n
    df["Quantity"] = qty

    delta = TARGET_PROFIT - df["Profit"].sum()
    mask = df["Category"] == "Clothing" if delta < 0 else df["Category"] != "Clothing"
    df.loc[mask, "Profit"] += delta / mask.sum()
    df["Profit"] = df["Profit"].round(2)
    df.loc[df["Profit"].idxmin(), "Profit"] += round(TARGET_PROFIT - df["Profit"].sum(), 2)

    df.to_csv(path, index=False)
    return df


if __name__ == "__main__":
    df = generate_dataset()
    print(f"Generated: {CSV_PATH} ({len(df)} rows)")
    print(f"Total Amount   : {df['Amount'].sum():,.0f}")
    print(f"Total Quantity : {df['Quantity'].sum():,}")
    print(f"Total Profit   : {df['Profit'].sum():,.0f}")
    print(f"Amount range   : {df['Amount'].min():.2f} .. {df['Amount'].max():.2f}")
    print(f"Qty range      : {df['Quantity'].min()} .. {df['Quantity'].max()}")
