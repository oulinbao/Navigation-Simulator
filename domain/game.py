import wx
from time import sleep
from direction import Direction
from algrithm.dqn import DQN

EPISODE = 10000     # Episode limitation
STEP = 1000          # Step limitation in an episode
TARGET_POS = [4, 30]
INIT_POSITION = [2, 2]
INIT_DIRECTION = Direction.EAST


class Game(object):
    def __init__(self, house_frame, env):
        self._house_frame = house_frame
        self._env = env

    def play(self):
        dqn = DQN()

        for episode in xrange(EPISODE):
            print 'start episode:', episode
            sleep(3)

            self.train_episode(dqn)
            dqn.save_train_params()

            if episode % 10 == 0:
                self.test_dqn(dqn)

    def train_episode(self, dqn):
        total_reward = 0
        state = self._env.reset()

        for step in xrange(STEP):
            sleep(0)
            action_type = dqn.get_egreedy_action(state)
            next_state, reward, done = self._env.accept(action_type)
            dqn.perceive(state, action_type, reward, next_state, done)

            position = (next_state[0], next_state[1])
            wx.CallAfter(self._house_frame.refresh, position, 'training...')
            state = next_state
            total_reward += reward

            if done:
                break

        print 'this episode total reward is %d' % total_reward

    def test_dqn(self, dqn):
        total_reward = 0
        state = self._env.reset()

        for step in xrange(STEP):
            sleep(0)
            action_type = dqn.get_action(state)
            next_state, reward, done = self._env.accept(action_type)
            dqn.perceive(state, action_type, reward, next_state, done)
            print state, action_type, reward, next_state, done

            position = (next_state[0], next_state[1])
            wx.CallAfter(self._house_frame.refresh, position, 'testing...')
            state = next_state
            total_reward += reward

            if done:
                break

        print 'TEST!!! total reward is %d' % total_reward