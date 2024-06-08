import asyncio
import functools
import json
import logging
import os
import time

from dotenv import load_dotenv
from websockets import serve, WebSocketServerProtocol

from websocket.user_actions.types import UserApp
from websocket.user_actions.utils import static_data_on_demand
from websocket.emitters import *
from websocket.utils.mongo_handler import users

load_dotenv()

PORT = os.getenv('PORT')
HOST = os.getenv('HOST')
BOT_USERNAME = os.getenv("BOT_USERNAME")


# logging.basicConfig(
#     format="%(asctime)s --- SpaceX Swap --- %(message)s",
#     level=logging.INFO,
# )


def save_on_ws_close(user_data: UserApp):
    del user_data["_id"]

    users.update_one({"user_id": user_data['user_id']}, {"$set": user_data})


async def on_socket_close(websocket, user_data: UserApp):
    closed = asyncio.ensure_future(websocket.wait_closed())
    await asyncio.sleep(5)
    closed.add_done_callback(lambda task: save_on_ws_close(user_data))


async def handler(ws: WebSocketServerProtocol):
    tg_uid = ws.path[1:]
    user_data: UserApp = static_data_on_demand(tg_uid)
    if not user_data:
        logging.warning("user is not registered in the bot")
        return

    logging.info(f"user Connected! Telegram Id: {user_data['user_id']} Client IP: {ws.remote_address[0]}")
    await tp_balance_emit(ws=ws, user_data=user_data)
    await tp_boost_emit(ws=ws, user_data=user_data)
    await tp_energy_emit(ws=ws, user_data=user_data)
    await tp_bot_earning_emit(ws=ws, user_data=user_data)
    await tp_special_boost_emit(ws=ws, user_data=user_data)
    await tp_stats_emit(ws=ws, user_data=user_data)
    await tp_tasks_emit(ws=ws, user_data=user_data)
    await tp_task_stat_emit(ws=ws, user_data=user_data)
    await tp_referral_emit(ws=ws, user_data=user_data)
    loop = asyncio.get_running_loop()
    await loop.create_task(on_socket_close(ws, user_data))
    async for message in ws:
        data = json.loads(message)
        request = data["request"]
        topic = data["topic"]
        if topic == "activate":
            await tp_activate_callback(request, ws=ws, user_data=user_data)
        elif topic == "upgrade":
            await tp_upgrade_callback(request, ws=ws, user_data=user_data)
        elif topic == "tap":
            await tp_tap_callback(request, ws=ws, user_data=user_data)
        elif topic == "task pending":
            await tp_task_pending_callback(request, ws=ws, user_data=user_data)
        elif topic == "task check":
            await tp_task_check_callback(request, ws=ws, user_data=user_data)
        elif "claim league" == topic:
            await tp_claim_league_callback(request, ws=ws, user_data=user_data)
        elif "claim task" == topic:
            await tp_claim_task_callback(request, ws=ws, user_data=user_data)
        elif "claim referral" == topic:
            await tp_claim_ref_callback(request, ws=ws, user_data=user_data)


async def main():
    async with serve(host=HOST, port=PORT, ws_handler=handler):
        await asyncio.Future()
