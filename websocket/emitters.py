import asyncio
import logging
import os
import time
from asyncio import AbstractEventLoop
from threading import Thread
from typing import Unpack, Any

from dotenv import load_dotenv
from functools import cache
from websockets import serve, WebSocketServerProtocol

from websocket.response_type import send_wss_msg
from websocket.topic import TopicEmitter, Topics
from websocket.topics.balance import BalanceOutboundData, BotEarningOutboundData, TapOutboundResponse
from websocket.topics.boost import BoosterOutboundData, BoosterDetailOutboundData, SpecialBoosterOutboundData, \
    ActivateOutboundResponse, UpgradeOutboundData
from websocket.topics.energy import EnergyOutboundData
from websocket.topics.refferral import ReferralOutboundData, RefData
from websocket.topics.stats import StatsOutboundData
from websocket.topics.tasks import TaskStatus, TasksOutboundData, TasksSpecialOutboundData, TasksLeagueOutboundData, \
    TasksReferralOutboundData, ClaimLeagueOutboundResponse
from websocket.user_actions.types import UserApp
from websocket.user_actions.utils import static_data_on_demand, referral_link_factory, get_user_data
from websocket.utils.constants import LEAGUES, LEVELS, TASKS, REFERRALS


@cache
def kwarg_getter(kwa: dict[str, Any]) -> (WebSocketServerProtocol, dict):
    ws = kwa.get("ws")
    user_data = kwa.get("user_data")
    return ws, user_data


async def tp_balance_emit(**kwargs: Unpack[TopicEmitter]):
    ws = kwargs.get("ws")
    user_data = kwargs.get("user_data")
    result = BalanceOutboundData(balance=user_data['balance'],
                                 multi_tap=user_data['multi_tap'], auto_bot=user_data['tap_bot'],
                                 guru=user_data['is_guru'],
                                 league=LEAGUES[LEAGUES.index(user_data['league'])])
    await send_wss_msg(ws, Topics.BALANCE, result, True)


async def tp_energy_emit(**kwargs: Unpack[TopicEmitter]):
    ws = kwargs.get("ws")
    user_data = kwargs.get("user_data")
    result = EnergyOutboundData(energy=(int(user_data["energy"])),
                                max_energy=user_data["limit"] * 500,
                                energy_speed=user_data["speed"])
    await send_wss_msg(ws, Topics.ENERGY, result, True)


async def tp_bot_earning_emit(**kwargs: Unpack[TopicEmitter]):
    ws = kwargs.get("ws")
    user_data = kwargs.get("user_data")
    result = BotEarningOutboundData(earning=user_data['bot_earning'])
    await send_wss_msg(ws, Topics.BOT_EARNING, result, user_data['tap_bot'])
    user_data['bot_earning'] = 0



async def tp_special_boost_emit(**kwargs: Unpack[TopicEmitter]):
    ws = kwargs.get("ws")
    user_data = kwargs.get("user_data")
    result = SpecialBoosterOutboundData(max_special_boost=3,
                                        guru_left=user_data["guru_left"],
                                        next_update=user_data['next_update'],
                                        full_tank_left=user_data["refill_left"])
    # todo: shit code line below

    await send_wss_msg(ws, Topics.SPECIAL_BOOST, result, True)


async def tp_stats_emit(**kwargs: Unpack[TopicEmitter]):
    ws = kwargs.get("ws")
    user_data = kwargs.get("user_data")
    # todo: result is fake
    print("tatata")
    result = StatsOutboundData(total_touches=100000,
                               total_shares="76.2 T",
                               total_players=2846128,
                               online_players=2131247,
                               daily_players=21421432)
    await send_wss_msg(ws, Topics.STATS, result, True)


async def tp_task_stat_emit(**kwargs: Unpack[TopicEmitter]):
    ws = kwargs["ws"]
    user_data = kwargs["user_data"]
    print(user_data, "sabababa")
    result = TaskStatus(check=user_data['task_check'], claim=user_data['task_claim'])
    await send_wss_msg(ws, Topics.TASKS_STATUS, result, True)


async def tp_referral_emit(**kwargs: Unpack[TopicEmitter]):
    ws = kwargs["ws"]
    user_data = kwargs["user_data"]
    refs: list = user_data['ref_to']

    for i in range(len(refs)):
        refs[i] = get_user_data(refs[i])
    result = ReferralOutboundData(
        invite_link=referral_link_factory(user_data['user_id']),
        my_refs=[RefData(
            league=LEAGUES.index(x['league']),
            name=x['name'],
            total_amount=x['amount'],
            referrer_link=""
        ) for x in refs],
        ref_num=len(refs)
    )
    await send_wss_msg(ws, Topics.REFERRAL, result, True)


