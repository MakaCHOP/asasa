from typing import TypedDict

class RefData(TypedDict):
    name: str
    league: int
    total_amount: int
    referrer_link: str


class ReferralOutboundData(TypedDict):
    invite_link: str
    my_refs: list[RefData]
    ref_num: int

