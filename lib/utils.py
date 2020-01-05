import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage
from pysc2.lib import actions as sc2_actions
from pysc2.lib import features
import lib.transform_pos as T
from lib import config as C

_MINIMAP_SELECTED = features.MINIMAP_FEATURES.selected.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_HEIGHT_MAP = features.SCREEN_FEATURES.height_map.index
_VISIABLE_MAP = features.SCREEN_FEATURES.visibility_map.index
_RELATIVE = features.SCREEN_FEATURES.player_relative.index

_SELF_INDEX = 1
_VISIBLE_INDEX = 1
_ENEMY_INDEX = 4
_PROBE_TYPE_INDEX = 84
_PYLON_TYPE_INDEX = 60
_FORGE_TYPE_INDEX = 63
_CANNON_TYPE_INDEX = 66


def pool_screen_power(power_map):
    pool_size = 4
    map_size = power_map.shape[0]

    out_size = map_size // pool_size
    out = np.zeros((out_size, out_size))

    for row_index in range(out_size):
        row_num = row_index * pool_size
        for col_index in range(out_size):
            col_num = col_index * pool_size
            out[row_index, col_index] = int(np.all(power_map[row_num:row_num + pool_size, col_num:col_num + 4]))

    return out


def get_power_mask_minimap(obs):
    minimap_camera = obs.observation["minimap"][3]
    screen_power = obs.observation["screen"][3]

    screen_unit_type = obs.observation["screen"][_UNIT_TYPE]
    screen_unit = (screen_unit_type == 0).astype("int")

    reduce_screen_power = np.logical_and(screen_power, screen_unit).astype("int")
    trans_power = pool_screen_power(reduce_screen_power).reshape(-1)

    minimap_camera = minimap_camera.reshape(-1)
    minimap_camera[minimap_camera == 1] = trans_power

    return (minimap_camera == 1).astype("int")


def dialted_unit(screen_unit, size=1):
    struct = ndimage.generate_binary_structure(2, 1)
    dialted_screen_unit = ndimage.binary_dilation(screen_unit,
                                                  structure=struct, iterations=size).astype(screen_unit.dtype)
    return dialted_screen_unit


def dialted_area(area, size=1):
    struct = ndimage.generate_binary_structure(2, 1)
    dialted_area = ndimage.binary_dilation(area,
                                           structure=struct, iterations=size).astype(area.dtype)
    return dialted_area


def get_power_mask_screen(obs, size=None, show=False):
    screen_power = obs.observation["screen"][3]
    screen_unit_type = obs.observation["screen"][_UNIT_TYPE]
    screen_unit = (screen_unit_type != 0).astype("int")
    area_1 = dialted_area(1 - get_available_area(obs), size=size)
    area_2 = dialted_area(screen_unit, size=size)
    area_3 = dialted_area(1 - screen_power, size=size)

    reduce_area = np.logical_and(1 - area_1, 1 - area_2).astype("int")
    reduce_area = np.logical_and(reduce_area, 1 - area_3).astype("int")

    if show:
        imgplot = plt.imshow(reduce_area)
        plt.show()
    return reduce_area.reshape(-1)


def get_pos(pos_prob_array):
    if pos_prob_array.sum() != 0:
        pos = np.random.choice(64 * 64, size=1, p=(pos_prob_array / pos_prob_array.sum()))
    else:
        pos = 0

    x = pos % 64
    y = pos // 64
    return [x, y]


def get_available_area(obs, show=False):
    height_type = obs.observation["screen"][_HEIGHT_MAP].astype("int")
    area_1 = (height_type == np.amax(height_type)).astype("int")
    visiable_type = obs.observation["screen"][_VISIABLE_MAP].astype("int")
    area_2 = (visiable_type == np.amax(visiable_type)).astype("int")
    available_area = np.logical_and(area_1, area_2).astype("int")
    if show:
        imgplot = plt.imshow(available_area)
        plt.show()
    return available_area


def get_unit_mask_screen(obs, size=None, show=False):
    screen_unit_type = obs.observation["screen"][_UNIT_TYPE]
    screen_unit = (screen_unit_type != 0).astype("int")
    not_available_area = np.logical_or(1 - get_available_area(obs), screen_unit).astype("int")
    if size:
        not_available_area = dialted_area(not_available_area, size=size)
    reduce_area = 1 - not_available_area
    if show:
        imgplot = plt.imshow(reduce_area)
        plt.show()
    return reduce_area.reshape(-1)


def find_unit(obs, index):
    unit_set = obs.raw_observation.observation.raw_data.units
    for unit in unit_set:
        if unit.unit_type == index and unit.build_progress == 1:
            return unit

    return None


