import pandas as pd

print("="*60)
print("CONSTELLATION PERFORMANCE")
print("="*60)

# ---------------------------------------
# Load Previous Reports
# ---------------------------------------

mission = pd.read_excel("MissionStatistics.xlsx")

satellite = pd.read_excel("SatellitePerformance.xlsx")

ground = pd.read_excel("GroundStationPerformance.xlsx")

# ---------------------------------------
# Read Values
# ---------------------------------------

total_satellites = len(satellite)

total_images = mission.loc[
    mission["Metric"]=="Total Images Captured",
    "Value"
].values[0]

downloaded_images = mission.loc[
    mission["Metric"]=="Downloaded Images",
    "Value"
].values[0]

remaining_images = mission.loc[
    mission["Metric"]=="Remaining Images",
    "Value"
].values[0]

peak_memory = mission.loc[
    mission["Metric"]=="Peak Memory (MB)",
    "Value"
].values[0]

rf_downloads = mission.loc[
    mission["Metric"]=="RF Downloads",
    "Value"
].values[0]

ol_downloads = mission.loc[
    mission["Metric"]=="Optical Downloads",
    "Value"
].values[0]

# ---------------------------------------
# Calculations
# ---------------------------------------

avg_images = round(total_images / total_satellites,2)

avg_downloaded = round(downloaded_images / total_satellites,2)

download_efficiency = round(
    downloaded_images / total_images * 100,
    2
)

rf_percent = round(
    rf_downloads / downloaded_images * 100,
    2
)

ol_percent = round(
    ol_downloads / downloaded_images * 100,
    2
)

avg_peak_memory = round(
    satellite["Peak Memory (MB)"].mean(),
    2
)

# ---------------------------------------
# Create Report
# ---------------------------------------

report = pd.DataFrame({

    "Metric":[

        "Total Satellites",
        "Images Captured",
        "Images Downloaded",
        "Images Remaining",
        "Average Images/Satellite",
        "Average Downloads/Satellite",
        "Downlink Efficiency (%)",
        "Average Peak Memory (MB)",
        "Maximum Peak Memory (MB)",
        "RF Downloads",
        "Optical Downloads",
        "RF Percentage (%)",
        "Optical Percentage (%)"

    ],

    "Value":[

        total_satellites,
        total_images,
        downloaded_images,
        remaining_images,
        avg_images,
        avg_downloaded,
        download_efficiency,
        avg_peak_memory,
        peak_memory,
        rf_downloads,
        ol_downloads,
        rf_percent,
        ol_percent

    ]

})

report.to_excel(
    "ConstellationPerformance.xlsx",
    index=False
)

print()
print(report)
print()
print("ConstellationPerformance.xlsx Created")