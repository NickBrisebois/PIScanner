from typing import Annotated
from fastapi import APIRouter, Depends, WebSocket

from handlers.websocket_handler import WebSocketHandler, get_websocket_handler


router = APIRouter(prefix="/ws")


@router.websocket("/scan/{scan_id}")
async def scan_websocket(
    websocket: WebSocket,
    scan_id: str,
    websocket_handler: Annotated[WebSocketHandler, Depends(get_websocket_handler)],
):
    async with websocket_handler.register_websocket(
        scan_id=scan_id, websocket=websocket
    ):
        while True:
            data = await websocket.receive_text()
            if data == "stop":
                await websocket.send_text("Scan stopped")
                break

            await websocket.send_text(f"Received: {data}")