def find_unit_on_screen(obs, index):
    unit_set = obs.raw_observation.observation.raw_data.units
    for unit in unit_set:
        if unit.unit_type == index and unit.build_progress == 1 and unit.is_on_screen:
            return unit
    return None


def check_base_camera(game_info, obs):
    camera_world_pos = obs.raw_observation.observation.raw_data.player.camera
    camera_minimap_pos = T.world_to_minimap_pos(game_info, camera_world_pos)
    if camera_minimap_pos == C.base_camera_pos:
        return True
    return False


def get_minimap_data(timestep, verbose=False):
    obs = timestep
    map_width = 64
    relative_type_map = obs.observation["minimap"][C._M_RELATIVE_TYPE].reshape(-1, map_width, map_width) / 255
    if verbose:
        imgplot = plt.imshow(relative_type_map[0])
        plt.show()
    visiable_type_map = obs.observation["minimap"][C._M_VISIABLE_TYPE].reshape(-1, map_width, map_width) / 255
    player_id_map = obs.observation["minimap"][C._M_PLAYID_TYPE].reshape(-1, map_width, map_width) / 255
    if verbose:
        imgplot = plt.imshow(visiable_type_map[0])
        plt.show()
    if verbose:
        imgplot = plt.imshow(player_id_map[0])
        plt.show()
    map_data = np.concatenate([relative_type_map, visiable_type_map, player_id_map], axis=0)
    return map_data


def find_gas(obs, index):
    # index == 1 or 2
    gas = []
    unit_set = obs.raw_observation.observation.raw_data.units
    for unit in unit_set:
        if unit.unit_type == C._ASSIMILATOR_TYPE_INDEX:
            # if unit is visible and on screen
            if unit.alliance == _SELF_INDEX:
                gas.append(unit)
    if len(gas) == 2:
        if gas[0].pos.x > gas[1].pos.x:
            tmp = gas[0]
            gas[0] = gas[1]
            gas[1] = tmp
        return gas[index - 1]
    elif len(gas) == 1:
        return gas[0]

    return None


def find_gas_pos(obs, index):
    # index == 1 or 2
    unit_set = obs.raw_observation.observation.raw_data.units
    for unit in unit_set:
        if unit.unit_type == C._GAS_TYPE_INDEX:
            if unit.display_type == _VISIBLE_INDEX and unit.is_on_screen == True:
                print(unit)
    return None


def find_initial_gases(obs):
    # index == 1 or 2
    gas = []
    unit_set = obs.raw_observation.observation.raw_data.units
    for unit in unit_set:
        if unit.unit_type == C._GAS_TYPE_INDEX:
            # if unit is visible and on screen
            if unit.display_type == _VISIBLE_INDEX and unit.is_on_screen == True:
                gas.append(unit)
    if len(gas) == 2:
        if gas[0].pos.x > gas[1].pos.x:
            tmp = gas[0]
            gas[0] = gas[1]
            gas[1] = tmp

        # print(gas[0])
        # print(gas[1])

        return gas

    return None


def is_assimilator_on_gas(obs, gas):
    unit_set = obs.raw_observation.observation.raw_data.units
    for unit in unit_set:
        if unit.unit_type == C._ASSIMILATOR_TYPE_INDEX:
            if unit.pos.x == gas.pos.x and unit.pos.y == gas.pos.y:
                return True
    return False


def get_unit_num(obs, unit_type):
    num = 0
    unit_set = obs.raw_observation.observation.raw_data.units
    for unit in unit_set:
        if unit.unit_type == unit_type:
            num += 1

    return num


def get_unit_num_array(obs, unit_type_list):
    num_array = np.zeros(len(unit_type_list))

    unit_set = obs.raw_observation.observation.raw_data.units
    for unit in unit_set:
        if unit.unit_type in unit_type_list:
            num_array[unit_type_list.index(unit.unit_type)] += 1

    return np.array(num_array)


def get_tech_action_num(obs, action_id):
    num = 0
    unit_set = obs.raw_observation.observation.raw_data.units
    for unit in unit_set:
        if unit.orders:
            if unit.orders[0].ability_id == action_id:
                num += 1

    return num


def judge_gas_worker_too_many(obs):
    gas_1 = find_gas(obs, 1)
    gas_2 = find_gas(obs, 2)
    have_gas_1, have_gas_2 = 0, 0
    if gas_1:
        if gas_1.assigned_harvesters > gas_1.ideal_harvesters:
            have_gas_1 = 1
    if gas_2:
        if gas_2.assigned_harvesters > gas_2.ideal_harvesters:
            have_gas_2 = 1
    if have_gas_1 + have_gas_2 > 0:
        return True
    else:
        return False


