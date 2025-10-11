from contextlib import asynccontextmanager
from logging import Logger
import os
import fastapi
from pydantic.types import DirectoryPath
import uvicorn

from fastapi.staticfiles import StaticFiles

from core.loghandler import LogHandler
from core.settings import PiScannerServerSettings, get_settings
from api.base import router as base_router
from api.images import router as images_router
from api.scan_websocket import router as scan_websocket_router
from views.scans import router as scans_router


def startup(settings: PiScannerServerSettings, logger: Logger):
    datastore_path: str = os.path.expanduser(settings.datastore_path)

    # Initialize image storage directory
    logger.info(f"Initializing image storage directory at {datastore_path}")
    if not os.path.exists(datastore_path):
        os.makedirs(datastore_path, exist_ok=True)


def get_lifespan(settings: PiScannerServerSettings, logger: Logger):
    @asynccontextmanager
    async def lifespan(app: fastapi.FastAPI):
        startup(settings, logger)
        yield

    return lifespan


def get_application(settings: PiScannerServerSettings, logger: Logger):
    app = fastapi.FastAPI(lifespan=get_lifespan(settings, logger))

    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Backend routes
    app.include_router(base_router)
    app.include_router(images_router)
    app.include_router(scan_websocket_router)

    # Frontend routes
    app.include_router(scans_router)

    return app


settings = get_settings()
logger = LogHandler.get_logger(name="main")
app = get_application(settings, logger)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
