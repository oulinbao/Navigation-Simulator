
REWARD_DONE = 100
REWARD_ZERO = 0
REWARD_NOT_FINISHED = -100

COVERAGE_THRESHOLD = 1.0
NORMAL_STEP = 100


class RewardCalculator(object):

    def __init__(self, coverage_rate, repeat_rate, total_steps):
        self._coverage_rate = coverage_rate
        self._repeat_rate = repeat_rate
        self._total_steps = total_steps

    def calculate(self):
        # coverage_reward = REWARD_DONE if self._coverage_rate > COVERAGE_THRESHOLD else REWARD_ZERO
        coverage_reward = self._coverage_rate * REWARD_DONE
        repeat_reward = self._repeat_rate * REWARD_DONE
        # steps_reward = float(self._total_steps - NORMAL_STEP) / self._total_steps * REWARD_DONE

        print 'coverage rate %.2f and reward:%d, repeat rate %.2f and reward:%d' \
              % (self._coverage_rate, coverage_reward, self._repeat_rate, -repeat_reward)
        return coverage_reward - repeat_reward
