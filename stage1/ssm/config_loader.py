import boto3
import logging
from config import constants

logger = logging.getLogger()
ssm = boto3.client("ssm", region_name=constants.AWS_REGION)

def get_config_param(name, fallback=None):
    param_path = f"/chx/org/datalake/i8883/_env/stage1/{name}"
    try:
        response = ssm.get_parameter(Name=param_path, WithDecryption=True)
        return response["Parameter"]["Value"]
    except Exception as e:
        logger.warning(f"SSM lookup failed for {param_path}: {e}")
        return fallback
