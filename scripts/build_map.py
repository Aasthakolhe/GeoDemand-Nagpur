import pandas as pd
import folium
from folium.plugins import HeatMap

# ---------------------------------------------------------
# Step 5: Build an interactive map showing:
#  1. A heatmap of opportunity scores across Nagpur
#  2. Markers for existing cafes/restaurants (competitors)
#  3. Top-ranked markers for the best new-location candidates
# ---------------------------------------------------------

# Load our results
scores_df = pd.read_csv('nagpur_opportunity_scores.csv')
places_df = pd.read_csv('nagpur_food_places.csv')

# Center the map on Nagpur
nagpur_center = [21.1458, 79.0882]
m = folium.Map(location=nagpur_center, zoom_start=12, tiles='CartoDB positron')

# ---------------------------------------------------------
# Layer 1: Heatmap of opportunity scores
# ---------------------------------------------------------
heat_data = [
    [row['lat'], row['lon'], row['opportunity_score']]
    for _, row in scores_df.iterrows()
]
HeatMap(heat_data, radius=25, blur=20, max_zoom=13,
        name='Opportunity Heatmap').add_to(m)

# ---------------------------------------------------------
# Layer 2: Existing competitors (small red dots)
# ---------------------------------------------------------
competitor_layer = folium.FeatureGroup(name='Existing Cafes/Restaurants')
for _, row in places_df.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=3,
        color='crimson',
        fill=True,
        fill_opacity=0.6,
        popup=f"{row['name']} ({row['type']})"
    ).add_to(competitor_layer)
competitor_layer.add_to(m)

# ---------------------------------------------------------
# Layer 3: Top 10 recommended new locations (gold stars)
# ---------------------------------------------------------
top_10 = scores_df.sort_values('opportunity_score', ascending=False).head(10)

recommend_layer = folium.FeatureGroup(name='Top 10 Recommended Locations')
for i, (_, row) in enumerate(top_10.iterrows(), start=1):
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=(
            f"<b>Rank #{i}</b><br>"
            f"Opportunity Score: {row['opportunity_score']:.1f}<br>"
            f"Nearby Competitors: {int(row['competitor_count'])}<br>"
            f"Density Score: {row['density_score_normalized']:.1f}"
        ),
        icon=folium.Icon(color='green', icon='star')
    ).add_to(recommend_layer)
recommend_layer.add_to(m)

# Layer control so users can toggle layers on/off
folium.LayerControl().add_to(m)

m.save('nagpur_opportunity_map.html')
print("Map saved to nagpur_opportunity_map.html - open this file in your browser to view it!")
