import streamlit as st
import plotly.express as px

from utils.load_data import load_data

df = load_data()
# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Analytics Dashboard")
st.markdown("### Interactive Business Intelligence Dashboard")

# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------
st.sidebar.header("🔍 Filters")

region = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

category = st.sidebar.multiselect(
    "Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

segment = st.sidebar.multiselect(
    "Segment",
    options=sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

state = st.sidebar.multiselect(
    "State",
    options=sorted(df["State"].unique()),
    default=sorted(df["State"].unique())
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Segment"].isin(segment)) &
    (df["State"].isin(state))
]

# -------------------------------------------------
# KPI Cards
# -------------------------------------------------
sales = filtered_df["Sales"].sum()
profit = filtered_df["Profit"].sum()
orders = filtered_df["Order ID"].nunique()
quantity = filtered_df["Quantity"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"${sales:,.0f}")
col2.metric("📈 Total Profit", f"${profit:,.0f}")
col3.metric("📦 Orders", orders)
col4.metric("🛒 Quantity Sold", quantity)

st.divider()

# -------------------------------------------------
# Row 1 Charts
# -------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    sales_category = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        sales_category,
        x="Category",
        y="Sales",
        color="Category",
        title="Sales by Category"
    )

    st.plotly_chart(fig, width="stretch")

with col2:
    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        title="Sales by Region",
        hole=0.4
    )

    st.plotly_chart(fig, width="stretch")

st.divider()

# -------------------------------------------------
# Monthly Sales Trend
# -------------------------------------------------

st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .groupby(filtered_df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

fig = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales"
)

st.plotly_chart(fig, width="stretch")

st.divider()

# -------------------------------------------------
# Top 10 Products
# -------------------------------------------------

st.subheader("🏆 Top 10 Products by Sales")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    color="Sales",
    title="Top 10 Products"
)

fig.update_layout(
    yaxis={
        "categoryorder": "total ascending"
    }
)

st.plotly_chart(fig, width="stretch")

st.divider()

# -------------------------------------------------
# Sales vs Profit
# -------------------------------------------------

st.subheader("💹 Sales vs Profit")

fig = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    color="Category",
    size="Quantity",
    hover_name="Product Name",
    title="Sales vs Profit Analysis"
)

st.plotly_chart(fig, width="stretch")

st.divider()

# -------------------------------------------------
# Top 10 States
# -------------------------------------------------

st.subheader("🌎 Top 10 States by Sales")

state_sales = (
    filtered_df.groupby("State")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    state_sales,
    x="State",
    y="Sales",
    color="Sales",
    title="Top States by Sales"
)

st.plotly_chart(fig, width="stretch")

st.divider()

# -------------------------------------------------
# Raw Data
# -------------------------------------------------

st.subheader("📄 Filtered Dataset")

st.dataframe(filtered_df, width="stretch")

st.divider()

# -------------------------------------------------
# Download Button
# -------------------------------------------------

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)