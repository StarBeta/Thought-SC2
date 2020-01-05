import lib.config as C
import lib.utils as U
import lib.transform_pos as T
import numpy as np

"""For the sake of simplicity, we give the macro-action directly and not provide the way on how to get them. 
Also for simplicity, the information required for macro operations is extracted directly from the original interface."""


def check_params(agent, action, unit_type, args, action_type):
    valid = False
    if action_type == 0:  # select
        if action in agent.obs.observation["available_actions"]:
            valid = True
            # if params have none, not right
            for arg in args:
                if arg is None:
                    valid = False
    elif action_type == 1:  # action
        if action == C._NO_OP or action == C._MOVE_CAMERA:
            valid = True
        # type and action is correct, right
        elif agent.on_select == unit_type and action in agent.obs.observation["available_actions"]:
            valid = True
            # if params have none, not right
            for arg in args:
                if arg is None:
                    valid = False
    return valid


def control_step(agent):
    agent.select(C._SELECT_POINT, C._GATEWAY_GROUP_INDEX, [C._DBL_CLICK, selectGateway(agent)])
    agent.safe_action(C._CONTROL_GROUP, C._GATEWAY_GROUP_INDEX, [C._SET_GROUP, C._GATEWAY_GROUP_ID])


def attack_step(agent, pos_index=None):
    # select army and attack, first main-mineral then sub-mineral
    agent.select(C._SELECT_ARMY, C._ARMY_INDEX, [[0]])
    agent.safe_action(C._CONTROL_GROUP, C._ARMY_INDEX, [C._SET_GROUP, C._ARMY_GROUP_ID])

    if pos_index is None or pos_index == 0:
        agent.safe_action(C._ATTACH_M, C._ARMY_INDEX, [C._QUEUED, C.enemy_sub_pos])
        agent.safe_action(C._ATTACH_M, C._ARMY_INDEX, [C._QUEUED, C.enemy_main_pos])


def retreat_step(agent):
    # select army and assemble to our sub-mineral location
    agent.select(C._SELECT_ARMY, C._ARMY_INDEX, [[0]])
    agent.safe_action(C._CONTROL_GROUP, C._ARMY_INDEX, [C._SET_GROUP, C._ARMY_GROUP_ID])
    agent.safe_action(C._MOVE_M, C._ARMY_INDEX, [C._QUEUED, C.my_sub_pos])


def move_worker(agent, gas_pos, pos=None):
    # get a probe to gas
    agent.select(C._SELECT_POINT, C._PROBE_TYPE_INDEX, [C._CLICK, pos if pos else selectProbe(agent)])
    # first back to base, then go to change the target
    agent.safe_action(C._HARVEST_S, C._PROBE_TYPE_INDEX, [C._NOT_QUEUED, gas_pos])


def mineral_worker(agent):
    camera_on_base = U.check_base_camera(agent.env.game_info, agent.obs)

    if not camera_on_base:
        return

    gas_pos = U.judge_gas_worker(agent.obs, agent.env.game_info)
    if gas_pos:
        probe = U.get_mineral_probe(agent.obs)
        probe_pos = T.world_to_screen_pos(agent.env.game_info, probe.pos, agent.obs) if probe else None
        move_worker(agent, gas_pos, probe_pos)

    if U.judge_gas_worker_too_many(agent.obs):
        probe = U.get_gas_probe(agent.obs)
        probe_pos = T.world_to_screen_pos(agent.env.game_info, probe.pos, agent.obs) if probe else None
        mineral = U.find_unit_on_screen(agent.obs, C._MINERAL_TYPE_INDEX)
        mineral_pos = T.world_to_screen_pos(agent.env.game_info, mineral.pos, agent.obs) if mineral else None
        move_worker(agent, mineral_pos, probe_pos)
    else:
        # train_worker(agent, C.base_pos, C._TRAIN_PROBE)
        base = U.find_unit_on_screen(agent.obs, C._NEXUS_TYPE_INDEX)
        base_pos = T.world_to_screen_pos(agent.env.game_info, base.pos, agent.obs) if base else None
        train_worker(agent, base_pos, C._TRAIN_PROBE)


