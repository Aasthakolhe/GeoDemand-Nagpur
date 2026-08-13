# 📍 GeoDemand Nagpur

**Data-driven site selection for retail expansion — pinpointing optimal new coffee shop locations in Nagpur using geospatial analytics, live REST APIs, and population density modeling.**

![Python](https://img.shields.io/badge/Python-Pandas%20%7C%20NumPy-blue)
![APIs](https://img.shields.io/badge/REST%20APIs-Overpass%20%7C%20Nominatim-orange)
![Geospatial](https://img.shields.io/badge/Geospatial-Folium%20%7C%20Haversine-brightgreen)
![Streamlit](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B)

🔗 **[View Live Interactive Dashboard](https://geodemand-nagpur-9zs9bdpk9qgzsnw3owxm4x.streamlit.app/)**

---

## 📌 The Question

*"If a coffee brand wanted to open its next outlet in Nagpur, where should it go?"*

This project answers that question with data instead of guesswork — building a full geospatial analytics pipeline from live API sourcing to an interactive, scored opportunity map covering the entire city.

---

## 🔑 Key Results

- **Analyzed 315 grid points** across Nagpur, scored against **88 real, live-sourced competitor locations** (65 restaurants, 23 cafes) pulled directly from OpenStreetMap
- **Top-ranked location** (21.15° N, 79.08° E — near Sitabuldi/Civil Lines) scored **82.2/100** on the Opportunity Index, combining strong estimated demand with manageable competition
- Identified multiple **underserved high-density pockets** near Sadar (21.18° N, 79.08° E) scoring 79+ despite being adjacent to the city's commercial core — a genuine "hidden opportunity" signal a manual scouting process could easily miss
- Average opportunity score across the city sits at **46.4/100**, meaning the model successfully differentiates strong locations from the rest of the map rather than flattening everything to "good"

---

## 🌐 Real-Time Data via REST APIs
- Integrated the **OpenStreetMap Overpass API** to pull 88 live, real cafe and restaurant locations across Nagpur — no static/downloaded dataset
- Integrated the **Nominatim Geocoding API** to programmatically resolve 12 key Nagpur neighborhoods (Sitabuldi, Dharampeth, Sadar, Civil Lines, and more) into precise coordinates, used as density anchor points
- Built with multi-server retry logic and rate-limit-respecting delays for production-grade reliability, not just a one-shot script

## 🗺️ Geospatial Modeling
- Engineered a **distance-decay population density model** anchored to 12 known commercial/residential hubs, since authoritative ward-level census data for Nagpur is gated behind institutional or paid GIS access
- Implemented the **Haversine formula** from scratch to calculate real-world distances between coordinates on Earth's curved surface — not flat-plane approximations
- Generated a **315-point analytical grid** spanning the full city, scoring every point on estimated demand

## 🎯 Opportunity Scoring
- Calculated competitor density within a **1km walkable radius** for every grid point
- Combined population density (60%) and low competition (40%) into a single weighted **Opportunity Score** — weights are explicit, named variables in the code, not hidden assumptions
- Surfaced the top-ranked, underserved locations for new store placement, ready to explore on the interactive map

## 📊 Interactive Visualization
- Built a live dashboard using **Streamlit** and **Folium**
- Features a dynamic opportunity heatmap, real competitor markers, top-10 recommended location pins with detailed popups, and adjustable filters (top-N locations, minimum score threshold, layer toggles)

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python (Pandas, NumPy)** | Data processing, grid generation, distance calculations |
| **Requests** | REST API integration (Overpass, Nominatim) |
| **Folium** | Interactive map rendering (heatmaps, markers, layers) |
| **Streamlit** | Live, interactive web dashboard |
| **OpenStreetMap Overpass API** | Real-time competitor (cafe/restaurant) location data |
| **OpenStreetMap Nominatim API** | Geocoding neighborhood names to coordinates |

---

## 📂 Repository Contents

| File | Description |
|------|--------------|
| `fetch_nagpur_cafes_restaurants.py` | Step 1 — Pulls real cafe/restaurant data via the Overpass REST API |
| `geocode_nagpur_areas.py` | Step 2 — Geocodes 12 key Nagpur neighborhoods via the Nominatim REST API |
| `estimate_density.py` | Step 3 — Builds a 315-point grid and estimates population density using distance-decay modeling |
| `calculate_opportunity_score.py` | Step 4 — Combines density and competitor data into a final Opportunity Score |
| `build_map.py` | Step 5 — Generates a standalone interactive HTML map |
| `app.py` | Streamlit dashboard source code (live app) |
| `requirements.txt` | Python dependencies |
| `data/nagpur_food_places.csv` | 88 real competitor locations (Overpass API output) |
| `data/nagpur_anchor_points.csv` | 12 geocoded neighborhood hub coordinates (Nominatim API output) |
| `data/nagpur_density_grid.csv` | 315-point grid with estimated population density scores |
| `data/nagpur_opportunity_scores.csv` | Final scored dataset — density, competition, and combined opportunity scores |

---

## 🧠 Methodology & Key Decisions

This project intentionally documents its analytical judgment calls rather than hiding them — reflecting how real-world analytics works when perfect data isn't available:

- **Why a distance-decay model instead of official ward data?** Ward-level and pincode-level population data for Nagpur is gated behind institutional (MIT-only) or paid GIS vendor access. Rather than compromise on data authenticity, this project uses a transparent, documented proxy: relative density estimated from known commercial/residential hub locations.
- **Why 60/40 weighting for density vs. competition?** Foot traffic and population density were judged to matter more than complete market exclusivity for a coffee shop — a stated, reasoned business assumption rather than an unexplained default.
- **Why a 1km competitor radius?** Chosen to represent a realistic walkable catchment area for a cafe or coffee shop.

---

## 📊 Dashboard Preview

The live dashboard includes:
- **KPI cards**: grid points analyzed, existing competitor count, top opportunity score, average nearby competitors
- **Interactive heatmap** of opportunity scores across Nagpur
- **Real competitor markers** (red) and **top recommended locations** (green stars) with detailed popups
- **Adjustable controls**: number of top locations shown, heatmap/competitor layer toggles, minimum score filter
- **Ranked results table** of the best-scoring locations

---

## 🚀 How to Run This Project Locally

```bash
git clone https://github.com/Aasthakolhe/GeoDemand-Nagpur.git
cd GeoDemand-Nagpur
pip install -r requirements.txt

# Re-run the full pipeline (optional - CSVs are already included)
python fetch_nagpur_cafes_restaurants.py
python geocode_nagpur_areas.py
python estimate_density.py
python calculate_opportunity_score.py

# Launch the dashboard
streamlit run app.py
```

---

## 📈 Future Improvements

- Replace the distance-decay proxy with official ward-level census data if/when freely accessible
- Extend the pipeline to support any city by parameterizing the bounding box and neighborhood list
- Add a business-type selector (restaurants, gyms, pharmacies, etc.) instead of a fixed coffee shop focus
- Incorporate foot traffic or transit accessibility data as an additional scoring factor

---

## 🎯 Why This Project

Location intelligence is a real, high-value discipline used by companies like Starbucks, Chipotle, and food-delivery platforms to guide expansion decisions. This project demonstrates that same analytical workflow end-to-end — live API integration, geospatial modeling, transparent handling of data limitations, and an interactive decision-support tool — using Nagpur as a real, grounded case study.

---

## 📬 Contact

**Aastha Kolhe**
📧 aasthakolhe04@gmail.com | [LinkedIn](https://www.linkedin.com/in/aastha-kolhe)

---

⭐ If you found this project useful, consider giving it a star on GitHub!
