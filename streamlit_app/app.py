import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Data Dashboard")

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
@st.cache_resource
def get_engine():
    engine = create_engine(
        "mysql+pymysql://sales_user:sales123@localhost:3306/sales_pipeline"
    )
    return engine

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    query = "SELECT * FROM sales_data"
    engine = get_engine()
    df = pd.read_sql(query, engine)
    return df

df = load_data()

# -------------------------------
# DATA CLEANING
# -------------------------------
df["quantity_ordered"] = pd.to_numeric(df["quantity_ordered"], errors="coerce")
df["price_each"] = pd.to_numeric(df["price_each"], errors="coerce")
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

df.dropna(inplace=True)

df["sales"] = df["quantity_ordered"] * df["price_each"]
df["month"] = df["order_date"].dt.to_period("M").astype(str)

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("🔍 Filters")

product_filter = st.sidebar.multiselect(
    "Select Product(s)",
    options=sorted(df["product"].unique()),
    default=sorted(df["product"].unique())[:5]
)

month_filter = st.sidebar.multiselect(
    "Select Month(s)",
    options=sorted(df["month"].unique()),
    default=sorted(df["month"].unique())
)

filtered_df = df[
    (df["product"].isin(product_filter)) &
    (df["month"].isin(month_filter))
]

# -------------------------------
# KPI METRICS
# -------------------------------
total_sales = filtered_df["sales"].sum()
total_orders = filtered_df["order_id"].nunique()
total_quantity = filtered_df["quantity_ordered"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"₹ {total_sales:,.0f}")
col2.metric("🧾 Total Orders", total_orders)
col3.metric("📦 Quantity Sold", int(total_quantity))

st.divider()

# -------------------------------
# SALES BY MONTH
# -------------------------------
st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .groupby("month")["sales"]
    .sum()
    .reset_index()
    .sort_values("month")
)

st.line_chart(
    monthly_sales,
    x="month",
    y="sales",
    use_container_width=True
)

# -------------------------------
# TOP PRODUCTS
# -------------------------------
st.subheader("🏆 Top 10 Products by Sales")

top_products = (
    filtered_df
    .groupby("product")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top_products)

# -------------------------------
# DATA PREVIEW
# -------------------------------
st.subheader("📄 Data Preview")
st.dataframe(filtered_df.head(50), use_container_width=True)

# -------------------------------
# DOWNLOAD BUTTON
# -------------------------------
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)

st.success("✅ Dashboard loaded successfully")
