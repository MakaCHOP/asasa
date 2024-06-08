import uuid

from websocket.utils.game_types import ReferralLeagueData, TaskData

LEVELS = {
    "multi_tap": [200, 500, 2000, 5000, 20_000, 75_000, 200_000, 300_000, 500_000, 750_000, 1_250_000, 2_500_000],
    "limit": [200, 500, 2000, 5000, 20_000, 75_000, 200_000, 300_000, 500_000, 750_000, 1_250_000, 2_500_000],
    "speed": [1000, 20_000, 50_000, 125_000, 250_000],
    "bot": [200_000]

}

REFERRALS = [
    ReferralLeagueData(title="invite 1 friends", reward=25_000, threshold=1),
    ReferralLeagueData(title="invite 3 friends", reward=50_000, threshold=3),
    ReferralLeagueData(title="invite 10 friends", reward=200_000, threshold=10),
    ReferralLeagueData(title="invite 25 friends", reward=250_000, threshold=25),
    ReferralLeagueData(title="invite 50 friends", reward=300_000, threshold=50),
    ReferralLeagueData(title="invite 100 friends", reward=500_000, threshold=100),
    ReferralLeagueData(title="invite 500 friends", reward=2_000000, threshold=500),
    ReferralLeagueData(title="invite 1000 friends", reward=2_500000, threshold=1000),
    ReferralLeagueData(title="invite 10000 friends", reward=10_000000, threshold=10000),
    ReferralLeagueData(title="invite 100000 friends", reward=100_000000, threshold=100000),
]

LEAGUES = [
    ReferralLeagueData(title="Wooden League", reward=500, threshold=1),
    ReferralLeagueData(title="Bronze League", reward=1000, threshold=100),
    ReferralLeagueData(title="Silver League", reward=5000, threshold=5000),
    ReferralLeagueData(title="Gold League", reward=10000, threshold=50000),
    ReferralLeagueData(title="Platinum League", reward=25000, threshold=250000),
]


TASKS = [
    TaskData(title="Google", reward=500, link="https://google.com", uuid=uuid.uuid4().__str__()),
    TaskData(title="Ice me Out", reward=50000, link="https://fbi.gov", uuid=uuid.uuid4().__str__()),
    TaskData(title="Intelligence", reward=500554, link="https://cia.gov", uuid=uuid.uuid4().__str__()),
]