from datetime import datetime
import logging
from pathlib import Path
from typing import Annotated
from xxlimited import new

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi import Path as FastAPIPath
from fastapi.responses import FileResponse

from core.loghandler import get_logger
from core.settings import PiScannerServerSettings, get_settings
from handlers.websocket_handler import WebSocketHandler, get_websocket_handler
from schemas.images_schemas import ImageInfo, ImageListResponse, ImageUploadResponse
from schemas.websocket_schemas import MessageType, ScanUpdateMessage, WebSocketMessage


router = APIRouter(prefix="/images")


@router.post(
    "/upload/{scan_id}",
    response_model=ImageUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_image(
    scan_id: Annotated[
        str, FastAPIPath(..., description="The ID of the scan to upload the image to")
    ],
    file: Annotated[UploadFile, File(...)],
    websocket_handler: Annotated[WebSocketHandler, Depends(get_websocket_handler)],
    settings: Annotated[PiScannerServerSettings, Depends(get_settings)],
    logger: Annotated[logging.Logger, Depends(get_logger)],
) -> ImageUploadResponse:
    # Create the datastore directory if it doesn't exist
    datastore_path = Path(settings.datastore_path).expanduser().joinpath(scan_id)
    datastore_path.mkdir(parents=True, exist_ok=True)

    new_filename = f"{datetime.now().timestamp()}.jpg"
    out_file = f"{datastore_path}/{new_filename}"
    content = await file.read()
    with open(out_file, "wb") as f:
        _ = f.write(content)

    logger.info(f"Receiving image for scan {scan_id}, view at /scans/{scan_id}")
    await websocket_handler.broadcast(
        scan_id=scan_id,
        data=ScanUpdateMessage(
            message_type=MessageType.NEW_IMAGE,
            scan_id=scan_id,
            image_url=f"/images/{scan_id}/{new_filename}",
            filename=new_filename,
        ),
    )

    return ImageUploadResponse(
        message="File uploaded successfully", filename=new_filename
    )


@router.get("/{scan_id}/{image_id}")
async def get_image(
    scan_id: Annotated[
        str, FastAPIPath(..., description="The ID of the scan to get images for")
    ],
    image_id: Annotated[
        str, FastAPIPath(..., description="The file name of the image to get")
    ],
    settings: Annotated[PiScannerServerSettings, Depends(get_settings)],
) -> FileResponse:
    datastore_path = Path(settings.datastore_path).expanduser().joinpath(scan_id)
    image_path = datastore_path.joinpath(image_id)
    if not image_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    return FileResponse(image_path)


@router.get("/{scan_id}", response_model=ImageListResponse)
async def list_images(
    scan_id: Annotated[
        str, FastAPIPath(..., description="The ID of the scan to get images for")
    ],
    settings: Annotated[PiScannerServerSettings, Depends(get_settings)],
) -> ImageListResponse:
    datastore_path = Path(settings.datastore_path).expanduser().joinpath(scan_id)
    images = [
        ImageInfo(
            filename=str(image.relative_to(datastore_path)),
            timestamp=image.stat().st_mtime,
        )
        for image in datastore_path.glob("*.jpg")
    ]
    return ImageListResponse(images=images, scan_id=scan_id)
