"""
E-Commerce Profitability & Risk Analysis — Streamlit Dashboard
Author: Ishika Kour
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import os

from generate_data import CSV_PATH, generate_dataset


def csv_is_stale(path: str) -> bool:
    if not os.path.exists(path):
        return True
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("OrderID,"):
                continue
            parts = line.strip().split(",")
            if len(parts) >= 10 and float(parts[9]) <= 0:
                return True
    return False


if csv_is_stale(CSV_PATH):
    generate_dataset(CSV_PATH)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="E-Commerce Profitability & Risk Analysis",
    page_icon="📊",
    layout="wide",
)

# ---------------- DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)

df = load_data()

# ---------------- HEADER ----------------
st.title("📊 E-Commerce Profitability & Risk Analysis")
st.markdown("##### Q3 Analysis · Built by Ishika Kour")
st.markdown("---")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Filters")
state_filter = st.sidebar.multiselect(
    "State",
    sorted(df['State'].unique()),
    default=sorted(df['State'].unique()),
)
category_filter = st.sidebar.multiselect(
    "Category",
    sorted(df['Category'].unique()),
    default=sorted(df['Category'].unique()),
)
payment_filter = st.sidebar.multiselect(
    "Payment Mode",
    sorted(df['PaymentMode'].unique()),
    default=sorted(df['PaymentMode'].unique()),
)

filtered = df[
    df['State'].isin(state_filter)
    & df['Category'].isin(category_filter)
    & df['PaymentMode'].isin(payment_filter)
]

# ---------------- KPI CARDS ----------------
c1, c2, c3, c4 = st.columns(4)
total_amount = filtered['Amount'].sum()
total_quantity = filtered['Quantity'].sum()
total_profit = filtered['Profit'].sum()
aov = total_amount / filtered['OrderID'].nunique() if filtered['OrderID'].nunique() else 0

c1.metric("Total Sales", f"₹{total_amount:,.0f}")
c2.metric("Total Quantity", f"{total_quantity:,}")
c3.metric(
    "Total Profit",
    f"₹{total_profit:,.0f}",
    delta=f"₹{total_profit:,.0f}",
    delta_color="inverse" if total_profit < 0 else "normal",
)
c4.metric("Avg Order Value", f"₹{aov:,.0f}")

st.markdown("---")

# ---------------- ROW 1 ----------------
r1a, r1b = st.columns(2)

with r1a:
    st.subheader("Sales by State")
    state_data = (
        filtered.groupby('State', as_index=False)['Amount']
        .sum().sort_values('Amount', ascending=True)
    )
    fig = px.bar(
        state_data, x='Amount', y='State', orientation='h',
        color='Amount', color_continuous_scale='Blues', text='Amount',
    )
    fig.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
    fig.update_layout(showlegend=False, coloraxis_showscale=False, height=350)
    st.plotly_chart(fig, use_container_width=True)

with r1b:
    st.subheader("Order Distribution by Payment Mode")
    pay_data = filtered.groupby('PaymentMode', as_index=False)['Quantity'].sum()
    fig = px.pie(
        pay_data, values='Quantity', names='PaymentMode',
        hole=0.5, color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# ---------------- ROW 2 ----------------
r2a, r2b = st.columns(2)

with r2a:
    st.subheader("Profit by Month")
    order = ['July', 'August', 'September']
    month_data = filtered.groupby('Month', as_index=False)['Profit'].sum()
    month_data['Month'] = pd.Categorical(month_data['Month'], order, ordered=True)
    month_data = month_data.sort_values('Month')
    colors = ['#EF553B' if p < 0 else '#00CC96' for p in month_data['Profit']]
    fig = go.Figure(go.Bar(
        x=month_data['Month'], y=month_data['Profit'],
        marker_color=colors, text=month_data['Profit'],
    ))
    fig.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
    fig.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with r2b:
    st.subheader("Quantity Split by Category")
    cat_data = filtered.groupby('Category', as_index=False)['Quantity'].sum()
    fig = px.pie(
        cat_data, values='Quantity', names='Category',
        hole=0.5, color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# ---------------- ROW 3 ----------------
r3a, r3b = st.columns(2)

with r3a:
    st.subheader("Profit by Sub-Category")
    sub_data = (
        filtered.groupby('SubCategory', as_index=False)['Profit']
        .sum().sort_values('Profit', ascending=True)
    )
    fig = px.bar(
        sub_data, x='Profit', y='SubCategory', orientation='h',
        color='Profit', color_continuous_scale='RdYlGn', text='Profit',
    )
    fig.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
    fig.update_layout(showlegend=False, coloraxis_showscale=False, height=350)
    st.plotly_chart(fig, use_container_width=True)

with r3b:
    st.subheader("Sales by Customer")
    cust_data = (
        filtered.groupby('CustomerName', as_index=False)['Amount']
        .sum().sort_values('Amount', ascending=False)
    )
    fig = px.bar(
        cust_data, x='CustomerName', y='Amount',
        color='Amount', color_continuous_scale='Purples', text='Amount',
    )
    fig.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
    fig.update_layout(showlegend=False, coloraxis_showscale=False, height=350)
    st.plotly_chart(fig, use_container_width=True)

# ---------------- INSIGHTS ----------------
st.markdown("---")
st.subheader("🔍 Auto-Generated Insights")

if filtered.empty:
    st.info("No rows match the current filters.")
else:
    profit_by_state = (
        filtered.groupby("State", as_index=False)["Profit"].sum()
        .sort_values("Profit")
    )
    worst_month = month_data.loc[month_data["Profit"].idxmin(), "Month"]
    worst_state = profit_by_state.iloc[0]["State"]
    worst_state_profit = profit_by_state.iloc[0]["Profit"]
    top_pay = pay_data.sort_values("Quantity", ascending=False).iloc[0]
    top_pay_pct = top_pay["Quantity"] / pay_data["Quantity"].sum() * 100

    i1, i2, i3 = st.columns(3)
    i1.info(f"**Worst Month:** {worst_month}\n\nLowest profit month in the filtered Q3 data.")
    i2.warning(
        f"**Highest Loss State:** {worst_state} (₹{worst_state_profit:,.0f})\n\n"
        "Primary regional profit drag."
    )
    i3.success(
        f"**Dominant Payment (units):** {top_pay['PaymentMode']} ({top_pay_pct:.1f}%)\n\n"
        "Largest share of units sold."
    )

st.caption("Built with Python · Pandas · Plotly · Streamlit")