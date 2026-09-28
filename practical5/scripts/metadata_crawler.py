
import boto3
import pandas as pd
from botocore.client import Config
from collections import defaultdict
from pathlib import Path

# Connect to MinIO
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="admin",
    aws_secret_access_key="password123",
    region_name="us-east-1",
    config=Config(signature_version="s3v4")
)

bucket = "de-prac5"

# Store metadata for each partition
partitions = defaultdict(lambda: {"files": 0, "size_bytes": 0})

# Crawl all objects in the bucket
paginator = s3.get_paginator("list_objects_v2")

total_files = 0
total_size = 0

for page in paginator.paginate(Bucket=bucket):
    for obj in page.get("Contents", []):
        key = obj["Key"]
        size = obj["Size"]

        total_files += 1
        total_size += size

        # Extract Hive-style partition identifiers
        parts = key.split("/")

        year = next(
            (p for p in parts if p.startswith("year=")), "unknown"
        )
        month = next(
            (p for p in parts if p.startswith("month=")), "unknown"
        )
        region = next(
            (p for p in parts if p.startswith("region=")), "unknown"
        )

        partition_name = f"{year}/{month}/{region}"

        partitions[partition_name]["files"] += 1
        partitions[partition_name]["size_bytes"] += size

# Convert metadata into a DataFrame
rows = []

for name, details in sorted(partitions.items()):
    rows.append({
        "partition": name,
        "files": details["files"],
        "size_bytes": details["size_bytes"],
        "size_MB": round(details["size_bytes"] / (1024 ** 2), 4)
    })

df = pd.DataFrame(rows)

# Calculate balance and skew metrics
if not df.empty:
    avg_size = df["size_bytes"].mean()
    max_size = df["size_bytes"].max()
    min_size = df["size_bytes"].min()

    max_to_avg = max_size / avg_size if avg_size else 0
    min_to_avg = min_size / avg_size if avg_size else 0

    # Save partition metadata
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "partition_metadata.csv"
    df.to_csv(output_file, index=False)

    print("\n--- MINIO METADATA CRAWLER ---")
    print("Bucket:", bucket)
    print("Total objects:", total_files)
    print("Total size (MB):", round(total_size / (1024 ** 2), 4))
    print("Active partitions:", len(df))
    print("Average partition size (MB):",
          round(avg_size / (1024 ** 2), 4))
    print("Largest partition (MB):",
          round(max_size / (1024 ** 2), 4))
    print("Smallest partition (MB):",
          round(min_size / (1024 ** 2), 4))
    print("Max-to-average skew ratio:", round(max_to_avg, 4))
    print("Min-to-average size ratio:", round(min_to_avg, 4))
    print("\nPartition details:")
    print(df.to_string(index=False))
    print("\nMetadata saved to:", output_file)
else:
    print("No objects found in the bucket.")