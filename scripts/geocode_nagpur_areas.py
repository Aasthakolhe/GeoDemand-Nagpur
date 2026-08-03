import requests
import pandas as pd
import time

# ---------------------------------------------------------
# Nominatim API: free geocoding service by OpenStreetMap
# Converts place names -> exact latitude/longitude coordinates
# No API key needed, but they require a descriptive User-Agent
# and a max of 1 request per second (we respect that with time.sleep)
# ---------------------------------------------------------

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# Well-known neighborhoods/areas in Nagpur we want exact coordinates for.
# These will act as "anchor points" for our population density model in Step 3.
nagpur_areas = [
    "Sitabuldi, Nagpur",
    "Dharampeth, Nagpur",
    "Sadar, Nagpur",
    "Civil Lines, Nagpur",
    "Ramdaspeth, Nagpur",
    "Manish Nagar, Nagpur",
    "Wardha Road, Nagpur",
    "Hingna, Nagpur",
    "Kamptee, Nagpur",
    "Trimurti Nagar, Nagpur",
    "Pratap Nagar, Nagpur",
    "Nandanvan, Nagpur",
]

results = []

for area in nagpur_areas:
    print(f"Geocoding: {area} ...")
    try:
        response = requests.get(
            NOMINATIM_URL,
            params={'q': area, 'format': 'json', 'limit': 1},
            headers={'User-Agent': 'GeoDemand-Nagpur-Project/1.0 (student project)'},
            timeout=15
        )
        data = response.json()

        if data:
            results.append({
                'area': area,
                'lat': float(data[0]['lat']),
                'lon': float(data[0]['lon'])
            })
            print(f"  -> Found: {data[0]['lat']}, {data[0]['lon']}")
        else:
            print(f"  -> No result found for {area}")

    except requests.exceptions.RequestException as e:
        print(f"  -> Failed: {e}")

    time.sleep(1.2)  # respectful delay - Nominatim's usage policy asks for max 1 request/sec

anchors_df = pd.DataFrame(results)
print("\nFinal anchor points:")
print(anchors_df)

anchors_df.to_csv('nagpur_anchor_points.csv', index=False)
print("\nSaved to nagpur_anchor_points.csv")
