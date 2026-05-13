import logging
import sys

logger = logging.getLogger('event_logger')
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)

log_format = logging.Formatter("[%(asctime)s] %(levelname)s | %(message)s", datefmt="%H:%M:%S")

handler.setFormatter(log_format)

logger.addHandler(handler)