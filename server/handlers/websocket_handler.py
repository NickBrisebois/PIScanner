from contextlib import asynccontextmanager
from fastapi.websockets import WebSocket

from core.loghandler import LogHandler
from schemas.websocket_schemas import WebSocketMessage


logger = LogHandler.get_logger(__name__)


class WebSocketHandler:
    _active_connections: dict[str, list[WebSocket]] = {}

    def __init__(self):
        self._active_connections = {}

    @asynccontextmanager
    async def register_websocket(self, websocket: WebSocket, scan_id: str):
        if scan_id not in self._active_connections:
            self._active_connections[scan_id] = []

        self._active_connections[scan_id].append(websocket)

        await websocket.accept()
        yield websocket
        await websocket.close()

    async def kill_scan_sockets(self, scan_id: str):
        if scan_id not in self._active_connections:
            return

        for websocket in self._active_connections[scan_id]:
            await websocket.close()

        del self._active_connections[scan_id]

    async def broadcast(self, scan_id: str, data: WebSocketMessage):
        if scan_id not in self._active_connections:
            return

        for websocket in self._active_connections[scan_id]:
            try:
                await websocket.send_text(data.model_dump_json())
            except Exception as e:
                logger.error(f"Error sending message to websocket: {e}")


websocket_handler = WebSocketHandler()


def get_websocket_handler():
    return websocket_handler
