import numpy as np
from pysc2.lib import point
from pysc2.lib import transform


class Pos(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


def world_to_screen_pos(game_info, pos, obs):
    """

    :param game_info: env.game_info
    :param pos: target_world_space_pos
    :param obs: obs.raw_observation.observation.raw_data.player.camera
    :return: screen_pos
    """

    # init parameter and define
    map_size = point.Point.build(game_info.start_raw.map_size)
    fl_opts = game_info.options.feature_layer
    feature_layer_screen_size = point.Point.build(fl_opts.resolution)
    camera_width_world_units = fl_opts.width

    world_to_screen = transform.Linear(point.Point(1, -1), point.Point(0, map_size.y))
    screen_to_fl_screen = transform.Linear(feature_layer_screen_size / camera_width_world_units)
    world_to_fl_screen = transform.Chain(world_to_screen, screen_to_fl_screen, transform.Floor())

    # Update the camera transform based on the new camera center.
    camera_center = obs.raw_observation.observation.raw_data.player.camera
    camera_radius = (feature_layer_screen_size /
                     feature_layer_screen_size.x *
                     camera_width_world_units / 2)
    camera_center = point.Point.build(camera_center)
    center = camera_center.bound(camera_radius, map_size - camera_radius)
    camera = point.Rect(
        (center - camera_radius).bound(map_size),
        (center + camera_radius).bound(map_size))
    world_to_screen.offset = (-camera.bl * world_to_screen.scale)

    trans_pos = world_to_fl_screen.fwd_pt(point.Point.build(pos))
    return np.clip(np.array(trans_pos), 0, 63).tolist()


def world_to_minimap_pos(game_info, pos):

    map_size = point.Point.build(game_info.start_raw.map_size)
    fl_opts = game_info.options.feature_layer
    feature_layer_minimap_size = point.Point.build(fl_opts.minimap_resolution)

    max_map_dim = map_size.max_dim()

    world_to_minimap = transform.Linear(point.Point(1, -1), point.Point(0, map_size.y))
    minimap_to_fl_minimap = transform.Linear(feature_layer_minimap_size / max_map_dim)
    world_to_fl_minimap = transform.Chain(
        world_to_minimap,
        minimap_to_fl_minimap,
        transform.Floor()
    )

    trans_pos = world_to_fl_minimap.fwd_pt(point.Point.build(pos))
    return np.clip(np.array(trans_pos), 0, 63).tolist()


def screen_to_minimap_pos(game_info, screen_pos, obs):

    screen_pos = Pos(screen_pos[0], screen_pos[1])

    # init parameter and define
    map_size = point.Point.build(game_info.start_raw.map_size)
    fl_opts = game_info.options.feature_layer
    feature_layer_screen_size = point.Point.build(fl_opts.resolution)
    feature_layer_minimap_size = point.Point.build(fl_opts.minimap_resolution)

    # screen to world
    camera_width_world_units = fl_opts.width

    world_to_screen = transform.Linear(point.Point(1, -1), point.Point(0, map_size.y))
    screen_to_fl_screen = transform.Linear(feature_layer_screen_size / camera_width_world_units)
    world_to_fl_screen = transform.Chain(world_to_screen, screen_to_fl_screen, transform.Floor())

    # Update the camera transform based on the new camera center.
    camera_center = obs.raw_observation.observation.raw_data.player.camera
    camera_radius = (feature_layer_screen_size /
                     feature_layer_screen_size.x *
                     camera_width_world_units / 2)
    camera_center = point.Point.build(camera_center)
    center = camera_center.bound(camera_radius, map_size - camera_radius)
    camera = point.Rect(
        (center - camera_radius).bound(map_size),
        (center + camera_radius).bound(map_size))
    world_to_screen.offset = (-camera.bl * world_to_screen.scale)

    world_pos = world_to_fl_screen.back_pt(point.Point.build(screen_pos))

    # world to minimap
    max_map_dim = map_size.max_dim()

    world_to_minimap = transform.Linear(point.Point(1, -1), point.Point(0, map_size.y))
    minimap_to_fl_minimap = transform.Linear(feature_layer_minimap_size / max_map_dim)
    world_to_fl_minimap = transform.Chain(
        world_to_minimap,
        minimap_to_fl_minimap,
        transform.Floor()
    )
    minimap_pos = world_to_fl_minimap.fwd_pt(point.Point.build(world_pos))
    return np.clip(np.array(minimap_pos), 0, 63).tolist()
