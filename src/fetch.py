import requests
import pandas as pd

CITIES = {
    "Delhi":     (28.61, 77.21),
    "Mumbai":    (19.08, 72.88),
    "Kolkata":   (22.57, 88.36),
    "Bengaluru": (12.97, 77.59),
    "Hyderabad": (17.39, 78.49),
    "Lucknow":   (26.85, 80.95),
    "Guwahati":  (26.14, 91.74),
}

URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

def fetch_city(name, lat, lon, start, end):
    params = {
        "latitude": lat, "longitude": lon,
        "hourly": "pm2_5",
        "start_date": start, "end_date": end,
        "timezone": "Asia/Kolkata",
    }
    resp = requests.get(URL, params=params, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"{name}: HTTP {resp.status_code} - {resp.text[:200]}")
    data = resp.json()
    df = pd.DataFrame(data["hourly"])
    df["time"] = pd.to_datetime(df["time"])
    df["city"] = name
    return df, data["hourly_units"]

if __name__ == "__main__":
    df, units = fetch_city("Delhi", *CITIES["Delhi"], "2025-01-01", "2025-01-03")
    print("units:", units)
    print("shape:", df.shape)
    print(df.dtypes)
    print(df.head())