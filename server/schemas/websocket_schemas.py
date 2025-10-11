from enum import Enum

from pydantic import BaseModel


class MessageType(str, Enum):
    NEW_IMAGE = "NEW_IMAGE"


class WebSocketMessage(BaseModel):
    message_type: MessageType


class ScanUpdateMessage(WebSocketMessage):
    scan_id: str
    image_url: str
    filename: str
