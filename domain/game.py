import wx
from time import sleep
from direction import Direction
from algrithm.dqn import DQN

EPISODE = 100000     # Episode limitation
MAX_STEP = 400          # Step limitation in an episode
INIT_POSITION = [3, 3]
INIT_DIRECTION = Direction.EAST


class Game(object):
    def __init__(self, house_frame, env):
        self._house_frame = house_frame
        self._env = env

    def play(self):
        dqn = DQN()

        for episode in xrange(EPISODE):
            print '\n*****start episode******:', episode
            sleep(2)
            self.train_episode(dqn, episode)
            dqn.save_train_params()

            sleep(1)
            if episode % 5 == 0:
                self.test_dqn(dqn)

    def train_episode(self, dqn, episode):
        total_reward = 0
        state = self._env.reset()

        for step in xrange(MAX_STEP):
            # if episode % 4 == 0:
            #     action_type = dqn.get_action_from_good_example(state[1])
            # else:
            action_type = dqn.get_egreedy_action(state)
            next_state, reward, done = self._env.accept(action_type)
            print 'step reward:', reward, ' total:', total_reward
            dqn.perceive(state, action_type, reward, next_state, done)

            wx.CallAfter(self._house_frame.refresh, 'training...')
            sleep(0.01)
            state = next_state
            total_reward += reward

            if done:
                print 'done!'
                break

        print '###############This episode total reward is %d' % total_reward

    def test_dqn(self, dqn):
        total_reward = 0
        state = self._env.reset()

        for step in xrange(MAX_STEP):
            action_type = dqn.get_action(state)
            next_state, reward, done = self._env.accept(action_type)
            print 'step reward:', reward, ' total:', total_reward
            dqn.perceive(state, action_type, reward, next_state, done)

            wx.CallAfter(self._house_frame.refresh, 'testing...')
            sleep(0.01)
            state = next_state
            total_reward += reward

            if done:
                break

        print 'TEST!!!!!! total reward is %d' % total_reward
