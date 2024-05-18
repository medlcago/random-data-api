import logging

import uvicorn
from fastapi import FastAPI

from api.main import api_router
from core.config import config

app = FastAPI(title=config.api.project_name)
app.include_router(api_router, prefix=config.api.api_v1_str)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    datefmt="%d-%m-%Y %H:%M:%S"
                    )

if __name__ == "__main__":
    try:
        uvicorn.run(app, host=config.api.domain, port=config.api.port)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Application stopped.")
