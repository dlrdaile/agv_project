"""
author:dlr123
date:2022年06月14日
"""
from collections import defaultdict
from typing import Dict,Union

from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder

class ConnectionManager :
    def __init__(self) :
        self.active_connections: Dict[str,Dict[int,WebSocket]] = defaultdict(dict)

    async def connect(self,id: int,route: str,websocket: WebSocket) :
        await websocket.accept()
        self.active_connections[route][id] = websocket

    def disconnect(self,id: int,route: str) :
        self.active_connections[route].pop(id)

    async def send_personal_text(self,message: str,id: int,route: str) :
        await self.active_connections[route][id].send_text(message)

    async def send_personal_json(self,message: Union[dict,list],id: int,route: str) :
        message = jsonable_encoder(message)
        await self.active_connections[route][id].send_json(message)

    async def send_personal_stream(self,message,id: int,route: str) :
        await self.active_connections[route][id].send_bytes(message)

    async def broadcast_text(self,route: str,message: str) :
        for connection in self.active_connections[route].values() :
            await connection.send_text(message)

    async def broadcast_json(self,route: str,message: Union[dict,list]) :
        message = jsonable_encoder(message)
        for connection in self.active_connections[route].values() :
            await connection.send_json(message)

    async def broadcast_stream(self,route: str,message) :
        for connection in self.active_connections[route].values() :
            await connection.send_bytes(message)
