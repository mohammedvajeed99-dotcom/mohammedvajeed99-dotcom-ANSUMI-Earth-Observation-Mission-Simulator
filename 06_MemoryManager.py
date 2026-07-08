import pandas as pd

print("=" * 60)
print("SATELLITE MEMORY MANAGER")
print("=" * 60)

# ---------------------------------------
# PARAMETERS
# ---------------------------------------

IMAGE_SIZE_MB = 100
MAX_MEMORY_MB = 512 * 1024      # 512 GB

# ---------------------------------------
# LOAD DOWNLINK SCHEDULE
# ---------------------------------------

df = pd.read_excel("DownlinkSchedule.xlsx")

# ---------------------------------------
# MEMORY FOR EACH SATELLITE
# ---------------------------------------

memory = {}

results = []

# ---------------------------------------
# PROCESS EVERY IMAGE
# ---------------------------------------

for _, row in df.iterrows():

    sat = row["Satellite"]

    if sat not in memory:
        memory[sat] = 0

    # Image captured
    memory[sat] += IMAGE_SIZE_MB

    overflow = "NO"

    if memory[sat] > MAX_MEMORY_MB:
        overflow = "YES"

    # If image downloaded, remove from memory

    if row["Status"] == "DOWNLOADED":

        memory[sat] -= IMAGE_SIZE_MB

        if memory[sat] < 0:
            memory[sat] = 0

    results.append({

        "Satellite": sat,

        "Image Time": row["ImageTime"],

        "Memory(MB)": memory[sat],

        "Images Stored": memory[sat] // IMAGE_SIZE_MB,

        "Overflow": overflow

    })

# ---------------------------------------
# SAVE
# ---------------------------------------

output = pd.DataFrame(results)

output.to_excel(
    "SatelliteMemoryLog.xlsx",
    index=False
)

print()
print("=" * 60)
print("Finished")
print("=" * 60)

print()

print("Total Records :", len(output))

print("Output : SatelliteMemoryLog.xlsx")