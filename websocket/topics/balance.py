from typing import TypedDict, Literal

class BalanceOutboundData(TypedDict):
    balance: int
    multi_tap: int
    guru: bool
    auto_bot: bool
    league: int


class BotEarningOutboundData(TypedDict):
    earning: int

class TapOutboundResponse(TypedDict):
    balance: int
    amount: int
    energy: int
