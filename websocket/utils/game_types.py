from typing import TypedDict


class ReferralLeagueData(TypedDict):
    title: str
    reward: int
    threshold: int


class TaskData(TypedDict):
    title: str
    uuid: str
    link: str
    reward: int
