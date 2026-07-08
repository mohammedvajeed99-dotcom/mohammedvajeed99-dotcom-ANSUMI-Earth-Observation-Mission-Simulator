import pandas as pd
from datetime import datetime, timedelta

# =====================================================
# MISSION START TIME (CHANGE IF REQUIRED)
# =====================================================

MISSION_START = datetime.strptime(
    "03 Jul 2026 00:00:00.000",
    "%d %b %Y %H:%M:%S.%f"
)

# =====================================================
# READ STATE REPORT
# =====================================================

df = pd.read_excel("StateReport.xlsx")

time_column = "ASC_074_01.UTCGregorian"

print("Converting Elapsed Time to UTC...")

utc_times = []

# =====================================================
# CONVERT ELAPSED → UTC
# =====================================================

for t in df[time_column]:

    t = str(t).strip()

    h, m, s = t.split(":")

    seconds = float(s)

    elapsed = timedelta(
        hours=int(h),
        minutes=int(m),
        seconds=seconds
    )

    utc = MISSION_START + elapsed

    utc_times.append(
        utc.strftime("%d %b %Y %H:%M:%S.%f")[:-3]
    )

# =====================================================
# REPLACE COLUMN
# =====================================================

df[time_column] = utc_times

# =====================================================
# SAVE
# =====================================================

df.to_excel(
    "StateReport_UTC.xlsx",
    index=False
)

print()
print("=========================================")
print("Finished Successfully")
print("=========================================")
print()

print("Output File : StateReport_UTC.xlsx")