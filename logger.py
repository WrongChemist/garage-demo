import logging
from datetime import datetime
from flask import request

def setup_logger(app):
    logger = logging.getLogger("garage_logger")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("access.log")
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    @app.before_request
    def log_request():
        logger.info(f"{request.method} {request.path} from {request.remote_addr}")
