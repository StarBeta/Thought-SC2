import tensorflow as tf
import numpy as np
import copy
import lib.layer as layer
import param as P


# This part of the code was borrowed mainly from the PPO part of
# https://github.com/uidilr/gail_ppo_tf and was partially modified.

class Policy_net:

    def __init__(self, name: str, sess, ob_space, act_space_array, activation=tf.nn.relu):
        """
        :param name: string
        """
        self.sess = sess
        with tf.variable_scope(name):
            self.obs = tf.placeholder(dtype=tf.float32, shape=[None, ob_space], name='obs')

            with tf.variable_scope('policy_net'):
                with tf.variable_scope('controller'):
                    layer_1 = layer.dense_layer(self.obs, 64, "DenseLayer1", func=activation)
                    layer_2 = layer.dense_layer(layer_1, 64, "DenseLayer2", func=activation)

                    # act_space_array = wait, build worker, build pylon,
                    self.tech_probs = layer.dense_layer(layer_2, act_space_array, "tech_output", func=tf.nn.softmax)
                    self.tech_act = tf.multinomial(tf.log(self.tech_probs), num_samples=1)
                    self.tech_act = tf.reshape(self.tech_act, shape=[-1])

            with tf.variable_scope('value_net'):
                layer_1 = layer.dense_layer(self.obs, 64, "DenseLayer1", func=activation)
                layer_2 = layer.dense_layer(layer_1, 64, "DenseLayer2", func=activation)
                self.v_preds = layer.dense_layer(layer_2, 1, "DenseLayer4", func=None)

            # self.act_stochastic = tf.multinomial(tf.log(self.act_probs), num_samples=1)
            # self.act_stochastic = tf.reshape(self.act_stochastic, shape=[-1])
            # self.act_deterministic = tf.argmax(self.act_probs, axis=1)

            self.scope = tf.get_variable_scope().name

    def get_action(self, obs, verbose=True):
        tech_act_probs, tech_act, v_preds \
            = self.sess.run([self.tech_probs, self.tech_act, self.v_preds], feed_dict={self.obs: obs.reshape([1, -1])})

        if verbose:
            print("Tech:", 'act_probs:', tech_act_probs, 'act:', tech_act)
            print("Value:", v_preds)
        return tech_act[0], v_preds[0]

    def get_action_probs(self, obs, verbose=True):
        tech_act_probs, tech_act, v_preds \
            = self.sess.run([self.tech_probs, self.tech_act, self.v_preds], feed_dict={self.obs: obs.reshape([1, -1])})

        if verbose:
            print("obs:", obs)
            print("Tech:", 'act_probs:', tech_act_probs, 'act:', tech_act)
            print("Value:", v_preds)
        return tech_act_probs[0], v_preds[0]

    def get_values(self, obs):
        v_preds = self.sess.run(self.v_preds, feed_dict={self.obs: obs.reshape([1, -1])})
        v_preds = np.asscalar(v_preds)
        return v_preds

    def get_variables(self):
        return tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, self.scope)

    def get_trainable_variables(self):
        return tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, self.scope)


