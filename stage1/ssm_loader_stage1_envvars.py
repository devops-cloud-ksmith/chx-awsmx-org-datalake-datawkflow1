
import boto3
import os

# Set these before running (or use .env loader)
region = "us-west-2"
prefix = "/chx/org/datalake/i8883/_env/stage1/"

env_vars = {
    "BUCKET_NAME": "chx-aws-org-datalake-s3bucket-cdrive1",
    "AWS_REGION_PARAM": "us-west-2",
    "SYSTEMNAME": "orgdatalake",
    "PROJECT_TAG": "CHX-AWSMultiOrgDataLake-IT-8883",
    "CLASSIFICATION": "PHI",
    "BOOTSTRAP": "True",
    "DEFAULT_RECORD": "contacts",
    "ENABLE_METRICS": "true",
    "LOG_LEVEL": "INFO",
    "METRIC_NAMESPACE": "CHX/DataLake/Provisioning"
}

ssm = boto3.client("ssm", region_name=region)

for key, value in env_vars.items():
    param_name = f"{prefix}{key}"
    print(f"Uploading {param_name} -> {value}")
    try:
        ssm.put_parameter(
            Name=param_name,
            Value=value,
            Type="SecureString",
            Overwrite=True,
            Tags=[
                {"Key": "Project", "Value": env_vars["PROJECT_TAG"]},
                {"Key": "Bootstrap", "Value": env_vars["BOOTSTRAP"]}
            ]
        )
        print(f"✅ {param_name} written successfully.")
    except Exception as e:
        print(f"❌ Failed to write {param_name}: {str(e)}")