async def tp_boost_emit(**kwargs: Unpack[TopicEmitter]):
    ws = kwargs["ws"]
    user_data = kwargs["user_data"]
    result = BoosterOutboundData(
        multi_tap=BoosterDetailOutboundData(
            level=user_data["multi_tap"],
            is_max=user_data['multi_tap'] == len(LEVELS['multi_tap']),
            next_level_price=LEVELS["multi_tap"][int(user_data["multi_tap"])]
        ),
        energy_limit=BoosterDetailOutboundData(
            level=user_data["limit"],
            is_max=user_data['limit'] == len(LEVELS['limit']),
            next_level_price=LEVELS['limit'][user_data["limit"]]
        ),
        recharging_speed=BoosterDetailOutboundData(
            level=user_data["speed"],
            is_max=user_data['speed'] == len(LEVELS['speed']),
            next_level_price=LEVELS["speed"][user_data["speed"]]
        ),
        tap_bot=BoosterDetailOutboundData(
            level=user_data["tap_bot"],
            is_max=user_data['tap_bot'] == len(LEVELS['bot']),
            next_level_price=LEVELS["bot"][0]
        )
    )
    await send_wss_msg(ws, Topics.BOOST, result, True)


def current_ref_calc(num_ref: int) -> int:
    for i in range(len(REFERRALS)):
        if num_ref < REFERRALS[i]["threshold"]:
            return i
    return 0


async def tp_tasks_emit(**kwargs: Unpack[TopicEmitter]):
    ws = kwargs["ws"]
    user_data = kwargs["user_data"]
    result = TasksOutboundData(
        special_tasks=[TasksSpecialOutboundData(
            title=x["title"],
            uuid=x["uuid"],
            link=x["link"],
            reward=x["reward"],
            status=True,
            claimed=x in user_data["task_claimed"]) for x in TASKS],
        leagues=TasksLeagueOutboundData(
            unclaimed=[LEAGUES.index(x) for x in LEAGUES[:LEAGUES.index(user_data['league'])]],
            claimed=[LEAGUES.index(x) for x in user_data["league_claimed"]],
            current=LEAGUES.index(user_data["league"]),
            total_amount=user_data["amount"]
        ),
        referral=TasksReferralOutboundData(
            unclaimed=list(
                set([REFERRALS.index(x) for x in REFERRALS if x['threshold'] < len(user_data['ref_to'])]) - set(
                    [REFERRALS.index(x) for x in user_data["referral_claimed"]])),
            claimed=[REFERRALS.index(x) for x in user_data["referral_claimed"]],
            current=current_ref_calc(len(user_data['ref_to'])),
            total_referral=len(user_data["ref_to"]),
        ),
        balance_up=232323,
        balance=user_data['balance']
    )  # todo task confirm for done
    await send_wss_msg(ws, Topics.TASKS, result, True)


async def tp_activate_callback(*args, **kwargs: Unpack[TopicEmitter]):
    ws = kwargs["ws"]
    user_data = kwargs["user_data"]
    if user_data[args[0] + "_left"] > 0:
        if args[0] == "refill":
            user_data['energy'] = user_data["limit"] * 500
        else:
            user_data['is_guru'] = True
            user_data['end_guru'] = time.time() + 20
        user_data[args[0] + "_left"] = user_data[args[0] + "_left"] - 1

        result = ActivateOutboundResponse(
            unit=args[0],
            new_left=user_data[args[0] + "_left"],
            finish_time=user_data['next_update'],
            energy=int(user_data["energy"])
        )  #  todo: guru worker

        await send_wss_msg(ws, Topics.ACTIVATE, result)


async def tp_upgrade_callback(*args, **kwargs: Unpack[TopicEmitter]):
    ws = kwargs["ws"]
    user_data = kwargs["user_data"]

    if args[0] != "bot":
        new_level = user_data[args[0]] + 1

        if new_level < len(LEVELS[args[0]]) and user_data["balance"] > LEVELS[args[0]][new_level - 1]:
            user_data[args[0]] += 1
            user_data['balance'] -= LEVELS[args[0]][new_level - 1]
            is_max = user_data[args[0]] == len(LEVELS)
            result = UpgradeOutboundData(
                is_max=is_max,
                new_level=new_level,
                next_level_price=LEVELS[args[0]][new_level] if not is_max else 0,
                upgraded_unit=args[0],
                balance=user_data["balance"] - LEVELS[args[0]][new_level - 1]
            )
            await send_wss_msg(ws, Topics.UPGRADE, result)
        else:
            pass
    elif user_data['tap_bot'] is not True:
        user_data["balance"] = user_data["balance"] - LEVELS[args[0]][0]
        user_data['tap_bot'] = True
        await send_wss_msg(ws, Topics.UPGRADE, UpgradeOutboundData(
            is_max=True,
            new_level=1,
            next_level_price=0,
            upgraded_unit=args[0],
            balance=user_data["balance"] - LEVELS[args[0]][0]
        ))
    else:
        pass


