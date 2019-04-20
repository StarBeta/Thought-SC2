from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

USED_DEVICES = "-1"
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = USED_DEVICES

import sys
import threading
import time

import tensorflow as tf
from absl import app
from absl import flags
from pysc2 import maps
from pysc2.lib import stopwatch

import lib.config as C
import mini_source_agent

from lib import my_sc2_env as sc2_env
from lib.replay_buffer import Buffer

from mini_network import MiniNetwork

from datetime import datetime
import multiprocessing as mp
import numpy as np

FLAGS = flags.FLAGS
flags.DEFINE_bool("training", True, "Whether to train agents.")
flags.DEFINE_bool("on_server", True, "Whether is running on server.")
flags.DEFINE_integer("num_for_update", 100, "Number of episodes for each train.")
flags.DEFINE_string("log_path", "./logs/", "Path for log.")
flags.DEFINE_string("device", USED_DEVICES, "Device for training.")

# Simple64

flags.DEFINE_string("map", "Simple64", "Name of a map to use.")
flags.DEFINE_bool("render", False, "Whether to render with pygame.")
flags.DEFINE_integer("screen_resolution", 64, "Resolution for screen feature layers.")
flags.DEFINE_integer("minimap_resolution", 64, "Resolution for minimap feature layers.")

flags.DEFINE_enum("agent_race", "P", sc2_env.races.keys(), "Agent's race.")
flags.DEFINE_enum("bot_race", "T", sc2_env.races.keys(), "Bot's race.")
flags.DEFINE_integer("max_agent_steps", 18000, "Total agent steps.")
flags.DEFINE_integer("step_mul", 8, "Game steps per agent step.")

flags.DEFINE_bool("profile", False, "Whether to turn on code profiling.")
flags.DEFINE_bool("trace", False, "Whether to trace the code execution.")
flags.DEFINE_bool("save_replay", False, "Whether to replays_save a replay at the end.")
flags.DEFINE_string("replay_dir", "multi-agent/", "dir of replay to replays_save.")

flags.DEFINE_string("restore_model_path", "./model/20190122-215114_source/", "path for restore model")
flags.DEFINE_bool("restore_model", True, "Whether to restore old model")

flags.DEFINE_integer("parallel", 10, "How many processes to run in parallel.")
flags.DEFINE_integer("thread_num", 1, "How many thread to run in the process.")
flags.DEFINE_integer("port_num", 24370, "the start port to create distribute tf")
flags.DEFINE_integer("max_iters", 1, "the rl agent max run iters")
flags.DEFINE_integer("game_num", 100, "How many games to evaluate.")

flags.DEFINE_string("game_version", None, "game version of SC2")

FLAGS(sys.argv)


# set the play map
play_map = C.get_map_class('lib.config.' + FLAGS.map)

C.my_sub_pos = play_map.my_sub_pos
C.enemy_sub_pos = play_map.enemy_sub_pos
C.enemy_main_pos = play_map.enemy_main_pos
C.base_camera_pos = play_map.base_camera_pos

DIFF = 1

if not FLAGS.on_server:
    PARALLEL = 1
    THREAD_NUM = 1
    MAX_AGENT_STEPS = 18000
    DEVICE = ['/gpu:0']
    NUM_FOR_UPDATE = 2
    TRAIN_ITERS = 5
    PORT_NUM = FLAGS.port_num
else:
    PARALLEL = FLAGS.parallel
    THREAD_NUM = FLAGS.thread_num
    MAX_AGENT_STEPS = FLAGS.max_agent_steps
    # DEVICE = ['/gpu:' + dev for dev in FLAGS.device.split(',')]
    DEVICE = ['/cpu:0']
    NUM_FOR_UPDATE = FLAGS.num_for_update
    TRAIN_ITERS = FLAGS.max_iters
    PORT_NUM = FLAGS.port_num


LOG = FLAGS.log_path
if not os.path.exists(LOG):
    os.makedirs(LOG)

