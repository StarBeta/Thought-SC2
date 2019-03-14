from pysc2.lib import actions as sc2_actions
from pysc2.lib import features

_LOAD_MODEL_PATH = "./model/"
_SAVE_MODEL_PATH = "./model/"

_LOAD_DYNAMIC_PATH = ""
_SAVE_DYNAMIC_PATH = ""

# define the num of input and output
# for source game
_SIZE_HIGH_NET_INPUT = 19
_SIZE_BATTLE_NET_OUT = 2

_SIZE_TECH_NET_INPUT = 9
_SIZE_TECH_NET_OUT = 4

_SIZE_POP_NET_INPUT = 12
_SIZE_POP_NET_OUT = 3

_SIZE_SOURCE_INPUT = _SIZE_HIGH_NET_INPUT + _SIZE_TECH_NET_INPUT + _SIZE_POP_NET_INPUT
_SIZE_SOURCE_ACTIONS = _SIZE_TECH_NET_OUT + _SIZE_POP_NET_OUT + _SIZE_BATTLE_NET_OUT + 1

# for prototype game
_SIZE_SIMPLE_INPUT = 10
_SIZE_SIMPLE_OUT = 2
_SIZE_MAX_ACTIONS = 3

# for mini game
_SIZE_MINI_INPUT = 20
_SIZE_MINI_ACTIONS = 10

# timesteps per second
_FPS = 22.4

# Minimap index
_M_SELECTED = features.MINIMAP_FEATURES.selected.index

# Screen index
_S_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index
_M_VISIABLE_TYPE = features.MINIMAP_FEATURES.visibility_map.index
_M_RELATIVE_TYPE = features.MINIMAP_FEATURES.player_relative.index
_M_PLAYID_TYPE = features.MINIMAP_FEATURES.player_id.index
_M_MINIMAP_CHANNELS = 3

# Unit type index
# Protoss
_MINERAL_TYPE_INDEX = 483
_GAS_TYPE_INDEX = 342

_PROBE_TYPE_INDEX = 84
_ZEALOT_TYPE_INDEX = 73
_STALKER_TYPE_INDEX = 74

_NEXUS_TYPE_INDEX = 59
_PYLON_TYPE_INDEX = 60
_ASSIMILATOR_TYPE_INDEX = 61
_FORGE_TYPE_INDEX = 63
_CANNON_TYPE_INDEX = 66
_GATEWAY_TYPE_INDEX = 62
_CYBER_TYPE_INDEX = 72

# Terran
_MARINE_TYPE_INDEX = 48
_MARAUDER_TYPE_INDEX = 51
_REAPER_TYPE_INDEX = 49
_SIEGETANK_TYPE_INDEX = 33

#_M_RELATIVE_TYPE
_RELATIVE_NONE = 0
_RELATIVE_SELF = 1
_RELATIVE_ALLY = 2
_RELATIVE_NEUTRAL = 3
_RELATIVE_ENEMY = 4

# Action type index
_NO_OP = sc2_actions.FUNCTIONS.no_op.id
_SMART_SCREEN = sc2_actions.FUNCTIONS.Smart_screen.id
_SELECT_ARMY = sc2_actions.FUNCTIONS.select_army.id
_SELECT_WORKER = sc2_actions.FUNCTIONS.select_idle_worker.id
_SELECT_BY_ID = sc2_actions.FUNCTIONS.select_unit.id
_CONTROL_GROUP = sc2_actions.FUNCTIONS.select_control_group.id
_ATTACH_M = sc2_actions.FUNCTIONS.Attack_minimap.id
_MOVE_M = sc2_actions.FUNCTIONS.Move_minimap.id

_SELECT_UNIT = sc2_actions.FUNCTIONS.select_unit.id
_SELECT_POINT = sc2_actions.FUNCTIONS.select_point.id
_MOVE_CAMERA = sc2_actions.FUNCTIONS.move_camera.id

_TRAIN_PROBE = sc2_actions.FUNCTIONS.Train_Probe_quick.id
_TRAIN_ZEALOT = sc2_actions.FUNCTIONS.Train_Zealot_quick.id
_TRAIN_STALKER = sc2_actions.FUNCTIONS.Train_Stalker_quick.id

_TRAIN_PROBE_LABEL = 0
_MOVE_PROBE_GAS_1_LABEL = 1
_MOVE_PROBE_GAS_2_LABEL = 2
_TRAIN_ZEALOT_LABEL = 3
_TRAIN_STALKER_LABEL = 4

