from pydantic import BaseModel


class ImageUploadResponse(BaseModel):
    message: str
    filename: str


class ImageInfo(BaseModel):
    filename: str
    timestamp: float


class ImageListResponse(BaseModel):
    scan_id: str
    images: list[ImageInfo]
