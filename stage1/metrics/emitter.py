# Placeholder for metrics/emitter.py
from config import constants
import boto3
import logging

logger = logging.getLogger()
cw = boto3.client("cloudwatch", region_name=constants.AWS_REGION)

def emit_metric(name, value=1, org="unknown"):
    if not constants.ENABLE_METRICS:
        return
    try:
        cw.put_metric_data(
            Namespace=constants.METRIC_NAMESPACE,
            MetricData=[{
                "MetricName": name,
                "Dimensions": [
                    {"Name": "Org", "Value": org},
                    {"Name": constants.METRIC_DIMENSION_1, "Value": constants.METRIC_DIMENSION_1_VALUE}
                ],
                "Unit": "Count",
                "Value": value
            }]
        )
    except Exception as e:
        logger.warning(f"Failed to emit metric {name} for {org}: {str(e)}")
