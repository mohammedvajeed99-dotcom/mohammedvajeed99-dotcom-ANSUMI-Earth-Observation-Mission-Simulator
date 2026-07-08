import pandas as pd

print("=" * 60)
print("SATELLITE PERFORMANCE")
print("=" * 60)

# -------------------------------------------------
# LOAD FILES
# -------------------------------------------------

images = pd.read_excel("AustraliaImaging.xlsx")

downlinks = pd.read_excel("DownlinkLog.xlsx")

memory = pd.read_excel("SatelliteMemoryLog.xlsx")

# -------------------------------------------------
# CALCULATE PERFORMANCE
# -------------------------------------------------

results = []

for i in range(1, 49):

    sat = f"ASC_074_{i:02d}"

    captured = len(images[images["Satellite"] == sat])

    downloaded = len(downlinks[downlinks["Satellite"] == sat])

    remaining = captured - downloaded

    sat_memory = memory[memory["Satellite"] == sat]

    if len(sat_memory) > 0:
        peak_memory = sat_memory["MemoryMB"].max()
        peak_images = sat_memory["ImagesStored"].max()
    else:
        peak_memory = 0
        peak_images = 0

    efficiency = 0

    if captured > 0:
        efficiency = round(downloaded / captured * 100, 2)

    results.append({

        "Satellite": sat,

        "Images Captured": captured,

        "Images Downloaded": downloaded,

        "Images Remaining": remaining,

        "Peak Images Stored": peak_images,

        "Peak Memory (MB)": peak_memory,

        "Download Efficiency (%)": efficiency

    })

# -------------------------------------------------
# SAVE
# -------------------------------------------------

performance = pd.DataFrame(results)

performance.to_excel(
    "SatellitePerformance.xlsx",
    index=False
)

print()

print("SatellitePerformance.xlsx Created")

print()

print(performance)