async def tp_task_pending_callback(*args, **kwargs: Unpack[TopicEmitter]):
    ws = kwargs["ws"]
    user_data = kwargs["user_data"]
    uuid = args[0]
    # ind = 0
    # for i in TASKS:
    #     if i['uuid'] == uuid:
    #         break
    #     ind += 1
    user_data["task_check"].append(uuid)
    await send_wss_msg(ws, Topics.TASKS_STATUS, TaskStatus(
        check=user_data["task_check"],
        claim=user_data["task_claim"]
    ))


async def tp_task_check_callback(*args, **kwargs: Unpack[TopicEmitter]):
    ws = kwargs["ws"]
    user_data = kwargs["user_data"]
    uuid = args[0]
    # ind = 0
    # for i in TASKS:
    #     if i['uuid'] == uuid:
    #         break
    #     ind += 1
    user_data["task_claim"].append(uuid)
    user_data["task_check"].remove(uuid)
    user_data['task_claimed'].append(uuid)
    await send_wss_msg(ws, Topics.TASKS_STATUS, TaskStatus(
        check=user_data["task_check"],
        claim=user_data["task_claim"]
    ))


async def tp_tap_callback(*args, **kwargs: Unpack[TopicEmitter]):
    ws = kwargs["ws"]
    user_data = kwargs["user_data"]
    energy = int(user_data["energy"])
    multi_tap = user_data['multi_tap']
    if energy - multi_tap >= 0:
        # user_data['energy'] -= multi_tap
        if user_data['is_guru']:
            multi_tap *= 5
        else:
            user_data['energy'] -= multi_tap
        user_data['balance'] += multi_tap
        user_data["amount"] += multi_tap
        user_data['last_click'] = int(time.time())
        user_data['total_click'] += 1
        if user_data["amount"] > user_data['league']['threshold']:
            user_data['league'] = LEAGUES[LEAGUES.index(user_data['league']) + 1]
            await tp_balance_emit(ws=ws, user_data=user_data)
        await send_wss_msg(ws, Topics.TAP, TapOutboundResponse(
            balance=user_data["balance"] + 1,
            amount=user_data['amount'] + 1,
            energy=int(user_data['energy'])
        ))


async def tp_claim_league_callback(*args, **kwargs: Unpack[TopicEmitter]):
    ws = kwargs["ws"]
    user_data = kwargs["user_data"]
    ind = args[0]

    if args[0] < LEAGUES.index(user_data['league']) and args[0] not in user_data['league_claimed']:
        user_data['league_claimed'].append(LEAGUES[ind])
        user_data['balance'] += LEAGUES[ind]['reward']
        user_data['rewards'] += LEAGUES[ind]['reward']

        await send_wss_msg(ws, Topics.CLAIM_LEAGUE, ClaimLeagueOutboundResponse(
            leagues=TasksLeagueOutboundData(
                unclaimed=list(set(LEAGUES[:LEAGUES.index(user_data['league'])]) - set(user_data['league_claimed'])),
                claimed=user_data['league_claimed'],
                current=LEAGUES.index(user_data['league']),
                total_amount=user_data['amount'],
            ),
            balance=user_data['balance'],
            balance_up=LEAGUES[ind]['reward']
        ))


async def tp_claim_task_callback(*args, **kwargs: Unpack[TopicEmitter]):
    ws = kwargs["ws"]
    user_data = kwargs["user_data"]
    uuid = args[0]
    ind = 0
    for i in TASKS:
        if i['uuid'] == uuid:
            break
        ind += 1

    if TASKS[ind] not in user_data['task_claimed'] and args[0] in user_data['task_claimed']:
        user_data['task_claimed'].append(TASKS[ind])
        user_data['balance'] += TASKS[ind]['reward']
        user_data['rewards'] += TASKS[ind]['reward']
        await tp_tasks_emit(ws=ws, user_data=user_data)
        await tp_balance_emit(ws=ws, user_data=user_data)


async def tp_claim_ref_callback(*args, **kwargs: Unpack[TopicEmitter]):
    ws = kwargs["ws"]
    user_data = kwargs["user_data"]
    ind = args[0]

    if REFERRALS[ind] not in user_data['referral_claimed'] and REFERRALS[ind]['threshold'] < len(user_data['ref_to']):
        user_data['referral_claimed'].append(REFERRALS[ind])
        user_data['balance'] += REFERRALS[ind]['reward']
        user_data['rewards'] += REFERRALS[ind]['reward']
        await tp_tasks_emit(ws=ws, user_data=user_data)
        await tp_balance_emit(ws=ws, user_data=user_data)
