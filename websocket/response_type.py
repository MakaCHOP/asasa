import json

from websockets import WebSocketServerProtocol

from websocket.topic import Topics, OutboundData


async def send_wss_msg(websocket: WebSocketServerProtocol, topic: Topics, result: dict, status: bool = True) -> bool:
    await websocket.send(
        json.dumps(
            OutboundData(
                topic=topic.value,
                status=status,
                result=result,
            )
        )
    )
    return True
