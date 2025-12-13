import logging
from logging.handlers import RotatingFileHandler
import os

os.makedirs('logs', exist_ok=True)

logger = logging.getLogger('OnSitePresence')
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    filename='logs/presence.log',
    maxBytes=1_000_000,
    backupCount=3)

file_handler.setFormatter(
    logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

logger.propagate = False
