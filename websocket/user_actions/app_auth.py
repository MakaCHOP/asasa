import json
import time

from bson import json_util

from websocket.utils.mongo_handler import users


def app_login(user_id: int, ip):
    # user = json.loads(json_util.dumps(users.find_one({"user_id": user_id})))
    users.update_one({"user_id": user_id}, {
        '$addToSet': {'ip': ip},
        "last_online": time.time(),
    })


def app_log_out():
    pass  # todo: handle exit to save data and free up memory
