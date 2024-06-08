import json
import os
import time

from bson import json_util

from websocket.utils.mongo_handler import users
from dotenv import load_dotenv

load_dotenv()


def referral_link_factory(user_id: int) -> str:
    return f'https://telegram.me/{os.getenv("BOT_USERNAME")}?start={user_id}'


def get_user_data(user_id) -> dict:
    return json.loads(json_util.dumps(users.find_one({"user_id": user_id})))


def tomorrow_unix() -> int:
    return (int(time.time() / 86400) + 1) * 86400


def today_unix() -> int:
    return int(time.time() / 86400) * 86400


def energy_and_auto_bot_on_demand_calc(user_data: dict) -> (int, int):
    energy = user_data["energy"]
    last_online = user_data['last_online']
    speed = user_data['speed']
    limit = user_data['limit'] * 500
    time_diff = int(time.time()) - last_online
    time_needed = (limit - energy) / speed

    if time_diff > time_needed:
        offline_bot_earning = min(int(time_diff - time_needed) * speed, (43200 - time_needed) * speed)
        return limit, offline_bot_earning
    else:
        offline_bot_earning = min(time_diff * speed, 43200 * speed)
        energy = min(time_diff * speed + energy, limit)
        return energy, offline_bot_earning


def static_data_on_demand(user_id: int):
    user_data = get_user_data(user_id)
    user_data['energy'], user_data["bot_earning"] = energy_and_auto_bot_on_demand_calc(user_data)
    if user_data['next_update'] <= today_unix():
        user_data['next_update'] = tomorrow_unix()
        user_data['guru_left'] = 3
        user_data['refill_left'] = 3
    users.update_one({"user_id": user_id}, user_data)
    return user_data