class PPOTrain:

    def __init__(self, name, sess, Policy, Old_Policy, gamma=0.995, clip_value=0.2, c_1=0.01, c_2=1e-6, lr=1e-4, epoch_num=20):
        """
        :param Policy:
        :param Old_Policy:
        :param gamma:
        :param clip_value:
        :param c_1: parameter for value difference
        :param c_2: parameter for entropy bonus
        :param epoch_num: num for update
        """
        self.Policy = Policy
        self.Old_Policy = Old_Policy
        self.sess = sess

        # comman param for all ppo
        self.gamma = P.gamma
        self.lamda = P.lamda
        self.batch_size = P.batch_size
        self.clip_value = P.clip_value
        self.c_1 = P.c_1
        self.c_2 = P.c_2

        # for different network
        self.adam_lr = lr
        self.epoch_num = epoch_num

        self.adam_epsilon = 1e-5
        self.update_count = 0
        self.restore_model = P.restore_model

        with tf.variable_scope(name):
            pi_trainable = self.Policy.get_trainable_variables()
            old_pi_trainable = self.Old_Policy.get_trainable_variables()

            # assign_operations for policy parameter values to old policy parameters
            with tf.variable_scope('assign_op'):
                self.assign_ops = []
                for v_old, v in zip(old_pi_trainable, pi_trainable):
                    self.assign_ops.append(tf.assign(v_old, v))

            # inputs for train_op
            with tf.variable_scope('train_inp'):
                self.tech_actions = tf.placeholder(dtype=tf.int32, shape=[None], name='tech_actions')
                self.rewards = tf.placeholder(dtype=tf.float32, shape=[None], name='rewards')
                self.v_preds_next = tf.placeholder(dtype=tf.float32, shape=[None], name='v_preds_next')
                self.gaes = tf.placeholder(dtype=tf.float32, shape=[None], name='gaes')
                self.returns = tf.placeholder(dtype=tf.float32, shape=[None], name='returns')

                # define distribute variable
                self.returns_sum = tf.get_variable(name="returns_sum", shape=[], initializer=tf.zeros_initializer)
                self.proc_num = tf.get_variable(name="proc_num", shape=[], initializer=tf.zeros_initializer)

            tech_act_probs = self.Policy.tech_probs
            tech_act_probs_old = self.Old_Policy.tech_probs

            # probabilities of actions which agent took with policy
            tech_act_probs = tech_act_probs * tf.one_hot(indices=self.tech_actions, depth=tech_act_probs.shape[1])
            tech_act_probs = tf.reduce_sum(tech_act_probs, axis=1)

            act_probs = tech_act_probs

            # probabilities of actions which agent took with old policy
            tech_act_probs_old = tech_act_probs_old * tf.one_hot(indices=self.tech_actions, depth=tech_act_probs_old.shape[1])
            tech_act_probs_old = tf.reduce_sum(tech_act_probs_old, axis=1)

            act_probs_old = tech_act_probs_old

            with tf.variable_scope('loss'):
                # construct computation graph for loss_clip
                # ratios = tf.divide(act_probs, act_probs_old)
                ratios = tf.exp(tf.log(tf.clip_by_value(act_probs, 1e-10, 1.0))
                                - tf.log(tf.clip_by_value(act_probs_old, 1e-10, 1.0)))
                clipped_ratios = tf.clip_by_value(ratios, clip_value_min=1 - self.clip_value,
                                                  clip_value_max=1 + self.clip_value)
                loss_clip = tf.minimum(tf.multiply(self.gaes, ratios), tf.multiply(self.gaes, clipped_ratios))
                self.loss_clip = -tf.reduce_mean(loss_clip)

                # construct computation graph for loss of entropy bonus
                tech_entropy = -tf.reduce_sum(self.Policy.tech_probs *
                                              tf.log(tf.clip_by_value(self.Policy.tech_probs, 1e-10, 1.0)), axis=1)
                entropy = tech_entropy
                self.entropy = tf.reduce_mean(entropy, axis=0)  # mean of entropy of pi(obs)

                # construct computation graph for loss of value function
                v_preds = self.Policy.v_preds
                loss_vf = tf.squared_difference(self.rewards + self.gamma * self.v_preds_next, v_preds)
                self.loss_vf = tf.reduce_mean(loss_vf)

                # construct computation graph for loss
                self.total_loss = self.loss_clip + self.c_1 * self.loss_vf - self.c_2 * self.entropy
                self.sum_mean_returns = tf.summary.scalar('mean_return_dis', self.returns_sum / (self.proc_num + 0.0001))

            self.merged_dis = tf.summary.merge([self.sum_mean_returns])
            optimizer = tf.train.AdamOptimizer(learning_rate=self.adam_lr, epsilon=self.adam_epsilon)
            self.gradients = optimizer.compute_gradients(self.total_loss, var_list=pi_trainable)

            self.train_op = optimizer.minimize(self.total_loss, var_list=pi_trainable)
            self.train_value_op = optimizer.minimize(self.loss_vf, var_list=pi_trainable)

    def train(self, obs, tech_actions, gaes, rewards, v_preds_next):
        _, total_loss = self.sess.run([self.train_op, self.total_loss], feed_dict={self.Policy.obs: obs,
                                                                                   self.Old_Policy.obs: obs,
                                                                                   self.tech_actions: tech_actions,
                                                                                   self.rewards: rewards,
                                                                                   self.v_preds_next: v_preds_next,
                                                                                   self.gaes: gaes})
        return total_loss

    def train_value(self, obs, gaes, rewards, v_preds_next):
        _, value_loss = self.sess.run([self.train_value_op, self.loss_vf], feed_dict={self.Policy.obs: obs,
                                                                                      self.Old_Policy.obs: obs,
                                                                                      self.rewards: rewards,
                                                                                      self.v_preds_next: v_preds_next,
                                                                                      self.gaes: gaes})
        return value_loss

    def get_summary_dis(self):
        return self.sess.run(self.merged_dis)

    def assign_policy_parameters(self):
        # assign policy parameter values to old policy parameters
        return self.sess.run(self.assign_ops)

    def reset_mean_returns(self):
        self.sess.run(self.returns_sum.assign(0))
        self.sess.run(self.proc_num.assign(0))

    def get_gaes(self, rewards, v_preds, v_preds_next):
        deltas = [r_t + self.gamma * v_next - v for r_t, v_next, v in zip(rewards, v_preds_next, v_preds)]
        # calculate generative advantage estimator(lambda = 1), see ppo paper eq(11)
        gaes = copy.deepcopy(deltas)
        for t in reversed(range(len(gaes) - 1)):  # is T-1, where T is time step which run policy
            gaes[t] = gaes[t] + self.gamma * self.lamda * gaes[t + 1]
        return gaes

    def ppo_train_dis(self, observations, tech_actions, rewards, v_preds, v_preds_next,
                      gaes, returns, verbose=False):
        if verbose:
            print('PPO train now..........')

        # convert list to numpy array for feeding tf.placeholder
        observations = np.array(observations).astype(dtype=np.float32)
        tech_actions = np.array(tech_actions).astype(dtype=np.int32)
        gaes = np.array(gaes).astype(dtype=np.float32).reshape(-1)
        gaes = (gaes - gaes.mean()) / gaes.std()
        rewards = np.array(rewards).astype(dtype=np.float32).reshape(-1)
        v_preds_next = np.array(v_preds_next).astype(dtype=np.float32).reshape(-1)
        inp = [observations, tech_actions, gaes, rewards, v_preds_next]

        train_num = observations.shape[0]
        if train_num <= 0:
            return

        # self.assign_policy_parameters()
        # train
        # batch_size = max(observations.shape[0] // 10, self.batch_size)
        batch_size = min(train_num, self.batch_size)
        print('batch_size is:', batch_size)

        max_steps = train_num // batch_size + 1
        print('max_steps is:', max_steps)

        for epoch in range(self.epoch_num):
            for step in range(max_steps):
                # sample indices from [low, high)
                sample_indices = np.random.randint(low=0, high=train_num, size=batch_size)
                sampled_inp = [np.take(a=a, indices=sample_indices, axis=0) for a in inp]  # sample training data

                if self.restore_model and self.update_count < 3:
                    value_loss = self.train_value(obs=sampled_inp[0],
                                                  gaes=sampled_inp[2],
                                                  rewards=sampled_inp[3],
                                                  v_preds_next=sampled_inp[4])
                else:
                    total_loss = self.train(obs=sampled_inp[0],
                                            tech_actions=sampled_inp[1],
                                            gaes=sampled_inp[2],
                                            rewards=sampled_inp[3],
                                            v_preds_next=sampled_inp[4])
                if verbose:
                    print('total_loss:', total_loss)

        self.update_count += 1

        self.sess.run(self.returns_sum.assign_add(np.mean(returns)))
        self.sess.run(self.proc_num.assign_add(1))

        if verbose:
            print('PPO train end..........')
        return
