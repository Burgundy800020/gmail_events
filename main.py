import time
from typing import List

import uvicorn

from config import settings
from structlog import get_logger
logger = get_logger(__name__)
from api_server import app

def main():
    logger.info("starting_application", mode=settings.mode)
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)

if __name__ == "__main__":
    main()