SERVER_DICT = {"worker": [], "ps": []}

FLAGS(sys.argv)
THREAD_NUM = PARALLEL

# define some global variable
LOCK = threading.Lock()
UPDATE_EVENT, ROLLING_EVENT = threading.Event(), threading.Event()
COUNTER = 0
WAITING_COUNTER = 0

#[1, 2, 3, 4, 5, 6, 7]
Difficulty_list = [7]
Reward_list = [1, 0, -1]
RESULT_ARRAY = np.zeros((len(Difficulty_list), len(Reward_list)))

GAME_NUM = FLAGS.game_num
PER_GAME_NUM = GAME_NUM // PARALLEL


def run_thread(agent, Synchronizer):
    global COUNTER, WAITING_COUNTER, GAME_NUM, PER_GAME_NUM
    C._FPS = 2.8
    step_mul = FLAGS.step_mul
    for difficulty in Difficulty_list:
        with sc2_env.SC2Env(
                map_name=FLAGS.map,
                agent_race=FLAGS.agent_race,
                bot_race=FLAGS.bot_race,
                difficulty=difficulty,
                step_mul=step_mul,
                score_index=-1,
                screen_size_px=(FLAGS.screen_resolution, FLAGS.screen_resolution),
                minimap_size_px=(FLAGS.minimap_resolution, FLAGS.minimap_resolution),
                visualize=False, game_steps_per_episode=900 * 22.4,
                game_version=FLAGS.game_version) as env:

            # Only for a single player!
            agent.set_env(env)
            if difficulty == "A":
                C.difficulty = 10
            else:
                C.difficulty = difficulty

            for j in range(PER_GAME_NUM):
                agent.play()
                reward = agent.result['reward']

                with LOCK:
                    RESULT_ARRAY[Difficulty_list.index(difficulty), Reward_list.index(reward)] += 1
                    COUNTER += 1
                    print("difficulty %s:  finished %d games!" % (difficulty, COUNTER))

                agent.reset()
                time.sleep(2)

            if ROLLING_EVENT.is_set():
                ROLLING_EVENT.clear()

            WAITING_COUNTER += 1
            if WAITING_COUNTER == PARALLEL:
                UPDATE_EVENT.set()

            if agent.index == 0:
                UPDATE_EVENT.wait()

                win = RESULT_ARRAY[Difficulty_list.index(difficulty), Reward_list.index(1)]
                fair = RESULT_ARRAY[Difficulty_list.index(difficulty), Reward_list.index(0)]
                lose = RESULT_ARRAY[Difficulty_list.index(difficulty), Reward_list.index(-1)]

                log_path = "./result/" + FLAGS.agent_race + 'v' + FLAGS.bot_race + '_' + \
                           FLAGS.restore_model_path.split('/')[-2] + '_' + FLAGS.map + '.txt'

                log_file = open(log_path, "a")
                log_file.write('difficulty: %s, game_num: %d\n' % (difficulty, GAME_NUM))
                log_file.write('win: %d, %.2f\n' % (int(win), win / GAME_NUM))
                log_file.write('fair: %d, %.2f\n' % (int(fair), fair / GAME_NUM))
                log_file.write('loss: %d, %.2f\n\n' % (int(lose), lose / GAME_NUM))
                log_file.close()

                UPDATE_EVENT.clear()
                ROLLING_EVENT.set()
                WAITING_COUNTER = 0
                COUNTER = 0

            ROLLING_EVENT.wait()

    if agent.index == 0:
        Synchronizer.wait()


