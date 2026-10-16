import time

import requests
import duckdb

URL = "https://archive-api.open-meteo.com/v1/archive"
DB_PATH = "data/climate_data_dwh.duckdb"
DAILY_VARIABLES = "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum"

FIRST_YEAR = 2016
LAST_YEAR = 2025
PAUSE_SECONDS = 1
MAX_ATTEMPTS = 3


def get_locations(con):
    return con.execute(
        "SELECT location_name, latitude, longitude FROM raw.raw_manual_locations ORDER BY location_name"
    ).fetchall()


def already_loaded(con, latitude, longitude, start_date, end_date):
    count = con.execute(
        """
        SELECT count(*)
        FROM raw.raw_open_meteo_daily
        WHERE request_latitude = ?
          AND request_longitude = ?
          AND request_start_date = ?
          AND request_end_date = ?
        """,
        [latitude, longitude, start_date, end_date],
    ).fetchone()[0]
    return count > 0


def fetch_weather(latitude, longitude, start_date, end_date):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": DAILY_VARIABLES,
        "timezone": "auto",
    }
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(URL, params=params, timeout=60)
            response.raise_for_status()
            return response.text
        except (requests.Timeout, requests.ConnectionError) as error:
            if attempt == MAX_ATTEMPTS:
                raise
            wait = attempt * 10
            print(f"Attempt {attempt} failed ({type(error).__name__}), retrying in {wait}s")
            time.sleep(wait)


def load_raw(con, latitude, longitude, start_date, end_date, response_text):
    con.execute(
        """
        INSERT INTO raw.raw_open_meteo_daily
            (request_latitude, request_longitude, request_start_date, request_end_date, response_json, _source)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [latitude, longitude, start_date, end_date, response_text, URL],
    )


def main():
    con = duckdb.connect(DB_PATH)
    loaded = 0
    skipped = 0
    try:
        for name, latitude, longitude in get_locations(con):
            for year in range(FIRST_YEAR, LAST_YEAR + 1):
                start_date = f"{year}-01-01"
                end_date = f"{year}-12-31"

                if already_loaded(con, latitude, longitude, start_date, end_date):
                    skipped += 1
                    continue

                try:
                    response_text = fetch_weather(latitude, longitude, start_date, end_date)
                except requests.HTTPError as error:
                    if error.response.status_code == 429:
                        print("Rate limit reached, stopping. Run the script again later.")
                        return
                    print(f"Failed: {name} {year}: {error}")
                    continue

                except requests.HTTPError as error:
                    if error.response.status_code == 429:
                        print("Rate limit reached, stopping. Run the script again later.")
                        return
                    print(f"Failed: {name} {year}: {error}")
                    continue
                except requests.RequestException as error:
                    print(f"Failed after retries: {name} {year}: {type(error).__name__}")
                    continue

                load_raw(con, latitude, longitude, start_date, end_date, response_text)
                loaded += 1
                print(f"Loaded {name} {year}")
                time.sleep(PAUSE_SECONDS)
    finally:
        con.close()
        print(f"Done. Loaded: {loaded}, skipped: {skipped}")


main()