import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Zomato Market Intelligence",
    page_icon="🍽️",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.main {
    background-color: #fafafa;
}

[data-testid="stMetric"] {
    background: white;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BASE_DIR /
    "data" /
    "processed" /
    "final_zomato.csv"
)

df = pd.read_csv(DATA_PATH)

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🔍 Dashboard Filters")

selected_location = st.sidebar.selectbox(
    "Location",
    ["All"] + sorted(df["location"].dropna().unique())
)

selected_online = st.sidebar.selectbox(
    "Online Order",
    ["All", "Yes", "No"]
)

# ==================================================
# FILTER DATA
# ==================================================

filtered_df = df.copy()

if selected_location != "All":
    filtered_df = filtered_df[
        filtered_df["location"] == selected_location
    ]

if selected_online != "All":
    filtered_df = filtered_df[
        filtered_df["online_order"] == selected_online
    ]

# ==================================================
# HERO SECTION
# ==================================================

st.markdown("""
<div style="
background: linear-gradient(90deg,#E23744,#FF6B6B);
padding:25px;
border-radius:20px;
color:white;
">

<h1>🍽️ Zomato Market Intelligence Platform</h1>

<p>
Analyze Bengaluru restaurant trends, cuisine demand,
pricing patterns and restaurant success metrics.
</p>

</div>
""", unsafe_allow_html=True)

st.write("")

