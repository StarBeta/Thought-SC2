from enum import Enum
from copy import copy, deepcopy
import numpy as np
import math
import time

from unit.units import Army
from lib.replay_buffer import Buffer


class StrategyforSC2(Enum):
    RUSH = 1
    ECONOMY = 2
    DEFENDER = 3


class Agent:

    def __init__(self, agent_id=0, global_buffer=None, net=None, restore_model=False):
        self.env = None
        self.mpc = None
        self.net = net

        self.agent_id = agent_id
        self.player_id = 0

        self.global_buffer = global_buffer
        self.restore_model = restore_model

        self.local_buffer = Buffer()
        self.restart_game()

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            # print(k)
            if k == 'net' or k == 'env' or k == 'mpc':
                #print(k, 'is not deepcopy')
                setattr(result, k, v)
                continue
            setattr(result, k, deepcopy(v, memo))
        return result

    def reset(self, pos):
        self.set_pos(pos)
        self.set_army()

        self.local_buffer.reset()
        self.restart_game()

    def restart_game(self):
        self.is_end = False
        self._result = None

        self.time_seconds = 0
        self.mineral_worker_nums = 12
        self.gas_worker_nums = 0
        self.mineral = 50
        self.gas = 0
        self.food_cup = 15
        self.food_used = 12
        self.army_nums = 0
        self.enemy_army_nums = 0
        self.building_nums = 1
        self.enemy_building_nums = 1
        self.defender_nums = 0
        self.enemy_defender_nums = 0
        self.strategy = StrategyforSC2.RUSH
        self.enemy_strategy = StrategyforSC2.ECONOMY
        self.creatures_list = {}
        self.building_list = {}
        self.remain_buildings_hp = 1500

        self.on_building_list = []
        self.production_building_list = []

        self.time_for_one_step = 9

    def obs():
        return None

    def init(self, env, player_id, pos):
        self.set_env(env)
        self.set_id(player_id)
        self.set_pos(pos)
        self.set_army()

    def init_network(self):
        self.net.initialize()
        if self.restore_model:
            self.net.restore_policy()

    def update_network(self, result_list):
        self.net.Update_policy(self.global_buffer)
        self.net.Update_result(result_list)

    def reset_old_network(self):
        self.net.reset_old_network()

    def save_model(self):
        self.net.save_policy()

    def update_summary(self, counter):
        return self.net.Update_summary(counter)

    def set_buffer(self, global_buffer):
        self.global_buffer = global_buffer

    def set_env(self, env):
        self.env = env

    def set_net(self, net):
        self.net = net

    def set_mpc(self, mpc):
        self.mpc = mpc

    def set_id(self, player_id):
        self.player_id = player_id

    def set_pos(self, pos):
        self.pos = pos

    def set_army(self):
        army = Army(self.player_id)
        army.pos = self.pos
        self.env.army[self.player_id] = army

    def init_building(self, building_obj):
        self.on_building_list.append(building_obj)

    def add_unit(self, unit_obj, num=1):
        unit_type = type(unit_obj)
        if unit_type in self.creatures_list:
            self.creatures_list[unit_type] += num
        else:
            self.creatures_list[unit_type] = num

    def add_building(self, building_obj, num=1):
        building_type = type(building_obj)

        # TODO: add shied to hp
        hp = building_type().hp
        self.remain_buildings_hp += hp * num

        if building_type in self.building_list:
            self.building_list[building_type] += num
        else:
            self.building_list[building_type] = num

        queue = getattr(building_obj, "queue", None)
        if queue is not None:
            self.production_building_list.append(building_obj)

    def building_hp(self):
        return self.remain_buildings_hp

    def under_attack(self, attack_hp):
        self.remain_buildings_hp -= attack_hp

    def military_force(self):
        return self.creatures_list

    def buildings(self):
        return self.building_list

    def building_num(self):
        count = 0
        for key, value in self.building_list.items():
            count += value
        return count

    def military_num(self):
        count = 0
        for key, value in self.creatures_list.items():
            count += value
        return count

    def reset_military(self, remain_hp):
        all_hp = 0
        remain_creatures_list = {}
        for key, value in self.creatures_list.items():
            unit_type = key
            number = value
            unit = unit_type()
            count = 0
            for _ in range(number):
                all_hp += unit.hp
                if all_hp <= remain_hp:
                    count += 1
                else:
                    break
            remain_creatures_list[unit_type] = count
            if all_hp >= remain_hp:
                break

        self.creatures_list = remain_creatures_list
