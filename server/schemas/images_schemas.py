from pydantic import BaseModel


class ImageUploadResponse(BaseModel):
    message: str
    filename: str
