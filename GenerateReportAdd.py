lines = []

# Add time once
lines.append("ASC_074_01.UTCGregorian")

# Add all spacecraft
for i in range(1, 49):
    sc = f"ASC_074_{i:02d}"

    lines.append(f"{sc}.Latitude")
    lines.append(f"{sc}.Longitude")
    lines.append(f"{sc}.Altitude")
    lines.append(f"{sc}.RMAG")
    lines.append(f"{sc}.ECC")

print("GMAT StateReport.Add = {" + ", ".join(lines) + "};")