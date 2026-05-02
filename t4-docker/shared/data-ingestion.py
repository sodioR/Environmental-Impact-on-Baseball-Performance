import pandas as pd
import requests
import time
import re
from pybaseball import statcast

# Open-Meteo API

# base URL for Open-Meteo weather API
OPENMETEO_URL = "https://archive-api.open-meteo.com/v1/archive"

# daily weather variables to retrieve
DAILY_VARS = ["temperature_2m_max",
              "temperature_2m_min",
              "precipitation_sum",
              "windspeed_10m_max",
              "relative_humidity_2m_mean",
              ]

# standardizes text for consistent matching (lowercase, remove punctuation, trim spaces)
def clean_name(name):

    name = name.lower()
    name = re.sub(r"[^\w\s]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip()

# # pulls daily weather data for a given location and date range
def get_weather_daily(lat, lon, start_date, end_date):

    params = {"latitude": lat,
              "longitude": lon,
              "start_date": start_date,
              "end_date": end_date,
              "daily": ",".join(DAILY_VARS),
              "temperature_unit": "fahrenheit",
              "wind_speed_unit": "mph",
              "precipitation_unit": "inch",
              "timezone": "auto",
              }

    r = requests.get(OPENMETEO_URL, params = params)
    r.raise_for_status()

    data = r.json()
    
    # convert API response to data frame
    df = pd.DataFrame(data["daily"])
    df = df.rename(columns = {"time": "date"})
    df["date"] = pd.to_datetime(df["date"])

    return df

# extracts park_id and coordinates from Seamheads dataset
def get_park_coordinates():

    parks = pd.read_csv("./data-sources/Parks.csv")

    parks = parks.rename(columns = {"PARKID": "park_id",
                                  "Latitude": "latitude",
                                  "Longitude": "longitude"
                                  })[["park_id", "latitude", "longitude"]]

    # remove rows with missing coordinates
    parks = parks.dropna(subset = ["latitude", "longitude"])

    return parks

# pulls weather data for all parks and saves to CSV
def pull_weather_data():

    parks = get_park_coordinates()
    frames = []

    print(f"Pulling weather for {len(parks)} parks...")

    for i, (_, row) in enumerate(parks.iterrows(), start = 1):
        print(f"[Weather {i}/{len(parks)}] {row['park_id']}")
        df = get_weather_daily(row["latitude"],
                               row["longitude"],
                               "2023-06-30",
                               "2023-08-31"
                               )

        # attach park identifier for later joins
        df["park_id"] = row["park_id"]
        frames.append(df)

        time.sleep(2) # pause between requests

    # combine all park level data into one dataset
    weather = pd.concat(frames, ignore_index = True)
    weather.to_csv("./data-sources/weather_raw.csv", index = False)
    print("weather_raw.csv created")

# Pybaseball Stats

# pulls statcast data in chunks to avoid large API requests
def pull_statcast_chunked(start_date, end_date, chunk_days = 7):

    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    frames = []
    cur = start
    chunk_num = 1

    while cur <= end:
        chunk_end = min(cur + pd.Timedelta(days = chunk_days - 1), end)

        s = cur.strftime("%Y-%m-%d")
        e = chunk_end.strftime("%Y-%m-%d")

        print(f"[Statcast chunk {chunk_num}] {s} to {e}")
        df = statcast(start_dt = s, end_dt = e) # pull data for current chunk

        frames.append(df)
        time.sleep(2) # pause to avoid rate limits

        cur = chunk_end + pd.Timedelta(days = 1)
        chunk_num += 1

    return pd.concat(frames, ignore_index = True)

# pulls Statcast data and saves to CSV
def pull_statcast_data():

    df = pull_statcast_chunked("2023-06-30", "2023-08-31")
    df.to_csv("./data-sources/statcast_raw.csv", index = False)
    print("statcast_raw.csv created")

# main runner
def main():

    pull_weather_data()
    pull_statcast_data()

if __name__ == "__main__":

    main()