import os
import logging
from logging.handlers import RotatingFileHandler

# Setup logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

xlogger = logging.getLogger("tarsier")
xlogger.setLevel(logging.INFO)

# Create rotating file handler
file_handler = RotatingFileHandler(
    os.path.join(log_dir, "tarsier.log"),
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=5,
)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

# Add both handlers to the logger
xlogger.addHandler(file_handler)
xlogger.addHandler(console_handler)
