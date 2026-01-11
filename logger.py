import logging
from logging.handlers import RotatingFileHandler
import os

os.makedirs('logs', exist_ok=True)

logger = logging.getLogger('OnSitePresence')
logger.setLevel(logging.INFO)

access_logger = logging.getLogger('OnSitePresence.access')
access_logger.setLevel(logging.INFO)
access_logger.propagate = False

file_handler = RotatingFileHandler(
    filename='logs/presence.log',
    maxBytes=1_000_000,
    backupCount=3)

access_handler = RotatingFileHandler(
    filename='logs/access.log',
    maxBytes=1_000_000,
    backupCount=3)

file_handler.setFormatter(
    logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))

access_handler.setFormatter(
    logging.Formatter('[%(asctime)s] %(client_ip)s %(path)s %(user_agent)s'))

console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))


class AccessDefaultsFilter(logging.Filter):
    def filter(self, record: dict) -> bool:
        record.client_ip = getattr(record, 'client_ip', 'unknown')
        record.path = getattr(record, 'path', 'unknown')
        record.user_agent = getattr(record, 'user_agent', 'unknown')
        return True


if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False

if not access_logger.handlers:
    access_logger.addHandler(access_handler)
    access_logger.addFilter(AccessDefaultsFilter())
