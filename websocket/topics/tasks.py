from typing import TypedDict


class TasksSpecialOutboundData(TypedDict):
    uuid: str
    title: str
    reward: int
    link: str
    status: bool
    claimed: bool


class TasksLeagueOutboundData(TypedDict):
    unclaimed: list[int]
    claimed: list[int]
    current: int
    total_amount: int


class TasksReferralOutboundData(TypedDict):
    unclaimed: list[int]
    claimed: list[int]
    current: int
    total_referral: int


class TasksOutboundData(TypedDict):
    special_tasks: list[TasksSpecialOutboundData]
    leagues: TasksLeagueOutboundData
    referral: TasksReferralOutboundData
    balance_up: int
    balance: int

class CheckTaskOutboundResponse(TypedDict):
    balance_up: int
    new_balance: int


class ClaimLeagueOutboundResponse(TypedDict):
    balance: int
    balance_up: int
    leagues: TasksLeagueOutboundData


class ClaimReferralOutboundResponse(TypedDict):
    unclaimed: list[int]
    claimed: list[int]
    current: int
    total_referral: int
    balance: int
    balance_up: int


class TaskStatus(TypedDict):
    claim: list[str]  # uuid to return
    check: list[str]  # uuid to return