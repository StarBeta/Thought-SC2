from enum import Enum

import numpy as np
import time

from strategy.agent import Agent as A
from unit.units import Army

import unit.protoss_unit as P


class ProtossAction(Enum):
    Do_nothing = 0
    Build_pylon = 1
    Build_gateway = 2
    Build_Assimilator = 3
    Build_CyberneticsCore = 4
    Build_probe = 5
    Build_zealot = 6
    Build_Stalker = 7
    Attack = 8
    Retreat = 9
    All = 10


class MiniAgent(A):

    def __init__(self, agent_id=0, global_buffer=None, net=None, restore_model=False):
        A.__init__(self, agent_id=agent_id, global_buffer=global_buffer,
                   net=net, restore_model=restore_model)
        self.init_feature()
        self.init_rl_param()
        self.MAX_ACTIONS = ProtossAction.All.value

    def __str__(self):
        return str(self.time_seconds) + ', ' + str(self.mineral) + \
            ', ' + str(self.mineral_worker_nums) + ', ' + str(self.zealot_num) + ', ' + str(self.food_cup)

    def reset(self, pos=0):
        super().reset(pos=0)
        self.init_feature()
        self.init_rl_param()

    def init_feature(self):
        self.gateway_num = 0
        self.pylon_num = 0
        self.Assimilator_num = 0
        self.CyberneticsCore_num = 0
        self.probe_num = 0
        self.zealot_num = 0
        self.Stalker_num = 0
        self.collected_mineral = 0
        self.spent_mineral = 0
        self.collected_gas = 0
        self.spent_gas = 0
        self.Nexus_num = 1

        self.production_building_list.append(P.Nexus())

    def obs(self):
        simple_input = np.zeros([20])

        simple_input[0] = 0  # self.time_seconds
        simple_input[1] = self.mineral_worker_nums
        simple_input[2] = self.gas_worker_nums
        simple_input[3] = self.mineral
        simple_input[4] = self.gas
        simple_input[5] = self.food_cup
        simple_input[6] = self.food_used
        simple_input[7] = self.army_nums

        simple_input[8] = self.gateway_num
        simple_input[9] = self.pylon_num
        simple_input[10] = self.Assimilator_num
        simple_input[11] = self.CyberneticsCore_num

        simple_input[12] = self.zealot_num
        simple_input[13] = self.Stalker_num
        simple_input[14] = self.probe_num

        simple_input[15] = self.collected_mineral
        simple_input[16] = self.spent_mineral
        simple_input[17] = self.collected_gas
        simple_input[18] = self.spent_gas
        simple_input[19] = self.Nexus_num

        return simple_input

    def set_obs(self, state):
        self.mineral_worker_nums = state[1]
        self.gas_worker_nums = state[2]
        self.mineral = state[3]
        self.gas = state[4]
        self.food_cup = state[5]
        self.food_used = state[6]
        self.army_nums = state[7]

        self.gateway_num = state[8]
        self.pylon_num = state[9]
        self.Assimilator_num = state[10]
        self.CyberneticsCore_num = state[11]

        self.zealot_num = state[12]
        self.Stalker_num = state[13]
        self.probe_num = state[14]

        self.collected_mineral = state[15]
        self.spent_mineral = state[16]
        self.collected_gas = state[17]
        self.spent_gas = state[18]

        self.Nexus_num = state[19]

    def get_next_state(self, action):
        self.step(action)
        return self.obs()

    @property
    def result(self):
        return self._result

    def play(self, verbose=False):
        self.env.simulate()

    def reset_env(self, verbose=False):
        self.env.reset()

    def init_rl_param(self):
        self.policy = None
        if self.global_buffer is not None:
            self.policy = self.net.policy
        else:
            self.policy = self.net.policy_old

        self.state_last = None
        self.state_now = self.obs()

        self.action_last = None
        self.action = None
        self.v_preds = None

    def step_auto(self, verbose=False):
        if self.env.is_end:
            # print(self.env.is_end)
            final_reward = 0
            if self.env.win_index == self.player_id:
                final_reward = 1
            elif self.env.win_index == -1:   # no one wins
                final_reward = 0
            else:
                final_reward = -1

            self.local_buffer.rewards[-1] += final_reward
            self._result = final_reward

            if 0:
                print(self.local_buffer.rewards)

            if self.global_buffer is not None:
                # print(self.agent_id)
                self.global_buffer.add(self.local_buffer)
            return

        if self.state_last is not None:
            v_preds_next = self.policy.get_values(self.state_now)
            v_preds_next = self.get_values(v_preds_next)
            reward = 0
            self.local_buffer.append(self.state_last, self.action_last, self.state_now, reward, self.v_preds, v_preds_next)

        self.action, self.v_preds = self.policy.get_action(self.state_now, verbose=False)
        self.state_last = self.state_now
        self.state_now = self.get_next_state(self.action)

        if verbose:
            #print('player_id:', self.player_id)
            print('state now:', self.state_now.astype(dtype=np.int32))
            print('action:', self.action)
            time.sleep(1)
        self.action_last = self.action

    def get_values(self, values):
        # check if the game is end
        if self.is_end and self.result != 0:
            return 0
        else:
            return values

    def get_action_by_policy(self, obs):
        act, v_preds = self.policy.get_action(obs, verbose=False)
        return act, v_preds

    def fullfill_technology(self, unit):
        if type(unit) == P.Pylon:
            if self.Nexus_num > 0:
                return True

        if type(unit) == P.Gateway:
            if self.pylon_num > 0:
                return True

        if type(unit) == P.CyberneticsCore:
            if self.pylon_num > 0 and self.gateway_num > 0:
                return True

        if type(unit) == P.Assimilator:
            if self.pylon_num > 0 and self.Assimilator_num < 2:
                return True

        if type(unit) == P.Probe:
            if self.Nexus_num > 0:
                return True

        if type(unit) == P.Zealot:
            if self.gateway_num > 0:
                return True

        if type(unit) == P.Stalker:
            if self.gateway_num > 0 and self.CyberneticsCore_num > 0:
                return True

        return False

    def fullfill_creature_condition(self, unit):
        if self.mineral >= unit.mineral_price and self.gas >= unit.gas_price:
            if self.food_cup >= self.food_used + unit.food_used and self.fullfill_technology(unit):
                return True
        else:
            return False

    def fullfill_food_condition(self, unit):
        if self.food_cup >= self.food_used + unit.food_used:
            return True
        else:
            return False

    def fullfill_building_condition(self, unit):
        if self.mineral >= unit.mineral_price and self.gas >= unit.gas_price:
            if self.fullfill_technology(unit):
                return True
        else:
            return False

    def caclulate_resources(self, unit, n=1):
        mineral_price = unit.mineral_price
        gas_price = unit.gas_price

        self.mineral -= mineral_price * n
        self.gas -= gas_price * n
        self.spent_mineral += mineral_price * n
        self.spent_gas += gas_price * n

    def step(self, action):
        if action == ProtossAction.Build_probe.value:
            Probe = P.Probe()
            if self.fullfill_creature_condition(Probe):
                self.caclulate_resources(Probe)
                self.build_from_nexus(Probe)

        elif action == ProtossAction.Build_zealot.value:
            Zealot = P.Zealot()
            if self.fullfill_creature_condition(Zealot):
                self.caclulate_resources(Zealot)
                #self.add_unit(Zealot, 1)
                self.build_from_gateway(Zealot)

        elif action == ProtossAction.Build_Stalker.value:
            Stalker = P.Stalker()
            if self.fullfill_creature_condition(Stalker):
                self.caclulate_resources(Stalker)
                #self.add_unit(Stalker, 1)
                self.build_from_gateway(Stalker)

        elif action == ProtossAction.Build_pylon.value:
            Pylon = P.Pylon()
            if self.fullfill_building_condition(Pylon):
                self.caclulate_resources(Pylon)
                self.init_building(Pylon)

        elif action == ProtossAction.Build_gateway.value:
            Gateway = P.Gateway()
            if self.fullfill_building_condition(Gateway):
                self.caclulate_resources(Gateway)
                self.init_building(Gateway)

        elif action == ProtossAction.Build_Assimilator.value:
            Assimilator = P.Assimilator()
            if self.fullfill_building_condition(Assimilator):
                self.caclulate_resources(Assimilator)
                self.init_building(Assimilator)

        elif action == ProtossAction.Build_CyberneticsCore.value:
            CyberneticsCore = P.CyberneticsCore()
            if self.fullfill_building_condition(CyberneticsCore):
                self.caclulate_resources(CyberneticsCore)
                self.init_building(CyberneticsCore)

        elif action == ProtossAction.Attack.value:
            if self.military_num() > 0:
                self.env.army[self.player_id].order = Army.Order.ATTACK

        elif action == ProtossAction.Retreat.value:
            if self.military_num() > 0:
                self.env.army[self.player_id].order = Army.Order.DEFEND

        self.update()

    def update(self):
        self.time_seconds += self.time_for_one_step
        self.update_resources()

        self.update_population_progress()
        self.update_population()

        self.update_building_progress()
        self.update_buildings()

        self.update_army()

    def manage_workers(self):
        idle_worker_for_mineral = 16
        idle_worker_for_gas = self.Assimilator_num * 3

        self.food_used += 1
        if self.mineral_worker_nums < idle_worker_for_mineral:
            self.mineral_worker_nums += 1
        elif self.gas_worker_nums < idle_worker_for_gas:
            self.gas_worker_nums += 1
        else:
            self.mineral_worker_nums += 1

    def get_empty_gateway(self):
        min_produce_len = 5
        min_building = None

        for b in self.production_building_list:
            if type(b) == type(P.Gateway()):
                produce_len = b.queue.size()
                if produce_len < min_produce_len:
                    min_produce_len = produce_len
                    min_building = b

        return min_building

    def build_from_gateway(self, unit):
        gateway = self.get_empty_gateway()
        if gateway is not None:
            gateway.queue.enqueue(unit)

    def build_from_nexus(self, unit):
        for b in self.production_building_list:
            if type(b) == type(P.Nexus()):
                b.queue.enqueue(unit)

    def update_population_progress(self):
        for b in self.production_building_list:
            if not b.queue.isEmpty():
                unit = b.queue.first_item()
                unit.progress += self.time_for_one_step
                if unit.progress >= unit.build_time and self.fullfill_food_condition(unit):
                    u = b.queue.dequeue()
                    if type(u) == type(P.Probe()):
                        self.manage_workers()
                    else:
                        self.add_unit(u)

    def update_building_progress(self):
        for b in self.on_building_list:
            b.progress += self.time_for_one_step
            if b.progress >= b.build_time:
                self.on_building_list.remove(b)
                self.add_building(b)

    def update_army(self):
        if self.military_num() == 0:
            self.env.army[self.player_id].order = Army.Order.NOTHING
            self.env.army[self.player_id].pos = self.pos

    def update_resources(self):
        # update mineral
        idle_worker_for_mineral = 20
        max_mineral_for_one_base = 10000

        add_mineral = min(self.mineral_worker_nums, idle_worker_for_mineral) * 3

        if self.collected_mineral + add_mineral < max_mineral_for_one_base:
            self.mineral += add_mineral
            self.collected_mineral += add_mineral

        idle_worker_for_gas = self.Assimilator_num * 3
        max_gas_for_one_base = 3000

        add_gas = min(self.gas_worker_nums, idle_worker_for_gas) * 2
        if self.collected_gas + add_gas < max_gas_for_one_base:
            self.gas += add_gas
            self.collected_gas += add_gas

    def update_population(self):
        # update population
        self.probe_num = self.mineral_worker_nums + self.gas_worker_nums
        self.army_nums = self.military_num()

        if type(P.Zealot()) in self.creatures_list.keys():
            self.zealot_num = self.creatures_list[type(P.Zealot())]
        else:
            self.zealot_num = 0
        if type(P.Stalker()) in self.creatures_list.keys():
            self.Stalker_num = self.creatures_list[type(P.Stalker())]
        else:
            self.Stalker_num = 0

        self.food_used = self.zealot_num * 2 + \
            self.Stalker_num * 2 + \
            self.probe_num * 1

    def update_buildings(self):
        self.building_nums = self.building_num()

        if type(P.Pylon()) in self.building_list.keys():
            self.pylon_num = self.building_list[type(P.Pylon())]
        else:
            self.pylon_num = 0

        if type(P.Gateway()) in self.building_list.keys():
            self.gateway_num = self.building_list[type(P.Gateway())]
        else:
            self.gateway_num = 0

        if type(P.Assimilator()) in self.building_list.keys():
            self.Assimilator_num = self.building_list[type(P.Assimilator())]
        else:
            self.Assimilator_num = 0

        if type(P.CyberneticsCore()) in self.building_list.keys():
            self.CyberneticsCore_num = self.building_list[type(P.CyberneticsCore())]
        else:
            self.CyberneticsCore_num = 0

        self.food_cup = self.pylon_num * 8 + \
            self.Nexus_num * 15
