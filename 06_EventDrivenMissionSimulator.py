import pandas as pd

print("="*60)
print("EVENT DRIVEN MISSION SIMULATOR")
print("="*60)

# ----------------------------------------------------
# Load Imaging Events
# ----------------------------------------------------

images = pd.read_excel("AustraliaImaging.xlsx")

images["DateTime"] = pd.to_datetime(
    images["Time"],
    format="%d %b %Y %H:%M:%S.%f"
)

images["EventType"] = "IMAGE"

# ----------------------------------------------------
# Load Contacts
# ----------------------------------------------------

contacts = pd.read_excel("ContactDatabase.xlsx")

contacts["DateTime"] = pd.to_datetime(
    contacts["StartDate"] + " " + contacts["StartTime"],
    format="%d %b %Y %H:%M:%S.%f"
)

contacts["EventType"] = contacts["Link"]

# ----------------------------------------------------
# Image Events
# ----------------------------------------------------

image_events = images[[
    "DateTime",
    "Satellite",
    "EventType",
    "Latitude",
    "Longitude",
    "Altitude(km)"
]].copy()

image_events["Duration"] = 0

# ----------------------------------------------------
# Contact Events
# ----------------------------------------------------

contact_events = contacts[[
    "DateTime",
    "Satellite",
    "EventType",
    "Duration"
]].copy()

contact_events["Latitude"] = None
contact_events["Longitude"] = None
contact_events["Altitude(km)"] = None

# ----------------------------------------------------
# Merge Timeline
# ----------------------------------------------------

timeline = pd.concat(
    [image_events, contact_events],
    ignore_index=True
)

timeline.sort_values(
    "DateTime",
    inplace=True
)

timeline.reset_index(
    drop=True,
    inplace=True
)

# =====================================================
# SATELLITE MEMORY INITIALIZATION
# =====================================================

IMAGE_SIZE_MB = 100
RF_RATE_MBPS = 150
OL_RATE_MBPS = 1000

sat_memory = {}

for i in range(1, 49):

    sat = f"ASC_074_{i:02d}"

    sat_memory[sat] = []

# Unique Image ID Counter
image_counter = 1


# =====================================================
# EVENT SIMULATION
# =====================================================

memory_log = []
downlink_log = []

for _, event in timeline.iterrows():

    sat = event["Satellite"]

    # ------------------------------------------------
    # IMAGE EVENT
    # ------------------------------------------------
    if event["EventType"] == "IMAGE":

        sat_memory[sat].append({

            "ImageID": image_counter,
            "CaptureTime": event["DateTime"],
            "Latitude": event["Latitude"],
            "Longitude": event["Longitude"],
            "SizeMB": IMAGE_SIZE_MB,
            "Downloaded": False

        })

        image_counter += 1

    # ------------------------------------------------
    # RF / OL CONTACT
    # ------------------------------------------------
    elif event["EventType"] in ["RF", "OL"]:

        if event["EventType"] == "RF":
            rate = RF_RATE_MBPS
        else:
            rate = OL_RATE_MBPS

        # Mbps → MB/s
        rate_MBps = rate / 8.0

        # Total downloadable MB
        capacity_MB = rate_MBps * event["Duration"]

        # Number of images that fit
        images_can_download = int(capacity_MB // IMAGE_SIZE_MB)

        downloaded = 0

        while len(sat_memory[sat]) > 0 and downloaded < images_can_download:

            image = sat_memory[sat].pop(0)

            image["Downloaded"] = True

            downlink_log.append({

                "Satellite": sat,
                "ImageID": image["ImageID"],
                "CaptureTime": image["CaptureTime"],
                "DownloadTime": event["DateTime"],
                "Link": event["EventType"]

            })

            downloaded += 1

    # ------------------------------------------------
    # MEMORY LOG
    # ------------------------------------------------
    memory_log.append({

        "Time": event["DateTime"],
        "Satellite": sat,
        "ImagesStored": len(sat_memory[sat]),
        "MemoryMB": len(sat_memory[sat]) * IMAGE_SIZE_MB,
        "LatestImageID": image_counter - 1 if len(sat_memory[sat]) > 0 else None

    })

timeline.to_excel(
    "MissionTimeline.xlsx",
    index=False
)

print()
print("Image Events :", len(image_events))
print("Contact Events :", len(contact_events))
print("Total Events :", len(timeline))

print()
print("MissionTimeline.xlsx Created")
memory_df = pd.DataFrame(memory_log)

memory_df.to_excel(
    "SatelliteMemoryLog.xlsx",
    index=False
)

print()

print("SatelliteMemoryLog.xlsx Created")

downlink_df = pd.DataFrame(downlink_log)

downlink_df.to_excel(
    "DownlinkLog.xlsx",
    index=False
)

print("DownlinkLog.xlsx Created")

print("Downloaded Images :", len(downlink_df))

# =====================================================
# MISSION STATISTICS
# =====================================================

total_images = image_counter - 1
downloaded_images = len(downlink_df)
remaining_images = total_images - downloaded_images

peak_memory = memory_df["MemoryMB"].max()
peak_images = memory_df["ImagesStored"].max()

rf_downloads = len(downlink_df[downlink_df["Link"] == "RF"])
ol_downloads = len(downlink_df[downlink_df["Link"] == "OL"])

stats = pd.DataFrame({

    "Metric": [

        "Total Images Captured",
        "Downloaded Images",
        "Remaining Images",
        "Peak Memory (MB)",
        "Peak Images Stored",
        "RF Downloads",
        "Optical Downloads"

    ],

    "Value": [

        total_images,
        downloaded_images,
        remaining_images,
        peak_memory,
        peak_images,
        rf_downloads,
        ol_downloads

    ]

})

stats.to_excel("MissionStatistics.xlsx", index=False)

print()
print("MissionStatistics.xlsx Created")
print()
print(stats)