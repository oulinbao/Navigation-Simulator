from abc import ABCMeta, abstractmethod
from actiontype import ActionType
from reward import RewardCalculator, REWARD_ZERO
from domain.game import MAX_STEP


class Command(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self):
        raise NotImplementedError


class Action(Command):
    def __init__(self, house_map):
        self._house_map = house_map
        self._src_pos = self._house_map.robot.position
        self._robot = house_map.robot

    def _calc_reward(self, next_pos):
        if self._robot.action_count == MAX_STEP or self._house_map.is_all_covered():
            calculator = RewardCalculator(self._house_map.calculate_coverage_rate(),
                                          self._house_map.calculate_repeat_rate(),
                                          self._robot.action_count)
            return calculator.calculate()
        return REWARD_ZERO

    def _calc_stop_reward(self):
        # if self._robot.always_turn_around():
        #     return -10
        return -0.5

    def _calc_repeat_reward(self, pos):
        box = self._house_map.get_box(pos)
        if box.passed_count > 1:
            return -0.1
        return 0

    def _calc_hitwall_reward(self, next_pos):
        if self._src_pos == next_pos:
            return -100
        return 0

    def _move(self, action):
        next_box, next_pos = self._house_map.get_next_box(action)
        if not next_box.is_wall():
            self._house_map.record_footprint(next_pos)
            return next_pos
        else:
            # print 'hit wall'
            return self._src_pos

    def response(self, next_pos):
        return next_pos, self._calc_reward(next_pos) + self._calc_hitwall_reward(next_pos), \
            self._house_map.is_all_covered()


class MoveEast(Action):
    def __init__(self, house_map):
        Action.__init__(self, house_map)

    def execute(self):
        next_pos = self._move(ActionType.E)
        self._robot.position = next_pos
        self._robot.action_count += 1
        return self.response(next_pos)


class MoveWest(Action):
    def __init__(self, house_map):
        Action.__init__(self, house_map)

    def execute(self):
        next_pos = self._move(ActionType.W)
        self._robot.position = next_pos
        self._robot.action_count += 1
        return self.response(next_pos)


class MoveSouth(Action):
    def __init__(self, house_map):
        Action.__init__(self, house_map)

    def execute(self):
        next_pos = self._move(ActionType.S)
        self._robot.position = next_pos
        self._robot.action_count += 1
        return self.response(next_pos)


class MoveNorth(Action):
    def __init__(self, house_map):
        Action.__init__(self, house_map)

    def execute(self):
        next_pos = self._move(ActionType.N)
        self._robot.position = next_pos
        self._robot.action_count += 1
        return self.response(next_pos)
