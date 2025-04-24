import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from s3.prefix_creator import create_prefix
from ssm.ssm_writer import write_parameter
from ssm.config_loader import get_config_param
from config import constants
from datetime import datetime
import logging

logger = logging.getLogger()

def lambda_handler(event, context):
    org = event.get("org")
    record = event.get("record", get_config_param("DEFAULT_RECORD", constants.DEFAULT_RECORD))
    data_tiers = event.get("tiers", ["raw"])
    date_path = event.get("date", datetime.utcnow().strftime("%Y/%m/%d"))

    results = []

    for tier in data_tiers:
        try:
            key = f"{constants.SYSTEMNAME}/{tier}/{org}/{record}/{date_path}/jira_{record}.json"
            s3_key = f"s3://{constants.BUCKET_NAME}/{key}"
            create_prefix(tier, org, record, date_path)
            write_parameter(tier, org, record, s3_key)
            results.append(f"{tier}: OK")
        except Exception as e:
            logger.error(f"{tier}: ERROR - {str(e)}")
            results.append(f"{tier}: ERROR - {str(e)}")
            if constants.FAIL_FAST:
                break

    return {
        "status": "complete",
        "executed_on": datetime.utcnow().isoformat(),
        "executed_for": org,
        "date_path": date_path,
        "record": record,
        "results": results
    }