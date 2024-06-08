from websocket.user_actions.types import UserApp
from websocket.user_actions.utils import tomorrow_unix
from websocket.utils.mongo_handler import users
from websocket.utils.constants import LEAGUES


def new_user_bot(user_id: int, user_name: str, name: str, ref_id: int = None):
    user = UserApp(
        user_id=user_id,
        name=name,
        user_name=user_name,
        ip=[],
        amount=2,
        last_click=None,
        last_online=None,
        league=LEAGUES[0],
        energy=500,
        league_claimed=[],
        referral_claimed=[],
        task_claimed=[],
        multi_tap=1,
        limit=1,
        speed=1,
        tap_bot=True,

        balance=250250,
        total_click=0,

        rewards=0,
        ref_direct_rewards=0,
        guru_left=3,
        refill_left=3,
        next_update=tomorrow_unix(),
        ref_from_id=ref_id,
        ref_to=[],
        is_guru=False,
        end_guru=None,
        task_check=[],
        task_claim=[]
    )
    users.insert_one(user)
    return True
