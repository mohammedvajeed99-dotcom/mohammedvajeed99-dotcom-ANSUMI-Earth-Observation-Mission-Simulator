import pandas as pd

# Read GMAT StateReport.txt
df = pd.read_csv(
    "StateReport.txt",
    sep=r"\s+",
    engine="python"
)

print("=" * 60)
print("State Report Loaded Successfully")
print("=" * 60)

print("\nRows:", len(df))
print("Columns:", len(df.columns))

print("\nFirst Five Rows:\n")
print(df.head())

# Save to Excel
df.to_excel("StateReport.xlsx", index=False)

print("\n======================================")
print("StateReport.xlsx created successfully!")
print("======================================")