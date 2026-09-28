
import pandas as pd
from pathlib import Path

# Load the dataset
df = pd.read_csv("data/retail_sales.csv")

# Create the partitioned output folder
output_dir = Path("output/partitioned")
output_dir.mkdir(parents=True, exist_ok=True)

# Partition by year, month, and region
for (year, month, region), group in df.groupby(
    ["year", "month", "region"]
):
    folder = (
        output_dir
        / f"year={year}"
        / f"month={month:02d}"
        / f"region={region}"
    )

    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder / "data.csv"
    group.to_csv(file_path, index=False)

print("Dataset partitioned successfully!")
print("Total records:", len(df))
print("Partition folders:", len(list(output_dir.rglob("data.csv"))))
print("Output location:", output_dir)