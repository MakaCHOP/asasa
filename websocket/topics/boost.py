from typing import TypedDict, Literal


class SpecialBoosterOutboundData(TypedDict):
    max_special_boost: int
    guru_left: int
    full_tank_left: int
    next_update: int


class BoosterDetailOutboundData(TypedDict):
    level: int
    is_max: bool
    next_level_price: int


class BoosterOutboundData(TypedDict):
    multi_tap: BoosterDetailOutboundData
    energy_limit: BoosterDetailOutboundData
    recharging_speed: BoosterDetailOutboundData
    tap_bot: BoosterDetailOutboundData


class UpgradeOutboundData(TypedDict):
    upgraded_unit: Literal["multi_tap", "tap_bot", "limit", "speed"]
    new_level: int
    is_max: bool
    next_level_price: int
    balance: int


class ActivateOutboundResponse(TypedDict):
    unit: Literal["guru", "refill"]
    new_left: int
    finish_time: int
    energy: int
