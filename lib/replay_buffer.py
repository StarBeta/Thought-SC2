import copy
import param as P


class Buffer(object):

    def __init__(self):
        self.observations = []
        self.tech_actions = []
        self.next_observations = []

        self.rewards = []
        self.values = []

        self.values_next = []
        self.gaes = []
        self.returns = []

    def reset(self):
        self.observations = []
        self.tech_actions = []
        self.next_observations = []

        self.rewards = []
        self.values = []

        self.values_next = []
        self.gaes = []
        self.returns = []

    def append(self, obs, tech_action, next_obs, reward, value, value_next):
        self.observations.append(obs)
        self.tech_actions.append(tech_action)
        self.next_observations.append(next_obs)

        self.rewards.append(reward)
        self.values.append(value)
        self.values_next.append(value_next)

    def add(self, buffer, add_return=True):

        gaes = self.get_gaes(buffer.rewards, buffer.values, buffer.values_next)
        #print('gaes:', gaes)
        self.observations += buffer.observations
        self.tech_actions += buffer.tech_actions
        self.next_observations += buffer.next_observations
        self.rewards += buffer.rewards
        self.values += buffer.values

        self.values_next += buffer.values_next
        self.gaes += gaes
        if add_return:
            self.returns += [self.get_returns(buffer.rewards)]

    def get_gaes(self, rewards, v_preds, v_preds_next):
        gamma = P.gamma
        lamda = P.lamda
        deltas = [r_t + gamma * v_next - v for r_t, v_next, v in zip(rewards, v_preds_next, v_preds)]
        # calculate generative advantage estimator(lambda = 1), see ppo paper eq(11)
        gaes = copy.deepcopy(deltas)
        for t in reversed(range(len(gaes) - 1)):  # is T-1, where T is time step which run policy
            gaes[t] = gaes[t] + gamma * lamda * gaes[t + 1]
        return gaes

    def get_returns(self, rewards):
        val = 0
        gamma = P.gamma
        for r in reversed(rewards):
            val = r + gamma * val

        return val
