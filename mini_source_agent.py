from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
from pysc2.agents import base_agent
from pysc2.lib import actions as sc2_actions

from lib import utils as U
from lib import config as C

from lib import transform_pos as T
from lib import option as M
from lib import environment
from lib import my_sc2_env as sc2_env
from lib.replay_buffer import Buffer
from mini_agent import ProtossAction


class MiniSourceAgent(base_agent.BaseAgent):
    """Agent for source game of starcraft."""

    def __init__(self, index=0, rl_training=False, restore_model=False, global_buffer=None, net=None, strategy_agent=None, greedy_action=False):
        super(MiniSourceAgent, self).__init__()
        self.net = net
        self.index = index
        self.global_buffer = global_buffer
        self.restore_model = restore_model

        # model in brain
        self.strategy_agent = strategy_agent
        self.strategy_act = None

        # count num
        self.step = 0

        self.strategy_wait_secs = 2
        self.strategy_flag = False
        self.policy_wait_secs = 2
        self.policy_flag = True

        self.env = None
        self.obs = None

        # buffer
        self.local_buffer = Buffer()

        self.num_players = 2
        self.on_select = None
        self._result = None
        self._gases = None
        self.is_end = False

        self.greedy_action = greedy_action
        self.rl_training = rl_training

    def reset(self):
        super(MiniSourceAgent, self).reset()
        self.step = 0
        self.obs = None
        self._result = None
        self._gases = None
        self.is_end = False

        self.strategy_flag = False
        self.policy_flag = True

        self.local_buffer.reset()

        if self.strategy_agent is not None:
            self.strategy_agent.reset()

    def set_env(self, env):
        self.env = env

    def init_network(self):
        self.net.initialize()
        if self.restore_model:
            self.net.restore_policy()

    def reset_old_network(self):
        self.net.reset_old_network()

    def save_model(self):
        self.net.save_policy()

    def update_network(self, result_list):
        self.net.Update_policy(self.global_buffer)
        self.net.Update_result(result_list)

    def update_summary(self, counter):
        return self.net.Update_summary(counter)

    def mini_step(self, action):
        if action == ProtossAction.Build_probe.value:
            M.mineral_worker(self)

        elif action == ProtossAction.Build_zealot.value:
            M.train_army(self, C._TRAIN_ZEALOT)

        elif action == ProtossAction.Build_Stalker.value:
            M.train_army(self, C._TRAIN_STALKER)

        elif action == ProtossAction.Build_pylon.value:
            no_unit_index = U.get_unit_mask_screen(self.obs, size=2)
            pos = U.get_pos(no_unit_index)
            M.build_by_idle_worker(self, C._BUILD_PYLON_S, pos)

        elif action == ProtossAction.Build_gateway.value:
            power_index = U.get_power_mask_screen(self.obs, size=5)
            pos = U.get_pos(power_index)
            M.build_by_idle_worker(self, C._BUILD_GATEWAY_S, pos)

        elif action == ProtossAction.Build_Assimilator.value:
            if self._gases is not None:
                #U.find_gas_pos(self.obs, 1)
                gas_1 = self._gases[0]
                gas_2 = self._gases[1]

                if gas_1 is not None and not U.is_assimilator_on_gas(self.obs, gas_1):
                    gas_1_pos = T.world_to_screen_pos(self.env.game_info, gas_1.pos, self.obs)
                    M.build_by_idle_worker(self, C._BUILD_ASSIMILATOR_S, gas_1_pos)

                elif gas_2 is not None and not U.is_assimilator_on_gas(self.obs, gas_2):
                    gas_2_pos = T.world_to_screen_pos(self.env.game_info, gas_2.pos, self.obs)
                    M.build_by_idle_worker(self, C._BUILD_ASSIMILATOR_S, gas_2_pos)

        elif action == ProtossAction.Build_CyberneticsCore.value:
            power_index = U.get_power_mask_screen(self.obs, size=3)
            pos = U.get_pos(power_index)
            M.build_by_idle_worker(self, C._BUILD_CYBER_S, pos)

        elif action == ProtossAction.Attack.value:
            M.attack_step(self)

        elif action == ProtossAction.Retreat.value:
            M.retreat_step(self)

        elif action == ProtossAction.Do_nothing.value:
            self.safe_action(C._NO_OP, 0, [])

    def get_the_input(self):
        high_input, tech_cost, pop_num = U.get_input(self.obs)
        controller_input = np.concatenate([high_input, tech_cost, pop_num], axis=0)
        return controller_input

    def mapping_source_to_mini_by_rule(self, source_state):
        simple_input = np.zeros([20])
        simple_input[0] = 0  # self.time_seconds
        simple_input[1] = source_state[28]  # self.mineral_worker_nums
        simple_input[2] = source_state[30] + source_state[32]  # self.gas_worker_nums
        simple_input[3] = source_state[2]  # self.mineral
        simple_input[4] = source_state[3]  # self.gas
        simple_input[5] = source_state[6]  # self.food_cup
        simple_input[6] = source_state[7]  # self.food_used
        simple_input[7] = source_state[10]  # self.army_nums

        simple_input[8] = source_state[16]  # self.gateway_num
        simple_input[9] = source_state[14]  # self.pylon_num
        simple_input[10] = source_state[15]  # self.Assimilator_num
        simple_input[11] = source_state[17]  # self.CyberneticsCore_num

        simple_input[12] = source_state[12]  # self.zealot_num
        simple_input[13] = source_state[13]  # self.Stalker_num
        simple_input[14] = source_state[11]  # self.probe_num

        simple_input[15] = source_state[4] + source_state[2]  # self.collected_mineral
        simple_input[16] = source_state[4]  # self.spent_mineral
        simple_input[17] = source_state[5] + source_state[3]  # self.collected_gas
        simple_input[18] = source_state[5]  # self.spent_gas
        simple_input[19] = 1  # self.Nexus_num

        return simple_input

    def play(self, verbose=False):
        self.play_train_mini(verbose=verbose)

    def play_train_mini(self, verbose=False):
        is_attack = False
        state_last = None

        self.safe_action(C._NO_OP, 0, [])
        self.safe_action(C._MOVE_CAMERA, 0, [C.base_camera_pos])
        self._gases = U.find_initial_gases(self.obs)
        while True:

            self.safe_action(C._MOVE_CAMERA, 0, [C.base_camera_pos])
            if self.policy_flag and (not self.is_end):

                state_now = self.mapping_source_to_mini_by_rule(self.get_the_input())
                if self.greedy_action:
                    action_prob, v_preds = self.net.policy.get_action_probs(state_now, verbose=False)
                    action = np.argmax(action_prob)
                else:
                    action, v_preds = self.net.policy.get_action(state_now, verbose=False)

                # print(ProtossAction(action).name)
                self.mini_step(action)

                if state_last is not None:
                    if 0:
                        print('state_last:', state_last, ', action_last:', action_last, ', state_now:', state_now)
                    v_preds_next = self.net.policy.get_values(state_now)
                    v_preds_next = self.get_values(v_preds_next)
                    reward = 0
                    self.local_buffer.append(state_last, action_last, state_now, reward, v_preds, v_preds_next)

                # continuous attack, consistent with mind-game
                if action == ProtossAction.Attack.value:
                    is_attack = True
                if is_attack:
                    self.mini_step(ProtossAction.Attack.value)

                state_last = state_now
                action_last = action
                self.policy_flag = False

            if self.is_end:
                if self.rl_training:
                    self.local_buffer.rewards[-1] += 1 * self.result['reward']  # self.result['win']
                    print(self.local_buffer.rewards)
                    self.global_buffer.add(self.local_buffer)
                    print("add %d buffer!" % (len(self.local_buffer.rewards)))
                break

    def set_flag(self):
        if self.step % C.time_wait(self.strategy_wait_secs) == 1:
            self.strategy_flag = True

        if self.step % C.time_wait(self.policy_wait_secs) == 1:
            self.policy_flag = True

    def safe_action(self, action, unit_type, args):
        if M.check_params(self, action, unit_type, args, 1):
            obs = self.env.step([sc2_actions.FunctionCall(action, args)])[0]
            self.obs = obs
            self.step += 1
            self.update_result()
            self.set_flag()

    def select(self, action, unit_type, args):
        # safe select
        if M.check_params(self, action, unit_type, args, 0):
            self.obs = self.env.step([sc2_actions.FunctionCall(action, args)])[0]
            self.on_select = unit_type
            self.update_result()
            self.step += 1
            self.set_flag()

    @property
    def result(self):
        return self._result

    def update_result(self):
        if self.obs is None:
            return
        if self.obs.last() or self.env.state == environment.StepType.LAST:
            self.is_end = True
            outcome = 0
            o = self.obs.raw_observation
            player_id = o.observation.player_common.player_id
            for r in o.player_result:
                if r.player_id == player_id:
                    outcome = sc2_env._possible_results.get(r.result, 0)
            frames = o.observation.game_loop
            result = {}
            result['outcome'] = outcome
            result['reward'] = self.obs.reward
            result['frames'] = frames

            self._result = result
            print('play end, total return', self.obs.reward)
            self.step = 0

    def get_values(self, values):
        # check if the game is end
        if self.is_end and self.result['reward'] != 0:
            return 0
        else:
            return values
