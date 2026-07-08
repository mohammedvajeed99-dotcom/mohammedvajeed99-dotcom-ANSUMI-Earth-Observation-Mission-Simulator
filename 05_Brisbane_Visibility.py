import pandas as pd

# ==========================================
# Australia Boundary
# ==========================================

MIN_LAT = -44.0
MAX_LAT = -10.0

MIN_LON = 112.0
MAX_LON = 154.0

# ==========================================
# Read Excel
# ==========================================

df = pd.read_excel("StateReport_UTC.xlsx")

results = []

print("===================================")
print("Checking Australia Imaging...")
print("===================================")

# ==========================================
# Check Every Satellite
# ==========================================

for row in range(len(df)):

    time = df.iloc[row]["ASC_074_01.UTCGregorian"]

    for i in range(1,49):

        sat = f"ASC_074_{i:02d}"

        lat_col = f"{sat}.Latitude"
        lon_col = f"{sat}.Longitude"
        alt_col = f"{sat}.Altitude"

        if lat_col not in df.columns:
            continue

        lat = df.iloc[row][lat_col]
        lon = df.iloc[row][lon_col]
        alt = df.iloc[row][alt_col]

        if pd.isna(lat) or pd.isna(lon):
            continue

        imaging = (
            MIN_LAT <= lat <= MAX_LAT and
            MIN_LON <= lon <= MAX_LON
        )

        if imaging:

            results.append([
                time,
                sat,
                lat,
                lon,
                alt,
                "YES"
            ])

# ==========================================
# Save Output
# ==========================================

output = pd.DataFrame(
    results,
    columns=[
        "Time",
        "Satellite",
        "Latitude",
        "Longitude",
        "Altitude(km)",
        "Imaging"
    ]
)

output.to_excel(
    "AustraliaImaging.xlsx",
    index=False
)

print()
print("===================================")
print("Finished Successfully")
print("===================================")
print()

print("Total Imaging Events :", len(output))
print()

print("Output : AustraliaImaging.xlsx")