import streamlit as st
import pandas as pd

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Sales Data Dashboard",
    layout="wide",
)

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/sales_data_cleaned.csv")

    # Type conversions
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["quantity_ordered"] = pd.to_numeric(df["quantity_ordered"], errors="coerce")
    df["price_each"] = pd.to_numeric(df["price_each"], errors="coerce")

    # Derived columns
    df["sales"] = df["quantity_ordered"] * df["price_each"]
    df["month"] = df["order_date"].dt.to_period("M").astype(str)

    return df.dropna()

df = load_data()

# -----------------------------
# Title
# -----------------------------
st.title("📊 Sales Data Analytics Dashboard")
st.caption("End-to-End Data Pipeline | CSV → Python → Streamlit")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filters")

product_filter = st.sidebar.multiselect(
    "Select Product",
    options=sorted(df["product"].unique()),
    default=sorted(df["product"].unique())
)

month_filter = st.sidebar.multiselect(
    "Select Month",
    options=sorted(df["month"].unique()),
    default=sorted(df["month"].unique())
)

filtered_df = df[
    (df["product"].isin(product_filter)) &
    (df["month"].isin(month_filter))
]

# -----------------------------
# KPI Section
# -----------------------------
total_sales = filtered_df["sales"].sum()
total_orders = filtered_df["order_id"].nunique()
total_quantity = filtered_df["quantity_ordered"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"₹ {total_sales:,.0f}")
col2.metric("🧾 Total Orders", total_orders)
col3.metric("📦 Quantity Sold", int(total_quantity))

st.divider()

# -----------------------------
# Monthly Sales Trend
# -----------------------------
st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .groupby("month")["sales"]
    .sum()
    .reset_index()
    .sort_values("month")
)

st.line_chart(
    monthly_sales.set_index("month")
)

# -----------------------------
# Top Products
# -----------------------------
st.subheader("🏆 Top Products by Sales")

top_products = (
    filtered_df
    .groupby("product")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

st.bar_chart(
    top_products.set_index("product")
)

# -----------------------------
# Data Preview
# -----------------------------
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df.head(100))

# -----------------------------
# Footer
# -----------------------------
st.caption("Built by Varun | Streamlit • Pandas • Data Engineering")
