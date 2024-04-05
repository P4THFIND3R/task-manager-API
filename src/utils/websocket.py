from fastapi import WebSocket
from typing import List


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    def connect(self, websocket: WebSocket):
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    @staticmethod
    async def send_personal_message(websocket: WebSocket, message: str):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.connections:
            await connection.send_text(message)


websocket_manager = ConnectionManager()