# ==================================================
# KPI SECTION
# ==================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="
    background:#1E1E2F;
    padding:20px;
    border-radius:15px;
    text-align:center;
    border-left:5px solid #E23744;
    ">
    <h4>🍽 Restaurants</h4>
    <h2>{filtered_df.shape[0]:,}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
    background:#1E1E2F;
    padding:20px;
    border-radius:15px;
    text-align:center;
    border-left:5px solid #E23744;
    ">
    <h4>📍 Locations</h4>
    <h2>{filtered_df['location'].nunique()}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
    background:#1E1E2F;
    padding:20px;
    border-radius:15px;
    text-align:center;
    border-left:5px solid #E23744;
    ">
    <h4>⭐ Avg Rating</h4>
    <h2>{round(filtered_df['rate'].mean(), 2)}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="
    background:#1E1E2F;
    padding:20px;
    border-radius:15px;
    text-align:center;
    border-left:5px solid #E23744;
    ">
    <h4>💰 Avg Cost</h4>
    <h2>₹{round(filtered_df['approx_cost(for two people)'].mean())}</h2>
    </div>
    """, unsafe_allow_html=True)

# ==================================================
# TABS
# ==================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Market Overview",
    "📍 Location Intelligence",
    "🏆 Restaurant Success",
    "🍜 Cuisine Intelligence",
    "📈 Market Expansion Advisor"
])

# ==================================================
# TAB 1
# ==================================================

with tab1:

    colA, colB = st.columns(2)

    with colA:

        st.subheader("📍 Top Restaurant Locations")

        top_locations = (
            df["location"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        top_locations.columns = [
            "Location",
            "Restaurant Count"
        ]

        fig1 = px.bar(
            top_locations,
            x="Restaurant Count",
            y="Location",
            orientation="h",
            text="Restaurant Count",
            color="Restaurant Count",
            color_continuous_scale="Reds"
        )

        fig1.update_layout(
            height=500,
            yaxis=dict(categoryorder="total ascending")
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with colB:

        st.subheader("🍜 Top Cuisines")

        cuisine_counts = (
            df["cuisines"]
            .dropna()
            .str.split(",")
            .explode()
            .str.strip()
            .value_counts()
            .head(10)
            .reset_index()
        )

        cuisine_counts.columns = [
            "Cuisine",
            "Count"
        ]

        fig2 = px.bar(
            cuisine_counts,
            x="Count",
            y="Cuisine",
            orientation="h",
            text="Count",
            color="Count",
            color_continuous_scale="Reds"
        )

        fig2.update_layout(
            height=500,
            yaxis=dict(categoryorder="total ascending")
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

# ==================================================
# TAB 2 - LOCATION INTELLIGENCE
# ==================================================

with tab2:

    st.subheader(
        f"📍 Location Analysis : {selected_location}"
    )

    if selected_location == "All":
        st.info(
            "Please select a location from the sidebar to view location-specific insights."
        )

    else:

        # ------------------------------------------
        # KPI INSIGHTS
        # ------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div style="
            background:#1E1E2F;
            padding:20px;
            border-radius:15px;
            text-align:center;
            border-left:5px solid #E23744;
            ">
            <h4 style="color:white;">🍽 Restaurants</h4>
            <h2 style="color:white;">{filtered_df.shape[0]}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="
            background:#1E1E2F;
            padding:20px;
            border-radius:15px;
            text-align:center;
            border-left:5px solid #E23744;
            ">
            <h4 style="color:white;">⭐ Average Rating</h4>
            <h2 style="color:white;">{round(filtered_df['rate'].mean(),2)}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style="
            background:#1E1E2F;
            padding:20px;
            border-radius:15px;
            text-align:center;
            border-left:5px solid #E23744;
            ">
            <h4 style="color:white;">💰 Average Cost</h4>
            <h2 style="color:white;">₹{round(filtered_df['approx_cost(for two people)'].mean())}</h2>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # ------------------------------------------
        # AVERAGE RATING BY COST RANGE
        # ------------------------------------------

        st.subheader(
            "⭐ Average Rating by Cost Range"
        )

        cost_analysis = filtered_df.copy()

        cost_analysis = cost_analysis.dropna(
            subset=[
                "approx_cost(for two people)",
                "rate"
            ]
        )

        cost_analysis["Cost Range"] = pd.cut(
            cost_analysis["approx_cost(for two people)"],
            bins=[0, 300, 600, 900, 1200, 5000],
            labels=[
                "₹0-300",
                "₹301-600",
                "₹601-900",
                "₹901-1200",
                "₹1200+"
            ]
        )

        rating_by_cost = (
            cost_analysis
            .groupby("Cost Range")["rate"]
            .mean()
            .reset_index()
        )

        fig_cost = px.bar(
            rating_by_cost,
            x="Cost Range",
            y="rate",
            text="rate",
            title=f"Average Rating by Cost Range in {selected_location}",
            color="rate",
            color_continuous_scale="Reds"
        )

        fig_cost.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside"
        )

        fig_cost.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_cost,
            use_container_width=True
        )

        st.divider()

        # ------------------------------------------
        # TOP CUISINES IN LOCATION
        # ------------------------------------------

        st.subheader(
            f"🍜 Popular Cuisines in {selected_location}"
        )

        cuisine_counts = (
            filtered_df["cuisines"]
            .dropna()
            .str.split(",")
            .explode()
            .str.strip()
            .value_counts()
            .head(10)
            .reset_index()
        )

        cuisine_counts.columns = [
            "Cuisine",
            "Count"
        ]

        fig_cuisine = px.bar(
            cuisine_counts,
            x="Count",
            y="Cuisine",
            orientation="h",
            text="Count",
            color="Count",
            color_continuous_scale="Reds"
        )

        fig_cuisine.update_layout(
            height=500,
            yaxis=dict(
                categoryorder="total ascending"
            )
        )

        st.plotly_chart(
            fig_cuisine,
            use_container_width=True
        )

        st.divider()

        # ------------------------------------------
        # TOP RESTAURANTS IN LOCATION
        # ------------------------------------------

        st.subheader(
            f"🏆 Top Restaurants in {selected_location}"
        )

        top_restaurants = (
            filtered_df[
                [
                    "name",
                    "rate",
                    "votes",
                    "approx_cost(for two people)"
                ]
            ]
            .sort_values(
                ["rate", "votes"],
                ascending=False
            )
            .head(10)
        )

        st.dataframe(
            top_restaurants,
            use_container_width=True
        )
# ==================================================
# TAB 3
# ==================================================

with tab3:

    st.subheader(
        "🏆 Top Restaurants by Success Score"
    )

    if "success_score" in filtered_df.columns:

        leaderboard = (
            filtered_df[
                [
                    "name",
                    "location",
                    "rate",
                    "votes",
                    "success_score"
                ]
            ]
            .sort_values(
                "success_score",
                ascending=False
            )
            .head(20)
        )

        st.dataframe(
            leaderboard,
            use_container_width=True
        )

# ==================================================
# TAB 4 - CUISINE INTELLIGENCE
# ==================================================

with tab4:

    st.subheader("🍜 Cuisine Intelligence")

    cuisine_analysis = (
        df["cuisines"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
        .head(15)
        .reset_index()
    )

    cuisine_analysis.columns = [
        "Cuisine",
        "Count"
    ]

    fig_cuisine = px.bar(
        cuisine_analysis,
        x="Count",
        y="Cuisine",
        orientation="h",
        text="Count",
        color="Count",
        color_continuous_scale="Reds"
    )

    fig_cuisine.update_layout(
        height=600,
        yaxis=dict(
            categoryorder="total ascending"
        )
    )

    st.plotly_chart(
        fig_cuisine,
        use_container_width=True
    )

    st.info(
        "North Indian, Chinese and South Indian cuisines dominate Bengaluru's restaurant market."
    )

    # ==================================================
# TAB 5 - MARKET EXPANSION ADVISOR
# ==================================================

with tab5:

    st.subheader(
        "📈 Market Expansion Advisor"
    )

    st.markdown(
        """
        Select a cuisine and budget.
        The platform will recommend the best locations
        for opening a restaurant.
        """
    )

    cuisine_options = sorted(
        df["cuisines"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .unique()
    )

    selected_cuisine = st.selectbox(
        "Select Cuisine",
        cuisine_options
    )

    budget = st.slider(
        "Budget for Two (₹)",
        min_value=100,
        max_value=3000,
        value=1000,
        step=100
    )

    if st.button("Generate Recommendations"):

        temp = df.copy()

        temp = temp[
            temp["cuisines"]
            .str.contains(
                selected_cuisine,
                case=False,
                na=False
            )
        ]

        temp = temp[
            temp["approx_cost(for two people)"]
            <= budget
        ]

        recommendations = (
            temp.groupby("location")
            .agg({
                "rate": "mean",
                "votes": "mean",
                "success_score": "mean"
            })
            .reset_index()
        )

        recommendations["score"] = (
            recommendations["success_score"] * 0.8
            +
            (
                recommendations["votes"]
                /
                recommendations["votes"].max()
            ) * 0.2
        )

        recommendations = recommendations.sort_values(
            "score",
            ascending=False
        ).head(10)

        st.success(
            f"Top locations for {selected_cuisine} restaurants under ₹{budget}"
        )

        st.dataframe(
            recommendations,
            use_container_width=True
        )
# ==================================================
# DATA PREVIEW
# ==================================================

with st.expander("📄 Dataset Preview"):
    st.dataframe(
        filtered_df.head(20),
        use_container_width=True
    )

st.markdown("---")

st.caption(
    "Built with Streamlit, Plotly, Pandas | Zomato Market Intelligence"
)
