import os

# Core Configuration
BUCKET_NAME = os.environ["BUCKET_NAME"]
AWS_REGION = os.environ.get("AWS_REGION_PARAM", "us-west-2")
SYSTEMNAME = os.environ.get("SYSTEMNAME", "orgdatalake")

# Tagging / Compliance
PROJECT_TAG = os.environ["PROJECT_TAG"]
CLASSIFICATION = os.environ.get("CLASSIFICATION", "PHI")
BOOTSTRAP = os.environ.get("BOOTSTRAP", "True")

# Defaults
DEFAULT_RECORD = os.environ.get("DEFAULT_RECORD", "contacts")

# Observability
ENABLE_METRICS = os.environ.get("ENABLE_METRICS", "true").lower() == "true"
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
METRIC_NAMESPACE = os.environ.get("METRIC_NAMESPACE", "CHX/DataLake/Provisioning")
METRIC_DIMENSION_1 = os.environ.get("METRIC_DIMENSION_1", "Component")
METRIC_DIMENSION_1_VALUE = os.environ.get("METRIC_DIMENSION_1_VALUE", "PrefixBootstrap")

# Optional
KMS_KEY_ID = os.environ.get("KMS_KEY_ID")
SSM_ENABLE_TAGGING = os.environ.get("SSM_ENABLE_TAGGING", "true").lower() == "true"
SSM_OVERWRITE = os.environ.get("SSM_OVERWRITE", "true").lower() == "true"
DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"
FAIL_FAST = os.environ.get("FAIL_FAST", "false").lower() == "true"
TAGS_ENVIRONMENT = os.environ.get("TAGS_ENVIRONMENT", "DEV")
RETENTION_DAYS = os.environ.get("RETENTION_DAYS", "90")

SSM_USE_SECURESTRING = os.environ.get("SSM_USE_SECURESTRING", "false").lower() == "true"
