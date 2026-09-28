
import boto3
import pandas as pd
import time
from io import BytesIO
from botocore.client import Config

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

# Query conditions
target_year = 2024
target_month = 1
target_region = "North"

# Get all uploaded CSV object keys
paginator = s3.get_paginator("list_objects_v2")
all_keys = []

for page in paginator.paginate(Bucket=bucket):
    for obj in page.get("Contents", []):
        if obj["Key"].endswith(".csv"):
            all_keys.append(obj["Key"])

# 1. Partitioned query
partition_prefix = (
    f"year={target_year}/"
    f"month={target_month:02d}/"
    f"region={target_region}/"
)

start = time.perf_counter()

partition_keys = [
    key for key in all_keys
    if key.startswith(partition_prefix)
]

partition_frames = []

for key in partition_keys:
    response = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(BytesIO(response["Body"].read()))
    partition_frames.append(df)

if partition_frames:
    partition_result = pd.concat(
        partition_frames, ignore_index=True
    )
else:
    partition_result = pd.DataFrame()

partition_time = time.perf_counter() - start

# 2. Full dataset scan
start = time.perf_counter()

all_frames = []

for key in all_keys:
    response = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(BytesIO(response["Body"].read()))
    all_frames.append(df)

full_df = pd.concat(all_frames, ignore_index=True)

full_result = full_df[
    (full_df["year"] == target_year) &
    (full_df["month"] == target_month) &
    (full_df["region"] == target_region)
]

full_scan_time = time.perf_counter() - start

# Display results
print("\n--- PARTITIONED QUERY ---")
print("Records found:", len(partition_result))
print("Time taken:", round(partition_time, 4), "seconds")

print("\n--- FULL DATASET SCAN ---")
print("Records found:", len(full_result))
print("Time taken:", round(full_scan_time, 4), "seconds")

print("\n--- PERFORMANCE COMPARISON ---")
if partition_time > 0:
    speedup = full_scan_time / partition_time
    print("Speedup:", round(speedup, 2), "x")

print("\nResults match:",
      len(partition_result) == len(full_result))