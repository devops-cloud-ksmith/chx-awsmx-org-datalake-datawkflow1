# Placeholder for utils/logger.py
import logging
from config import constants

logger = logging.getLogger()
logger.setLevel(getattr(logging, constants.LOG_LEVEL, logging.INFO))
