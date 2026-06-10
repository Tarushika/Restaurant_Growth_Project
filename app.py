import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Restaurant Growth Dashboard",
    layout="wide"
)

# Load Dataset
df = pd.read_csv("final_restaurant_analysis.csv")

# Title
st.title("🍽 Restaurant Growth Potential Dashboard")

st.markdown(
"""
This dashboard analyzes restaurant performance,
growth potential, profitability, and cluster segmentation.
"""
)

# Sidebar Filter

st.sidebar.header("Filters")

cluster = st.sidebar.selectbox(
    "Select Cluster",
    ["All"] + list(df["ClusterLabel"].unique())
)

if cluster != "All":
    df = df[df["ClusterLabel"] == cluster]

# KPIs

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Restaurants",
    len(df)
)

col2.metric(
    "Average Revenue",
    f"${df['TotalRevenue'].mean():,.0f}"
)

col3.metric(
    "Average Profit",
    f"{df['TotalProfit'].mean():.2f}"
)

col4.metric(
    "Average GPS",
    f"{df['GrowthPotentialScore'].mean():.2f}"
)

# Cluster Distribution

st.subheader("Restaurant Cluster Distribution")

cluster_count = (
    df["ClusterLabel"]
    .value_counts()
    .reset_index()
)

cluster_count.columns = [
    "Cluster",
    "Count"
]

fig1 = px.bar(
    cluster_count,
    x="Cluster",
    y="Count",
    title="Restaurants by Cluster"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# Growth Potential

st.subheader(
    "Average Growth Potential by Cluster"
)

gps_cluster = (
    df.groupby("ClusterLabel")
    ["GrowthPotentialScore"]
    .mean()
    .reset_index()
)

fig2 = px.bar(
    gps_cluster,
    x="ClusterLabel",
    y="GrowthPotentialScore",
    title="Growth Potential Score"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# Top Restaurants

st.subheader(
    "Top 10 Growth Potential Restaurants"
)

top10 = df.sort_values(
    "GrowthPotentialScore",
    ascending=False
).head(10)

st.dataframe(
    top10[
        [
            "RestaurantName",
            "GrowthPotentialScore",
            "Recommendation"
        ]
    ]
)

# Revenue by Cuisine

st.subheader(
    "Revenue by Cuisine Type"
)

cuisine = (
    df.groupby("CuisineType")
    ["TotalRevenue"]
    .sum()
    .reset_index()
)

fig3 = px.bar(
    cuisine,
    x="CuisineType",
    y="TotalRevenue",
    title="Cuisine Revenue"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# Full Dataset

st.subheader("Dataset")

st.dataframe(df)