def judge_gas_worker(obs, game_info):
    gas_1 = find_gas(obs, 1)
    gas_2 = find_gas(obs, 2)
    if gas_1:
        a = gas_1.assigned_harvesters
        i = gas_1.ideal_harvesters
        if a < i:
            return T.world_to_screen_pos(game_info, gas_1.pos, obs)
            # return C.gas1_pos
    if gas_2:
        a = gas_2.assigned_harvesters
        i = gas_2.ideal_harvesters
        if a < i:
            return T.world_to_screen_pos(game_info, gas_2.pos, obs)
            # return C.gas2_pos

    return None


def get_gas_probe(obs):
    # if have resources, back to base
    buff = None
    unit_set = obs.raw_observation.observation.raw_data.units

    for unit in unit_set:
        if unit.unit_type == C._PROBE_TYPE_INDEX and unit.is_on_screen == True:
            buff = unit.buff_ids
            # [274] gas
            # [271] mineal
            if buff and buff[0] == 274:
                return unit


def get_mineral_probe(obs):
    # if have resources, back to base
    buff = None
    unit_set = obs.raw_observation.observation.raw_data.units

    for unit in unit_set:
        if unit.unit_type == C._PROBE_TYPE_INDEX and unit.is_on_screen == True:
            buff = unit.buff_ids
            # [274] gas
            # [271] mineral
            if buff and buff[0] == 271:
                return unit


def get_back_pos(obs, game_info):
    # if have resources, back to base
    buff = None
    unit_set = obs.raw_observation.observation.raw_data.units
    for unit in unit_set:
        if unit.unit_type == C._PROBE_TYPE_INDEX and unit.is_selected == True:
            buff = unit.buff_ids
            # print('buff:', buff)

    if buff and buff[0] > 0:
        # return C.base_pos
        base = find_unit_on_screen(obs, C._NEXUS_TYPE_INDEX)
        base_pos = T.world_to_screen_pos(game_info, base.pos, obs) if base else None
        return base_pos

    base = find_unit_on_screen(obs, C._NEXUS_TYPE_INDEX)
    # number of probe for mineral and the ideal num
    if base:
        a = base.assigned_harvesters
        i = base.ideal_harvesters
        if a < i:
            mineral = find_unit_on_screen(obs, C._MINERAL_TYPE_INDEX)
            mineral_pos = T.world_to_screen_pos(game_info, mineral.pos, obs) if mineral else None
            return mineral_pos
            # return C.mineral_pos

    gas_1 = find_gas(obs, 1)
    gas_2 = find_gas(obs, 2)
    if gas_1:
        a = gas_1.assigned_harvesters
        i = gas_1.ideal_harvesters
        if a < i:
            return T.world_to_screen_pos(game_info, gas_1.pos, obs)
            # return C.gas1_pos
    if gas_2:
        a = gas_2.assigned_harvesters
        i = gas_2.ideal_harvesters
        if a < i:
            return T.world_to_screen_pos(game_info, gas_2.pos, obs)
            # return C.gas2_pos
    return T.world_to_screen_pos(game_info, base.pos, obs) if base else None
    # return C.mineral_pos


def get_production_num(obs, train_order_list):
    num_list = np.zeros(len(train_order_list))

    unit_set = obs.raw_observation.observation.raw_data.units
    for unit in unit_set:
        if unit.alliance == 1 and unit.orders:
            for order in unit.orders:
                if order.ability_id in train_order_list:
                    index = train_order_list.index(order.ability_id)
                    num_list[index] += 1

    return num_list


def get_best_gateway(obs):
    unit_set = obs.raw_observation.observation.raw_data.units
    best_unit = None

    for unit in unit_set:
        if unit.unit_type == C._GATEWAY_TYPE_INDEX and unit.build_progress == 1:
            if (not best_unit) or (not unit.orders) or len(best_unit.orders) > len(unit.orders):
                best_unit = unit
            if not best_unit.orders:
                return best_unit

    return best_unit


def get_attack_num(obs, army_index_list):
    unit_set = obs.raw_observation.observation.raw_data.units
    num = 0

    for unit in unit_set:
        if unit.unit_type in army_index_list:
            if unit.orders:
                for order in unit.orders:
                    if order.ability_id == C._A_ATTACK_ATTACK_MINIMAP_S:
                        num += 1

    return num


