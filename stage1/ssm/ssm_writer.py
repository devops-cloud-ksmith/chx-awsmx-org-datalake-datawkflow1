# Placeholder for ssm/ssm_writer.py
from config import constants
import boto3
import logging
from botocore.exceptions import ClientError
from metrics.emitter import emit_metric

logger = logging.getLogger()
ssm = boto3.client("ssm", region_name=constants.AWS_REGION)

def write_parameter(tier, org, record, s3_key):
    param_name = f"/chx/org/datalake/i8883/{org}/{tier}/{record}"
    tags = [
        {"Key": "Project", "Value": constants.PROJECT_TAG},
        {"Key": "Bootstrap", "Value": constants.BOOTSTRAP}
    ] if constants.SSM_ENABLE_TAGGING else []

    try:
        # ssm.put_parameter(
        #     Name=param_name,
        #     Value=s3_key,
        #     Type="SecureString" if constants.SSM_USE_SECURESTRING else "String",
        #     Overwrite=constants.SSM_OVERWRITE
        # )
        from datetime import datetime
        timestamp_param = f"{param_name}/last_updated"
        ssm.put_parameter(
            Name=timestamp_param,
            Value=datetime.utcnow().isoformat(),
            Type="String",
            Overwrite=True
        )

        if tags:
            ssm.add_tags_to_resource(ResourceType='Parameter', ResourceId=param_name, Tags=tags)
        logger.info(f"SSM parameter created: {param_name}")
        emit_metric("SSMParametersWritten", org=org)
    except ClientError as e:
        logger.error(f"Failed to write SSM: {e}")
        if constants.FAIL_FAST:
            raise
