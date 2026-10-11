response = {
    "latitude": 50.11,
    "longitude": 8.68,
    "daily": {
        "time": ["2026-10-01", "2026-10-02", "2026-10-03"],
        "temperature_2m_max": [16.2, 17.8, 15.1],
    },
}

print(response["latitude"])
print(response["daily"]["time"])
print(response["daily"]["temperature_2m_max"][1])

dates = response["daily"]["time"]
temps = response["daily"]["temperature_2m_max"]

for i in range(len(dates)):
    print(dates[i], temps[i])



geo_lat = response["latitude"]
geo_long = response["longitude"]

rows = []

for i in range(len(dates)):
    row = {
        "date": dates[i],
        "temp_max": temps[i],
        "lat": geo_lat,
        "long": geo_long
    }
    rows.append(row)

print(rows)