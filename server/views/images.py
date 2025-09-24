from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi import Path as FastAPIPath

from core.settings import PiScannerServerSettings, get_settings
from schemas.images_schemas import ImageUploadResponse


router = APIRouter(prefix="/images")


@router.post("/upload/{scan_id}", response_model=ImageUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_image(
    scan_id: Annotated[str, FastAPIPath(..., description="The ID of the scan to upload the image to")],
    file: Annotated[UploadFile, File(...)],
    settings: Annotated[PiScannerServerSettings, Depends(get_settings)]
) -> ImageUploadResponse:
    # Create the datastore directory if it doesn't exist
    datastore_path = Path(settings.datastore_path).expanduser().joinpath(scan_id)
    datastore_path.mkdir(parents=True, exist_ok=True)

    new_filename = f"{datetime.now().timestamp()}.jpg"
    out_file = f"{datastore_path}/{new_filename}"
    content = await file.read()
    with open(out_file, "wb") as f:
        _ = f.write(content)

    return ImageUploadResponse(message="File uploaded successfully", filename=new_filename)
