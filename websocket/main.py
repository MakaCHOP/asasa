import asyncio
import logging
import os
from typing import Unpack

from dotenv import load_dotenv
from websockets import serve, WebSocketServerProtocol

from Socket.main import LEAGUES
from websocket.response_type import send_wss_msg
from websocket.topic import TopicEmitter, Topics
from websocket.topics.balance import BalanceOutboundData
from websocket.user_actions.utils import static_data_on_demand

load_dotenv()

PORT = os.getenv('PORT')
HOST = os.getenv('HOST')
BOT_USERNAME = os.getenv("BOT_USERNAME")

logging.basicConfig(
    format="%(asctime)s --- SpaceX Swap --- %(message)s",
    level=logging.INFO,
)


async def handler(ws: WebSocketServerProtocol):
    tg_uid = ws.path[1:]
    user_data = static_data_on_demand(tg_uid)


async def main():
    async with serve(host=HOST, port=PORT, ws_handler=handler):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
