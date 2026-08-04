# 📍 GeoDemand Nagpur

**A data-driven site selection tool for identifying optimal new coffee shop locations in Nagpur, India — built with geospatial analytics, public REST APIs, and population density modeling.**

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Folium](https://img.shields.io/badge/Folium-Mapping-77B829?logo=leaflet&logoColor=white)](https://python-visualization.github.io/folium/)
[![OpenStreetMap](https://img.shields.io/badge/Data-OpenStreetMap-7EBC6F?logo=openstreetmap&logoColor=white)](https://www.openstreetmap.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🧭 Overview

Where should a new coffee shop open in Nagpur? **GeoDemand Nagpur** answers that question quantitatively instead of anecdotally.

The pipeline geocodes 12 well-known Nagpur neighborhoods, models relative population density across a 315-point city grid using a distance-decay algorithm, pulls **88 real existing cafes/restaurants** from OpenStreetMap, and combines both signals into a single **Opportunity Score** — surfacing the pockets of the city with high foot-traffic potential and low existing competition. Results are rendered as an interactive Folium heatmap and a full Streamlit dashboard.

> 🏆 **Top opportunity score found: 82.2/100** — a high-density zone with zero nearby competitors.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🌍 **Automated Geocoding** | Converts 12 named Nagpur neighborhoods into precise lat/lon anchors via the Nominatim API |
| 📊 **Population Density Modeling** | Distance-decay model estimates relative density across a 315-point grid when authoritative census data isn't freely available |
| ☕ **Live Competitor Data** | Pulls real cafes & restaurants (88 found: 65 restaurants, 23 cafes) from OpenStreetMap via the Overpass API |
| 🧮 **Opportunity Scoring Engine** | Weighted formula (60% density, 40% low competition) ranks every grid point city-wide |
| 🗺️ **Interactive Map** | Toggleable Folium layers: opportunity heatmap, competitor markers, top-10 recommended sites |
| 📈 **Streamlit Dashboard** | Live KPIs, adjustable filters, and a sortable table of ranked locations |

---

## 🗺️ Live Demo

The interactive map (`nagpur_opportunity_map.html`) visualizes three layers you can toggle independently:

- 🔥 **Opportunity Heatmap** — citywide density of scores
- 🔴 **Existing Competitors** — every cafe/restaurant currently in Nagpur
- ⭐ **Top 10 Recommended Locations** — best new-site candidates, ranked

*(Screenshot below — or clone the repo and open the HTML file directly.)*

---

## 🏗️ How It Works — Pipeline

```
1. geocode_nagpur_areas.py        →  nagpur_anchor_points.csv
   Geocodes 12 Nagpur neighborhoods (Nominatim API)

2. estimate_density.py            →  nagpur_density_grid.csv
   Builds a 315-point city grid, estimates relative population
   density via a distance-decay model anchored to known hubs

3. fetch_nagpur_cafes_restaurants.py  →  nagpur_food_places.csv
   Pulls live cafe/restaurant data for Nagpur (Overpass API)

4. calculate_opportunity_score.py →  nagpur_opportunity_scores.csv
   Counts competitors within 1km of each grid point, then computes:
      Opportunity Score = 0.6 × Density Score + 0.4 × (100 − Competitor Score)

5. build_map.py                   →  nagpur_opportunity_map.html
   Renders the final interactive Folium map

6. app.py
   Streamlit dashboard wrapping the full analysis in a live UI
```

Every modeling decision — hub weights, scoring formula, distance thresholds — is documented directly in code comments rather than hidden behind a black box.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation

```bash
git clone https://github.com/Aasthakolhe/GeoDemand-Nagpur.git
cd GeoDemand-Nagpur
pip install -r requirements.txt
```

### Run the pipeline

```bash
python scripts/geocode_nagpur_areas.py
python scripts/estimate_density.py
python scripts/fetch_nagpur_cafes_restaurants.py
python scripts/calculate_opportunity_score.py
python scripts/build_map.py
```

### Launch the dashboard

```bash
streamlit run app.py
```

---

## 🛠️ Tech Stack

- **Python** — pandas, numpy for data processing
- **Streamlit** + **streamlit-folium** — interactive dashboard
- **Folium** — map rendering & heatmaps
- **OpenStreetMap Nominatim API** — geocoding
- **OpenStreetMap Overpass API** — live competitor/POI data
- **Haversine distance** — geospatial proximity calculations

---

## 📂 Project Structure

```
GeoDemand-Nagpur/
├── data/                          # Generated CSV outputs at each pipeline stage
├── output/                        # Final interactive HTML map
├── scripts/                       # Pipeline scripts (geocode → density → score → map)
├── app.py                         # Streamlit dashboard
├── requirements.txt
├── LICENSE
└── README.md
```

---

## 📌 Methodology Notes

- **Why distance-decay density instead of census data?** Ward/pincode-level population data for Nagpur isn't freely available outside paid GIS providers. A distance-decay model anchored to well-known commercial hubs is a transparent, defensible proxy for *relative* density — this project estimates relative opportunity, not exact population counts.
- **Why 60/40 weighting?** A judgment call, documented in `calculate_opportunity_score.py`, favoring foot-traffic potential slightly over pure white-space — easily tunable for different business types.
- **Data freshness:** Competitor data reflects a live OpenStreetMap snapshot at the time of the last pipeline run.

---

## 🔮 Future Improvements

- [ ] Incorporate real foot-traffic or transit-stop data
- [ ] Add rent/commercial real-estate cost layer
- [ ] Support other cities via config-driven anchor lists
- [ ] Cache Overpass/Nominatim responses to reduce repeated API calls

---

## 👩‍💻 Project By

**Aastha Kolhe**

If you find this project useful, consider ⭐ starring the repo!

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
