response = {
    "latitude": 50.11,
    "longitude": 8.68,
    "daily": {
        "time": ["2026-10-01", "2026-10-02", "2026-10-03"],
        "temperature_2m_max": [16.2, 17.8, 15.1],
    },
}


def parse_daily(response):
    dates = response["daily"]["time"]
    temps = response["daily"]["temperature_2m_max"]
    latitude = response["latitude"]
    longitude = response["longitude"]

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


result = parse_daily(response)
print(result)

response_2 = {
    "latitude": 53.55,
    "longitude": 10.0,
    "daily": {
        "time": ["2026-10-01", "2026-10-02"],
        "temperature_2m_max": [14.0, 15.5],
    },
}

result_1 = parse_daily(response)
result_2 = parse_daily(response_2)

print(len(result_1))
print(len(result_2))