from websocket.utils.game_types import TaskData
from websocket.utils.storage_types import *

class UserApp(TypedDict):
    user_id: int
    name: str
    user_name: str | None
    ip: list[str]
    amount: int
    last_click: int | None
    last_online: int | None
    league: ReferralLeagueData
    energy: int
    league_claimed: list[ReferralLeagueData]
    referral_claimed: list[ReferralLeagueData]
    task_claimed: list[TaskData]
    multi_tap: int
    limit: int
    speed: int
    tap_bot: bool
    balance: int
    total_click: int
    rewards: int
    ref_direct_rewards: int
    guru_left: int
    refill_left: int
    next_update: int
    ref_from_id: int
    ref_to: list[int]
    is_guru: bool
    end_guru: float | None
    task_check: NotRequired[list[int]]
    task_claim: NotRequired[list[int]]
