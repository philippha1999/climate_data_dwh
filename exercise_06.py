import requests

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

print(response.status_code)
print(response.json())