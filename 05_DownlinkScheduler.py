import pandas as pd

print("=" * 60)
print("DOWNLINK SCHEDULER")
print("=" * 60)

# --------------------------------------------------
# Read Australia Imaging Events
# --------------------------------------------------

images = pd.read_excel("AustraliaImaging.xlsx")

# --------------------------------------------------
# Read Contact Database
# --------------------------------------------------

contacts = pd.read_excel("ContactDatabase.xlsx")

print("Images Columns:")
print(images.columns.tolist())

print("\nContacts Columns:")
print(contacts.columns.tolist())

# --------------------------------------------------
# Create Datetime Columns
# --------------------------------------------------

images["ImageDateTime"] = pd.to_datetime(
    images["Time"],
    format="%d %b %Y %H:%M:%S.%f"
)

contacts["StartDateTime"] = pd.to_datetime(
    contacts["StartDate"] + " " + contacts["StartTime"],
    format="%d %b %Y %H:%M:%S.%f"
)

contacts["StopDateTime"] = pd.to_datetime(
    contacts["StopDate"] + " " + contacts["StopTime"],
    format="%d %b %Y %H:%M:%S.%f"
)

print()
print("Images Loaded :", len(images))
print("Contacts Loaded :", len(contacts))
print()

print(images.head())

print()

print(contacts.head())

contacts["StopDateTime"] = pd.to_datetime(
    contacts["StopDate"] + " " + contacts["StopTime"],
    format="%d %b %Y %H:%M:%S.%f"
)


# Read Australia Imaging
images = pd.read_excel("AustraliaImaging.xlsx")

# Read Contact Database
contacts = pd.read_excel("ContactDatabase.xlsx")

# Convert Times
images["ImageDateTime"] = pd.to_datetime(
    images["Time"],
    format="%d %b %Y %H:%M:%S.%f"
)

contacts["StartDateTime"] = pd.to_datetime(
    contacts["StartDate"] + " " + contacts["StartTime"],
    format="%d %b %Y %H:%M:%S.%f"
)

contacts["StopDateTime"] = pd.to_datetime(
    contacts["StopDate"] + " " + contacts["StopTime"],
    format="%d %b %Y %H:%M:%S.%f"
)

# 👇 PASTE THE NEW SCHEDULER CODE HERE

# =====================================================
# DOWNLINK SCHEDULER
# =====================================================

results = []

for _, img in images.iterrows():

    sat = img["Satellite"]
    img_time = img["ImageDateTime"]

    sat_contacts = contacts[
        (contacts["Satellite"] == sat) &
        (contacts["StartDateTime"] >= img_time)
    ].copy()

    if sat_contacts.empty:

        results.append({
            "Satellite": sat,
            "ImageTime": img["Time"],
            "Latitude": img["Latitude"],
            "Longitude": img["Longitude"],
            "Altitude(km)": img["Altitude(km)"],
            "Link": "NONE",
            "DownloadStart": "",
            "DownloadEnd": "",
            "Wait(min)": "",
            "Duration(s)": "",
            "Status": "NO CONTACT"
        })

        continue

    first = sat_contacts.sort_values("StartDateTime").iloc[0]

    wait = (
        first["StartDateTime"] - img_time
    ).total_seconds() / 60

    results.append({

        "Satellite": sat,

        "ImageTime": img["Time"],

        "Latitude": img["Latitude"],

        "Longitude": img["Longitude"],

        "Altitude(km)": img["Altitude(km)"],

        "Link": first["Link"],

        "DownloadStart":
            first["StartDate"] + " " + first["StartTime"],

        "DownloadEnd":
            first["StopDate"] + " " + first["StopTime"],

        "Wait(min)": round(wait,2),

        "Duration(s)": first["Duration"],

        "Status": "DOWNLOADED"

    })

schedule = pd.DataFrame(results)

schedule.to_excel(
    "DownlinkSchedule.xlsx",
    index=False
)

print()
print("="*60)
print("Scheduler Finished")
print("="*60)

print("Images :", len(images))
print("Scheduled :", len(schedule))
print()

print(schedule.head())