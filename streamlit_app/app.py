import os
import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

st.title("📊 Sales Dashboard")

# ------------------ Load Data ------------------
@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(
        BASE_DIR,
        "..",
        "data",
        "processed",
        "cleaned_sales_data.csv"
    )

    df = pd.read_csv(DATA_PATH)

    # Data types
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["quantity_ordered"] = pd.to_numeric(df["quantity_ordered"], errors="coerce")
    df["price_each"] = pd.to_numeric(df["price_each"], errors="coerce")

    # Features
    df["sales"] = df["quantity_ordered"] * df["price_each"]
    df["month"] = df["order_date"].dt.to_period("M").astype(str)

    return df.dropna()

df = load_data()

# ------------------ Sidebar Filters ------------------
st.sidebar.header("🔍 Filters")

products = st.sidebar.multiselect(
    "Select Product(s)",
    options=sorted(df["product"].unique()),
    default=sorted(df["product"].unique())[:5]
)

months = st.sidebar.multiselect(
    "Select Month(s)",
    options=sorted(df["month"].unique()),
    default=sorted(df["month"].unique())
)

filtered_df = df[
    (df["product"].isin(products)) &
    (df["month"].isin(months))
]

# ------------------ KPIs ------------------
total_sales = filtered_df["sales"].sum()
total_orders = filtered_df["order_id"].nunique()
total_quantity = filtered_df["quantity_ordered"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"₹ {total_sales:,.0f}")
col2.metric("🧾 Total Orders", f"{total_orders:,}")
col3.metric("📦 Quantity Sold", f"{int(total_quantity):,}")

st.divider()

# ------------------ Monthly Trend ------------------
monthly_sales = (
    filtered_df
    .groupby("month", as_index=False)["sales"]
    .sum()
)

fig_trend = px.line(
    monthly_sales,
    x="month",
    y="sales",
    title="📈 Monthly Sales Trend",
    markers=True
)

st.plotly_chart(fig_trend, use_container_width=True)

# ------------------ Top Products ------------------
top_products = (
    filtered_df
    .groupby("product", as_index=False)["sales"]
    .sum()
    .sort_values(by="sales", ascending=False)
    .head(10)
)

fig_products = px.bar(
    top_products,
    x="sales",
    y="product",
    orientation="h",
    title="🏆 Top 10 Products by Sales"
)

st.plotly_chart(fig_products, use_container_width=True)
