import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)
n = 150

states = ['Madhya Pradesh', 'Maharashtra', 'Uttar Pradesh', 'Kerala']
state_weights = [0.40, 0.30, 0.20, 0.10]

payment_modes = ['COD', 'UPI', 'Credit Card', 'Debit Card', 'EMI']
payment_weights = [0.4287, 0.2468, 0.1347, 0.1170, 0.0728]

categories = ['Clothing', 'Furniture', 'Electronics']
category_weights = [0.60, 0.21, 0.19]

customers = ['Vishakha', 'Surabhi', 'Ayush', 'Madhav']

sub_categories = {
    'Clothing': ['Saree', 'Accessories'],
    'Furniture': ['Bookcases', 'Tables'],
    'Electronics': ['Electronic Games'],
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

    # Loss pattern: high-risk combos produce negative profit
    if category == 'Clothing' and state == 'Madhya Pradesh' and payment == 'COD':
        profit = -random.uniform(200, 800)
    elif category == 'Clothing':
        profit = -random.uniform(50, 200)
    else:
        profit = random.uniform(100, 600)

    month = random.choice(['July', 'August', 'September'])

    rows.append({
        'OrderID': f'ORD-{1000 + i}',
        'Month': month,
        'Quarter': 'Qtr 3',
        'State': state,
        'CustomerName': customer,
        'Category': category,
        'SubCategory': sub_cat,
        'PaymentMode': payment,
        'Quantity': qty,
        'Amount': round(amount, 2),
        'Profit': round(profit, 2),
    })

df = pd.DataFrame(rows)

# Adjust to match target totals exactly
df.loc[0, 'Amount'] += 72000 - df['Amount'].sum()
df.loc[1, 'Quantity'] += 1017 - df['Quantity'].sum()
df.loc[2, 'Profit'] += -1469 - df['Profit'].sum()

df.to_csv('ecommerce_data.csv', index=False)

print(f"Generated: ecommerce_data.csv ({len(df)} rows)")
print(f"Total Amount   : {df['Amount'].sum():,.0f}")
print(f"Total Quantity : {df['Quantity'].sum():,}")
print(f"Total Profit   : {df['Profit'].sum():,.0f}")