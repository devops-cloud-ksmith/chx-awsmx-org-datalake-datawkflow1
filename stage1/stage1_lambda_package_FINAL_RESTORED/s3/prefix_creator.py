from config import constants
import boto3
import urllib.parse
import logging
from botocore.exceptions import ClientError
from metrics.emitter import emit_metric

logger = logging.getLogger()
s3 = boto3.client("s3", region_name=constants.AWS_REGION)

def create_prefix(tier, org, record, date_path):
    if constants.DRY_RUN:
        logger.info(f"[DRY_RUN] Would create: {tier}/{org}/{record}/{date_path}")
        return

    key = f"{constants.SYSTEMNAME}/{tier}/{org}/{record}/{date_path}/jira_{record}.json"
    s3_key = f"s3://{constants.BUCKET_NAME}/{key}"
    
    tags = {
        "Project": constants.PROJECT_TAG,
        "Org": org,
        "Record": record,
        "Tier": tier,
        "Classification": constants.CLASSIFICATION,
        "Bootstrap": constants.BOOTSTRAP,
        "Environment": constants.TAGS_ENVIRONMENT,
        "RetentionDays": constants.RETENTION_DAYS
    }

    tag_string = '&'.join([
        f"{urllib.parse.quote_plus(k)}={urllib.parse.quote_plus(v)}" for k, v in tags.items()
    ])

    try:
        s3.put_object(
            Bucket=constants.BUCKET_NAME,
            Key=key,
            Body="INIT STRUCTURE",
            Tagging=tag_string,
            ServerSideEncryption="aws:kms" if constants.KMS_KEY_ID else "AES256",
            SSEKMSKeyId=constants.KMS_KEY_ID if constants.KMS_KEY_ID else None
        )
        logger.info(f"S3 object created: {s3_key}")
        emit_metric("PrefixesCreated", org=org)
    except ClientError as e:
        logger.error(f"Failed to write to S3: {e}")
        if constants.FAIL_FAST:
            raise