def train_worker(agent, building_pos, train_action, click=C._CLICK):
    # select a building and train
    agent.select(C._SELECT_POINT, C._NEXUS_TYPE_INDEX, [click, building_pos])
    agent.safe_action(train_action, C._NEXUS_TYPE_INDEX, [C._NOT_QUEUED])


def build_by_idle_worker(agent, build_action, build_pos):
    if C._SELECT_WORKER in agent.obs.observation["available_actions"]:
        agent.select(C._SELECT_WORKER, C._PROBE_TYPE_INDEX, [[0]])
    else:
        agent.select(C._SELECT_POINT, C._PROBE_TYPE_INDEX, [C._CLICK, selectProbe(agent)])
    agent.safe_action(build_action, C._PROBE_TYPE_INDEX, [C._NOT_QUEUED, build_pos])

    # some times the probe dont get back to work,
    agent.safe_action(C._SMART_SCREEN, C._PROBE_TYPE_INDEX, [C._QUEUED, U.get_back_pos(agent.obs, agent.env.game_info)])


def train_army(agent, train_action):
    count = U.get_unit_num(agent.obs, C._GATEWAY_TYPE_INDEX)
    pos = selectGateway(agent)
    camera_on_base = U.check_base_camera(agent.env.game_info, agent.obs)
    if pos and camera_on_base:
        agent.select(C._SELECT_POINT, C._GATEWAY_GROUP_INDEX, [C._DBL_CLICK, pos])
        agent.safe_action(C._CONTROL_GROUP, C._GATEWAY_GROUP_INDEX, [C._SET_GROUP, C._GATEWAY_GROUP_ID])

        agent.select(C._SELECT_POINT, C._GATEWAY_GROUP_INDEX, [C._CLICK, pos])
    else:
        agent.select(C._CONTROL_GROUP, C._GATEWAY_GROUP_INDEX, [C._RECALL_GROUP, C._GATEWAY_GROUP_ID])

    use_multi = False
    if use_multi:
        for _ in range(count):
            agent.safe_action(train_action, C._GATEWAY_GROUP_INDEX, [C._NOT_QUEUED])
    else:
        agent.safe_action(train_action, C._GATEWAY_GROUP_INDEX, [C._NOT_QUEUED])


def set_source(agent):
    agent.safe_action(C._NO_OP, 0, [])
    base = U.find_unit_on_screen(agent.obs, C._NEXUS_TYPE_INDEX)
    base_pos = T.world_to_screen_pos(agent.env.game_info, base.pos, agent.obs)

    agent.select(C._SELECT_POINT, C._NEXUS_TYPE_INDEX, [C._CLICK, base_pos])
    agent.safe_action(C._CONTROL_GROUP, C._NEXUS_TYPE_INDEX, [C._SET_GROUP, C._BASE_GROUP_ID])


def reset_select(agent):
    agent.select(C._CONTROL_GROUP, C._NEXUS_TYPE_INDEX, [C._RECALL_GROUP, C._BASE_GROUP_ID])


def selectProbe(agent):
    # random select a probe
    unit_type_map = agent.obs.observation["screen"][U._UNIT_TYPE]
    pos_y, pos_x = (unit_type_map == U._PROBE_TYPE_INDEX).nonzero()

    num = len(pos_y)
    if num > 0:
        rand = np.random.choice(num, size=1)
        pos = [pos_x[rand], pos_y[rand]]
        return pos
    return None


def selectGateway(agent):
    # random select a Gateway
    gateway = U.get_best_gateway(agent.obs)
    pos = T.world_to_screen_pos(agent.env.game_info, gateway.pos, agent.obs) if gateway else None
    return pos