_BUILD_PYLON_LABEL = 0
_BUILD_ASSIMILATOR_LABEL = 1
_BUILD_GATEWAY_LABEL = 2
_BUILD_CYBER_LABEL = 3

_BUILD_PYLON_S = sc2_actions.FUNCTIONS.Build_Pylon_screen.id
_BUILD_ASSIMILATOR_S = sc2_actions.FUNCTIONS.Build_Assimilator_screen.id
_BUILD_FORGE_S = sc2_actions.FUNCTIONS.Build_Forge_screen.id
_BUILD_GATEWAY_S = sc2_actions.FUNCTIONS.Build_Gateway_screen.id
_BUILD_CYBER_S = sc2_actions.FUNCTIONS.Build_CyberneticsCore_screen.id

_MOVE_S = sc2_actions.FUNCTIONS.Move_screen.id
_HARVEST_S = sc2_actions.FUNCTIONS.Harvest_Gather_screen.id

_A_SMART_SCREEN = sc2_actions.FUNCTIONS.Smart_screen.ability_id
_A_TRAIN_PROBE = sc2_actions.FUNCTIONS.Train_Probe_quick.ability_id
_A_TRAIN_ZEALOT = sc2_actions.FUNCTIONS.Train_Zealot_quick.ability_id
_A_TRAIN_STALKER = sc2_actions.FUNCTIONS.Train_Stalker_quick.ability_id

_A_BUILD_PYLON_S = sc2_actions.FUNCTIONS.Build_Pylon_screen.ability_id
_A_BUILD_ASSIMILATOR_S = sc2_actions.FUNCTIONS.Build_Assimilator_screen.ability_id
_A_BUILD_FORGE_S = sc2_actions.FUNCTIONS.Build_Forge_screen.ability_id
_A_BUILD_GATEWAY_S = sc2_actions.FUNCTIONS.Build_Gateway_screen.ability_id
_A_BUILD_CYBER_S = sc2_actions.FUNCTIONS.Build_CyberneticsCore_screen.ability_id

_A_ATTACK_ATTACK_MINIMAP_S = sc2_actions.FUNCTIONS.Attack_Attack_minimap.ability_id
_A_ATTACK_MINIMAP_S = sc2_actions.FUNCTIONS.Attack_minimap.ability_id
_A_ATTACK_ATTACK_SCREEN_S = sc2_actions.FUNCTIONS.Attack_Attack_screen.ability_id
_A_ATTACK_SCREEN_S = sc2_actions.FUNCTIONS.Attack_screen.ability_id


_NOT_QUEUED = [0]
_QUEUED = [1]

_CLICK = [0]
_SHIFT_CLICK = [1]
_DBL_CLICK = [2]

_RECALL_GROUP = [0]
_SET_GROUP = [1]
_APPEND_GROUP = [2]

_GATEWAY_GROUP_ID = [9]
_BASE_GROUP_ID = [0]
_ARMY_GROUP_ID = [3]

_ARMY_INDEX = -1
_GATEWAY_GROUP_INDEX = -9


'''
In order to attack the enemy, we need to know the location of the enemy, 
and sometimes we need to know the location of the enemy sub-base. 
These locations are different for different maps and can be obtained by some algorithms.
For the sake of simplicity, we provide the theses points of positions for different maps. 
These points are approximate values and can be got by some automating algorithms 
such as calculations of positions of minerals..
'''


class AbyssalReef:
    my_sub_pos = [41, 20]   # not used
    enemy_sub_pos = [42, 47]
    enemy_main_pos = [53, 50]
    base_camera_pos = [12, 17]


class Simple64:
    my_sub_pos = [41, 20]   # not used
    enemy_sub_pos = [13, 50]
    enemy_main_pos = [45, 47]
    base_camera_pos = [19, 24]


class Flat64:
    my_sub_pos = [41, 20]   # not used
    enemy_sub_pos = [12, 35]
    enemy_main_pos = [13, 50]
    base_camera_pos = [42, 24]


class Simple96:
    my_sub_pos = [41, 20]   # not used
    enemy_sub_pos = [32, 14]
    enemy_main_pos = [11, 14]
    base_camera_pos = [46, 53]


class Flat32:
    my_sub_pos = [41, 20]   # not used
    enemy_sub_pos = [43, 10]
    enemy_main_pos = [45, 47]
    base_camera_pos = [24, 26]


def get_map_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m

# fixed point pos
my_sub_pos = []
enemy_sub_pos = []
enemy_main_pos = []
base_camera_pos = []

# game difficulty
difficulty = 7


def time_wait(sec):
    return int(sec * _FPS)
