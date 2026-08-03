import requests
import pandas as pd
import time

# ---------------------------------------------------------
# Overpass API: free access to OpenStreetMap data, no API key needed
# We try a couple of different servers in case one is busy/down
# ---------------------------------------------------------
overpass_servers = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.openstreetmap.ru/api/interpreter",
]

# Nagpur's approximate bounding box (south, west, north, east)
bbox = "21.05,78.95,21.20,79.15"

query = f"""
[out:json][timeout:60];
(
  node["amenity"="cafe"]({bbox});
  node["amenity"="restaurant"]({bbox});
  node["shop"="coffee"]({bbox});
);
out body;
"""

data = None

for server in overpass_servers:
    print(f"Trying server: {server} ...")
    try:
        response = requests.get(
            server,
            params={'data': query},
            headers={'User-Agent': 'GeoDemand-Nagpur-Project/1.0'},
            timeout=60
        )
        print(f"Status code: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()
                print("Success! Got valid JSON response.")
                break
            except ValueError:
                print("Server responded but not with valid JSON. Trying next server...")
                print("First 200 chars of response:", response.text[:200])
        else:
            print(f"Server returned status {response.status_code}. Trying next server...")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}. Trying next server...")

    time.sleep(2)  # small pause before trying next server

if data is None:
    print("\n❌ All servers failed. Please check your internet connection and try again in a few minutes.")
else:
    rows = []
    for el in data.get('elements', []):
        tags = el.get('tags', {})
        rows.append({
            'name': tags.get('name', 'Unnamed'),
            'lat': el.get('lat'),
            'lon': el.get('lon'),
            'type': tags.get('amenity', tags.get('shop')),
            'cuisine': tags.get('cuisine', None)
        })

    df = pd.DataFrame(rows)
    print(f"\nTotal cafes/restaurants found in Nagpur: {len(df)}")
    print(df['type'].value_counts())
    print(df.head(10))

    df.to_csv('nagpur_food_places.csv', index=False)
    print("\nSaved to nagpur_food_places.csv")