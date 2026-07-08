import pandas as pd

print("=" * 60)
print("GROUND STATION PERFORMANCE")
print("=" * 60)

# -------------------------------------------------
# LOAD FILES
# -------------------------------------------------

contacts = pd.read_excel("ContactDatabase.xlsx")
downlinks = pd.read_excel("DownlinkLog.xlsx")

IMAGE_SIZE_MB = 100

# -------------------------------------------------
# CONTACT STATISTICS
# -------------------------------------------------

rf_contacts = contacts[contacts["Link"] == "RF"]
ol_contacts = contacts[contacts["Link"] == "OL"]

rf_contact_count = len(rf_contacts)
ol_contact_count = len(ol_contacts)

rf_contact_time = rf_contacts["Duration"].sum()
ol_contact_time = ol_contacts["Duration"].sum()

# -------------------------------------------------
# DOWNLOAD STATISTICS
# -------------------------------------------------

rf_downloads = downlinks[downlinks["Link"] == "RF"]
ol_downloads = downlinks[downlinks["Link"] == "OL"]

rf_images = len(rf_downloads)
ol_images = len(ol_downloads)

rf_data_MB = rf_images * IMAGE_SIZE_MB
ol_data_MB = ol_images * IMAGE_SIZE_MB

rf_data_GB = round(rf_data_MB / 1024, 2)
ol_data_GB = round(ol_data_MB / 1024, 2)

# -------------------------------------------------
# GROUND STATION UTILIZATION
# -------------------------------------------------

simulation_time = 24 * 3600        # 24 hours

total_contact_time = rf_contact_time + ol_contact_time

utilization = round(
    total_contact_time / simulation_time * 100,
    2
)

# -------------------------------------------------
# CREATE REPORT
# -------------------------------------------------

report = pd.DataFrame({

    "Metric":[

        "RF Contacts",
        "Optical Contacts",
        "RF Contact Time (s)",
        "Optical Contact Time (s)",
        "Total Contact Time (s)",
        "RF Images Downloaded",
        "Optical Images Downloaded",
        "RF Data Downloaded (GB)",
        "Optical Data Downloaded (GB)",
        "Ground Station Utilization (%)"

    ],

    "Value":[

        rf_contact_count,
        ol_contact_count,
        round(rf_contact_time,2),
        round(ol_contact_time,2),
        round(total_contact_time,2),
        rf_images,
        ol_images,
        rf_data_GB,
        ol_data_GB,
        utilization

    ]

})

report.to_excel(
    "GroundStationPerformance.xlsx",
    index=False
)

print()
print(report)
print()
print("GroundStationPerformance.xlsx Created")