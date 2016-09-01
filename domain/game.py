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
            state = self._env.reset()

            for step in xrange(STEP):
                sleep(0.01)
                action_type = dqn.get_egreedy_action(state)
                next_state, reward, done = self._env.accept(action_type)
                dqn.perceive(state, action_type, reward, next_state, done)
                wx.CallAfter(self._house_frame.refresh, (next_state[0], next_state[1]))
                state = next_state

                if done:
                    break
