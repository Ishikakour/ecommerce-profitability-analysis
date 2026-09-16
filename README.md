# E-Commerce Profitability & Risk Analysis

**Live Dashboard:** [ecommerce-profitability-analysis.streamlit.app](https://YOUR-APP-URL-HERE) 
---

## Business Problem

An e-commerce marketplace generated ₹72,000 in total sales across 1,017 units sold in Q3 (July–September). Despite strong top-line revenue, the company suffered a net loss of ₹1,469. Leadership had no visibility into which regions, payment modes, and product categories were driving the losses.

This project builds an end-to-end analytics pipeline — from synthetic data generation to a live interactive dashboard — that surfaces loss drivers and recommends mitigation strategies.

## Data Architecture
generate_data.py (Python) → ecommerce_data.csv → app.py
 (Streamlit + Plotly)
        ↓
analysis.sql (RFM + Cohort + Profitability)



## Key Findings

- **Regional Loss Concentration:** Madhya Pradesh accounted for the highest sales volume but was the primary driver of negative profit margins.
- **Payment Mode Risk:** Cash on Delivery (COD) represented 42.87% of orders and correlated with the highest return/loss rates. UPI (24.68%) and Credit Card (13.47%) showed healthier margins.
- **Category Imbalance:** Clothing accounted for 60% of units sold but had a disproportionate negative impact on profit. Only Bookcases and Tables were profitable sub-categories.
- **Monthly Trend:** July and September were loss-making months. August was the only profitable month in Q3.

## Business Recommendations

1. **Migrate COD to Prepaid:** Introduce a 5% discount on UPI/Credit Card transactions to reduce COD dependency and lower return-related losses.
2. **Bundle Low-Margin with High-Margin:** Pair low-margin Clothing items with high-margin Accessories to improve average basket profitability.
3. **Regional Risk Policy:** Require a partial deposit for high-value COD orders in Madhya Pradesh to hedge against returns.

## Tech Stack

- **Python:** Pandas, NumPy (data generation and transformation)
- **Streamlit:** Interactive web dashboard
- **Plotly:** Dynamic visualizations
- **SQL:** RFM segmentation, cohort retention, profitability ranking (window functions)

## Repository Contents

| File | Purpose |
|---|---|
| `generate_data.py` | Python script that generates a synthetic dataset matching real-world e-commerce distributions |
| `ecommerce_data.csv` | Generated synthetic dataset (150 orders) |
| `app.py` | Streamlit dashboard application |
| `analysis.sql` | SQL queries: RFM segmentation, state profitability, payment risk, category concentration |
| `requirements.txt` | Python dependencies |
| `dashboard.png` | Dashboard screenshot |

## How to Run Locally

```bash
pip install -r requirements.txt
python generate_data.py
streamlit run app.py

Author
Ishika Kour — M.Tech Data Analytics, NIT Jalandhar | Ex-Philips Analytics | GATE CSE/DA Qualified
