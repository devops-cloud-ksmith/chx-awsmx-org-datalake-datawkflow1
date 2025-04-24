import logging
import os
from config import constants

LOG_PATH = "logs"
os.makedirs(LOG_PATH, exist_ok=True)

logger = logging.getLogger()
logger.setLevel(getattr(logging, constants.LOG_LEVEL, logging.INFO))

# File handler
fh = logging.FileHandler(os.path.join(LOG_PATH, "lambda_run.log"))
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# Console handler
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
