import wx
from time import sleep
from algrithm.dqn import DQN

EPISODE = 100000     # Episode limitation
STEP = 300          # Step limitation in an episode



class Game(object):
    def __init__(self, house_frame, env):
        self._house_frame = house_frame
        self._env = env

    def play(self):
        dqn = DQN()

        for episode in xrange(EPISODE):
            print 'start episode:', episode
            sleep(1)
            self._env.reset_target_pos()
            self.train_episode(dqn)
            dqn.save_train_params()

            sleep(1)
            if episode % 1 == 0:
                self.test_dqn(dqn)

    def train_episode(self, dqn):
        total_reward = 0
        state = self._env.reset()

        for step in xrange(STEP):
            action_type = dqn.get_egreedy_action(state)
            next_state, reward, done = self._env.accept(action_type)
            dqn.perceive(state, action_type, reward, next_state, done)

            position = (next_state[0], next_state[1])
            wx.CallAfter(self._house_frame.refresh, position, 'training...')
            sleep(0)
            state = next_state
            total_reward += reward

            if done:
                break

        print 'this episode total reward is %d' % total_reward

    def test_dqn(self, dqn):
        total_reward = 0
        state = self._env.reset()

        for step in xrange(STEP):
            action_type = dqn.get_action(state)
            next_state, reward, done = self._env.accept(action_type)
            dqn.perceive(state, action_type, reward, next_state, done)

            position = (next_state[0], next_state[1])
            wx.CallAfter(self._house_frame.refresh, position, 'testing...')
            sleep(0)
            state = next_state
            total_reward += reward

            if done:
                break

        print 'TEST!!! total reward is %d' % total_reward
