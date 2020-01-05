import numpy as np
import tensorflow as tf

import param as P

from algo.ppo import Policy_net, PPOTrain

# for mini game
_SIZE_MINI_INPUT = 20
_SIZE_MINI_ACTIONS = 10


class MiniNetwork(object):

    def __init__(self, sess=None, summary_writer=tf.summary.FileWriter("logs/"), rl_training=False,
                 reuse=False, cluster=None, index=0, device='/gpu:0',
                 ppo_load_path=None, ppo_save_path=None):
        self.policy_model_path_load = ppo_load_path + "mini"
        self.policy_model_path_save = ppo_save_path + "mini"

        self.rl_training = rl_training

        self.use_norm = True

        self.reuse = reuse
        self.sess = sess
        self.cluster = cluster
        self.index = index
        self.device = device

        self._create_graph()

        self.rl_saver = tf.train.Saver()
        self.summary_writer = summary_writer

    def initialize(self):
        init_op = tf.global_variables_initializer()
        self.sess.run(init_op)

    def reset_old_network(self):
        self.policy_ppo.assign_policy_parameters()
        self.policy_ppo.reset_mean_returns()

        self.sess.run(self.results_sum.assign(0))
        self.sess.run(self.game_num.assign(0))

    def _create_graph(self):
        if self.reuse:
            tf.get_variable_scope().reuse_variables()
            assert tf.get_variable_scope().reuse

        worker_device = "/job:worker/task:%d" % self.index + self.device
        with tf.device(tf.train.replica_device_setter(worker_device=worker_device, cluster=self.cluster)):
            self.results_sum = tf.get_variable(name="results_sum", shape=[], initializer=tf.zeros_initializer)
            self.game_num = tf.get_variable(name="game_num", shape=[], initializer=tf.zeros_initializer)

            self.global_steps = tf.get_variable(name="global_steps", shape=[], initializer=tf.zeros_initializer)
            self.win_rate = self.results_sum / self.game_num

            self.mean_win_rate = tf.summary.scalar('mean_win_rate_dis', self.results_sum / self.game_num)
            self.merged = tf.summary.merge([self.mean_win_rate])

            mini_scope = "MiniPolicyNN"
            with tf.variable_scope(mini_scope):
                ob_space = _SIZE_MINI_INPUT
                act_space_array = _SIZE_MINI_ACTIONS
                self.policy = Policy_net('policy', self.sess, ob_space, act_space_array)
                self.policy_old = Policy_net('old_policy', self.sess, ob_space, act_space_array)
                self.policy_ppo = PPOTrain('PPO', self.sess, self.policy, self.policy_old, lr=P.mini_lr, epoch_num=P.mini_epoch_num)
            var_list = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)
            self.policy_saver = tf.train.Saver(var_list=var_list)

    def Update_result(self, result_list):
        win = 0
        for i in result_list:
            if i > 0:
                win += 1
        self.sess.run(self.results_sum.assign_add(win))
        self.sess.run(self.game_num.assign_add(len(result_list)))

    def Update_summary(self, counter):
        print("Update summary........")

        policy_summary = self.policy_ppo.get_summary_dis()
        self.summary_writer.add_summary(policy_summary, counter)

        summary = self.sess.run(self.merged)
        self.summary_writer.add_summary(summary, counter)
        self.sess.run(self.global_steps.assign(counter))

        print("Update summary finished!")

        steps = int(self.sess.run(self.global_steps))
        win_game = int(self.sess.run(self.results_sum))
        all_game = int(self.sess.run(self.game_num))
        win_rate = win_game / float(all_game)

        return steps, win_rate

    def get_win_rate(self):
        return float(self.sess.run(self.win_rate))

    def Update_policy(self, buffer):
        self.policy_ppo.ppo_train_dis(buffer.observations, buffer.tech_actions,
                                      buffer.rewards, buffer.values, buffer.values_next, buffer.gaes, buffer.returns, verbose=False)

    def get_global_steps(self):
        return int(self.sess.run(self.global_steps))

    def save_policy(self):
        self.policy_saver.save(self.sess, self.policy_model_path_save)
        print("policy has been saved in", self.policy_model_path_save)

    def restore_policy(self):
        self.policy_saver.restore(self.sess, self.policy_model_path_load)
        print("Restore policy from", self.policy_model_path_load)