def Worker(index, update_game_num, Synchronizer, cluster, model_path):
    config = tf.ConfigProto(
        allow_soft_placement=True, log_device_placement=False,
    )
    config.gpu_options.allow_growth = True
    worker = tf.train.Server(cluster, job_name="worker", task_index=index, config=config)
    sess = tf.Session(target=worker.target, config=config)
    Net = MiniNetwork(sess=sess, summary_writer=None, rl_training=FLAGS.training,
                      cluster=cluster, index=index, device=DEVICE[index % len(DEVICE)],
                      ppo_load_path=FLAGS.restore_model_path, ppo_save_path=model_path)

    global_buffer = Buffer()
    agents = []
    for i in range(THREAD_NUM):
        agent = mini_source_agent.MiniSourceAgent(index=i, global_buffer=global_buffer, net=Net,
                                                  restore_model=FLAGS.restore_model, rl_training=FLAGS.training, greedy_action=True)
        agents.append(agent)

    print("Worker %d: waiting for cluster connection..." % index)
    sess.run(tf.report_uninitialized_variables())
    print("Worker %d: cluster ready!" % index)

    while len(sess.run(tf.report_uninitialized_variables())):
        print("Worker %d: waiting for variable initialization..." % index)
        time.sleep(1)
    print("Worker %d: variables initialized" % index)

    UPDATE_EVENT.clear()
    ROLLING_EVENT.set()

    # Run threads
    threads = []
    for i in range(THREAD_NUM - 1):
        t = threading.Thread(target=run_thread, args=(agents[i], Synchronizer))
        threads.append(t)
        t.daemon = True
        t.start()
        time.sleep(3)

    run_thread(agents[-1], Synchronizer)

    for t in threads:
        t.join()


def Parameter_Server(Synchronizer, cluster, log_path, model_path):
    config = tf.ConfigProto(
        allow_soft_placement=True, log_device_placement=False,
    )
    config.gpu_options.allow_growth = True
    server = tf.train.Server(cluster, job_name="ps", task_index=0, config=config)
    sess = tf.Session(target=server.target, config=config)
    summary_writer = tf.summary.FileWriter(log_path)
    Net = MiniNetwork(sess=sess, summary_writer=summary_writer, rl_training=FLAGS.training,
                      cluster=cluster, index=0, device=DEVICE[0 % len(DEVICE)],
                      ppo_load_path=FLAGS.restore_model_path, ppo_save_path=model_path)

    agent = mini_source_agent.MiniSourceAgent(index=-1, net=Net, restore_model=FLAGS.restore_model,
                                              rl_training=FLAGS.training, greedy_action=True)

    print("Parameter server: waiting for cluster connection...")
    sess.run(tf.report_uninitialized_variables())
    print("Parameter server: cluster ready!")

    print("Parameter server: initializing variables...")
    agent.init_network()
    print("Parameter server: variables initialized")

    Synchronizer.wait()
    print("done!")


def _main(unused_argv):
    """Run agents"""
    maps.get(FLAGS.map)  # Assert the map exists.

    # create distribute tf cluster
    start_port = FLAGS.port_num
    SERVER_DICT["ps"].append("localhost:%d" % start_port)
    for i in range(1):
        SERVER_DICT["worker"].append("localhost:%d" % (start_port + 1 + i))

    Cluster = tf.train.ClusterSpec(SERVER_DICT)

    now = datetime.now()
    model_path = "./model/" + now.strftime("%Y%m%d-%H%M%S") + "_source/"
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    log_path = "./logs/" + now.strftime("%Y%m%d-%H%M%S") + "_source/"

    if FLAGS.restore_model:
        C._LOAD_MODEL_PATH = FLAGS.restore_model_path

    Synchronizer = mp.Barrier(1 + 1)
    # Run parallel process
    procs = []
    for index in range(1):
        p = mp.Process(name="Worker_%d" % index, target=Worker, args=(index, 0, Synchronizer, Cluster, model_path))
        procs.append(p)
        p.daemon = True
        p.start()
        time.sleep(1)

    Parameter_Server(Synchronizer, Cluster, log_path, model_path)

    for p in procs:
        p.join()

    if FLAGS.profile:
        print(stopwatch.sw)


if __name__ == "__main__":
    app.run(_main)
