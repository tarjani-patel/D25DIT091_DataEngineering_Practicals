
import boto3
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

# Test connection
response = s3.list_buckets()

print("Connected to MinIO successfully!")
print("Available buckets:")

for bucket in response["Buckets"]:
    print("-", bucket["Name"])