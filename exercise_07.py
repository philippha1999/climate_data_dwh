import json
import requests
from pathlib import Path


def parse_daily(data):
    dates = data["daily"]["time"]
    temps = data["daily"]["temperature_2m_max"]
    latitude = data["latitude"]
    longitude = data["longitude"]

    rows = []
    for i in range(len(dates)):
        row = {
            "date": dates[i],
            "temp_max": temps[i],
            "latitude": latitude,
            "longitude": longitude,
        }
        rows.append(row)

    return rows


url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": 50.11,
    "longitude": 8.68,
    "start_date": "2026-09-01",
    "end_date": "2026-09-07",
    "daily": "temperature_2m_max",
    "timezone": "Europe/Berlin",
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)

    raw_file = raw_dir / "open_meteo_frankfurt_2026-09-01_2026-09-07.json"
    with open(raw_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    rows = parse_daily(data)
    for row in rows:
        print(row)
else:
    print("Request failed:", response.status_code)