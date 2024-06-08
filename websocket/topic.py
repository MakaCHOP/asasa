from enum import Enum
from typing import TypedDict, Required

from websockets import WebSocketServerProtocol

from websocket.user_actions.types import UserApp


class Topics(Enum):
    ACTIVATE = "activate"
    ENERGY = 'energy'
    BALANCE = "balance"
    BOT_EARNING = "bot earning"
    STATS = "stats"
    SPECIAL_BOOST = "special boost"
    BOOST = "boost"
    TASKS = "tasks"
    REFERRAL = "referral"
    TASKS_STATUS = "task status"
    CLAIM_TASK = "claim task"
    UPGRADE = "upgrade"
    TAP = "tap"
    CLAIM_LEAGUE = "claim league"
    CLAIM_REFERRAL = "claim referral"


class OutboundData(TypedDict):
    topic: Topics
    result: object
    status: bool


class TopicEmitter(TypedDict):
    ws: Required[WebSocketServerProtocol]
    user_data: Required[UserApp]


