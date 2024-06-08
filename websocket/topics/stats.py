from typing import TypedDict


class StatsOutboundData(TypedDict):
    total_touches: int
    total_shares: str
    total_players: int
    online_players: int
    daily_players: int

