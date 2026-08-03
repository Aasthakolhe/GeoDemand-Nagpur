import pandas as pd
import numpy as np

# ---------------------------------------------------------
# Step 4: Combine population density with competitor density
# to produce a final "Opportunity Score" for each grid point.
#
# Logic: A good location = high estimated population density
#        AND low nearby competitor density.
# ---------------------------------------------------------

# Load our previous outputs
density_df = pd.read_csv('nagpur_density_grid.csv')
places_df = pd.read_csv('nagpur_food_places.csv')

# Haversine distance function (same as Step 3)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in km
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))

# ---------------------------------------------------------
# For each grid point, count how many existing cafes/restaurants
# fall within a 1km radius - this represents "competition level"
# ---------------------------------------------------------
def count_nearby_competitors(lat, lon, radius_km=1.0):
    dists = haversine(lat, lon, places_df['lat'].values, places_df['lon'].values)
    return int((dists <= radius_km).sum())

print("Calculating competitor counts for each grid point (this may take ~30-60 seconds)...")
density_df['competitor_count'] = density_df.apply(
    lambda r: count_nearby_competitors(r['lat'], r['lon']), axis=1
)

# ---------------------------------------------------------
# Normalize competitor count to a 0-100 scale (inverted, since
# FEWER competitors = better opportunity)
# ---------------------------------------------------------
max_competitors = density_df['competitor_count'].max()
if max_competitors > 0:
    density_df['competitor_score'] = 100 - (density_df['competitor_count'] / max_competitors * 100)
else:
    density_df['competitor_score'] = 100

# ---------------------------------------------------------
# Final Opportunity Score: weighted combination of
# population density (60%) and low competition (40%)
# These weights are a judgment call - documented, not hidden.
# ---------------------------------------------------------
density_df['opportunity_score'] = (
    0.6 * density_df['density_score_normalized'] +
    0.4 * density_df['competitor_score']
)

# Sort to find the best opportunities
top_opportunities = density_df.sort_values('opportunity_score', ascending=False).head(15)

print("\n=== TOP 15 OPPORTUNITY LOCATIONS FOR A NEW COFFEE SHOP IN NAGPUR ===\n")
print(top_opportunities[['lat', 'lon', 'density_score_normalized', 'competitor_count', 'opportunity_score']].to_string(index=False))

density_df.to_csv('nagpur_opportunity_scores.csv', index=False)
print("\nSaved full results to nagpur_opportunity_scores.csv")
