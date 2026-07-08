import pandas as pd
import matplotlib.pyplot as plt

print("=" * 60)
print("MISSION DASHBOARD")
print("=" * 60)

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

sat = pd.read_excel("SatellitePerformance.xlsx")

mission = pd.read_excel("MissionStatistics.xlsx")

# -------------------------------------------------------
# 1. Images Captured vs Downloaded
# -------------------------------------------------------

plt.figure(figsize=(14,6))

x = range(len(sat))

plt.bar(
    [i-0.2 for i in x],
    sat["Images Captured"],
    width=0.4,
    label="Captured"
)

plt.bar(
    [i+0.2 for i in x],
    sat["Images Downloaded"],
    width=0.4,
    label="Downloaded"
)

plt.xticks(x, sat["Satellite"], rotation=90)

plt.xlabel("Satellite")
plt.ylabel("Images")
plt.title("Images Captured vs Downloaded")
plt.legend()

plt.tight_layout()
plt.savefig("ImagesCaptured_vs_Downloaded.png")
plt.close()

# -------------------------------------------------------
# 2. Remaining Images
# -------------------------------------------------------

plt.figure(figsize=(14,6))

plt.bar(
    sat["Satellite"],
    sat["Images Remaining"]
)

plt.xticks(rotation=90)

plt.xlabel("Satellite")
plt.ylabel("Images")

plt.title("Remaining Images Onboard")

plt.tight_layout()

plt.savefig("RemainingImages.png")
plt.close()

# -------------------------------------------------------
# 3. Peak Memory
# -------------------------------------------------------

plt.figure(figsize=(14,6))

plt.bar(
    sat["Satellite"],
    sat["Peak Memory (MB)"]
)

plt.xticks(rotation=90)

plt.xlabel("Satellite")
plt.ylabel("MB")

plt.title("Peak Memory Usage")

plt.tight_layout()

plt.savefig("PeakMemory.png")
plt.close()

# -------------------------------------------------------
# 4. RF vs Optical
# -------------------------------------------------------

rf = mission.loc[
    mission["Metric"]=="RF Downloads",
    "Value"
].values[0]

ol = mission.loc[
    mission["Metric"]=="Optical Downloads",
    "Value"
].values[0]

plt.figure(figsize=(6,6))

plt.pie(
    [rf, ol],
    labels=["RF","Optical"],
    autopct="%1.1f%%"
)

plt.title("RF vs Optical Downloads")

plt.savefig("RF_vs_Optical.png")
plt.close()

# -------------------------------------------------------
# 5. Download Efficiency
# -------------------------------------------------------

eff = mission.loc[
    mission["Metric"]=="Downloaded Images",
    "Value"
].values[0]

capt = mission.loc[
    mission["Metric"]=="Total Images Captured",
    "Value"
].values[0]

efficiency = eff / capt * 100

plt.figure(figsize=(5,5))

plt.bar(
    ["Efficiency"],
    [efficiency]
)

plt.ylim(0,100)

plt.ylabel("%")

plt.title("Overall Downlink Efficiency")

plt.savefig("DownlinkEfficiency.png")
plt.close()

print()
print("Dashboard Generated Successfully")
print()

print("Created:")

print("ImagesCaptured_vs_Downloaded.png")
print("RemainingImages.png")
print("PeakMemory.png")
print("RF_vs_Optical.png")
print("DownlinkEfficiency.png")