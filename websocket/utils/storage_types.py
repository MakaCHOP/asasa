from typing import TypedDict, NotRequired

from websocket.utils.game_types import ReferralLeagueData, TaskData
from websocket.topics.refferral import RefData


class BaseUserRef(TypedDict):
    user_id: int
    name: str
    link: str
    amount: int


class BaseUser(TypedDict):
    name: str
    username: str
    ip: list[str]
    amount: int


class UserReferralData(TypedDict):
    ref_from: BaseUserRef
    ref_to: list[RefData]
    ref_link: str
    current: int


class UserReferralTaskData(TypedDict):
    claimed_tasks: list[ReferralLeagueData]
    tasks: list[ReferralLeagueData]


class UserLeagueData(TypedDict):
    claimed_tasks: list[ReferralLeagueData]
    tasks: list[ReferralLeagueData]


class UserTaskData(TypedDict):
    claimed_tasks: list[TaskData]
    tasks: list[TaskData]


class UserBalance(TypedDict):
    balance: int
    total_click: int
    rewards: int
    ref_direct_rewards: int


class UserBoosts(TypedDict):
    multi_tap: int
    limit: int
    speed: int
    tap_bot: bool


class SpecialPerks(TypedDict):
    left: int
    next_update: int


class UserSpecialBoost(TypedDict):
    guru: SpecialPerks
    refill: SpecialPerks


class UserInGameData(TypedDict):
    last_click: int | None
    league: ReferralLeagueData
    energy: int
    last_online: int | None


class UserData(TypedDict):
    _id: NotRequired[str]
    user_id: int
    user: BaseUser
    referral: UserReferralData
    ref_task: UserReferralTaskData
    special_task: UserTaskData
    league_task: UserLeagueData
    in_game: UserInGameData
    special_boost: UserSpecialBoost
    boost: UserBoosts
    balance: UserBalance
