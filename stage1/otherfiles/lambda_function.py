
import boto3
import json
import os
import logging
import urllib.parse
from datetime import datetime
from botocore.exceptions import ClientError

# Setup structured logging
logger = logging.getLogger()
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logger.setLevel(getattr(logging, log_level))

# Clients
REGION = os.environ.get("AWS_REGION_PARAM", "us-west-2")
s3 = boto3.client("s3", region_name=REGION)
ssm = boto3.client("ssm", region_name=REGION)
cw = boto3.client("cloudwatch", region_name=REGION)

# Env vars
BUCKET_NAME = os.environ["BUCKET_NAME"]
SYSTEMNAME = os.environ.get("SYSTEMNAME", "orgdatalake")
PROJECT_TAG = os.environ.get("PROJECT_TAG", "CHX-AWSMultiOrgDataLake-IT-8883")
CLASSIFICATION_TAG = os.environ.get("CLASSIFICATION", "PHI")
BOOTSTRAP_TAG = os.environ.get("BOOTSTRAP", "True")
METRIC_NAMESPACE = os.environ.get("METRIC_NAMESPACE", "CHX/DataLake/Provisioning")
DEFAULT_RECORD = os.environ.get("DEFAULT_RECORD", "contacts")
ENABLE_METRICS = os.environ.get("ENABLE_METRICS", "true").lower() == "true"

def emit_metric(name, value=1, org="unknown"):
    if not ENABLE_METRICS:
        return
    try:
        cw.put_metric_data(
            Namespace=METRIC_NAMESPACE,
            MetricData=[{
                "MetricName": name,
                "Dimensions": [{"Name": "Org", "Value": org}],
                "Unit": "Count",
                "Value": value
            }]
        )
    except ClientError as e:
        logger.warning(f"Failed to emit metric {name} for {org}: {str(e)}")

def create_prefix(data_tier, org, record, date_path):
    if not all([org, record, data_tier]):
        logger.error(f"Missing required inputs: {org=}, {record=}, {data_tier=}")
        raise ValueError("All parameters must be provided")

    key = f"{SYSTEMNAME}/{data_tier}/{org}/{record}/{date_path}/jira_{record}.json"
    s3_key = f"s3://{BUCKET_NAME}/{key}"

    tags = {
        "Project": PROJECT_TAG,
        "Org": org,
        "Record": record,
        "Tier": data_tier,
        "Classification": CLASSIFICATION_TAG,
        "Bootstrap": BOOTSTRAP_TAG
    }

    tag_string = '&'.join([f"{urllib.parse.quote_plus(k)}={urllib.parse.quote_plus(v)}" for k, v in tags.items()])

    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body="INIT STRUCTURE",
            Tagging=tag_string,
            ServerSideEncryption="aws:kms"
        )
        logger.info(f"S3 object created: {s3_key}")
    except ClientError as e:
        logger.error(f"Failed to create S3 prefix: {str(e)}")
        raise

    ssm_param_name = f"/chx/org/datalake/i8883/{org}/{data_tier}/{record}"
    ssm_tags = [{"Key": "Project", "Value": PROJECT_TAG}, {"Key": "Bootstrap", "Value": BOOTSTRAP_TAG}]

    try:
        ssm.put_parameter(Name=ssm_param_name, Value=s3_key, Type="String", Tags=ssm_tags)
    except ssm.exceptions.ParameterAlreadyExists:
        ssm.put_parameter(Name=ssm_param_name, Value=s3_key, Type="String", Overwrite=True)
        ssm.add_tags_to_resource(ResourceType='Parameter', ResourceId=ssm_param_name, Tags=ssm_tags)
    except ClientError as e:
        logger.error(f"Failed to write to SSM: {str(e)}")
        raise

    emit_metric("PrefixesCreated", org=org)
    emit_metric("SSMParametersWritten", org=org)

def lambda_handler(event, context):
    org = event.get("org")
    record = event.get("record", DEFAULT_RECORD)
    data_tiers = event.get("tiers", ["raw"])
    date_path = event.get("date", datetime.utcnow().strftime("%Y/%m/%d"))

    results = []
    for tier in data_tiers:
        try:
            create_prefix(tier, org, record, date_path)
            results.append(f"{tier}: OK")
        except Exception as e:
            results.append(f"{tier}: FAILED - {str(e)}")
            continue

    return {
        "status": "complete",
        "executed_on": datetime.utcnow().isoformat(),
        "executed_for": org,
        "date_path": date_path,
        "record": record,
        "results": results
    }
