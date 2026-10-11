station = {
    "name": "Frankfurt",
    "country": "Germany",
    "latitude": 50.11,
    "longitude": 8.68,
}





stations = [
    {"name": "Frankfurt", "latitude": 50.11, "temp": 18.5},
    {"name": "Hamburg", "latitude": 53.55, "temp": 15.2},
    {"name": "Munich", "latitude": 48.14, "temp": 19.8},
]

print(stations[0]["name"])

for s in stations:
    print(s["name"], s["temp"])

-- 1. 
for s in stations: 
    if s["temp"] > 18: 
        print(s["name"])



        

start_count = 0 

for s in stations: 
    if s["latitude"] > 50:
        start_count +=1 

print(start_count)

total = 0 

for s in stations: 
    total += s["temp"]

average = total / len(stations)

print(average)