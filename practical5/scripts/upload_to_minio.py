
import boto3
from botocore.client import Config
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

bucket_name = "de-prac5"
partition_dir = Path("output/partitioned")

# Upload partitioned files
files = list(partition_dir.rglob("data.csv"))

uploaded = 0

for file_path in files:
    # Preserve the Hive-style partition structure
    object_key = file_path.relative_to(partition_dir).as_posix()

    s3.upload_file(
        str(file_path),
        bucket_name,
        object_key
    )

    uploaded += 1
    print(f"Uploaded: {object_key}")

print("\nUpload completed successfully!")
print("Total files uploaded:", uploaded)
print("Destination bucket:", bucket_name)