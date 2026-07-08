import pandas as pd

print("====================================")
print("Creating Contact Database...")
print("====================================")

# --------------------------------------------
# Read RF Contact Excel
# --------------------------------------------

rf = pd.read_excel("RF_Contacts.xlsx")

rf["Link"] = "RF"

# --------------------------------------------
# Read Optical Contact Excel
# --------------------------------------------

ol = pd.read_excel("OL_Contacts.xlsx")

ol["Link"] = "OL"

# --------------------------------------------
# Rename Columns
# --------------------------------------------

rf.rename(columns={
    "Sl No": "Event",
    "Spacecraft": "Satellite",
    "Start Date": "StartDate",
    "Start Time": "StartTime",
    "Stop Date": "StopDate",
    "Stop Time": "StopTime",
    "Duration (s)": "Duration"
}, inplace=True)

ol.rename(columns={
    "Sl No": "Event",
    "Spacecraft": "Satellite",
    "Start Date": "StartDate",
    "Start Time": "StartTime",
    "Stop Date": "StopDate",
    "Stop Time": "StopTime",
    "Duration (s)": "Duration"
}, inplace=True)

# --------------------------------------------
# Combine
# --------------------------------------------

contacts = pd.concat([rf, ol], ignore_index=True)

# --------------------------------------------
# Sort
# --------------------------------------------

contacts.sort_values(
    by=["Satellite", "StartDate", "StartTime"],
    inplace=True
)

# --------------------------------------------
# Save
# --------------------------------------------

contacts.to_excel(
    "ContactDatabase.xlsx",
    index=False
)

print()
print("====================================")
print("Finished Successfully")
print("====================================")

print(f"Total Contacts : {len(contacts)}")
print("Output : ContactDatabase.xlsx")