def get_map_data(obs):
    map_width = 64
    m_height = obs.observation["minimap"][C._M_HEIGHT].reshape(-1, map_width, map_width) / 255
    m_visible = obs.observation["minimap"][C._M_VISIBILITY].reshape(-1, map_width, map_width) / 2
    m_camera = obs.observation["minimap"][C._M_CAMERA].reshape(-1, map_width, map_width)
    m_relative = obs.observation["minimap"][C._M_RELATIVE].reshape(-1, map_width, map_width) / 4
    m_selected = obs.observation["minimap"][C._M_SELECTED].reshape(-1, map_width, map_width)

    s_relative = obs.observation["screen"][C._S_RELATIVE].reshape(-1, map_width, map_width) / 4
    s_selected = obs.observation["screen"][C._S_SELECTED].reshape(-1, map_width, map_width)
    s_hitpoint = obs.observation["screen"][C._S_HITPOINT_R].reshape(-1, map_width, map_width) / 255
    s_shield = obs.observation["screen"][C._S_SHIELD_R].reshape(-1, map_width, map_width) / 255
    s_density = obs.observation["screen"][C._S_DENSITY_A].reshape(-1, map_width, map_width) / 255

    map_data = np.concatenate([m_height, m_visible, m_camera, m_relative, m_selected,
                               s_relative, s_selected, s_hitpoint, s_shield, s_density], axis=0)
    return map_data


def get_input(obs):
    high_input = np.zeros([C._SIZE_HIGH_NET_INPUT])
    tech_cost = np.zeros([C._SIZE_TECH_NET_INPUT])
    pop_num = np.zeros([C._SIZE_POP_NET_INPUT])

    # ###################################  high input ##########################################
    high_input[0] = C.difficulty
    # time
    high_input[1] = int(obs.raw_observation.observation.game_loop)
    # minerals
    high_input[2] = obs.raw_observation.observation.player_common.minerals
    # gas
    high_input[3] = obs.raw_observation.observation.player_common.vespene
    # mineral cost
    high_input[4] = obs.raw_observation.observation.score.score_details.spent_minerals
    # gas cost
    high_input[5] = obs.raw_observation.observation.score.score_details.spent_vespene
    # others
    player_common = obs.raw_observation.observation.player_common
    high_input[6] = player_common.food_cap
    high_input[7] = player_common.food_used
    high_input[8] = player_common.food_army
    high_input[9] = player_common.food_workers
    high_input[10] = player_common.army_count
    # num of probe, zealot, stalker, pylon, assimilator, gateway, cyber
    index_list = [C._PROBE_TYPE_INDEX, C._ZEALOT_TYPE_INDEX, C._STALKER_TYPE_INDEX,
                  C._PYLON_TYPE_INDEX, C._ASSIMILATOR_TYPE_INDEX, C._GATEWAY_TYPE_INDEX, C._CYBER_TYPE_INDEX]
    high_input[11:18] = get_unit_num_array(obs, index_list)

    high_input[18] = get_attack_num(obs, [C._ZEALOT_TYPE_INDEX, C._STALKER_TYPE_INDEX])

    # print('high_input:', high_input)

    # ##################################  tech cost ###############################################
    # cost of pylon vespene gateway cyber
    tech_cost[:4] = [100, 75, 150, 150]
    tech_cost[4] = player_common.food_cap - player_common.food_used
    tech_cost[5] = get_tech_action_num(obs, C._A_BUILD_PYLON_S)
    tech_cost[6] = get_tech_action_num(obs, C._A_BUILD_ASSIMILATOR_S)
    tech_cost[7] = get_tech_action_num(obs, C._A_BUILD_GATEWAY_S)
    tech_cost[8] = get_tech_action_num(obs, C._A_BUILD_CYBER_S)

    # #################################  pop num  #################################################
    base = find_unit(obs, C._NEXUS_TYPE_INDEX)
    # number of probe for mineral and the ideal num
    if base:
        pop_num[0] = base.assigned_harvesters
        pop_num[1] = base.ideal_harvesters

    gas_1 = find_gas(obs, 1)
    gas_2 = find_gas(obs, 2)
    have_gas_1, have_gas_2 = 0, 0
    if gas_1:
        pop_num[2] = gas_1.assigned_harvesters
        pop_num[3] = gas_1.ideal_harvesters
        have_gas_1 = 1
    if gas_2:
        pop_num[4] = gas_2.assigned_harvesters
        pop_num[5] = gas_2.ideal_harvesters
        have_gas_2 = 1

    # all the num of workers
    pop_num[6] = player_common.food_army / max(player_common.food_workers, 1)

    pop_num[7] = have_gas_1
    pop_num[8] = have_gas_2

    # num of the training probe, zealot, stalker
    production_list = get_production_num(obs, [C._A_TRAIN_PROBE, C._A_TRAIN_ZEALOT, C._A_TRAIN_STALKER])
    pop_num[9] = production_list[0]
    pop_num[10] = production_list[1]
    pop_num[11] = production_list[2]

    # pop_num[[12, 13, 14]] = [50, 100, 125]

    return high_input, tech_cost, pop_num
