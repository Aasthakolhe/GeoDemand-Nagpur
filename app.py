import pandas as pd
import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# ---------------------------------------------------------
# Page config
# ---------------------------------------------------------
st.set_page_config(
    page_title="GeoDemand Nagpur",
    page_icon="📍",
    layout="wide"
)

# ---------------------------------------------------------
# Custom styling (consistent with the retail project theme)
# ---------------------------------------------------------
st.markdown("""
    <style>
        .hero {
            padding: 24px 30px;
            border-radius: 16px;
            background: linear-gradient(120deg, #1f3a2e 0%, #0f5132 60%, #1a6b47 100%);
            margin-bottom: 18px;
        }
        .hero h1 { color: white; font-size: 32px; margin: 0; }
        .hero p { color: rgba(255,255,255,0.8); font-size: 15px; margin-top: 6px; }

        .kpi-card {
            background: linear-gradient(135deg, #0f5132 0%, #1a6b47 100%);
            padding: 20px; border-radius: 14px; text-align: center;
            box-shadow: 0 4px 14px rgba(0,0,0,0.25);
        }
        .kpi-label {
            font-size: 13px; color: rgba(255,255,255,0.85);
            text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;
        }
        .kpi-value { font-size: 30px; color: white; font-weight: 700; }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
@st.cache_data
def load_data():
    scores = pd.read_csv("nagpur_opportunity_scores.csv")
    places = pd.read_csv("nagpur_food_places.csv")
    return scores, places

scores_df, places_df = load_data()

# ---------------------------------------------------------
# Hero header
# ---------------------------------------------------------
st.markdown("""
    <div class="hero">
        <h1>📍 GeoDemand Nagpur — Coffee Shop Site Selection</h1>
        <p>Identifying optimal new coffee shop locations using population density modeling and competitor analysis</p>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# KPI row
# ---------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Grid Points Analyzed</div>
        <div class="kpi-value">{len(scores_df)}</div></div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Existing Cafes/Restaurants</div>
        <div class="kpi-value">{len(places_df)}</div></div>""", unsafe_allow_html=True)
with k3:
    best_score = scores_df['opportunity_score'].max()
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Top Opportunity Score</div>
        <div class="kpi-value">{best_score:.1f}</div></div>""", unsafe_allow_html=True)
with k4:
    avg_competitors = scores_df['competitor_count'].mean()
    st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Avg Competitors Nearby</div>
        <div class="kpi-value">{avg_competitors:.1f}</div></div>""", unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------------
# Sidebar controls
# ---------------------------------------------------------
st.sidebar.header("🔍 Controls")
top_n = st.sidebar.slider("Number of top locations to show", 5, 30, 10)
show_heatmap = st.sidebar.checkbox("Show opportunity heatmap", value=True)
show_competitors = st.sidebar.checkbox("Show existing competitors", value=True)
min_score = st.sidebar.slider("Minimum opportunity score filter", 0, 100, 0)

filtered_scores = scores_df[scores_df['opportunity_score'] >= min_score]
top_locations = filtered_scores.sort_values('opportunity_score', ascending=False).head(top_n)

# ---------------------------------------------------------
# Map
# ---------------------------------------------------------
st.markdown("### 🗺️ Interactive Opportunity Map")

nagpur_center = [21.1458, 79.0882]
m = folium.Map(location=nagpur_center, zoom_start=12, tiles='CartoDB positron')

if show_heatmap:
    heat_data = [[r['lat'], r['lon'], r['opportunity_score']] for _, r in scores_df.iterrows()]
    HeatMap(heat_data, radius=25, blur=20, max_zoom=13).add_to(m)

if show_competitors:
    for _, row in places_df.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=3, color='crimson', fill=True, fill_opacity=0.6,
            popup=f"{row['name']} ({row['type']})"
        ).add_to(m)

for i, (_, row) in enumerate(top_locations.iterrows(), start=1):
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=(f"<b>Rank #{i}</b><br>Score: {row['opportunity_score']:.1f}<br>"
               f"Competitors nearby: {int(row['competitor_count'])}"),
        icon=folium.Icon(color='green', icon='star')
    ).add_to(m)

st_folium(m, use_container_width=True, height=550)

# ---------------------------------------------------------
# Top locations table
# ---------------------------------------------------------
st.markdown("### 🏆 Top Recommended Locations")
display_table = top_locations[['lat', 'lon', 'density_score_normalized', 'competitor_count', 'opportunity_score']].reset_index(drop=True)
display_table.index += 1
display_table.columns = ['Latitude', 'Longitude', 'Density Score', 'Nearby Competitors', 'Opportunity Score']
st.dataframe(display_table.style.format({
    'Latitude': '{:.4f}', 'Longitude': '{:.4f}',
    'Density Score': '{:.1f}', 'Opportunity Score': '{:.1f}'
}), use_container_width=True)

st.markdown("---")
st.caption(
    "Built with Python, OpenStreetMap Overpass API, Nominatim Geocoding API, and Streamlit. "
    "Population density estimated via distance-decay modeling due to unavailability of free ward-level census data. "
    "By Aastha Kolhe"
)
