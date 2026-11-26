import pandas as pd
from datetime import date

path = "../data/raw/gpx-tracks-from-hikr.org.csv"
df = pd.read_csv(path)

# Capture necessary columns
FEATURES = [
    "start_time",
    "end_time",
    "uphill"
]
df = df[FEATURES]

# Clean data
df["end_time"] = pd.to_datetime(df["end_time"], errors="coerce")
df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
df = df.dropna()

df["elapsed_time(hours)"] = (df["end_time"] - df["start_time"]).dt.total_seconds() / 3600
df = df.drop(columns=["end_time", "start_time"])

df = df.rename(columns={"uphill": "elevation_gain(feet)"})
df["elevation_gain(feet)"] = df["elevation_gain(feet)"] * 3.28084

df.to_csv("../data/processed/cleaned_hike_data.csv")

