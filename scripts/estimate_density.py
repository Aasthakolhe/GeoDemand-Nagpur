import pandas as pd
import numpy as np

# ---------------------------------------------------------
# Step 3: Estimate population density across Nagpur using a
# distance-decay model anchored to known dense neighborhoods.
#
# Why this approach: Official ward/pincode-level population data
# for Nagpur is not freely available (gated behind institutional
# or paid GIS providers). This is a common, defensible workaround
# used when authoritative data isn't accessible - we estimate
# relative density instead of claiming exact population counts.
# ---------------------------------------------------------

# Load our geocoded anchor points from Step 2.5
anchors = pd.read_csv('nagpur_anchor_points.csv')

# Assign each anchor a relative "hub weight" based on general
# knowledge of Nagpur - central/commercial areas are denser than
# outer residential/semi-urban areas. (This is a judgment call we
# make explicit and documented, not hidden.)
hub_weights = {
    "Sitabuldi, Nagpur": 1.0,       # central commercial hub - highest density
    "Sadar, Nagpur": 0.9,
    "Dharampeth, Nagpur": 0.85,
    "Civil Lines, Nagpur": 0.7,
    "Ramdaspeth, Nagpur": 0.8,
    "Pratap Nagar, Nagpur": 0.7,
    "Trimurti Nagar, Nagpur": 0.65,
    "Manish Nagar, Nagpur": 0.6,
    "Nandanvan, Nagpur": 0.55,
    "Wardha Road, Nagpur": 0.5,
    "Hingna, Nagpur": 0.35,          # outer/industrial - lower density
    "Kamptee, Nagpur": 0.3,          # satellite town - lower density
}

anchors['weight'] = anchors['area'].map(hub_weights)

# ---------------------------------------------------------
# Build a grid of points covering Nagpur city
# ---------------------------------------------------------
lat_range = np.arange(21.05, 21.20, 0.01)   # ~15 rows
lon_range = np.arange(78.95, 79.15, 0.01)   # ~20 columns

grid_points = [(lat, lon) for lat in lat_range for lon in lon_range]
grid_df = pd.DataFrame(grid_points, columns=['lat', 'lon'])

# ---------------------------------------------------------
# Haversine distance function (distance in km between two
# lat/lon points on Earth's surface)
# ---------------------------------------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in km
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))

# ---------------------------------------------------------
# For each grid point, calculate an estimated density score:
# sum of (hub_weight / distance) across all anchor points.
# Closer to a high-weight hub = higher estimated density.
# ---------------------------------------------------------
def estimate_density(lat, lon):
    score = 0
    for _, row in anchors.iterrows():
        dist = haversine(lat, lon, row['lat'], row['lon'])
        dist = max(dist, 0.3)  # avoid division by ~0 for points very close to a hub
        score += row['weight'] / dist
    return score

grid_df['density_score'] = grid_df.apply(lambda r: estimate_density(r['lat'], r['lon']), axis=1)

# Normalize to a 0-100 scale for easier interpretation
grid_df['density_score_normalized'] = (
    (grid_df['density_score'] - grid_df['density_score'].min()) /
    (grid_df['density_score'].max() - grid_df['density_score'].min()) * 100
)

print(grid_df.sort_values('density_score_normalized', ascending=False).head(10))

grid_df.to_csv('nagpur_density_grid.csv', index=False)
print("\nSaved to nagpur_density_grid.csv")
print(f"Total grid points: {len(grid_df)}")
